Title: SD Basic - Encrypting Data
Subtitle: A key from a passphrase, encrypted fields, and a conversion that shows them decrypted.

**Read this first.** SD can encrypt a value for your program, but **SD does not look
after the key.** The key comes from a passphrase that a person knows, and the passphrase
and the salt live where your application puts them. SD has no vault, no recovery and no
administrator override: **a passphrase that is forgotten is data that is lost.** Keep
the passphrase and the salt safe, and prove that you can decrypt from a backup before you
rely on any of this.

SD folds case, so a program may be written in either case. Functions and codes are
shown here in lower case. *Italics* mark something you supply.

## Three functions that make a key

| | |
|---|---|
| `sdsalt()` | a fresh random salt: 24 characters, base64 for 16 bytes. Not a secret: keep it with the data |
| `sdkey(passphrase, salt)` | the 44 character base64 key that passphrase and salt always make |
| `sdrandkey()` | a random 256 bit key, 44 characters, for a program that will keep the key in a protected place |

Any account may use them. Nothing is gated, because they compute on what the program
already holds and give nothing away.

`sdkey()` uses argon2id with **2 passes and 64 MiB of memory**. Those two numbers are
part of the key's format: they are fixed, so a passphrase and salt that made a key today
make the same key on any later release. A call takes about a tenth of a second, so
**derive the key once, when the program starts, and not once for each field.**

They return the null string and set `status()` when they cannot:

| `status()` | |
|---|---|
| `10206` | the salt is not base64 for exactly 16 bytes (`sdkey` only) |
| `10207` | the passphrase is empty, or longer than 65,536 bytes (`sdkey` only) |

A failed call leaves nothing in the target: `x = sdkey('', salt)` makes `x` null.

## Encrypting one field with sdencrypt()

```
salt = sdsalt()                       ;* once, when the application is set up; kept with the data
key = sdkey(passphrase, salt)         ;* every run: the passphrase is typed, the salt is read back
cipher = sdencrypt('41250', key, 202)
plain = sddecrypt(cipher, key, 202)   ;* '41250', and status() is 0
```

Encoding **202** takes a 44 character base64 key, which is what `sdkey()` and
`sdrandkey()` make. Encoding 201 (hexadecimal) wants a 64 hex character key, which they
do not make. A wrong key gives the null string and `status()` **10201**; changing one
character of the cipher text does the same, because the value carries a check; a key of
the wrong length is **10204**; an empty value is **10200**. The cipher text of a value is
different every time it is made, so the same salary encrypts to two different strings.

## The XE conversion: show the field decrypted

`sdencrypt()` makes a program do the work at every place a field is read. The conversion
**`XE`** lets a dictionary item do it, so that `list customers name salary` shows `salary`
decrypted for a session that holds the key and shows what is stored for one that does not.

| code | |
|---|---|
| `XE` | the key called `default` |
| `XE;name` | the key called *name*: 1 to 31 letters, digits, dots, dashes or underscores, in either case |

`iconv(value, 'XE;salary')` encrypts and `oconv(value, 'XE;salary')` decrypts. A dictionary
item puts it in field 3: `D`, the field number, `XE;salary`, a heading, a format, `S`.

### The key ring

The conversion never holds a key. It names one, and the key is looked up in a **ring in
the memory of your own process**: it is set by `!keyset`, cleared by `!keyclear` or by
`logto`, and not handed to a phantom (a phantom that must decrypt calls `!keyset` itself).
The ring is never written to a disk, the audit trail or a `$como` file. It holds 16 keys.

```
call !keyset(name, key, id)     ;* id: the key's id (8 hex digits), or '' and status() 10213, 10204, 10203 or 10211
call !keyclear(name, n)         ;* n keys of that name removed; '*' empties the ring
call !keylist(list)             ;* a field per key: name, id and 1 if new values use it; never a key
```

A second key set under a name does not replace the first: the **newest encrypts**, and
the older ones stay to read what they made, so a key can be changed without losing the
data under the old one. `encrypt.key` is the same thing for a person at a terminal, and
**the passphrase is typed at a hidden prompt, never given as an argument:**

```
encrypt.key set salary kXz0pQ3b8mYw1sVt5aGfRA== confirm
encrypt.key list
encrypt.key clear salary
```

`set` takes the salt that `sdsalt()` made. **Use `confirm` the first time:** it asks for the
passphrase twice, because data encrypted under a mistyped passphrase cannot be read again.
`clear` with no name empties the ring. The verb applies no strength rule to the passphrase;
a long phrase of words is a better one than eight characters of every kind.

### What is stored

A value is the base64 of: a version byte (1), a 4 byte **key id** (the start of the SHA-256
of the key), a 24 byte nonce, and libsodium's secretbox (a 16 byte tag and the encrypted
bytes). It is printable and holds no field, value or subvalue mark. The id lets SD tell
*wrong key* from *not encrypted*. **The null string is not encrypted:** an empty field is
still empty, which also tells an observer that it is.

### What the conversion does when it cannot

Nothing is silent, and **nothing ever answers with the plaintext of an input**:

| `status()` | `oconv(value, 'XE;name')` | `iconv(value, 'XE;name')` |
|---|---|---|
| `10208` no such key in the ring | the stored value, unchanged | the **null string** |
| `10209` the name has keys, none made this value | the stored value | |
| `10210` the value is not an encrypted value | the value | |
| `10212` the check fails: changed or damaged | the stored value | |
| `2` a mistake in the code (`XEfoo`) | the value | the **null string** |

A `list` over a file with no key in the ring therefore shows the cipher text, not a blank.
An `iconv` with no key gives the null string: **test `status()` before you write it.**

## What a query does with an encrypted field

The stored value is cipher text everywhere SD looks at it, and only the final display
applies the conversion. So:

| | |
|---|---|
| `list`, `sort` (by another field) | shows the field decrypted, with the key; the stored value without it |
| `list` of a multivalued field | each value decrypted on its own line |
| `sort by` the field | sorts the **cipher text**, which is in no useful order |
| `with salary = "41250"` | **finds nothing, even with the key**: the literal is encrypted with a fresh nonce. `with salary = ""` does find the empty ones |
| `with` on the stored token | works (`with raw = "AQ..."`): you can look a known value up |
| `count`, `select` | count what is there; `with salary # ""` counts the filled fields |
| `total salary` | adds the cipher text, which is 0 |
| an I-type that uses the field (`salary * 2`) | an error: it works on the stored value |
| an I-type that decrypts: `oconv(raw, "XE;salary")` | decrypted, with the key |
| an index on the field | holds the **cipher text**; no plaintext reaches the disk |
| `copy` | moves the cipher text untouched, with no key in the ring |

If you must search or total an encrypted field, do it in a program that holds the key.

## A worked example

```
* once, at set-up: the salt is made and kept with the data
open 'settings' to s else stop
write sdsalt() on s, 'salt'

* every run
open 'settings' to s else stop
read salt from s, 'salt' else stop
crt 'Passphrase: ' :
input pw hidden
key = sdkey(pw, salt) ; pw = ''
if key = '' then stop 'bad salt'
call !keyset('salary', key, id) ; key = ''

open 'staff' to f else stop
x = iconv(new.salary, 'XE;salary')
if status() # 0 then stop 'not stored: no key'
rec = new.name : @fm : x                    ;* field 2 holds cipher text
write rec on f, new.id
execute 'list staff name salary'            ;* salary shows decrypted here
call !keyclear('*', n)
```

`pw = ''` and `key = ''` empty your own variables. SD wipes the C buffers it copies a passphrase
or key into; the strings your program held are freed, not wiped, so keep them short-lived.

## What this does not do

| | |
|---|---|
| a person with the key, or a program that holds it | sees everything |
| root, or anyone who can read the memory of the process | the ring is protected from swap and core dumps, not from a debugger |
| the length of a value, whether it is empty, the record id, the other fields | are not hidden |
| a passphrase kept in a file, a variable or a command line | is as safe as the file, the variable or the history |
| a forgotten passphrase or a lost salt | is lost data |
| the disk | is protected by the operating system, not by SD |

**Cost:** twenty thousand `oconv(value, 'XE')` calls take under a second on the test machine,
so a listing of a large file is not slowed noticeably. `sdkey()` is the one slow call.

Title: Encryption and the SDEXT interface
Subtitle: What libsodium provides, what an application can reach, and what SD does and does not do about keys.

SD Core for Linux links libsodium (`libsodium-dev`, installed as an ordinary
distribution package by the installer) rather than shipping its own copy.
Two things are built on it: the credential exchange that authenticates an
API login, and BASIC functions and a conversion that encrypt the data an
application chooses to encrypt.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case.

## The short version

**For credentials**, nothing needs configuring. Passwords are never stored. SD
keeps a SCRAM-SHA-256 verifier in the credential store, the API login proves
knowledge of the password without sending it, and the primitives behind that
exchange are the ones listed further down.

**For encrypting application data** there is a route, and it is the
application's. SD gives a program a way to make a key from a passphrase and to
encrypt a field with it, and a conversion that shows the field decrypted to a
session that holds the key. **SD does not keep the key, escrow it or recover
it.** A passphrase or a salt that is lost is data that is lost; no
administrator can recover it, and there is no setting that changes that. A site
that plans to encrypt fields has to decide where the passphrase lives before it
writes the application.

## Three layers, and what each one protects

| Layer | What it is | Protects against | Does not protect against |
|---|---|---|---|
| The disk | encryption of the volume the SD directories are on, by the operating system (LUKS, fscrypt). SD is unchanged. It has a page of its own in this set | a stolen or discarded disk; a backup copied off the machine | anyone logged in to the running system; root; a mounted volume |
| The program | `sdkey()` and `sdencrypt()` in an application | a copy of the SD files, a backup, a person with file access but not the key | the program itself, its variables, anyone who holds the key |
| The conversion | `XE` in a dictionary item, with the key held in a ring in the process | the same, and the field reads decrypted for a session that holds the key | the same, and root or a debugger on that process |

None of them hides the record id, the other fields, which values are empty or
how long a value is. The second and third are the application's; the first is
the machine's.

## What was removed

| | |
|---|---|
| The `encrypt.field` verb | Removed. It pointed at a program, `$CRYPTO`, which never existed in the GPL release, so the verb could not have worked in any build derived from it |
| `encrypt()` and `decrypt()` | Removed upstream in July 2024 and replaced by `sdencrypt()` and `sddecrypt()`. The old names do not compile |

## The functions an application uses

All of these are ordinary BASIC functions. **Any account may compile a call to
them: nothing is gated**, because they compute on data the program already holds
and give nothing away. The programmer's page for them, with a worked example, is
in the User set.

| Function | Result |
|---|---|
| `sdsalt()` | a fresh random salt, base64 for 16 bytes |
| `sdkey(passphrase, salt)` | a 44 character base64 key by argon2id |
| `sdrandkey()` | a random 256 bit key, 44 characters |
| `sdencrypt(data, key, 202)` · `sddecrypt(data, key, 202)` | libsodium's authenticated `secretbox`; 201 selects hexadecimal and wants a 64 character key, which the first three do not make |

**The argon2id limits are fixed: 2 passes and 64 MiB.** They are part of the
format of every key `sdkey()` has made. A later release that changed them would
make a different key from the same passphrase and salt, and everything encrypted
under the first would be lost, so they are written into the source as numbers
and held by a build-time check. The cost is about a tenth of a second and 64 MiB
of memory for each call; an application derives the key once per run.

`status()` after a failure: **10206** the salt is not base64 for 16 bytes,
**10207** the passphrase is empty or over 65,536 bytes, **10204** a key of the
wrong length, **10201** a wrong key or a damaged value.

### Before this existed

`sdencrypt('The quick brown fox', 'secretkey', 202)` returns nothing and sets
`status()` to **10204**: a passphrase is not a key. Until the three functions
above the only way to turn a passphrase into a key was `sdext()`'s
`SD_KEYFROMPW`, which is internal-only, so an ordinary program could not obtain
a key these functions accepted. That is no longer so, and `10204` for a
passphrase passed straight in is still the answer.

## The XE conversion and the key ring

A dictionary item names a key and never holds one: field 3 is `XE` or
`XE;name`. The key is looked up in a **ring in the memory of the session's own
process**, put there by `!keyset` (a subroutine a program calls) or by the
`encrypt.key` verb (a person, at a hidden prompt), and taken out by `!keyclear`.

- **Held in memory only.** The ring is `sodium_malloc` memory: locked against
  swap and left out of a core dump where the system allows it, guarded by pages
  that fault, protected against all access between uses and zeroed when
  released. It is never written to a file, the audit trail, the error log or
  `$como`.
- **Cleared** at `logto` (going in and coming back), at sign-off, and by
  `!keyclear`. **Not handed to a phantom**: a phantom starts with an empty ring.
- **16 keys**, each under a name of 1 to 31 letters, digits, dots, dashes or
  underscores. The newest key of a name encrypts; the older ones stay to read
  what they made, which is how a key is changed.
- **Audited by name only:** `encrypt.key set` and `encrypt.key clear` write the
  event and the key name to the audit trail. `!keyset` from a program writes
  nothing.
- The verb asks for no privilege and affects only the process that runs it.

A value is base64 of a version byte, a 4 byte key id, a 24 byte nonce and the
`secretbox`; it is printable and holds no mark character. If there is no key the
session sees the stored cipher text, never a blank, and an input conversion with
no key gives the null string, never the plaintext. The statuses are **10208**
(no key of that name), **10209** (the name's keys did not make the value),
**10210** (not an encrypted value) and **10212** (the value has been changed).

**What a query does with such a field is the application designer's to know:**
`sort by` sorts the cipher text, `with field = "value"` cannot match (the literal
is encrypted with a fresh nonce), `total` adds cipher text, an index holds cipher
text and no plaintext reaches the disk, and `copy` moves the stored value. The
User page lists each.

**`encrypt.key set` refuses a passphrase of fewer than 12 characters** (since 30
October 2026; message 11994), after it has seen that the two typed copies match.
That is its only rule. The rule for SD passwords is not applied, because this is
not an SD password: nothing is stored or compared. `sdkey()`, the function a
program calls, is unchanged and takes any passphrase that is not empty, so a site
that wants a stricter or a looser rule writes it into the application that asks
for the passphrase. A long phrase of words is a better passphrase than eight
characters of every kind.

## The SDEXT interface

`sdext()` is the internal entry point to the cryptographic primitives.

```
rtnval = sdext(arg, isargmv, key)
```

`key` selects the operation, `arg` carries the arguments and `isargmv` says
whether `arg` holds several values rather than one.

**It cannot be called from an application.** `sdext` is in the compiler's
internal function table, so an ordinary account does not merely get refused. It
gets a misleading error: an unknown function is read as a matrix reference, so
the complaint is about a `dim` statement the program does not contain, reported
at the last line rather than at the call. That behaviour is covered by
[SD Basic - Restricted Commands](10-sd-basic-restricted-commands.html) in this
set. `$internal` needs both halves: the compiler tests for internal mode **and**
for the administrator flag.

### The keys

Every binary value is base64, because the interface carries NUL-terminated
strings and a raw 32-byte digest would contain a mark character about one time
in nine. The argument buffers are zeroed when a call ends.

| Key | Value | Arguments | Result |
|---|---|---|---|
| `SDEXT_TestIt` | 1 | any | Prints each argument and returns a count. A diagnostic |
| `SD_SALT` | 100 | none | A fresh salt, base64 |
| `SD_KEYFROMPW` | 101 | password, salt | A 256-bit key derived from the password. A salt that is not 16 bytes is refused (10206) |
| `SD_EUID_SET` | 102 | user name | Sets the process effective user and group |
| `SD_EUID_RESTORE` | 103 | none | Restores what they were on entry |
| `SD_SHA256` | 104 | one | SHA-256 of the argument |
| `SD_HMACSHA256` | 105 | base64 key, text message | HMAC-SHA256 |
| `SD_PBKDF2` | 106 | password, salt, iterations, length | Derived key |
| `SD_RANDBYTES` | 107 | count | Random bytes |
| `SD_XORBYTES` | 108 | two equal-length values | Their exclusive-or |
| `SD_CTEQUAL` | 109 | two values | `1` or `0`, compared in constant time |
| `SD_TLS_CBIND` | 110 | none | This session's TLS channel binding, as the `c=` value its SCRAM login must carry; empty when the session is not TLS |
| `SD_KEYRING` | 120 | `set` name key · `clear` name · `list` | The key ring of the XE conversion: the key id, the number removed, or one field per key. Reached only through `!keyset`, `!keyclear` and `!keylist` |

`SD_CTEQUAL` reports a malformed argument as an error rather than as `0`,
because by the time the login path compares these values both sides are the
server's own: a decode failure there is a defect, not a wrong password. A
caller deciding whether to admit a login must still treat the error as a
refusal.

**`SD_EUID_SET` and `SD_EUID_RESTORE` are load-bearing on this port, not
dormant.** They call the real POSIX identity functions (`sdext_eguid.c`), and
`logto` uses them directly: `SD_EUID_SET` also reloads the caller's
supplementary Linux group membership on the way in. `!EUID_SET('sdsys', ...)` is
also how `cproc` drops back to `sdsys`'s own identity after a privileged step.

### What uses it

The shipped programs that call `sdext()` are `apisrvr`, `cred_set`,
`cred_verify`, `sd_get_salt`, `sd_key_from_pw`, `sdclient`, `euid_set`,
`euid_restore` and the three key ring subroutines `keyring_set`, `keyring_clear`
and `keyring_list`. The last three are catalogued for general use as `!keyset`,
`!keyclear` and `!keylist`, so an application reaches the ring without reaching
`sdext()`.

## Two constants that are not SDEXT keys

`SD_ENCODEHX` (201) and `SD_ENCODE64` (202) are defined alongside the SDEXT
keys and are easily mistaken for them. They are not keys and `sdext()` does not
implement them: passing either as a key returns a key error. They are the third
argument to `sdencrypt()` and `sddecrypt()`.

Title: SDNet
Subtitle: The NET switch and the server definitions: what is in place for files on another SD server, and what is not there yet.

SDNet is the name for opening a file that lives on **another SD server** and using
it with `READ`, `WRITE`, `SELECT` and `LIST` as if it were local. **This release
has the first slice only: the permission and the list of servers. Nothing in it
connects to anything, and no remote file can be opened.** The switch and the
definitions are in place so that the work that follows has something to stand on,
and so that you can see, and set, what it will be allowed to use.

An earlier SDNet was removed on 9 September 2026 (a `server;file` VOC entry over
port 4245, with each server's password in `sd.conf`, which any local user could
read). **This is not that.** Nothing from it is back: there is no `;` in a path, no
port 4245 and no password in any file.

## What SDNet is planned to be

Planned, not built yet:

- **Files on another SD server, read only first.** Writing would come later and
  only for a server that SDSYS marks `write`.
- **The same channel as the API.** The connection would be the target server's
  own API port, TLS 1.3 with the SCRAM login bound to the TLS session, and no
  new listener. A full SD Core listens for the API on 4247; a Solo on 4249.
- **Delivered off, and loosened by SDSYS.** The switch is off for every account,
  the list of accounts allowed to use a server is empty, and a server is
  `read` unless SDSYS says otherwise. SDSYS turns each on, one account and one
  server at a time.

## What is in this slice

| | |
|---|---|
| the **NET switch** | `modify.account` *name* `net-on` / `net-off`, and `net-on` in `create.account user`. See [Accounts and Security](01-accounts-and-security.html#the-net-switch-net-on-and-net-off) |
| the **server definitions** | one file, `netservers`, in the SDSYS directory |
| **`set.server`** | adds a definition, or replaces one |
| **`delete.server`** | removes one |
| **`list.servers`** | shows them |

**The three verbs are SDSYS's.** They are in SDSYS's VOC and in no other account's,
and each one also stops with "Command requires administrator privileges" for
anyone who is not the administrator. Commands are shown here in lower case.

### What does not exist yet

- **The connection.** No verb, statement or program in SD opens a socket to a
  server defined here. A definition is a record on disk and nothing reads it
  but these three verbs.
- **Confirming the key hash.** `set.server` cannot connect, so it cannot show you
  the hash the server presents and ask you to confirm it. You type the pin, and
  nothing checks it. This slice has no command that prints a server's key hash,
  so it has to come from the other server's administrator.
- **Credentials.** No user name or password for the remote account is asked
  for or stored anywhere.
- **Remote files.** There is no VOC pointer to a remote file, and the NET switch
  and the *accounts* list are not consulted by anything yet.
- **`NETFILES`** in `sd.conf` is still accepted and still does nothing (see
  [SD Admin Configuration](07-sd-admin-configuration.html)).

## The security model

**Nothing a user can type chooses a host.** The only machines SD will ever be
asked to call are the ones SDSYS has written down, and only SDSYS can write them:
the file is replaced only by these verbs, and the verbs are SDSYS's. A program
cannot define, change or point at a server. Two things must then both be true
before an account could use one: it has the NET switch (off by default), and it
is named in that server's *accounts* list (empty by default). Neither is a
judgement that nobody should have the capability; each is a decision about who
decides, and it is yours.

**The file holds no secret, and must never hold one.** A definition is a name, an
address, a port, the name of an account, and the hash of a *public* key. The file
is readable by every user (mode 644) on purpose, and only the `sdsys` user writes
it. When credentials exist, they will be kept somewhere else.

## The file: `netservers`

It is a plain text file in the SDSYS directory (`/usr/local/sdsys/netservers` on a
standard install), one definition to a line, at most **ten**:

```
name|host|port|account|pin|mode|accounts|created
```

It is always written **whole**: the new text goes to `netservers.new` beside it
and is renamed over the old file, so it is never half written. A session that
changes it holds a lock for the length of the change (a second administrator
session that tries meanwhile is told to try again). The mode of the new file is
644 whoever asked, and the file is owned by whoever ran the session, which is
`sdsys`.

| field | rule |
|---|---|
| **name** | a lower case letter, then up to 15 lower case letters or digits. Capitals typed are converted |
| **host** | 1 to 253 letters, digits, dots, hyphens or colons: a DNS name, an IPv4 address or an IPv6 literal. It does not start with a hyphen or a dot. Capitals are converted |
| **port** | a whole number from 1 to 65535: the port **of the server you are defining**, chosen when you define it (4247 for a full SD Core, 4249 for a Solo). SD does not insist on either number. `04249` is stored as 4249 |
| **account** | the account to enter on the remote server: 1 to 32 letters, digits, dots, underscores or hyphens. Kept as typed, because the other server's names are its own |
| **pin** | the SHA-256 hash of the server's public key: exactly 64 hexadecimal digits, stored in lower case. A new certificate with the same key keeps the same pin |
| **mode** | `read` or `write`. `read` unless `write` is given. What a program may do with the server's files, once it can open them |
| **accounts** | the **local** accounts that may use the server: registered account names separated by commas, no spaces, no empty name, at most 2000 characters, each listed once. **Empty means nobody**, and empty is what you get unless you list some |
| **created** | the date the definition was made, `yyyy-mm-dd`. Set by SD |

No field may hold a vertical bar, a control character or a character above the
ASCII range, so a line cannot be made into something else.

## Defining a server: `set.server`

```
set.server name host port account pin {read | write} {accounts a,b,c} {no.query}
```

Everything after the pin is optional and may come in either order. Capitals in the
name, host, pin, mode and account list are converted. Words are split at spaces, so
nothing can be quoted.

```
:set.server solo2 192.168.1.40 4249 sduser 5f29e23fd38c423996bef4450ba56aa16e11f06e926ddb0828b5d9649064b9b9
Server solo2 (192.168.1.40:4249) is defined
No account is listed, so no account may use server solo2 yet.  Set it again with accounts, and give each account the NET gate (modify.account name net-on)
```

(The pin above is an example value, not a real server's.) The last line is there
on purpose: a definition with an empty *accounts* list is complete and harmless,
and nobody may use it. To name accounts, give them with the definition:

```
:set.server solo2 192.168.1.40 4249 sduser 5f29e23fd38c423996bef4450ba56aa16e11f06e926ddb0828b5d9649064b9b9 read accounts fred,jane
Server solo2 is already defined (192.168.1.40:4249).  Replace it (y/<n>)?y
Server solo2 (192.168.1.40:4249) was replaced
```

Fewer than six words (the verb, then name, host, port, account and pin) print the
usage and a reminder of where the pin comes from, and stop:

```
:set.server solo2 192.168.1.40 4249 sduser
Usage: set.server name host port account pin {read | write} {accounts a,b,c} {no.query}
The pin is the SHA-256 hash of the server's public key, 64 hexadecimal digits, from the other server's administrator.  Nothing connects to the server yet, so the hash cannot be shown here for confirmation.
```

**Every field is checked before anything is written, and each field that is wrong
gets a message of its own**, so one run shows all of them:

```
:set.server solo2 -bad 99999 sduser abc
Host -bad is not valid: 1 to 253 letters, digits, dots, hyphens or colons, not starting with a hyphen or a dot
Port 99999 is not valid: a whole number from 1 to 65535
The pin is not valid: it must be exactly 64 hexadecimal digits
```

The other refusals have messages of their own: a name that is not valid, a remote
account that is not valid, a mode that is not `read` or `write`, an accounts list
that is not valid, and "Account *x* in the accounts list is not a registered
account" for a name that is not in the register (SDSYS is never in it, so it cannot
be listed). A refusal writes nothing.

**Replacing.** A name that is already defined is replaced, after the question
above, which defaults to no (and so does an input that ends). `no.query` goes
ahead without asking. **A replacement is the whole definition, not a merge:**
the accounts list is whatever the new command gives, so give it again. With ten
servers already defined, a new name is refused until you delete one.

## Removing a server: `delete.server`

```
delete.server name
```

```
:delete.server solo2
Server solo2 was deleted
```

It does not ask: a definition is one line and `set.server` makes it again. A name
that is not defined gets "No server is defined with the name solo2".

## Showing them: `list.servers`

```
list.servers {name}
```

One line for each server: the name, *host*:*port*, the remote account and the mode
as *account*/*mode*, the pin cut to its first sixteen digits, and the local accounts
allowed (the word `none` when there are none).

```
:list.servers
solo2  192.168.1.40:4249  sduser/read  5f29e23fd38c4239...  fred,jane
hq  hq.example.com:4247  reports/read  90b7bd01319812c2...  none
```

With a name it shows only that server, with the **whole** pin, and the date it was
defined:

```
:list.servers hq
hq  hq.example.com:4247  reports/read  90b7bd01319812c22b8a37b3170d3026955a4e640bb9b216acf9db468475bc06  none
Defined on 2026-10-17
```

With none defined, on its own it says "No servers are defined". It changes nothing and takes no
lock. If the file holds a line these verbs did not write, all three stop and say
which line, "The server definitions file has a line that is not a definition",
without changing anything; correct the file at the operating system.

## What is audited

Defining and deleting are written to the audit trail, in lower case:

```
set.server name=solo2 host=192.168.1.40 port=4249 mode=read replaced=no
delete.server name=solo2 host=192.168.1.40 port=4249
```

The pin is not in the line (it is not secret, only long). A refusal, a declined
replacement and `list.servers` write nothing. Giving or taking the NET switch is
audited like every other `modify.account` word (`modify.account net-on
account=fred`).

## See also

[Accounts and Security](01-accounts-and-security.html) for the NET switch beside the
other per-account switches. [Remote Access and the Machine](05-remote-access-and-the-machine.html)
for the API listener a server's port refers to.

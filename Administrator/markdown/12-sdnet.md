Title: SDNet
Subtitle: The NET switch and the server definitions: what is in place for files on another SD server, and what is not there yet.

SDNet is the name for opening a file that lives on **another SD server** and using
it with `READ`, `WRITE`, `SELECT` and `LIST` as if it were local. **This release
has the first slices only: the permission, the list of servers, and one
connection that `set.server` can make so that it can show you a server's key hash.
Nothing else connects to anything, and no remote file can be opened.** The switch and the
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

- **The connection, apart from one.** The only thing in SD that opens a socket to
  a server is `set.server` with the word `connect`, once, for the handshake
  alone (see below). No verb, statement or program opens a socket to a server
  *defined* here. A definition is a record on disk and nothing reads it but
  these three verbs.
- **A check that a typed pin is right.** When you type the 64 digits, nothing
  connects and nothing checks them; use `connect` to have the server's own hash
  shown to you. And nothing yet checks a pin on a later connection, because
  there is no later connection.
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
cannot define, change or point at a server. (The one connection that exists
today is SDSYS's own: `set.server ... connect` dials the host SDSYS typed, for a
handshake, and sends nothing.) Two things must then both be true
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
set.server name host port account {pin | connect} {read | write} {accounts a,b,c} {no.query}
```

The fifth word is **either the pin, 64 hexadecimal digits, typed (no connection is
made), or the word `connect`** (SD fetches the hash and asks you to confirm it:
see "Getting the pin by connecting" below). Everything after it is optional and may
come in either order. `no.query` skips the question about replacing a definition,
**and never the question about trusting a key**. Capitals in the name, host, pin,
mode and account list are converted. Words are split at spaces, so nothing can be
quoted.

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

Fewer than six words (the verb, then name, host, port, account and pin or
`connect`) print the usage and a reminder of where the pin comes from, and stop:

```
:set.server solo2 192.168.1.40 4249 sduser
Usage: set.server name host port account {pin | connect} {read | write} {accounts a,b,c} {no.query}
The pin is the server's public key hash: 64 hexadecimal digits from its administrator (nothing is dialled), or the word connect to see the hash the server presents and confirm it.  no.query never skips that question.
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
ahead without asking **that** question, and no other (see the next section).
**A replacement is the whole definition, not a merge:**
the accounts list is whatever the new command gives, so give it again. With ten
servers already defined, a new name is refused until you delete one.

### Getting the pin by connecting: `set.server ... connect`

Typing 64 digits from a message is how a pin gets mistyped, or swapped for the
wrong one. Give the word `connect` in place of the pin and SD fetches the hash
itself, shows it to you, and writes the definition only if you say the hash is
the right one:

```
set.server name host port account connect {read | write} {accounts a,b,c} {no.query}
```

`connect` may be in any case. This is what happens, in this order:

1. **Every other field is checked first**, exactly as above (the pin check is
   the only one left out, because there is no pin yet). **Nothing is dialled for
   a definition that would be refused.**
2. The definitions are read and the limit of ten is checked. If the name is
   already defined and `no.query` was not given, the replacement question is
   asked **before any connection**, so answering no (or ending the input)
   dials nothing.
3. SD opens a **TLS connection to *host*:*port*, waiting at most 5 seconds**, and
   reads the SHA-256 hash of the public key the server presented. It closes the
   connection at once. **It is a handshake only: nothing is sent to the server.**
4. SD shows the hash and asks you to trust it. The answer defaults to no, and so
   does an input that ends.
5. On **y** the definition is written with that hash as its pin. On **n** nothing
   is written.

```
:set.server hq hq.example.com 4247 reports connect read accounts fred
Connected to hq.example.com:4247 (a TLS handshake only: nothing was sent).  The server presented a public key with this hash:
90b7bd01319812c22b8a37b3170d3026955a4e640bb9b216acf9db468475bc06
Compare it with the hash the administrator of that server gives you, by a way that does not use this network.  If it differs, answer n: something may be standing between this server and that one.
Trust this key (y/<n>)?y
Server hq (hq.example.com:4247) is defined
```

(The hash above is an example value, not a real server's. The hash is printed
alone on its line, in lower case, so it can be copied.) Answering n:

```
Trust this key (y/<n>)?n
The key was not trusted.  Nothing was written: server hq is as it was
```

**THE KEY QUESTION IS ALWAYS ASKED. `no.query` does not skip it.** `no.query` only
skips the question about replacing a definition that exists. An administrator
who scripts `set.server` with `no.query` and `connect` still has to answer
whether the hash is the right one, because that answer is the whole point of
`connect`: with no one to compare, the pin would be whatever answered the call,
and that is no check at all. A replacement with `connect` therefore asks two
questions when `no.query` is absent (replace, then trust) and one when it is
present (trust). When the input ends before an answer, the answer is no.

**Why you compare, and what to compare with.** SD does not check the server's
certificate against anything here: it has nothing to check it against, which is
what the pin is for. So the connection can tell you what key *something* at that
address holds, but not that the something is the server you meant. If another
machine were standing between the two (or the address were wrong), the hash
would be that machine's. **Compare the hash with one you get another way: ask the
administrator of that server, by telephone or in person or by a channel you
already trust, and not over the network this connection used.**

**What the hash is.** It is the SHA-256 of the server's **public key** (the
certificate's SubjectPublicKeyInfo, DER encoded), shown as 64 lower case hex
digits. It is not the hash of the certificate. A certificate that is renewed over
the **same key** therefore has the same hash, and a pin does not go stale at a
renewal; a new key is a new hash and the pin has to be set again.

**How the other administrator gets the hash.** The administrator of the server
being defined asks that server for it: run as SDSYS, `settings.report` shows a
line `public key sha256: ` followed by the 64 digits in its `[api]` section, and
the same line comes from the privileged helper on its own:

```
sudo /usr/local/sbin/sd-elevate tls-key
```

If that server has not taken a TLS connection yet the line says
`certificate: not yet generated` (the file is made by the first connection). The
command reads only the public key; the private key in the same file is never
read into the output. It takes no argument and no path.

The same figure can be worked out by hand with `openssl`, with these two
commands run as a pipeline, which is also how to check that `tls-key` and the
connection agree:

```
sudo sh -c 'openssl x509 -pubkey -noout -in /etc/sd-tls/api.pem | openssl pkey -pubin -outform DER | openssl dgst -sha256'
```

(`sudo`: the file also holds the server's private key, so only root can read it.
The `sudo sh -c` form is used so that the pipe runs as root; run bare, the
first `openssl` would be refused.) The 64 hexadecimal digits at the end of the
output are the hash, and they should match what `set.server` showed. Depending on
the version, `openssl` puts a short label such as `(stdin)= ` in front of the digits;
the label is not part of the hash.

What was and was not confirmed about that command, so you can weigh it:

- **Confirmed from the source:** `/etc/sd-tls/api.pem` is where an SD Core server
  keeps its API identity (the certificate and its private key): the file is
  `api.pem` in a directory named `sd-tls` inside the directory that holds
  `sd.conf`, which is normally `/etc`; `sd-elevate
  tls-show` reads the same file. The hash SD shows is computed from the DER
  encoding of the certificate's public key, which is what the pipeline hashes.
- **Confirmed by test:** `sd-elevate tls-key` gives the same figure as an
  independent computation (the key's DER bytes hashed in Python) on a test
  certificate, and the figure `set.server ... connect` shows for a local TLS 1.3 test
  server equals the same computation.
- **Not confirmed:** the pipeline has not been run against a live SD server and its
  output compared with what `set.server ... connect` shows. They should agree,
  and if they do not, trust neither until you know why. The file is made by the
  API's first TLS connection, so a server that has never taken one has no
  `api.pem` yet. Where the identity of a Solo server is kept was not checked, and
  a server with a different `sd.conf` directory has its `sd-tls` there.

**When it does not work, nothing is written.** There is a message for each case:

| you see | meaning |
|---|---|
| `Cannot connect to host:port (status n, os error m).  Nothing was written` | the connection was not made: nothing is listening there, the address is wrong, or the 5 seconds passed (the operating system's error for a timeout, 110, is what is expected) |
| `The TLS handshake with host:port did not complete.  Is that the API port of an SD server?  Nothing was written` | something answered, but it did not complete a TLS handshake: most likely the port is not an SD server's API port |
| `host:port completed the handshake but gave no public key hash.  Nothing was written` | a TLS session was made but no hash could be read from it |

The first two are told apart by the operating system's error number, which is
zero for a handshake that failed after the connection was made. That is read off
the source and has not been tried against a closed port, a port that is not TLS
and an address that does not answer.

**One thing to know about the lock.** The definitions are locked from the time
they are read until the answer is acted on, which includes the connection (up to
5 seconds) and the time you take to answer. A second administrator session that
changes the definitions meanwhile is told to try again. The lock is so that the
definition cannot change between the confirmation and the write.

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
set.server name=solo2 host=192.168.1.40 port=4249 mode=read replaced=no pin=typed
set.server name=hq host=hq.example.com port=4247 mode=read replaced=no pin=confirmed
delete.server name=solo2 host=192.168.1.40 port=4249
```

The last word of a `set.server` line says how the pin was obtained: `pin=typed`
for 64 digits typed in the command, `pin=confirmed` for a hash that SD fetched with
`connect` and SDSYS answered y to. The pin itself is not in the line (it is not
secret, only long). A refusal, a declined replacement, a key that was not trusted,
a connection that failed and `list.servers` write nothing. Giving or taking the NET switch is
audited like every other `modify.account` word (`modify.account net-on
account=fred`).

## See also

[Accounts and Security](01-accounts-and-security.html) for the NET switch beside the
other per-account switches. [Remote Access and the Machine](05-remote-access-and-the-machine.html)
for the API listener a server's port refers to.

Title: SDNet: Servers
Subtitle: Defining a server, removing it, and listing the servers.

This page continues [SDNet](12-sdnet.html).

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
3. SD opens a **TLS connection to *host*:*port*, waiting at most `NETWAIT` seconds (5
   unless `sd.conf` says otherwise; see "The two waits")**, and
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

What that command relies on:

- `/etc/sd-tls/api.pem` is where an SD Core server keeps its API identity (the
  certificate and its private key): the file is `api.pem` in a directory named
  `sd-tls` inside the directory that holds `sd.conf`, which is normally `/etc`;
  `sd-elevate tls-show` reads the same file. The hash SD shows is computed from the
  DER encoding of the certificate's public key, which is what the pipeline hashes,
  and `sd-elevate tls-key` gives the same figure.
- The figure the pipeline gives and the figure `set.server ... connect` shows
  should agree. If they do not, trust neither until you know why.
- The file is made by the API's first TLS connection, so a server that has never
  taken one has no `api.pem` yet. A server with a different `sd.conf` directory has
  its `sd-tls` there. Where the identity of a Solo server is kept is not covered
  here.

**When it does not work, nothing is written.** There is a message for each case:

| you see | meaning |
|---|---|
| `Cannot connect to host:port (status n, os error m).  Nothing was written` | the connection was not made: nothing is listening there, the address is wrong, or `NETWAIT` seconds passed (the operating system's error for a timeout, 110, is what is expected) |
| `The TLS handshake with host:port did not complete.  Is that the API port of an SD server?  Nothing was written` | something answered, but it did not complete a TLS handshake: most likely the port is not an SD server's API port |
| `host:port completed the handshake but gave no public key hash.  Nothing was written` | a TLS session was made but no hash could be read from it |

The first two are told apart by the operating system's error number, which is
zero for a handshake that failed after the connection was made.

**One thing to know about the lock.** The definitions are locked from the time
they are read until the answer is acted on, which includes the connection (up to
`NETWAIT` seconds, 5 unless changed) and the time you take to answer. A second administrator session that
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

## Continued in

[SDNet: Your Login on a Server](12b-sdnet-logins.html) — set.netlogin,
delete.netlogin and the helper that keeps the credentials.

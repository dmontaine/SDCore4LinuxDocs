Title: SDNet: The Two Waits and What Is Audited
Subtitle: NETWAIT and NETREPLY, and the audit trail of SDNet.

This page continues [SDNet: Writing and
Locking](12e-sdnet-writing-and-locking.html).

## The two waits: `NETWAIT` and `NETREPLY`

Two settings in `sd.conf` (and readable with `config('NETWAIT')` and `config('NETREPLY')`,
listed by `config`) say how long SD waits on another server. Both are in **seconds, 1 to
3600**, and both are per computer, not per server definition:

| setting | what it bounds | default |
|---|---|---|
| `NETWAIT` | the connection: `set.server ... connect`, `set.netlogin`, and the first use of a defined server by an `OPEN` of a remote file. **Each of the two steps of making it has this long: the TCP connect, then the TLS handshake** | 5 |
| `NETREPLY` | each wait for a reply from the server once connected, in the login and in every request, **whatever the server has sent meanwhile** (the TLS session tickets, or half of a record, do not use the wait up) | 30 |

A server that is slower than `NETREPLY` is treated as lost, as it always was (the 30 seconds
were fixed in the programs); **a changing request that gets no answer is never sent again**
whatever the setting is. A `CLEARFILE` waits for the longer of five minutes and `NETREPLY`,
because a big file takes longer than a reply bound. The login exchange of `set.netlogin`
keeps its own 15 seconds for each packet. **A zero is refused**, and SD does not start with
`NETWAIT=0` or `NETREPLY=0` in `sd.conf` (openQM reads zero as "wait for ever"; here
that is never what an administrator of a pinned peer wants). **A value that is too large is
refused whatever it looks like in 16 bits**: `NETWAIT=65541` is refused and SD does not start
(`NETWAIT` and `NETREPLY` are 32 bit values; `PWDELAY` and `DHCACHE` are read as 16 bit values
and wrap). The names are eight characters
or fewer because `config()` reads no longer one. openQM's `NETDELAY`, which keeps a
connection open after the last file is closed, is not this and does not exist in SD.

**A reply that cannot be true.** The client reads the length a reply announces before it reads
the reply. A server that announces less than the ten bytes of its own header, or more than the
largest string SD can hold (a little over a gigabyte), is treated as a lost connection at once:
nothing of it is read, a changing request answers 11509 as for any lost reply, and the
connection is dropped. Nothing is refused that a real record could
need: the ceiling is the size of the largest record. **The ceiling applies once the login is
over.** The login exchange itself has no ceiling on the length a reply announces (only the test
for less than ten bytes), so a server whose key you have pinned, and which has turned hostile,
can still announce a large length in a login reply and send slowly, for `NETREPLY` seconds a
read; the pin is what you trust it with.

**How the limits apply.** With `NETWAIT=2` and a listener that never answers,
`set.server ... connect`, `set.netlogin` and the connection that a remote file's client makes
each give up in about two seconds more than a refused connection costs. With `NETREPLY=3`, a
server that sent its acknowledgement byte, read the first login message and then said nothing
is given up on in about three seconds.

A server that completes the TLS handshake and then sends nothing at all, or that stops in the
middle of a TLS record, is waited for no longer than the caller's limit: the wait is on the
connection, for the time that is *left* of the limit, so the session tickets a TLS 1.3 server
sends after the handshake, and a half record, cost what they have used and no more. With
`NETREPLY=3` and `NETWAIT=2`, the time a caller waits is:

| the server | the caller waits |
|---|---|
| completes the handshake, never sends the acknowledgement byte | 3.0 s |
| accepts the connection and never answers the TLS hello (`NETWAIT=2`) | 2.0 s |
| sends the acknowledgement byte as half of a TLS record | 3.0 s |
| answers the first login message with half of a TLS record | 3.1 s |
| answers a request after 1.5 s (a slow server inside the limit) | 1.5 s, and the record is read |

What the caller sees is what it sees for any lost connection: `set.netlogin` and the login of
an `OPEN` say "No acknowledgement from host:port at the start of the session", "No reply from
host:port during the login" or "The TLS handshake with host:port did not complete"; a request
that was sent and got no answer is message 11497 (message 11509 for a change, and **a change
that got no answer is never sent again**). A reply that stops in the *middle of its body* is
the same lost connection as a reply that never started: message 11497, and the connection is
dropped. A server that sends a little at a time and never stops is still waited for one read at
a time; the limit is for each read, not for a whole reply.

`open.socket` takes the number of seconds to wait for the connection as its fourth argument
(`NETWAIT` for every SDNet caller); see the User set's page on sockets.

## What is audited

Defining and deleting are written to the audit trail, in lower case:

```
set.server name=solo2 host=192.168.1.40 port=4249 mode=read replaced=no pin=typed
set.server name=hq host=hq.example.com port=4247 mode=read replaced=no pin=confirmed
delete.server name=solo2 host=192.168.1.40 port=4249
set.netlogin server=hq remote=reports
delete.netlogin server=hq
```

The last word of a `set.server` line says how the pin was obtained: `pin=typed`
for 64 digits typed in the command, `pin=confirmed` for a hash that SD fetched with
`connect` and SDSYS answered y to. The pin itself is not in the line (it is not
secret, only long). A refusal, a declined replacement, a key that was not trusted,
a connection that failed and `list.servers` write nothing. `set.netlogin` and
`delete.netlogin` write a line **on success only**; the `set.netlogin` line carries
the remote user name you typed, and **no password, key, salt or hash is ever
audited**. A refusal, a failed exchange and a login that was not stored write
nothing. Giving or taking the NET switch is
audited like every other `modify.account` word (`modify.account net-on
account=fred`).

On the client, a write-mode handle adds lines in lower case (no record data, no id):

```
netfile open server=hq file=customers mode=write
netfile write server=hq file=customers
netfile delete server=hq file=customers
netfile clear server=hq file=customers
netfile filelock server=hq file=customers
netfile refused server=hq reason=mode
netfile lost server=hq op=write
```

`write` and `delete` are written the first time through a handle, `clear` every time, `filelock`
the first time a `FILELOCK` is tried through a handle (before the request, so an attempt the other
server refuses is on the trail too; waiting for a busy file is many requests and one line),
`refused ... reason=mode` once per handle when the definition says `read` by then, and `lost` when a
change got no answer. A lost connection during a `FILELOCK`, `FILEUNLOCK` or `RECORDLOCKED()` is
not a `lost` line: they change no data, so it is message 11497 and nothing else. The refusals the kernel makes itself (a read-mode handle, a transaction,
an edit gate) write nothing. The administration group adds
`netfile admin server=hq file=customers op=create.index` (written before the
request is sent) and `netfile fcontrol server=hq file=customers key=n`.

On the server that is reached, the files-only route writes, in lower case:

```
api login route=sdfiles write=off admin=off user=reports
api refused request=20 route=sdfiles write=off admin=off user=reports
modify.account files-on account=reports
modify.account files-write-on account=reports
modify.account files-admin-on account=reports
api login route=sdfiles write=on admin=on user=reports
api admin request=70 op=create.index file=customers user=reports
api refused user=reports reason=not a member of sdapi or sdfiles
```

The first is a successful files-only login (`write=on` when the person is also in
`sdfileswrite`, `admin=on` when also in `sdfilesadmin`, as in the sixth line), the second a request
the route does not allow or, for a login without the write or administration group, a change, a lock
or an administration request (the number is the request; `write` and `admin` are the state of the
login), the third to fifth the administrator giving the route and the two groups, the seventh an
administration act (written before the verb runs, so a killed command is on the trail), and the last a
login of a person who is in neither `sdapi` nor `sdfiles` (the decision is made on both). All of them are written on the server being reached.

## See also

[Accounts and Security: The Edit Switches and the NET Switch](01-accounts-and-security-3-edit-switches.html) for the NET switch beside the
other per-account switches. [Remote Access and the Machine](05-remote-access-and-the-machine.html)
for the API listener a server's port refers to.

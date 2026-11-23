Title: API access
Subtitle: The client API, the port it answers on, the SCRAM login, and what a remote session may reach.

The client API is a normal way for any account to use SD. A person running a
custom GUI program that talks to SD needs API access and may need nothing
else — no ssh, no terminal. **An account has it only if SDSYS gave it — a new
account has none, and `api` (or `both`) gives it:**

```
create.account user jane api
modify.account jane api
```

Your application code does not change. `SDConnect()` and `SDConnectLocal()`
take the same arguments and return the same things. **What changed is
underneath: the login protocol, the port, the identity a session runs as, and
what it is allowed to open.**

> **SDSYS is the one exception: from another computer it has no API access
> until the administrator opens that door**, and then only from the addresses
> named; on this machine it comes through the local Unix socket from a
> process running as `sdsys` — see
> [Reaching the port is not getting in](#reaching-the-port-is-not-getting-in)
> below. **Every other account has no API access until SDSYS gives it** —
> `modify.account` *name* `api` (or `both`), or `api` at `create.account` — and
> an account that has not been given it is refused at the door.

**There is a second, narrower route for a client that only needs files.** An
account SDSYS gave `files-on` (and not `api`) can log in over the API but is
held to files: opening, closing, reading, writing, deleting, selecting, locking,
indices and file information. A request to call a subroutine, execute a
command, enter another account (`logto`), read a variable or use a sequential
file is refused with *"This login is for files only: request n is not
allowed"*, and the connection stays open. An account with `api` has the whole
API whether or not it also has `files-on`. This is the route SDNet's logins are
meant to use.
## The login is SCRAM-SHA-256

**A client that sends a password in clear is refused.** It gets *"Cleartext
login is no longer supported; this server requires SCRAM authentication"* and
the connection drops.

The API runs a challenge and response rather than sending the user name and
password as plain text: the server sets a puzzle only someone who knows the
password can answer, and **the password itself is never sent in any form.**

**The server also proves itself to you.** It finishes by returning a value
only the real server can compute, and the client refuses the connection if it
does not match. Another program that grabbed the port before SD started cannot
pretend to be SD in order to collect passwords.

**The client library pins the server's certificate.** The first connection from
a client to an address and port is trusted, and its certificate is remembered —
the SHA-256 of the whole certificate — in `~/.sdcore/known_servers` (or the file
named by the environment variable `SD_KNOWN_SERVERS`), one line,
`<host>:<port> <64 hex digits>`, per server. Any later connection to the same
address and port that presents another certificate is **refused before a single
byte of the login is sent**, with a message that names both fingerprints and the
line to remove. A server that has been reinstalled has a new certificate: remove
its line and connect again. **Removing the line is the remedy**, and only if you
know why the certificate changed. **A store the
client cannot read or write refuses the connection** rather than connecting
unchecked, so a program that runs with no home directory (a web server's, a
service's) needs `SD_KNOWN_SERVERS` set to a file it may write. This is done in
the client library, so it applies to every program that connects with
`SDConnect`. **The very first connection is trusted**, as with ssh: someone in
the middle at that moment would be remembered instead of the server.

**A client library that does not speak SCRAM is refused outright.** Use the
client library that comes with SD (see
[Client distribution](10-client-distribution.html)).

**An account that has no password set is refused, and the refusal reads as a
wrong password.** From the server's point of view there is no credential to
check; `modify.password` sets one.

**Known issue: `TLS read failed`.** A refused login made through the C client
library can report `TLS read failed` instead of *Invalid username or password*.
The login is refused either way and nothing else is affected.

**The password is never kept anywhere, by design** — SD stores only what the
challenge and response needs to check an answer.

**Programs using the `!sdclient` class are covered.** The class module BASIC
programs use to reach another SD server speaks the same login, so a program
that uses it needs no change.

**`SDConnectLocal()` connections are unaffected.** They send no password and
never did.

## The port

**Whether SD listens for the API at all is `systemd`'s `sdclient.socket`
unit**, activated independently of whether `sd` itself is running — not a
line in `sd.conf`. It defaults to `127.0.0.1:4247`, local only.

**Reaching the port from another computer is off unless you say so during
installation.** Answering yes rebinds the socket to `0.0.0.0:4247` and
adds a firewall rule for 4247/tcp (`ufw`, or firewalld where that is the firewall in use); answering no leaves it local-only. Change
it afterward, as SDSYS:

```
remote.api on | local | off
```

`on` and `local` restart the socket unit (not SD itself — no session is
ended); `off` stops it. See
[Administrator commands](06-administrator-commands.html).

**If you tunnel, you no longer need to.** `ssh -L 4247:127.0.0.1:4247
user@host` still works, but the design expects a direct connection to
port 4247 once you have opened it — tunnelling is only for a `local`-only
install reached from elsewhere.

## The connection is encrypted

**Every API connection is wrapped in TLS 1.3 before SD sends anything**, and
the login is bound to that encrypted connection. A machine sitting between a
client and the server cannot read the traffic or log in on the client's behalf,
even by pretending to be the server. The client libraries and the `!sdclient`
class negotiate it themselves; a program linked against an older copy of the
library cannot connect and needs to be linked again. Which certificate a client
accepts is described under the pin, above.

## Reaching the port is not getting in

A caller must clear two gates, in this order, and SDSYS has a door of its own:

1. **Complete the SCRAM exchange** against a password held for that account —
   so **an account with no password cannot connect at all**.
2. **Be a member of the `sdapi` group** (or of `sdfiles`, for the files-only
   route), which an account joins only when you give it API access:
   `create.account user fred api` or `... both` does that; `ssh` or `none` does
   not.

**SDSYS is never joined to `sdapi`**, because only `create.account` does that
and SDSYS is not created that way, so the ordinary route is closed to it. It has
two doors of its own, and in both it must still complete the SCRAM exchange with
SDSYS's own SD password — the third password the installer asks for:

* **On this machine**, through the local Unix socket only, and only when the
  operating system reports that the connecting process runs as the Linux user
  `sdsys` and that the login that started it is `sdsys`'s own, so `sudo -u sdsys`
  or `su` does not pass. Over the network port on this machine's own loopback
  (`127.0.0.1:4247`) it is refused.
* **From another computer, only through a door the administrator opens.** Signed in
  as `sdsys` at the machine, the administrator opens it for chosen addresses or
  ranges with `remote.sdsys api on` *address ...* and shuts it with
  `remote.sdsys api off`; as delivered it is shut, and an address that is not listed is
  refused. The API must also be open to other computers (`remote.api`) for a client to
  reach it at all. **A session that comes through this door is the administrator's,
  with every right SDSYS has at the machine, so nothing but SDSYS's SD password
  stands between the listed addresses and the administrator.** Open it only for
  addresses you control, with a long password used nowhere else, and shut it when it
  is not needed. The Administrator set's chapter *Remote Administration through the
  API* says what opening it means. **A connection tunnelled through ssh
  (`ssh -L`) arrives from `127.0.0.1`, because the tunnel ends on this machine, and
  SD counts that as this computer.** The address list is not consulted for it, so
  listing `127.0.0.1` (or `any`) does not let a tunnel in: SDSYS over a tunnel is
  refused like any other loopback connection, and only the Unix socket door above
  admits it.

An API session into any other account has exactly that account's rights and
nothing more. See [Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**Failed API logins are written to the audit trail**, with the reason and
the address they came from. The line is written **before** the three-second
wait SD adds to slow down guessing, so a program that hangs up during the wait
is recorded as well. See [Other hardening](13-hardening.html).

## A session is confined to its own account

| | |
|---|---|
| **Allowed** | everything inside its own account, and the shipped SDSYS files every account needs — messages, `syscom`, the dictionaries. Ordinary programs are unaffected |
| **Not allowed** | opening, renaming, deleting or listing anything else, while the account's `os-on` switch is off (as delivered) |

**A refused `OPEN` takes the `ELSE` branch and `STATUS()` is 3035**, which means
*not permitted* rather than *not found*. That distinction matters when you are
debugging: 3035 is a containment refusal, not a missing file.

**A suspended account is refused here too, and deliberately says nothing
about why.** `modify.account fred suspended` denies the API as well as ssh,
and the message is the one this page already gives for an account that does
not exist and for one you are not granted:

```
User not allowed in requested account
```

**All three answer identically on purpose**, so the API cannot be used to
enumerate which accounts exist or what state they are in. If you are debugging
a client that has suddenly stopped connecting, `list accounts` from SDSYS
is where the answer is — a suspended account shows it in that listing.

### If your data lives outside an account

**An API session's file access is its own account's**: what the account's own
file permissions and the confinement described above allow. The one setting that
widens it is `NETDIRS` in `sd.conf`, a list of directories outside every account that
an account without `os-on` may also reach; it is empty as delivered, and the
administrator fills it (see *`NETDIRS`* in the Administrator set's *Configuration*
chapter). `APIPORT` is not a parameter of SD Core for Linux. **The account's `os-on`
switch lifts this confinement**, for an API session as for any other: an
account that holds it reaches whatever its Linux user may (see
[Security and the operating system](12a-security-and-the-operating-system.html)).
If data needs to be reachable from more than one account, put it somewhere
every account can already open on its own terms, or reach it through a
program running in the account that owns it.

## An API session runs as you

**Records an API session creates are owned by the account that logged in**,
and the session reaches files with your Linux permissions rather than a
service account's. If your account may not read something, the API session
may not read it either.

**This is a real `setuid`, not a filtered credential** — SD drops root's
privilege entirely (`initgroups`/`setgid`/`setuid`, `K$ASSUME.USER`) before
the session is ever marked logged in. **If the identity cannot be assumed,
the login is refused outright** rather than continued under any other
identity:

```
Authentication succeeded but the session could not take your Linux identity
```

Because the privilege drop is one atomic system call that either succeeds
or is checked and refused, there is no window in which a session could
believe it is you while actually running as something else — the failure
mode a filtered credential could have.

## `sh` and `OS.EXECUTE` over the API

**They follow the account's switches, the same as anywhere else.** The
per-account switches `sh-on` and `os-on` are read when a session enters its
account — at sign-in and `logto` for a terminal, and by the API server when it
enters the account for an API session — so an account that holds `sh-on` has
the `sh` verb over the API, one that holds `os-on` has `OS.EXECUTE`, and a new
account has neither. **That puts a shell behind the account's API credential,
reachable from wherever the API port is** — weigh it before you turn either
on for an account that also has the `api` route. (SDSYS holds no `sh-on` or `os-on`
switch; an administrator who needs a shell uses the local login.) An API session still
runs as the real account (`setuid`, above), so what it can reach is bounded by
that account's own file permissions. `SDCLIENT` in `sd.conf` is the further
control, if you want one: non-zero disables file access outright for an API
session, and `2` additionally refuses any subroutine not compiled as
callable from a client. It defaults to `0` — see the *Administrator* set's
*Configuration* chapter.

## Client libraries

| | |
|---|---|
| The shared library | `sdclilib.so` |
| Source | built as part of SD Core, or standalone at <https://github.com/dmontaine/linuxsdclilib> |

**It must speak SCRAM.** A client library that sends the password in clear
is refused by the server.

Title: Known Limits
Subtitle: Parts of SD Core for Linux whose behaviour depends on your environment, and what to check before an application relies on them.

Nothing on this page is known to be broken. Each entry is a place where what
happens depends on conditions SD cannot establish for itself: the load on
your machine, the network between two servers, the program you run beside
SD. Treat the page as a list of things to try on your own system before an
application depends on them.

## How to read an entry

| | |
|---|---|
| **What to expect** | how the feature behaves, as far as SD controls it |
| **Check before relying on it** | what to try, on your own system |

## Sessions

### Starting `sd` from inside an `sh` session

**What to expect.** `sh` runs a shell for an account that has the `sh-on`
switch (and always for SDSYS), and starting `sd` from an ordinary Linux shell
works normally. SD does not include a guard that refuses to start `sd` from
*inside* an `sh` session that SD itself launched, so the result is a second,
nested interactive session. See [Operating System
Access](03-operating-system-access.html).

**Check before relying on it.** Do not build a procedure on it. If you need to
know what a nested session does in your environment, start `sd`, then `sh`,
then `sd` again at a real terminal and watch the second one.

## Locking and contention

### Semaphores under heavy contention

**What to expect.** A semaphore is used on every record lock, so ordinary use
exercises it all the time.

**Check before relying on it.** If an application will have many sessions
waiting for the same lock, try that load on your own machine first and watch
how long the waiters wait.

### A lock held by a terminal session and wanted by an API connection

**What to expect.** Two local sessions compete correctly, and the API's own
session-confinement gate is described in *API access* in the **Getting
Started** set.

**Check before relying on it.** If an application mixes terminal sessions and
API clients on the same records, try an API client and a terminal session
competing for one record.

### Task locks taken twice by the same session

**What to expect.** Taking a task lock you already hold succeeds, and one
`unlock` releases it however many times you locked it: the test is "unowned
or mine", and `unlock` clears the slot outright. A program that takes the same
lock twice and expects to hold it after one `unlock` will be wrong.

## Application data

### Large and long-established data

**What to expect.** SD creates, writes, reads and deletes files, records,
indexes, select lists and sequential files, and the system files it starts
with are ordinary files of the same kind.

**Check before relying on it.** Before moving a production application, restore
a copy of its account on SD Core for Linux and run it: a file of hundreds of
thousands of records, a deep dictionary or a schema built over years by
someone else is the case worth trying first.

## Sockets

### UDP and ICMP

**What to expect.** TCP is the supported protocol: listening, connecting,
accepting, reading, writing, the blocking and non-blocking modes and the error
codes. The flags `0x00010000` and `0x00020000` for UDP and ICMP exist in the
language, but SD makes no promise about sockets opened with them.

**Check before relying on it.** Use TCP. If you need a datagram socket, try a
datagram to a listener and back first.

## Scheduled jobs

### A cron job or systemd timer running as an account that `create.account` made

**What to expect.** The `batch.permitted` gate at login (see *Scheduled jobs*
in the **Getting Started** set) decides whether an unattended run is allowed,
and its messages and audit reasons say why a run was refused.

**Check before relying on it.** Point a crontab entry at an SD account and
watch that it runs, and is permitted or refused as you intend, when nobody is
at the terminal.

## SDNet: remote files between SD servers

### Anything between two machines

**What to expect.** The route works between a client and a server: a TLS 1.3
handshake, the pinned key, the SCRAM login from the stored keys, and reads,
writes, locks and deletes through the `sdfiles` route and the write group.
`NETWAIT` and `NETREPLY` bound how long a call waits for a server that never
answers or goes silent after its acknowledgement.

**Check before relying on it.** A firewall in between, a name that has to be
resolved, real network latency, a connection that a router drops, and the key
hash carried from one screen to the other are conditions of your own network.
Set up the server and a client on two machines and try each of them,
including a server that hangs, before depending on remote files in production.

### Changing the `sdfiles` groups

**What to expect.** `modify.account` `files-on`, `files-off`, `files-write-on`,
`files-write-off`, `files-admin-on` and `files-admin-off` change the groups
through the privileged helper. When a removal fails part way, the screen and the
audit trail say which group was changed and which was not.

**Check before relying on it.** After any change, look at the real group file
(`getent group sdfiles`, `sdfileswrite`, `sdfilesadmin`) and sign in as that
account to see what it can do: create, index and delete a file on the server,
and be refused without the group. Check the same after an installation over an
older one that has `sdfiles` and not `sdfileswrite`.

### `MUSTLOCK` on a remote file

**What to expect.** With `MUSTLOCK=1` a write to a file needs the record lock
to be held first, and a remote file follows the same rule.

**Check before relying on it.** `MUSTLOCK` applies to every session, so set it
on a scratch installation first, with a write to a remote file with and without
the lock held.

## SD BASIC statements that depend on something outside SD

| | needs |
|---|---|
| `sendmail` | a mail relay configured on the machine |
| `chgphant()` | a phantom process to change |
| `ccall()` | a C function registered into the executable |

**What to expect.** All three compile in an ordinary account, and none of them
does anything useful without what it needs. Nothing else in the documentation
depends on them.

**Check before relying on it.** Try each with what it needs, on your own
system.

## The terminal editors' key bindings

**`micro`'s key bindings are the program's own, unmodified.** SD only launches
it and stages its syntax highlighting. If a binding surprises you, that is the
program's own documented behaviour.

## What is not on this page

The places where SD Core for Linux deliberately differs from OpenQM,
ScarletDME or SD Core for Windows are documented as differences, in the pages
that describe the feature. This page is only about behaviour that depends on
your own environment.

## See also

[Sessions and Locks](02-sessions-and-locks.html) covers the locking model that
some of the entries above qualify.
[Installation and the daemon](08-sd-installation.html) covers scheduled jobs
and the account model behind the cron entry.
[SD System Limits](06-sd-system-limits.html) states the figures SD works within.

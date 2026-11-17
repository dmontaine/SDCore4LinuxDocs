Title: SD Client API
Subtitle: The sdclilib client library, its functions across eight language bindings, and the server status codes.

The SDClient API lets an external application connect to SD, open
files, read and write records, execute commands, call subroutines,
and manage select lists — all through a single shared library.

**The API is a normal way for any account to use SD**, not a facility reserved
for developers and administrators. A person running a custom GUI program that
talks to SD needs API access and may need nothing else.

## The library

Two names are installed, built from one source in one step:

| | |
|---|---|
| `sdclilib.so` | what existing applications ask for |
| `libsdcli.so` | the ordinary Unix `lib*.so` convention (`-lsdcli` at link time) |

**This port carries no 32-bit build** — a difference from SD Core for
Windows, which ships a separate pair for QM-heritage applications.

### Where it is, and how to use it

Built to `bin/` under the source tree, installed alongside the server
under `/usr/local/sdsys/bin`. Link against it (`-lsdcli`) or load it at
runtime (`dlopen("sdclilib.so", ...)`) the ordinary way for a Linux shared
library — there is no PATH-order concern the way a Windows DLL search has,
because Linux resolves a shared library by its own rules (`rpath`,
`LD_LIBRARY_PATH`, or the standard library paths), not by which directory
happens to be searched first.

The header, `sdclilib.h`, is installed in `/usr/local/sdsys/syscom` with the
other language headers (see
[SD Client API: Language Bindings](37b-sd-client-api-bindings.html)).

## Connection

| | |
|---|---|
| `SDConnect(host, port, user, pass, account)` | over the network, to port **4247** (the default when you name none) |
| `SDConnectLocal(account)` | on the same machine. Sends no password and never did |

> **`SDConnectUDS` (Unix Domain Socket) is not available, on either
> port.** It sent its credential over the socket in a way that predates
> SCRAM, and was removed here for the same reason the old cleartext API
> login was: `SDConnect` and `SDConnectLocal` are the two routes.

**The connection is encrypted.** Every connection to the server is wrapped in
TLS 1.3 before the login, and the client library does this itself. A program
linked against an older copy of the library cannot connect; relink it. The
Getting Started set's *API access* page has the whole story.

### How SDConnectLocal actually works here

**Unlike SD Core for Windows, where `SDConnectLocal` runs the server
binary found beside the loaded DLL** (so a copy of the library sitting
somewhere else fails to find it), **this port `fork()`s and `exec()`s the
server directly, at a path it already knows** — the installation's own
`bin/sd`, not a path relative to wherever `sdclilib.so` happened to be
loaded from. Communication is over a pair of pipes to the child process,
not a socket. There is nothing to copy alongside your application for a
local connection to work; the library finds the server itself.

`SDConnectLocal` sends no password at all. It takes the identity of the
process that called it (`setuid`/`setgid` to match, before the child
process starts) and checks that account's grants, so the account has to
be one the calling Linux user may enter.

**The login is SCRAM-SHA-256.** A client that sends a password in
clear is refused. The server sets a puzzle only someone who knows the
password can answer, and the password itself is never sent in any
form. The server also proves itself to the client — another program
that grabbed the port before SD started cannot pretend to be SD.

> **Run `modify.password` again for every account that uses the API**
> after upgrading. The stored credentials changed shape and the old
> ones cannot be converted — the password was never kept anywhere, by
> design.

A session is confined to its own account. An API session can open
everything inside its own account and the shipped SDSYS files every
account needs, but cannot open, rename, delete or list anything else.

### How big a request may be, and what the server does with one it cannot accept

Every request starts with a 4-byte length that counts the whole packet, itself included, and a 2-byte request code, so the smallest packet is 6 bytes. The client library never sends one that breaks the rules below, so a program using it does not meet them; they matter to a program that speaks the protocol itself, and to anyone probing the port.

| When | The length of a packet may be |
|---|---|
| before the client has logged in (the server is still running as root) | 6 to 65,536 bytes. The login messages are all under 4 KB |
| after the login | 6 to 1,073,741,832 bytes: the largest SD string (1,073,741,822) plus the 10 bytes of header the client library allows for, the number `SD_MAX_PACKET_BYTES` in the library |

A packet that declares anything else (below 6, negative, or over the limit) is not read: the server ends the session at once and writes one line to the system log (`API packet length ... refused (before login)` or `(after login)`). The same test applies to the reply a client sends to an `INPUT` prompt. A client that closes its connection, however early, also ends its session at once, so no server process is left running.

## Server status codes

| Constant | Value | Meaning |
|---|---|---|
| `SV_OK` | 0 | success |
| `SV_ON_ERROR` | 1 | an `ON ERROR` clause fired |
| `SV_ELSE` | 2 | an `ELSE` clause fired |
| `SV_ERROR` | 3 | an error occurred |
| `SV_LOCKED` | 4 | the record is locked by another session |
| `SV_PROMPT` | 5 | the command issued a prompt and is waiting for input |

## Function reference

### Connection management

| Function | Returns | Description |
|---|---|---|
| `SDConnect(host, port, user, pass, account)` | Boolean | connect over TCP. A connection that fails returns false and `SDError()` says why; the session number it was given is the current one afterwards, so **select the session you were using with `SDSetSession`** before going on |
| `SDConnectLocal(account)` | Boolean | connect on the same machine |
| `SDConnected()` | Boolean | is a session active |
| `SDDisconnect()` | none | end the current session |
| `SDDisconnectAll()` | none | end all sessions |
| `SDGetSession()` | Integer | get the current session number |
| `SDSetSession(session)` | Boolean | switch to a session |
| `SDLogto(account)` | Boolean | switch to another account: true if the server moved there, false (and `SDError()` says why) if not, in which case the session stays where it was |

**Sessions.** One program can hold up to **1024** sessions at once, each with its own server process, number and account. The server's own user table (`USERPOOL`, 1023 by default) is the real ceiling. Open more than one with `SDConnect` or `SDConnectLocal`, one after another, noting `SDGetSession()` each time, and move between them with `SDSetSession`.

**Threads.** The client library may be used from several threads of one process, as OpenQM's QMClient may, on these rules:

- **The current session belongs to the thread.** `SDSetSession` and `SDGetSession` act on the calling thread's own selection, so two threads can work on two sessions at the same time. A thread that has not selected a session starts on session 0, which is the one the first connection of the process received; a thread given a session by another thread must `SDSetSession` it before use.
- **A session must not be used by two threads at the same time.** The library does not serialise requests on one session. If more than one thread can reach it, take your own lock round each action, and treat an `SDExecute` and the `SDRespond` calls that answer it as one action.
- **The table of sessions is shared**, so `SDConnect`, `SDConnectLocal`, `SDDisconnect` and `SDDisconnectAll` may be called from any thread; each connect is given a slot of its own however many start at the same moment.
- **The transfer buffer and the `SDCallx` / `SDGetArg` arguments are per thread**, so one thread's call does not overwrite another's results. They are released when the thread ends, or when no session is left.
- **A connection that fails keeps its slot for the thread that made it**, so that `SDError()` still says why after another thread has connected and disconnected; the slot is given back by that thread's next `SDConnect`, `SDSetSession` or `SDDisconnect`, by its end, or by `SDDisconnectAll`.
- The same applies to a session that dies under its thread (`SDConnected()` is false for it and `SDError()` says why).

*Not changed:* a local session is still a server process of its own, so a program that starts many threads each with a session starts that many `sd` processes.

**A session whose server has ended** — its `AUTOLOGOUT` period ran out, the administrator logged it out, the process was killed — does not hang the client: the next request on it comes back empty, `SDError()` says the pipe or connection failed, and `SDDisconnect()` cleans it up. A session can set its own limit by executing the `AUTOLOGOUT` command (`SDExecute("AUTOLOGOUT 10")`: ten minutes idle; the period is in minutes, 0 turns it off).

**`MASTER.LOGIN`.** If the administrator has put a `MASTER.LOGIN` paragraph in the SDSYS VOC it is run when an API session first enters an account, before that account's own `LOGIN` paragraph, as it is for a terminal session; entering another account with `SDLogto` runs the new account's `LOGIN` only. A session can be recognized inside either paragraph by `@TTY`, which is `apisrvr`.

### File operations

| Function | Returns | Description |
|---|---|---|
| `SDOpen(filename)` | Integer (file number) | open a file |
| `SDClose(fileNo)` | none | close a file |
| `SDRead(fileNo, id, err)` | String | read a record |
| `SDReadl(fileNo, id, wait, err)` | String | read with a shared lock |
| `SDReadu(fileNo, id, wait, err)` | String | read with an update lock |
| `SDWrite(fileNo, id, data)` | none | write a record |
| `SDWriteu(fileNo, id, data)` | none | write with an update lock |
| `SDDelete(fileNo, id)` | none | delete a record |
| `SDDeleteu(fileNo, id)` | none | delete with an update lock |
| `SDRecordlock(fileNo, id, updateLock, wait)` | none | set a record lock |
| `SDRecordlocked(fileNo, id)` | Integer | query the lock on a record, as `recordlocked()` does: **-3** another user holds a file lock, **-2** an update lock, **-1** a read lock; **0** not locked; **1** this session holds a read lock, **2** an update lock, **3** a file lock. A file number that is not open gives 0 and `SDError()` says so |
| `SDRelease(fileNo, id)` | none | release a record lock |
| `SDMarkMapping(fileNo, state)` | none | enable/disable mark mapping |
| `SDTrans(file, id, field, action)` | String | `trans()` on the server. `field` is a dictionary name, a field number or -1 for the whole record; `id` may be several ids separated by value marks; `action` is `X` (null if the record is missing, the default) or `C` (the id). The marks of the answer are lowered one level, as `trans()` lowers them. The `B` (binary open) action is refused |
| `SDRTrans(file, id, field, action)` | String | the same with the marks left as they are |

`SDTrans` and `SDRTrans` open the file and its dictionary on the server, so a session that the administrator has restricted with `SDCLIENT` is refused them (message 5262, "File access is disabled").

### Record manipulation

| Function | Returns | Description |
|---|---|---|
| `SDExtract(src, fno, vno, svno)` | String | extract a field, value or subvalue |
| `SDIns(src, fno, vno, svno, newdata)` | String | insert into a dynamic array |
| `SDDel(src, fno, vno, svno)` | String | delete from a dynamic array |
| `SDReplace(src, fno, vno, svno, newdata)` | String | replace a field, value or subvalue |
| `SDLocate(item, src, fno, vno, svno, pos, order)` | Boolean | find a position for ordered insert |

### String functions

| Function | Returns | Description |
|---|---|---|
| `SDField(str, delim, first, occurrences)` | String | extract a field from a delimited string |
| `SDDcount(src, delim)` | Long | the number of delimited items: 1 more than the number of times `delim` occurs, counting non-overlapping occurrences from the left; 0 for a null string or a null delimiter. **The delimiter may be more than one character** (`a::b::c` by `::` is 3) |
| `SDChange(str, old, new, occurrences, start)` | String | replace substrings |
| `SDMatch(src, template)` | Boolean | match a string against a pattern |
| `SDMatchfield(src, template, component)` | String | extract a matched component |
| `SDSubstr(...)` | String | substring (language-specific) |
| `SDChecksum(data)` | Long | the number SD's own `checksum()` gives for the same string, worked out in the library **with no connection to SD**. A byte of 128 or more is taken as a signed character, as the server reads it. A check for accidental damage, not a hash for security (the message digests are the server's `digest()`); the null string is 0 |

### Command execution

| Function | Returns | Description |
|---|---|---|
| `SDExecute(cmnd, err)` | String | execute a TCL command |
| `SDRespond(response, err)` | String | respond to a prompt from `SDExecute` |
| `SDEndCommand()` | none | end a multi-line command |
| `SDCall(name, argcount, ...)` | none | call a cataloged subroutine; the arguments the subroutine changed are put back into yours |
| `SDCallx(name, argcount, ...)` | none | the same call, but your arguments are **not** changed: read each one the subroutine changed with `SDGetArg(n)` afterwards |
| `SDGetArg(argNo)` | String | argument *n* (1 to 20) of the last `SDCallx`; free it with `SDFree` |

> `SDCall` and `SDCallx` are variadic: 0 to 20 arguments. The PureBasic
> header provides per-arity wrappers — `SDCall0` through `SDCall20`, and
> `SDCallx0` through `SDCallx20`.

## Continued in

[SD Client API: Select Lists to Error
Handling](37-sd-client-api-2-select-lists-and-the-rest.html) — the rest of the
function reference.

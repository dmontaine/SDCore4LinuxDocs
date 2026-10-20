Title: SD Client API
Subtitle: The sdclilib client library, its functions across four language bindings, and the server status codes.

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

The header, `sdclilib.h`, ships with the source tree at
`sdb_ai/sd64/gplsrc/sdclilib`.

## Connection

| | |
|---|---|
| `SDConnect(host, port, user, pass, account)` | over the network, to port **4247** |
| `SDConnectLocal(account)` | on the same machine. Sends no password and never did |

> **`SDConnectUDS` (Unix Domain Socket) is not available, on either
> port.** It sent its credential over the socket in a way that predates
> SCRAM, and was removed here for the same reason the old cleartext API
> login was: `SDConnect` and `SDConnectLocal` are the two routes.

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

A packet that declares anything else (below 6, negative, or over the limit) is not read: the server ends the session at once and writes one line to the system log (`API packet length ... refused (before login)` or `(after login)`). The same test applies to the reply a client sends to an `INPUT` prompt. A client that closes its connection, however early, also ends its session at once; *before 20 Oct 2026 about half of the clients that completed the TLS handshake and closed straight away, and every one that sent four bytes that read as a huge length, left the server process running at 100% of a processor until it was killed.*

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

**Sessions.** One program can hold up to **1024** sessions at once, each with its own server process, number and account (it held four before 15 Oct 2026). The server's own user table (`USERPOOL`, 1023 by default) is the real ceiling. Open more than one with `SDConnect` or `SDConnectLocal`, one after another, noting `SDGetSession()` each time, and move between them with `SDSetSession`.

**Threads** (from 15 Oct 2026; before that the library kept its state in plain globals and a program with more than one thread could not use it safely). The client library may be used from several threads of one process, as OpenQM's QMClient may, on these rules:

- **The current session belongs to the thread.** `SDSetSession` and `SDGetSession` act on the calling thread's own selection, so two threads can work on two sessions at the same time. A thread that has not selected a session starts on session 0, which is the one the first connection of the process received; a thread given a session by another thread must `SDSetSession` it before use.
- **A session must not be used by two threads at the same time.** The library does not serialise requests on one session. If more than one thread can reach it, take your own lock round each action, and treat an `SDExecute` and the `SDRespond` calls that answer it as one action.
- **The table of sessions is shared**, so `SDConnect`, `SDConnectLocal`, `SDDisconnect` and `SDDisconnectAll` may be called from any thread; each connect is given a slot of its own however many start at the same moment.
- **The transfer buffer and the `SDCallx` / `SDGetArg` arguments are per thread**, so one thread's call does not overwrite another's results. They are released when the thread ends, or when no session is left.
- **A connection that fails keeps its slot for the thread that made it**, so that `SDError()` still says why after another thread has connected and disconnected; the slot is given back by that thread's next `SDConnect`, `SDSetSession` or `SDDisconnect`, by its end, or by `SDDisconnectAll`.
- The same applies to a session that dies under its thread (`SDConnected()` is false for it and `SDError()` says why).

*Not changed:* a local session is still a server process of its own, so a program that starts many threads each with a session starts that many `sd` processes.

**A session whose server has ended** — its `AUTOLOGOUT` period ran out, the administrator logged it out, the process was killed — does not hang the client: the next request on it comes back empty, `SDError()` says the pipe or connection failed, and `SDDisconnect()` cleans it up. *Before 15 Oct 2026 a local session in that state waited for ever, and writing to it could end the program with `SIGPIPE`.* A session can set its own limit by executing the `AUTOLOGOUT` command (`SDExecute("AUTOLOGOUT 10")`: ten minutes idle; the period is in minutes, 0 turns it off).

**`MASTER.LOGIN`.** If the administrator has put a `MASTER.LOGIN` paragraph in the SDSYS VOC it is run when an API session first enters an account, before that account's own `LOGIN` paragraph, as it is for a terminal session; entering another account with `SDLogto` runs the new account's `LOGIN` only. A session can be recognised inside either paragraph by `@TTY`, which is `apisrvr`.

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
| `SDDcount(src, delim)` | Long | the number of delimited items: 1 more than the number of times `delim` occurs, counting non-overlapping occurrences from the left; 0 for a null string or a null delimiter. **The delimiter may be more than one character** (`a::b::c` by `::` is 3); before 15 Oct 2026 only its first character was used |
| `SDChange(str, old, new, occurrences, start)` | String | replace substrings |
| `SDMatch(src, template)` | Boolean | match a string against a pattern |
| `SDMatchfield(src, template, component)` | String | extract a matched component |
| `SDSubstr(...)` | String | substring (language-specific) |

### Command execution

| Function | Returns | Description |
|---|---|---|
| `SDExecute(cmnd, err)` | String | execute a TCL command |
| `SDRespond(response, err)` | String | respond to a prompt from `SDExecute` |
| `SDEndCommand()` | none | end a multi-line command |
| `SDCall(name, argcount, ...)` | none | call a catalogued subroutine; the arguments the subroutine changed are put back into yours |
| `SDCallx(name, argcount, ...)` | none | the same call, but your arguments are **not** changed: read each one the subroutine changed with `SDGetArg(n)` afterwards |
| `SDGetArg(argNo)` | String | argument *n* (1 to 20) of the last `SDCallx`; free it with `SDFree` |

> `SDCall` and `SDCallx` are variadic: 0 to 20 arguments. The PureBasic
> header provides per-arity wrappers — `SDCall0` through `SDCall20`, and
> `SDCallx0` through `SDCallx20`.

### Select lists

| Function | Returns | Description |
|---|---|---|
| `SDSelect(fileNo, listNo)` | none | select all records in a file |
| `SDSelectIndex(fileNo, indexName, indexValue, listNo)` | none | select by index value |
| `SDSelectLeft(fileNo, indexName, listNo)` | String | select left of an index cursor |
| `SDSelectRight(fileNo, indexName, listNo)` | String | select right of an index cursor |
| `SDSetLeft(fileNo, indexName)` | none | position cursor left |
| `SDSetRight(fileNo, indexName)` | none | position cursor right |
| `SDReadNext(listNo, err)` | String | read next select list id |
| `SDReadList(listNo, err)` | String | read the whole list as a dynamic array |
| `SDClearSelect(listNo)` | none | clear a select list |
| `SDIndices(fileNo, indexName)` | String | `indices()` on the server: with a null name the names of the file's alternate key indexes, with a name that index's details; the null string for an index the file has not |

### The server: revision, variables, SYSTEM() and transactions

| Function | Returns | Description |
|---|---|---|
| `SDRevision()` | String | the client's revision on its own before a connection; once connected, the client's and the server's, as two values separated by a value mark. Works without a connection |
| `SDGetVar(name)` | String | the value of an `@` variable on the server, with or without the `@`, in either case. The names it knows are `@SELECTED`, `@LOGNAME` (also `@USER`), `@WHO`, `@PATH`, `@USERNO`, `@TTY`, `@DS`, `@SENTENCE`, `@COMMAND`, `@SYSTEM.RETURN.CODE`, `@USER.RETURN.CODE`, `@DATE`, `@TIME`, `@ID`, `@ANS` and `@USER0` to `@USER4`; any other name gives the null string, not an error |
| `SDSystem(key)` | String | `system(key)` on the server |
| `SDTxn(mode)` | none | **1** start a transaction, **2** commit, **3** abort, **4** commit *non-durably*: a transaction nested in another is merged into its parent, which alone writes to the files (see *Locks and transactions*). Modes 2 to 4 need a transaction to be running; a mode out of range or a commit with nothing to commit is refused with a message and the session goes on |

### Dictionary items and conversions

| Function | Returns | Description |
|---|---|---|
| `SDEvaluate(dictFileNo, names, data, id)` | String | evaluate dictionary items on the server against a record. `dictFileNo` is the number `SDOpen("DICT name")` gave, `names` one name or several separated by value marks, `data` the record (it becomes `@RECORD`) and `id` its id (`@ID`; pass the null string when the item does not use it). The answers come back joined by **item marks** (character 255). D, A, S, C and I items all work; an I-type or correlative that is not compiled is compiled for the call and the dictionary is **not written to**. A name that is not in the dictionary gives the null string; a phrase or other item that defines no data, and an expression that will not compile, give the null string with `SDError()` saying which. Conversion codes in the item are *not* applied |
| `SDEvalConv(dictFileNo, names, data, id)` | String | the same, and the item's output conversion is applied to each value of its answer |
| `SDIConv(data, code)` | String | `iconv()` on the server, which has every conversion code |
| `SDOConv(data, code)` | String | `oconv()` on the server |
| `SDIConvs(data, code)` | String | `iconvs()`: the conversion is applied to each element of a dynamic array in turn |
| `SDOConvs(data, code)` | String | `oconvs()` |

After a conversion `SDStatus()` is **the conversion's own status** — 0 after a successful one, otherwise as `iconv()` and `oconv()` describe it — and it is for that call alone: the next successful conversion leaves it 0. These need a connection. **A session that the administrator has restricted with `SDCLIENT` cannot reach a file or call a program, so it is refused a conversion code that does either** — a `T` code with a file in it, or a `U` code; the ordinary codes (dates, masked decimals, case) are not affected.

### Sequential files

| Function | Returns | Description |
|---|---|---|
| `SDOpenSeq(file, id, modes)` | Integer | open a sequential file, as `openseq` does. With an `id`, `file` is the name of a **directory file** and `id` the item in it; with a **null `id`**, `file` is a **pathname**. Returns a file number, or **0** with `SDStatus()` and `SDError()` saying why. A file that is not there yet gets a number and is made by the first write. `modes` is added up from: **2** give up with a locked answer if another process has the file (without it the call waits), **16** read only, **256** append, **512** overwrite (empty the file on opening), **1024** flush after every write, **4096** shared (append, for several writers) |
| `SDReadSeq(fileNo, err)` | String | the next line, without its terminator. `err` is the server's answer: **2** at the end of the file, where the string is empty |
| `SDReadBlk(fileNo, bytes, actual)` | String | up to *bytes* bytes (1 to 100,000,000). `actual` is how many came back: fewer at the end of the file, **0** with nothing left. The data may hold any byte, zero included, so read it by `actual` and not by its terminator |
| `SDWriteSeq(fileNo, rec)` | none | write a line and a terminator |
| `SDWriteBlk(fileNo, rec, bytes)` | none | write exactly *bytes* bytes, no terminator added |
| `SDSeek(fileNo, offset, relTo)` | none | position: *relTo* **0** from the start, **1** from here, **2** from the end (a negative offset counts back) |
| `SDWeofSeq(fileNo)` | none | cut the file off at the current position |
| `SDClose(fileNo)` | none | close it (the same function as for any file) |
| `SDWriteSeqKey(fileNo, rec)` | String | **not a sequential file function**: write *rec* to the **hashed** file `SDOpen` gave, under the id the file's own counter gives it (`write … creating.seqkey`), and return that id. The update lock the write takes is released before the call returns. A directory file is refused, with the null string and `SDError()` saying a hashed file is needed |
| `SDWriteuSeqKey(fileNo, rec)` | String | the same, and the update lock is **kept** (`writeu`) |

Their numbers begin at 10001 and are not those of `SDOpen`, so a number of one kind given to a function of the other is refused. The counter starts at 1 and is set with `configure.file … next` ([SD Basic - File Handling](07-sd-basic-file-handling.html)).

**The gates are the ones `openseq` has for any program.** A session whose server is restricted with `SDCLIENT` cannot open any file. An item of a directory file is an SD file and is opened through the VOC, as `openseq` opens it; a file flagged trusted is refused. **A bare pathname is an operating system file, and an account without the `os-on` switch reaches only its own directory by it**: `/etc/hostname`, a sibling account's file, a path that climbs out with `..` and a new file in `/tmp` are all refused with *… is not a file this account may open*, and nothing is made. (The API server asks the account's own switch itself: it is an internal program, which the kernel does not otherwise hold to the gate.)

### Packages

| Function | Returns | Description |
|---|---|---|
| `SDEnterPackage(name)`, `SDExitPackage(name)` | Boolean | **not supported**: licensed packages are not part of SD and the server refuses both. The library still exports them, and the language headers do not declare them |

### Error handling

| Function | Returns | Description |
|---|---|---|
| `SDError()` | String | get the last error message |
| `SDDebug(mode)` | none | enable/disable debug mode |
| `SDStatus()` | Long | get the last server status code |
| `SDFree(ptr)` | none | free a returned pointer |

## Continued in

[SD Client API: Language Bindings](37b-sd-client-api-bindings.html) — the six
language headers and what the API cannot do

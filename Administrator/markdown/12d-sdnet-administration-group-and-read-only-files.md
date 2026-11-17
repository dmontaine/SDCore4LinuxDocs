Title: SDNet: The Administration Group and Remote Files, Read Only
Subtitle: The sdfilesadmin group, and what a program may do with a remote file it can only read.

This page continues [SDNet: The Files-only
Route](12c-sdnet-files-only-route.html).

### The administration group: `sdfilesadmin`

**QMNet's remote administration, behind a third permission that is off for everyone.** A files-only
login that is in **both** `sdfileswrite` and the Linux group **`sdfilesadmin`** may, on that
server and for the account it enters there, do the things below. They are requests 68 to 71 of the
API, and they are the only door a files-only login has to them.

| | |
|---|---|
| 68, 69 | `WRITE` and `WRITEU ... CREATING.SEQKEY`: the file's own counter on this server gives the id |
| 70 | a verb run **on this server for the login**: `analyze.file`, `configure.file`, `create.index`, `build.index`, `delete.index`, `disable.index`, `create.file`, `delete.file` |
| 71 | `FCONTROL(file, key {, value})` |

- **Who gives it, and how.** SDSYS, one person at a time, on the server being reached:
  `modify.account` *name* `files-admin-on`, taken away with `files-admin-off`, and
  `files-admin-on` after `files-on` and `files-write-on` in `create.account user`. **It is off
  for a new account, and the installer does not turn it on** (you do that by hand). The installer makes the group, empty,
  beside the other three.
- **The chain is `sdfiles` < `sdfileswrite` < `sdfilesadmin`: each needs the ones below it, and
  none is ever added over one above it.** `files-admin-on` needs `files-on` and `files-write-on`
  first ("Account *name* does not have files-write, so it cannot be given files-admin: use
  files-write-on first", message 11526, nothing changed). The group alone gives nothing: a login
  in `sdfilesadmin` and not in `sdfileswrite` is refused 68 to 71 as a login without the write group
  is (message 11521). `files-admin-off` takes away only the administration group.
  `files-write-off` and `files-off` take away **the group above first** - administration, then
  write, then files - each removal read back before the next, so a failure half way leaves the
  person with the lower access and never the higher without it. If a step fails after an earlier
  one went, the command says what did happen (`Account fred has files-admin no`, and the audit
  line `modify.account files-admin-off account=fred`) before it reports the failure.
  `files-on` and `files-write-on` take a stray `sdfilesadmin` membership away before they add
  anything, so a leftover can never turn into administration nobody gave. A person who is in
  `sdfilesadmin` alone is taken out of it by `files-off`, where it would have been told "already had
  that access".
- **What it allows is a real capability, and it is the server's own verbs.** A login with both groups
  can create and **delete files**, build indices and reconfigure files in the account it enters on this
  server, as that Linux user, without anyone at this server present. The request is audited on both
  machines. The server runs the verb itself *for the login*, in the account the login entered, so that
  account's switches apply as they would to the same person at a terminal: the edit switches
  (`voc.edit`, `bp.edit`, `dict.edit`) are asked by the file's path for everything but the report
  (`analyze.file`), and the shared account's structure rule holds (a files-only login is never SDSYS).
- **What the server checks before it runs anything.** The verb is chosen by the number of the
  operation and never read from the text. The file is **named by the open file** (the name it was
  opened under on this connection), so a login cannot name one it did not open. The words are
  letters, digits and `. _ -` with single blanks, at most 200 characters; `PATHNAME`, `LPTR`,
  `FORCE` and `NO.QUERY` are refused, `DIRECTORY` is accepted only as the last word (it makes a
  directory file), and a slash or a quote is refused (message 11530). `create.file` and
  `delete.file` are run with `NO.QUERY` because the question was asked at the client. The file is
  closed on this side before the verb runs and opened again after it (the verbs need the file
  to themselves), so an index verb refuses, with the words "Cannot gain exclusive access", if another
  process has the file open; nothing is changed then. Where the server's command execution is
  switched off (`SDCLIENT`) the request is refused with message 5265.
- **A refusal** says "This login cannot administer files here: ask the administrator for
  files-admin-on (request *n*)" (message 11524), or the write-group text (11521) when the write
  group is what is missing, and **nothing is carried out**. It is written
  `api refused request=70 route=sdfiles write=on admin=off user=name`; an act is written, **before** the
  verb runs, `api admin request=70 op=create.index file=customers user=name` (for `create.file` the
  file named is the new one), so a killed command is still on the trail. A login is written
  `api login route=sdfiles write=on admin=on user=name`.
- **The group is read at login**, like the other two, so a change takes effect at the person's next
  login on that server.
- **On the client** the same four things are the statements and verbs of *Programming with a Remote
  File* (User set): `WRITE ... CREATING.SEQKEY`, `FCONTROL`, the six verbs on an `N` pointer,
  `CREATE.FILE name SERVER srv {AS remote}` and `DELETE.FILE` of a pointer. The server definition
  must say `write` (the administrator of the client chose that), and the pointer is written only after
  the server confirmed the file and removed in the same act that the server deleted it.
- **Still refused on a remote file:** the statements that read or change the tree of an index
  (`AKREAD`, `AKWRITE`, `AKDELETE`, `CLEAR.AK`, `AKENABLE`, `AKMAP`), `OPENSEQ` and the other
  sequential-file statements. The statements that *query* an index (`INDICES`, `SELECTINDEX`,
  `SETLEFT`, `SETRIGHT`, `SELECTLEFT`, `SELECTRIGHT`) are not in this list and have no gate of
  their own: a login that is in `sdfiles` may use them on any file it can open, because they change
  nothing.

**The remote user must be a real account on that server.** It is still a Linux user,
a member of `sdusers`, with an SD account of its own, and every gate that account has
there applies to it. What `files-on` replaces is the need for `sdapi`, not for the
account. An administrator who wants an SDNet login for a person on another SD server
creates it there with `create.account user` *name* `files-on` (no `api`; add `files-write-on` only if the person is to change files there, and `files-admin-on` only if the person is to administer them), then gives
the name and the password to the person, who runs `set.netlogin` here.

**The client.** The SDNet client logs in with the stored login (made by
`set.netlogin`) and uses only the requests this route allows, so that it needs no more
than `sdfiles`, plus `sdfileswrite` for a server defined `write`. Opening a remote file
through an `N` pointer is the client. `set.netlogin` itself makes the login exchange as it
always did, which does not depend on the route: the server decides the route at the end of
the exchange. A `set.netlogin` made against a user who is only in `sdfiles` succeeds, and
remote reads and queries work for that user; writes and locks work once it is also in
`sdfileswrite`.

**On the machine being reached:** the group `sdfiles` is made, empty, by the
installer beside `sdssh` and `sdapi`. An installation made before this release has
neither the group nor a copy of the helper that accepts it until the installer is run
again; until then `files-on` says "sdfiles is not a valid Linux Group" and changes
nothing. The API listener has to be on (`remote.api`), as for any API login.

## Remote files, read only

A VOC entry whose first field is `N` names a file on another SD server. It has two more
fields: the server's **name** as defined with `set.server` (field 2) and the file's name
on that server (field 3). Names are lower case; the server name is a letter and up to 15
letters or digits, the file name up to 63 letters, digits and `. _ - $`. Anything else is
refused.

```
N
nfa
customers
```

Opening it with `OPEN 'customers' TO f` (using the VOC name) gives a file variable that
`READ`, `MATREAD`, `READV`, `SELECT`, `SELECTV`, `SSELECT`, `FILEINFO` and `CLOSE` work on, and
`GETLOCKS()` (the local view, see "Writing and locking" below).
`RECORDLOCKED()` is **not** on this list: it needs a `write` definition and the write group like
a lock (see "Writing and locking" below).
`OPEN 'DICT', 'customers' TO d` opens the **dictionary** of the remote file, from the same
server, and the same statements work on it. (The request the client sends for a dictionary
is `dict customers` in lower case; the server opens `dict` and a name, in any case, as a
dictionary. A client on this release against a server that has not been updated cannot
open a dictionary, so `LIST`, `COUNT`, `SORT` and `SELECT` on a remote file stop at
"Cannot open dictionary".)
**Nothing else does.** Every other statement
given the file variable (writes, deletes, `CLEARFILE`, locks including `FILELOCK` and
`FILEUNLOCK`, `AKREAD`...) stops with
message 11501 (or, with `ON ERROR`, sets `STATUS()` and goes on), and nothing is sent to the
other server. `OPENPATH`, `OPENTEMP`, `OPENSEQ` and `CALL "file program"` never see such a
pointer.

**Queries.** `LIST`, `COUNT`, `SORT`, `SELECT`, `SSELECT`, `LIST.ITEM` and `LIST DICT` work on
the VOC name, with the dictionary read from the server. A `SELECT` takes **every record id** of
the remote file in one reply and turns it into an ordinary select list; each record a query
needs is then one request to the server, so a query that reads every record of a big file costs
one round trip per record, and a `WITH` clause reads each record. An id list given on the
command line (`LIST customers 'c2'`) selects nothing and reads only those records.
`INDICES(f)` and the index query statements (`SELECTINDEX`, `SETLEFT`, `SETRIGHT`, `SELECTLEFT`,
`SELECTRIGHT`) go to the server, so a `WITH` clause on a field the server has an
index for asks the server's index (one request for the ids of a value, or a scan from one key to the
next) and reads only the records it names; a file with no index is read as before. A remote file
answers `FILEINFO(f, FL$TYPE)` with 7 (`FL$TYPE.NET`) and counts as case-insensitive, as every file
on a current server is.

Who may open one, checked in this order before anything is dialled: the account holds the
**NET switch** (or is SDSYS), the server is defined, the account is in the definition's
*accounts* list, the user has a stored login (`set.netlogin`) and the server's key still
matches the pin, and the limits (10 servers, 100 open remote files per process) hold.
An `$internal` program is not exempt. Each failure has its own message and an audit line,
`netfile refused server=... reason=...`; a success writes `netfile open server=... file=...`.

**Who may write the pointer.** The VOC is protected by the `voc.edit` switch, which is off
for an ordinary account, so only SDSYS or an account SDSYS has given `voc.edit` can make
one. The switch that matters for *using* it is the NET switch of whoever opens the file.

The login to the other server is the stored one of the person running the program, made
with `set.netlogin`; the connection is the other server's API port, TLS 1.3, with the
pinned key checked before a byte is sent. A connection that dies is noticed on the next
use and reported; it is never quietly remade in the middle of an operation. All of a
process's connections end when the process does, and **at `LOGTO`**: going into another account,
and coming back, closes every connection and invalidates every remote file variable opened before
(a `READ` on one is an error), so a remote file never follows a person into an account that was
not asked whether it may use it. A new `OPEN` dials again.

**The record cache.** To save requests, a process keeps the last 64 records it `READ` from remote
files for **2 seconds**, and the fact that the server did not have a record. A second `READ` of the
same record from the same file variable in that time is answered from memory. This means a `READ`
can show a record up to 2 seconds old: a program that waits for another user's change to a remote
record sees it up to 2 seconds late. A record over 32,768 bytes is not kept, `READV` is not cached,
and the entries of a file go when it is closed, when it is `SELECT`ed again, and at `LOGTO`. Ids
are kept as given, so `READ`s of `JACK` and `jack` are two entries. The cache roughly halves
the requests of a `SORT`; it does little for a `LIST` that reads every record once.

**What is not here yet:** saved lists on the remote side.

`COUNT`, `LIST`, `LIST DICT` and `SORT` work on a remote file, as does the opening of its
dictionary. A read-only definition refuses a write, and a definition whose pin the stored
login was not made for is refused before anything is sent.

### Which remote files work

A remote file is whatever the remote **account's VOC** names, opened by the server with its
ordinary `OPEN`, so the rules are the server's. What the client adds is on this page: the
name is 63 characters or fewer, an id is 1 to 63 characters (anything longer is refused on
the client before it is sent), and what a program receives is the record the server sends,
with the marks as the server holds them. The User set's page 42,
*Programming with a Remote File*, has the table of ids, directory files and the case of ids.

## Continued in

[SDNet: Writing and Locking](12e-sdnet-writing-and-locking.html) — the write
mode and locking.

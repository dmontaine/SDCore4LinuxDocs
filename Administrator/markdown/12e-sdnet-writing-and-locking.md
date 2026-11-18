Title: SDNet: Writing and Locking
Subtitle: The definition's write mode: what a program may change on a remote file, and its locks.

This page continues [SDNet: The Administration Group and Remote Files, Read
Only](12d-sdnet-administration-group-and-read-only-files.html).

## Writing and locking: the definition's `write` mode

A server is `read` unless SDSYS defined it with the word `write` (`set.server ... write`).
**With `read` nothing changes from the section above: every statement that changes or locks a
remote file is refused with message 11501 and nothing is sent.** With `write`, a file opened
through an `N` pointer to that server can be changed and locked by the statements below, for
every account that holds the `net` switch and is on the definition's *accounts* list.

**The mode is the client's.** It is a field of the definition on the machine that is
reading; the server it points at is never told. The server's own limits still apply to the
stored login: the files-only route lets a login write and delete, the server's `voc.edit`,
`dict.edit` and `bp.edit` switches (off by default) refuse a write to a VOC, dictionary or
program file of the remote account, and the remote user's own file permissions decide the
rest. The mode is looked up when the file is opened **and again on every change**, so
`set.server ... read` stops writes through a handle that is already open; a handle opened
while the mode was `read` does not write after the mode is changed to `write` until it is
opened again.

| Statement | What happens |
|---|---|
| `WRITE`, `WRITEU`, `MATWRITE` | one request; the record is written on the server. `WRITE` releases the session's lock on the record, `WRITEU` keeps it |
| `WRITEV`, `WRITEVU` | read the record (never from the cache), change the field, write it, as for a local file |
| `DELETE`, `DELETEU` | one request; a record that is not there is not an error |
| `CLEARFILE` | one request; a big file can take minutes, and the connection is only called lost after five |
| `READU`, `READL`, `MATREADU/L`, `READVU/L` | the lock, then the read; a busy record takes the `LOCKED` branch (`STATUS()` is the holder) or, without a `LOCKED` clause, the statement tries again every quarter of a second until the lock is free |
| `RECORDLOCKU`, `RECORDLOCKL` | the lock, with the same busy behavior |
| `FILELOCK` | one request for the **whole file's** lock; a busy file (another user's file lock, or another user's lock on any record of the file) takes the `LOCKED` clause and `STATUS()` is the holder's user number on that server; with no `LOCKED` clause the statement asks again every quarter of a second. **Only for a server defined `write` and a login in the other server's `sdfileswrite` group** |
| `FILEUNLOCK` | one request; `STATUS()` afterwards is 0 (it was this session's and is free now), 3011 (another user's, still held) or 3012 (nobody held it), as for a local file. Same conditions as `FILELOCK`. It is never stopped by the definition being set back to `read`: giving a lock back changes no data |
| `RELEASE` | the record form, the file form (which also gives the file lock back) and plain `RELEASE` (every lock this process holds on a write-mode server) |
| `RECORDLOCKED()` | the other server's answer (-3 -2 -1 another user holds a file, update or read lock; 0 none; 1 2 3 this session holds a read, update or file lock), and `STATUS()` is the lock owner's user number on that server. **Only for a server defined `write` and a login in the other server's `sdfileswrite` group**, like a lock. A `read` definition stops the program with message 11501 (`recordlocked`) and nothing is sent; a login without the write group is refused by the other server (message 11500 with its text, "request 34"). It is allowed inside `BEGIN TRANSACTION` for a `write` definition: it changes nothing, so a rollback has nothing to undo |
| `GETLOCKS()` | **the local view, for either mode, and nothing is sent**: the one field of three counters (`NUMLOCKS`, the lock count, the peak) of *this* machine's lock table and no lock line. The locks of a remote file are held on the other server and never appear here, in `GETLOCKS()` or in `LIST.READU`; look on the other server for them. `GETLOCKS()` is an internal-programs-only function |

**A verb that takes the file lock works.** `CLEAR.FILE` locks the file, clears it and gives the
lock back, so it clears a write-mode remote file, to the same two conditions as a `CLEARFILE`
statement in a program (and the edit gates by the remote file's name still apply). The query
processor's `LOCKING` keyword (`LIST customers LOCKING`) takes the same file lock and works the same
way; a `read` definition still stops both, because `FILELOCK` is refused there.

Locks are held by the connection: closing the file variable releases the locks taken through
it (a file lock too), ending the process or a `LOGTO` closes the connection and releases them all, and a file
variable that merely goes out of scope has its close sent at the next prompt. Waiting is done
by asking again, so it costs about four requests a second and two machines cannot detect a
deadlock between them. **The wait is never done by the other server:** the client always sends
the "do not wait" form of a lock request (the wait flag of API request 32 is 0), so a wait cannot
look like a lost connection and the break key ends it.

**A file lock keeps everyone else out of a whole file** (they cannot take a read or update lock on
any record of it, or a file lock). That is what `FILELOCK` is for, and it is also why it is held
to the same two conditions as a write: your definition says `write` **and** the other server's
administrator put this login in `sdfileswrite`. A login that is only in `sdfiles` is refused by
the other server with message 11521 and the line `api refused request=32 route=sdfiles write=off
user=...` in its audit trail. The administrator of the server that is reached sees a file lock in
`list.readu` (type `FX`, on the server's own user number) and can clear one with
`unlock file n filelock` (the *Sessions and locks* page); the lock also ends when the session that
holds it does. The first `FILELOCK` through each file variable is audited on the client
(`netfile filelock server=... file=...`); a file lock waited for is one line, not one for each
request.

**`RECORDLOCKED()` is held to the same two conditions.** It asks the other server who holds a record, and the answer names the holder by his user
number on that server, so it is not offered to a login that cannot lock. A `read` definition
stops the program with message 11501 (`recordlocked`, "The file on server ... is read only:
recordlocked is refused. Nothing was sent") and **nothing reaches the other server**. That is the
clear text; the wall is on the other server, where request 34 is in the change set of the
files-only route: a login that is only in `sdfiles` is refused with message 11521 and the line
`api refused request=34 route=sdfiles write=off user=...` in that server's audit trail, whatever
this machine's definition says, and a program is told by message 11500 with that text ("request
34"). `RECORDLOCKED()` has no `ON ERROR` clause, so a refusal always stops the program. Inside
`BEGIN TRANSACTION` it works for a `write` definition: it is a read of the lock table and changes
nothing, so unlike a lock it has nothing for a rollback to undo. **One consequence:** under
`MUSTLOCK` the check that this session holds the lock is the same request, so for a login
without the write group the check itself is refused by the other server, and a write or delete
ends with `STATUS()` 7000 and message 11500 naming request 34 instead of `STATUS()` 3023; nothing
is written in either case.

**Never repeated.** A change that gets no answer (the connection dropped, the server stopped)
is *not* sent again: its outcome is not known. Without `ON ERROR` the program stops with
message 11509 ("it is not known whether the change was made"); with `ON ERROR` `STATUS()` is
7000. The handle and every other handle of that server are dropped; open the file again and
read the record to find out.

**What is refused even with `write`.** A change or lock inside `BEGIN TRANSACTION` (message
11510: a remote write can't be rolled back, so it never joins a local transaction; this holds for
`FILELOCK` and `FILEUNLOCK` too, where openQM's QMNet lets them through without a rollback, which
is a silent loss of the guarantee the program asked for); the statements that read or change the tree
of an index (`AKREAD`, `AKWRITE`, `AKDELETE`, `CLEAR.AK`, `AKENABLE`, `AKMAP`),
`OPENSEQ` and the other sequential-file statements (message 11511). `FILELOCK`, `FILEUNLOCK`,
`GETLOCKS` and `RECORDLOCKED()` are not on this list; they work as the table above says
(`RECORDLOCKED()` and the file lock for a `write` definition and the write group).
**`CONFIGURE.FILE`, `ANALYZE.FILE`, `FCONTROL`, `CREATE.INDEX` and the other index verbs,
creating or deleting a remote file and `WRITE ... CREATING.SEQKEY` work for a login that also has
the administration group (*The administration group*, above), and are refused, with nothing
sent, for a `read` definition.** `MUSTLOCK`
is honored as for a local file (there is no `$MODE AUTOLOCK`): a write without the lock held is refused
with `STATUS()` 3023 (for a login without the write group see `RECORDLOCKED()` above).

**The local edit gates apply by the remote file's name.** A write, delete or clear of a remote
file named `voc`, `bp`, `bp.out`, `*.bp`, `*.bp.out` or `*.dic`, or of a remote dictionary
(`OPEN 'DICT', ...`), needs the account to hold `voc.edit`, `bp.edit` or `dict.edit` as it would for
a local file (messages 11405 to 11407). The programs the system supplies that edit a file the
user names (`ED`, `COPY` and the like) ask the same question.

**The cache is off for a write-mode handle**, so a record is never read from memory a second
before it is changed; a `LIST` or `SORT` over such a file makes about twice the read requests.

**What to expect.** A second session that finds a record locked by the first is told so. A
connection lost while a change is in flight stops the program with message 11509, and no
change is sent twice. `CLEARFILE` of a remote file works; a change inside `BEGIN TRANSACTION` is
refused; the edit gates are applied by the remote file's name; and a gate that is off, a
definition that says `read`, an account that is not listed, a wrong pin and a login removed
from its group are each refused. A write is refused until the person has `files-write-on`;
then `WRITE`, `WRITEU`, `DELETE`, `READU`, `RECORDLOCKU`, `READVU` and `CLEARFILE` work on the
server's file.

`FILELOCK` and `FILEUNLOCK` are refused by the server for a login without the write group
(message 11521; the audit trail has `api refused request=32` and `request=33 route=sdfiles
write=off`), and by the client for a `read` definition and inside `BEGIN TRANSACTION`. With
the write group, `FILELOCK` shows in the server's own `list.readu` as a file lock (type `FX`,
no id) held by the client's session; a second session finds the file busy, with the holder's
user number in `STATUS()`, and then waits for it; `FILEUNLOCK` leaves 0 and 3012; and the lock
is gone from `list.readu` after `CLOSE`, after `RELEASE f`, after a bare `RELEASE` and after a
program that ended holding it.

**`RECORDLOCKED()` and request 34.** A `read` definition stops the program with message 11501
and nothing is sent. A login without the write group is refused by the other server with
message 11521 and the audit line `api refused request=34 route=sdfiles write=off`, and the
client reports message 11500; `MUSTLOCK` is refused for such a login. `RECORDLOCKED()` is
allowed inside `BEGIN TRANSACTION` for a `write` definition.

## Continued in

[SDNet: The Two Waits and What Is Audited](12f-sdnet-waits-and-audit.html) —
NETWAIT, NETREPLY and the audit.

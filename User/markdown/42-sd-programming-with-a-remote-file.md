Title: Programming with a Remote File
Subtitle: What a program can do with a file on another SD server, and what it is told when it is refused.

A file on another SD server is opened by a VOC entry of type `N`. A program opens it by the VOC name and uses it like a local file, with the differences on this page. **Whether you may is not the program's business:** the administrator of your machine defines the server and your account's place on it, the administrator of the other machine decides whether your remote login may change anything, and a program that is refused is told so in the ways below. Setting it all up is in the *Administrator* set, in the SDNet page; this page is for the person who writes the program.

## Opening it

```
N
nfa
customers
```

Field 2 is the server's name as the administrator defined it, field 3 is the file's name on that server (lower case; up to 63 letters, digits and `. _ - $`). An id is 1 to 63 characters; a longer one is refused on your machine before anything is sent. A program cannot make this entry unless its account has the `voc.edit` switch.

```
OPEN 'customers' TO f ELSE CRT 'no such remote file, STATUS() ':STATUS() ; STOP
OPEN 'DICT', 'customers' TO d ELSE ...        ;* the dictionary of the remote file, from the same server
```

`LIST`, `COUNT`, `SORT`, `SELECT`, `SSELECT`, `LIST.ITEM` and `LIST DICT` work on the VOC name, with the dictionary read from the server. Each record a query needs is one request to the server, so a query over a big file is a round trip per record.

## What the statements do

| | A read-only definition | A `write` definition, and the remote login has the write group |
|---|---|---|
| `READ`, `READV`, `MATREAD`, `SELECT`, `SSELECT`, `FILEINFO`, `CLOSE` | work | work |
| `WRITE`, `WRITEU`, `MATWRITE`, `WRITEV`, `WRITEVU`, `DELETE`, `DELETEU`, `CLEARFILE` | refused, **nothing is sent** | one request each, done on the server |
| `READU`, `READL`, `READVU`, `RECORDLOCKU`, `RECORDLOCKL`, `RELEASE` | refused, nothing is sent | work; a busy record takes the `LOCKED` clause |
| `FILELOCK`, `FILEUNLOCK` | refused, nothing is sent | work; a busy file takes the `LOCKED` clause; `FILEUNLOCK` leaves `STATUS()` 0, 3011 or 3012 (below) |
| `RECORDLOCKED()` | refused, **nothing is sent** (message 11501) | works: the other machine says |
| `GETLOCKS()` (internal programs only) | works, **the local view only** (below) | works, the same |
| inside `BEGIN TRANSACTION` | reads work | reads work, and so does `RECORDLOCKED()` (it changes nothing); a change or a lock (`FILELOCK` and `FILEUNLOCK` too) is refused: a remote write cannot be rolled back |
| `WRITE ... CREATING.SEQKEY`, `FCONTROL`, `CONFIGURE.FILE`, `ANALYZE.FILE`, `CREATE.INDEX`, `BUILD.INDEX`, `DELETE.INDEX`, `DISABLE.INDEX`, `CREATE.FILE ... SERVER`, `DELETE.FILE` of a pointer | refused, nothing is sent | work **only if the remote login also has the administration group** (below, *Administering a remote file*) |
| `INDICES()`, `SELECTINDEX`, `SETLEFT`, `SETRIGHT`, `SELECTLEFT`, `SELECTRIGHT` | work: they ask the other machine's indices (below, *Indices of a remote file*) | work, the same: no gate beyond opening the file |
| `OPENSEQ` and the other sequential-file statements, the statements that read or change an index's tree (`AKREAD`, `AKWRITE`, `AKDELETE`, `CLEAR.AK`, `AKENABLE`, `AKMAP`) | refused (message 11501) | refused (message 11511) |

Two things have to be true for a change to be made, a lock to be taken or `RECORDLOCKED()` to be asked, and they are on **two different machines**: the definition on *your* machine says `write` (the administrator of your machine chose that), and the remote login you use is also in the other machine's write group (the administrator of *that* machine chose that, with `modify.account <account> files-write-on`). Either one missing is a refusal, and the program can tell which (below). A definition that says `write` is looked up again at every change, so an administrator who switches it to `read` stops writes through a handle that is already open. **Administering the file is a third thing**, with its own group on the other machine (below).

## What a refused program sees

Write `ON ERROR` after the statement and read `STATUS()`; without it the program stops with a message.

| What happened | With `ON ERROR` | Without it |
|---|---|---|
| your definition says `read` | `STATUS()` is 7000 | message 11501, "The file on server `s` is read only: write is refused.  Nothing was sent" |
| the other machine's login lacks the write group | `STATUS()` is 7000 | message 11500 with the other machine's own reason: "Server `s` answered write with an error: This login cannot change or lock files here: ask the administrator for files-write-on (request 16)" |
| the remote login has the write group but **not the administration group**, and the statement administers the file | `STATUS()` is 7000 | message 11500 with the other machine's words: "Server `s` answered fcontrol with an error: This login cannot administer files here: ask the administrator for files-admin-on (request 71)" (the request is 68, 69, 70 or 71) |
| the connection is lost while a change is in flight | `STATUS()` is 7000 | message 11509: it is not known whether the change was made. **The change is never sent again.** Open the file again and read the record to find out |
| a change or lock inside `BEGIN TRANSACTION` | `STATUS()` is 7000 | message 11510 |
| `MUSTLOCK` is set and the record is not locked | `STATUS()` is 3023 | as for a local file |
| `MUSTLOCK` is set and the other machine's login lacks the write group | `STATUS()` is 7000 (the check "do I hold the lock?" is itself refused, see `RECORDLOCKED()` below) | message 11500, "request 34"; nothing is written |
| `RECORDLOCKED()` of a file whose definition says `read` | (the function has no `ON ERROR`) | message 11501, "recordlocked is refused", nothing sent |
| the id is empty | the `ELSE` branch, `STATUS()` 3000 | as for a local file |

The other machine's text in message 11500 is cut at 100 characters and anything that is not a printable character is dropped. A reply with no text is shown as `status n`. The same holds for a `SELECT` of a remote file whose answer is such an error: it is message 11500 with the other machine's words; it does not stop the program.

## Locks

`READU`, `READVU`, `RECORDLOCKU` and `FILELOCK` on something that is busy take the `LOCKED` clause, and `STATUS()` is the **user number of the session that holds it on the other machine** (the same number its `LIST.READU` shows). With no `LOCKED` clause the statement asks again every quarter of a second until the lock is free, so it costs about four requests a second, **the break key ends the wait**, and **two machines cannot see a deadlock between them**. The other machine is never asked to wait: it is always asked "can I have it now?", so a long wait cannot be mistaken for a lost connection. Locks belong to the connection: closing the file variable releases the locks taken through it (a file lock too), `RELEASE f` and a bare `RELEASE` give back a file lock as they do on a local file, and ending the process or a `LOGTO` releases them all.

**`FILELOCK f`** locks the whole file: nobody else can take a read or update lock on any record of it, or a file lock, until you give it back. It is busy when another user holds the file lock **or any record lock in the file**, and then `STATUS()` is that user's number. It takes **two things**, the same two as a write: your definition says `write`, and the remote login is in the other machine's write group. Without the second, the other machine refuses it (message 11521). **`FILEUNLOCK f`** leaves `STATUS()` set the way it is for a local file: **0** the lock was yours and is free now, **3011** another user holds it (it stays theirs), **3012** nobody held it. Neither is allowed inside `BEGIN TRANSACTION` (message 11510); openQM lets them through without a rollback, SDNet does not.

**`RECORDLOCKED(f, id)`** asks the other machine and gives the code a local file gives: **-3** another user holds a file lock, **-2** an update lock, **-1** a read lock; **0** nobody; **1**, **2**, **3** this session holds a read lock, an update lock or the file lock. `STATUS()` afterwards is the lock owner's user number on that machine (0 when nothing is held). **It needs the same two things as a lock:** a `write` definition on your machine and the remote login in the other machine's write group. A `read` definition stops the program with message 11501 ("recordlocked is refused") and nothing is sent; a login without the write group is refused by the other machine, and the program stops with message 11500 and that machine's words, which end "(request 34)". The function has no `ON ERROR` clause, so a refusal always stops the program. (The answer names the holder by his user number on the other machine, which is why it is not given to a login that cannot lock.) Inside `BEGIN TRANSACTION` it works for a `write` definition: it changes nothing, so a rollback has nothing to undo. Under `MUSTLOCK` the check "do I hold the lock?" is this same request, so for a login without the write group it is refused too: the write ends with `STATUS()` 7000 instead of 3023, and nothing is written. A lost connection stops the program with message 11497.

**`GETLOCKS(f, user)`** (internal programs only) of a remote file is the **local view**, as in openQM: the locks of a remote file are held on the other machine and do not appear in this machine's lock table, in `LIST.READU` or in `GETLOCKS()`. It returns the one field of three numbers (`NUMLOCKS`, the number of record locks held on this machine, the peak) and **no lock line**, whatever the user number, and it asks the other machine nothing. To see who holds what on the other machine, look there (`LIST.READU`, which an administrator of that machine can run).

## Continued in

[Programming with a Remote File: Administering and
Indices](42a-sd-programming-with-a-remote-file-administering.html) —
administering, indices and the refusals.

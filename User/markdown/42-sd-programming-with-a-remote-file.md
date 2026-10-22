Title: Programming with a Remote File
Subtitle: What a program can do with a file on another SD server, what it is told when it is refused, and which of this was measured.

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
| `WRITE ... CREATING.SEQKEY`, `FCONTROL`, `CONFIGURE.FILE`, `ANALYSE.FILE`, `CREATE.INDEX`, `BUILD.INDEX`, `DELETE.INDEX`, `DISABLE.INDEX`, `CREATE.FILE ... SERVER`, `DELETE.FILE` of a pointer | refused, nothing is sent | work **only if the remote login also has the administration group** (below, *Administering a remote file*) |
| `INDICES()`, `SELECTINDEX`, `SETLEFT`, `SETRIGHT`, `SELECTLEFT`, `SELECTRIGHT` | work: they ask the other machine's indices (below, *Indices of a remote file*) | work, the same: no gate beyond opening the file |
| `OPENSEQ` and the other sequential-file statements, the statements that read or change an index's tree (`AKREAD`, `AKWRITE`, `AKDELETE`, `CLEAR.AK`, `AKENABLE`, `AKMAP`) | refused | refused |

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

The other machine's text in message 11500 is cut at 100 characters and anything that is not a printable character is dropped. A reply with no text is shown as `status n`. The same holds for a `SELECT` of a remote file whose answer is such an error: it is message 11500 with the other machine's words (until 19 October 2026 the program was stopped with "READLIST generated an abort event", which `ON ERROR` cannot trap; no real server was seen to send this reply, the case is tested against a fake one).

## Locks

`READU`, `READVU`, `RECORDLOCKU` and `FILELOCK` on something that is busy take the `LOCKED` clause, and `STATUS()` is the **user number of the session that holds it on the other machine** (the same number its `LIST.READU` shows). With no `LOCKED` clause the statement asks again every quarter of a second until the lock is free, so it costs about four requests a second, **the break key ends the wait**, and **two machines cannot see a deadlock between them**. The other machine is never asked to wait: it is always asked "can I have it now?", so a long wait cannot be mistaken for a lost connection. Locks belong to the connection: closing the file variable releases the locks taken through it (a file lock too), `RELEASE f` and a bare `RELEASE` give back a file lock as they do on a local file, and ending the process or a `LOGTO` releases them all.

**`FILELOCK f`** locks the whole file: nobody else can take a read or update lock on any record of it, or a file lock, until you give it back. It is busy when another user holds the file lock **or any record lock in the file**, and then `STATUS()` is that user's number. It takes **two things**, the same two as a write: your definition says `write`, and the remote login is in the other machine's write group. Without the second, the other machine refuses it (message 11521). **`FILEUNLOCK f`** leaves `STATUS()` set the way it is for a local file: **0** the lock was yours and is free now, **3011** another user holds it (it stays theirs), **3012** nobody held it. Neither is allowed inside `BEGIN TRANSACTION` (message 11510); openQM lets them through without a rollback, SDNet does not.

**`RECORDLOCKED(f, id)`** asks the other machine and gives the code a local file gives: **-3** another user holds a file lock, **-2** an update lock, **-1** a read lock; **0** nobody; **1**, **2**, **3** this session holds a read lock, an update lock or the file lock. `STATUS()` afterwards is the lock owner's user number on that machine (0 when nothing is held). **It needs the same two things as a lock:** a `write` definition on your machine and the remote login in the other machine's write group. A `read` definition stops the program with message 11501 ("recordlocked is refused") and nothing is sent; a login without the write group is refused by the other machine, and the program stops with message 11500 and that machine's words, which end "(request 34)". The function has no `ON ERROR` clause, so a refusal always stops the program. (The answer names the holder by his user number on the other machine, which is why it is not given to a login that cannot lock.) Inside `BEGIN TRANSACTION` it works for a `write` definition: it changes nothing, so a rollback has nothing to undo. Under `MUSTLOCK` the check "do I hold the lock?" is this same request, so for a login without the write group it is refused too: the write ends with `STATUS()` 7000 instead of 3023, and nothing is written. A lost connection stops the program with message 11497.

**`GETLOCKS(f, user)`** (internal programs only) of a remote file is the **local view**, as in openQM: the locks of a remote file are held on the other machine and do not appear in this machine's lock table, in `LIST.READU` or in `GETLOCKS()`. It returns the one field of three numbers (`NUMLOCKS`, the number of record locks held on this machine, the peak) and **no lock line**, whatever the user number, and it asks the other machine nothing. To see who holds what on the other machine, look there (`LIST.READU`, which an administrator of that machine can run).

## Administering a remote file (added 21 October 2026)

These do on the other machine what they do on a local file, **for your remote login and in the account that login entered there**, so every switch that account has on that machine applies (a file named `voc`, `*.bp` or `*.dic` still needs `voc.edit`, `bp.edit` or `dict.edit` there, and the shared account's structure rule holds). They need **three things**, the last on the other machine: a `write` definition here, the remote login in the other machine's write group, **and** in its administration group (`modify.account <account> files-admin-on`; it needs `files-on` and `files-write-on` first and is off for every account until the administrator of that machine gives it).

| | |
|---|---|
| `WRITE rec TO f CREATING.SEQKEY id`, `WRITEU ...` | the other machine's **own counter for that file** gives the id and it comes back in `id`; the update lock on the new record is held there for `WRITEU` and given back for `WRITE`. A directory file is refused as it is locally (message 11348). Not inside `BEGIN TRANSACTION` (message 11510) |
| `FCONTROL(f, key {, value})` | goes to the other machine with its key (`FC$SET.SEQ.KEY`, `FC$GET.SEQ.KEY`, `FC$VALID.ID`, `FC$SYNC`, `FC$CRLF`, `FC$MINMOD`) and returns what it returned; `STATUS()` is what it left there. Asking whether a name is a valid record id (key 6) changes nothing, every other key is a change |
| `ANALYSE.FILE`, `CONFIGURE.FILE`, `CREATE.INDEX`, `BUILD.INDEX`, `DELETE.INDEX`, `DISABLE.INDEX` on the VOC name of a remote file | run **on the other machine**, as the remote login's Linux user; **what the verb printed there is printed here**, and the verb's return code is the one the other machine's verb ended with. The file is the one the pointer opened (you cannot name another), and the rest of the command is passed on as it stands |
| `CREATE.FILE name ... SERVER srv {AS remote}` | makes the file on server *srv* (as *remote* there when `AS` is given) and, **only after that machine has confirmed it**, writes the `N` pointer *name* in your VOC: there is never a pointer to a file that is not there. `DICT`, `DATA`, `USING`, `PATHNAME`, a comment, `MULTIFILE` and `KEEPCASE` mean nothing for a remote file and are refused (message 11528) before anything is sent; a name already in your VOC is refused (11539) before anything is sent; `voc.edit` is needed because the pointer is a VOC entry |
| `DELETE.FILE name` where *name* is an `N` pointer | asks, as a local delete does (`NO.QUERY` does not), deletes the file on the other machine and, in the same act, the pointer here. If that machine says the file is not there (someone removed it) the pointer would dangle, so the verb offers to remove it (`NO.QUERY` removes it). If that machine refuses, the pointer stays |

**What the other machine accepts in the words.** Letters, digits and `. _ -`, single blanks, at most 200 characters. `PATHNAME`, `LPTR`, `FORCE`, `NO.QUERY`, a slash, a quote or two blanks in a row are refused with message 11530 and nothing is run; `DIRECTORY` is accepted only as the last word. The verb that asks questions is told not to (`CREATE.FILE` and `DELETE.FILE` get `NO.QUERY` there, since you answered here). The index verbs need the file to themselves: if another process has it open on that machine the verb says "Cannot gain exclusive access" and does nothing, as it does locally.

**What it records.** The other machine writes `api admin request=70 op=create.index file=customers user=name` before it runs the verb, and this machine writes `netfile admin server=nfa file=customers op=create.index` (and `netfile fcontrol ... key=n`), so a killed command is still on both trails.

**Not available:** the statements that read or change the tree of an index (`AKREAD`, `AKWRITE`, `AKDELETE`, `CLEAR.AK`, `AKENABLE`, `AKMAP`) on a remote file are still refused, as are `OPENSEQ` and the other sequential-file statements. A change is never sent twice: a lost reply is message 11509, and the program must look at the file to find out what happened.

## Indices of a remote file

A remote file's indices are the other machine's, and the statements that *query* them work on a remote file the way they do on a local one. They change nothing, so they need no write definition, no administration group and no gate of their own: a program that may open the file may use them, on a read definition as well as a write one, and inside `BEGIN TRANSACTION`.

| Statement | What it does on a remote file |
|---|---|
| `INDICES(f)`, `INDICES(f, name)` | the names of the indices of the file on the other machine, and the description of one (null for a name that is not an index) |
| `SELECTINDEX name FROM f TO n` | the indexed values, as a select list; `STATUS()` 1 and an empty list for an index that is not there |
| `SELECTINDEX name, value FROM f TO n` | the ids that hold the value; `STATUS()` 0 and an empty list for a value nobody holds |
| `SETLEFT name FROM f`, `SETRIGHT name FROM f` | put the scan at the left (lowest) or the right (highest) end |
| `SELECTRIGHT name FROM f SETTING key TO n`, `SELECTLEFT ...` | the next key to the right (or left) of the scan, in `key`, with its ids as the select list; `STATUS()` 1 and nothing when there is no further key |

The other machine keeps the position of a scan *for the open file*, so `SETLEFT` followed by `SELECTRIGHT` walks the keys in order, and `SELECTINDEX name, value` followed by `SELECTRIGHT` goes on from that value, as locally. Each call is one request (a scan that finds a key makes a second one to fetch its ids), so a scan is as slow as the line between the machines. A lost connection stops the statement with message 11497, as a lost `SELECT` does; these statements have no `ON ERROR` clause.

The `INDICES()` that every query asks of every file now gets the other machine's answer, so `LIST`, `COUNT` and `SELECT ... WITH` on a remote file use the other machine's index when the field in the `WITH` clause has one, and read only the records the index names instead of every record. A file with no index is read as before.

## The 2-second cache

A process keeps the last 64 records it `READ` from remote files for **2 seconds**, and also the fact that the server did not have a record. A second `READ` of the same record from the same file variable in that time is answered from memory, so a `READ` can show a record up to 2 seconds old. A record over 32,768 bytes is not kept; `READV` is not cached; a handle that can write is not cached at all.

## Ids, case and size

These were measured at the request layer, with the file opened by name and not through an `N` pointer, on 19 October 2026:

| | |
|---|---|
| a **dynamic** file | folds the case of ids: a record written as `AbC` is read as `abc` |
| a **directory** file | keeps ids as given: a record written as `d1` is not found as `D1` |
| a record written to a directory file | is **text**, one field to a line: the field mark becomes a line end, and it reads back as the same fields |
| a directory file whose lines end CR LF | the record is read as its fields **with the CR kept** at the end of each |
| a record of 1 MB, and one of 20 MB | written and read back byte for byte; the server accepts a request of that size |
| an id holding a **mark** byte (251 to 255, the five marks) | refused by a `WRITE`: `ON ERROR`, `STATUS()` 3000, nothing stored; an id holding byte 247 to 250 is an ordinary one and is written and read back |

Ids that differ only in case are two records in a directory file and one in a dynamic file, as on a local file, so a program that is moved from a local file to a remote one keeps the behaviour of the kind of file it is.

## A program that tells the refusals apart

```
   open 'customers' to f else crt 'OPEN FAILED, STATUS() ':status() ; stop
   oc = 'then'
   write 'viaremote' to f, 'n1' on error oc = 'error'
   if oc = 'error' then
      begin case
         case status() = 7000 ; crt 'refused or lost: read the record to find out which'
         case 1 ; crt 'STATUS() ':status()
      end case
   end
   close f
end
```

This is the shape the SDNet witness (`gplbld/witness-sdnet-files-route.sh`) uses: every change and lock is tried with `ON ERROR` and the branch and `STATUS()` are printed, so a refusal is told from a success by what the program prints and by the other machine's file and audit trail, never by the absence of an error.

## What was measured, and what was not

**`FILELOCK`, `FILEUNLOCK`, `RECORDLOCKED()` and `GETLOCKS()` (added 20 October 2026).** The statements, with the bytes they put on the wire, the answers of the other machine and the files and lock table it ended with, were run in a private sandbox against the test server (`gplbld/sandbox-netfile.py`, 994 rows in the suite now, 969 when the lock statements were added; red on the source before the change, green after, and five deliberate faults each caught by the rows built for them). What the real server answers to requests 32, 33 and 34, which the test server imitates, was measured on a real server by `gplbld/sandbox-req29.py` (rows F20 to F49: the three `FILEUNLOCK` answers, who the holder is when a file is busy because of a record lock, that a close of the right file number releases the lock and a close of another number does not, that `RELEASE` and the end of the session release it). On 20 October 2026 the same statements were run on one real installation talking to itself over the loopback address (`gplbld/witness-sdnet-files-route.sh`, 239 of 239 rows): refused for a login without the write group (and audited on the other machine), refused for a `read` definition and inside `BEGIN TRANSACTION`, and with the write group `FILELOCK` showed in the other machine's own `LIST.READU` as a file lock for exactly as long as the program held it, a second session was told the file was busy with the holder's number in `STATUS()` and then waited for it, and `CLOSE`, `RELEASE`, a bare `RELEASE` and the end of the program each gave it back. **Not measured:** the other machine's `FILELOCK` wait with no `LOCKED` clause on a real server for longer than a few seconds, and anything between two machines.

**`RECORDLOCKED()` needing a `write` definition and the write group (decided the same day).** The rules in "Locks" above were run in the sandbox against the test server and, for the other machine's refusal of request 34 and its audit line, against a real `apisrvr`. The 20 October run on a real installation just described was made **before** this rule: there request 34 was still answered to a login without the write group. The rows for the new rule are written in `gplbld/witness-sdnet-files-route.sh` and **not run**; until they are, a real files-only login asking `RECORDLOCKED()` has not been seen.

All of this was run in a private sandbox against a fake server written for the tests and, for the statements and refusals above, on one real installation talking to itself over the loopback address on 18 October 2026 (before the write group) and, for the write group, at commit `c42aa13`. The table of ids, case and size is measured on a real server at the request layer in a sandbox (`gplbld/sandbox-req29.py`, section H, 64 rows in the suite). **Not measured:** anything between two machines (the owner-run `gplbld/witness-sdnet-two-machines.sh` is the step), `MUSTLOCK` on a real installation, the handler running inside the recursion `WRITEV` uses, and a directory file or an id with a mark byte reached **through an `N` pointer** (the table above is the server's behaviour, not the pointer's).

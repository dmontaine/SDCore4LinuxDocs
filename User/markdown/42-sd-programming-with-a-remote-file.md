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
| inside `BEGIN TRANSACTION` | reads work | a change or a lock is refused: a remote write cannot be rolled back |
| `FILELOCK`, `FILEUNLOCK`, `GETLOCKS`, `RECORDLOCKED()`, `CONFIGURE.FILE`, `ANALYSE.FILE`, `FCONTROL`, index statements, `WRITE ... CREATING.SEQKEY` | refused | refused |

Two things have to be true for a change to be made, and they are on **two different machines**: the definition on *your* machine says `write` (the administrator of your machine chose that), and the remote login you use is also in the other machine's write group (the administrator of *that* machine chose that, with `modify.account <account> files-write-on`). Either one missing is a refusal, and the program can tell which (below). A definition that says `write` is looked up again at every change, so an administrator who switches it to `read` stops writes through a handle that is already open.

## What a refused program sees

Write `ON ERROR` after the statement and read `STATUS()`; without it the program stops with a message.

| What happened | With `ON ERROR` | Without it |
|---|---|---|
| your definition says `read` | `STATUS()` is 7000 | message 11501, "The file on server `s` is read only: write is refused.  Nothing was sent" |
| the other machine's login lacks the write group | `STATUS()` is 7000 | message 11500 with the other machine's own reason: "Server `s` answered write with an error: This login cannot change or lock files here: ask the administrator for files-write-on (request 16)" |
| the connection is lost while a change is in flight | `STATUS()` is 7000 | message 11509: it is not known whether the change was made. **The change is never sent again.** Open the file again and read the record to find out |
| a change or lock inside `BEGIN TRANSACTION` | `STATUS()` is 7000 | message 11510 |
| `MUSTLOCK` is set and the record is not locked | `STATUS()` is 3023 | as for a local file |
| the id is empty | the `ELSE` branch, `STATUS()` 3000 | as for a local file |

The other machine's text in message 11500 is cut at 100 characters and anything that is not a printable character is dropped. A reply with no text is shown as `status n`. The same holds for a `SELECT` of a remote file whose answer is such an error: it is message 11500 with the other machine's words (until 19 October 2026 the program was stopped with "READLIST generated an abort event", which `ON ERROR` cannot trap; no real server was seen to send this reply, the case is tested against a fake one).

## Locks

`READU`, `READVU` and `RECORDLOCKU` on a busy record take the `LOCKED` clause, and `STATUS()` is the **user number of the session that holds it on the other machine** (the same number its `LIST.READU` shows). With no `LOCKED` clause the statement asks again every quarter of a second until the lock is free, so it costs about four requests a second and **two machines cannot see a deadlock between them**. Locks belong to the connection: closing the file variable releases the locks taken through it, and ending the process or a `LOGTO` releases them all.

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

All of this was run in a private sandbox against a fake server written for the tests and, for the statements and refusals above, on one real installation talking to itself over the loopback address on 18 October 2026 (before the write group) and, for the write group, at commit `c42aa13`. The table of ids, case and size is measured on a real server at the request layer in a sandbox (`gplbld/sandbox-req29.py`, section H, 64 rows in the suite). **Not measured:** anything between two machines (the owner-run `gplbld/witness-sdnet-two-machines.sh` is the step), `MUSTLOCK` on a real installation, the handler running inside the recursion `WRITEV` uses, and a directory file or an id with a mark byte reached **through an `N` pointer** (the table above is the server's behaviour, not the pointer's).

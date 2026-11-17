Title: Programming with a Remote File: Administering and Indices
Subtitle: Administering a remote file, indices, the cache, ids and a program that tells the refusals apart.

This page continues [Programming with a Remote
File](42-sd-programming-with-a-remote-file.html).

## Administering a remote file

These do on the other machine what they do on a local file, **for your remote login and in the account that login entered there**, so every switch that account has on that machine applies (a file named `voc`, `*.bp` or `*.dic` still needs `voc.edit`, `bp.edit` or `dict.edit` there, and the shared account's structure rule holds). They need **three things**, the last on the other machine: a `write` definition here, the remote login in the other machine's write group, **and** in its administration group (`modify.account <account> files-admin-on`; it needs `files-on` and `files-write-on` first and is off for every account until the administrator of that machine gives it).

| | |
|---|---|
| `WRITE rec TO f CREATING.SEQKEY id`, `WRITEU ...` | the other machine's **own counter for that file** gives the id and it comes back in `id`; the update lock on the new record is held there for `WRITEU` and given back for `WRITE`. A directory file is refused as it is locally (message 11348). Not inside `BEGIN TRANSACTION` (message 11510) |
| `FCONTROL(f, key {, value})` | goes to the other machine with its key (`FC$SET.SEQ.KEY`, `FC$GET.SEQ.KEY`, `FC$VALID.ID`, `FC$SYNC`, `FC$CRLF`, `FC$MINMOD`) and returns what it returned; `STATUS()` is what it left there. Asking whether a name is a valid record id (key 6) changes nothing, every other key is a change |
| `ANALYZE.FILE`, `CONFIGURE.FILE`, `CREATE.INDEX`, `BUILD.INDEX`, `DELETE.INDEX`, `DISABLE.INDEX` on the VOC name of a remote file | run **on the other machine**, as the remote login's Linux user; **what the verb printed there is printed here**, and the verb's return code is the one the other machine's verb ended with. The file is the one the pointer opened (you cannot name another), and the rest of the command is passed on as it stands |
| `CREATE.FILE name ... SERVER srv {AS remote}` | makes the file on server *srv* (as *remote* there when `AS` is given) and, **only after that machine has confirmed it**, writes the `N` pointer *name* in your VOC: there is never a pointer to a file that is not there. `DICT`, `DATA`, `USING`, `PATHNAME`, a comment and `KEEPCASE` mean nothing for a remote file and are refused (message 11528) before anything is sent; a name already in your VOC is refused (11539) before anything is sent; `voc.edit` is needed because the pointer is a VOC entry |
| `DELETE.FILE name` where *name* is an `N` pointer | asks, as a local delete does (`NO.QUERY` does not), deletes the file on the other machine and, in the same act, the pointer here. If that machine says the file is not there (someone removed it) the pointer would dangle, so the verb offers to remove it (`NO.QUERY` removes it). If that machine refuses, the pointer stays |

**What the other machine accepts in the words.** Letters, digits and `. _ -`, single blanks, at most 200 characters. `PATHNAME`, `LPTR`, `FORCE`, `NO.QUERY`, a slash, a quote or two blanks in a row are refused with message 11530 and nothing is run; `DIRECTORY` is accepted only as the last word. The verb that asks questions is told not to (`CREATE.FILE` and `DELETE.FILE` get `NO.QUERY` there, since you answered here). The index verbs need the file to themselves: if another process has it open on that machine the verb says "Cannot gain exclusive access" and does nothing, as it does locally.

**What it records.** The other machine writes `api admin request=70 op=create.index file=customers user=name` before it runs the verb, and this machine writes `netfile admin server=nfa file=customers op=create.index` (and `netfile fcontrol ... key=n`), so a killed command is still on both trails.

**Not available:** the statements that read or change the tree of an index (`AKREAD`, `AKWRITE`, `AKDELETE`, `CLEAR.AK`, `AKENABLE`, `AKMAP`) on a remote file are still refused (message 11501, or 11511 on a write definition), as are `OPENSEQ` and the other sequential-file statements. A change is never sent twice: a lost reply is message 11509, and the program must look at the file to find out what happened.

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

These are the rules for a file opened by name and not through an `N` pointer:

| | |
|---|---|
| a **dynamic** file | folds the case of ids: a record written as `AbC` is read as `abc` |
| a **directory** file | keeps ids as given: a record written as `d1` is not found as `D1` |
| a record written to a directory file | is **text**, one field to a line: the field mark becomes a line end, and it reads back as the same fields |
| a directory file whose lines end CR LF | the record is read as its fields **with the CR kept** at the end of each |
| a record of 1 MB, and one of 20 MB | written and read back byte for byte; the server accepts a request of that size |
| an id holding a **mark** byte (251 to 255, the five marks) | refused by a `WRITE`: `ON ERROR`, `STATUS()` 3000, nothing stored; an id holding byte 247 to 250 is an ordinary one and is written and read back |

Ids that differ only in case are two records in a directory file and one in a dynamic file, as on a local file, so a program that is moved from a local file to a remote one keeps the behavior of the kind of file it is.

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

This is the shape to use: try every change and lock with `ON ERROR` and print the branch and `STATUS()`, so a refusal is told from a success by what the program prints and by the other machine's file and audit trail, never by the absence of an error.

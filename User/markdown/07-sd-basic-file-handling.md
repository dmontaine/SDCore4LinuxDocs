Title: SD Basic - File Handling
Subtitle: Opening files, reading and writing records, locking, and transactions.

This page covers the statements that reach the database: opening a file,
reading and writing whole records or single fields, the locking that keeps two
sessions out of each other's way, and transactions.

Sequential files — ordinary operating-system files read a line at a time — are
in [SD Basic - Sequential Files](10-sd-basic-sequential-files.html). Select lists are in
[SD Basic - Select Lists](08-sd-basic-select-lists.html).

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## Opening

```
open {dict,} file.name to file.variable {readonly}
   then statements
else statements

openpath pathname to file.variable {readonly}
   then statements
else statements
```

`open` looks the name up in the account's VOC. `openpath` takes an operating
system path and bypasses the VOC entirely.

**The `else` branch is where a missing file arrives, and it is not
optional.** A program that omits it does not compile. Never leave it empty:

```
open 'CUSTOMERS' to f.cust else
   stop 'Cannot open CUSTOMERS'
end
```

**`dict` opens the dictionary rather than the data portion** —
`open 'dict', 'CUSTOMERS' to f.dict else ...`.

`close file.variable` releases it. A file left open is closed when the program
ends, so `close` matters mainly in a long-running program that opens files in a
loop.

### A temporary file

```
opentemp {pathname} {non.transactional} to file.variable
   then statements
else statements
```

`opentemp` makes a new dynamic file and opens it; **the file is deleted when the
file variable is closed** (or goes out of scope). With no pathname, or a null
string, SD makes the file in its temporary directory (the `TEMPDIR` setting;
`system(38)` names it) under a name built from the process number and a counter.
A name that already exists is refused — `else` is taken — never taken over. A temporary file's updates are never part of
a transaction, so that closing it really deletes it, and a session that is killed
leaves its file behind.

**It needs the account's OS-access permission, like `openpath`:** both the
temporary directory and a pathname you give lie outside the account. An account
without the permission can use `opentemp` only with a name inside its own
directory, and takes `else` for the others.

### Flushing the file cache

```
flush.dh.cache {local | no.wait}
```

A dynamic file that a program closes is kept open in a cache of recently closed
files, so that opening it again is quick. A program that is about to do
something outside SD that fails while a file is still open somewhere (moving the
file, say) can ask every process to close its cached files. `flush.dh.cache`
does that and waits, for up to four seconds, for the other processes to say they
have; a process waiting at an `input` does not answer until a key arrives, so it
costs the four seconds. **no.wait** asks and carries on; **local** flushes only
the calling process.

## Reading

```
read variable from file.variable, record.id then ... else ...
readv variable from file.variable, record.id, field then ... else ...
matread matrix from file.variable, record.id then ... else ...
```

| | |
|---|---|
| `read` | the whole record into one dynamic array |
| `readv` | a single field |
| `matread` | the record spread across a dimensioned matrix, one field per element |

For a record holding `alpha` and `beta|gamma`:

| | Result |
|---|---|
| `read got from f, 'R1'` | `then` branch; `dcount(got, @fm)` is `2` |
| `read got from f, 'NOSUCH'` | **`else` branch** |
| `readv fv from f, 'R1', 2` | `beta\|gamma` |

**A missing record is the `else` branch, not an error.** And `status()` after
one reads **3006**, which is how you tell "no such record" from a real failure
such as a permission problem.

**`matread` puts everything past the end of the matrix into element zero.**
A three-field record read into `dim mm(2)` gives `mm(1)` = `f1`,
`mm(2)` = `f2` and **`mm(0)` = `f3`**. Nothing is lost and nothing is reported.

**`inmat()` does not tell you it happened** — it reads `0` after that
`matread`, not `3`. It reports the element count after `matparse`, not after
`matread`. If a record may have more fields than your matrix, `read` it and use
`dcount(rec, @fm)`, or size the matrix from the dictionary.

After `matbuild` and `matwrite`, `inmat()` gives the index of the last element
that went into the string or record, or `0` when the zero element of the matrix
was added at the end.

## Writing

```
write variable to file.variable, record.id
writev variable to file.variable, record.id, field
matwrite matrix to file.variable, record.id
```

Writing creates the record if it does not exist and replaces it if it does.
There is no "insert only" form — read first if that distinction matters, and
hold a lock between the read and the write or two sessions will both find it
absent.

### Files an account may not change: the edit switches

Three kinds of file can be changed only by an account whose administrator
has given it the matching switch (`voc-on`, `bp-on`, `dict-on`; see the
*Administrator* set, *Accounts and security*): a **VOC** (a file called
`voc`), a **dictionary** (a name ending `.dic`) and a **program file** (`bp`,
`bp.out`, or a name ending `.bp` or `.bp.out`). Without the switch `write`,
`writev`, `matwrite`, `delete` and `clearfile` on such a file stop the program
with a message that names the missing switch, or, with an `on error` clause,
take that clause and leave `status()` set; nothing is changed. Reading is
never refused, and neither is a file of any other name. The compiler and
`catalog` refuse in the same way without `bp-on`. The switch is that of the
account the person signed on to, so `logto` does not change the answer.

### Letting the file number its records: `creating.seqkey`

```
write variable to file.variable creating.seqkey id.variable {on error ...}
writeu variable to file.variable creating.seqkey id.variable {on error ...}
```

A **hashed** file keeps a counter in its header. With `creating.seqkey` the record is written
under the counter's next value, **1** in a file that has never used it, and `id.variable`
is given that id (as text). An update lock on the new id is taken for the write and
released before the next statement, or with `writeu` **kept**. In a transaction the id is
taken at the `write`, not at the `commit`, so a transaction that does not commit leaves a gap.
**A directory file is refused** (*WRITE … CREATING.SEQKEY needs a hashed file*; status 3005 under
`on error`) and `id.variable` is left as it was. `fileinfo(file, 1031)` is the id of the last record written this way
(0 if none), and `configure.file` *file* `next` *n* sets the next id (`next query` shows it).

**An id that already names a record is skipped.** Before it uses an id, `write … creating.seqkey`
looks in the file: if a record is already there (written by a copy, by a load, or by a program that
chose its own numbers) it takes the next id instead, so that record is never overwritten. **This is
SD's behavior, not openQM's** — openQM does not look, and its manual tells the programmer to write
every record of the file this way. The skipped numbers leave gaps. In a transaction only the records
already committed to the file are looked at; an id this process took earlier is never given out twice.
**`clear.file` keeps the counter**, so the ids go on from where they were; `configure.file`
*file* `next 1` starts them again. A file made by `copy` starts its own counter at 1, even when
records with numeric ids were copied in; the skipping is what protects them. The counter is changed in
the file header at once, so a power failure can leave it one behind the records; setting it with
`configure.file … next` puts that right. The client library
has it as `SDWriteSeqKey` and `SDWriteuSeqKey` ([SD Client API](37-sd-client-api.html)).

### `fcontrol`: the counter, a test for an id, the minimum modulus

```
result = fcontrol(file.variable, action {, qualifier})
```

`fcontrol` has openQM 4's action numbers, and the tokens `FC$…` are in `keys.h`. An ordinary
program may use it; it changes only the file it is given.

| action | token | what it does |
|---|---|---|
| 1 | `FC$SYNC` | forced writes of a hashed file: the qualifier 1 turns them on, 0 off, -1 only asks. The result is the state before the call. See *Forced writes* below |
| 2 | `FC$SET.SEQ.KEY` | the qualifier *n* (1 or more) becomes the next id `write … creating.seqkey` gives out; returns 1 |
| 3 | `FC$GET.SEQ.KEY` | takes the next id and moves the counter on, so a program can reserve an id without writing a record; the null string if the file is not hashed |
| 4 | `FC$CRLF` | the line terminator mode of a directory file or a sequential file: the qualifier 0 to 3 sets it, -1 only asks. The result is the mode before the call. See *Line terminators* below |
| 5 | | does the user have access to the field position in the qualifier? Always 1: SD has no field level encryption |
| 6 | `FC$VALID.ID` | 1 if the qualifier could be the id of a record of this file (not null, not longer than the limit, no mark characters; a directory file also applies its name mapping), else 0 |
| 7 | `FC$MINMOD` | sets the minimum modulus of a hashed file to the qualifier (1 or more); returns 1 |

Actions 2, 3 and 7 are refused on a file opened `readonly`: `status()` is 3018 and the result is 0
(null for 3), and the counter is not touched. On a file that is not hashed `status()` is 3005; a
qualifier under 1 sets `status()` to 1. `FC$CRLF` on a hashed file gives 0 with `status()` 3004 (*not a directory
file*: a hashed file has no line terminators); a mode outside 0 to 3 gives the mode the file is in and sets
`status()` to 1, changing nothing. Any action number SD does not know stops the program with *the action is not one SD knows*.
`FC$SYNC` works on a hashed file only (`status()` is 3005 on any other). The qualifier may be left out where the action does not use it. The
internal programs' own function is called `fcontrol.int` and is not available to
ordinary programs. On a file reached through an `N` pointer to another SD server the call goes to
that server: the test for an id (action 6) needs only read access there, and every other action needs
the server's administration group, as the server decides ([page 42](42-sd-programming-with-a-remote-file.html)).

### Line terminators: `fcontrol` `FC$CRLF` and the letters `L C B X`

A directory file record is a file of text, and a field mark in a record is a line end on the disk. What counts as a line end
when the record is read back, and what is written for a field mark, is the *line terminator mode* of the open file. There are
four, with the openQM numbers and `keys.h` tokens (`FC$CRLF.LF` 0, `FC$CRLF.CRLF` 1, `FC$CRLF.BOTH` 2, `FC$CRLF.NOCR` 3, which the
manual also spells `FC$CRLF.NO.CR`; both are defined):

| mode | letter | a line ends at | a lone CR | a lone LF | `write` puts for a field mark |
|---|---|---|---|---|---|
| 0 LF | `L` | LF | data | (that is the end) | LF |
| 1 CRLF | `C` | CR LF | data | data | CR LF |
| 2 BOTH | `B` | CR LF or LF | data | (end) | LF |
| 3 NOCR | `X` | LF, with the CRs thrown away | dropped | (end) | LF |

The last line end of a record is not turned into a field mark in any mode, so a record `a`, LF, `b`, LF reads as `a<FM>b`. An
open file starts in the mode its VOC entry names with one of the letters in field 6 (a capital or a small letter; a hashed file
ignores them), and `fcontrol(f, FC$CRLF, mode)` changes it for that file variable only. **A file with no letter and no
`fcontrol` behaves as it always has on this port:** a `read` ends a line at LF and keeps every CR (mode 0), a `write` ends it
with LF, a `readseq` ends a line at LF and drops a CR in front of it (mode 2), a `writeseq` adds LF. So a program that never
asks changes nothing. The modes are for a directory that another system's tools write: a CRLF file read in mode 2 or 3 has no
stray CR on each line (it has one on every line in mode 0), and a file read in mode 1 can hold an LF inside a line. `readseq` and
`writeseq` follow the same four modes (see [SD Basic - Sequential Files](10-sd-basic-sequential-files.html)); `mark.mapping off`
(image mode) turns the conversion off altogether, whatever the mode, and `readblk`, `writeblk`, `osread` and `oswrite` never use
it.

```
open 'IMPORTS' to f.in else stop 'cannot open'
was = fcontrol(f.in, FC$CRLF, FC$CRLF.NOCR)   ;* was = 0, the mode it was in
read rec from f.in, 'from.windows' then ... else ...
```

### Forced writes: `sync`

A file that must survive a power failure can be told to write to disk as it goes. Without it SD, like any
program that writes files, leaves data in the operating system's cache for a short while.

```
open 'LEDGER' to f.ledger sync else stop 'cannot open'
openpath '/data/ledger' to f.ledger sync else stop
x = fcontrol(f.ledger, FC$SYNC, 1)       ;* or turn it on, or off, for a file already open
x = fileinfo(f.ledger, FL$SYNC)          ;* 1 if this open has it on
```

With the state on, every write and delete flushes the primary and the overflow subfiles before the
statement returns. The `S` flag in field 6 of the file's VOC entry (an `F` entry) gives the same state to every
`open` of it, and bit 4 of the `FSYNC` parameter in `sd.conf` gives it to every hashed file. **It is much slower: a write costs a disk flush, so use it on the
files that need it and not on all.** It protects the file you flagged and nothing else on the machine, and a file
that is not hashed (a directory file) does not take it.

`delete file.variable, record.id` removes a record. After
`delete f, 'R2'`, reading `R2` takes the `else` branch.

`clearfile file.variable` empties the file but leaves it in place.

## Continued in

[SD BASIC - File Handling: Locking and Asking About a
File](07a-sd-basic-locking-and-asking-about-a-file.html) — locks, transactions
and asking about a file.

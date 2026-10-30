Title: SD Basic - Sequential Files
Subtitle: Reading and writing ordinary operating-system files a line or a block at a time.

A sequential file is an ordinary file on disk, read and written a line at a
time rather than a record at a time. It is how SD exchanges data with anything
that is not SD — a log, an export, a file dropped in a folder by another
system.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## Opening

```
openseq file.name, record.id {append | overwrite | readonly} to file.variable
   then statements
else statements

openseq pathname {append | overwrite | readonly} to file.variable
   then ... else ...
```

The two-name form addresses a record inside a **directory** file — an SD file
whose records are ordinary files in a folder. The one-name form takes an
operating system path and reaches anything on the machine the account is
allowed to read.

**The `then` and `else` branches do not mean success and failure.**

| | |
|---|---|
| `then` | the file **already existed** |
| `else` | it did **not** exist, and has been created — **or** the open genuinely failed |

`openseq 'ZZDIR', 'LINES'` on a name that does not exist takes the
`else` branch and gives a usable file variable.

**So `else` is not an error branch**, and a program that writes `stop 'cannot
open'` there will refuse to create a file it was supposed to create. To tell
"created" from "failed", test the variable — a failed open leaves it unusable
and the next `writeseq` takes *its* `else` branch.

| keyword | |
|---|---|
| **append** | position at the end, so writes add to what is there |
| **overwrite** | truncate on open |
| **readonly** | open without taking a write lock |
| **creating** | when the name does not exist, make the file now (an existing file is opened as without the word). **The file is made exclusively** (since 30 October 2026): if something has taken the name by the moment it is made, or the name is a symbolic link that leads nowhere, nothing is created and `status()` is 6032 - where before the open found the file that had appeared, or made the link's target. **The same holds for the `openseq file, record` form** (a record whose name is such a link takes the `else`, `status()` 6032, and nothing is made). An `openseq` with a pathname of such a link, without `creating`, opens a file that cannot be written, so the `writeseq` that would have made the link's target is refused; and a link put at the name after the open is refused too. The directory it goes in must be there; it is never made |
| **shared** | includes `creating`, but keeps open-or-create, so that several processes can add to one file; it is not exclusive, except that a name that is a symbolic link leading nowhere is refused with `status()` 6032 as it is for `creating` |

## Reading

```
readseq variable from file.variable {on error statements} then ... else ...
readblk variable from file.variable, bytes then ... else ...
```

| | |
|---|---|
| `readseq` | one line, **without** its terminator |
| `readblk` | a fixed number of bytes, terminators included |

`readseq`'s `else` branch is end of file. Three lines written and read back
give `3` and the first as `line one`, and `status()` at end of file is
**3006** — the same code a missing record gives in
[SD Basic - File Handling](07-sd-basic-file-handling.html).

```
openseq 'EXPORT', 'DATA' to f else stop 'cannot open'
loop
   readseq line from f else exit
   ...
repeat
close f
```

## Writing

```
writeseq variable to file.variable then ... else ...
writeseqf variable to file.variable then ... else ...
writeblk variable to file.variable
send expression {:} to file.variable then ... else ...
weofseq file.variable
```

| | |
|---|---|
| `writeseq` | write a line and a terminator |
| `writeseqf` | the same, then **flush** to disk |
| `writeblk` | write bytes with no terminator added |
| `send` | `writeseq` of an expression; with a **colon** after it, `writeblk` of it: `send 'a' to f` writes `a` and the terminator, `send 'a' : to f` writes `a` alone. `then` or `else` is needed, as for `writeseq` |
| `weofseq` | truncate the file at the current position |

**`writeseq` does not flush.** A program that writes a log and then aborts
can lose the tail. `writeseqf` costs a disk write per line, which is why it is
a separate statement — use it for anything that has to survive a crash, and
`writeseq` plus a `flush` at the end for bulk output.

`weofseq` at the start of a file is how you empty it: `openseq` positions at
the beginning, and truncating there discards everything.

### The line terminator is LF

Two lines written with `writeseq` and read back with `readblk`, byte by byte:

| | |
|---|---|
| bytes | `65 66 10 67 68 10` |
| meaning | `A` `B` **LF** `C` `D` **LF** |

**Unlike SD Core for Windows, which deliberately writes CRLF so a file
opens correctly in Notepad, this port writes the platform's own LF only**
— the original Linux behaviour, kept because there is no Windows tool
here to accommodate. `readseq` accepts either LF or CRLF, and strips
whichever it finds, so a file that started life on a Windows machine
still reads correctly here.

**It matters when you count bytes.** A file of *n* lines written on
this port is *n* bytes shorter than the same file written by SD Core for
Windows, whose CRLF endings cost an extra byte per line.

**You can choose the line end, for one file** (16 Oct 2026). `fcontrol(s, FC$CRLF, mode)` on the file variable of an `openseq`
sets one of four modes, and a letter in field 6 of the VOC entry of the directory file does the same for every `openseq` of its
records: `L` (mode 0) ends a line at LF only and keeps every CR; `C` (mode 1) ends it at CR LF only, so a line may hold an LF
or a CR of its own and `writeseq` adds CR LF; `B` (mode 2) is what `readseq` has always done, CR LF or LF with a lone CR kept;
`X` (mode 3) ends a line at LF and throws every CR away. Only mode 1 changes what `writeseq` writes. A file with no letter and no
`fcontrol` is in mode 2 for `readseq`, as above; `fcontrol(s, FC$CRLF, -1)` says so. The table of all four modes, and what a
directory file `read` and `write` do in each, is under *Line terminators* in
[SD Basic - File Handling](07-sd-basic-file-handling.html). A last line with no line end at the end of the file is a line in
every mode, and a CR left at the very end of a file counts as a line only where it is data.

## A whole file by pathname: `osread`, `oswrite`, `osdelete`

```
osread variable from pathname then ... else ...
oswrite expression to pathname
osdelete pathname
```

`osread` reads the **whole** of the file into the variable, byte for byte: a
newline stays a newline and is not turned into a field mark, and a mark
character stays what it is. `then` is taken when the file was read; `else` when
it could not be opened or read (a missing file, no permission, **a path the
account may not reach**), and the variable is then the null string. A file over
a gigabyte takes `else`. `oswrite` makes the file, or replaces it and **cuts it
to the length of the data**, with no change to a byte; `status()` is 0 if it was
written. `osdelete` deletes a file and says nothing if it cannot: `status()`
tells. **It deletes a file only**, where the openQM statement deletes a
directory too, so that a mistake cannot take a directory and what is in it.

They are built on `openseq` and `deleteseq`, so **the OS-access gate is the
same as theirs**: an account without it reaches only its own directory by these
statements (`oswrite` to anywhere else leaves `status()` 3035 and writes
nothing), and one with it reaches what the user can. openQM's `on error`
clause is not supported; a fault is the `status()`. They take no locks.

**What was read about the file: `system(1071)`.** After a successful `osread` it
gives the file's `status` array, as the system reported it for the file that was read;
it is null before any `osread` and after one that failed, and it belongs to the
process.

## Position

```
seek file.variable {, offset {, relative.to}}
```

| *relative.to* | |
|---|---|
| `0` | from the start of the file |
| `1` | from the current position |
| `2` | from the end |

`seek sq, 0, 0` followed by `readseq` returns the first line; `seek sq, 5, 0`
followed by `readblk sq, 4` returns the four bytes from offset 5.

`seek` with no offset returns to the start. Mixing `seek` with `readseq` is
safe, but an offset that lands in the middle of a CRLF gives a `readseq` that
starts with a stray terminator.

## Buffering and timeouts

```
nobuf file.variable
flush file.variable
timeout file.variable, seconds
```

| | |
|---|---|
| `nobuf` | turn buffering off for this file — every write goes straight out |
| `flush` | push what is buffered now |
| `timeout` | how long a read waits before giving up |

`nobuf` is for a file another process is watching. `timeout` matters on a
named pipe or a device, where a read can otherwise block for ever; on an
ordinary file it does nothing useful.

## Reading what arrives: `get`

```
get variable {, length} {setting count} from file.variable
    {until terminator} {returning last} {waiting seconds} {then ... else ...}
```

`readseq` waits for a whole line. **`get` takes characters as they come**, which is what a
program listening on a named pipe, a serial line or another process's output needs.

| clause | |
|---|---|
| `, length` | read this many characters. With no length and no `until`, one character |
| `setting count` | the number of characters read |
| `until terminator` | read on until this character. **The terminator is kept in the data** — `until char(10)` gives `hello` and the line feed |
| `returning last` | with `until`, the terminator that ended the read (`char(10)` in the example below) |
| `waiting seconds` | how long to wait for each character |

```
openseq '/tmp/feed' to f else stop 'cannot open'
get a, 3 setting c from f                   ;* hel    c = 3
get b setting c from f until char(10)       ;* lo and a line feed
get d, 5 from f waiting 3 then ... else ...
```

**A timeout takes the `else` branch and leaves `status()` at 0**: nothing went wrong, nothing came,
and anything that arrived before the time ran out is in the variable and counted. A later `get` finds
the data that arrived afterwards. **The end of an ordinary file before the length is reached also
takes `else`, but with `status()` not 0**; what there was is in the variable and counted. That is
how a program tells the two apart.

**The wait is for each character, not for the whole read**: a read of 100 characters with
`waiting 5` can take as long as the characters keep arriving inside five seconds of each other.

A pipe or device is opened by its pathname, so the account's OS access gate applies as it does to
any other `openseq` of a path. It was tested on a named pipe fed on a clock and on an ordinary
file; a serial port or other character device was not tried. `get` with no `from` is still a class
module's property declaration, as in [SD Basic - Modern Program Structure](18-sd-basic-modern-program-structure.html).

## Asking about the file

```
status variable from file.variable then ... else ...
```

Fills *variable* with the operating system's view of the file: **21 fields** —
size, timestamps, permissions and the rest, in the order the C library reports
them.

`fileinfo(file.variable, 5)` reports a sequential file's type as **5**, and
key `1006` gives the current position.

## Deleting

```
deleteseq file.name, record.id then ... else ...
deleteseq pathname then ... else ...
```

Removes the file. `close` releases the variable without deleting anything;
a sequential file left open is closed when the program ends, but the buffered
tail is only guaranteed once `close` has run.

## Directory files, and where the marks go

A **directory** file is an SD file whose records are ordinary files. That is
what makes sequential access to them possible, and it is the usual target for
`openseq`.

Because the records are ordinary files, SD has to decide what to do with mark
characters on the way in and out. `mark.mapping` controls it — see
[SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html). With mapping on,
field marks become newlines and back again; with it off the bytes pass through
untouched, which is what you want for a file another system produced.

## What is not here

Nothing in the sequential-file group has been removed from this port. The
**VFS** layer, which used to sit between these statements and the operating
system, has been removed from the C entirely.

## See also

[SD Basic - File Handling](07-sd-basic-file-handling.html) ·
[SD Basic - CSV Files](11-sd-basic-csv-files.html) ·
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html).

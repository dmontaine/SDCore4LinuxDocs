Title: SD TCL - Files and Records
Subtitle: Making, configuring and removing files; copying, renaming, deleting and dumping the records inside them.

This page covers the verbs that act on a whole file or on the records in it,
from the command line. What a program does with the same files is
[SD Basic - File Handling](07-sd-basic-file-handling.html); this is the part you
type.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case, which is what this port uses on disk. In the tables, *italics*
mark something you supply and **bold** marks a word typed as it stands; braces
mark an optional part.

## The two kinds of file, and what they look like on disk

**Both kinds are a Linux directory.** This surprises people who expect a
database file to be one file.

| | |
|---|---|
| **dynamic** | a directory holding components named `%0`, `%1`, … The records are hashed across them and none of it is readable from outside SD |
| **directory** | a directory holding **one ordinary file per record**, named by the record id |

`voc`, `$ipc` and `dict.dic` are dynamic. `messages`, `accounts` and `bp` are
directory files — which is why you can open a BASIC program in any text
editor and why `gpl.bp` is readable in the source tree.

**A dictionary is a separate file that travels with the data file.** Verbs that
can act on either take `dict` in front of the file name; with no `dict` they
mean the data portion.

**The shipped file names are lower case on disk in this port, and unlike SD
Core for Windows, that rename is load-bearing rather than cosmetic.**
`voc`, `bp`, `newvoc`, `accounts`, `messages` and the rest were renamed —
NTFS is case-insensitive and would have matched the old spelling anyway,
but `ext4` is case sensitive, so a mismatch here would have been a real
file-not-found rather than an invisible non-issue. What you can type is
unaffected either way (SD tries as-typed, then lower, then upper), and
the lower-case spelling is what you will see in the path text SD reports
back.

## Making and removing files

```
create.file {dict|data} voc.name directory
create.file {dict|data} voc.name dynamic {parameters}
create.file voc.name using dict filename
```

`create.file` makes the file **and** the VOC record that names it. Without
`dict` or `data` it makes both portions. `using dict` *filename* takes the
dictionary from an existing file instead of creating an empty one, and
`no.query` suppresses the confirmation.

Dynamic files take parameters, all optional:

| | |
|---|---|
| `minimum.modulus` *n* | the floor the file will not shrink below |
| `group.size` *n* | group size in 1 KB units |
| `large.record` *n* | the size above which a record is stored separately |
| `split.load` *n* · `merge.load` *n* | the load factors that trigger growth and shrink |
| `directory` *path* | put the file at *path* instead of in the account |
| `no.case` | record ids are case-insensitive |
| `no.resize` | disable automatic resizing |

```
delete.file {dict|data} voc.name {force} {no.query}
clear.file {dict|data} file
```

`delete.file` removes the file and its VOC record. **`force` is needed if the
file is not empty.** `clear.file` empties a file and keeps it, along with its
dictionary, its indexes and its `creating.seqkey` counter (the next sequential id carries on; this is
SD's behavior, and `configure.file` *file* `next 1` starts it again).

## Changing a file after it exists

```
configure.file {dict} voc.name {parameters}
configure.file {dict} voc.name default
```

The parameters are the `create.file` ones, plus `immediate` to do the work now
rather than lazily, and `dynamic` or `directory` to change the file's kind.
`default` puts the settings back.

**Changing `group.size` restructures the whole file**; the other parameters take effect without
a restructure. Plan for the time and the disk on a large file.

**`reporting`** shows how far the work has got: a line *1000 records converted* at every thousand
and the total at the end, when `dynamic` or `directory` converts the file, and *n groups moved* in the same way
for `immediate`. It changes nothing else, and without it nothing is shown.

`no.case` / `case` and `resize` / `no.resize` are the pairs that turn a setting
on and off. For a directory file, `binary` turns on mark mapping.

**`next` *n*** sets the next record id that `write … creating.seqkey` will give out in a
**hashed** file (see [SD Basic - File Handling](07-sd-basic-file-handling.html)); **`next query`** says
what it is (*The next sequential record id is 103*). A new file's counter is 1, `clear.file` keeps it (SD's behavior), and rebuilding a file
with a different group size carries the counter over. A file made by `copy` starts its own
counter at 1; `write … creating.seqkey` skips an id that already names a record. A directory file is refused:
*NEXT applies to a hashed file only*.

## Looking at a file

```
analyze.file {dict} file {statistics} {lptr}
```

Without `statistics` it reports the shape: the account, the file name, the path,
the type, the group size, the large-record size, the minimum and current
modulus, the load factors and the size in bytes. With `statistics` it walks the
whole file and adds record counts, per-group minimum, maximum and average, and a
size distribution. **`statistics` reads every group**, so it is not free on a big
file.

`analyze.file` is the same verb under the other spelling.

```
fstat filename on            start collecting, clearing the counters
fstat filename {lptr}        show what has been collected
fstat filename off           stop collecting
fstat global {lptr}          the global counters
fstat reset                  clear the global counters
fstat                        the periodic global summary
```

**`fstat` only works on dynamic files.** A directory file named on the command
line gets a warning; one arriving through a select list is skipped silently.
Where a file name is taken, a select list or several names may be given instead.

```
hsm {on|off|display} {user n}
```

The Hot Spot Monitor. `display` is the default. It counts each program's
opens, reads, writes and deletes as well as its calls and processor time, and
the report has a column for each. **What a program asks for through the `open`
of a name (its VOC lookup), or through `readv` and `writev`, which read and
write the record themselves, is not counted against it.** `hsm user n` shows
another session's program names and file names, and each
control character, `del`, byte from 128 to 159 and mark character in them is shown as `?`,
so that a session cannot send a code to your terminal by what it opens (as `pstat` does).

```
profiler on {user n} {event ...}
profiler off {user n}
profiler {display} {user n}
```

The application event profiler: where the Hot Spot Monitor counts per program,
this records **what** the programs did and **where**. `profiler on` starts
logging in your session, or, for the administrator, in session *n*; `profiler off`
stops it and keeps what was found; `profiler` (or `display`) shows it. The events
are `call` (a subroutine), `open`, `read` (including `readu`, `readv` and
`matread`), `write`, `delete`, `openseq`, `readseq`, `writeseq`, `execute` (the
first 32 characters of the command) and `object` (a call of a class module's
object). Name some after `on` to log only those; none means all of them.

The names the display shows (files, subroutines, commands, programs) are made safe to
print in the same way: a control character, `del`, a byte from 128 to 159 or
a mark character is shown as `?`.

`display` is a list of the event types with a count of each. Type the **number** of
a line to open it: the names the events were on (the file, the subroutine, the
command), then the programs that did them, then the **line numbers** in the
program. **`b`** goes back a level and **`q`** leaves. (openQM uses the cursor
keys; a number works on any terminal.) With one profile available it opens
without asking which.

**What it is and is not.** The profile is kept in memory while it is on, and
written to the `$ipc` file when it is turned off, so nothing is left on the
disk and it is gone when SD is restarted. **Only the administrator can profile
another user's session** (what a profile holds is the files and commands of
that user), and an ordinary user sees only their own. It holds 4,000 different
events: when there are more, `display` says how many were not logged. A user's
program is named by the pathname of its compiled code. Only a program's own
statements are counted: a `readv` is one `read`, not that and the reads the
language does for it. The listings, and the four levels of `display`, are under
*Where the work goes: `profiler`* in
[SD TCL - Processes and Phantoms](30-sd-tcl-processes-and-phantoms.html).

```
list.files
```

Reports how many files are open now, the peak for the session and the
configured limit, then lists them:

```
Number of files open = 2.  Peak = 6.  Limit = 80.
```

The limit is the `NUMFILES` configuration parameter. **The peak is what matters
when you are sizing it** — the current figure moves constantly and tells you
almost nothing.

```
find.file {dict} file
```

A summary of one file, opened the way any program would open it: its type
(*Dynamic hashed file, group size 1, modulus 3*, or *Directory file*), its
pathname, and a line for each of these that is true of it — *File uses case
insensitive record ids*, *File has indices*, *File has trigger* name, *File is
read only*. A name that is not in the VOC, or a file that will not open, is said
so. Unlike `analyze.file` it does not walk the file.

## Permission bits of records: `set.mode`

```
set.mode {dict} file {all | from n | id ...} {no.query} mode
```

Sets the permission bits of records of a **directory file**, as `chmod` does
for files. *mode* is three octal digits, owner then group then other (`640`).
The records are named on the line, or `all` of them, or those of select list
*n*, or the active select list if none of these is given — which it asks about
first, unless `no.query` is given. The last word on the line is the mode, so a
record cannot be named after it. It answers `3 record(s) set to mode 640`, and
`@system.return.code` is the count.

**It is behind the account's OS gate.** A change of permission bits is a change
to the operating system's files, so the verb refuses an account whose
`os.execute` gate is off — *SET.MODE changes operating system file permissions
and needs the account's operating system access* — and the administrator turns
the gate on with `modify.account` *name* `os-on`. The administrator needs no
grant.

**It changes the rwx bits and nothing else.** No set-id and no sticky bit (four
digits are refused), only regular files, and a record that is itself a symbolic
link is not followed — it is reported and the file it points at keeps its mode.
A record that is not there is `Record 'xx' not found`. A dynamic file is refused
(*A directory file is required*). What the mode lets other users do is still up
to the account's directory and the file system.

## Reaching a file in another account

```
set.file account file.name pointer.name
```

This writes a **Q-pointer** into your VOC — an indirect pointer naming another
account and a file in it. After it, *pointer.name* is usable wherever a file name
is, and the data stays where it is.

**The account must be in the accounts register**, and the name is folded to
upper case before the register is read. If it is not there you get *Account name
'…' is not in register* and nothing is written.

**The pointer is followed only into an account you could `logto`** — you are a
member of its group and it is not suspended — whether or not your account holds
`os-on`. If you could not, opening the pointer is refused with status 3035 (an
`OPEN … ELSE` takes its `ELSE`), even though `set.file` itself wrote it. The
administrator's *Accounts and security* chapter has the whole rule.

> **Read what `set.file` prints, not just whether it printed.** Its refusals
> echo the names you passed in, so a script that checks its output for the
> pointer name it asked for will find that name in the refusal as well as in the
> success. Check for the success wording, and treat *not in register* and *not
> found* as disqualifiers.

## Copying, deleting and renaming records

```
copy from {dict} src.file {to {dict} tgt.file} {s1{,t1} {s2{,t2}}...}
copy from {dict} src.file {to {dict} tgt.file} all
```

With no `to` clause the copy is **within the source file**, which is how you
duplicate a record under a new id. Each *s*`,`*t* pair is a source id and the id
to give the copy; a bare *s* keeps the id. Options:

| | |
|---|---|
| `overwriting` | replace records that already exist in the target |
| `updating` | copy **only** records that already exist in the target |
| `deleting` | delete the source record after a successful copy |
| `reporting` | list what was copied |
| `binary` | force binary mode when one side is hashed and the other a directory |

`@system.return.code` comes back as the **number of records copied**, or
negative on error.

```
delete {dict} file.name {record.name} {no.query}
delete {dict} file.name all
```

`@system.return.code` is the **number of records deleted**, or negative on error.

```
cname old.file.name to new.file.name
cname {dict} file.name old.record.name to new.record.name
```

A comma may be used instead of `to`. (`rename`, a second name for this verb, was
removed in 2.0-0.) `@system.return.code` is `0` on success and `-1` if the arguments were
wrong.

**`cname` on a file renames the VOC record too**, which is the point — the
name you type and the name on disk stay together. **The new name is stored in lower
case**, in the VOC and as the file's directory, whatever case you typed: `cname old to NEW`
leaves the file as `new`. A new name that is already in the VOC in any case, or that differs
from the old name only in case, is refused with "... is already defined in your VOC".
A file that already has an upper-case name is not renamed by this.

## Seeing what is actually in a record

```
ct {dict} file.name {record.name... | *} {options}
dump {dict} file.name {record.name... | *} {options}
```

Both are the same program. `ct` is a field-by-field listing; `dump` reports the
same data in binary. Options: `hex` for hexadecimal, `binary` for a full-width
report that is not field-based, `no.query` to skip the prompt when a select list
is in use, and `lptr` {*n*} to send it to a print unit.

**Every account has both `ct` and `dump`** — they run the same code, reached
by two separate VOC records rather than one.

## Continued in

[SD TCL - Files and Records: Comparing, Triggers and
Importing](20-sd-tcl-files-and-records-2-comparing-triggers-and-import.html) —
comparing, triggers and importing data.

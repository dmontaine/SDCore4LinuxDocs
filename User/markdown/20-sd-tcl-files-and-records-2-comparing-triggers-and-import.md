Title: SD TCL - Files and Records: Comparing, Triggers and Importing
Subtitle: Comparing files, copying operating system files, triggers, file.stat, and moving data in and out.

This page continues [SD TCL - Files and
Records](20-sd-tcl-files-and-records.html).

## Comparing two files

```
compare.files {dict} file1 {dict} file2 {detail}
```

Counts what two files hold: the records **only in the first**, **only in the
second**, **in both but different**, and **the same**. `detail` lists the ids of
the first three groups, indented three spaces under their count. A dictionary
is named with `dict` in front of its file, so a file and its dictionary can be
compared with each other or with another.

```
compare.files stock stock.new detail
```

```
Records only in stock: 1
   1004
Records only in stock.new: 1
   1006
Records in both that differ: 1
   1002
Records that are the same: 3
```

**`@system.return.code` is 0 when the two files hold the same records and 1 when
they do not**, so a paragraph can test it. Two names are required (*Two file names
required*), and a file that will not open stops it (*Cannot open* the name). The
records of a data collection file are compared as their JSON text, so two equal
collections count as the same.

## Taking the carriage returns out of directory file items

```
fixdir file {id ...}
```

An item of a **directory file** that arrived from a Windows machine has a carriage
return at the end of each line (CR LF line ends), which the Linux side does not
expect. `fixdir` takes the carriage return off the end of each line of the items
named; with no ids it does every item of the file.

```
fixdir notes
```

```
1 record(s) fixed in notes
```

An item with no carriage return is **not rewritten**, so a second run says
*0 record(s) fixed in notes*. The file must be a directory file (*is not a
directory file*), and it must open (*Cannot open*). A file name is required.

## Copying an operating system file

```
oscopy source target {overwrite | append}
```

Copies one **operating system** file, named by its path, which no record verb
can do. Without an option it **will not replace** a target that exists:

```
oscopy /home/pat/in.txt /home/pat/out.txt
oscopy /home/pat/in.txt /home/pat/out.txt
```

```
/home/pat/in.txt copied to /home/pat/out.txt
Target /home/pat/out.txt already exists: give overwrite or append
```

`overwrite` replaces it and `append` adds the source to the end of it. A source
that is not there is reported (*Source ... not found*); any other failure says
*Cannot copy* with the status. **A directory is not copied** — the SD BASIC
subroutine `!ioscopy` does a whole tree — and a program does the same as the
verb with `!oscopy`.

**It runs `cp` as you, so it has your own permissions and nobody else's**, and a
path with a single quote in it is refused. **A path outside the account's own
directory needs the `os-on` switch**, the same one as `OS.EXECUTE`; an account
without it gets *name has no OS access, so outside its own account it can reach
by pathname only a directory the administrator opened to all* and nothing is copied.

## Triggers

```
set.trigger file.name trigger.name {modes}
set.trigger file.name ""
set.trigger file.name
```

Set, remove, or display a file's trigger function. An empty string in quotes
removes it; no argument at all displays it. **`all`** in place of the modes sets
every one of them: pre- and post-write, pre- and post-delete, read, and pre- and
post-clear. **The function must be cataloged** first — *Trigger function is not
cataloged* otherwise.

```
set.trigger stock zztrig all
```

```
Trigger function: zztrig
Modes: PRE.WRITE, PRE.DELETE, POST.WRITE, POST.DELETE, READ, PRE.CLEAR, POST.CLEAR
```

```
list.triggers {file ...} {lptr {n}}
```

**`list.triggers` says the same for every file of the account at once**: the file,
its trigger function and the modes it is set for, with a count at the end. It looks
at the data part and the dictionary of every file the account's VOC points to; with
names after it, only those files.

```
list.triggers
```

```
File                 Trigger function     Modes
-------------------  -------------------  ------------------------------
stock.new            zztrig               PRE.WRITE, PRE.DELETE
stock                zztrig               PRE.WRITE, PRE.DELETE, POST.WRITE, POST.DELETE, READ, PRE.CLEAR, POST.CLEAR
2 file(s) with a trigger function
```

### A trigger on a directory file

A directory file can have a trigger function too. `set.trigger` works on it as on a hashed file, and
`list.triggers` lists it. The directory has no header to hold the trigger, so it is kept in a small text file named
`%header%` in the directory itself, which SD makes when the trigger is set and removes when it is taken away:

```
trigger=zztrig
modes=127
```

`select`, `count` and `analyze.file` do not count it as a record, `clear.file` leaves it (and so the trigger), and no record id
can reach it: `%` is one of the characters SD rewrites in a directory file's record ids, so a program that writes the id
`%header%` makes an ordinary record under another name. The file is not locked away, though: anyone who can write to the
directory can change it with an editor, just as anyone who can write to it can add or remove records, so the trigger is only
as safe as the directory is. A file that is not a header in this form, or names a function whose name no function can have, is
read as no trigger.

**What calls it.** `read`, `write`, `delete` and `clearfile` (and the verbs built on them) call the function for the modes that
are set, in the same order as for a hashed file, with the same arguments, and a pre-write or pre-delete trigger can refuse the
operation with `@trigger.return.code` or change the data being written. **`writeseq`, `writeblk`, `oswrite` and `osdelete` do
not call it**, so a query report sent to a file, or a compile listing, never does; that is openQM's limit too. **A change to the
trigger takes effect when the file is next opened**, not for a program that has it open already (`set.trigger` itself needs the
file to itself, as it does for a hashed file). If the header names a function that is not cataloged, the first operation that
needs it stops with *Trigger function 'name' not loaded for the file*.

## Sizes and who is busy: `file.stat` and `fstat.user`

```
file.stat {dict} {file ...} {lptr {n}} {no.page}
fstat.user {top} {user n} {lptr {unit}} {no.page}
```

**`file.stat`** prints one line for each file of **the current account**: the type
(`DYN`, `DIR` or `COL`), the current and minimum modulus, the group size, the number
of records, the bytes in the primary and overflow subfiles and their total, and `Y` or
`N` for indexes (`AK`), trigger (`TR`), statistics (`ST`), case-insensitive ids (`NC`),
`NO.RESIZE` (`NR`), encryption (`EN`), replication (`RP`) and journalling (`JN`).
A directory file shows its type and record count only. With no names it takes the files
on an active select list (list 0) or, if there is none, every file the VOC points at with
an `F` entry; `dict` reports the dictionaries instead. The report needs **122 columns**.
`EN`, `RP` and `JN` are always `N`: SD has no file encryption, replication or journalling.
**openQM can also report on other accounts (`file.stat account.list`, `file.stat all`);
SD does not**: the report reads each file, and another account's files are the business
of that account's users and of the administrator, who has `list.files` and the
account's own session.

**`fstat.user`** reports file activity by session: how many records each has read,
written and deleted since it started — the counts the system keeps in `fstat global`,
kept for each session as well. Sessions come in user number order, or with **`top`** in
descending order of reads + writes + deletes, which shows where a slow system is busy.
**`user n`** shows all the counts of one session: opens, reads, writes, deletes, clears,
selects, index reads, writes and deletes, splits and merges. **An administrator sees
every session; anyone else sees the sessions of their own login name**, because the file
activity of other people is theirs to see only through an administrator. openQM's verb
repeats the report every two seconds and takes `t`, `i`, `d` and `u` at the keyboard; this
one shows it once — run it again for another look.

## Moving data in and out: `import.csv`, `import.json`, `import.xml` and `convert.data`

```
import.csv pathname file {header} {delimiter x} {quote x} {escape x} {id column | generate} {dict} {overwriting}
import.json pathname collection.file {id name | generate} {overwriting}
import.xml pathname file {id name | generate} {overwriting}
convert.data from.pathname to.pathname {from format} {as format} {header} {no.query}
```

**`import.csv`** reads a CSV file, named by its path, into the records of an SD
file in one line. Each row is a record: the id is the **first column** (or the
column `id` names; `generate` numbers the records 1, 2, 3 and keeps every column
as a field), and the other columns are fields 1, 2, 3 in order. `header` says the
first row names the columns and is not data; with `dict`, a name that has no item
in the dictionary of the file gets a D item pointing at the field of its column.
`delimiter`, `quote` and `escape` name a dialect, as on the
[CSV page](11-sd-basic-csv-files.html), and a quoted field may hold a line break.
Every cell is text: nothing is made a number.

**`import.json`** reads a JSON array of objects, or a JSON Lines file, into a
[collection file](20a-sd-tcl-collection-files.html), one record for each object, kept
as it was. The id is the member `id` names (a string or a number), or `generate`.
An element of the array that is not an object, or an object without that member, is
skipped and counted.

**`import.xml`** is the reverse of the `xml` keyword of the query processor
([the report as XML](21-sd-tcl-query-processor.html)): a document in that shape,
with or without `elements`, is read into the records of a file, the fields
named by the dictionary of the file (a name is the item's id with what XML cannot
have in a name made an underscore). The children of the root are the records; a
single valued field is an attribute (or a child with text), a row of an
association is a child with attributes or children of its own, and a multivalued
field in no association is a child called *name*`_MV`. The id is the attribute
or child `id` names, or the record's number. A value that has no field of that name in the
dictionary is left out and counted (message 11862).

All three leave alone a record that is **already there** and count it as skipped,
unless `overwriting`, and end with *file: n record(s) written, m skipped*. Nothing is
changed by a file that cannot be read (*is not valid JSON/XML ... near character n*) or by a
file that is not there.

**`convert.data`** writes a CSV, JSON, JSON Lines or XML file as another of them. The
format is what each name ends in (`.csv`, `.json`, `.jsonl` or `.ndjson`, `.xml`), or what
`from` (for the file read) and `as` (for the file written) say. A **table** — a CSV file
with `header`, an array of JSON objects, a JSON Lines file, the children of the root of an
XML document — goes to any of the four; to CSV the columns are the names in order of first
appearance, and a value that is not text (a nested array or object) cannot be a CSV cell
and is refused. To XML a table is `<table>` with a `<row>` for each row and a child for
each column. A CSV file without `header` is an array of arrays (columns `c1`, `c2` ... in
XML). A JSON object that is not a table goes to JSON as it is, to XML only when it is an
XML element as `xparse()` gives it, and is refused for CSV and JSON Lines. A file that is
there is asked about (*Overwrite(y/<n>)?*, Enter is no) unless `no.query`.

**All four go through the same gates as `oswrite` and `write`.** The pathnames need the
account's OS-access switch (`os-on`) for anything outside the account's own directory
(*has no OS access ... can reach by pathname only a directory the administrator opened to
all*, and nothing is read or written),
and the file or the path they write goes through the edit gates: a program file, VOC or
dictionary changes only when the account has `bp.edit`, `voc.edit` or `dict.edit`.

## Who has these verbs

**Every account has all of them now** — there is no longer a withheld set.
`ct`, `list.files`, `set.file`, `analyze.file`, `clear.file`,
`cname`, `configure.file`, `compare.files`, `copy`, `create.file`,
`delete`, `delete.file`, `dump`, `file.stat`, `fixdir`, `find.file`, `fstat`,
`fstat.user`, `hsm`, `import.csv`, `import.json`, `import.xml`, `convert.data`,
`list.triggers`, `oscopy`, `set.mode`, `set.trigger` are all in every
account's VOC. (`set.mode` is there but refuses an account without the OS gate,
as above.)

## What is not here

**Indexes are their own subject** and are not on this page. For what an index
is and what it does to a file, see [SD Basic - Alternate Key
Indexes](09-sd-basic-alternate-key-indexes.html).

**Selecting records is the query processor's job**, not these verbs'. `copy`,
`delete` and `ct` all accept a select list built by `select` or `sselect`, and
that is how they are usually driven over more than a handful of ids.

**`reformat` and `sreformat`** rewrite records through a dictionary and are run
by the query processor, so they are documented with it.

**There is no verb that repairs a damaged file.** `analyze.file statistics` will
tell you a file is badly overflowed; `configure.file` is what acts on that.

## See also

[SD TCL - The Command Processor](19-sd-tcl-command-processor.html) ·
[SD Basic - File Handling](07-sd-basic-file-handling.html) ·
[SD Basic - Select Lists](08-sd-basic-select-lists.html).

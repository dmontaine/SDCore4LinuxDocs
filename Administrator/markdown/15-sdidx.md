Title: sdidx, the Index Relocation Tool
Subtitle: Reporting where a hashed file's indexes are kept, moving them to another directory or back, pointing a file at indexes you have moved yourself, and deleting them: every option, and what each does to the disk.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

An index on an SD hashed file lives in an extra file beside the data, `%2` for
the file's first index, `%3` for the next, up to 32 in all. Normally it sits in
the data file's own directory. An index can instead be kept in another
directory, **relocated**, which is how an index is put on a faster or larger
disk. The data file's header records where. `sdidx` is the stand-alone program
that reads and changes that record and moves the files. It works on the files
on disk, not through SD.

You can relocate an index at creation from SD: `create.index` *file* *field*
`pathname` *path*. `sdidx` is for everything after that, and for the case where
SD is not running.

> **How this page was made.** Everything here was read from `sdidx.c` and run
> on scratch copies of a small indexed file in a private sandbox built from SD
> Core for Linux `Dev` at commit `1adf913` (banner `SDIDX L1.1-3`). The sections
> say *run* where output is real. It was not run as another user, as root, on a
> file with more than one index, on a path over 255 characters or on a big file.

## The short version

```
sdidx -q /home/sd/user_accounts/acct/orders        # where are its indexes?
```

* **Take a copy of the file's whole directory first (`cp -a`) if you use `-m`
  or `-d`.** `-m` deletes the old index location afterwards and `-d` deletes
  indexes. Neither can be undone.
* **Give full paths, for the data file and for the index directory.** The data
  path is resolved for you. The index path is stored exactly as typed
  (*run*: `-p` with `by-hand` reported `Index directory is by-hand`), and SD uses
  the stored text as the path, so a relative one only works from one directory.
* **Close the file in every session first.** The program refuses if the file is
  open within the running SD: see below. **It refuses nothing if SD is not
  running**, because it has nothing to ask.
* **Check two things after `-m` or `-d` on a file in an account**: that the old
  `%2` really went (see the fault below), and who owns the files you moved.

## Where it is and who can run it

`/usr/local/sdsys/bin/sdidx`. Only `sd` is linked into `/usr/local/bin`, so
type the full path. **It opens the file's `%0` for read and write even to answer
`-q`**, so you need write access to the file even to ask where its indexes are
(*run*: on a copy with the write permission removed, `-q` printed *Cannot open
data file [13]* and exited 1). Run it as the user who owns the account, or as
`sdsys`. Files it creates (`-m` copies the index to a new file) belong to
whoever runs it, with that user's umask, so a run as root leaves root-owned
index files that an account's own user may not be able to write. *Not run as
root here*; check with `ls -l` and `chown` them back.

It needs no configuration file and takes no option other than the mode.

## The command line

```
sdidx -d datapath             delete the indexes
sdidx -m datapath {akpath}    move the indexes to akpath (or back, if omitted)
sdidx -p datapath {akpath}    set the index path in the header, move nothing
sdidx -q datapath             report where the indexes are
sdidx datapath                the same as -q
```

Give exactly one mode. Letters are not case sensitive, and only the second
character of a word is read, so `-qx` is `-q`. Anything else, two modes, an
extra argument or no path prints the five usage lines above and exits 1. A
**datapath** is the OS path of the file's directory, not an SD file name. A
path that does not exist, or is not an SD hashed file, gives *Cannot open data
file [2]* and exit 1.

Every run prints the banner. Success exits 0; any failure exits 1.

### `-q`, report *(run)*

```
$ sdidx -q orders
Indices are not relocated
$ sdidx plain
File has no indices
$ sdidx orders          (after a move)
Index directory is /tmp/sdi_demo/orders.idx
```

The three answers are the only ones. It changes nothing.

### `-m`, move *(run)*

```
$ sdidx -m orders /tmp/sdi_demo/orders.idx
Moving index subfile 2
Indices have been moved
```

What it does, in order: refuses if the file is open in SD; stops with
*Indices are already at this location* if `akpath` is where they are; checks that
each index file really belongs to this data file (it compares a creation stamp in
both headers, and says *Index subfile n does not appear to belong to the data
file* or *Incorrect magic number* if not); refuses with *`akpath` already exists*
if the target is there; creates the target directory, **and any missing parents**
(*run*: `a/b/c` was made from nothing); **copies** each index file to the new
place; writes the new path into the data header; **then deletes the old
location.** If it stops before the header is written, the copy at the target is
left behind and the file is as before.

* **With no `akpath`, it moves the indexes back** into the data file's own
  directory and clears the path in the header. *Run.*
* **The old location is deleted whole.** If the indexes were relocated, the
  entire old directory is removed, **including anything else in it** (*run*: a
  file named `note-from-admin` put in the old directory was gone). Never point
  indexes at a directory that holds anything else, or move them from one.
* It needs room for a second copy of the indexes while it moves them.

### `-p`, point *(run)*

`-p` writes the path into the header and moves nothing. Use it when you have
moved the index files yourself (or restored them elsewhere) and only the header
is out of date.

* It checks that the directory exists and is a directory (*does not exist*, *is
  not a directory*), and that **every index the header lists is in it and belongs
  to this file**. A directory without the index files gives *Cannot open index
  subfile 2 [2]*.
* **On success it prints nothing at all**, apart from the banner. Run `sdidx -q`
  to see what it did. A program that needs to know checks `-q`, which is how
  SD's own account restore uses it.
* Omit `akpath` to say "the indexes are in the data file's directory".
* It does not know about accounts. It will point a file at any directory you can
  write, inside the account or not. The account restore goes through a helper
  that keeps both paths in one account; typing `sdidx -p` yourself does not.

### `-d`, delete *(run)*

```
$ echo y | sdidx -d o4
Delete /tmp/sdi_demo/o4.idx (Y/N)? All indices deleted
```

The result is a file with no indexes: the header's index map is cleared. To get
the indexes back you create them and build them again with `create.index` and
`build.index`.

* If the indexes are relocated and the directory exists, it asks
  `Delete path (Y/N)?` and, on `y`, deletes that directory **and everything in
  it**.
* **Answering `n` still prints "All indices deleted" and still clears the header.**
  The directory stays on the disk, now referred to by nothing. *Run*: the `%2`
  was still there and `-q` said *File has no indices*. If you answer `n`, you have
  orphaned the index files and the file has lost its indexes.
* With indexes in the data file's own directory there is no question. It deletes
  the files (with the fault below) and clears the map.
* **If standard input ends at the question, the program loops for ever.** *Run*:
  killed by `timeout` after five seconds. Run it from a terminal, or give `echo y |`.

## The check that SD does not have the file open *(run)*

`sdidx` attaches to SD's shared memory when SD is running and looks through the
table of open files for the data directory's resolved path. If it finds one in use
it prints *File is currently open within SD* and exits 1, for every mode, `-q`
included. A program in a running sandbox opened the file and ran `sdidx -q` and
`-m` on it: both were refused; after `close` the `-q` succeeded.

That is all it does. **It does not look for a file held by another program, by
`sdfix` or by `sdconv`, and when SD is not running it checks nothing.** Do not
run it while any of those has the file.

## Faults found while writing this page *(run)*

1. **The old local index files are not deleted when the path is long.** `-m` (from
   local to elsewhere) and `-d` (local) delete each `%n` through a name buffer of
   33 bytes, so a data path with `/%2` after it longer than 32 characters is cut
   short, the delete misses, and the program prints *Overflowed path/filename
   buffer* (with the full name, not the cut one) and then reports success. Almost
   every real path is longer: `/home/sd/user_accounts/acct/orders` is 34 characters before the `/%2`.
   After the move the old `%2` is still in the data directory; after `-d` the
   file has no indexes but the `%2` is still there, and `sdfix` calls it *AK0
   subfile found but not expected*. Delete it by hand, after checking the move
   worked. **A stale `%2` also stops `-m` moving the indexes back**: *Cannot create
   new index subfile 2 [17]* (*run*).
2. **`-d` with the answer `n`** as above.
3. **Input that ends** as above.

The relocated cases (a directory that is deleted whole) are not affected by the first.

## What it will not do

* It does not check, rebuild or repair an index. Use `sdfix` to check one
  ([sdfix](14-sdfix.html)) and `build.index` to rebuild it.
* It does not take a backup, and does not warn before it deletes.
* It does not stop other programs using the file, and does not check the file is
  open anywhere except within SD.
* It does not change an index's definition, only where its files are. It cannot
  move one index and leave the others.
* It does not work on directory files, sequential files or other things that are
  not SD hashed files.
* It does not tell you what it did with `-p`.

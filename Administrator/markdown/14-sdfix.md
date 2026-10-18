Title: sdfix, the File Check Tool
Subtitle: Checking a hashed file's structure on disk, repairing what it can, recovering space and clearing dead space: when to run it, every option, and what it does to the file.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

`sdfix` is a stand-alone program, not an SD command. It reads and, with the
right options, **rewrites the files of an SD hashed file** directly on disk,
without going through SD. Use it when you suspect a file's structure is
damaged (after a crash, a full disk, a restore from a bad copy), or to give a
file back disk space it no longer needs. It has no effect on a file that is
sound.

> **How this page was made.** Everything here was read from `sdfix.c` and run on
> scratch copies of a small file in a private sandbox built from SD Core for
> Linux `Dev` (the program's banner reads `SDFIX L1.1-3`).
> Each result is marked *run* (the damage was made and the output is real) or
> *source* (read from the code, not provoked). It was not run on a large file,
> on a file owned by another user, or as root.
>
> **Revised 18 October 2026.** The first version of this page described the
> program as built at `Dev` commit `1adf913` and listed faults in it. Six were
> fixed on 18 October (see the end of
> [sdfix: what it checks and repairs](14a-sdfix-checks-and-repairs.html)), and
> this page describes the program as fixed. An older copy of `sdfix` behaves as
> the first version said.

## The short version

```
back up the file, close it everywhere (or stop SD), then:
/usr/local/sdsys/bin/sdfix /home/sd/user_accounts/acct/orders    # a check; changes nothing
```

* **Take a copy of the file first, whatever the options.** The file is a
  directory holding `%0` and `%1` (and `%2` onward for indexes); copy the whole
  directory with `cp -a`. `-F`, `-R` and `-Z` write into the file and none of
  them can be undone.
* **`sdfix` refuses a file that SD has open** (*run*): `File is currently open
  within SD`, `Status: 1`, and it reads nothing. It looks in the running SD's
  table of open files for the file's resolved path, so a symbolic link or a
  trailing slash makes no difference, and it does so for every option, a plain
  check included. **It checks nothing when SD is not running**, and it cannot see
  a file held by another program, `sdidx` or `sdconv`. Close the file in every
  session, or stop SD ([Installation](08-sd-installation.html) gives the
  commands). Older copies of `sdfix` processed a file a running session held
  open without a word.
* **A plain `sdfix file` is safe to run** on a file that nobody has open. It
  reads. The one exception is `-Z`, which writes (see below).
* **"Status: 0" does not mean the file is sound.** It means the program ran. A
  file full of errors still ends `Status: 0`.

## Where it is and who can run it

`/usr/local/sdsys/bin/sdfix`. Only `sd` is linked into `/usr/local/bin`, so
type the full path. The directory is readable by everyone, but the program opens
the file's subfiles for read and write: **you need write access to them**, even
for a check. Without it the file is reported as *No SD hashed files found
matching given name(s)* (*run*: a copy with the write permission removed), which
is easy to misread as "not an SD file". The users with the right are normally the
account's own user and `sdsys`.

**Do not run it with `sudo` unless you must.** New files are created with the
owner and umask of whoever runs the program. `-R` writes a new overflow subfile
(`%1`) and renames it into place, so after a run as root that file belongs to
root and the account's own user may no longer be able to write it. This was
*not run* as root here; check with `ls -l` after any run you did not make as
the file's owner, and `chown` it back.

It reads the configuration file named by the environment variable `SD_CONFIG`
or else `/etc/sd.conf`, and **stops with "*path* not found" if it cannot read
it**. The only item it looks at is `DEBUG` (see Interactive mode).

## The command line

```
sdfix {options} pathname ...
```

A pathname is the file's directory, as an operating system path, not an SD
file name and not a VOC entry. Options start with `-`, may be joined in one word
(`-BF`), and are not case sensitive. Several files may be named; each is
processed in turn. A path that is not an SD hashed file is skipped without
comment, and if none was found the program says *No SD hashed files found
matching given name(s)*.

| Option | What it does |
|---|---|
| `-C` | Check the file. This is the default when no other mode is given. |
| `-F` | Check, and **fix every error it knows how to fix, without asking.** Not combinable with `-Q`. |
| `-Q` | Check, and **ask `Fix?` at each error it knows how to fix.** Answer `y` or `n`. Not combinable with `-F`. |
| `-R` | Recover disk space: shrink the primary subfile and rewrite the overflow subfile with the free blocks squeezed out. **Not combinable with `-F` or `-Q`** (*run*): `-r cannot be combined with -f or -q: run the fix first, then -r on its own`, status 1, and the file is not touched. (Older copies accepted the combination, ran neither the check nor the repair, and recovered space from an unchecked file.) Add `-C` or `-Z` to make it check first. |
| `-Z` | Clear the dead space at the end of each group (implies `-C`). **Writes to the file.** |
| `-B` | No progress bar. Use it when you log or redirect, since the bar is drawn with carriage returns. |
| `-V` | Verbose. Changes the output of `-R` only; it does nothing to a check. Not listed in the usage text. |
| `-L` | Log everything the program prints, except the banner, to `sdfix.log` in the current directory. |
| `-Lname` | The same, to the file `name`. The rest of the word is the name, so put `-L` last in a joined word (`-BLcheck.log`). An existing log is overwritten. |
| `-I` | Interactive mode. Refused unless the configuration file sets `DEBUG` with bit 2 on. Not listed in the usage text. See below. |

The usage text printed for a bad option names only `-F`, `-L`, `-Q`, `-R` and
`-Z`; `-B`, `-C`, `-V` and `-I` work but are not listed. *Run.*

**Exit status.** The program's status is that of the **last** pathname: 0 if it
could be processed, 1 if it was not a hashed file, could not be opened, or its
overflow subfile had a wrong magic number. Finding and even fixing errors gives 0. Each file
also prints a line ` SDFIX processed:  name   Status: n`.

### Paging, and what happens when input runs out

Output stops every 24 lines with *Press return to continue...* (the program
reads standard input one character; `q` quits, `s` stops paging). The `Fix?` and
*Dump and rebuild* questions also read standard input.

**If standard input ends while `-Q` is asking `Fix?`, the end of input is taken
as `n`** (*run*): the program prints `Fix? N (end of input)`, repairs nothing,
and carries on with the check without waiting for any further answer. At the
*Press return* pause the end of input means "stop paging". The *Dump and
rebuild* question uses the same routine (source; not run separately). Older
copies looped for ever at `Fix?` (`sdfix -Q file < /dev/null` was still
running when `timeout` stopped it after five seconds). To answer the questions
from a script, feed every answer, starting with `s` to stop the paging:
`printf 'sY' | sdfix -B -Q file`.

## A check, with nothing wrong *(run)*

```
$ sdfix zzcust
[ SDFIX L1.1-3   Copyright, Ladybridge Systems, 2007.  All rights reserved. ]

Processing zzcust
Checking file header...
Checking data groups...
*************************-------------------------| 1/2**************************************************| 2/2
Checking free chain...
Checking for unreferenced blocks...
0 overflow blocks allocated, 0 on free chain
 SDFIX processed:  zzcust   Status: 0
```

The row of asterisks is the progress bar: it is redrawn on one line and appears
like this when the output is captured. A file that has indexes adds
*Checking AK 0*, *Checking AK free chain* and *Checking I-type chain*.

## Fixing errors *(run)*

A scratch file was damaged so that its minimum modulus and its header record
count were wrong. A check reports them and changes nothing:

```
Minimum modulus is invalid (1660944384)
Record count error: Actual 000000000040, file header (adjusted) 000117440511
```

With `-Q`, answering `n` and then `y`:

```
Minimum modulus is invalid (1660944384)
Fix? N
Record count error: Actual 000000000040, file header (adjusted) 000117440511
Fix? Y
   Corrected by updating header
```

The first error is still there on the next run; the second is gone. `-F` does
the same for every error, with no questions. Which errors can be fixed, and how,
is on the next page of this set, [sdfix: what it checks and repairs](14a-sdfix-checks-and-repairs.html).
That page also covers the dump-and-rebuild of mis-hashed groups, interactive
mode, and the faults in the tool that were found while writing these pages and
fixed afterwards.

## Recovering space with `-R` *(run)*

A file that once held 3,000 records and now holds 305 keeps all the disk it
grew to: `%0` was 428,032 bytes and `%1` 223,232.

```
$ sdfix -B -R zzbig
Processing zzbig
Recovering space
Overflow subfile contracted to 32768 bytes
 SDFIX processed:  zzbig   Status: 0
```

Afterwards `%0` was 69,632 bytes and `%1` 32,768. The 305 records were read back
through SD and all were present and the right length (the five long records
among them). `-V` adds a line for every block it moves.

**`-R` rewrites the file in place and is the most dangerous option.**

* It first empties the file's free chain in the header, then rewrites the
  primary subfile's links group by group. From that point the old overflow
  subfile no longer matches the primary subfile. If the run stops part way (a
  full disk, a kill, a power cut) the program says *The original file is no
  longer usable* if it notices, and **the only remedy is your copy.**
* It does not touch the index subfiles. The source says they were too hard to
  shrink, so an indexed file keeps its index sizes.
* It does not check the file first unless you also give `-C` (or `-Z`), and
  `-F` and `-Q` are refused alongside it. **Run a check, and `-F` any errors in
  a separate run, before you recover space**, not after.

## Clearing dead space with `-Z` *(run)*

When a record is deleted or shortened, the bytes after the used part of a block
keep their old text. `-Z` zeroes them. It does not change a record. It makes a
file compress better and stops old text lingering in a backup, and the file
works the same without it.

```
$ sdfix -B -Z zzbig
...
Dead space cleared in 18 block(s)
...
$ sdfix -B -Z zzbig
Dead space cleared in 0 block(s)
```

It walks the groups in the primary subfile and the overflow blocks chained from
them. It does **not** clear free overflow blocks (those on the free chain), and
it does not visit the blocks that hold a large record's data (source, not
provoked). Unlike a plain check it
**writes**, so back up and close the file first, as for `-F`.

## Writing it down

Give `-L` when a run matters, so there is a record:

```
sdfix -B -F -Lfix-20261018.log /home/sd/user_accounts/acct/orders
```

The log has everything but the banner and the progress bar, and the lines
` SDFIX processed:  name   Status: n`.

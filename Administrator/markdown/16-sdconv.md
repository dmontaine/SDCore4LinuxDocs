Title: sdconv, the Byte Order Convertor
Subtitle: A tool for turning compiled program files between big-endian and little-endian form: what it converts in this build, what it refuses, and why you will rarely need it.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

`sdconv` was written to move SD files between computers that store numbers in
opposite byte orders. SD Core for Linux is built and tested here on a
little-endian machine (x86-64). Nothing on this page can say whether a result
would run on a big-endian machine, because there is none to run it on.

> **Read this first: `sdconv` does not convert hashed files.** Given one it says
> so, changes nothing and exits 1. It converts **compiled program files** only,
> and only the header of each. *Run*, below. (Before 18 Oct 2026 it printed
> nothing and exited 0, which read as a successful conversion; an older copy
> still does.) The routine that converts a hashed file's subfiles is in the
> source, but the program does not call it, and this SD cannot open a
> big-endian hashed file, so a converted file would be of no use here. Linux and
> Windows are both little-endian.

> **How this page was made.** Everything here was read from `sdconv.c` and run on
> scratch copies in a private sandbox built from SD Core for Linux `Dev` at
> commit `1adf913` (banner `SDCONV L1.1-3`). Results are marked *run* where the
> output is real. It was not run as another user or as root.

## The short version

* **You almost certainly do not need it.** SD loads a program whose header is in
  the other byte order and swaps the header in memory; the file is left as it is.
  *Run*: a program converted with `-B` ran correctly, and the file was still
  big-endian afterwards. Only the header was converted there, so this shows that
  SD tolerates a flipped header, not that a program compiled on a big-endian
  machine would run.
* **Every conversion rewrites the file in place with no copy.** Take your own
  copy first.
* **It rewrites even a file that needs no conversion.** *Run*: a program already
  in the right order had its modified time changed by `sdconv -L`.
* **A hashed file is refused: a message, the file untouched, exit status 1.**
* **A path that is neither a hashed file nor a program object is skipped with no
  message and the exit status is 0**, including a path that does not exist.

## Where it is and who can run it

`/usr/local/sdsys/bin/sdconv`. Only `sd` is linked into `/usr/local/bin`, so type
the full path. It opens each file for read and write, so you need write access
to it. A file it cannot open for writing is skipped without a word. It takes no
configuration file. Run it with SD stopped, or on files SD is not using: it
makes no check for that.

## The command line

```
sdconv {options} pathname ...
```

| Option | What it does |
|---|---|
| `-B` | Convert to big-endian. |
| `-L` | Convert to little-endian. |
| `-D` | Debug. It is accepted, is not listed in the usage text, and **does nothing** for a program file: the progress it would print belongs to the hashed-file routine that is not called. *Run*: no extra output. |
| (neither `-B` nor `-L`) | Convert to the byte order of the machine it is run on, which here is little-endian, so the same as `-L`. |

Options may be joined in one word (`-BD`) and are not case sensitive. If both
`-B` and `-L` appear, the last one wins. Several pathnames may follow, and the
shell may expand a wildcard (`bp.out/*`). The program does not descend into a
directory: a directory that is not a hashed file is skipped. With no pathname,
or an option it does not know, it prints the usage text and exits 1.

```
$ sdconv

Usage: SDCONV {options} pathname(s)

Options:
   -B      Force conversion to big-endian
   -L      Force conversion to little-endian

Only compiled programs are converted; a hashed file is refused (exit status 1).
```

(preceded, as always, by the banner.) A run that did something looks like a run
that did nothing:

```
$ sdconv -B objfile
[ SDCONV L1.1-3   Copyright, Ladybridge Systems, 2007.  All rights reserved. ]

$ echo $?
0
```

The only failures it reports are *Cannot read name*, *Error converting name*, a
seek or write error naming the file, and *Cannot allocate memory for name*, and
only for a file it had already recognised as a program object.

## What it converts: compiled program files *(run)*

A compiled program is a plain operating system file that begins with a one-byte
marker, `0x64` for little-endian and `0x65` for big-endian. SD keeps them in:

* the `.out` directory beside each program file (`bp.out` holds the compiled
  form of the programs in `bp`; `gpl.bp.out` and `pcode.out` are others), and
* the global catalogue, `gcat` in the SDSYS directory. An account's own `cat`
  directory is the local catalogue; it was empty in the sandbox, so it was not
  looked at.

A file whose first byte is neither value, or that is shorter than the 165-byte
header, is not touched.

```
before   64 00 00 00 00 00 bf 01 00 00 00 00 08 00 68 00
after -B 65 00 00 00 00 00 00 00 01 bf 00 00 00 08 00 68
```

(the first 16 bytes of a global catalogue entry, before and after). Then
`sdconv -L` on the same file restored it **byte for byte**, and a second `-B` on a
file already big-endian changed nothing.

**Only the object header is converted**: the program id, the start offset, the
argument, variable and stack counts, the offsets of the symbol and line tables,
the object size, the flags and the compile time. The compiled code, the symbol
tables and the constants are not touched. SD's own source says that floating
point constants are the one thing in the code that needs swapping, and that SD
does it when it loads them.

## What it does not convert: hashed files *(run)*

```
$ ls zzcust; sdconv -B zzcust; echo rc=$?
%0  %1
zzcust is a hashed file: sdconv converts compiled programs only, nothing was changed
rc=1
```

`%0` and `%1` are byte for byte as before, with `-B`, with `-L` and with no
option. The source has a routine, `process_file`, that would convert the header,
the data groups and the index nodes with a "partly converted" marker for a run
that stops part way. It was commented out of `convert_file` in a compiler-warning
clean-up, nothing records a decision to do that, and it has faults of its own
(an endless loop on an unknown block type, a 64-bit field cut to 32 bits, two
buffer overflows, no open-file check and no backup), so it is not used.

**A hashed file taken to a machine of the other byte order cannot be converted by
this tool, and this SD could not open it if it were.** The change-log entry that
once said a conversion of a file "carries the sequential counter over; sdconv
reverses it" was wrong and has been removed.

## What it will not do

* It will not convert a hashed file; it tells you so and exits 1.
* It will not report a path it skipped, a file it could not open, or one that was
  not a program object. The exit status is 0 for all of them.
* It will not make a copy, and will not reverse a conversion except by running it
  again the other way on a file that was converted completely.
* It will not convert the compiled code of a program, only its header.
* It will not tell you whether the file needed converting.
* It does not move or check index files ([sdidx](15-sdidx.html)) or check a
  file's structure ([sdfix](14-sdfix.html)).

Title: SD Basic - System and Environment
Subtitle: Asking SD about itself, about the machine, and about the session you are in.

This page covers the enquiries: what time is it, who am I, where is the data,
what did the last thing that failed say, and what may this account do. Most of
it is one function, `system()`.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

> **Values that are particular to one machine — a user number, a computer
> name, a process id — are marked as examples; the shapes are not.** What you
> see back will differ in the value and match in the form.

## SYSTEM()

```
system(key)
```

### The session

| Key | | Value |
|---|---|---|
| `7` | terminal type | `linux` |
| `9` | CPU time used, ms | `45` |
| `12` | time, as `time()` | `70787` |
| `18` | **user number** | `67` (example) |
| `23` | break key enabled? | `1` |
| `24` | echo enabled? | `1` |
| `25` | is this a phantom? | `0` |
| `26` | prompt character | `?` |
| `1000` | `capturing` in effect? | `0` |
| `1029` | internal subroutine depth | `0` at the top, `1` inside a `gosub` |
| `1030` | login time, internal | `1851017987` |
| `1031` | operating system process id | `605` (example) |
| `1050` | administrator? | `0` |

### The machine

| Key | | Value |
|---|---|---|
| `31` | licence number | `0` |
| `42` | IP address | *empty* |
| `91` | is this Windows? | `0` — this port is never Windows |
| `1006` | Windows NT style? | `0` — vestigial, never set on this port |
| `1009` | endian — 0 little | `0` |
| `1010` | platform name | `Linux` |
| `1012` | SD version | `L1.1-3` |
| `1013` / `1014` | user limit, without / with the phantom pool | `20` / `20` |
| `1015` | computer name | `myhost` (example) |
| `1017` | port number of a tcp connection | `0` |
| `1028` | system id | `1028` |

**`system(91)` and `system(1006)` are both Windows-only questions, and
both read `0` here — that is not a keys-to-leave-alone caveat, it is the
correct answer.** `system(1010)` is the one that actually tells you the
platform: `Linux`, reliably.

### Paths — one form, no translation layer

| Key | | Value |
|---|---|---|
| `32` | the `sdsys` directory | `/usr/local/sdsys` |
| `38` | the temporary directory | `/tmp` (example — falls back to the system default when `TEMPDIR` is unset in `sd.conf`) |
| `1011` | the configuration file | `/etc/sd.conf` |
| `1024` | the directory SD was started in | `/home/don/myproject` (example) |

**Unlike SD Core for Windows, which reads paths back in up to three
different spellings** (a backslash path, a POSIX `/cygdrive/` path, and a
forward-slash drive path, because its runtime sits on top of a POSIX
emulation layer) **— there is only one spelling here.** This port runs
natively, so every path `system()` returns is an ordinary Linux path, and
`@sdsys` and `@path` agree with it without any conversion to worry about.

### Lists and structures

| Key | | |
|---|---|---|
| `1002` | the call stack | field per level: `path`, then `offset` and line pairs — `.../BP.OUT/ZZMATH` at line 41, then `$CPROC` |
| `1003` | open files | field per file, `unit` and path. **`$ipc` is always one of them** |
| `1025` | environment variables | **two fields**: field 1 every name, field 2 every value, value-mark separated |

`system(1025)` returns **2** fields, every name in the first — it is not a
list of `NAME=value` pairs.

### Time

| Key | | |
|---|---|---|
| `1005` | internal time | `date() * 86400 + time()` — the difference is **0** |
| `1020` | milliseconds since midnight | `9587454` |

`system(1020)` is the one to time something with: against a lock wait it gives
252 ms where `time()` gives 0.

### Where a file or an account is: `vocpath()` and `account.path()`

```
vocpath(filename {, dict.flag})
account.path(account)
```

`vocpath()` gives the operating system pathname of a file named through the VOC:
the data part, or the dictionary part if `DICT ` is written in front of the name
or the second argument is true. The file is opened as `open` opens it, so a
Q-pointer and the other forms `open` takes are resolved as `open` resolves them.
`status()` is 0 if it was found; a null string comes back with the error of the
open if it was not. `account.path()` gives the directory of an account from the
accounts register, in either case of the name, and a null string when there is no
such account.

**A path is told only where the account could open it.** The account's own
directory and the files in it always; anything else only to an account that has
the OS access gate, and to any other the answer is a null string (with `status()`
3035 from `vocpath()`). So a program cannot learn where another account lives, or
which accounts there are, by asking.

### Unique values, and a few more

| Key | | Value |
|---|---|---|
| `14` | characters waiting at the terminal | a snapshot; for **piped input** it is only what has been read ahead, so do not rely on it |
| `20` | print jobs passed to the spooler | a count for the whole system since SD started, all sessions together. openQM gives the job's reference; SD does not read the spooler's own job number back |
| `19` | a unique value from the date and time | two five digit numbers, the day and the second; a second value in the same second, from **any** process, gets a letter on the end (`a`, `b` … `z`, `aa`). The time is the process's own, so two users in different time zones can get the same value |
| `21` | a unique value from the date and a sequence | two five digit numbers, the day and a count that starts at 1 again each day |
| `45` | the name of the running program | its catalogue name |
| `1048` | a sequence number | unique across all sessions until SD restarts, then 1 again |
| `1049` | is `hush` in effect? | `0` or `1` |
| `1062` | has `signal()` been raised for this process? | `1` and **cleared by reading it**: `until system(1062)` is the loop of a phantom that waits to be told |
| `1067` | the default group size of a dynamic file | in bytes |
| `1071` | the `status` array of the last `osread` | null before any `osread`, and after one that failed; the information the system gave about the file that was read. Held per process |
| `1073` | the phantoms grouped with this process | their user numbers, field mark delimited (`phantom group`; `system(1058)` lists every child) |
| `1086` | are string comparisons case sensitive in this program? | `0` after `$nocase.strings` or `casing off` |
| `1088` | where `maximum()` or `minimum()` found its element | the field, value and subvalue numbers joined by value marks: for `'61' : @vm : '42' : @fm : '71' : @vm : '57'` the maximum is `71` and `system(1088)` is `2` vm `1` vm `1`. The first of equal elements is the one. Null when the array has no number |

`signal(userno)` raises the flag in another process and is true if that process
is logged in. **SD signals only a process of the same login user**, or any
process when the caller is the administrator; to any other it gives false and
nothing happens. `child(userno)` is true while a phantom this process started
is running. See [SD TCL - Processes and Phantoms](30-sd-tcl-processes-and-phantoms.html).

## DATE, TIME and TIMEDATE

```
date()      time()      timedate()
```

Taken together at one instant:

| | |
|---|---|
| `date()` | `21423` — days since 31 December 1967 |
| `time()` | `70787` — seconds since midnight |
| `timedate()` | `19:39:47 26 AUG 2026` |
| `oconv(date(), 'D4-')` | `08-26-2026` |
| `oconv(time(), 'MTS')` | `19:39:47` |

`@date` and `@time` hold the same numbers, **but they are set once per command**
rather than read afresh, so in a long loop they do not move while `date()` and
`time()` do.

`timedate()` returns a formatted string, not a number. Do not do arithmetic on
it — see
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html) for the
conversion codes.

## ENV()

```
env(name)
```

**`env()` is case sensitive, the ordinary Linux rule** — a wrong case
looks exactly like a missing variable, because on Linux it *is* a
different name.

| | |
|---|---|
| `env('PATH')` | non-empty |
| `env('path')` | **empty** — no such variable, lower case |
| `env('HOME')` | your home directory |
| `env('NOSUCHVAR')` | empty |

**Get the spelling from `system(1025)` field 1 rather than from memory**
if you are ever unsure what a variable is actually called in this
session's environment.

## CONFIG()

```
config(name)
```

On a stock installation:

| | |
|---|---|
| `config('GRPSIZE')` | `4` |
| `config('MAXIDLEN')` | `63` |
| `config('NUMFILES')` | `80` |
| `config('NUMLOCKS')` | `100` |
| `config('SORTMEM')` | `4096` |
| `config('SPOOLER')` | empty |

**The name is case sensitive and at most eight characters. both failures now
look the same**, which is the point — a name that is too long is a name that
does not exist, and a caller cannot tell the two apart:

| | |
|---|---|
| `config('numlocks')` — right name, wrong case | empty, `status()` **1004** |
| `config('NOSUCHKEY')` — **nine** characters | empty, `status()` **1004** |

**Keep every `config()` name to eight characters and upper case.**

`config('TIMEZONE')` is the zone the epoch functions convert in (see
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html)); `config('USPLIT')`
is `1` when the administrator has turned on the split of user numbers.

Neither call aborts the caller: a name that is too long comes back empty with
a status, the same as a name that does not exist.

## SYSMSG()

```
sysmsg(number {, substitution ...})
```

Returns the text of one of SD's own messages, with `%s` substitutions filled
in.

| | |
|---|---|
| `sysmsg(2831)` | `Unrecognised statement` |
| `sysmsg(6711, 'ABC')` | `Unable to find source record ABC` |
| `sysmsg(2201)` | `Account name '' is not in register` — an unfilled substitution comes back empty |
| `sysmsg(99999)` | `[99999] Message not found` |
| `sysmsg(1)` | `[1] Message not found` |

**A message number is not a `status()` code.** They are separate numbering
schemes that overlap. `status()` **3006** is *record not found*; `sysmsg(3006)`
is `Modes: `. Do not render a status code by passing it to `sysmsg()`.

`get.messages()` takes **no arguments** and returned **nothing** — zero fields
— in an ordinary session. It reports messages sent between sessions, and
nothing had sent any.

## Continued in

[SD Basic - Status, Encryption and the
Machine](16a-sd-basic-status-and-the-machine.html) — status codes, checksums,
encryption, umask, the @variables, os.execute and logmsg.

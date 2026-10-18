Title: Configuration
Subtitle: The sd.conf file, the two ways to read a setting, and every parameter SD accepts.

SD reads one configuration file at start-up. It sizes the shared memory
segment, sets the limits every session inherits, and names the directories SD
writes to.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case.

> The parameter list and categories on this page are read from `config.c`
> itself (`tools/confmap.py`, 22 Sep 2026), not from a live `:config`
> capture on this port — the sample output below is illustrative, ported
> from a real SD Core for Windows capture with Linux's own values swapped
> in where they differ.

## The file

```
/etc/sd.conf
```

The server and the client both read the `SD_CONFIG` environment variable
first and fall back to that path (`sddefs.h`'s `SD_CONFIG_ENV`/
`SD_CONFIG_DEFAULT` — one pair of names, both sides of the client/server
split).

It is plain text in one section:

```
[sd]
SDSYS=/usr/local/sdsys
GRPSIZE=2
NUMUSERS=20
USRDIR=/home/sd/user_accounts
GRPDIR=/home/sd/group_accounts
DUMPDIR=/usr/local/sdsys/dumps
```

Lines beginning `#` are comments. The shipped file is heavily commented and
those comments record why each value was chosen. Read them before changing
anything.

### A name SD does not recognise stops it starting

An unrecognised parameter is not ignored. The parser abandons the file with
`Unrecognised configuration parameter`, and SD does not start.

That is why obsolete names are still parsed rather than deleted. `CREATUSR` has
done nothing since 14 August 2026, but a configuration file copied from a Linux
installation still carries it, and removing the branch would turn a tidy-up
into a failure to start.

Range failures behave the same way. `GRPSIZE`, `INTPREC`, `LPTRHIGH`,
`LPTRWIDE`, `MAXCALL`, `RECCACHE`, `SORTMRG` and `MAXIDLEN` are bounds-checked
once the file has been read, and a value outside its range stops start-up with
a message naming the parameter.

## Reading the settings

The `config` verb reports what is in force:

```
:config
Virtual Machine Version Number W1.0-0
APILOGIN  1
CMDSTACK  99
DEADLOCK  0
DUMPDIR   /usr/local/sdsys/dumps
ERRLOG    50 kb
...
YEARBASE  1930
```

SD accepts **50** parameters on this port (`APIPORT` and `NETDIRS` do not
exist here — see *The API*, below) and the verb prints **42** of them.
Eight are accepted in the file and never displayed: `CODEPAGE`, `CREATUSR`,
`DEBUG`, `FDS`, `FIXUSERS`, `PORTMAP`, `SDSYS` and `TXCHAR`.

The `config()` function reads one parameter from a program:

```
group.size = config('GRPSIZE')
```

**47 parameters are readable this way.** The three that are not are `CREATUSR`,
which stores nothing, `SDSYS`, and `TXCHAR`. The name is truncated to eight
characters before it is matched; no parameter name is longer than eight, so
that only shows up if you pass something which is not a parameter.

Two further forms exist. `config lptr` reports the settings of the default
printer, and `config gpl` and `config contrib` display the licence and the list
of contributors.

## Changing a parameter

Editing `sd.conf` and restarting SD is the durable route, and for most
parameters it is the only one.

**28 parameters can also be changed for the current session:**

```
config sortmem 8192
```

That writes to the session's own copy of the settings, taken from shared memory
when the session started. It does not reach `sd.conf`, it does not affect any
other session, and it is gone when the session ends.

The 28 are `CODEPAGE`, `DUMPDIR`, `EXCLREM`, `FILERULE`, `FLTDIFF`, `FSYNC`,
`GDI`, `GRPSIZE`, `INTPREC`, `LPTRHIGH`, `LPTRWIDE`, `MAXCALL`, `MUSTLOCK`,
`OBJECTS`, `OBJMEM`, `RECCACHE`, `RINGWAIT`, `SAFEDIR`, `SDCLIENT`, `SH`,
`SH1`, `SORTMEM`, `SORTMRG`, `SORTWORK`, `SPOOLER`, `TEMPDIR`, `TERMINFO` and
`YEARBASE`.

Everything else takes effect only when SD is next started. That includes every
limit which sizes the shared memory segment and every setting the API listener
reads.

## Sessions and limits

| Parameter | Default | Effect |
|---|---|---|
| `NUMUSERS` | 20 | Maximum concurrent sessions. Sizes the user table in shared memory |
| `NUMFILES` | 80 | Maximum open files across all sessions |
| `NUMLOCKS` | 100 | Maximum record locks across all sessions. Range 1 to 32767 (the lock table's cells are 16 bits; a value outside it stops SD starting, which it did not before the check of 16 Oct 2026, when 40000 wrapped) |
| `MAXCALL` | 10000 | Maximum subroutine call depth. Range 10 to 1000000 |
| `CMDSTACK` | 99 | Depth of the command stack |
| `FDS` | unset | Limit on file descriptors. No limit when unset |
| `FIXUSERS` | unset | `base,range` — user numbers reserved for sessions that ask for a specific number |
| `PORTMAP` | unset | `base_port,base_user,range` — gives a session a fixed user number derived from the port its connection arrived on. Refused if the range overlaps `FIXUSERS` |
| `USERPOOL` | 1023 | The highest user number handed out; user numbers rotate through 1 to this, 0 always takes the lowest free one |
| `USPLIT` | 0 | `1`: interactive sessions take the lowest free user number and every other process (a phantom, an API session) the highest free one in 1 to `NUMUSERS`, so the two never meet. `FIXUSERS`, `PHANTOMS`, `PORTMAP` and `USERPOOL` are ignored while it is on. `config('USPLIT')` reads it |
| `PHANTOMS` | unset | `base,range` — user numbers kept for phantoms started with `phantom user n`. Nobody else is given one: not a session, not an API session, not a phantom started without `user`. It must lie between 1 and the highest user number and must not overlap `FIXUSERS` or `PORTMAP`, or SD will not start. `config('PHANTOMS')` reads it as `base,range`, null when none are kept |
| `CLEANUP` | 300 | Seconds between the checks that look for sessions that ended without logging out (a killed terminal, a lost connection) and clear them from the user table. 30 to 3600. The daemon wakes every ten seconds, so an interval is kept to within ten seconds; a very short one costs a pass over the user table that often. `config('CLEANUP')` reads it |

## Files and locking

| Parameter | Default | Effect |
|---|---|---|
| `GRPSIZE` | 2 | Default group size for a new dynamic file, in 1 KB units. Read by `create.file` and `configure.file` when no group size is given |
| `MAXIDLEN` | 63 | Maximum record id length. 63 is also the lower bound |
| `MUSTLOCK` | 0 | When 1, a `write` or `delete` requires the record to be locked first |
| `DEADLOCK` | 0 | When 1, SD traps deadlocks |
| `SAFEDIR` | 0 | When 1, directory files are updated by write-and-rename rather than in place |
| `RECCACHE` | 0 | Records cached per file. Range 0 to 32 |
| `FSYNC` | 0 | Bit flags controlling when SD forces data to disk |
| `FILERULE` | 0 | Bit flags deciding which special VOC file references are honoured: bit 1 `account:file`, bit 4 `path:` followed by a pathname, and bit 2 `system:account:file`, which opens nothing on this port. See below the table of inert parameters |

## Directories

| Parameter | Default on a new install | Effect |
|---|---|---|
| `SDSYS` | `/usr/local/sdsys` | The system account. SD does not start if the global catalogue is not found beneath it |
| `USRDIR` | `/home/sd/user_accounts` | Where `create.account` puts a user account |
| `GRPDIR` | `/home/sd/group_accounts` | Where `create.account` puts a group account |
| `DUMPDIR` | `/usr/local/sdsys/dumps` | Where process dumps are written |
| `TEMPDIR` | unset | Temporary files. Falls back to the system default when unset |
| `SORTWORK` | unset | Work files for a sort that does not fit in memory. Falls back to the system default when unset |
| `TERMINFO` | empty | An additional terminfo directory. The shipped definitions are found without it |

`DUMPDIR` is set rather than left empty on purpose. A blank value falls back to
the system directory, which SD users can write to, and a process dump carries
the whole variable state of the session that wrote it. The installer makes the
dump directory write-only to SD users, so a dump can be added and nobody else's
can be listed or read.

## The API

| Parameter | Default | Effect |
|---|---|---|
| `APILOGIN` | 1 | Whether the API requires authentication. `0` is the weaker setting, not the safer one |
| `SDCLIENT` | 0 | Restricts what an API session may do. Non-zero disables file access outright (no file can be opened, so no dictionary can be evaluated either) and refuses `SDIConv`, `SDOConv`, `SDIConvs` and `SDOConvs` a conversion code that reads a file (`T` with a file) or calls a program (`U`); any non-zero value also refuses `SDOpenSeq` and `SDExecute`; `2` additionally refuses any subroutine not compiled as callable from a client (a subroutine whose name begins with `$` must be so compiled at every setting, `0` included). Before 15 Oct 2026 the refusal at `2` was reported but the subroutine still ran |

**There is no `APIPORT` and no `NETDIRS` on this port — a real structural
difference, not an oversight.** SD Core for Windows sizes its listener from
`sd.conf` at start-up and restarts SD itself to change it; here, whether SD
listens for the API at all is `systemd`'s `sdclient.socket` unit, activated
independently of any running `sd` process (see *Remote access and the
machine*, in this set), and who may reach it is the firewall (`ufw`, or firewalld on Fedora), moved
by the `remote.api` verb rather than by editing this file. **And there is
no config-file mechanism here that widens an API session's reach beyond
its own account** — Windows's `NETDIRS` names directories every API session
in every account may additionally open; this port has nothing playing that
role, so an API session's file access is exactly its own account's, full
stop. (The `os-on` switch is read for an API session like any other, but it
does not lift that confinement — see *Accounts and Security*.)

`SDCLIENT` is not reported by the `config` verb and has no entry in the shipped
`sd.conf`. It defaults to 0, which permits everything.

## Printing

| Parameter | Default | Effect |
|---|---|---|
| `LPTRWIDE` | 80 | Default page width for the printer. Range 10 to 1000 |
| `LPTRHIGH` | 66 | Default page depth for the printer. Range 10 to 32767 |
| `SPOOLER` | empty | The spooler to hand print jobs to |
| `GDI` | 0 | Selects the Windows printing interface used by default |

## Sorting

| Parameter | Default | Effect |
|---|---|---|
| `SORTMEM` | 4096 kb | Above this much data a sort works on disk instead of in memory |
| `SORTMRG` | 4 | Files merged at once in a disk sort. Range 2 to 10 |

## Numbers and dates

| Parameter | Default | Effect |
|---|---|---|
| `INTPREC` | 13 | Digits of precision in integer arithmetic. Range 0 to 14 |
| `FLTDIFF` | 0.00000000002910 | Two floating point numbers closer together than this compare equal |
| `YEARBASE` | 1930 | The century a two-digit year is read into |

## Diagnostics

| Parameter | Default | Effect |
|---|---|---|
| `ERRLOG` | 50 kb | Size of the error log. A non-zero value below 10 KB is raised to 10 KB, and the oldest entries are discarded when it fills |
| `PDUMP` | 0 | Bit flags controlling when a process dump is written |
| `DEBUG` | unset | Bit flags enabling debugging features |
| `STARTUP` | empty | A command run when SD starts |
| `OBJECTS` | 0 (no limit) | Compiled programs held in memory at once |
| `OBJMEM` | 0 (no limit) | Memory those programs may occupy, in KB |

## The screen

| Parameter | Default | Effect |
|---|---|---|
| `SCREENTHEME` | unset (`mono`) | The colour theme that a program using the `SCREEN` statement gets when it does not choose one: `mono`, `classic` or `blue`. `mono` uses only reverse video and underline and reads on any terminal. A name that is not a theme, or a colour theme on a terminal that cannot show colour, is ignored without an error and the screen stays `mono`. A program that asks for a theme gets that one. A program reads the value with `config('SCREENTHEME')` |

## The shell

| Parameter | Default | Effect |
|---|---|---|
| `SH` | `/bin/bash -i`, unset in the file | The shell a bare `sh` starts |
| `SH1` | `/bin/bash -c`, unset in the file | The shell `sh command` uses |

Unset falls back to the compiled-in default:

```
SH        /bin/bash -i
SH1       /bin/bash -c
```

**Both run at the account's own Linux permissions, and only for an account
that has the `sh-on` switch** (see *Accounts and Security*, "The
operating-system switches: `sh-on` and `os-on`"); the setting says which
shell it is, the switch says who may use it. Operating system access has its
own page in this set.

## Parameters that are accepted and do nothing

These are parsed so that an existing `sd.conf` still loads. None of them
changes SD's behaviour, and none should be offered to a site as a control.

| Parameter | Why it is inert |
|---|---|
| `JNLMODE` | Stored, shown by `config` and readable with `config('JNLMODE')`. SD has no journalling: nothing reads the value and nothing writes a journal. Checked by setting `JNLMODE=3` and `JNLDIR` to an empty directory, writing 50 records and deleting one: the directory stayed empty and `fileinfo(f, 1010)`, the file's journal number, was 0 |
| `JNLDIR` | The same: stored, shown, readable with `config('JNLDIR')`, and used by nothing. The journal error codes 8801 to 8804 are in the error table, and nothing in the kernel raises them (searched in the source) |
| `CREATUSR` | SD has accounts rather than accounts and users, so `create.account` always creates the operating system account and there is nothing to opt in to. The value is discarded as it is read |
| `CODEPAGE` | Stored, readable and settable. Nothing acts on it |
| `EXCLREM` | Stored, readable and settable. It described leaving remote files out of an account save. Nothing reads it |
| `RINGWAIT` | Stored, readable and settable. Nothing acts on it |
| `TXCHAR` | Stored, and not readable — there is no `config('TXCHAR')` |

**`NETFILES` is not in this list, but it is not what SDNet uses either.**
SDNet is the way a program opens a file that lives on another SD server: a VOC
entry of type `N`, a server you define with `set.server`, and a per-account
`net-on` switch, all off until SDSYS turns them on. It is built and is
described on the SDNet page of this set, with what has and has not been tested
(no two real machines have been connected yet). None of it reads `NETFILES`,
and the older SDNet that was removed on 9 September 2026 (a `server;file` VOC
entry, with each server's password in `sd.conf`) is still gone: that form of
name is refused. `NETFILES` is parsed, stored, shown by `config` and readable
with `config('NETFILES')`, and setting it to 2 made `config` show 2. **One
thing in the source reads it:** the API server's request 29, "open an SDNet
file", answers "Remote server disallowed access" (7009) unless bit 2 of
`NETFILES` is set, and the files-only API route refuses request 29 whatever the
value is. That was read from `apisrvr`; no client function sends request 29,
so it was not run. The value is 0 unless `sd.conf` sets it, and the installer
does not, so the request is refused as delivered. Leave it at 0.

`FILERULE` is **not** in this list, and is easy to mistake for it. It is a set
of bits that decide which special VOC names are honoured when the name is not
a VOC entry: bit 1 allows `account:file`, bit 4 allows `path:` followed by a
pathname, and bit 2 allows `system:account:file`, a form that names another
system. In a test with `FILERULE=7`, `sdsys:bp` and `path:/tmp` opened;
`localhost:sdsys:bp` did not (the open failed with status 3003), because this
port has nothing that reaches another system by that form. With `FILERULE`
at 0, none of the three opened. The `path:` form is still held to the
account's operating-system access switches.

There is no licence parameter and no licence verb. SD Core for Windows is
GPL v3 and is not licensed per site or per user; `config gpl` displays the
licence text.

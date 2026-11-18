Title: Configuration: The API, Printing and the Rest
Subtitle: The parameters for the API, file transfer, printing, sorting, diagnostics, the screen, the shell, NETDIRS and NETFILES.

This page continues [Configuration: Changing a Parameter from
SD](07a-sd-admin-configuration-changing-from-sd.html).

## The API

| Parameter | Default | Effect |
|---|---|---|
| `SDCLIENT` | 0 | Restricts what an API session may do. Non-zero disables file access outright (no file can be opened, so no dictionary can be evaluated either) and refuses `SDIConv`, `SDOConv`, `SDIConvs` and `SDOConvs` a conversion code that reads a file (`T` with a file) or calls a program (`U`); any non-zero value also refuses `SDOpenSeq`, `SDExecute`, `SDTrans` and `SDRTrans`; `2` additionally refuses any subroutine not compiled as callable from a client (a subroutine whose name begins with `$` must be so compiled at every setting, `0` included) |
| `BACKUPDIR` | unset | The directory `backup.account` and `restore.account` use. Set by `set.backup.directory`, not by hand - see [Backing Up and Restoring Accounts](01b-backup-and-restore.html) |
| `NETDIRS` | unset | Directories outside any account that an account without `os-on` may still open by path (every session, the API's included), separated by semicolons; see *`NETDIRS`: directories outside an account*, below |

**There is no `APIPORT`.** Whether SD listens for the API at all is
`systemd`'s `sdclient.socket` unit, activated independently of any running `sd`
process (see *Remote access and the machine*, in this set), and who may reach it
is the firewall (`ufw`, or firewalld), moved by the `remote.api` verb rather than
by editing this file. **An API session's file access is its own account's,
widened only by `NETDIRS`** (below, *`NETDIRS`: directories outside an account*),
which is empty as delivered. (The `os-on` switch is read for an API session like
any other, but it does not lift that confinement — see *Accounts and Security*.)

`SDCLIENT` is not reported by the `config` verb and has no entry in the shipped
`sd.conf`. It defaults to 0, which permits everything.

## File transfer over ssh

File transfer lets a person move plain-text files (CSV, JSON, BASIC source, any
text) into and out of their own account with an sftp client over the same ssh
login they use for SD. It is delivered off twice: `XFER` below is the system's
switch, and each account also needs `modify.account <account> xfer-on`. Both
must be on before anything can be transferred. **Turning them on lets that
person put files into, and take copies out of, their account from another
machine**, with the `receive` and `send` commands and an sftp client; what
that opens and how it is confined is in *Accounts and Security: File
transfer*. The parameters are read by each process as it starts, so a change
is seen by the next session and the next connection without restarting SD.

| Parameter | Default | Effect |
|---|---|---|
| `XFER` | 0 | `1` lets accounts that have `xfer-on` transfer files; `0` refuses every transfer |
| `XFERFILE` | 10240 | The largest file one transfer slot takes, in kilobytes (1 to 1048576) |
| `XFERSLOT` | 102400 | The most one slot takes in all its files, in kilobytes (1 to 4194304) |
| `XFERWAIT` | 600 | Seconds a slot waits for the sftp client's first connection (10 to 3600) |
| `XFERIDLE` | 120 | Seconds a slot stays open with nothing happening after a client has connected (10 to 3600). A file being sent keeps it open; one left half sent and silent this long is dropped |
| `XFERMAX` | 3600 | Seconds a slot may stay open at most; `0` removes the ceiling (0 to 86400). At the ceiling the transfer ends and a file that is not complete is dropped |
| `XFERKIND` | blank | The extensions a received file must have, separated by commas; blank takes any plain-text file (no NUL byte and no SD mark byte) |

None of them can be changed from `tool.config` or `set.config`; edit
`/etc/sd.conf` by hand. `config('XFER')` and the others read them.

## Printing

| Parameter | Default | Effect |
|---|---|---|
| `LPTRWIDE` | 80 | Default page width for the printer. Range 10 to 1000 |
| `LPTRHIGH` | 66 | Default page depth for the printer. Range 10 to 32767 |
| `SPOOLER` | empty | The spooler to hand print jobs to |

## Sorting

| Parameter | Default | Effect |
|---|---|---|
| `SORTMEM` | 4096 kb | Above this much data a sort works on disk instead of in memory |
| `SORTMRG` | 4 | Files merged at once in a disk sort. Range 2 to 10 |

## Numbers and dates

| Parameter | Default | Effect |
|---|---|---|
| `INTPREC` | 11 | Digits of precision in integer arithmetic. Range 0 to 14 |
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
| `SCREENTHEME` | unset (`mono`); `paper` in the shipped `sd.conf` | The color theme that a program using the `SCREEN` statement gets when it does not choose one: `paper`, `night`, `mono`, `classic` or `blue`. `paper` is black and dark blue text on light gray, with the menu bar and menus the other way round (light gray on black); `night` is white and yellow text on black, its menus black on light gray; `mono` uses only reverse video, underline and bold and reads on any terminal. The shipped `sd.conf` says `SCREENTHEME=paper`, so the toolkit pages and any program that opens a screen show paper on a color terminal on a fresh install; the IDE, SED and the debugger follow it too (the IDE falls back to paper for a name that is not a theme). On an upgrade that keeps the configuration, the installer adds `SCREENTHEME=paper` to a restored `/etc/sd.conf` that has no `SCREENTHEME` line, and changes a restored `SCREENTHEME=blue` (the delivered theme before 2.0-0) to `paper` once, leaving a comment line in the file that says so; set `SCREENTHEME=blue` again afterwards to keep the old look, and later installs leave it. Any other line, `mono` included, is left alone. A terminal with no color (vt100, a phantom, a pipe) is `mono` whatever the line says, and so is a name that is not a theme, without an error. A program that asks for a theme gets that one. A program reads the value with `config('SCREENTHEME')`. **A person's own choice wins for that person**: Ctrl-T or View > Theme on any full-screen program keeps the theme chosen as the record `theme.`*login name* of the file `&menus&` in the account they are in, and every full-screen program starts in it from then on; `SCREENTHEME` is what a person who has never chosen sees. To give someone the site's theme again, delete that record |

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

**A value longer than 80 characters for `SH`, `SH1` or `STARTUP` stops SD** with "SH value is
longer than 80 characters." (or `SH1`, `STARTUP`); a terminal type given to `sd -term`
that is longer than 32 characters is refused the same way. A value that fits is unchanged.
If the shell named cannot be run, the command ends with status 127.

**Both run at the account's own Linux permissions, and only for an account
that has the `sh-on` switch** (see *Accounts and Security*, "The
operating-system switches: `sh-on` and `os-on`"); the setting says which
shell it is, the switch says who may use it. Operating system access has its
own page in this set.

## `NETDIRS`: directories outside an account

An account that has not been given `os-on` is held to its own directory: it
opens no file by pathname anywhere else. `NETDIRS` names directories that such
an account may reach all the same, for a site whose data lives in a shared
directory outside every account:

```
NETDIRS=/srv/sales;/srv/shared
```

The entries are absolute paths separated by semicolons. **Nothing is listed as
delivered**: `sd.conf` has no `NETDIRS` line, and every account is held to its
own directory as before.

**What filling it opens.** Every account without `os-on`, on every route (a
terminal session, a phantom, the API), can then read, change, create and delete
files in the listed directories and below them, by pathname: `openseq`,
`openpath`, `dir()`, `select.dir`, `ospath`, `deleteseq`, a print file, an `f`
pointer in its VOC. The Linux permissions of the account's own user still
apply. It is a smaller thing to open than `os-on`, which opens the whole
machine to one account, but it is opened for every account at once: list only
directories that hold nothing one account must keep from another.

**What it does not open.** `sh` and `os.execute`, the edit gates (`voc-on`,
`bp-on`, `dict-on`), the shared account's rules and what the `ai` line may send
are separate and unchanged. The administrator and an account with `os-on` are
not affected: they reach every path already. `NETDIRS` is asked last: after the
account's own directory and the `sd-on` gate. The shipped SDSYS entries that
every VOC names are open to an account without `os-on` whatever this line says
(read only), and are not part of the list.

**Entries SD ignores.** An entry is left out, and named in the error log and
the system log when SD starts, when it is not an absolute path, is not an
existing directory, is `/`, or holds or lies inside the SD system directory,
the directory of `sd.conf`, the user or group accounts directory, or the
directory of any registered account. An account created later inside a listed
directory closes that entry at once. At most 16 entries are taken.

**How a path is judged.** The name a program gives is resolved first, links
and `..` included, and then compared: a link inside a listed directory that
leads somewhere unlisted is refused, upper and lower case differ, and
`/data/xkey` is not inside `/data/x`. An entry that is itself a link counts as
the directory it leads to.

A session reads the line when it starts, so a change reaches the sessions
started after it; no restart is needed. **A value longer than 191 characters is
refused, by name**: SD does not start, and a new session does not begin, with
`NETDIRS value is longer than 191 characters.` It is never cut, because a cut
path is a shorter directory and would admit more than you wrote. It is not shown
by `config`, and `config('NETDIRS')` does not read it: read the file.

One API route is not widened: request 29, the old remote open of an account's
file that `NETFILES` gates (below). A pointer followed there must still lead
inside the account, whatever `NETDIRS` lists.

## `NETFILES` and SDNet

**`NETFILES` is not what SDNet uses.**
SDNet is the way a program opens a file that lives on another SD server: a VOC
entry of type `N`, a server you define with `set.server`, and a per-account
`net-on` switch, all off until SDSYS turns them on. It is built and is
described on the SDNet page of this set. None of it reads `NETFILES`,
and the older SDNet (a `server;file` VOC
entry, with each server's password in `sd.conf`) does not exist: that form of
name is refused. `NETFILES` is parsed, stored, shown by `config` and readable
with `config('NETFILES')`. **One
thing reads it:** the API server's request 29, "open an SDNet
file", answers "Remote server disallowed access" (7009) unless bit 2 of
`NETFILES` is set, and the files-only API route refuses request 29 whatever the
value is. **`NETDIRS` does not widen this request**: a pointer followed there must still lead inside the account, whatever `NETDIRS` lists. **Setting the bit is not enough.** The request also refuses unless
`SDCLIENT` is 0, the account has a register record (a path names none), the
caller may enter the account by the same rule as `logto` (a member of its
group, the account not suspended, the reason never told to the caller), and
the account's `net-on` switch is on (SDSYS's own account excepted). It also asks the
operating-system question of the file the VOC names: a file pointer that leads out of
the account's directory is followed only if the account holds `os-on` (see *Accounts and
Security*, the VOC pointers section). Each
refusal is on the audit trail as `api refused request=29 reason=...`. The value
is 0 unless `sd.conf` sets it, and the installer does not, so the request is
refused as delivered. Leave it at 0: no client function in this set sends
request 29.

There is no `FILERULE` parameter. **The
`account:file` form of a file name is always available** (for programs moved
from openQM): a name that is in no VOC record and has one colon,
such as `open 'sales:orders'`, opens that account's file exactly as a Q-pointer to it
would, with the same checks: the account must be registered, the person must be able
to `logto` it, and it must not be suspended. It reaches nothing a Q-pointer could not.
The `path:` form is gone, and so is the old `system:account:file` form. To reach a
directory outside the accounts, put an F-pointer in the VOC, where the
operating-system access switches apply to it. A Q-pointer whose fourth field
names another system is refused with status 3003 and is not opened as a local file.

There is no license parameter and no license verb. SD Core for Windows is
GPL v3 and is not licensed per site or per user; `config gpl` displays the
license text.

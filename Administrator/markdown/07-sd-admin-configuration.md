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
GRPSIZE=4
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

That is why a name SD has dropped has to be taken out of the file. On 27 October
2026 eleven parameters were removed (`APILOGIN`, `CODEPAGE`, `CREATUSR`,
`EXCLREM`, `FIXUSERS`, `GDI`, `JNLDIR`, `JNLMODE`, `PORTMAP`, `RINGWAIT` and
`TXCHAR`), and `INVCASE` before them; `FILERULE` followed on 28 October 2026. The installer removes those lines from a
`sd.conf` it restores when you keep the configuration across a re-install, and
says which it removed. A file copied in by hand must have them taken out before SD will
start.

Range failures behave the same way. `GRPSIZE`, `INTPREC`, `LPTRHIGH`,
`LPTRWIDE`, `MAXCALL`, `RECCACHE`, `SORTMRG` and `MAXIDLEN` are bounds-checked
once the file has been read, and a value outside its range stops start-up with
a message naming the parameter.

## Reading the settings

The `config` verb reports what is in force:

```
:config
Virtual Machine Version Number W1.0-0
CLEANUP   300 seconds
CMDSTACK  99
DEADLOCK  0
DUMPDIR   /usr/local/sdsys/dumps
ERRLOG    50 kb
...
YEARBASE  1930
```

SD accepts **50** parameters on this port (`APIPORT` and `NETDIRS` do not
exist here — see *The API*, below). The verb prints all of them except
`BACKUPDIR` and `SDSYS`, and `DEBUG` and `FDS` only when they are set.

The `config()` function reads one parameter from a program:

```
group.size = config('GRPSIZE')
```

**47 parameters are readable this way.** The three that are not are `BACKUPDIR`,
`SCREENTHEME` and `SDSYS`. The name is truncated to eight
characters before it is matched; no parameter name is longer than eight, so
that only shows up if you pass something which is not a parameter.

Two further forms exist. `config lptr` reports the settings of the default
printer, and `config gpl` and `config contrib` display the licence and the list
of contributors.

## Changing a parameter

Editing `sd.conf` and restarting SD is the durable route, and for most
parameters it is the only one. Fourteen tuning parameters can also be changed from SD itself, with
`set.config` or the `E` key of `tool.config` (see *Changing a parameter from SD*, below).

**23 parameters can also be changed for the current session:**

```
config sortmem 8192
```

That writes to the session's own copy of the settings, which the session read
from `sd.conf` when it started. It does not reach `sd.conf`, it does not affect any
other session, and it is gone when the session ends.

The 23 are `DUMPDIR`, `FLTDIFF`, `FSYNC`, `GRPSIZE`, `INTPREC`,
`LPTRHIGH`, `LPTRWIDE`, `MAXCALL`, `MUSTLOCK`, `OBJECTS`, `OBJMEM`, `RECCACHE`,
`SAFEDIR`, `SDCLIENT`, `SH`, `SH1`, `SORTMEM`, `SORTMRG`, `SORTWORK`,
`SPOOLER`, `TEMPDIR`, `TERMINFO` and `YEARBASE`. (The list predates `MAXRLOCK`, `PWDELAY` and, since 19 October 2026,
`NETWAIT` and `NETREPLY`, which can be changed for the session in the same way.)

Everything else takes effect only when SD is next started. That includes every
limit which sizes the shared memory segment and every setting the API listener
reads.

**Since 1.2-0 a session reads `sd.conf` itself when it starts.** It used to copy
the settings the starter had left in the shared memory, which an SD user with a
shell could change. So an edit to a setting a session keeps for itself (the 23
above, and others such as `USRDIR`, `GRPDIR` and `TIMEZONE`)
reaches the sessions started after it, without a restart. **A bad line in
`sd.conf` stops a new session from starting**, with the message `sd -start`
gives, until it is repaired; SD and the sessions already running are not
affected. Every SD user's session now opens the file, so it must stay readable by
them (as installed: mode 0644, owned by root). Edit the file with the same care as before.

## The parameters on one screen: `tool.config`

```
tool.config
```

A full-screen page in SDSYS's VOC only (a window of 140 columns by 43 lines or more). **It looks, and
it can change 14 of the parameters**; it writes no file itself. A change is made by the verb
`set.config` (see *Changing a parameter from SD*, below) through the root helper, and only after you
have typed a value, the page has checked it against the range SD enforces and a box has shown the
exact command and been answered Run. The other 36 parameters are not changed from SD; editing the
file as root and restarting SD stays the way to change them.

The page has three views. **P, the parameters**: one row for every parameter SD knows, from the table
`config.table` in the system directory (`test-toolconfig-units.py` holds that table to the parser in
`config.c`: a parameter the parser takes and the table lacks, or the reverse, fails it). The columns are
the value this SD is running with (what `config()` reports), the value `sd.conf` says now (the file is
read again, a parameter written twice counted the way SD counts it, the flag parameters added up),
the default (what SD uses when the file does not say), when a change takes effect and whether anything
acts on it:

| Takes effect | Meaning |
|---|---|
| `session` | a session reads `sd.conf` itself when it starts, so an edit reaches the sessions started after it, and not the ones already running |
| `restart` | the parameter sizes or starts the system (everything in the shared memory segment, the start-up command, the API's settings); it takes effect when SD is next started |
| `now` | a program reads `sd.conf` each time it uses the parameter (`BACKUPDIR`), so a change needs no restart and no new session |

| Status | Meaning |
|---|---|
| `live` | something acts on it |
| `file` | read from `sd.conf` by a program each time it is used, not by the kernel (`BACKUPDIR`) |
| `unknown` | a name in the file that SD does not know |

A row marked `*` is one where the file and the running SD disagree. The box at the foot says for that
parameter whether the sessions started now will read the file's value (`session`) or SD keeps the old
one until it is restarted (`restart`). **A name in the file that SD does not know is listed at the end
as `unknown`, and the top of the page names it: SD does not start with it, and no new session starts
while the file holds it** (the section *A name SD does not recognise stops it starting* above). `D`
shows only the rows where the file and SD disagree, and `S` only the parameters the file sets. The last
column, `Change`, says `e` for a parameter the page can change (press `E`) and `by hand` for every
other.

`SCREENTHEME`, `SDSYS` and `BACKUPDIR` cannot be read with the `config()` function
(a name longer than eight characters, or one the function does not have); the page says
`(not readable)` for what SD is running with and shows the file's value. `DEBUG` is not compared: the
function reports it in another form than the file writes it.

**B, the backup directory**: the directory saved with `set.backup.directory` and whether it is there;
**R, the report**: the operating system part of `settings.report` (the ssh and API doors, the groups of
`sdusers`, `sdssh` and `sdapi`, the services and the sudoers file), made when the view is opened and on
F5. It holds no key and no password hash. `F5` reads the file, the backup directory and the report
again; `E` changes the parameter under the cursor, or says why it cannot be changed here; `F1`
explains the page; `Ctrl-Q` leaves. Opening the page writes the audit line
`tool start app=tool.config`; a change writes the line of `set.config` (below), and nothing else the
page does is written.

### Changing a parameter from SD: `set.config` and the `E` key

```
set.config cleanup 600
```

The administrator's verb (SDSYS's VOC only). It changes **one** line of `/etc/sd.conf`: the first word
is a parameter name (letters and digits; SD makes it capitals, as the file spells it) and the second a
whole number of up to seven digits. It asks the root helper (`sd-elevate conf-set`, run through sudo)
to make the change; the helper checks everything again and is the authority. `set.config` prints
`CLEANUP is now 600 in sd.conf` and, for a parameter that sizes the system, that it takes effect when
SD is next stopped and started (`sd -stop`, then `sd -start`), or, for one a session reads for itself,
that sessions started from now on use it. A refusal prints the helper's own sentence after
`sd.conf was not changed:` and writes nothing.

**What the helper does.** It accepts only the 14 parameters in the first table below, and only a value
inside the range `config.c` itself enforces for that parameter when SD starts (so it cannot accept
what SD would refuse). It adds or replaces the line **inside the `[sd]` section**, the only place SD
reads (a line appended after another section's header would be ignored without a word); a second
line for the same parameter in an `[sd]` section is dropped, because SD keeps the last one; every
other line is kept exactly as it was. The new file is written beside the old one, given the old
file's owner and mode, and renamed over it, so a session that reads the file at that moment sees
either the old text or the new, never half of it. **The file as it was is kept as `/etc/sd.conf.bak`**
(one generation; a second change replaces it with the file as it was before that change). A change
that says what the file already says writes nothing and leaves the `.bak` alone. The helper writes
`/etc/sd.conf` and nothing a caller passes moves it; when the session reads another file (the
`SD_CONFIG` variable) the page says so in its box. Only the user `sdsys` can ask: sudo's rule for `sdsys` lets it run the
helper with any arguments, the rule for ordinary users names four exact argument lists and `conf-set`
is not one of them, and the helper also refuses a caller sudo says is someone else. SD has no key
that puts `sd.conf.bak` back; as root, `cp /etc/sd.conf.bak /etc/sd.conf` does.

**One audit line** for each time the helper is asked: `set.config key=cleanup value=600 status=ok`, or
`status=refused`. Every changeable parameter is a number, so the value is written.

**On the page.** `E` on a row whose `Change` column says `e` asks for the new value (the question
shows what SD runs with and what the file says), checks that it is a whole number inside the range
before anything else happens, and then shows the exact command in the toolkit's box with a plain
sentence about when it takes effect. Cancel, which is what Enter chooses, runs nothing. Run runs
`set.config` and the page reads the file and SD's own values again and says what changed: the file's
old and new value, and what SD is running with. `E` on any other row writes nothing: it shows why the
parameter is not changed from SD, and the exact line to add by hand, as root, in the `[sd]` section
of the file SD reads.

**The 14 parameters** are the tuning ones: capacity, performance, timeouts and the printer's defaults.
Each is range-checked by `config.c` and each only sizes or times something SD does (how many locks a
process may hold, how deep a program may call, how long a sign-on waits for a user number, the cache
sizes, the printer's defaults); none is a door, a path, a command, a log or a security setting:

| Parameter | Range | Takes effect |
|---|---|---|
| `CLEANUP` | 30 to 3600 | restart |
| `DHCACHE` | 0 to 1024 | session |
| `GRPSIZE` | 1 to 8 | session |
| `LGNWAIT` | 0 to 32767 | restart |
| `LPTRHIGH` | 10 to 32767 | session |
| `LPTRWIDE` | 10 to 1000 | session |
| `MAXCALL` | 10 to 1000000 | session |
| `MAXRLOCK` | 0 to 100000 | session |
| `NETREPLY` | 1 to 3600 | session |
| `NETWAIT` | 1 to 3600 | session |
| `NUMLOCKS` | 1 to 32767 | restart |
| `RECCACHE` | 0 to 32 | session |
| `SORTMRG` | 2 to 10 | session |
| `USPLIT` | 0 to 1 | restart |

**The other 36 are not changed from SD**, and the helper refuses them by name (a name it does not
know at all it refuses with a different sentence, because an unknown name in `sd.conf` stops SD from
starting). They are the doors and what they allow (`NETFILES`, `SDCLIENT`), every
path and command, the log, dump and diagnostic settings, the security throttle `PWDELAY`, the sizes
and combinations that `config.c` does not check or checks against each other, and the ones that change
what existing programs compute. Change them by hand, as before. The page
shows the same sentence in its box:

| Parameter | Why it is not changed from SD |
|---|---|
| `BACKUPDIR` | A directory: set.backup.directory saves it, with its own checks of the path. |
| `CMDSTACK` | Sizes a table in shared memory and config.c checks no range: a mistake shows only at the next start. |
| `DEADLOCK` | A diagnostic: 2 makes SD write a file of the locks involved; set it by hand while you hunt one. |
| `DEBUG` | Debugging flags of the kernel: they change what SD writes and exposes. |
| `DUMPDIR` | A directory: process dumps are written there and can hold what a session had in memory. |
| `ERRLOG` | Sizes the error log; config.c checks no range, and a small size discards its oldest entries sooner. |
| `FDS` | Limits the file descriptors SD uses; config.c checks no range: a mistake shows at the next start. |
| `FLTDIFF` | Changes how every program compares floating point numbers. |
| `FSYNC` | Trades the safety of data against speed; flag bits that config.c does not check. |
| `GRPDIR` | A directory: group accounts are made there. |
| `INTPREC` | Changes the results of arithmetic in programs that already exist. |
| `MAXIDLEN` | Structural: the longest record id of the whole system, which reaches every file and program. |
| `MUSTLOCK` | Makes a write fail unless the record is locked first, which can stop programs that exist. |
| `NETFILES` | A door: bit 2 gates API request 29, a remote open of an account. |
| `NUMFILES` | Sizes the open file table in shared memory; config.c checks no range. |
| `NUMUSERS` | Sizes the user table, which bounds who can sign on; config.c checks no range. |
| `OBJECTS` | Limits the programs a session keeps in memory; config.c checks no range. |
| `OBJMEM` | Limits the memory those programs may take; config.c checks no range. |
| `PDUMP` | Flag bits that say when a process dump is written; a dump can hold what a session had in memory. |
| `PHANTOMS` | Must agree with USERPOOL: a wrong combination stops SD from starting. |
| `PWDELAY` | A security throttle: the pause after a failed network sign-on; 0 removes it. |
| `SAFEDIR` | Changes how SD replaces the files of a directory file, by writing a new one and renaming it. |
| `SCREENTHEME` | Text that SD acts on; config.c checks no value. |
| `SDCLIENT` | A door: restricts what an API session may do, and a lower value loosens it. |
| `SDSYS` | The system directory: SD cannot start, or finds another system, if it is wrong. |
| `SH` | A command SD runs as an interactive shell. |
| `SH1` | A command SD runs for a shell command line. |
| `SORTMEM` | A size in kilobytes that config.c does not check, so a mistake shows only when a sort runs. |
| `SORTWORK` | A directory: the work files of a large sort are written there. |
| `SPOOLER` | Text that names the spooler print jobs are handed to. |
| `STARTUP` | A command SD runs when it starts. |
| `TEMPDIR` | A directory: temporary files are written there. |
| `TERMINFO` | A directory: terminal definitions are read from there. |
| `USERPOOL` | The highest user number: PHANTOMS is checked against it; a mistake stops SD. |
| `USRDIR` | A directory: user accounts are made there. |
| `YEARBASE` | Changes how every program reads a two-digit year; config.c checks no range. |

**What this does not do.** It does not restart SD: a `restart` parameter changes the file and the
running SD keeps its old value until it is stopped and started. It does not reach a file other than
`/etc/sd.conf`. It cannot change a parameter that `config.c` does not range-check, however useful that
would be; such a parameter joins the list when SD itself checks it. And SD itself does not write the
file as root: the verb asks the helper, and the helper is the one program that does.

## Sessions and limits

| Parameter | Default | Effect |
|---|---|---|
| `NUMUSERS` | 20 | Maximum concurrent sessions. Sizes the user table in shared memory |
| `NUMFILES` | 80 | Maximum open files across all sessions |
| `NUMLOCKS` | 100 | Maximum record locks across all sessions. Range 1 to 32767 (the lock table's cells are 16 bits; a value outside it stops SD starting, which it did not before the check of 16 Oct 2026, when 40000 wrapped) |
| `MAXCALL` | 10000 | Maximum subroutine call depth. Range 10 to 1000000 |
| `CMDSTACK` | 99 | Depth of the command stack |
| `FDS` | unset | Limit on file descriptors. No limit when unset |
| `USERPOOL` | 1023 | The highest user number handed out; user numbers rotate through 1 to this, 0 always takes the lowest free one |
| `USPLIT` | 0 | `1`: interactive sessions take the lowest free user number and every other process (a phantom, an API session) the highest free one in 1 to `NUMUSERS`, so the two never meet. `PHANTOMS` and `USERPOOL` are ignored while it is on. `config('USPLIT')` reads it |
| `PHANTOMS` | unset | `base,range` — user numbers kept for phantoms started with `phantom user n`. Nobody else is given one: not a session, not an API session, not a phantom started without `user`. It must lie between 1 and the highest user number, or SD will not start. `config('PHANTOMS')` reads it as `base,range`, null when none are kept |
| `CLEANUP` | 300 | Seconds between the checks that look for sessions that ended without logging out (a killed terminal, a lost connection) and clear them from the user table. 30 to 3600. The daemon wakes every ten seconds, so an interval is kept to within ten seconds; a very short one costs a pass over the user table that often. `config('CLEANUP')` reads it |

## Other SD servers (SDNet)

| Parameter | Default | Effect |
|---|---|---|
| `NETWAIT` | 5 | Seconds to wait for a connection to another SD server: `set.server ... connect`, `set.netlogin` and the first use of a defined server. It bounds the TCP connect and then, again, the TLS handshake (the handshake had 15 seconds fixed until 20 October 2026). 1 to 3600; **0 is refused and SD does not start with it** (openQM reads 0 as "wait for ever") |
| `NETREPLY` | 30 | Seconds to wait for each reply from another SD server once connected. 1 to 3600, 0 refused. A server slower than this is treated as lost, whatever it has sent meanwhile (the TLS session tickets, or half a record, no longer use the wait up: 20 October 2026), and a change that got no answer is never sent again. A `CLEARFILE` waits the longer of 300 seconds and this |
| `NETFILES` | 0 | Not read by SDNet. Bit 2 gates one old API request, number 29 (below). Leave it at 0 |

Both waits are per computer. See [SDNet](12-sdnet.html#the-two-waits-netwait-and-netreply) for what they bound and
the check on the length a reply announces.

## Files and locking

| Parameter | Default | Effect |
|---|---|---|
| `GRPSIZE` | 4 | Default group size for a new dynamic file, in 1 KB units. Read by `create.file` and `configure.file` when no group size is given. **4 since 25 Oct 2026** (the shipped `sd.conf` said 2): 200,000 records of 130 bytes had 5 to 11 percent of their groups overflowed at 2 KB and under 2 percent at 4 KB. A system that is already installed keeps the `sd.conf` it has, and so keeps 2 until you change it; a file keeps the size it was made with |
| `MAXIDLEN` | 63 | Maximum record id length. 63 is also the lower bound |
| `MUSTLOCK` | 0 | When 1, a `write` or `delete` requires the record to be locked first |
| `DEADLOCK` | 0 | When 1, SD traps deadlocks |
| `SAFEDIR` | 0 | When 1, directory files are updated by write-and-rename rather than in place |
| `RECCACHE` | 0 | Records cached per file. Range 0 to 32 |
| `FSYNC` | 0 | Bit flags controlling when SD forces data to disk |

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

## `NETFILES` and SDNet

**`NETFILES` is not what SDNet uses.**
SDNet is the way a program opens a file that lives on another SD server: a VOC
entry of type `N`, a server you define with `set.server`, and a per-account
`net-on` switch, all off until SDSYS turns them on. It is built and is
described on the SDNet page of this set, with what has and has not been tested
(it has been run on one real installation talking to itself; no two real machines
have been connected yet). None of it reads `NETFILES`,
and the older SDNet that was removed on 9 September 2026 (a `server;file` VOC
entry, with each server's password in `sd.conf`) is still gone: that form of
name is refused. `NETFILES` is parsed, stored, shown by `config` and readable
with `config('NETFILES')`, and setting it to 2 made `config` show 2. **One
thing in the source reads it:** the API server's request 29, "open an SDNet
file", answers "Remote server disallowed access" (7009) unless bit 2 of
`NETFILES` is set, and the files-only API route refuses request 29 whatever the
value is. **Setting the bit is no longer enough** (changed 18 October 2026).
Until then the bit was the whole gate: with it set, any API login could open
the VOC-named file of *any* account through request 29, including an account it
could not `logto`, a suspended one, one named by a path and one whose `net-on`
switch was off, and `SDCLIENT` did not stop it; that was run on a private SD and
the planted record came back from the disk. The request now also refuses unless
`SDCLIENT` is 0, the account has a register record (a path names none), the
caller may enter the account by the same rule as `logto` (a member of its
group, the account not suspended, the reason never told to the caller), and
the account's `net-on` switch is on (SDSYS's own account excepted). Since 20
October 2026 it also asks the operating-system question of the file the VOC names:
a file pointer that leads out of the account's directory is followed only if the
account holds `os-on` (see *Accounts and Security*, the VOC pointers section), where
before it was opened for any caller the other rules admitted (found by reading the
source and then run on a private SD, which read a planted record from a directory
outside every account). Each
refusal is on the audit trail as `api refused request=29 reason=...`. The value
is 0 unless `sd.conf` sets it, and the installer does not, so the request is
refused as delivered. Leave it at 0: no client function in this set sends
request 29.

There is no `FILERULE` parameter any more (removed 28 October 2026). A name that
is in no VOC record is not found: the `account:file` and `path:` forms of a file
name are gone, and so is the old `system:account:file` form. To reach a file in
another account or directory, put a Q-pointer or an F-pointer in the VOC, where
the operating-system access switches apply to it. A Q-pointer whose fourth field
names another system is refused with status 3003 and is not opened as a local file.

There is no licence parameter and no licence verb. SD Core for Windows is
GPL v3 and is not licensed per site or per user; `config gpl` displays the
licence text.

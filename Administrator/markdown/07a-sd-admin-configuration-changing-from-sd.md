Title: Configuration: Changing a Parameter from SD
Subtitle: set.config and the E key, and the parameters for sessions, files and directories.

This page continues [Configuration](07-sd-admin-configuration.html).

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
inside the range SD itself enforces for that parameter when SD starts (so it cannot accept
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
Each is range-checked by SD and each only sizes or times something SD does (how many locks a
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

**The other 37 are not changed from SD**, and the helper refuses them by name (a name it does not
know at all it refuses with a different sentence, because an unknown name in `sd.conf` stops SD from
starting). They are the doors and what they allow (`NETDIRS`, `NETFILES`, `SDCLIENT`), every
path and command, the log, dump and diagnostic settings, the security throttle `PWDELAY`, the sizes
and combinations that SD does not check or checks against each other, and the ones that change
what existing programs compute. Change them by hand, as before. The page
shows the same sentence in its box:

| Parameter | Why it is not changed from SD |
|---|---|
| `BACKUPDIR` | A directory: set.backup.directory saves it, with its own checks of the path. |
| `CMDSTACK` | Sizes a table in shared memory and SD checks no range: a mistake shows only at the next start. |
| `DEADLOCK` | A diagnostic: 2 makes SD write a file of the locks involved; set it by hand while you hunt one. |
| `DEBUG` | Debugging flags of the kernel: they change what SD writes and exposes. |
| `DUMPDIR` | A directory: process dumps are written there and can hold what a session had in memory. |
| `ERRLOG` | Sizes the error log; SD checks no range, and a small size discards its oldest entries sooner. |
| `FDS` | Limits the file descriptors SD uses; SD checks no range: a mistake shows at the next start. |
| `FLTDIFF` | Changes how every program compares floating point numbers. |
| `FSYNC` | Trades the safety of data against speed; flag bits that SD does not check. |
| `GRPDIR` | A directory: group accounts are made there. |
| `INTPREC` | Changes the results of arithmetic in programs that already exist. |
| `MAXIDLEN` | Structural: the longest record id of the whole system, which reaches every file and program. |
| `MUSTLOCK` | Makes a write fail unless the record is locked first, which can stop programs that exist. |
| `NETDIRS` | A door: it widens what an account without os-on may reach beyond its own directory. |
| `NETFILES` | A door: bit 2 gates API request 29, a remote open of an account. |
| `NUMFILES` | Sizes the open file table in shared memory; SD checks no range. |
| `NUMUSERS` | Sizes the user table, which bounds who can sign on; SD checks no range. |
| `OBJECTS` | Limits the programs a session keeps in memory; SD checks no range. |
| `OBJMEM` | Limits the memory those programs may take; SD checks no range. |
| `PDUMP` | Flag bits that say when a process dump is written; a dump can hold what a session had in memory. |
| `PHANTOMS` | Must agree with USERPOOL: a wrong combination stops SD from starting. |
| `PWDELAY` | A security throttle: the pause after a failed network sign-on; 0 removes it. |
| `SAFEDIR` | Changes how SD replaces the files of a directory file, by writing a new one and renaming it. |
| `SCREENTHEME` | Text that SD acts on; SD checks no value. |
| `SDCLIENT` | A door: restricts what an API session may do, and a lower value loosens it. |
| `SDSYS` | The system directory: SD cannot start, or finds another system, if it is wrong. |
| `SH` | A command SD runs as an interactive shell. |
| `SH1` | A command SD runs for a shell command line. |
| `SORTMEM` | A size in kilobytes that SD does not check, so a mistake shows only when a sort runs. |
| `SORTWORK` | A directory: the work files of a large sort are written there. |
| `SPOOLER` | Text that names the spooler print jobs are handed to. |
| `STARTUP` | A command SD runs when it starts. |
| `TEMPDIR` | A directory: temporary files are written there. |
| `TERMINFO` | A directory: terminal definitions are read from there. |
| `USERPOOL` | The highest user number: PHANTOMS is checked against it; a mistake stops SD. |
| `USRDIR` | A directory: user accounts are made there. |
| `XFER` | A door: 1 opens file transfer over ssh for every account that has xfer-on. |
| `XFERFILE` | A transfer limit: raising it lets one file fill more of the disk. |
| `XFERIDLE` | A transfer limit: raising it keeps an unused slot open longer. |
| `XFERKIND` | A transfer filter: blank takes any plain-text file. |
| `XFERMAX` | A transfer limit: 0 lets a slot stay open for as long as its session does. |
| `XFERSLOT` | A transfer limit: raising it lets one slot fill more of the disk. |
| `XFERWAIT` | A transfer limit: raising it keeps a slot open longer before anyone connects. |
| `YEARBASE` | Changes how every program reads a two-digit year; SD checks no range. |

**What this does not do.** It does not restart SD: a `restart` parameter changes the file and the
running SD keeps its old value until it is stopped and started. It does not reach a file other than
`/etc/sd.conf`. It cannot change a parameter that SD does not range-check, however useful that
would be; such a parameter joins the list when SD itself checks it. And SD itself does not write the
file as root: the verb asks the helper, and the helper is the one program that does.

## Sessions and limits

| Parameter | Default | Effect |
|---|---|---|
| `NUMUSERS` | 20 | Maximum concurrent sessions. Sizes the user table in shared memory |
| `NUMFILES` | 80 | Maximum open files across all sessions |
| `NUMLOCKS` | 100 | Maximum record locks across all sessions. Range 1 to 32767 (the lock table's cells are 16 bits; a value outside it stops SD starting) |
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
| `NETWAIT` | 5 | Seconds to wait for a connection to another SD server: `set.server ... connect`, `set.netlogin` and the first use of a defined server. It bounds the TCP connect and then, again, the TLS handshake. 1 to 3600; **0 is refused and SD does not start with it** (openQM reads 0 as "wait for ever") |
| `NETREPLY` | 30 | Seconds to wait for each reply from another SD server once connected. 1 to 3600, 0 refused. A server slower than this is treated as lost, whatever it has sent meanwhile (the TLS session tickets, or half a record, do not use the wait up), and a change that got no answer is never sent again. A `CLEARFILE` waits the longer of 300 seconds and this |
| `NETFILES` | 0 | Not read by SDNet. Bit 2 gates one old API request, number 29 (below). Leave it at 0 |

Both waits are per computer. See [SDNet](12f-sdnet-waits-and-audit.html#the-two-waits-netwait-and-netreply) for what they bound and
the check on the length a reply announces.

## Files and locking

| Parameter | Default | Effect |
|---|---|---|
| `GRPSIZE` | 4 | Default group size for a new dynamic file, in 1 KB units. Read by `create.file` and `configure.file` when no group size is given. **4** is the shipped value: 200,000 records of 130 bytes had 5 to 11 percent of their groups overflowed at 2 KB and under 2 percent at 4 KB. A system whose `sd.conf` says 2 keeps 2 until you change it; a file keeps the size it was made with |
| `MAXIDLEN` | 63 | Maximum record id length. 63 is also the lower bound |
| `MUSTLOCK` | 0 | When 1, a `write` or `delete` requires the record to be locked first |
| `DEADLOCK` | 0 | When 1, SD traps deadlocks |
| `SAFEDIR` | 0 | When 1, directory files are updated by write-and-rename rather than in place |
| `RECCACHE` | 0 | Records cached per file. Range 0 to 32 |
| `FSYNC` | 0 | Bit flags controlling when SD forces data to disk |

## Directories

| Parameter | Default on a new install | Effect |
|---|---|---|
| `SDSYS` | `/usr/local/sdsys` | The system account. SD does not start if the global catalog is not found beneath it |
| `USRDIR` | `/home/sd/user_accounts` | Where `create.account` puts a user account |
| `GRPDIR` | `/home/sd/group_accounts` | Where `create.account` puts a group account |
| `DUMPDIR` | `/usr/local/sdsys/dumps` | Where process dumps are written |
| `TEMPDIR` | unset | Temporary files. Falls back to the system default when unset |
| `SORTWORK` | unset | Work files for a sort that does not fit in memory. When it is not set, or does not exist, SD uses `TEMPDIR` |
| `TERMINFO` | empty | An additional terminfo directory. The shipped definitions are found without it |

`DUMPDIR` is set rather than left empty on purpose. A blank value falls back to
the system directory, which SD users can write to, and a process dump carries
the whole variable state of the session that wrote it. The installer makes the
dump directory write-only to SD users, so a dump can be added and nobody else's
can be listed or read.

## Continued in

[Configuration: The API, Printing and the
Rest](07b-sd-admin-configuration-api-printing-and-netfiles.html) — the
remaining groups of parameters.

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

> The sample output below is illustrative; the values on your system will
> differ where your configuration does.

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
anything. **An upgrade keeps your `sd.conf`**: the installer puts a kept file
back and takes out only the parameters SD no longer has.

### A name SD does not recognize stops it starting

An unrecognized parameter is not ignored. The parser abandons the file with
`Unrecognized configuration parameter`, and SD does not start.

That is why a name SD does not have has to be taken out of the file. These
thirteen names are not parameters of SD: `APILOGIN`, `CODEPAGE`, `CREATUSR`,
`EXCLREM`, `FILERULE`, `FIXUSERS`, `GDI`, `INVCASE`, `JNLDIR`, `JNLMODE`,
`PORTMAP`, `RINGWAIT` and `TXCHAR`. The installer removes those lines from a
`sd.conf` it restores when you keep the configuration across a re-install, and
says which it removed. A file copied in by hand from an older installation must have them
taken out before SD will start.

Range failures behave the same way. `GRPSIZE`, `INTPREC`, `LPTRHIGH`,
`LPTRWIDE`, `MAXCALL`, `RECCACHE`, `SORTMRG` and `MAXIDLEN` are bounds-checked
once the file has been read, and a value outside its range stops start-up with
a message naming the parameter.

## Reading the settings

The `config` verb reports what is in force:

```
:config
Virtual Machine Version Number LC2.0-0
CLEANUP   300 seconds
CMDSTACK  99
DEADLOCK  0
DHCACHE   10
DUMPDIR   /usr/local/sdsys/dumps
ERRLOG    50 kb
...
YEARBASE  1930
```

SD accepts **58** parameters (`APIPORT` does not
exist here — see *The API*, below). The verb prints all of them except
`BACKUPDIR`, `NETDIRS` and `SDSYS`, and `DEBUG`, `FDS` and `PHANTOMS` only when they are set; it also prints `TIMEZONE`, which is not a file parameter.

`NETDIRS` is the one to know about. It decides what a session held to its account
by the `os` switch, the API's included, may reach outside its own account (see
[The API, Printing and the Rest](07b-sd-admin-configuration-api-printing-and-netfiles.html#netdirs-directories-outside-an-account)).
The verb will not tell you what it is set to, and `config('NETDIRS')` does not read it. Read it from the file.

**`config` pages its output** — press Return for more, or `Q`.

The `config()` function reads one parameter from a program:

```
group.size = config('GRPSIZE')
```

**55 of the 58 parameters are readable this way.** The three that are not are `BACKUPDIR`, `NETDIRS` and `SDSYS`; `TIMEZONE`, which is not a file parameter, can be read as well. A name of more than sixteen characters is not found (the function answers an empty string and `status()` is not 0); no parameter name is that long, so that only shows up if you pass something which is not a parameter.

Two further forms exist. `config lptr` reports the settings of the default
printer, and `config gpl` and `config contrib` display the license and the list
of contributors.

## Changing a parameter

Editing `sd.conf` and restarting SD is the durable route, and for most
parameters it is the only one. Fourteen tuning parameters can also be changed from SD itself, with
`set.config` or the `E` key of `tool.config` (see [Configuration: Changing a Parameter from SD](07a-sd-admin-configuration-changing-from-sd.html)).

**29 settings can also be changed for the current session:**

```
config sortmem 8192
```

That writes to the session's own copy of the settings, which the session read
from `sd.conf` when it started. It does not reach `sd.conf`, it does not affect any
other session, and it is gone when the session ends.

The 29 are `DHCACHE`, `DUMPDIR`, `FLTDIFF`, `FSYNC`, `GRPSIZE`, `INTPREC`,
`LPTRHIGH`, `LPTRWIDE`, `MAXCALL`, `MAXRLOCK`, `MUSTLOCK`, `NETREPLY`, `NETWAIT`,
`OBJECTS`, `OBJMEM`, `PWDELAY`, `RECCACHE`, `SAFEDIR`, `SDCLIENT`, `SH`, `SH1`,
`SORTMEM`, `SORTMRG`, `SORTWORK`, `SPOOLER`, `TEMPDIR`, `TERMINFO`, `TIMEZONE` and
`YEARBASE`.

Everything else takes effect only when SD is next started. That includes every
limit which sizes the shared memory segment and every setting the API listener
reads.

**A session reads `sd.conf` itself when it starts**, and not from the shared memory,
which an SD user with a shell could change. So an edit to a setting a session keeps for
itself (the 29 above, and others such as `USRDIR` and `GRPDIR`)
reaches the sessions started after it, without a restart. **A bad line in
`sd.conf` stops a new session from starting**, with the message `sd -start`
gives, until it is repaired; SD and the sessions already running are not
affected. Every SD user's session opens the file, so it must stay readable by
them (as installed: mode 0644, owned by root). Edit the file with care.

## The parameters on one screen: `tool.config`

```
tool.config
```

A full-screen page in SDSYS's VOC only (a window of 140 columns by 43 lines or more). **It looks, and
it can change 14 of the parameters**; it writes no file itself. A change is made by the verb
`set.config` (see [Configuration: Changing a Parameter from SD](07a-sd-admin-configuration-changing-from-sd.html)) through the root helper, and only after you
have typed a value, the page has checked it against the range SD enforces and a box has shown the
exact command and been answered Run. The other 44 parameters are not changed from SD; editing the
file as root and restarting SD stays the way to change them.

The page has three views. **P, the parameters**: one row for every parameter SD knows, from the table
`config.table` in the system directory, which names every parameter SD reads. The columns are
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
while the file holds it** (the section *A name SD does not recognize stops it starting* above). `D`
shows only the rows where the file and SD disagree, and `S` only the parameters the file sets. The last
column, `Change`, says `e` for a parameter the page can change (press `E`) and `by hand` for every
other.

`SDSYS`, `BACKUPDIR` and `NETDIRS` cannot be read with the `config()` function (a name longer than sixteen characters, or one the function does not have); the page says
`(not readable)` for what SD is running with and shows the file's value. `DEBUG` is not compared: the
function reports it in another form than the file writes it.

**B, the backup directory**: the directory saved with `set.backup.directory` and whether it is there;
**R, the report**: the operating system part of `settings.report` (the ssh and API doors, the groups of
`sdusers`, `sdssh` and `sdapi`, the services and the sudoers file), made when the view is opened and on
F5. It holds no key and no password hash. `F5` reads the file, the backup directory and the report
again, and while the report is made the status line says "Reading the settings (a few seconds)...", and while `set.config` runs a change it says "Making the change (a few seconds)...";
`E` changes the parameter under the cursor, or says why it cannot be changed here; `F1`
explains the page; `Ctrl-Q` leaves. Opening the page writes the audit line
`tool start app=tool.config`; a change writes the line of `set.config` (below), and nothing else the
page does is written.

## Continued in

[Configuration: Changing a Parameter from
SD](07a-sd-admin-configuration-changing-from-sd.html) — set.config, the E key
and the first groups of parameters.

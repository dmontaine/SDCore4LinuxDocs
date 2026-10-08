Title: Account Maintenance
Subtitle: Emptying scratch files, refreshing a VOC, keeping local versions of records, configuration, the system date, and deleting an account.

This page continues [Accounts and Security](01-accounts-and-security.html).

## Emptying an account's scratch files: `clean.account`

```
clean.account
```

Empties three things in the account you are standing in, and takes no
arguments — **there is no way to clean an account you are not in**:

```
:clean.account
Cleaned $COMO
Cleaned $hold
Cleaned $savedlists
```

| | |
|---|---|
| **`$COMO`** | captured session transcripts, including every phantom's |
| **`$hold`** | reports sent to the hold file instead of a printer |
| **`$savedlists`** | saved select lists |

**Nothing else is touched** — no data file, no program, no dictionary. A como
capture that is currently running is left alone and says so: *$COMO not cleaned
- COMO file active*.

**It needs nothing beyond being SDSYS** — the same as every other verb on
this page. It only ever touches the account you are already standing in.

## Refreshing an account's VOC: `update.accounts`

```
update.accounts {all}
```

```
Copying records from NEWVOC to VOC...
```

Copies the shipped verb and keyword definitions into an account, adding what is
missing and leaving that account's own VOC entries alone. It is what brings an
existing account up to date after SD itself is upgraded — every account gets
the same `newvoc`, so there is no tier for it to respect any more; a
suspended account is updated exactly like any other, since suspension
never touched the VOC to begin with.

With no keyword it updates the account you are standing in and then offers the
rest, asking each time. **`all` is the unattended form**: it updates every
registered account without asking.

You will not normally type `all` yourself. The installer runs it during an
upgrade, so a release that adds a VOC record reaches every existing account
without anybody visiting them. Before that existed, an upgrade replaced the
shipped files and no account gained a new verb.

`all` is an explicit keyword rather than something inferred from how SD was
started. The test for an internal session exists and would have worked, but it
would have decided a rewrite of every account's VOC from a property nobody
typing the verb can see.

A second word that is not `all` is refused by name rather than ignored:

```
:update.accounts everything
update.accounts does not take everything
```

Quietly ignoring it would run the interactive form while the caller believed
they had asked for the other one.

### It never takes anything away

`update.accounts` only ever adds. A record removed from an account stays
removed. To keep an edit of your own, mark the record — see below.

## Keeping your own version of a VOC record: `[locked]`

This has no equivalent in OpenQM or in SD on Linux. Nothing you know from
another MultiValue system will tell you it exists.

A site that has customised one of SD's own VOC records marks it by putting
`[locked]` in **field 1, after the type code**. `update.accounts` then leaves
that record alone.

```
V[locked]
CA
$MYVERSION
```

### After the type code, not at the front

The first character of field 1 **is** the type, so `[locked]V` would be read as
a record of type `[`. Two characters are the type for a `P` record, and those
are the only two-character types SD uses: `PA` for a paragraph and `PH` for a
phrase.

```
PA[locked]
```

Anywhere later in field 1 works — the test searches the field rather than
matching a fixed position. Case does not matter: both sides are upper-cased
before comparison, so `[LOCKED]` and `[Locked]` are the same marker. A lock
that failed open because somebody typed it in capitals would be worse than no
lock at all, because the record it was meant to protect would be replaced
silently.

### A verb is not protected by it

**`[locked]` is honoured on every kind of VOC record except a verb.** A verb
marked `[locked]` is updated anyway, and the account is told which ones:

```
2 verb(s) marked [locked] were updated anyway: MYLIST MYREPORT
```

A verb is what SD runs. A locked one would go on naming the program, or the
internal routine number, that this release replaced — and the internal case
fails in the worst way available, because field 3 of an internal verb record is
a *number*, so a reassignment sends the verb to a different function with no
sign that anything is wrong.

**The way to get a verb that behaves differently is to add your own**, under a
name SD does not ship, modelled on the system one. `update.accounts` walks the
records SD ships, so a verb of your own is never visited and needs no marker.

### You are told what was withheld

```
3 VOC record(s) were left alone because they are marked [locked]: WINDOWS ...
```

The message names each record, and says plainly that any correction this
release made to them has not been applied here.

**That is the cost, and it belongs to the site rather than to SD.** A locked
record keeps the version the account already had, so a defect fixed in that
record stays unfixed in this account. Remove the marker from field 1 and run
`update.accounts` again to take the new version.

## Reading and setting configuration: `config`

```
config                     report every setting
config lptr                the same, to the default printer
config param value         set one
config gpl                 display the licence
config contrib             display the contributors
```

```
:config
Virtual Machine Version Number L1.1-3
APILOGIN  1
CMDSTACK  99
DEADLOCK  0
DUMPDIR   /usr/local/sdsys/dumps
ERRLOG    50 kb
...
NUMFILES  80
NUMLOCKS  100
NUMUSERS  20
...
SH        /bin/bash -i
SORTWORK
TEMPDIR
YEARBASE  1930
```

*(Forty-odd lines; cut here.)* **Reading needs nothing** — any account with the
verb can do it, and it is the quickest answer to *how many users, how many
locks, how many open files is this machine set up for*.

| | |
|---|---|
| *New parameter value required* | `config numlocks` with nothing after it. **The report form is `config` alone**; naming one parameter means *set it* |
| *Not a recognised private configuration parameter name* | the name is not one that can be set per-session |
| *Invalid value for this parameter* | it is, and the value is not |

**`config param value` sets a private, session-local value and not the
machine's.** The machine's settings live in SD's configuration file and are
read when SD starts. This form overrides one for the session you are in, which
is the right tool for trying a value before writing it down and the wrong one
for changing an installation.

**`config gpl` and `config contrib` shell out to `less`**, against two plain
files in the system directory (`sdsys/licence`, `sdsys/contrib`) — not a VOC
record, despite reading like one. `gpl.bp/config` runs `!less
sdsys/licence` and `!less sdsys/contrib` directly. That still works in any
account: `sh`/`!`/`os.execute` run unconditionally for every account after
the tiered-account teardown (S.27, "no second wall"), so there is no
operating-system access this needs and does not already have.

## Setting the session's date: `set.date`

```
set.date date
```

Sets the date **this session** sees — not the machine's clock. The argument
goes through SD's `D` conversion, so anything `iconv(…, 'D')` accepts will do,
and anything it does not is refused:

| | |
|---|---|
| *Date required* | `set.date` with nothing after it |
| *Invalid date format* | the argument is not a date SD can read |

**What it actually changes** (read from the source, `op_misc.c` `set_date()`):
SD keeps an offset from the real date inside the one `sd` process that ran
the command, and adds it wherever that process reports the date — `DATE()`
and `TIMEDATE()` in BASIC, and so the `date` verb. Nothing else sees it:
other sessions, other users, the operating system, file timestamps and
scheduled jobs all keep the real date, and no Linux privilege is involved.
The time of day is unchanged; only the day moves.

**It lasts until the session ends.** To go back sooner, run `set.date` again
with today's date. Its use is testing date-dependent programs — month-end or
year-end processing — without touching the machine's clock.

## Deleting an account: `delete.account`

```
delete.account account.name {remove.home}
```

Removes the account directory, its Linux group, its entry in the accounts
register, and — for a user account SD itself created — the Linux user
itself. **One confirmation covers all of it**, and the wording is decided
before the question is asked, so it never offers to remove a Linux account it
is not going to. **The Linux user's home directory is kept unless you add
`remove.home`** — see *Managing accounts* in the Getting Started set.

**It will not delete a Linux account SD did not create.** The account is
left in place and it says so.

**Three refusals come before the confirmation**, so none of them can be reached
by accident:

| | |
|---|---|
| *Cannot delete SDSYS account* | `delete.account sdsys` |
| *Cannot delete own account* | the account you are standing in |
| *Account not registered in ACCOUNTS file* | the name is not one of SD's |

*(Those three wordings are the verb's own; they are not shown as a transcript
here because reaching them takes an SDSYS session, and an ordinary one is
refused by the privilege gate first — which is itself the fourth refusal, and
the one most people meet.)*

> **The confirmation is unconditional and no keyword suppresses it.** There
> is no `no.query` on this verb. **Never send `delete.account` down a pipe** —
> the prompt will eat the commands that follow it as its answers, and the
> session will then wait for ever.

## Backing up and restoring accounts: `backup.account`, `restore.account`

```
backup.account name {name ...} {to directory}
backup.account all {to directory}
restore.account archive name {name ...} {no.query}
restore.account archive all {no.query}
```

`backup.account` writes **one zip file**, named for the machine, the accounts
and the time. It holds each account's files and a plain-text **manifest** of how
the account was set up: its type, description, suspension, remote access and
group members. `restore.account` puts accounts back — over an account that
exists, or onto a machine that has never had it. A restored account's paths are
corrected to where it now lives, and programs it had in the global catalogue are
catalogued again. **Backups made here restore on SD Core for Windows, and the
other way round**; a backup of the full product restores only to a full system
(SD Core Solo's only to Solo).

**`restore.account latest` restores the most recent backup without your naming
it:**

```
restore.account latest name {name ...} {no.query}
restore.account latest all {no.query}
```

`latest` stands where the archive name goes. SD looks in the directory saved by
`set.backup.directory` and picks **the newest backup made on this computer that
really holds every account you named**. It decides by *looking inside*: a backup
is called `SD-<computer>-<accounts>-<yyyymmdd-hhmmss>.zip`, but one made with
`all`, or of many accounts, carries no account names, so SD opens each backup
the name might fit and reads its list of accounts (nothing is unpacked). It
prints which backup it chose (*The most recent backup is …*) and then restores
from it exactly as if you had typed its name.

**If a newer backup made on this computer does not hold the account** — or
cannot be read — SD says so before it asks you to go ahead: *The most recent
backup made on this computer, …, does not hold … (or cannot be read). The newest
backup that does is …*. You are then not restoring your latest backup, and you
can still answer `n`. If **no** backup holds the account it says *No backup of …
made on this computer was found in …* and changes nothing.

`latest all` takes the newest backup that was made with `all`, by its name, and
does not warn about a newer backup of one account. Whichever backup is picked is
still checked against its own manifest, in full, before anything is changed, and
only the accounts you named are restored from a backup of several. A backup made
on another computer is never picked. An archive name always ends in `.zip`, so
`latest` cannot be mistaken for one.

**`latest` only considers backups SD named itself**, `SD-<computer>-<accounts or
all>-<yyyymmdd-hhmmss>.zip`, and it passes over one whose name lists other
accounts without opening it. A backup you have renamed is never picked: restore
it by giving its name (`restore.account myfile.zip name`). A bare name is looked
for in the saved directory; a name with a directory in it is used as given.

**Both are SDSYS's.** A backup or restore starts only when every other session
has logged out, says who is still logged in if any are, and **no one can log in
— at the terminal, over ssh or through the API — until it has finished.**

**Every backup is checked as it is made.** The files, bytes and directories of
each account are counted before it is packed and compared with what was
written, and a backup that does not match is **deleted rather than kept**. **A
backup never overwrites a file:** if the name is taken, SD says so and writes
nothing. A restore checks the whole archive against its manifest **before it
changes anything**, lists what it will replace and create, and asks first. **An
archive that lies is refused with nothing changed** — counts that disagree with
the manifest, an entry path with `..` in it or an absolute path, no manifest or
two of them.

**A restored account comes back as it was:** each directory has the permissions
it was backed up with, and everything in the account belongs to its Linux user
and its own group (`sdu_<name>`) again. An account that already exists keeps its
Linux user, its password and its groups.

**What it does not do:**

- It does not back up SDSYS or the system's configuration (`settings.report`,
  below, records that for reference only).
- It carries **no passwords**: an account restored onto a machine that never
  had it asks for a new one, and an account that exists keeps its own.
- It does not follow symbolic links inside an account; any it finds are named
  and left out.
- A program recompiled after it was catalogued globally is not recognised as the
  account's and is not catalogued again.

## Saying where backups go: `set.backup.directory`

```
set.backup.directory directory
set.backup.directory
```

Saves the directory that `backup.account` writes to and `restore.account` reads
from, so it need not be typed each time. It **creates the directory if it is not
there**, checks that it can be written to, and keeps it in `sd.conf`
(`BACKUPDIR=`), where it takes effect at once — no restart. On its own it shows
the saved directory and changes nothing.

With a directory saved, `backup.account` no longer needs `to`; with none saved
it asks for one and saves the answer exactly as this verb would.
`restore.account` does the same for an archive named without a directory.
`to directory`, or an archive name that carries a directory, still works and
changes nothing that is saved.

**The directory must be a full path** — a relative one is refused, because a
setting that meant different places depending on where you were standing would
be a trap. **A directory that already exists is used as it is**, wherever it is
(a USB drive, the pCloud folder), and nothing about it is changed.

**A missing one is made readable by SDSYS only**, because a backup holds every
account's files. SDSYS makes it itself wherever SDSYS may create it; elsewhere
SD's privileged helper makes it, **but only below `/media`, `/run/media`,
`/mnt`, `/var/backups`, `/srv`, `/opt` and `/home/sdsys`.** The limit is
deliberate: a directory SDSYS owned inside a place the system reads its
configuration from (`/etc/systemd/system/ssh.service.d`, say) would let SDSYS
run commands as root, and SDSYS never is root. Anywhere else the verb says so
and creates nothing. **To allow another place,** an administrator lists its
directory, one per line, in `/etc/sd-backup-roots` (a file only root may own and
write; SD ignores it otherwise), or creates the directory and gives it to
`sdsys`.

> An earlier release refuses to start if `sd.conf` holds a `BACKUPDIR` line, so
> take the line out before going back to one.

## Recording the settings: `settings.report`

```
settings.report {directory}
```

Writes, or shows, a **plain-text record** of the system's settings — `sd.conf`,
ssh and API access, the accounts — for an administrator to keep. It is for
reference only: nothing reads it back. **It never contains a password or a
private key.** The API's certificate appears as its subject, dates and
fingerprint, or as *certificate: not yet generated* until the API has had its
first TLS connection.

## Who has these verbs

**All of them are SDSYS's** — `create.account`, `modify.account`,
`modify.password` for another account, `delete.account`, `clean.account`,
`update.accounts`, `config`, `backup.account`, `restore.account`,
`set.backup.directory`, `settings.report`. An ordinary account has none of these names at
all — this is not a permission it lacks, the verbs are simply not in its
VOC. **Unlike SD Core for Windows, there is no separate `grant`/`revoke`/
`list.grants` set** — `modify.account add`/`delete` folds the grant into
one place; see [Accounts and Security](01-accounts-and-security.html).

## See also

[Sessions and Locks](02-sessions-and-locks.html) ·
[Operating System Access](03-operating-system-access.html).

**In the user documentation**, which does not repeat any of this: *SD TCL - The
Command Processor* for how a verb is dispatched and what a VOC record holds, and
*SD Basic - System and Environment* for what a program can read about its own
session. Those pages are in a different set and are deliberately not linked from
here — see the note at the top.

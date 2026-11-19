Title: Account Maintenance
Subtitle: Emptying scratch files, refreshing a VOC, keeping local versions of records, configuration, the system date, and deleting an account.

This page continues [Accounts and Security: The Home Screen, ssh Keys and
Passwords](01-accounts-and-security-8-home-screen-ssh-keys-passwords.html).

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

Copies the shipped verb and keyword definitions into an account. A shipped
entry that is missing is added, and one that was changed there is put back as
`newvoc` has it: it asks first only when the type letter differs, and it keeps
an entry marked `[locked]` unless it is a verb. An entry SD does not ship is
never touched. It is what brings an
existing account up to date after SD itself is upgraded — every account gets
the same `newvoc`, so there is no tier for it to respect any more; a
suspended account is updated exactly like any other, since suspension
never touched the VOC to begin with.

With no keyword it updates the account you are standing in and then offers the
rest, asking each time. **`all` is the unattended form**: it updates every
registered account without asking.

**SDSYS can write the VOC of a user account only if the account lists it** (`modify.account`
*name* `sdsys-on`; the delivered state is that it does, and `sdsys-off` takes it away). An `all` run by SDSYS skips such an
account with a line that says so (message 11983), goes on to the next, and ends with the count of
accounts updated and, if there were any, the count left as they were. The installer's own run is
root's and updates every account.

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

### What it takes away: the deletion list

The copy from `newvoc` only ever adds and changes. A record SD has **stopped
shipping** (a second spelling of a keyword, say) would stay in every account
that already had it, so SD ships a second thing next to `newvoc`: a **deletion
list**, one small record for each VOC record a release has withdrawn. After
`update.accounts` has copied the shipped records into an account, it works
down the list and removes a listed record from that account's VOC, **but only
when it is the record SD shipped.** Each removal is checked, saved, reported
and audited:

- **It must be the shipped record.** The list says what the record was: its
  type, and for a keyword its number. An account that has its own record of
  the same name (a paragraph you called `margin`, say) is **kept** and the
  update says so (message 11901).
- **A record marked `[locked]` is kept** (11902), as the copy from `newvoc`
  keeps one. **A verb is the exception**, as it is everywhere in the update: a
  locked verb that SD no longer ships is removed all the same and the update
  says so (11903).
- **A copy is saved first.** The record goes to
  `sdsys/voc_removed.saved` under the account's name, the record's id, the date
  and the time, with who ran the update. If the copy cannot be saved the record
  is not removed (11904).
- **It is reported:** `3 VOC record(s) removed, because SD no longer ships
  them: margin stats supp` (11900), and on the audit trail one line for the
  account, `voc update account=sales removed=3 differs=0 locked=0 ids=margin,stats,supp`.
- **It runs before `newvoc.mods`**, so a record you add there on purpose has the
  last word.
- **A VOC the session may not write** ends that account's update, as for any
  write (11983).

The list is administrator-visible, and every removal can be undone:

```
list.voc.removed {account}
restore.voc account id | restore.voc account all
```

```
:list.voc.removed sales
13 VOC record(s) that SD no longer ships:
Name                          Went in   Use instead   sales
margin                        2.0-0     left.margin   [would be removed]
only                          2.0-0     id.only (written after the file name)   [kept: not the shipped record]
```

`list.voc.removed` prints the list with the release each record went in and
what to write instead. With an account it also says what the next update would
do in that account — removed, removed (a locked verb), kept (not the shipped
record), kept (locked), or absent — and **changes nothing**.

`restore.voc` puts back the newest saved copy of a record in an account, as it
was. It never overwrites: if the account holds a record of that name now it says
so (11918). `all` puts back every record of the account that has a saved copy.
The next `update.accounts` will remove a restored record again, because the
list has the last word; to keep one, give it a name SD does not ship or put it
in `newvoc.mods`.

Both verbs are SDSYS's, and are in the VOC of SDSYS only. The saved copies are
kept across a `deletesdcore.sh` that keeps your accounts and an install.

To keep an edit of your own to a record SD still ships, mark it — see below.

## Keeping your own version of a VOC record: `[locked]`

This has no equivalent in OpenQM or in SD on Linux. Nothing you know from
another MultiValue system will tell you it exists.

A site that has customized one of SD's own VOC records marks it by putting
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

**`[locked]` is honored on every kind of VOC record except a verb.** A verb
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
name SD does not ship, modeled on the system one. `update.accounts` walks the
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

## Your own changes to every account's VOC: `newvoc.mods`

An optional file called `newvoc.mods` in the SDSYS directory holds VOC records of
your own: a verb withdrawn, a Q-pointer to a shared file, a paragraph every
account should have. Each record in it is written to an account's VOC **after**
the standard records, so it has the last word.

| When | What happens to `newvoc.mods` |
|---|---|
| SD is installed | its records are written to SDSYS's own VOC as well (`bbproc`, the first bootstrap pass) |
| an account is created | its records are written to the new account's VOC |
| `update.accounts` runs | its records are written to the account's VOC where they differ, except over a record marked `[locked]` |
| SD is upgraded and the accounts are kept | `deletesdcore.sh` puts the file aside in `/home/sd` and `installsdcore.sh` puts it back before the first bootstrap pass |
| SD is deleted with its accounts | the file goes with them |

The file is a directory file: one record per file, the record id as the file
name, the VOC record as its contents. There is no file until you make one, and
nothing is created for you. The form to use is a directory file made by hand in
the SDSYS directory.

To see it work, put a record in the file and run `update.accounts`; then
`ct voc` the id in the account.

## The example programs: `load.examples` and `remove.examples`

SD ships a set of example programs: the five programs of the *SD Text User Interface -
Programmer's Guide* and a first course in programming (User guide, *SD Example
Programs*). They are installed in the directory `examples` of the SD system directory
(`/usr/local/sdsys/examples`), one file to a program. **No account gets them by itself**:
most accounts do not need them, so neither the installer nor `create.account` puts them
anywhere. A person who wants them loads them into their own account; you can load them
into accounts you name.

```
load.examples                       the account you are in
load.examples <account> ...         the accounts named, a list (the administrator only)
remove.examples                     the account you are in
remove.examples <account> ...       the accounts named, a list (the administrator only)
```

`load.examples` makes the file `examples.bp` in the account when it is not there, writes
each shipped program that is new or has changed, leaves alone a program it does not ship
(one you added), and compiles what it wrote, into `examples.bp.out`. A person types it in
their own account, or chooses **Example programs** in the Tools group of the home screen.
The two summary lines count the accounts, the programs written and compiled, and the
ones it kept; each program that did not compile, or account it could not enter, is named.
The run is on the audit trail (`load.examples accounts=... compiled=...`).

**It needs `bp.edit`.** Loading writes programs into `examples.bp` and compiles them, which
is what `bp.edit` decides, so an account without it (as delivered) is refused before
anything is written: *Programs can only be compiled or cataloged by an account that has
bp.edit*. On the home screen the tile is dimmed and says why. To let a person load the
examples, give the account `bp-on` (`modify.account <account> bp-on`), or load them for
the person with `load.examples <account>`. Either way `bp.edit` then also decides whether
the person may change the programs in `examples.bp`.

The administrator's list takes accounts by name (`load.examples ann bob`); a name that is
not registered is said and skipped, and the others go on. A suspended account cannot be
entered and is named. With no name the administrator's `load.examples` loads the SDSYS
account only.

`remove.examples` is the companion, with the same rule for who may. In each account it
deletes the shipped programs from `examples.bp` together with their compiled objects, and
keeps any program you added; it deletes `examples.bp` itself only when nothing of yours is
left in it. An account with no `examples.bp` is counted and left alone. Nothing puts the
programs back by itself; a `load.examples` does. The run is on the audit trail
(`remove.examples accounts=... removed=...`).

A change you want everywhere is made to the file under `examples` and spread with
`load.examples` to the accounts that have them; a change made in one account's
`examples.bp` is put back by the next run there.

## Reading and setting configuration: `config`

```
config                     report every setting
config lptr                the same, to the default printer
config param value         set one
config gpl                 display the license
config contrib             display the contributors
```

```
:config
Virtual Machine Version Number L2.0-0
CLEANUP   300 seconds
CMDSTACK  99
DEADLOCK  0
DHCACHE   10
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
| *Not a recognized private configuration parameter name* | the name is not one that can be set per-session |
| *Invalid value for this parameter* | it is, and the value is not |

**`config param value` sets a private, session-local value and not the
machine's.** The machine's settings live in SD's configuration file and are
read when SD starts. This form overrides one for the session you are in, which
is the right tool for trying a value before writing it down and the wrong one
for changing an installation.

**`config gpl` and `config contrib` shell out to `less`**, against two plain
files in the system directory (`sdsys/licence`, `sdsys/contrib`) — not a VOC
record, despite reading like one. `gpl.bp/config` runs `sh less
sdsys/licence` and `sh less sdsys/contrib` directly. That works because
SDSYS runs it — `config` is one of SDSYS's own verbs, and SDSYS is never
refused by the `sh-on` switch that gates `sh` for every other account.

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

**What it actually changes:**
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
delete.account account.name {remove.home} {no.query}
```

Removes the account directory, its Linux group, its entry in the accounts
register, and — for a user account SD itself created — the Linux user
itself. **One confirmation covers all of it**, and the wording is decided
before the question is asked, so it never offers to remove a Linux account it
is not going to. **The Linux user's home directory is kept unless you add
`remove.home`** — see *Managing accounts* in the Getting Started set.

**`no.query` leaves the confirmation out.** It is for a caller that has asked
already: `tool.accounts` gives it after you have typed the account's name in
its own dialog. Typed at the prompt it deletes at once, so leave it off there.

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

## Continued in

[Backing Up and Restoring Accounts](01b-backup-and-restore.html) —
backup.account, restore.account, set.backup.directory, tool.backups and
settings.report.

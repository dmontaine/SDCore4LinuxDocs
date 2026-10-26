Title: The Master Files
Subtitle: A copy of every account's VOC and dictionary records in the SDSYS account, kept up to date by a journal, and the way SDSYS changes any account's VOC or dictionary record by saving its copy: what is copied, how, what a save needs, what it refuses, and what it gives the sdsys user.

The SDSYS account holds **a copy of every VOC record and every dictionary record of every
account**. It exists so that SDSYS can look at all of them in one place and **change one by editing
its copy**. The copies follow the accounts in one direction (a journal, below) and the edits follow
the copies in the other (a save of a copy is written into the account's own file at once, or refused
with its reason and nothing changed). Only SDSYS sees any of it.

> **Read this first: what the grant is, and what it is not.** To write an edit into an account's own
> VOC or dictionary, **the `sdsys` operating-system user has to be a member of that account's Linux
> group (`sdu_`*name*), and the account's VOC and dictionaries have to be writable by that group.**
> **As delivered, `sdsys` is a member of no user account's group**, so a save of a copy to a user
> account is refused, with a message that names the way to switch it on. The administrator does that
> **for one account at a time**: `modify.account acme sdsys-on`; `modify.account acme sdsys-off` takes
> it away again. The membership gives the `sdsys` user **write access to everything the account's group
> may write** - not only the VOC and the dictionaries (files that SD sessions create are group-writable
> under SD's usual umask, 002) - and it is also, as far as the modes and the group show, what lets SDSYS
> write inside the account in any other way (`logto` and an editor, an interactive `update.accounts`);
> that part has been read from the modes and has not yet been measured on a real install. A VOC entry or an I-type is code that
> runs in the account, so **while it is on, a compromised `sdsys` login can change what that account
> runs.**
>
> **It is a default and a record of the administrator's decision. It is not a wall.** A person who has
> taken over the `sdsys` login can reach the code of every account without any membership, by three
> routes that this does not change: **the files that `root` runs belong to `sdsys`** (`bin/sd` and
> `bin/sdlnxd` are run by `sd.service` and `sd-lnxd.service` as root, and `sdsys` can replace them);
> **the global catalogue is the `sdsys` user's to write**, and every session loads programs from it;
> and **`sdsys` may run `sudo /usr/local/sbin/sd-elevate` with any arguments**, which can put `sdsys`
> back in a group, hand it an account's VOC directory or `%0`, or set an ordinary user's password. So
> **do not read the switch as protection against a stolen `sdsys` login: it is not tighter against
> one.** What it does is take away the *silent* route: until the administrator says so, no account's
> group lists `sdsys`; saying so leaves an audit line (`modify.account sdsys-on account=acme`) and a
> line in the system log (`sd-elevate`), and it can be taken back. It is not a route in from the
> network (`sdsys` has no remote access at all), and a process that is not a real `sdsys` login is not
> an administrator.
>
> **History.** The owner chose the membership of every account's group on 17 October 2026, with that
> warning, in place of the tighter arrangement, an *outbox* the account applies for itself, which would
> have given `sdsys` no such access. From 1.2-0 it is **off as delivered** and switched on per account.
> An install that finds `sdsys` in the groups of accounts a release before 1.2-0 put it in asks once
> whether to keep it there (below); the default answer takes it out.

| file | key | holds |
|---|---|---|
| `voc_master` | *account*`*`*record id* | a copy of every record of every account's VOC |
| `dict_master` | *account*`*`*file*`*`*record id* | a copy of every record of every dictionary |
| `master_state` | `v*`*account*`*`*id*, `d*`*account*`*`*file*`*`*id*, and `$journal` | for each copy, a checksum of the account's record when it was copied and the time; and where the last drain stopped |
| `$master.journal` | | one line for each change, waiting to be applied |

A key is cut at its **first** asterisk (a VOC key) or its **first two** (a dictionary key), and no
further, so a record id may itself contain asterisks. The *account* of a dictionary is **the account
whose directory holds it**, not the account that happened to open it: a dictionary reached through a
pointer in another account's VOC is the first account's, and the second has no copy of it. The *file*
is the dictionary's path below the account's directory without `.dic`, which is the file's own name
for the usual `zmf1.dic` next to the data file `zmf1`. The `master_state` key begins with a letter
because a VOC record whose id is `file*id` would otherwise have the key of a dictionary record.

All three are ordinary hashed files with case-insensitive ids, with a dictionary each, and each has
an entry in the **SDSYS VOC and in no other VOC**: a new account is made from `newvoc`, which has
none. **Their directories are mode 0700 and their files 0600, owned by the `sdsys` user** (made
under a umask of 077, and set again by `sync.masters` and by the install), so that nobody but
`sdsys` (and root) can open them. They hold every account's pointer paths and I-types, and the
group of an SDSYS session is `sdusers`, which every SD user is in: the group is not what keeps users
out, and the files have no group bit and no other bit whatever group they are made in. (They were
0770 and 0660 before the independent review of 19 October 2026, with a group that was never set; a
system that has them so is put right by the next install, or by `sync.masters` run by `sdsys`.)
The journal is mode 0620, owner `sdsys`, group `sdusers`, so that every SD user's session can append
a line and nobody but SDSYS can read one.

## How the copies are kept (account to master)

**Every write passes one place.** The kernel's hashed-file layer calls the hook after a record of a
VOC or a dictionary has been written, or deleted, or the file cleared; after such a file is made,
removed or renamed (`create.file`, `delete.file`, an `ospath` delete and `osrename`); and
after `oscopy` or `ioscopy` has copied something into one. It does not matter who wrote: a user
program, `ed`, `create.file`, `cd` compiling an I-type, `copy`, an `$internal` verb, SD itself, **or
SDSYS's own save of a copy** (the write it makes into the account is journalled like any other).
A **transaction** is journalled when it commits, because that is when the file is written, and a
rolled-back transaction is not journalled at all.

**What the hook writes is one line, and the line holds keys, never data:**

```
1760875000 d w acme zmf1 F1
```

the time; `v` (a VOC) or `d` (a dictionary); what was done (`w` written, `d` deleted, `c` cleared,
`n` made or copied into, `x` removed); the account; the dictionary file (`-` for a VOC); the record
id (`-` when the line is about the whole file). Spaces, control characters and `%` in a name or an id
are written as `%20`, `%0A`, `%25`, so that one id cannot become two lines. The line is written with
a single `O_APPEND` write, the way the audit trail is.

**The journal is made by SDSYS and never by a session**, so that a session cannot own it. A system
whose journal does not exist yet is a system with no master files: the hook says nothing and costs
one failed `open`. A journal that has gone missing where the master files exist (somebody moved it)
is a lost journal, and raises the *stale* flag below.

**The hook never stops the write that called it.** If the journal cannot be written, the user's
write still succeeds and a flag is raised in the shared memory that `check.masters` and
`list.master.pending` report (*stale*). A journal that has reached 4 MB is not appended to; the
lines that would have gone into it are counted, and a second flag (*resync*) is raised. Both flags
are cleared only by `sync.masters` with no account, because a lost line could have belonged to
anyone. They are held in shared memory, so they start again when SD restarts; `check.masters` compares
every record in any case, so a difference is found whether or not a flag survived.

**The drain** applies the journal. **It runs when SDSYS opens `voc_master`, `dict_master` or
`master_state`, by name or by path, and when `sync.masters` or `check.masters` runs.** The journal
from the saved position to its end is read, and each *distinct* key, or each distinct *file* for a
line about a whole file, is made to match the account's record **as it is then**: the account's
record is read; the copy is written if it differs, or removed if the account no longer has the
record; the checksum and the time go into `master_state`. Because it applies the state and not the
line, applying a line twice does nothing, and a crash half way is repaired by the next drain.
Lines for an account that is not registered, and lines that are not a line, are counted and skipped.
When everything up to the end of the journal has been taken the journal is emptied, under the same
lock that the hook appends under, so that a line cannot fall between the drain's last look and the
emptying. A drain that finds nothing writes nothing. **A last line with no newline** (a writer that
died half way, or one forged: the journal is writable by every SD user's group so that they can
append) is ended by the drain, so that the next line written is a line of its own and is not glued to
it and refused with it; the hook also cuts the journal back when a write comes up short.

## Changing an account by saving its copy (master to account)

SDSYS signs on, opens `voc_master` or `dict_master` (the drain has just made them true), **reads
a record**, and **saves it**: with `ed` (which reads the record first), or from a program's `read`
and `write`. Nothing else is needed, and the check is made in the one place every write to a hashed
file passes, so any other way of writing a record of a master file (another editor, `copy`,
`writev`, `matwrite`) is checked in the same way. **A save is of a record the session has READ**:
the kernel remembers, for this session only, the last 128 master records it read (`read`, `readu`,
`readv`, `matread`) and what each held, and a save is judged against that (step 5). For example, to
add a verb to account `acme` from the SDSYS account:

```
:ED VOC_MASTER acme*weekly.report
```

and file it. Its record is in `acme`'s VOC, in the account's own file, before the editor has
finished: a session of `acme`'s user that lists its VOC sees it.

**What the save does**, in this order, and **where it stops at the first thing that is wrong**:

1. Only **SDSYS, signed on at a terminal** (the administrator), may save a copy.
2. The key must be *account*`*`*id* (`voc_master`) or *account*`*`*file*`*`*id* (`dict_master`), with
   a registered account, a non-empty id and, for a dictionary, a dictionary of that name that the
   account holds. (A key is cut at the first one or two asterisks; an id may hold more.)
3. **This session must be able to write the account's file.** SD asks the operating system before
   it takes a lock or writes a byte: the directory must be searchable and `%0` and `%1` writable
   by the `sdsys` user. If not, the message says why (below).
4. The account's record is **locked by a try-lock that returns at once**. A save never waits: the
   account's own process may hold the record and be waiting for the master, and a wait would be a
   deadlock nobody could see. If another session holds the lock, the save is refused and says who.
5. **The account's record, as it is now, must be the one this session READ.** The kernel
   compares its checksum with that of the record the session read (it remembers it when the
   session reads a record of a master file). If the account has changed the record since,
   the save is **refused and nothing is lost**: open the master file again, read the record,
   and make the edit again. This is a comparison with what *you* read, and not with
   `master_state` (the version of the last drain), because a drain made by anyone between
   your read and your save - another administrator session opening a master file,
   `check.masters`, `sync.masters` - moves `master_state` to the account's newer record, and a
   save compared with that would overwrite the account's change. **A record this session has not read** (a program
   that writes a master record without reading it; a record read so long ago that 128 others
   have been read since) is refused when the account has a record of that name (message
   11596: read it first), and when `master_state` remembers one the account has since deleted.
   A *new* key (no such record in the account, none in `master_state`) is simply a new record.
6. **The account's own file is written, by SDSYS's own process,** through the same write every
   other writer uses: so the file keeps its owner and group (it is written in place), its indices
   are kept, and the write is journalled. **The comparison of step 5 is made again inside this
   write**, with the record's group locked in the file and before a byte is changed: a plain
   `write` by the account's user takes no record lock, which the try-lock of step 4 cannot see, and
   one that lands between step 5 and the write is therefore caught here, the save refused as in
   step 5 and the user's text kept. The account's user can still write the record just after
   SDSYS's write has finished; that is the later change of two writers, as it is anywhere.
7. `master_state` is brought up to date, and so is what the session has read of the key, so that a
   second save of the same key in the same session is not taken for a change by the account. The
   lock is let go.
8. The master record is written, as `write` would. (If that last write fails, the master and
   `master_state` are repaired by the next drain.)
9. **One line is written to the audit trail**, in lower case: `master edit account=acme file=voc
   id=weekly.report`, or `file=zmf1.dic` for a dictionary (the user, the process and the time are
   put in front by SD, as for every audit line).

**A save that is refused writes nothing anywhere**: not the account, not the copy, not
`master_state`, not the audit trail. Without `on error`, the program ends with the message below.
With `on error`, `status()` is **8910**, and `kernel(K$MASTERS, 'refusal')` returns the message
(field 2). **`ed` handles it as it handles any write error**: it prints `Write error 8910 (o/s error 0)
- Data not saved. Original data will be lost if you leave the editor now.`, then the message, and
stays open with your text, so that you can correct the cause and file it again. **`check.masters`
and `list.master.pending` end with the last refusal of the session** (`The last save of a master
record in this session was refused: ...`), which is the way to read it after an editor that shows
only the status.

| the message begins | and means | do |
|---|---|---|
| `Master record ... not saved: its key must be account*id or account*file*id of a registered account` | the key is not one | check the spelling |
| `... %s is not a registered account` | no such account in the register | |
| `... the account has no VOC` / `no dictionary of that name` | there is no such file to put it in | make it in the account first |
| `... the record in acme has changed since you read it. Nothing was changed.` | the account changed it after this session read it (or deleted it) | open the master file again, read the record and repeat the edit |
| `... this session has not read it, and the account has a record of that name` | the save is of a record this session has not read (or read so long ago that it has been forgotten) | read the record first, then save it |
| `... the account's record is locked by user N, and a save never waits` | another session holds the record | try again later |
| `... no lock could be taken on the account's record (the lock table is full or a limit was reached)` | no user holds it: the lock table is full, a deadlock was seen or this session is at its limit | try again later; `list.readu` |
| `... this session cannot write the VOC of acme (see check.masters)` | the mode does not let the group write, or this session cannot use it | `check.masters`; `modify.account acme sdsys-on` puts the modes right (it is repeatable) |
| `... this session began before sdsys joined group sdu_acme` | see below | sign on again as SDSYS and repeat the edit |
| `... sdsys is not in the group of acme. Nothing was changed. Use modify.account acme sdsys-on` | **master edits to the account are switched off, which is how every user account is delivered** | `modify.account acme sdsys-on`, then sign on again as SDSYS |
| `... only SDSYS, signed on at a terminal, can change a master file` | not the administrator | |
| `... the account's file could not be written (error)` | the write itself failed | `check.masters` |

**A session of SDSYS that began before `sdsys` was put in the account's group** (by
`modify.account acme sdsys-on`, or by an install that kept it) **cannot write that account's files**
until SDSYS signs on again. Linux fixes a process's groups when it starts and `sd` never reloads them,
so the session is still without the group even though `/etc/group` now lists `sdsys`. The save says
so (`began before sdsys joined group`) and `check.masters` shows `norights ... stale-session`. Sign
off and on as SDSYS. The same holds the other way: `sdsys-off` does not remove the group from a
session that is already running, so **a running SDSYS session keeps its write access until it
ends**; a stolen running session keeps it too.

**Two things are not delivered.**

* **A delete.** Deleting a copy does not delete the account's record, and the plan was that SDSYS
  *saves*. A `delete` of a record of a copy is refused (`Master record ... not deleted: that
  does not delete the account's record. Delete it in the account, then run sync.masters`). `clear.file`
  of a master file is allowed and touches no account; `sync.masters` puts the copies back.
* **A save inside a transaction.** The write reaches the file at `commit`, half way through the
  transaction's other writes, where a refusal could not be undone. A `write` or `delete` of a copy
  inside `begin transaction` is refused at the statement.

**What a save does not do.** It does not ask the account's `voc.edit` or `dict.edit` gate: SDSYS is
never refused those. A trigger set on the account's dictionary belongs to the statement that writes
it, and the account's write here is the kernel's own, so it is **not** run.

## The verbs

All three are in `voc_template` and nowhere else, so only the SDSYS account's VOC has them, and each
refuses an account that is not the administrator ("Command requires administrator privileges"). The
kernel asks again for each thing they do, so a copy of the verb in another VOC does nothing for anyone.

```
sync.masters
sync.masters acme
check.masters
check.masters acme
list.master.pending
```

**`sync.masters`** sets the master files up if they are not there (the journal, the three files, their
dictionaries, their VOC entries in the SDSYS VOC, their modes), applies the journal, and then makes
the copies of **every registered account** match the accounts. It also removes the copies of accounts
that are not registered. **With an account name** it does that for one account and does not clear the
flags. It prints, for each account, a line such as

```
Account acme: 466 VOC record(s), 4 dictionary file(s), 7 dictionary record(s)
   0 master record(s) written, 0 removed, 0 left out because the key is too long
```

The first run on a system is the only one that writes a great deal; a second run with nothing
changed writes nothing. **A full run makes one call to the kernel for all the accounts**, which
reads each master file once into a sorted index and finds each account's records in it: the time
grows about in step with the number of accounts. (It used to read every master file once for each
account, and 204 accounts took 2.7 to 3.2 times as long as 104.) Measured on a private SD
(19 October 2026, a machine with two virtual machines running), with accounts of about 500 VOC
records and a few dictionary files each, a full `sync.masters` with nothing changed took 2.8 s for
104 accounts and 4.3 s for 204 (11.9 s and 32.2 s before this was changed), and `check.masters`
1.7 s and 2.6 s (4.5 s and 12.5 s before); the install runs a full `sync.masters`. Doubling the
accounts took 1.5 times as long, not 2 and not 4 (a session start and the SDSYS account itself are
the same for both). `sync.masters` with one account name still reads the master files once for that
account.

**`check.masters`** applies the journal and then **compares and reports; it changes nothing.** For
every account (or the one named) it looks at the VOC and at every dictionary the account holds, and
prints a line for each of these, in the form *kind*: *account* *voc or dict* {*file*} {*id*}:

| kind | meaning |
|---|---|
| `differs` | the copy is not the account's record (an edit made outside SD, or a change the journal lost) |
| `missing` | the account has the record and the copy does not |
| `extra` | the copy has a record the account does not have: a dictionary the account no longer holds, a record deleted at the operating system level, or an account that is not registered |
| `nonwritable` | the VOC, or a dictionary, has a directory without group search and write, or a subfile (`%0`, `%1`) without group write. A save of a copy is written as a member of the account's group, so it needs the modes. **Said only of an account whose master edits are on** (the group lists `sdsys`; `modify.account acme sdsys-on` puts the modes right). (The SDSYS account's own files are not asked this: `sdsys` writes them as their owner, and the master files' dictionaries among them are 0700.) |
| `norights` | the modes are right and **this session** still cannot write the file. The last word says why: `mode` (the owner's permission, for a session that is the owner), `stale-session` (the group lists `sdsys` and this session began before it did: sign on again), `not-a-member` (the group does not list `sdsys`; an account that is off never gets this row, it is counted - below), or `no-write` (anything else: a mount, an ACL). **Said only of an account whose master edits are on** |
| `toolong` | the key (*account*`*`*id*, or with the file) is longer than the system's `MAXIDLEN` less two characters (the state key is two longer), and cannot be copied |
| `unreadable` | the file is there and could not be opened or read through; or (`unreadable: acme dict`, no file named) the account's directory could not be listed or its VOC could not be read, so the list of its dictionaries is not known: **no dictionary copy of that account is then called extra, and `sync.masters` deletes none of them** (a copy is never deleted for want of being able to read the original) |

When there is a `nonwritable` or `norights` row a line follows that says what they mean. **Then,
when any user account has master edits switched off, one line says how many** (`Master edits are
switched off for 3 account(s): the sdsys user is not in their group. To switch one on: modify.account
<account> sdsys-on`). **Those accounts are counted, once each, and are not differences**: nothing is
said of their modes, and the number of differences does not include them. (An account counts as off
when its files belong to another user and its group does not list `sdsys`; the SDSYS account, a group
account and any account whose files `sdsys` owns are never off, because `sdsys` writes them as their
owner. On a machine that has no `sdsys` user nothing is off.) Then the *stale* and *resync* lines if
the flags are up, then "Every master copy matches its account" when there is no difference, and last
**`Checked 5 account(s): 0 difference(s)`**. A listing stops at 2,000 rows. (A `differs` after stage 2 no longer comes from editing a copy: a saved copy is delivered
or refused. It comes from a change made to an account without the journal hearing of it.)

**`list.master.pending`** shows the journal lines that have not been applied and the flags, and
applies nothing. It says "Nothing is waiting in the journal" when there is nothing.

### All of it on one screen: `tool.masters`

```
tool.masters
```

**A full-screen page for the administrator** (SDSYS's VOC only; an ordinary account has no such
verb, and the page is refused before it reads anything to anyone who is not the administrator). It
needs a window of 140 columns by 43 lines. The top box says whether the master files are set up
(or prints the verb's own sentence that they are not), what the journal holds, whether the
*stale* or *resync* flag is up, how many accounts were compared and how many differences there
were, how many accounts have master edits switched off (a line of its own, when there are any), and
why the last save of a master record in this session was refused. The list is every
registered account with its state — *in sync* or *n differences* — and, last, any account that
has master copies but is not registered (*not registered: n to remove*). The box under it lists
the differences of the account under the cursor, one line each, and explains the state in plain
words, with a sentence for each kind of difference present.

| Key | What it does |
|---|---|
| arrows, Page Up, Page Down, Home, End, a click | move over the accounts |
| S | `sync.masters` for every account |
| Y | `sync.masters` *account* for the account under the cursor |
| P | show the journal lines not yet applied in the lower box, and back |
| F5 | check again |
| F1, ?, a click on the [?] | explain the page |
| Ctrl-Q | leave |

**It reads when it opens, after a sync and on F5 — not on a timer, because a check reads every
master file.** Like `check.masters` it first applies the journal, so a record an account's own
session wrote a moment ago is not shown as a difference. **For every account the number it shows
is the number `check.masters` prints**; the page's tests compare the two. S and Y each show the
command and what it does in a box answered Run or Cancel (Cancel is what Enter chooses) and run
the real `sync.masters` through the one routine that runs commands, which allows nothing else.
S says, when the files are not set up, that it sets them up first. Y says that it does **not**
clear the stale and resync flags — only S does. Y is refused, in words, for an account that is
not registered (use S, which removes its copies) and before the files are set up. The verb
writes its own audit line. **The page edits no master record and no account record**, and does
not ask the kernel to sync, set up or note anything itself.

**Not on the page:** the stale and resync flags are shown (as the verbs show them) but a test
cannot make a journal write fail or overflow, so that display is read from the source and not run.

## Who is in the group, and what the files must say

The save needs the `sdsys` user in the account's group **and** the account's files writable by that
group. **As delivered neither is arranged for a user account: it is the administrator's act.** The state
*is* the Linux group membership, as it is for `ssh` and the API (`sdssh`, `sdapi`); nothing is written
to the register, and there is no row for it in the gate matrix (`tool.gates`).

**`modify.account` *name* `sdsys-on` and `sdsys-off`** (a user account only; a group account has no
group of its own for the `sdsys` user and is refused: it owns the files of a group account, so it needs
nothing):

```
modify.account acme sdsys-on
modify.account acme sdsys-off
```

* **`sdsys-on`** puts the `sdsys` user in the account's group (`sd-elevate sdsys-join`) and then makes
  the account's VOC and dictionaries group-writable (`sd-elevate group-write`). It says `Account acme:
  master edits are on. The sdsys user is in the group of the account and can write everything that
  group may write. Sign on again as SDSYS; a session already running does not have it`. **It can be
  said again**: for an account that is already on it runs `group-write` again, which repairs a mode (a
  VOC or dictionary that arrived by `restore.account` or a copy at the operating system level, and
  that `check.masters` shows as `nonwritable`) and changes nothing else. The state it prints is read back from `/etc/group`: a read back that does not show the
  wanted state is reported as a failure, never as a success (`Account acme: ... failed, status 2`).
* **`sdsys-off`** takes the user out (`sd-elevate sdsys-leave`) and says `Account acme: master edits are
  off`. For an account that is already off it says `acme already had that access; nothing changed`.
  **It does not end a session of SDSYS that is already running** (a process keeps the groups it started
  with), so that session keeps its write access until it ends.
* The two words conflict only with each other (`modify.account acme sdsys-on sdsys-off` is refused,
  nothing changed) and may be given in a command with other words. Both are audited, in lower case:
  `modify.account sdsys-on account=acme`, and `sd-elevate` writes a line of its own to the system log
  (`journalctl -t sd-elevate`).
* **`create.account` does not switch it on**, and neither does the installer's "Open every access gate"
  answer: the installing user's account is delivered off like every other. Type it.

**What is expected to stop working when an account is off.** A save of its master record (above). So
is **SDSYS writing inside the account in any other way**: `logto` the account and make a file, edit a
program, catalogue; an interactive `update.accounts` for it; `sd -A`*account* from the operating
system. (The installer's own `update.accounts all` runs as root and is not affected.) `create.account`,
`delete.account`, `backup.account`, `restore.account`, `sync.masters`, `check.masters`, and reading the
account (`logto` and a listing) are done by the root helper or only read the files, and are expected to
work. **This is read from the modes and the code; it has not yet been measured on an install** (the
witness, `witness-masters.sh` sections 3 to 5, is written to measure it). Before 1.2-0 that general
write was there for every account, because the membership was; switch the account on for the time SDSYS
needs to work inside it.

**A new user account** gets its group `sdu_`*name* from `create.account` with `root` and the user as
members, and no one else. A **group account** is made with `root` and `sdsys` in its group
`sdg_`*name* and is owned by `sdsys`, so it needs nothing. **`delete.account` needs nothing**: the group
goes with the account.

**The install and every upgrade** make one decision, **once**, about the accounts that a release before
1.2-0 put the `sdsys` user in the group of. The question is asked up front, with the installer's other
questions, only while the marker `/home/sd/$groups.ruled` is absent and some `sdu_` group lists `sdsys`:

```
The sdsys user is in the group of 3 user account(s): an earlier release put it there, and it can write everything those groups may write in those accounts.
As delivered now, the sdsys user is in no user account's group, and SDSYS puts it in one with modify.account <account> sdsys-on and takes it out with sdsys-off.
This is asked once. Answer n to take it out of those groups now.
Keep the sdsys user in the group of 3 account(s) (it can then write their files)? (y/N)
```

**The default is n**, and it is also the answer when no answer can be read (no terminal, a closed
input; the installer prints `No answer could be read: N.`). With `n` the install runs
`sd-elevate sdsys-leave` for each of those groups and prints each (`the sdsys user is no longer in the
group sdu_acme`); with `y` it changes nothing. **Then it writes the marker**, so that the
administrator's later `sdsys-on` or `sdsys-off` stands: with the marker present the installer does not
ask and does not touch a group. A fresh install, and an upgrade that finds the user in no group, write
the marker without asking. **If a group could not be left, the install warns (with the command that
repairs it), goes on, and does not write the marker**: running the installer again asks again. The
marker is in `/home/sd`, not in the sdsys directory, because `deletesdcore.sh` removes the sdsys
directory in every cycle and would lose it; `/home/sd` is kept with the accounts and removed with them.
(Taking the marker away asks the question again. The question lists only groups named `sdu_`*name* whose
member list holds the whole name `sdsys`; `sdusers` and a group account's group are never asked about.)

**Three `sd-elevate` verbs do the work, each confined**, and none is more than `modify.account` and the
install need. Each leaves a line in the system log (`logger -t sd-elevate`) after it has changed
something:

| `sd-elevate` | does | refuses |
|---|---|---|
| `sdsys-join sdu_`*name* | puts the user `sdsys`, **and no other user**, in that group (`usermod -aG`: it adds, it never replaces) | any group that is not `sdu_`*user* of an SD user who exists (not `sdusers`, not a route group, not `sdg_`, not `sdu_root`, not `sdu_sdsys`), a group that does not exist |
| `sdsys-leave sdu_`*name* | takes the user `sdsys`, **and no other user**, out of that group (`gpasswd -d sdsys`: it removes that one membership and no other); a group that does not list `sdsys` is answered `sdsys is not in sdu_`*name* with exit 0 and left as it is | the same groups as `sdsys-join`, and the same user part; the user is written in the helper, never an argument and never taken from the environment |
| `group-write` *account directory* | gives the account's own group write on its VOC and its dictionaries (g+rwx and setgid on the directories, g+rw on the files in them) | an account directory that is not a direct child of `user_accounts` or `group_accounts`, or whose group is not `sdu_`*name* (`sdg_`*name* for a group account): never `sdusers`, which every account is in |

`sdsys-join` and `sdsys-leave` change one membership of one user and nothing else. `group-write` changes modes only, never owners or groups. It works on file descriptors opened
without following links, so a link a user plants in the tree cannot make root change another file;
it changes only what has the account directory's owner (or `sdsys`) and the account's own group,
leaves the other bits as they are, and does not leave the account directory's filesystem. It says
what it did, and a second run changes nothing.

### The modes of what SD makes

Every session starts with a `umask` of 002, so a VOC or a dictionary made in the ordinary way is
already group-writable (664 files, 775 directories). A user who changes the umask (the `umask`
verb) would make them closed, so **SD gives a VOC or a dictionary that it has just made its group's
write bit, whatever the umask**: the directory g+rwx and setgid, `%0` and `%1` g+rw. It does so
**only where the account's own directory lets that group write** (if the directory is 755, nothing
is added: a group that cannot write the account directory is not given the VOC), **and only where
the `sdsys` user is in that group** (from 1.2-0: where master edits to the account are off, group
write on a new VOC or dictionary would serve nobody, and nothing is forced), only to what the
session itself has just made, and it adds group bits and takes nothing away. The data file next to
a dictionary is not touched. A VOC or dictionary that arrives some other way (`restore.account`, a
copy at the operating system level) keeps the modes it came with: `check.masters` lists any that
are not writable in an account that is on, and `modify.account` *name* `sdsys-on` (`sd-elevate
group-write`) puts them right, the ones made while the account was off included.

## Accounts being made, restored and deleted

* **`create.account`** makes the group of a user account without `sdsys` in it (master edits start
  off; `modify.account` *name* `sdsys-on` switches them on), and copies the
  new account's VOC and dictionaries as soon as its register record is written. (The VOC is filled
  before the record exists, when the hook cannot yet tell whose it is.)
* **`delete.account`** removes the account's copies, after the register record has gone.
* **`restore.account`** copies the restored account, because a restore replaces its files at the
  operating system level. It does not change their modes; `check.masters` shows any that the
  archive did not keep group-writable.
* **The installer** runs the one-time ruling above and then the whole of `sync.masters` on every
  install, after the accounts have been brought forward and before the register is handed to `sdsys`,
  and prints a warning, and goes on, if either did not finish.
* **`update.accounts`**, like every other writer, writes through the hook and needs nothing more.

## What it does not do

* **It does not deliver a delete.** See above. (Whether deleting a copy should delete the account's
  record is a decision for the owner.)
* **It does not see a change made outside SD**: a shell command, a program run by an account that
  holds OS.EXECUTE, `sdfix`. `sync.masters` brings the copies up to date, and `check.masters` finds the
  difference. A save made after such a change is refused as a change.
* **A key that does not fit is not copied.** `MAXIDLEN` in `sd.conf` is 63 unless you set it, and a
  master file holding a longer id cannot be opened again, so the copy of a VOC record whose
  *account*`*`*id* is longer is left out, counted, and reported by `check.masters` as `toolong`.
  Raising `MAXIDLEN` (as far as 255) copies them. A dictionary file whose name contains an asterisk is
  not copied at all.
* **It finds the dictionaries an account holds** in the top level of its directory (`*.dic`) and
  those its VOC names that lie below it. A dictionary kept elsewhere is journalled when it is written
  but is not found by a full `sync.masters`. `sd-elevate group-write` looks for `*.dic` directories
  at any depth below the account directory. **A VOC or a dictionary that is a symbolic link to a place
  outside the account's directory** (another account's dictionary, say) **is not the account's file**:
  it is not copied under the account's keys, a save to it is refused as "the account has no dictionary
  of that name", and nothing is opened through it.
* **A dictionary key is case blind in its file part too.** `ZMONE*ZMF3*X` is `zmone`'s `zmf3.dic`
  (every dictionary SD makes is named in lower case, and a name that is really there in capitals is
  found as it is).
* **A save of a record the session has not read is refused** when the account has the record (step 5):
  a program that edits master records must read them first, as `ed` does.
* **It cannot be shown to work on a machine with one operating-system user.** The sandbox suite shows
  every part but ownership and groups; `witness-masters.sh` (run by the owner as root, on a real
  install) shows the group membership and its two verbs, the modes, root changing only the account's
  own files, the refusal for an account that is off, the administrator's `sdsys-on` and the edit
  reaching a user's VOC at once, the refusal for a session that began too early, the installer's
  one-time ruling, what is not lost when an account is off, the three routes of the first page
  (that they are there), and that the master files are owned by `sdsys`, have no group or other bit,
  and cannot be opened by a user who is in `sdusers` (section 6). **The version of the witness for
  1.2-0 has not been run on an install yet.**

## Cost

A write to a VOC or a dictionary does the work above; **a write to any other file costs one test of a
flag** (and one more, once per open file, to learn that it is none of the master files). Measured on
a private SD, on a memory file system, 100,000 writes of distinct records by an ordinary program,
the median of three runs (19 October 2026):

| | VOC record | dictionary record | data record |
|---|---|---|---|
| the build before the master files | 15.5 microseconds | 14.4 | 15.2 |
| this build, before the master files exist (no journal) | 19.4 | 20.4 | 14.5 |
| this build, with the master files and the journal | 21.6 | 20.1 | 13.1 |

So **a write to a VOC or a dictionary costs about 4 to 6 microseconds more (25 to 40 percent)
before the master files exist, and about 6 (40 percent) with them; a data file's writes are not
touched.** The numbers move with the load of the machine: an earlier run the same day, on a quieter
machine, gave 13.1, 18.3 and 19.5 microseconds for the VOC, the same differences on lower numbers.
The journal's own append is the difference between the last two rows, 2 microseconds for the VOC and
nothing that stands out of the noise for a dictionary; the rest is, as far as the code shows (not
measured apart), paid before the hook knows whether the file is anyone's: it asks for the journal
first, which on a system that has none is an `open` that fails and a `stat`. A program that writes the
VOC or a dictionary in a loop pays for each write; the writes people make by hand are few. Applying
the journal took 0.29 s for 5,000 waiting keys, 0.87 s for 20,000 and 1.69 s for 40,000, the open of
the master and a session start included: about 40 microseconds for each key. A journal that reaches
4 MB (about 90,000 lines of the length these loops wrote) takes no more and raises the resync flag.
`check.masters` compares every record of every account: it took 27 s for one account that held about
600,000 VOC records and as many dictionary records (the measurement above wrote them), the 91,422
journal lines it applied first included, and it found 508,578 differences, the changes the full
journal had dropped. **The journal grows with the changes people make, not with use.** On a private SD, signing on and off, `who`, `list` and `sselect` wrote no VOC or
dictionary record at all; `create.file` wrote two (the pointer and the dictionary's `@id`),
`delete.file` one, a new saved sentence (`.s`) one, and `save.list` one the first time (the
`$savedlists` pointer). The record `$command.stack` is written once, when an account is made; the
command stack itself is saved to a file in the account's `stacks` directory, which is not mirrored.
A save of a copy is a few session starts' worth of work only because it opens four files; it is
not a cost anyone else pays.

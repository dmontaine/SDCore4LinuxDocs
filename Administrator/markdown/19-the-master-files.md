Title: The Master Files
Subtitle: A copy of every account's VOC and dictionary records in the SDSYS account, kept up to date by a journal, and the way SDSYS changes any account's VOC or dictionary record by saving its copy: what is copied, how, what a save needs, what it refuses, and what it gives the sdsys user.

The SDSYS account holds **a copy of every VOC record and every dictionary record of every
account**. It exists so that SDSYS can look at all of them in one place and **change one by editing
its copy**. The copies follow the accounts in one direction (a journal, below) and the edits follow
the copies in the other (a save of a copy is written into the account's own file at once, or refused
with its reason and nothing changed). Only SDSYS sees any of it.

> **Read this first: what it gives the `sdsys` user.** To write an edit into an account's own VOC or
> dictionary, **the `sdsys` operating-system user is a member of every account's Linux group
> (`sdu_`*name*), and every account's VOC and dictionaries can be written by that group.** This
> gives the `sdsys` user **write access to those files in every account**, and to anything else in
> an account that the account's group may write (files that SD sessions create are group-writable
> under SD's usual umask, 002). A VOC entry or an
> I-type is code that runs in the account, so a compromised `sdsys` login is a route into every
> account. It is not a route in from the network (`sdsys` has no remote access at all), and a
> process that is not a real `sdsys` login is not an administrator. The owner chose this on
> 17 October 2026 in place of the tighter arrangement, an *outbox* the account applies for itself,
> which would have given `sdsys` no such access. If you do not want the membership, take it away
> (`gpasswd -d sdsys sdu_`*name*): saves of copies to that account are then refused with a message,
> and everything else works.

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
none. Their directories are mode 0770 and their files 0660, so that SDSYS and its group are the only
users who can read them; the journal is mode 0620, so that every SD user's session can append a line
and nobody but SDSYS can read one.

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
emptying. A drain that finds nothing writes nothing.

## Changing an account by saving its copy (master to account)

SDSYS signs on, opens `voc_master` or `dict_master` (the drain has just made them true), and
**saves a record**: with `ed`, or from a program's `write`. Nothing else is needed, and the check is
made in the one place every write to a hashed file passes, so any other way of writing a record of a
master file (another editor, `copy`, `writev`, `matwrite`) is checked in the same way. For example,
to add a verb to account `acme` from the SDSYS account:

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
5. **The account's record, as it is now, must be the one the copy was made from.** The kernel
   compares its checksum with `master_state`'s. If the account has changed it since SDSYS opened
   the master (the drain brings the copy and `master_state` up to date when SDSYS opens it), the
   save is **refused and nothing is lost**: open the master file again, look at the record, and
   make the edit again. A record the account has and the copy has never had is such a change, and
   so is a record the account has made since. A *new* key (no such record in the account, none in
   `master_state`) is simply a new record.
6. **The account's own file is written, by SDSYS's own process,** through the same write every
   other writer uses: so the file keeps its owner and group (it is written in place), its indices
   are kept, and the write is journalled.
7. `master_state` is brought up to date, so that a second save of the same key in the same session
   is not taken for a change by the account. The lock is let go.
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
| `... the record in acme has changed since this copy was made` | the account changed it after SDSYS opened the master | open the master file again and repeat the edit |
| `... the account's record is locked by user N, and a save never waits` | another session holds the record | try again later |
| `... this session cannot write the VOC of acme (see check.masters)` | the mode does not let the group write, or this session cannot use it | `check.masters`; the install's upgrade puts the modes right |
| `... this session began before sdsys was put in group sdu_acme` | see below | sign on again as SDSYS and repeat the edit |
| `... sdsys is not in group sdu_acme (sd-elevate sdsys-join ...)` | the membership is not there | run `sudo /usr/local/sbin/sd-elevate sdsys-join sdu_acme` from the `sdsys` login, sign on again |
| `... only SDSYS, signed on at a terminal, can change a master file` | not the administrator | |
| `... the account's file could not be written (error)` | the write itself failed | `check.masters` |

**A session of SDSYS that began before the account was made, or before `sdsys` was put in its
group, cannot write that account's files** until SDSYS signs on again. Linux fixes a process's
groups when it starts and `sd` never reloads them, so the session is still without the group even
though `/etc/group` now lists `sdsys`. The save says so (`began before sdsys was put in group`) and
`check.masters` shows `norights ... stale-session`. Sign off and on as SDSYS. This is the only
thing a new account asks of an administrator who has a session open.

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

The first run on a system is the only one that writes a great deal. A run over four small accounts,
session start included, took under a second, and a second run with nothing changed writes nothing.

**`check.masters`** applies the journal and then **compares and reports; it changes nothing.** For
every account (or the one named) it looks at the VOC and at every dictionary the account holds, and
prints a line for each of these, in the form *kind*: *account* *voc or dict* {*file*} {*id*}:

| kind | meaning |
|---|---|
| `differs` | the copy is not the account's record (an edit made outside SD, or a change the journal lost) |
| `missing` | the account has the record and the copy does not |
| `extra` | the copy has a record the account does not have: a dictionary the account no longer holds, a record deleted at the operating system level, or an account that is not registered |
| `nonwritable` | the VOC, or a dictionary, has a directory without group search and write, or a subfile (`%0`, `%1`) without group write. A save of a copy is written as a member of the account's group, so it needs the modes |
| `norights` | the modes are right and **this session** still cannot write the file. The last word says why: `mode` (the owner's permission, for a session that is the owner), `stale-session` (the group lists `sdsys` and this session began before it did: sign on again), `not-a-member` (the group does not list `sdsys`: `sd-elevate sdsys-join`), or `no-write` (anything else: a mount, an ACL) |
| `toolong` | the key (*account*`*`*id*, or with the file) is longer than the system's `MAXIDLEN` less two characters (the state key is two longer), and cannot be copied |
| `unreadable` | the file is there and could not be opened or read through |

When there is a `nonwritable` or `norights` row a line follows that says what they mean. Then the
*stale* and *resync* lines if the flags are up, then "Every master copy matches its account" when
there is no difference, and last **`Checked 5 account(s): 0 difference(s)`**. A listing stops at
2,000 rows. (A `differs` after stage 2 no longer comes from editing a copy: a saved copy is delivered
or refused. It comes from a change made to an account without the journal hearing of it.)

**`list.master.pending`** shows the journal lines that have not been applied and the flags, and
applies nothing. It says "Nothing is waiting in the journal" when there is nothing.

## Who is in the group, and what the files must say

The save needs the `sdsys` user in the account's group **and** the account's files writable by that
group. Both are arranged where an account is made, and repaired where one is brought forward.

**A new user account** gets its group `sdu_`*name* from `create.account`, which makes it with `root`,
`sdsys` and the user as members. If the group was already there (an attached user, an account made
again) and does not list `sdsys`, `create.account` adds it through `sd-elevate sdsys-join`; if that
fails it says so, with the command that repairs it, and still makes the account. A **group account**
is made with `root` and `sdsys` in its group `sdg_`*name* and is owned by `sdsys`, so it needs
nothing. **`delete.account` needs nothing**: the group goes with the account.

**The install and every upgrade** run a walk over the register, before the master files are filled,
which says what it did (the numbers below are an example):

```
Putting the sdsys user in the group of every account, and making each account's VOC and dictionaries writable by that group.
  The sdsys user is put in the group of every account, and the VOC and dictionaries of each account are made writable by that group,
  so that SDSYS can write a master edit into an account's own files.  This gives the sdsys user write access to those files in every account, and to anything else in an account that its group may write.
  sdsys is now in the group sdu_acme (account acme)
  acme: group-write: 3 directories and 6 file(s) changed, 0 already right, 0 skipped
  sdsys put in the group of 1 account(s); it was in 1 already.  Modes made right for 1 account(s); 1 were right already; 1 left as they are (their directory's group is not the account's own, as the shared account's).
```

This is what brings a kept install forward: when the old `sdsys` user is removed its memberships go
with it. For each registered account, **`sdu_`*name* without `sdsys` gets it** (a group account's
group is never asked: it has `sdsys` from the day it is made), and **an account directory directly
below `/home/sd/user_accounts` or `/home/sd/group_accounts` has its VOC and dictionaries made group
writable, but only when the directory's group is the register's own group for the account.** The
shared account is not (its directory belongs to `sdusers`, and its modes are its own); neither is an
account whose directory is somewhere else. A failure is a warning with the command that repairs it;
it does not stop the install, and running the installer again repeats the walk.

**Two `sd-elevate` verbs do the work, each confined**, and neither is more than the walk and
`create.account` need:

| `sd-elevate` | does | refuses |
|---|---|---|
| `sdsys-join sdu_`*name* | puts the user `sdsys`, **and no other user**, in that group (`usermod -aG`: it adds, it never replaces) | any group that is not `sdu_`*user* of an SD user who exists (not `sdusers`, not a route group, not `sdg_`, not `sdu_root`, not `sdu_sdsys`), a group that does not exist |
| `group-write` *account directory* | gives the account's own group write on its VOC and its dictionaries (g+rwx and setgid on the directories, g+rw on the files in them) | an account directory that is not a direct child of `user_accounts` or `group_accounts`, or whose group is not `sdu_`*name* (`sdg_`*name* for a group account): never `sdusers`, which every account is in |

`group-write` changes modes only, never owners or groups. It works on file descriptors opened
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
is added: a group that cannot write the account directory is not given the VOC), only to what the
session itself has just made, and it adds group bits and takes nothing away. The data file next to
a dictionary is not touched. A VOC or dictionary that arrives some other way (`restore.account`, a
copy at the operating system level) keeps the modes it came with: `check.masters` lists any that
are not writable, and the install's upgrade (`sd-elevate group-write`) puts them right.

## Accounts being made, restored and deleted

* **`create.account`** puts `sdsys` in the account's group when it is not (above), and copies the
  new account's VOC and dictionaries as soon as its register record is written. (The VOC is filled
  before the record exists, when the hook cannot yet tell whose it is.)
* **`delete.account`** removes the account's copies, after the register record has gone.
* **`restore.account`** copies the restored account, because a restore replaces its files at the
  operating system level. It does not change their modes; `check.masters` shows any that the
  archive did not keep group-writable.
* **The installer** runs the walk above and then the whole of `sync.masters` on every install, after
  the accounts have been brought forward and before the register is handed to `sdsys`, and prints a
  warning, and goes on, if either did not finish.
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
  at any depth below the account directory.
* **It cannot be shown to work on a machine with one operating-system user.** The sandbox suite shows
  every part but ownership and groups; `witness-masters.sh` (run by the owner as root, on a real
  install) shows the group membership, the modes, root changing only the account's own files, an
  edit reaching a user's VOC at once, and the refusal for a session that began too early.

## Cost

A write to a VOC or a dictionary does the work above; **a write to any other file costs one test of a
flag** (and one more, once per open file, to learn that it is none of the master files). The journal
write is an `open`, a `write` and a `close`: measured in isolation about 5 microseconds on a memory
file system and 12 to 13 microseconds on an ordinary disk. In SD, on a private SD with an ordinary
session, a loop of 2,000 writes to a VOC took a median of 35 ms on the build before the master files,
37 ms on the build before they existed and 41 ms with them (2 to 3 microseconds more for each write,
which is about the size of the difference between two sandboxes on the same machine: the same loop
of writes to a data file took 32 ms on the old build and 24 ms on both runs of the new one). Applying
six thousand journal lines took under a third of a second. **The journal grows with the changes people
make, not with use.** On a private SD, signing on and off, `who`, `list` and `sselect` wrote no VOC or
dictionary record at all; `create.file` wrote two (the pointer and the dictionary's `@id`),
`delete.file` one, a new saved sentence (`.s`) one, and `save.list` one the first time (the
`$savedlists` pointer). The record `$command.stack` is written once, when an account is made; the
command stack itself is saved to a file in the account's `stacks` directory, which is not mirrored.
A save of a copy is a few session starts' worth of work only because it opens four files; it is
not a cost anyone else pays.

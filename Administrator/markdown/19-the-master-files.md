Title: The Master Files
Subtitle: A copy of every account's VOC and dictionary records in the SDSYS account, kept up to date by a journal: what is copied, how, the three verbs, and what it does not do yet.

The SDSYS account holds **a copy of every VOC record and every dictionary record of every
account**. It exists so that SDSYS can look at all of them in one place, and, in the next stage,
change one by editing its copy. **This stage keeps the copies true and nothing more: the account is
the truth, and an edit made to a copy is not delivered to the account.** Only SDSYS sees any of it.

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

## How the copies are kept

**Every write passes one place.** The kernel's hashed-file layer calls the hook after a record of a
VOC or a dictionary has been written, or deleted, or the file cleared; after such a file is made,
removed or renamed (`create.file`, `delete.file`, an `ospath` delete and `osrename`); and
after `oscopy` or `ioscopy` has copied something into one. It does not matter who wrote: a user
program, `ed`, `create.file`, `cd` compiling an I-type, `copy`, an `$internal` verb, or SD itself.
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
| `differs` | the copy is not the account's record (an edit of the copy, or a change the journal lost) |
| `missing` | the account has the record and the copy does not |
| `extra` | the copy has a record the account does not have: a dictionary the account no longer holds, a record deleted at the operating system level, or an account that is not registered |
| `nonwritable` | the VOC, or a dictionary, has a subfile (`%0`, `%1`) without group write permission. The next stage writes an account's files as a member of the account's group, so it needs this |
| `toolong` | the key (*account*`*`*id*, or with the file) is longer than the system's `MAXIDLEN` less two characters (the state key is two longer), and cannot be copied |
| `unreadable` | the file is there and could not be opened or read through |

then the *stale* and *resync* lines if the flags are up, then "Every master copy matches its account"
when there is no difference, and last **`Checked 5 account(s): 0 difference(s)`**. A listing stops at
2,000 rows.

**`list.master.pending`** shows the journal lines that have not been applied and the flags, and
applies nothing. It says "Nothing is waiting in the journal" when there is nothing.

## Accounts being made, restored and deleted

* **`create.account`** copies the new account's VOC and dictionaries as soon as its register record is
written. (The VOC is filled before the record exists, when the hook cannot yet tell whose it is.)
* **`delete.account`** removes the account's copies, after the register record has gone.
* **`restore.account`** copies the restored account, because a restore replaces its files at the
operating system level.
* **The installer** runs the whole of `sync.masters` on every install, after the accounts have been
brought forward and before the register is handed to `sdsys`, and prints a warning, and goes on, if it
did not finish.
* **`update.accounts`**, like every other writer, writes through the hook and needs nothing more.

## What it does not do

* **It does not deliver an edit of a copy to the account.** That is the next stage. Until then an edit
of a copy is shown by `check.masters` as `differs`, and is overwritten the next time the account's
record changes or `sync.masters` runs.
* **It does not see a change made outside SD**: a shell command, a program run by an account that
holds OS.EXECUTE, `sdfix`. `sync.masters` brings the copies up to date, and `check.masters` finds the
difference.
* **A key that does not fit is not copied.** `MAXIDLEN` in `sd.conf` is 63 unless you set it, and a
master file holding a longer id cannot be opened again, so the copy of a VOC record whose
*account*`*`*id* is longer is left out, counted, and reported by `check.masters` as `toolong`.
Raising `MAXIDLEN` (as far as 255) copies them. A dictionary file whose name contains an asterisk is
not copied at all.
* **It finds the dictionaries an account holds** in the top level of its directory (`*.dic`) and
those its VOC names that lie below it. A dictionary kept elsewhere is journalled when it is written
but is not found by a full `sync.masters`.
* **It does not make sdsys a member of any account's group**, and does not change the modes of any
account's files. That is the next stage's.

## Cost

A write to a VOC or a dictionary does the work above; **a write to any other file costs one test of a
flag**. The journal write is an `open`, a `write` and a `close`: measured in isolation about 5
microseconds on a memory file system and 12 to 13 microseconds on an ordinary disk. In SD, on a
private SD with an ordinary session, a loop of 2,000 writes to a VOC took a median of 35 ms on the
build before this stage, 37 ms on the new build before the master files existed, and 41 ms with them
(2 to 3 microseconds more for each write, which is about the size of the difference between two
sandboxes on the same machine: the same loop of writes to a data file took 32 ms on the old build and
24 ms on both runs of the new one). Applying six thousand journal lines took under a third
of a second. **The journal grows with the changes people make, not with use.** On a private SD,
signing on and off, `who`, `list` and `sselect` wrote no VOC or dictionary record at all;
`create.file` wrote two (the pointer and the dictionary's `@id`), `delete.file` one, a new saved
sentence (`.s`) one, and `save.list` one the first time (the `$savedlists` pointer). The record
`$command.stack` is written once, when an account is made; the command stack itself is saved to a
file in the account's `stacks` directory, which is not mirrored.

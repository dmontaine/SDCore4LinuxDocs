Title: Backing Up and Restoring Accounts
Subtitle: Writing accounts to a zip file, putting them back, remembering the backup folder, and recording the system's settings.

This page continues [Account Maintenance](01a-account-maintenance.html).

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
corrected to where it now lives, and programs it had in the global catalog are
cataloged again. **Backups made here restore on SD Core for Windows, and the
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

**A restored account comes back as it was:** each file and directory has the
permissions it was backed up with, except that write for others is dropped and
the owner always keeps read and write, and everything in the account belongs to
its Linux user and its own group (`sdu_<name>`) again. An account that already
exists keeps its Linux user, its password and its groups, **and its own
switches**: the manifest's switches are used only for an account that has to be
created. **Moving an account to another machine** is covered by
[Moving an Account](17-moving-an-account.html).

**What it does not do:**

- It does not back up SDSYS or the system's configuration (`settings.report`,
  below, records that for reference only).
- It carries **no passwords**: an account restored onto a machine that never
  had it asks for a new one, and an account that exists keeps its own.
- It does not follow symbolic links inside an account; any it finds are named
  and left out.
- A program recompiled after it was cataloged globally is not recognized as the
  account's and is not cataloged again.

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

## Backups and restores on one screen: `tool.backups`

```
tool.backups
```

A full-screen page in SDSYS's VOC only (a window of 140 columns by 43 lines or more). The top box
names the saved backup directory, says how many archives it holds, and says **whether anyone else is
signed on**: `backup.account` and `restore.account` both run only when every other session has logged
out, and LOGIN refuses new ones while either runs, so the page lists the other sessions (the same
check the verbs make) and **shows no box for a command while any is there**. The list is the archives
of the directory (the files `SD-host-accounts-yyyymmdd-hhmmss.zip`), newest first: when each was made
(from its name), its size, how many accounts it holds and for which product (from its manifest). The
box at the foot shows the manifest of the one under the cursor, read without unpacking anything:
the product, the SD version, the host and the date, and each account with its files, bytes and
directories.

| Key | Runs |
|---|---|
| `B` | `backup.account all` |
| `A` | `backup.account name ...`, for the account names you type (a-z, 0-9, dot, dash, underscore; up to 20) |
| `R` | `restore.account archive all no.query`, the archive under the cursor |
| `D` | `set.backup.directory path`, for the absolute path you type |

Each shows its command and what it does in a box answered Run or Cancel, **and Cancel is what Enter
chooses**. The page runs those four commands and no other, through the routine all the toolkit pages
use; the verbs ask for the administrator again and write their own audit lines. **A restore replaces
every account the archive holds** with the account of the same name, so its box lists them, from the
manifest, and wants the word `restore` typed (in either case). The verb's own
question (Enter is No) cannot be answered through a page, so the page gives `no.query` after its box
has asked; it does not give it any other way. **A restore that would have to make an account is
refused by the page**: a new user account asks for a password, and that question cannot be answered
through a page, so the page checks that every account the archive holds is registered here already,
and says which are not. Restore such an archive at the prompt.

The packing of a backup and the placing of a restored account are done through the root helper
(`sd-elevate backup-pack`, `restore-place`); where they cannot be done, the verb says why and the page
shows its last line on the status line. `F5` reads the directory, the archives and the sessions again,
`F1` explains the page and `Ctrl-Q` leaves. Opening the page writes the audit line
`tool start app=tool.backups`.

## Recording the settings: `settings.report`

```
settings.report {directory}
```

Writes, or shows, a **plain-text record** of the system's settings — `sd.conf`,
ssh and API access, the accounts — for an administrator to keep. It is for
reference only: nothing reads it back. **It never contains a password or a
private key.** The API's certificate appears as its subject, dates and
fingerprint, or as *certificate: not yet generated* until the API has had its
first TLS connection. It also lists the entries of the global catalog that are
not SD's own, which a backup of an account carries only for the programs whose
object file is in that account.

## Who has these verbs

**All of them are SDSYS's** — `create.account`, `modify.account`,
`modify.password` for another account, `delete.account`, `clean.account`,
`update.accounts`, `config`, `backup.account`, `restore.account`,
`set.backup.directory`, `settings.report`. An ordinary account has none of these names at
all — this is not a permission it lacks, the verbs are simply not in its
VOC. **Who may enter an account is changed in one place**, `modify.account`
*name* `add` / `delete`; see [Accounts and Security: The Home Screen, ssh Keys and Passwords](01-accounts-and-security-8-home-screen-ssh-keys-passwords.html).

## See also

[Sessions and Locks](02-sessions-and-locks.html) ·
[Operating System Access](03-operating-system-access.html).

**In the user documentation**, which does not repeat any of this: *SD TCL - The
Command Processor* for how a verb is dispatched and what a VOC record holds, and
*SD Basic - System and Environment* for what a program can read about its own
session. Those pages are in a different set and are deliberately not linked from
here — see the note at the top.

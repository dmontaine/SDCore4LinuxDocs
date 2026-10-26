Title: Installation and the daemon
Subtitle: What the installer puts on the machine, what an upgrade replaces, and how the daemon behaves.

This page covers the parts of installation an administrator has to live with
afterwards: the groups and permissions the installer creates, the daemon, and
what an upgrade does and does not touch.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

The installer itself — the prompts and their defaults — is covered in the
GettingStarted set, under *Installing SD Core*, and is not repeated here.

## Two things to know before the first install

**SD cannot be installed unattended.** `installsdcore.sh` asks for
confirmation, two yes/no questions about remote access (and, on a first
install, a third: whether to open every access gate for the installing user's
own account, default no), and ends by setting three passwords at the terminal —
there is no flag to skip any of it.

The reason for the passwords is the same one Windows has: an account
without one cannot be used through the API at all, and the closing summary
would otherwise finish silently with a gap nobody noticed.

**The installer refuses to start if SD is already installed.**
`/usr/local/sdsys/bin/sd` existing is the test; uninstall with
`deletesdcore.sh` first. It also refuses if run as root, or if the calling
user cannot `sudo` at all — both checked before anything on the machine
changes.

**Unlike SD Core for Windows, this installer does not refuse to run
because of a pre-existing ssh server.** `openssh-server` is installed as
an ordinary package regardless, and the ssh boundary (below) is applied to
whatever `sshd_config` it finds, non-fatally: a customised configuration
gets a warning and the command to apply the boundary by hand, not a
refusal to install at all.

## What lands where

| What | Where |
|---|---|
| Binaries | `/usr/local/bin` |
| The client library, for applications | alongside the server, under `/usr/local/sdsys/bin` |
| The elevation helper and ssh boundary script | `/usr/local/sbin` |
| Configuration | `/etc/sd.conf` |
| The SDSYS account | `/usr/local/sdsys` |
| The SD BASIC guide and the knowledge pack for AI agents (text only) | `/usr/local/sdsys/agent-pack/guide` and `/usr/local/sdsys/agent-pack/pack` — see [Giving an AI Agent an Account](18-the-agent-account.html) |
| User accounts | `/home/sd/user_accounts` |
| Group accounts | `/home/sd/group_accounts` |

Neither root can be changed. The installer does not ask.

## What the installer creates

| | |
|---|---|
| `sdusers` group | the Linux group every SD account belongs to |
| `sdsys` user | the one administrator account — a real Linux user, its own home, shell and password |
| `sdu_<name>` | one supplementary group per user account, created by `create.account` with `root` and the user in it; **the `sdsys` user is a member of none of them as delivered**. `modify.account` *name* `sdsys-on` puts it in one, so that SDSYS can change that account by saving its master record — which gives the `sdsys` user write access to everything the group may write (see [The master files](19-the-master-files.html)); `sdsys-off` takes it out. An install that finds it in the groups of accounts it keeps asks once whether to keep it there (the answer when nothing can be read is no) |
| `sd.service`, `sdclient.socket` | the `systemd` units, enabled at boot |
| `sd-lnxd.service` | the unit that runs the daemon `sdlnxd` and starts it again if it fails; `sd.service` wants it, so there is nothing to enable (see [The audit trail](#the-daemon-is-restarted-if-it-dies) below) |
| the ssh boundary | a fenced block in `/etc/ssh/sshd_config` — see [Remote access and the machine](05-remote-access-and-the-machine.html) |

Group membership takes effect at the next login, the same as any Linux
service account. An administrator added to `sdusers` while already logged
in does not have it until they log out and back in, and until then cannot
read the data tree at all. The symptom looks like a broken install and is
not one.

## File modes SD relies on, and checks

SD trusts a program in its **global catalogue** (`/usr/local/sdsys/gcat`) to run as part of the system, because only `sdsys` can write there. **The kernel
therefore refuses to load a global catalogue object that other users, or the group `sdusers`, can write**, and stops with
`<name> in the global catalogue can be written by other users, so it was not loaded (chmod go-w it)`. The installer leaves every file in `gcat` mode 0755
after its last compile, so an installation never meets the check. If you see the message, someone changed a mode: `chmod go-w` the file named, and look for
why. **A fresh install made before this change left `gcat/$cproc` mode 0664 group `sdusers`; install again, or run `chmod go-w` on it by hand.**

`/home/sd`, `/home/sd/user_accounts` and `/home/sd/group_accounts` are mode 755, owner `sdsys`, group `sdusers`. They used to be 775: every SD user is in `sdusers`, so any of
them could rename another account's directory and make one of their own under the same name, and the account's owner would then sign on to a VOC the other person wrote. Nothing
needs the group's write here (SD makes an account directory in the `sdsys` session, which owns the parent, and the helper that runs as root does the rest). The installer sets
the modes every time it runs, so installing again fixes an installation made before this change; to do it by hand,
`sudo chmod 755 /home/sd /home/sd/user_accounts /home/sd/group_accounts`. The account directories themselves keep their own owner, group and setgid bit.

**The audit trail** (`/usr/local/sdsys/audit`) is mode 0600, owner `sdsys`, group `sdusers`, **and append-only** (`chattr +a`): the group cannot read it, write it or open it. (It was 0620 until 1.2-0, because
every session runs as its user and so had to append to the file itself; that also let a member of `sdusers` add a line of their own that claimed any user.) **Now a session sends each record to the root daemon
`sdlnxd`** over the Unix socket `/run/sd/audit.sock` (mode 0660, group `sdusers`, in a directory only root can write), and **the daemon writes the line**. The `user=` and the `pid=` on the line are the ones the
kernel reports for the sending process, not anything in the record's text, so no one can make a line that names someone else; the text of a record comes after them, and the `uid=` is the SD user number the
sender gave, which the daemon cannot check. `sudo=` is the user the kernel logged in, which survives `su` and `sudo`. A record is cut at 1900 bytes, its control characters become `?`, and one record is one line.
Read the file with `sudo`; `sudo lsattr /usr/local/sdsys/audit` shows the `a` the installer sets and checks (`WARNING: could not make ... append-only` when a filesystem will not take it).

**If the daemon is not running** (stopped by hand, or in the few seconds before it is started again after a crash; see below) a session appends to the file itself, which works for `sdsys` and root, who own it, and fails for everyone
else: the record is then in the system journal only. **So every record is also sent to the system journal** (identifier `sd_Log`, facility `authpriv`, prefix `sd-audit `), whose daemon stamps the real uid and pid
of the process that sent it, whatever the text says. To check a line, find its copy: `sudo journalctl -t sd_Log -o verbose | grep -B8 'the line'` shows `_UID` and `_PID`. The journal must be kept on disk for this to
survive a reboot (`/var/log/journal` present, or `Storage=persistent` in `journald.conf`), and whoever reads it must be root or in `adm` or `systemd-journal`.

**One user cannot flood the trail.** The daemon takes at most 600 records from one operating-system user in any 60 seconds (counted from the user the kernel reports, not from anything in the text). The rest are dropped,
and when that user's 60 seconds are over the daemon writes **one line** in the trail, `audit rate limit dropped=N taken=600 limit=600 window=60`, with that user's name and the pid of the last sender; it writes the
line at once if the daemon is stopped inside the window. A dropped record still has its copy in the journal, because a session sends that whether or not the daemon took the record. The error log says how many records
the bound dropped (`N over the rate bound`) each time the daemon reports. 600 a minute is far more than SD writes in ordinary use; the figure is fixed when SD is built (`AUDIT_RATE_MAX` and `AUDIT_RATE_WINDOW` in `sddefs.h`),
not a setting.

**The daemon rotates the file.** When the trail has reached 1 MB (`AUDIT_ROTATE_BYTES`) the daemon renames it to `audit.<date>-<time>` and starts a new one, as it writes, with no restart of SD: the new file has the old
one's owner, mode and append-only flag, and the old one keeps the flag. The same code runs when SD starts (that is how a machine whose daemon is not running still rotates). If the flag will not lift, nothing is
renamed, the trail stays whole and keeps growing, the error log says `N rotation(s) failed`, and the daemon tries again a minute later. SD deletes nothing; pruning the old files is yours, and starts with `chattr -a`.

### The daemon is restarted if it dies

`sdlnxd` is run by its own `systemd` unit, `sd-lnxd.service`, and `systemd` starts it again two seconds after it **fails** (`Restart=on-failure`): `kill -9`, a crash or the out-of-memory killer. While it is down the
audit records of ordinary users are in the journal only (see above) and lost sessions are not cleared down (the daemon scans for them every `CLEANUP` seconds, 300 by default); the new daemon takes up both at once.
`sd.service` starts SD with `sd -start -nodaemon`, which does not fork a daemon of its own, and wants `sd-lnxd.service`; stopping `sd.service` stops the daemon with it (`BindsTo=`).
Things to know:

- **A stop is not a failure.** `sd -stop` ends the daemon with SIGTERM and it exits with status 0, so it is **not** started again. After an `sd -stop` by hand `systemctl restart sd.service` brings SD and the daemon back (or `systemctl start sd-lnxd` for the daemon alone while SD is running).
- **A daemon that keeps failing is given up on.** Five starts in a minute and the unit is `failed`; `journalctl -u sd-lnxd` says why, and `sudo systemctl reset-failed sd-lnxd; sudo systemctl start sd-lnxd` starts it again once that is mended.
- **One daemon at a time.** A second `sdlnxd` (started by hand, or by a plain `sd -start`) finds the first named in the shared segment and ends at once with status 0, saying so in the error log.
- **`sd -restart` and a plain `sd -start`** still fork a daemon of their own, outside systemd, so nothing watches it. Use `systemctl restart sd.service`.
- An installation made before this change has the new units after SD is deleted (keeping the accounts and the configuration) and installed again, as for any upgrade. If the old `sd.service` was left behind by a delete, the installer replaces it, and adds `sd-lnxd.service`, when it does not mention the new unit.

The error log (`errlog`) is mode 664,
owner `sdsys`, group `sdusers` (it was 775): every session appends to it, and nothing runs it.

SD's shared memory segment and its semaphores are made mode 0660 and belong to the group `sdusers`, so only SD users can attach them. An installation that
was started before this change keeps its old, wider modes until SD is stopped and started again. `ipcs -m` shows the mode of the segment.

**A member of `sdusers` who has an operating-system shell can still write the segment**, because every SD user is in that group. So nothing a session *decides on* is read
from it any more. A session takes these from places only SDSYS or root can write:

| What | Where a session gets it now | It used to come from |
|---|---|---|
| the system directory (global catalogue, register, messages, audit trail, errlog) | `SDSYS=` in `sd.conf` | the segment |
| the p-code every session runs | `bin/pcode`, read by the session itself; a copy that others or `sdusers` can write is refused | the segment |
| the per-session settings (`SH`, `SPOOLER`, `USRDIR`, `GRPDIR`, `DUMPDIR`, `TEMPDIR` ...) | `sd.conf`, read by the session when it starts | a template in the segment |
| the session's own administrator, `sh`, `os.execute` and `sd.accounts` bits and its gates | memory only that process can change | its entry in the segment |

Two things follow. **`sd.conf` is read by every new session**, so an edit to one of the per-session settings reaches the sessions started after it, without a restart;
the parameters that size or configure the segment still need one. And **a bad line in `sd.conf` stops a new session starting**, with the message `sd -start`
gives, until the line is repaired. It does not stop SD or the sessions already running. If the segment's copy of the system directory differs from the
file's, the file is used and one line goes to the system log.

**What this does not close.** The lock table, the file table and the user table are still in the shared segment and still writable by an SD user with a
shell: such a person can release other people's locks, log other sessions out or fill the user table. That is damage and denial of service, not a way to a
privilege. The gates are walls for an SD *session*; a person with a shell is trusted with the segment. Giving SD users no login shell, or only the
forced-command ssh route, is how an installation that cannot accept that closes it.

**The file `$ipc`.** `$ipc`, in the system directory, is the one SD file every user's process has to write (it is `sdsys:sdusers` 0775), so a member of `sdusers`
with a shell can write it as well. It holds working records and nothing a session is configured from: the lock that orders a phantom's start-up, the start-up
records of a phantom (its command, the option flags it inherits, its `DATA` queue and its log file name), the messages waiting for a user, the phantom register
that `status` shows, and the tables that `profiler`, `hsm` and `pstat` ask another session for. A phantom no longer takes its command, options, `DATA` lines or
log file from it on trust. `phantom` seals the records with a secret that it makes for each phantom and gives only to the new process, in its environment, where
only the same operating-system user (and root) can read it, and which the new process copies and overwrites at once. The phantom runs, stacks and sets nothing unless the seal on
what it read checks; if it does not, the phantom ends at once, says so in its `como` log and to its parent, and writes `phantom refused` to the audit trail.
SD does not run, stack or set anything from the other records (messages, the register and the profiler, `hsm` and `pstat` tables); they are only shown, and a
message is shown as it was written. The conversation of the phantom debugger (`pdebug`) is still carried in `$ipc` and is trusted as the segment above is.
The secret is kept in no file and not in the segment. That another operating-system user cannot read the environment of this user's processes is the
operating system's rule; it has been tested here with one user only.

### The files root runs

`sd.service` runs `bin/sd` as root (`sd -start` and `sd -stop`), `sd-lnxd.service` runs `bin/sdlnxd` as root, `sdclient@.service` (the first stage of every API connection)
runs `bin/sd -n -q` as root, `sd-elevate akpath-set` runs `bin/sdidx` as root, and every session - that first stage included - reads `bin/pcode`. **A file that root runs
must not be one that the `sdsys` login can replace.** Until 1.2-0 the installer's `chown -R sdsys:sdusers` left all of them `sdsys`'s, so whoever held that login could
change one and have root run it at the next start. **Near its end the installer now makes `/usr/local/sdsys/bin` and every file in it `root:root`, with no group or other
write, and makes the directory itself immutable** (`chattr +i`).

| | owner, mode |
|---|---|
| `bin/sd`, `bin/sdlnxd`, `bin/sdidx` | `root:root` 755 |
| `bin/pcode`, `bin/pcode.old` | `root:root`, readable by everyone, writable by root only |
| `bin/sdfix`, `bin/sdconv`, `bin/sdtic`, `bin/sdclilib.so`, `bin/libsdcli.so` | `root:root` 755 (no unit runs them; they are in the same directory, and an administrator may run `sdfix` with `sudo`) |
| `bin` itself | `root:root` 755, immutable |
| `.sdcore-install`, `/usr/local/sbin/sd-elevate`, `sd-accarchive`, `sd-reconcile-accounts` | root's, as before |
| everything else in `/usr/local/sdsys` | `sdsys:sdusers`, as before (the register, the global catalogue, `voc`, `bp`, the SDSYS account's files) |

**Why the attribute.** The `sdsys` user owns `/usr/local/sdsys`, and the owner of a directory may rename any entry in it, whoever owns the entry. With the files root's
and nothing more, `sdsys` could move `bin` out of the way and make a `bin` of its own, which `systemd` would run at the next start. The attribute stops that rename, and any new
or removed entry in `bin`; only root can lift it. `lsattr -d /usr/local/sdsys/bin` shows an `i` when it holds. **If the file system does not keep the attribute** (the installer
prints `WARNING: the root-run files were NOT all sealed`, says the directory `could not be made immutable`, and repeats a warning in its closing summary), the files are still root's, but `sdsys` can rename `bin` and put its own in its place, and nothing else closes that.

What this changes for you:

- **To put a new file into `bin`** (a hand-built `sd`, say): `sudo chattr -i /usr/local/sdsys/bin`, copy it in as root, then `sudo chattr +i /usr/local/sdsys/bin`.
  Writing into a file that is already there with `cp` needs root and no change of the attribute; replacing it with `install` or `mv`, which make a new entry in the
  directory, needs the attribute lifted. So do SD's own writes of `bin/pcode` when `SAFEDIR` is set in `sd.conf` (it is off as delivered), because they write a new file and
  rename it.
- **The two things that write `bin/pcode`** - `catalog ... pcode` and compiling a `recursive` program under `sd -internal` - are SD's own developers' tools. As the code
  reads, they are root's from now on, and the second makes `bin/pcode.old` when it is not there yet, which needs the attribute lifted; the `sdsys` login does neither.
  The installer's own passes ran as root and finished before this step. (The statement about these two tools is read from the source; the rest of this section was
  measured on a Debian 13 install on 26 October 2026: `bin` and its files `root:root`, the `i` in `lsattr -d`, the `sdsys` login unable to write, make or rename an entry in
  `bin` or to rename `bin` itself, SD and the audit daemon started from it and the daemon started again by `systemd` after a `kill -9`, and the `SDSYS` account still able to
  compile, catalogue locally and globally, run a program and run `update.accounts all`.)
- **`deletesdcore.sh`** lifts the attribute before it removes the directory, so a delete (with or without keeping the accounts) works as before.

**What this does not close.** The global catalogue and the sudo helper `sd-elevate` are still routes from a stolen `sdsys` login to root-run or every-account code (see
[The master files](19-the-master-files.html)); data that root reads but does not run (`terminfo`, `messages`) is still `sdsys`'s; and during the minutes of an install,
before this step, `bin` is still `sdsys`'s - install while nobody holds that login (a first install has no such login yet).

## The daemon

| | |
|---|---|
| Unit | `sd.service` (the daemon), `sdclient.socket` (the API listener) |
| Start type | enabled — `systemd` starts both at every boot |
| Starting | `systemctl start sd.service`, or `sd -start` |
| Stopping | `systemctl stop sd.service sdclient.socket`, or `sd -stop` |
| Created by | the installer |
| Removed by | the uninstaller |

**Stopping the daemon ends every session on the machine**, without asking. It
signals every entry in the user table and has no "are users logged in" check,
so treat it as a machine-wide action rather than an administrative
convenience.

**Start it the way you stopped it.** `sd.service` is a one-shot unit that stays
"active" after it has started SD, and `sd -stop` does not tell it that SD has
gone: after `sd -stop` the unit still reads active, `systemctl start
sd.service` does nothing and `sd` answers "SD has not been started". Use
`sd -start` after `sd -stop`, or `systemctl restart sd.service`, which goes
through the unit and puts the unit and the daemon back in step. The installer
itself ends with such a restart for the same reason.

### After an unclean shutdown

SD's shared state is a System V IPC segment (`shmget`), which **does not
survive a reboot** — a real difference from SD Core for Windows, where the
equivalent segment does and needed its own discard-and-restart logic. A
crash the machine itself rebooted from always leaves a clean slate here.
What can still happen is the daemon dying while the box stays up (killed,
or `sd.service` restarted); `sd -start` checks the actual process, not
merely the segment's presence, and says so rather than reporting a false
success — see *Running SD* in the Getting Started set.

## Upgrading

Uninstalling with the database kept, then installing again, replaces the
shipped files and preserves everything the site owns.

| Replaced | Preserved |
|---|---|
| the catalogue and compiled programs | your accounts and their passwords |
| the BASIC source | the private catalogue |
| the messages and include records | your print queue and held reports |
| the VOC templates and library routines | everything under your own accounts, and `sd.conf` |
| terminfo, the licence, the contributor list | |

**An upgrade asks nothing** at the two remote-access prompts — no tasks
page is shown, on the principle that the machine already carries the
answers and every setting has a verb that changes it afterwards
(`remote.ssh`, `remote.api` — see *Remote access and the machine*).

### As in SD Core for Windows, the installer refreshes every account's VOC

**When you kept your accounts, the installer runs `update.accounts all`**
as the administrator near its end, announcing it with "Bringing every
registered account's VOC up to this release." A command the release adds
can then be typed in every account that already existed. If `newvoc`
changes the type of a record an account already has, it asks about that
record account by account, so stay at the keyboard until it finishes. See
*Upgrading and uninstalling* in the Getting Started set.

**The dictionaries are reapplied automatically.** The definitions the
release ships are added and updated by the install step that writes them
(`write_install_dicts`), and any you added are left alone. If that step
cannot run, the installer says so rather than finishing quietly.

Neither step can take anything away. `update.accounts` only ever adds
records, so an account created before a verb was withdrawn keeps it.

### An upgrade keeps what accounts could do: `sh` and `OS.EXECUTE`

**An account made before the per-account switches existed has always been
able to use `sh` and `OS.EXECUTE`, so the installer gives it both once.**
In the same step it runs `upgrade_gates` as the administrator, and every
user account whose `sh` or `OS.EXECUTE` setting is still blank gets that
setting switched on (ssh and the API are left exactly as they were). A
blank means the account was made before the switches existed; every account
made since holds an explicit `yes` or `no`. Nobody loses a command they were
using; SDSYS can then take either away one account at a time with
`modify.account` *name* `sh-off` / `os-off`, and **a later install does not
give them back**: the step changes only a blank setting, never a `no`
(neither the delivered default nor an administrator's `sh-off`), so it stays
safe even when an upgrade that keeps the accounts removes the marker the
step leaves. Group and `other` accounts are not touched, and accounts
created after the upgrade start with every switch off.
**A fresh install is not an upgrade**: the account it makes for whoever
installed SD starts with ssh, the API, `sh` and `OS.EXECUTE` all off, like
any other new account, and the installer prints the `modify.account`
commands that turn them on (as `sdsys`).

### An upgrade puts a group account's record files back in its group

**A group account made before 19 October 2026 has four files in the wrong
group, and an upgrade that keeps the accounts corrects them.** `create.account
group` used to leave `voc/%0`, `voc/%1`, `$hold.dic/%0` and `$hold.dic/%1`
in the group `sdusers`, which every SD user belongs to. They are the two
parts of the account's VOC and of the dictionary of its print-hold file, so
any SD user could write them from outside SD. The installer now asks
`sd-elevate` to give each of the four to the group of the account's own
directory (owner `sdsys`, group `sdg_`*name*, mode unchanged at 664), for
every group account **except `shared`**, whose group is `sdusers` by design.

The step prints each file it changes and a count. It changes only a file that
is not already right, so **a later install does nothing**. It leaves alone, and
reports in a warning, an account whose directory is not in an `sdg_` group, and
any path that is or sits behind a symbolic link (a member of the group can write
in the account's directory, and the installer runs as root, so it never follows
one). If `sd-elevate` refuses a file, for example one with a second hard link,
that file is named in a warning and the install goes on; the warning says the
command that gives it its group by hand:

```sh
sudo /usr/local/sbin/sd-elevate chown-account sdsys sdg_name /home/sd/group_accounts/name/voc/%0
```

A fresh install has only `shared`, so it has nothing to do here, and a group
account made after the fix is made right in the first place.

## Uninstalling

```sh
./deletesdcore.sh
```

**The default does not touch your accounts or your configuration.**
Removing the database needs an explicit `DELETE` confirmation beyond the
initial keep/discard prompt — see *Upgrading and uninstalling* in the
Getting Started set.

**The uninstaller does not remove the `openssh-server` package.** It may
predate SD or be in use for something else. It does remove the ssh
boundary block it wrote, leaving the rest of `sshd_config` as it was.

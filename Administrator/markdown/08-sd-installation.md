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
| `sdu_<name>` | one supplementary group per account, created by `create.account`; **the `sdsys` user is a member of every one**, and every account's VOC and dictionaries can be written by that group, so that SDSYS can change an account by saving its master record — this gives the `sdsys` user write access to those files in every account (see [The master files](19-the-master-files.html)). The install puts `sdsys` back in the groups of accounts it keeps |
| `sd.service`, `sdclient.socket` | the `systemd` units, enabled at boot |
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

**The audit trail** (`/usr/local/sdsys/audit`) is mode 0620, owner `sdsys`, group `sdusers`, **and append-only** (`chattr +a`). Every SD user's session runs as that user, so the group must be able
to write; the attribute turns that write into an append, so no one but root can empty, rewrite, rename or delete the file, and the group cannot read it (read it with `sudo`).
`sudo lsattr /usr/local/sdsys/audit` shows an `a`; the installer sets it, checks it and says `WARNING: could not make ... append-only` when a filesystem will not take it. **What this does not
prevent:** a person with a shell who is in `sdusers` can still *add* a line of their own, so a line in the trail shows what was written, not that SD wrote it; the lines SD writes carry the
user, the uid and the pid, and a forged line can claim any of them. **So every record is also sent to the system journal** (identifier `sd_Log`, facility `authpriv`, prefix `sd-audit `), whose daemon
stamps the real uid and pid of the process that sent it; the sender cannot choose those two. To check a line, find its copy: `sudo journalctl -t sd_Log -o verbose | grep -B8 'the line'` shows `_UID` and `_PID`, and
a line in the trail with no copy from that uid and pid is suspect. The journal must be kept on disk for this to survive a reboot (`/var/log/journal` present, or `Storage=persistent` in `journald.conf`), and whoever reads it
must be root or in `adm` or `systemd-journal`. A writer that is not the user, which would make the trail itself trustworthy, is a further step. The error log (`errlog`) is mode 664,
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

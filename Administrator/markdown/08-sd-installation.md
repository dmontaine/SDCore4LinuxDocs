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
user account that exists then has `sh-on` and `os-on` set (ssh and the API
are left exactly as they were). Nobody loses a command they were using;
SDSYS can then take either away one account at a time with `modify.account`
*name* `sh-off` / `os-off`, and **a later install does not give them back**
— the step runs once and leaves a marker. Group and `other` accounts are not
touched, and accounts created after the upgrade start with every switch off.
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

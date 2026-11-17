Title: Installation: The Daemon, Upgrading and Uninstalling
Subtitle: The daemon, upgrading and uninstalling.

This page continues [Installation: File Modes and the Files Root
Runs](08a-sd-installation-file-modes-and-root-files.html).

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
convenience. A session waiting at its prompt does not leave on that signal, so
ten seconds later `sd -stop` (and `sd -restart`) ends every process still
attached to SD with SIGKILL and says how many it ended, for example
`1 process(es) still attached after ten seconds were ended with SIGKILL`; each
is also written to syslog. Nothing that is not attached to SD's shared memory is
touched. A session ended this way does not run its own logout. If a session
does find SD gone under it, it ends at once with
`SD process N ended: its semaphores were removed ...` in syslog and on its
terminal.

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
| the catalog and compiled programs | your accounts and their passwords |
| the BASIC source | the private catalog |
| the messages and include records | your print queue and held reports |
| the VOC templates and library routines | everything under your own accounts, and `sd.conf` |
| terminfo, the license, the contributor list | |

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

**A group account made by an earlier version has four files in the wrong
group, and an upgrade that keeps the accounts corrects them.** An earlier
`create.account group` left `voc/%0`, `voc/%1`, `$hold.dic/%0` and `$hold.dic/%1`
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

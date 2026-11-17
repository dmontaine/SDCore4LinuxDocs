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
confirmation, two yes/no questions about remote access, one (default No, only
for a new account) about opening every access gate on the installing user's
own account, and ends by setting
three passwords at the terminal —
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
whatever `sshd_config` it finds, non-fatally: a customized configuration
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
| `sdsshnokey` group | the Linux users SD makes are put in it, and the ssh server's SD block offers its members no key sign-in; `modify.account` *name* `ssh-key-on` takes one out (see [Accounts and Security](01-accounts-and-security-8-home-screen-ssh-keys-passwords.html)). Empty as installed; SD never deletes it |
| `sdsys` user | the one administrator account — a real Linux user, its own home, shell and password |
| `sdu_<name>` | one supplementary group per user account, created by `create.account` with `root` and the user in it; **the `sdsys` user is a member of every one of them as delivered** (`create.account` puts it in a new account's group, the install in the groups of the accounts already there, once), which gives the `sdsys` user write access to everything the group may write (see [The master files](19-the-master-files.html)). `modify.account` *name* `sdsys-off` takes it out of one account's group and `sdsys-on` puts it back |
| `sd.service`, `sdclient.socket` | the `systemd` units, enabled at boot |
| `sd-lnxd.service` | the unit that runs the daemon `sdlnxd` and starts it again if it fails; `sd.service` wants it, so there is nothing to enable (see [The audit trail](08a-sd-installation-file-modes-and-root-files.html#the-daemon-is-restarted-if-it-dies) below) |
| the ssh boundary | a fenced block in `/etc/ssh/sshd_config` — see [Remote access and the machine](05-remote-access-and-the-machine.html) |

Group membership takes effect at the next login, the same as any Linux
service account. An administrator added to `sdusers` while already logged
in does not have it until they log out and back in, and until then cannot
read the data tree at all. The symptom looks like a broken install and is
not one.

## File modes SD relies on, and checks

SD trusts a program in its **global catalog** (`/usr/local/sdsys/gcat`) to run as part of the system, because only `sdsys` can write there. **The kernel
therefore refuses to load a global catalog object that other users, or the group `sdusers`, can write**, and stops with
`<name> in the global catalog can be written by other users, so it was not loaded (chmod go-w it)`. The installer leaves every file in `gcat` mode 0755
after its last compile, so an installation never meets the check. If you see the message, someone changed a mode: `chmod go-w` the file named, and look for
why. **A fresh install made before this change left `gcat/$cproc` mode 0664 group `sdusers`; install again, or run `chmod go-w` on it by hand.**

`/home/sd`, `/home/sd/user_accounts` and `/home/sd/group_accounts` are mode 755, owner `sdsys`, group `sdusers`. They used to be 775: every SD user is in `sdusers`, so any of
them could rename another account's directory and make one of their own under the same name, and the account's owner would then sign on to a VOC the other person wrote. Nothing
needs the group's write here (SD makes an account directory in the `sdsys` session, which owns the parent, and the helper that runs as root does the rest). The installer sets
the modes every time it runs, so installing again fixes an installation made before this change; to do it by hand,
`sudo chmod 755 /home/sd /home/sd/user_accounts /home/sd/group_accounts`. The account directories themselves keep their own owner, group and setgid bit.

**The audit trail** (`/usr/local/sdsys/audit`) is mode 0600, owner `sdsys`, group `sdusers`, **and append-only** (`chattr +a`): the group cannot read it, write it or open it. (It was 0620 until 2.0-0, because
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

## Continued in

[Installation: File Modes and the Files Root
Runs](08a-sd-installation-file-modes-and-root-files.html) — the restart of the
daemon and the files root runs.

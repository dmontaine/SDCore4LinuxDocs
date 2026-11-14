Title: Installing SD Core
Subtitle: What the installer does to the machine, and the choices it puts in front of you.

There is a compiler to run. `installsdcore.sh` clones the source from
`github.com/dmontaine/SDCore4Linux` and builds it on your machine — there is
no prebuilt package and no installer binary. A clone builds; that is why
installing means building.

This is a real difference from SD Core for Windows, which ships as a single
installer carrying its own compiled runtime. Windows has one target and one
ABI; this port supports Debian and Ubuntu (and their derivatives), detected
from `/etc/os-release`. Any other distribution — Fedora, RHEL and RHEL's
clones, Arch, openSUSE, or a machine with no `/etc/os-release` — is refused
before the installer changes anything. It builds from source so that changes elsewhere in the
system — library versions, kernel, `libssl` — are accounted for at build
time rather than papered over by a bundled runtime.

## Before you start

**Run it as yourself, not as root and not with `sudo`.** The script refuses
outright if `$EUID` is 0 — building as root would leave build artefacts
root-owned, and the script needs to know who "the installing user" is to
create your own SD account. It asks for your `sudo` password itself, at the
one point where it is needed, and checks up front that you can `sudo` at
all: a caller who cannot is refused in words, before anything changes,
rather than partway through with `sudo`'s own error.

**SD cannot be installed silently.** This is deliberate, not a missing
feature. The script asks two questions whose answers cannot be defaulted
safely — whether to open ssh and the API to other computers — and ends by
setting three passwords at the terminal.

**The installer does not ask where to put SD.** The roots are fixed. See
[What lands where](#what-lands-where).

**It refuses to start, and changes nothing, if SD is already installed** —
`/usr/local/sdsys/bin/sd` existing is the test. Uninstall first (see
[Upgrading and uninstalling](01a-upgrading-and-uninstalling.html)).

## Getting the installer

**The command that starts SD Core is `sd`, and `sd` is its only name.** SD Core
for Linux Solo, if you install it as well, is started by `sd-solo`; the two have
separate API ports (4247 and 4249) and separate shared-memory keys, so they can
share a computer. The installer is `installsdcore.sh` and the uninstaller
`deletesdcore.sh` (Solo's are `installsdsolo.sh` and `deletesdsolo.sh`).

Clone the repository, or fetch `installsdcore.sh` on its own — the script
itself clones the source it actually builds from, so having the whole
repository first is a convenience, not a requirement:

```sh
git clone https://github.com/dmontaine/SDCore4Linux
cd SDCore4Linux
chmod +x installsdcore.sh
./installsdcore.sh
```

The script downloads its own working copy of the source to
`~/.sdb64tmp`, builds from there, and deletes it when the install
finishes — it does not use the clone you ran it from as the build tree.

**From a USB stick.** A release zip can be unzipped on a USB stick and the
installer run from there. Use `bash`: a stick formatted FAT, exFAT or NTFS has
no execute permission, so `./installsdcore.sh` can fail on it.

```sh
bash /media/<you>/<stick>/installsdcore.sh
```

The zip carries the installer, the documentation and SD's complete source (its
`source` folder), and SD is built from that. The installer still downloads the
build packages, so the computer must be online. It checks first, before it asks
anything or changes anything, and stops with a message if it is not. It writes
nothing to the stick.

**The source is distributed with the installer and is not installed.** The
BASIC programs and the C source are compiled during the install and are not left
on the computer: `/usr/local/sdsys` holds the compiled system. To read or change
the source, use the `source` folder of the release zip or the repository.

## What you are asked

After confirming you want to continue, two questions about remote access,
both defaulting to **no**:

```
Allow ssh access from other computers? enables sshd at boot, opens port 22 (y/N)
Allow API access from other computers? opens TCP port 4247 (y/N)
```

**Answering "no" to both is a real, supported deployment**, not a degraded
one — it gives a working SD reachable only at this machine's own keyboard,
over `ssh localhost`, or by a local API client. Both settings have a verb
that changes them later (`remote.ssh`, `remote.api` — see the Administrator
set's *Remote access and the machine*), so nothing here is a one-time
choice.

**An upgrade does not ask them.** When the uninstaller kept the configuration
(its *Keep your existing configuration?* answered yes), the installer asks
neither question and keeps access as it was: ssh is left exactly as the
machine has it, and the API stays open to other computers if it was open, and
local if it was local. An install after the configuration was deleted asks
both again; that uninstall also removes the listener setting `remote.api`
wrote.

**Neither question is about whether an ssh server or an API listener
exist.** They always do — `openssh-server` is installed as an ordinary
package regardless of the answer, and SD's API socket is always defined
(`sdclient.socket`, activated by `systemd` independently of whether `sd`
itself is running). What the two questions actually decide:

| Question | "no" (default) | "yes" |
|---|---|---|
| ssh | `sshd` is left however the box already had it; the SD boundary (below) is written to `sshd_config` regardless, ready for whenever ssh is turned on | `sshd` is enabled at boot and `ufw allow 22/tcp` is added |
| API | `sdclient.socket` listens on `127.0.0.1:4247` only — a remote client reaches it by tunnelling over ssh (`ssh -L 4247:127.0.0.1:4247 <host>`) | the socket is rebound to `0.0.0.0:4247` and `ufw allow 4247/tcp` is added |

**SDSYS over ssh is not asked about: it is installed shut.** It is an
available feature that the administrator turns on after the install; an
upgrade that keeps the configuration leaves it as it was (open stays open, shut
stays shut). The closing summary says whether it is open and how to
open it from any login that has `sudo` - on a server with no screen or
keyboard, this is how SD is administered:

```
sudo /usr/local/sbin/sd-elevate sdsys-ssh on
```

(`remote.sdsys on` at the SD prompt does the same, but needs `sdsys` signed in
at the machine itself.) From then on `ssh sdsys@<host>` asks for the `sdsys`
Linux password and lands at the SD prompt. **Once the door is open, that
password alone stands between the network and the administrator**, so choose a
strong one and shut the door when it is not needed. If you skip the `sdsys`
password, the door can be open and still let nobody in until `sudo passwd sdsys`
sets one. See the Administrator set's *Remote administration over ssh*.

**The ssh boundary is applied either way, and it is what actually confines
SD accounts.** Every account except SDSYS is `ForceCommand`'d into `sd` the
moment it connects over ssh — it never reaches a plain shell that way — and
SDSYS is refused a network login outright, at the door, however the two
questions above were answered, until the administrator opens that door. This step is **non-fatal**: if `sshd_config`
has already been customized, the installer warns rather than aborting (SD
is otherwise installed and working) and prints the exact command to apply
it by hand once the conflict is resolved:

```sh
sudo /usr/local/sbin/ssh-forcecommand --install
```

## What lands where

| What | Where |
|---|---|
| Binaries | `/usr/local/bin` |
| The changelog | shipped with the source tree |
| Configuration | `/etc/sd.conf` |
| The SDSYS account | `/usr/local/sdsys` |
| User accounts | `/home/sd/user_accounts` |
| Group accounts | `/home/sd/group_accounts` |

### Configuration

Server and client both read `SD_CONFIG` first and fall back to
`/etc/sd.conf`. It is installed once and left alone on a later install over
a kept database, so your edits survive both an upgrade and a reinstall.

## What the installer creates on the machine

| | |
|---|---|
| `sdusers` | the Linux group every SD account belongs to. Everyone who uses SD needs it |
| `sdsys` | the one administrator account — a real Linux user with its own home, shell and password, never `root` |
| `sdu_<name>` | one supplementary group per user account, created by `create.account` with `root` and the user in it. **The `sdsys` user is a member of every one of them as delivered**, so that SDSYS can change that account (its VOC, dictionaries and programs); the administrator takes it out of one with `modify.account` *name* `sdsys-off` (and puts it back with `sdsys-on`). While it is in, it has write access to everything the group may write |
| `sd.service`, `sdclient.socket` | the `systemd` units that run SD and its API listener, enabled to start at boot |
| the ssh boundary | a fenced block in `/etc/ssh/sshd_config`, `ForceCommand`ing every `sdusers` member except `sdsys` into `sd`, and denying `sdsys` a network login outright until the administrator opens that door |

**Group membership needs a fresh login to take effect**, the same as on any
Linux box — if you were just added to `sdusers`, log out and back in (or
start a new session) before expecting `sd` to work.

## Ownership and administration

**Being SDSYS means being logged in to the machine as the `sdsys` Linux
user, at its own password, on a local session** — the keyboard, or a
desktop-sharing view of it (VNC, TeamViewer). There is no `sudo` or `su`
route into it: a session that reaches the `sdsys` account any way other
than a real login as `sdsys` is refused, and `sdsys` cannot sign in over
ssh at all. See [Security](12-security.html).

## The full-screen editors

**The installer installs `micro` as an ordinary package**, because the
`micro` verb runs it. It is not offered as a choice — an account with an
editor verb that does nothing is worse than either answer. **`ed`**, the line editor, and **`sed`**, the
full-screen editor with menus, are part of SD and need nothing installed; they
always work.

`micro` is one of the packages the install requires: if it cannot be
installed, the install stops. `micro`'s own syntax file still needs a
per-user copy (`~/.config/micro/syntax`), which the installer also stages
where it can.

## Your own account's access gates

An SD account starts with every access gate closed: ssh, the API, the shell,
`os.execute`, `sd.accounts`, saving changes to a VOC, a program file or a
dictionary, the recovery copy, SDNet, the shared account's files, the
files-only login (with its write and admin rights), the AI, pins, and the
`sdsys` user in the account's group — yours too, the account the installer
makes for you.

**When the installer is about to make that account, it asks once:** *Open every
access gate for <you>'s SD account? (y/N)*. **The answer is No unless you type
y**, and nothing is asked when your account already exists (an upgrade keeps
what it has). It is meant for a machine you are testing on. A **y** opens every
one of the gates above, and the install then says which ones the register and
the Linux groups really hold, naming any that did not open. The AI gate only
lets the account use the AI once SDSYS has chosen a provider and given its key.

With **No**, the installer prints the commands that open them. Signed in as SDSYS,
`modify.account <account> <word>` opens any of them (`both`, `sh-on`, `os-on`,
`sd-on`, `voc-on`, `bp-on`, `dict-on`, `recovery-on`, `net-on`, `shared-write-on`,
`files-on`, `files-write-on`, `files-admin-on`, `ai-on`, `pins-on`, `sdsys-on`;
several may be given in one command), and `modify.account <account> <word>-off`
closes it again (`none` closes ssh and the API).

This is not about who can reach the computer from the network — that is the two
questions above.

## Where sessions start

A new installation asks *Start new sessions at the home screen or at the command
prompt?* The home screen is a page of tiles for the account's tools; the command
prompt is SD's `:` prompt, as in earlier releases.

* **A new installation** offers the home screen (**H**): press Enter to keep it, or
  type **p** for the prompt.
* **An upgrade that keeps the accounts does not ask**: sessions go on starting
  where they did, and the installer says which. `deletesdcore.sh` saves the
  setting when it removes the old install, and an install **from before the home
  screen (L1.1-3 or earlier) is saved as the prompt**. Use the `deletesdcore.sh`
  of the new release package for the upgrade. When no setting was saved - an
  older `deletesdcore.sh`, such as L1.1-3's own - the upgrade starts sessions at
  the prompt, which is where L1.1-3 always started them.
* The answer is the system's default. An account that has a start setting of its
  own keeps it. Signed in as SDSYS, `set.start.default terminal` or
  `set.start.default menu` changes the default later, and `modify.account
  <account> start-terminal`, `start-menu` or `start-default` sets one account
  (*Accounts and Security* in the Administrator documentation).

## Changing any of it afterwards

Both remote-access settings have a verb that changes them later, which is
why an upgrade does not ask the two questions again. Both are SDSYS's, and
both report when given no keyword:

| | |
|---|---|
| `remote.ssh on` \| `off` | who may reach the ssh server from off this machine |
| `remote.api on` \| `local` \| `off` | whether SD opens its API socket, and who may reach it |

They are covered in the Administrator set, under *Remote access and the
machine*.

## At the end

The install ends by setting three passwords, at the terminal, each with its
own numbered heading — asked at most three times, and skipped with a clear
"kept from the previous install" if one from an earlier install (or an
earlier attempt) is already there:

```
1 of 3: Password for the SD <you> account
2 of 3: Password for the LINUX sdsys account
3 of 3: Password for the SD sdsys account
```

**These are three different things, deliberately kept apart:**

| | What it unlocks |
|---|---|
| 1. Your own SD password | reaching your account through the SD API (SCRAM) — not needed at all for a local `sd` session, which your Linux login already reaches |
| 2. `sdsys`'s Linux password | logging in to the machine **as** `sdsys` — the only way to administer SD |
| 3. `sdsys`'s SD password | reaching SDSYS through the API — and even with it, SD admits `sdsys` over the API only from a process already running as `sdsys` on this machine |

All three are required — the closing summary names any that are still
missing and prints the exact `modify.password` command to set it,
afterward, as `sdsys`.

The closing summary also restates: **SD is administered only by logging in
as `sdsys`, its own password, and running `sd`** — that session has every
admin verb. There is no `sudo` or `su` route into it, and `sdsys` cannot
log in over ssh; a desktop-sharing view of the console works because it is
a local login.

It then offers to reboot, so that group membership changes and the
`systemd` units take effect cleanly. After rebooting (or a fresh login),
open a terminal and type `sd`.

## Continued in

[Upgrading and uninstalling](01a-upgrading-and-uninstalling.html) — upgrading
an existing installation, and uninstalling.

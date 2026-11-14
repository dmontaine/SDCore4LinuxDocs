Title: Remote Administration over ssh
Subtitle: How SDSYS, the administrator, can sign in over ssh from another computer with its password; how to turn it on and off; what it refuses; the risk; and what can stop it working.

**SDSYS can sign in over ssh from another computer, but only after you have opened that door.** As
delivered the door is shut: `sdsys` is refused a network login at the ssh server. The installer does
not ask about it and never opens it, and an upgrade shuts it again; open it as "Opening and shutting
the door" below says. Once you open it, a
sign-in over ssh asks for `sdsys`'s password and lands in an SD session with every right the local
SDSYS has.

**Open it with care: with the door open, nothing but the `sdsys` password stands between the network
and the administrator.** Open it only on a machine whose `sdsys` password is long and used nowhere
else, and shut it again when it is not needed. SD asks for no second factor here; earlier test
versions of this release did, and it was taken out because it was more security than the people who
run SD wanted.

**The API is not part of this.** SDSYS still has no API access from another computer or over the
network port, under any setting; on the machine itself it uses the local Unix socket only. This
page is about ssh and nothing else.

**This page is about SD Core for Linux.** SD Core for Windows has the same door in its own form:
there the administrator is an elevated Windows account, so the door opens a separate account that
signs in over ssh only and is never elevated; its own documentation describes it. Neither SD Core
Solo has it.

> This document is separate so that it can be withheld. It links to nothing outside the
> administrator set. Where a page in another set is worth naming, it is named in words.

## What a sign-in looks like

```
$ ssh sdsys@server
Password:
```

* **The password** is `sdsys`'s Linux password. Someone who gets it wrong is told only that the
  sign-in failed.
* **What you get** is an SD session as SDSYS, in the terminal, and nothing else: there is no shell
  behind it, no port forwarding of any kind, no X11, no agent forwarding, no tunnel, no `scp` or
  `sftp`, and no key or authorized-keys sign-in. A command given on the ssh command line is not run.

## Opening and shutting the door

You need root for this: either the machine's own administrator account (`sudo`), or `sdsys` signed
in at the machine itself. Nothing here needs an ssh session as `sdsys`, so a server with no screen
and no keyboard is set up from your ordinary ssh login.

```
sudo /usr/local/sbin/sd-elevate sdsys-ssh on
sudo /usr/local/sbin/sd-elevate sdsys-ssh off
sudo /usr/local/sbin/sd-elevate sdsys-ssh status
```

`on` writes the ssh settings described below, checks with `sshd` itself that the result is what it
meant, and only then reports success. If the check does not come out right, the file is put back
exactly as it was and you are told why (see "What can stop it"). `off` shuts the door again: `sdsys`
is denied a network login. `status` says which it is now (`sdsys-arm=open` or `closed`).

### From inside SD: `remote.sdsys`

SDSYS signed in at the machine can do the same without leaving SD:

```
remote.sdsys {on | off}
```

| | |
|---|---|
| *(no keyword)* | says whether ssh lets `sdsys` in, and changes nothing |
| `on` | opens the door, as `sdsys-ssh on` does |
| `off` | shuts it, as `sdsys-ssh off` does |

The same is the sixth view of `tool.remote`, **`6` sdsys login**: it shows the report, and `O` and
`F` run `remote.sdsys on` and `off` after a box (the box for `on` wants the word `OPEN` typed).

Each use writes one audit line, `remote.sdsys on status=0` and the like: the keyword and the
helper's exit status.

## What SD changes on the machine

* **`/etc/ssh/sshd_config`**: in SD's fenced block, the arm for `sdsys` changes from "denied" to a
  set of settings that allow password sign-in only (no key, host-based or GSSAPI route, three
  tries), with every kind of forwarding shut, and `ForceCommand` into `sd`. Nothing else in the file
  is touched.
* **Nothing in the PAM files.** SD writes no PAM line for this.

`ssh-forcecommand --remove` takes SD's block out.

### A machine that an earlier test version set up

Earlier test versions of this release asked a second factor, a code from an authenticator app, and
left lines in `/etc/pam.d/sshd` and in the console sign-in files, a module in `/usr/local/lib/sd`, and
files under `/etc/sdcore/totp*` and `/run/sdcore`. The installer cleans all of it on an upgrade: the
`sdsys` arm is written shut, the lines are taken out of the PAM files (byte for byte as they were
before), and only then are the module and the files removed, because a PAM line naming a missing
module would fail a sign-in. If that cleaning could not be done the installer says so and leaves the
module where it is; run `sudo /usr/local/sbin/ssh-forcecommand --clean-legacy` once the cause is
resolved. After an upgrade the door is **shut**; open it again if you want it.

## What still refuses

* **`su sdsys` and `sudo -u sdsys`** from another user's session, as before: SD asks the kernel who
  logged in, and a sign-in that was somebody else's is refused. The root helper `sd-elevate` asks the
  same of anyone who is `sdsys` to `sudo`.
* **The API** from another computer or over the network port.
* **cron and at for the `sdsys` user.** A cron job starts a login of `sdsys` with nobody there, so the
  installer puts `sdsys` in `/etc/cron.deny` and, where `at` is installed, `/etc/at.deny`.
  A crontab `sdsys` already had is moved to `/var/backups/sdcore-sdsys-crontab.<date>` (root only),
  because cron would go on running it. SD's own scheduled work is set up with the Jobs view of
  `tool.jobs`, or `set.job`, instead (both ask `sudo /usr/local/sbin/sd-elevate job-set`): timers only
  root can set, each running one fixed SD command (see [Scheduled Jobs](23-scheduled-jobs.html)). To let `sdsys` use cron again, take it out of `/etc/cron.deny`; an `/etc/cron.allow` you
  wrote decides by itself, and the installer only warns when it names `sdsys`.

## What can stop it working

Turning it on asks `sshd` what it would do with `sdsys` and refuses, with nothing changed, if the
answer is not the one SD wrote. It names the cause. The ones that happen:

* **An earlier `Match` block** (above SD's, or in an included file) that sets a keyword for the
  connection first, such as `PasswordAuthentication no` or `AuthenticationMethods publickey` for an
  address range. A global line does not do this; a `Match` block does.
* **A `DenyUsers` or `DenyGroups`** that names `sdsys` or its group.
* **An `AllowUsers` or `AllowGroups`** that leaves `sdsys` out, which would shut the door without
  a word. Add `sdsys` to it, or remove it.

## What it does not do

* It does not accept a push approval, an ssh key, or a second factor of any kind.
* It does not give anyone but SDSYS a remote route. Every other account is unchanged.
* It does not protect against someone who has the password.

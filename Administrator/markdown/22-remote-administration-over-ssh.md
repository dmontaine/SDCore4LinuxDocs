Title: Remote Administration over ssh
Subtitle: How SDSYS, the administrator, can sign in over ssh from another computer with an authenticator code; how to turn it on and off; what it refuses; and what can stop it working.

**SDSYS can sign in over ssh from another computer, but only after you have enrolled an
authenticator code for it.** Until then the door is shut, exactly as it always was: `sdsys` is
refused a network login at the ssh server. Once a code is enrolled, a sign-in over ssh asks for the
code first and the password second, and lands in an SD session with every right the local SDSYS has.

**The API is not part of this.** SDSYS still has no API access from another computer or over the
network port, under any setting; on the machine itself it uses the local Unix socket only. This
page is about ssh and nothing else.

**This is a feature of SD Core for Linux only.** SD Core for Windows has no equivalent, because
Windows has Remote Desktop for this, and SD Core Solo does not have it either.

> This document is separate so that it can be withheld. It links to nothing outside the
> administrator set. Where a page in another set is worth naming, it is named in words.

## What a sign-in looks like

```
$ ssh sdsys@server
Verification code:
Password:
```

* **The code comes first and the password second, and both are always asked.** Someone who gets
  either wrong is told only that the sign-in failed: the machine does not say which of the two was
  wrong.
* **The code** is the six digits your authenticator app shows, or one of the eight recovery codes
  (see below). It is not echoed.
* **The password** is `sdsys`'s Linux password.
* **What you get** is an SD session as SDSYS, in the terminal, and nothing else: there is no shell
  behind it, no port forwarding of any kind, no X11, no agent forwarding, no tunnel, no `scp` or
  `sftp`, and no key or authorized-keys sign-in. A command given on the ssh command line is not run.

## Turning it on: enrolling a code

You need root for this: either the machine's own administrator account (`sudo`), or `sdsys` signed
in at the machine itself. Nothing here needs an ssh session as `sdsys`, so a server with no screen
and no keyboard is set up from your ordinary ssh login.

```
sudo /usr/local/sbin/sd-elevate totp-begin
```

It prints two lines, **once**, and never again:

```
secret=JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP
uri=otpauth://totp/SD%20Core:sdsys@server?secret=...&issuer=SD%20Core&algorithm=SHA1&digits=6&period=30
```

Put the secret into an authenticator app by typing it, or open the `otpauth://` link where the app
can read it. It is a standard time-based code (six digits, thirty seconds), which Google
Authenticator, Microsoft Authenticator (as an "Other account"), Authy, 1Password and FreeOTP all
accept. **Anyone who sees the secret can make the codes**, so clear your terminal when you are done.

Then prove that the app has it:

```
sudo /usr/local/sbin/sd-elevate totp-confirm
```

Type the six digits the app shows now and press Enter. If they are right you get `ok` and **eight
recovery codes**, again once only:

```
recovery=ABCDE-FGHIJ
...
```

**Keep the recovery codes somewhere that is not the phone.** Each works once, in place of the
six-digit code, if the phone is lost; SD keeps only a hash of them and cannot show them again.

Confirming also opens the door: SD writes the ssh settings and the two sign-in lines described
below, checks with `sshd` itself that the result is what it meant, and only then reports success. If
the check does not come out right, both files are put back exactly as they were and you are told
why (see "What can stop it").

* **Five wrong codes** at `totp-confirm` throw the new secret away; run `totp-begin` again.
* **`sudo /usr/local/sbin/sd-elevate totp-status`** says whether a code is enrolled, whether a new
  one is waiting to be confirmed, how many recovery codes are left, and whether the ssh door is open.
* **`totp-recovery`** makes a new set of eight recovery codes. The old set stops working.
* **To change the phone**, run `totp-begin` and `totp-confirm` again. The old secret keeps working
  until the new one has been confirmed, and then it stops.

### From inside SD: `remote.sdsys`

SDSYS signed in at the machine can do all of this without leaving SD:

```
remote.sdsys {on | recovery | off}
```

| | |
|---|---|
| *(no keyword)* | prints what `totp-status` reports, and changes nothing |
| `on` | shows a new secret and its link **once**, then asks `Code from the app (Enter to stop):` up to three times. A right code switches the code on, shows the eight recovery codes and opens the ssh door, exactly as `totp-confirm` does |
| `recovery` | shows eight new recovery codes; the old ones stop working |
| `off` | shuts the ssh door first, then removes the code, as `totp-off` does |

**The secret and the recovery codes appear on your terminal and nowhere else.** They are not
written to any file, the audit trail or the error log; after them the verb waits for Enter and
clears the screen. `on` and `recovery` refuse while a `como` file is recording the session, since
it would keep them (close it with `como off` first). The code you type is passed to the root
helper through a private file that is removed at once, never on a command line. Your terminal's
own scroll-back is outside SD's reach: clear it if anyone else may see it.

The same is the sixth view of `tool.remote`, **`6` sdsys login**: it shows the report, and `O`,
`R` and `F` run `remote.sdsys on`, `recovery` and `off` after a box (the box for `on` wants the word
`OPEN` typed). For `on` and `recovery` the page gives the terminal to the verb, so the secret and
the codes never pass through the page.

Each use writes one audit line, `remote.sdsys on status=0` and the like: the keyword and the
helper's exit status, never what it printed.

## Turning it off

```
sudo /usr/local/sbin/sd-elevate totp-off
```

It shuts the ssh door first (`sdsys` is denied a network login again) and then removes the secret and
the recovery codes. If the door cannot be shut it still removes them, tells you so, and exits with
status 3: with no code enrolled the sign-in refuses `sdsys` anyway, but close the door by hand.

## What SD changes on the machine

* **`/etc/pam.d/sshd`**: two lines, between marker comments, above its first `auth` line. The first
  skips the second for every user but `sdsys`. The second is SD's own module,
  `/usr/local/lib/sd/pam_sdtotp.so`, which asks for the code. **Nothing else is touched**: not the
  files `login`, `su` and `sudo` share, and not another user's sign-in.
* **`/etc/ssh/sshd_config`**: in SD's fenced block, the arm for `sdsys` changes from "denied" to a
  set of settings that allow keyboard-interactive sign-in only, with every kind of forwarding shut,
  and `ForceCommand` into `sd`.
* **`/etc/sdcore/totp/`**: the secret, the recovery codes and the record of failed sign-ins. The
  directory is 0700 and the files 0600, root's: no other user, SDSYS included, can read them, and
  no command prints a secret that is already stored. It is not part of an account backup.

`ssh-forcecommand --remove` takes both fences out, the ssh one first.

## Wrong codes and locks

* **Failures are counted for each source address**, not for the account: the name `sdsys` is public,
  and a lock on the account would let anyone shut the administrator out. An attempt is counted when
  it starts.
* **Five attempts from one address lock that address for ten minutes** after its last attempt. A
  locked address is not asked for a code at all, and does not use a code up.
* **A sign-in that succeeds all the way** (code and password) clears its address's count. A right code
  with a wrong password does not: it stays counted.
* **More than thirty attempts from anywhere in an hour** make every refusal wait ten seconds
  instead of three. Nobody is locked out by it.
* **A code is used once.** Neither the same code nor an older one is accepted again.

Every attempt is written twice, to the audit trail (see [The Audit Trail](21-the-audit-trail.html))
and to the system log (`authpriv`), with the address and a reason, and never a code:

```
remote sdsys login code accepted source=203.0.113.9
remote sdsys login code refused source=203.0.113.9 reason=wrong code
remote sdsys login recovery code used source=203.0.113.9
remote sdsys login succeeded source=203.0.113.9
```

The reasons are `wrong code`, `used code`, `bad code`, `no answer`, `locked`, `not enrolled` and
`store unsafe`. **A recovery code being used is logged at a higher priority**, since it usually means
the phone is gone. Leave `UseDNS` off in `sshd_config` (it has been the default since OpenSSH 8.7):
with it on, the "address" is a name that the other side chooses.

## What still refuses

* **`su sdsys` and `sudo -u sdsys`** from another user's session, as before: SD asks the kernel who
  logged in, and a sign-in that was somebody else's is refused. The root helper `sd-elevate` asks the
  same of anyone who is `sdsys` to `sudo`.
* **The API** from another computer or over the network port.
* **A store that is not what it should be.** If the directory or a file is open to others, is a link,
  has a second link, or is damaged, the sign-in is refused and nothing is changed.

## What can stop it working

Turning it on asks `sshd` what it would do with `sdsys` and refuses, with nothing changed, if the
answer is not the one SD wrote. It names the cause. The ones that happen:

* **`UsePAM no`** in `sshd_config`. The password would not go through PAM, so the code would never
  be asked. SD does not change this setting.
* **An earlier `Match` block** (above SD's, or in an included file) that sets a keyword for the
  connection first, such as `PasswordAuthentication yes` for an address range. A global line does
  not do this; a `Match` block does.
* **A `DenyUsers` or `DenyGroups`** that names `sdsys` or its group.
* **An `AllowUsers` or `AllowGroups`** that leaves `sdsys` out, which would shut the door without
  a word. Add `sdsys` to it, or remove it.
* **A module that is not as it should be**: missing, a link, or writable by anyone but root.

## What it does not do

* It does not accept a push approval (Entra ID, Google prompts), an ssh key, or a password alone.
* It does not give anyone but SDSYS a remote route. Every other account is unchanged.
* It does not protect against someone who has both the phone and the password.

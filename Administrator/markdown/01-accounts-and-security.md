Title: Accounts and Security
Subtitle: Making and changing accounts, passwords, and who may enter an account.

These are the verbs that decide **who may use this installation and what
they may do with it.** They are SDSYS's set — not in any other account's
VOC at all — and almost all of them need more than the verb before they
will do anything.

> **This document is separate so that it can be withheld.** Everything in
> the administrator set describes verbs an ordinary account does not have
> and cannot run. It is a complete set on its own and **links to nothing
> outside itself**, so that handing somebody the user documentation without
> this never leaves them at a page that is not there. Where a user-set page
> is worth naming, it is named in words rather than linked.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## Read this before anything else: being SDSYS is the whole of it

**Having the verb is not having the right to use it — and there is exactly
one gate, one route in, and nothing that widens it.** Every verb on this
page is refused outright to any session that is not actually SDSYS:

```
:modify.account don suspended
Command requires administrator privileges
:delete.account sdsys
Command requires administrator privileges
:modify.password sdsys
Command requires administrator privileges
```

**Every one of those refusals came before the command was looked at.**
`delete.account sdsys` would have been refused anyway — you cannot delete
`SDSYS` — and it never got that far.

**Being SDSYS means being logged in to the machine as the `sdsys` Linux
user, at its own password, on a local session** — the keyboard, or a
desktop-sharing view of it (VNC, TeamViewer). Nothing else grants it:

| route | result |
|---|---|
| a real login as `sdsys`, local | granted |
| `sudo sd` as root | refused — root is treated as *another* administrator, not SD's |
| `sudo -u sdsys sd` / `su - sdsys` | refused — the session runs as the `sdsys` Linux user, but the login that started it was somebody else's, and the kernel's own audit trail (unforgeable without root) says so |
| `sdsys` over ssh, or over the API from another computer or the network port | refused at the door — SDSYS has no remote access at all |
| `sdsys` over the API, on the local Unix socket, from a process running as `sdsys` | granted, with SDSYS's own SD password |

**This is not the elevation model SD Core for Windows uses**, and the
difference is deliberate, not a gap: Windows checks whether the session is
*elevated*; Linux checks whether the session *is* the `sdsys` account,
reached the one way that account can be reached. A `sudo`'d shell looks
like `sdsys` to the file system, but the login it came from was not — and
that distinction is exactly what closed the class of bug Windows found in
its own elevation check (an administrator's *own* account picking up SD
privilege it should never have had). There is no `sdsys` session that isn't
also a real login as `sdsys`, so there is nothing for that bug shape to
hide in here.

**Start SD as yourself, from the `sdsys` login, in an ordinary terminal —
`sd` needs no elevation, no `sudo`, because being SDSYS already *is* the
privilege.**

## Making an account: `create.account`

```
create.account user <name> {ssh | api | both | none} {sh-on} {os-on} {no.query}

create.account group <name> {no.query}

create.account other <name> <pathname> {no.query}
```

| | |
|---|---|
| **`user`** | an SD account **and** a Linux user account to log in as |
| **`group`** | a shared workspace with no Linux account, reached only with `logto` |
| **`other`** | an SD account over a directory you name |

**A new user account starts with every door shut.** Say nothing and it has
no ssh, no API, no `sh` and no `OS.EXECUTE`; you open each one by naming
it. `ssh`, `api` or `both` give the remote routes (`none` is the default
and is accepted so that a script can say so); `sh-on` and `os-on` give the
two operating-system switches, and they are independent, so `sh-on os-on`
gives both and neither cancels the other. **This is the setting SD is
delivered with, on purpose: it is the tighter one, and you loosen it for the
accounts that need it, one at a time** — the same words change an account
later in `modify.account`, below. When it has made the account SD says
where it stands:

```
fred has no remote access: not ssh, not the API
Account fred has SH no, OS.EXECUTE no
```

**The installing user's own account is no exception**: the account the
installer makes so that somebody can sign in starts with all four off too, and
the installer says so and how to change it. The accounts that keep their
access are the ones that already exist when you *upgrade* — see *Changing
one*, below.

**A group account and an `other` account have no Linux user of their own,
so `sh-on` and `os-on` are refused for them** — "is a group account and has
no Linux user, so it has no shell to permit". A shell is a fact about a
person, and a group account is not one.

> **It prompts for a password and `no.query` does not suppress that.**
> `no.query` covers the confirmation, not the credential — a password is
> never an argument anywhere in SD. **`create.account user` therefore
> cannot be driven from a script**, and a group account, which has no
> password, can.

**An account is never left without a password.** If SD cannot set the new
user's password and you answer `n` at "Retry", it removes the Linux user it
has just made, with its home directory, and says "An account must have a
password. Nothing was created." Should the removal itself fail it says so and
gives the `userdel` command that finishes it. This applies to a user SD
creates; it does not touch an existing Linux user, which `create.account`
still refuses.

**It warns when a route has nothing behind it.** An account given the ssh
or the API route is checked: if this computer has no ssh server installed,
or the API listener is off (`remote.api on` turns it on), `create.account`
says so after the route line. The warning does not stop anything: the
account is made and the route works the day the server or listener is
turned on.

**Every account gets the same VOC**, the whole of `newvoc` — there is no
tier. What differs from one account to the next is what it is *allowed to
do* with the verbs it has: its remote routes and its two operating-system
switches are per-account settings, all off until you turn them on.
**SDSYS is the exception and it is not a setting** — see above; it is never
refused by these switches, and it has no remote access whatever it is
given.

### Two settings that are easy to conflate

| | |
|---|---|
| `ssh`, `api` | say who may **connect** |
| `sh-on`, `os-on` | say who may reach the **operating system** |

Holding the first has never implied the second. **ssh alone does not give a
shell**: every ssh session is forced into `sd`, so what the person can do is
what SD lets them do — and an account without `sh-on` gets no shell from SD.

### The operating-system switches: `sh-on` and `os-on`

Two independent switches, kept per account in the register. **Both are off
for a new account** and SDSYS turns each on with `modify.account` (below).
An account with neither is still a full SD user: it runs programs, opens
every file its VOC names, builds indexes, runs queries — everything that
stays inside SD.

| | |
|---|---|
| **`sh-on`** · `sh-off` | the `sh` verb and `!` |
| **`os-on`** · `os-off` | `OS.EXECUTE` in a BASIC program, the screen editors `nano` and `micro`, the embedded Python, **and reaching an operating-system file or directory by its path outside the account's own directory** |

That last clause is the one that is easy to miss. Without `os-on` an
account can still open every file it reaches **through its VOC** —
dictionaries and other SD files included — and anything inside its own
directory, **provided the VOC pointer leads somewhere it may go** (the
section below the table). What it cannot do is name `/etc`, another account's
directory, or a symbolic link that points out of its own, in any of these:

| | without `os-on` |
|---|---|
| `OPENSEQ` and `OPENPATH` with a path | status 3035, so `OPEN ... ELSE` works as before |
| `DIR()` and the `select.dir` verb | no entries, and `STATUS()` is set (the verb says why) |
| `DELETESEQ` of a bare path | status 3035; the file is left alone |
| `!OSCOPY`, `!IOSCOPY` and the `oscopy` verb | refused, status -4 (the verb says why) |
| printing into a file by path (`setptr ... as pathname`, or the `SETPU` statement) | the verb refuses when the unit is set; for either, the first line printed is refused and the program stops |

The containment is by **real path**: `..` and a symbolic link are resolved
before the test, so neither gets round it. A path inside the account's own
directory always works.

**SD says no in words.** `sh` gives "*name* is not permitted to use the
operating system shell", `OS.EXECUTE` gives "*name* is not permitted to use
OS.EXECUTE", and the path routes give "*name* has no OS access, so a file or
directory outside its own account cannot be reached by pathname (SDSYS can
give it: `modify.account` *name* `os-on`)". **SDSYS is never refused.**

### The third switch: `sd-on`, other SD accounts' directories

`os-on` is wide: it reaches any path. `sd-on` is the narrow version, for an
account that has to read or write the **data** of a neighbouring SD account
(a shared reports folder, a hand-over directory) without being given the
whole machine. It is **off for a new account**, and `modify.account` *name*
`sd-on` / `sd-off` turns it on and off. It may be set on a group account
(`sh-on` may not).

With `sd-on`, the path routes in the table above also accept a path under the
directory of any SD account **the user could `logto`**: the register's group is
one the user belongs to, and the account is not suspended. Reading and writing
are one switch. Two things stay shut:

- **The other account's VOC** (`voc`, `voc.dic` at the top of its directory)
  is never reachable this way; the account's own VOC is, as always.
- Any directory that is not an SD account's, `/etc` included, still needs
  `os-on`.

**SDSYS is not affected** — it is never refused. `os-on` implies `sd-on`.
The setting lives in field 9 of the register record and is not carried by an
account archive, so a restored account starts with it off.

### VOC pointers: where a file pointer may lead, and which Q-pointers are followed

**A VOC pointer is a way to name a file, so it is held to the same rule.** An
account can write a pointer into its own VOC with `ed`, or make one with
`create.file ... pathname`, and a Q-pointer is what `set.file` makes into
another account. For everybody but SDSYS:

| | |
|---|---|
| **a file pointer (F-type)** | must lead **inside the account's own directory**, or inside the directory of an account a Q-pointer was followed into (below), or be **the pointer SD itself put in the VOC** — the same id, with the same path, as in `newvoc` (`syscom`, `$map`, `sd.voclib`, `dict.dict`, `voc`, `newvoc`, `$acc`). An account that holds `os-on` may go anywhere its Linux user can. Anything else is refused with status 3035 |
| **a Q-pointer** into a **registered account** | is followed only if the user **could `logto` that account**: a member of its Linux group, and the account not suspended — `logto`'s own test — **whether or not the account holds `os-on`**. SD's own two Q-pointers, `sd.accounts` (which leads into SDSYS, an account nobody can `logto`) and `md`, are exempt because they are exactly what SD put there |
| **a Q-pointer** that **names a path** | is an operating-system path, and the `os-on` question |

So `set.file` into somebody else's account works only for a user who may enter
that account, and a hand-made pointer at `/etc` or another account's
directory is refused unless the account holds `os-on`. A refused open takes
the `ELSE` branch with status 3035, like any other refusal here. **SDSYS is
never refused.**

**What this changes on an existing machine.** A Q-pointer that leads into an
account its owner can no longer enter stops opening, and so does a hand-made
file pointer to a directory outside the account in an account that does not
hold `os-on`. The accounts that existed at an upgrade hold `os-on`, so their
own pointers keep working; the Q-pointer rule applies to them too.

**`filerule`**, the `sd.conf` setting that turns on the `path:name` and
`account:name` forms of a file name, is off unless you set it. If you do, the
`path:` form is held to the `os-on` rule like the rest, and the `account:name`
form is a Q-pointer and is held to the Q-pointer rule above.

### What `os-on` actually costs

Granting `os-on`, or `sh-on`, to an account that also has a remote route is
a larger decision than it looks: **it puts an operating-system shell behind
that account's credential, reachable from wherever the route is reachable
from** — the ssh port, or the API port. What the shell can do is exactly
what that Linux user can do on this machine, and nothing more, because SD
runs it as that user and never as root; so the cost is the cost of giving
that person a login on the machine. For an account that needs only SD,
leave both off.

```
umask {mask}
```

With no argument `umask` reports the session's current value; with one, it
sets it — the standard Unix meaning, applied to files SD itself creates as
well as anything a shelled-out command creates. **This is a real,
per-session mechanism here** — it has no Windows equivalent because Windows
reaches the same guarantee a different way, one inheritable ACL entry set
once by the installer, applied by NTFS below the runtime rather than by a
value a process can forget to set.

## Changing one: `modify.account`

```
modify.account account add | delete  <user.name>
modify.account account ssh | api | both | none
modify.account account sh-on | sh-off
modify.account account os-on | os-off
modify.account account sd-on | sd-off
modify.account account suspended | unsuspended
```

### The other keywords

| | |
|---|---|
| **`ssh`** \| **`api`** \| **`both`** \| **`none`** | what the account's remote access **is**. Absolute: `api` takes ssh away |
| **`sh-on`** \| **`sh-off`** | the `sh` verb and `!` |
| **`os-on`** \| **`os-off`** | `OS.EXECUTE`, the screen editors, the embedded Python, and operating-system paths outside the account's own directory (see above) |
| **`add`** \| **`delete`** *user* | put a Linux user in, or out of, the account's group |

**The first group is absolute and the second is not.** `ssh`/`api`/`both`/
`none` are four names for one state, so whatever is not named is withdrawn.
`sh-on` and `os-on` are two independent switches over two separate settings,
so **`sh-off` says nothing about `OS.EXECUTE`** and leaves it alone.

After either pair SD says where the account **now** stands, both fields at
once, so that a command that did only what it named is plain to see:

```
:modify.account fred sh-on
Account fred has SH yes, OS.EXECUTE no
:modify.account fred os-on
Account fred has SH yes, OS.EXECUTE yes
:modify.account fred sh-off
Account fred has SH no, OS.EXECUTE yes
```

Asking for what is already so changes nothing and says so ("fred already had
that access; nothing changed"). A route word reports the route in the same
way ("SD routes for fred: ssh and the API." — "fred has no remote access:
not ssh, not the API").

**A change takes effect the next time the account is entered.** The setting
is read when a session signs in or `logto`s into the account, so a session
already open keeps what it started with. To take a grant away from somebody
who is signed in now, change the setting and then end their session.

**Every one of these words is written to the audit trail** (`modify.account
sh-on account=fred` and its siblings), and **SDSYS is never a target**: the
account name is refused as invalid before the word is read. A group account
is refused too for the `sh-on`/`sh-off`/`os-on`/`os-off` forms: it has no
Linux user to hold the switch.

**Upgrading keeps what accounts have.** The installer switches `sh` and
`OS.EXECUTE` on, once, for every user account that exists when you upgrade
(ssh and the API are left exactly as they were), so that nobody loses a
command they were using. You can then turn them off one account at a time,
and a later install does not turn them back on. Only accounts made after the
upgrade start with everything off.

### `suspended`/`unsuspended` is a state, not a tier

**Nothing about the account moves except the one field.** No group
membership changes, no VOC changes — every account's VOC is the whole of
`newvoc` regardless of the field. Three doors refuse a suspended account:
signing in, `logto`, and the API.

### `add`/`delete` is the grant

```
:modify.account don add pete
:modify.account don delete pete
```

**This is Linux group membership, and it *is* what a grant is** —
`usermod -aG` under `sd-elevate`, with SD's own audit line added. There is
no separate `grant`/`revoke`/`list.grants` set of verbs the way SD Core for
Windows has: on Windows, group membership is Windows' own mechanism and SD
wraps it with three verbs of its own name and an audit trail; on Linux the
wrapping is folded into `modify.account` instead, for the same reason
Windows's own reference names its `grant` as "not an extra capability" —
`usermod -aG` reaches the identical Linux group directly, outside SD, at
any time, by an administrator with a shell. `modify.account`'s value is the
audit line, not a gate nothing else could reach.

**`delete` is deliberately unguarded** — taking access away is always
allowed.

## Passwords: `modify.password`

```
modify.password {account}
```

With no account name it changes **your own**, and asks for the current
password first. With one, from SDSYS, it changes that account's — any
account, including SDSYS's own — and does not ask for the old password: an
administrator resetting a forgotten password does not know it.

**The password is never an argument, and a trailing token is refused rather
than ignored:**

```
:modify.password don hunter2
A password is never given on the command line; modify.password prompts for it
```

**That refusal is the point of the verb's design.** The older behaviour set
the password from the prompt and threw the extra word away without a word,
so every visible sign said it had worked — while the password had already
reached SD's command stack, and a shell's history and process list if the
verb was reached from one. Refusing does not put it back, but it says so.

The prompts are hidden, asked twice, and the account must already exist in
the register. **`modify.password` cannot be scripted**, by design.

**Under the hood, an ordinary account's own write goes through a
privileged helper it cannot bypass** (`sd-elevate cred-own`), because the
credential file (`$cred`) belongs to `sdsys` alone; an administrator — a
real `sdsys` login — writes it directly. Both follow the same visible
process from the terminal; only what happens underneath differs, and only
because the account writing its own record has no other way to reach a
file it does not own.

**SDSYS's own *Linux* login password is a separate thing** — set once,
during installation (`sudo passwd sdsys`), and changed afterward the
ordinary Linux way, not with this verb.

## Continued in

[Account Maintenance](01a-account-maintenance.html) — clean.account,
update.accounts, [locked], config, set.date and delete.account.

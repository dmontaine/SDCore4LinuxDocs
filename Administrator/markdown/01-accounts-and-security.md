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

> **Anything you put in the `shared` account can be read by every account,**
> by file name, with no `logto` and no pointer, **unless you type
> `shared-read-off` for an account.** The installer makes the `shared` account;
> every account, new or old, starts with the right to read its files, and
> without the right to write them. This is the one right here that is on until
> you take it away. See *The shared account*, below, and
> [The shared account](13-the-shared-account.html).

## Read this before anything else: being SDSYS is the whole of it

**Having the verb is not having the right to use it — and there is exactly
one gate, one route in, and nothing that widens it.** Every verb on this
page is refused outright to any session that is not actually SDSYS:

```
:modify.account fred suspended
Command requires administrator privileges
:delete.account sdsys
Command requires administrator privileges
:modify.password sdsys
Command requires administrator privileges
```

**Every one of those refusals came before the command was looked at.**
`delete.account sdsys` would have been refused anyway — you cannot delete
`SDSYS` — and it never got that far.

**A gate is a wall for an SD *session*, not for a person who has a shell on the
machine.** Every SD user is in the operating-system group `sdusers`, and a
member who has a shell can write SD's shared memory (the lock, file and user
tables): such a person can release other people's locks or log sessions out,
which is damage and denial of service, not a way to become SDSYS or to turn a
gate on. How far that matters, and how an installation that cannot accept it
closes it, is in [SD installation](08-sd-installation.html), *What this does
not close*.

**Being SDSYS means being logged in to the machine as the `sdsys` Linux
user, at its own password, on a local session** — the keyboard, or a
desktop-sharing view of it (VNC, TeamViewer). Nothing else grants it:

| route | result |
|---|---|
| a real login as `sdsys`, local | granted |
| `sudo sd` as root | refused — root is treated as *another* administrator, not SD's |
| `sudo -u sdsys sd` / `su - sdsys` | refused — the session runs as the `sdsys` Linux user, but the login that started it was somebody else's, and the kernel's own audit trail (unforgeable without root) says so |
| `sdsys` over ssh, as delivered | refused at the door |
| `sdsys` over ssh, after the administrator has opened that door (`remote.sdsys on`) | asked for the password, which is then all that stands between the network and the administrator — see [Remote Administration over ssh](22-remote-administration-over-ssh.html) |
| `sdsys` over the API from another computer or the network port | refused at the door — the API is never a remote route for SDSYS |
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

**SDSYS may be signed on in more than one place, and when it is you can see it.**
Nothing stops a second terminal window or a
second local login of the `sdsys` user from starting `sd`, and one reason to
want that is recovery: a session that is stuck at a page can be ended by
`logout` from another. A limit of one would lock the administrator out until
`sd -cleanup`. So the second session is made visible, three ways:

| where | what it shows |
|---|---|
| the audit trail | one line, `sdsys second session others=<n>`, written by a session of SDSYS that signs on while *n* other sessions of SDSYS are on a terminal (after the `login account=sdsys` line it writes as always) |
| `tool.sessions` | each of those rows says `sdsys x<n>` in its State column, the counts line says `SDSYS in <n> places`, and the box under the list says so for the row under the cursor |
| the home screen | the Sessions and locks tile says `<m> signed, <n> sdsys` in place of `<m> signed on` |

What counts is a session of the account `sdsys` that is **on a terminal**: a
phantom, an API or SDNet process, a session being logged out, and a session with
no terminal (a piped `sd 'command'`, `sd -internal`, a program started from a
script) are not counted and write no line, because they are not a second person
at the machine. Seeing the second session is not the same as stopping it; the
audit line and the page are how you notice one you did not expect.

**What the `sdsys` Linux user can write.** **As delivered, the `sdsys` user is a
member of the Linux group of every user account** (`sdu_`*name*), so SDSYS has
read and write access to everything in the `/home/sd` tree that an account's
group may write: the VOC, the dictionaries, the programs in `bp` and `bp.out`,
the catalog `cat` and the data files. That is how SDSYS compiles, catalogs
and debugs the programs of an account whose own `bp-edit` gate is off, and how
`tool.entries` edits an account's VOC entries and dictionary items in place (see
[The master files](19-the-master-files.html)). It is a deliberate default for a
system that has to stay simple to run: **how much further protection the
machine needs, from a locked room to operating-system permissions, is the
administrator's to decide.** `modify.account` *name* `sdsys-off` takes the
user out of one account's group, and `sdsys-on` puts it back (below).
**While it is on, the `sdsys` user has write access to everything the
account's group may write**, and a VOC entry or an I-type is code that runs in
the account: someone who took over the `sdsys` login could change what that
account runs. It is not reachable from the network (`sdsys` has no API access
from it, and ssh only when the administrator opens that door), and a process that is not a
real login as `sdsys` is not an administrator. **The membership is a default
and a record of your decision, not a wall against a stolen `sdsys` login**,
which has other ways into an account's code: the global catalog is the
`sdsys` user's to write, and `sdsys` may run `sudo /usr/local/sbin/sd-elevate`
with any arguments. (The files `root` runs at the next start are not
`sdsys`'s to write: they belong to `root`, see
[Installation and the daemon](08a-sd-installation-file-modes-and-root-files.html#the-files-root-runs).)
An install puts the `sdsys` user in the group of the
registered accounts that are already there **once** and records that in
`/home/sd/$sdsys.access`; after that a `sdsys-off` you gave stands.

### The sdsys user in an account's group: `sdsys-on` and `sdsys-off`

`modify.account` *name* `sdsys-on` puts the `sdsys` user in the account's
Linux group and makes the account's VOC and dictionaries writable by that group;
`sdsys-off` takes the user out. The state is the group membership, as it is for
`ssh` and the API, so nothing is written to the register. The lines printed are
`Account fred: sdsys-on done. ...` and `Account fred: sdsys-off
done. ...`; the audit trail has `modify.account sdsys-on account=fred`, and
`sd-elevate` writes a line to the system log. **User accounts only**: a group
account is refused ("is not a user account"), because `sdsys` owns the files of a
group account. `sdsys-on` can be given again to an account that is on, which
repairs the modes and changes nothing else; `sdsys-off` for an account that is
off changes nothing. The two words conflict only with each other. **A session of
SDSYS that is already running keeps the groups it started with**: sign on again
after `sdsys-on`, and after `sdsys-off` that session still has the write until
it ends. `create.account` and the installer switch it on for a new account.

## Continued in

[Accounts and Security: Making an
Account](01-accounts-and-security-2-making-an-account.html) — create.account,
the sh-on, os-on and sd-on switches.

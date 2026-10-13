Title: Operating System Access
Subtitle: The `sh` and `!` verbs, and the per-account switch that decides who may use them.

`sh` runs a Linux command from the SD prompt. `!` is the same verb under a
shorter name. **Each account has its own switch for them, `sh-on`, and a new
account does not have it** — SDSYS turns it on, account by account, with
`modify.account`. Without it both verbs refuse.

> **This document is separate so that it can be withheld.** It links to
> nothing outside the administrator set. Where a user-set page is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case.

> **The listings below were produced by running them**, on a build of SD Core
> for Linux made from the tree, in an account that had `sh-on`.

## The two verbs

```
sh command
! command
```

Everything after the verb is the command. It runs in the account's own
directory, at the account's own Linux permissions:

```
:sh echo hello-from-the-shell
hello-from-the-shell
:! echo via-the-bang-form
via-the-bang-form
:!echo no-space-needed
no-space-needed
```

**There is no interactive shell at the prompt.** A bare `sh`, with nothing
after it, is refused with the same "Error 2" as below, so a script, a phantom
or a scheduled job that types it does not hang waiting for somebody at a
keyboard. For a session of your own, use the local login.

## One rule about the shape of the command, for both verbs and for everybody

**Both verbs refuse a command that contains `;`, `|`, `&`, `$`, a backquote,
`<`, `>` or a newline**, before anything runs:

```
:sh echo alpha-beta | grep alpha
Error 2 executing operating system command
:sh echo gamma > zzsh.txt
Error 2 executing operating system command
```

That is a sanitizer on what a one-line command may look like — a safety
measure against an accidental injection, not a permission — and it applies
to every account, SDSYS included, whether or not the account has `sh-on`. So
**no pipe, no redirection, no chaining and no variable expansion is available
from the prompt.** What an account that has the switch can do about that is
the obvious thing: write the work into a script file and run the script
(`sh ./nightly`). The script's own contents are not filtered. This is why
`sh-on` is a decision to give a person a shell on the machine, not a
decision to give them a restricted one.

## Who is allowed: a switch in the account's own record

**The permission is a field of the account's own register record** — field 7,
`yes` or `no` — and not a tier and not a file of names. Anything other than
`yes` means no, and a record that never had the field means no. It is written
by `create.account` (`sh-on`) and changed by `modify.account` *name* `sh-on` /
`sh-off`; each reports where the account now stands, both switches at once:

```
:modify.account fred sh-on
Account fred has SH yes, OS.EXECUTE no
```

**The switch is read when a session signs in or `logto`s into the account**,
so a change reaches the account the next time it is entered. A session that is
already open keeps what it started with. To take the shell from somebody who is
signed in now, change the switch and then end their session.

| | `sh` and `!` |
|---|---|
| the account has `sh-on` | runs the command, subject to the rule above |
| SDSYS | runs it, whatever the register says |
| anybody else | refused, and the command is never looked at |

```
fred is not permitted to use the operating system shell
```

is message 10053 and names the Linux user, who is the account's own user.

## What this does not gate

**A program's `OS.EXECUTE` is not on this path**, and neither are the screen
editors, the embedded Python, or reaching an operating-system file by its path.
They are governed by the other switch, `os-on`, which is independent: `sh-off`
leaves it alone, and an account can be refused the shell and still run
`nano`. See [Accounts and
Security](01-accounts-and-security.html#the-operating-system-switches-sh-on-and-os-on)
for everything `os-on` covers.

**The form that does go through this gate is `execute 'sh …'` from a program**,
because that runs the TCL verb.

## Over the API

**A session that arrived over the API is held to the same switch**: the API
server reads the account's `sh-on` and `os-on` when it enters the account, as
sign-in and `logto` do, so an account with `sh-on` has the shell over the API
and an account without it is refused there too. **That is what makes `sh-on`
on an account that also has the API route a shell behind its credential from
wherever the API port is reachable** — see *What `os-on` actually costs* in
[Accounts and Security](01-accounts-and-security.html). SDSYS over the API is
the exception to the exception: an API session carries no administrator flag,
and SDSYS's own record holds no switch, so it has no shell over the API; use
the local login. See also
[Remote Access and the Machine](05-remote-access-and-the-machine.html).

## Who has these verbs

`sh` and `!` are in every account's VOC — there is no tier to withhold them.
**Having the verb is not having the permission**: an account without `sh-on`
has the verb and is refused by it.

## SDSYS's own shell

**SDSYS reaches `sh` the way it reaches everything else — as the `sdsys` Linux
user, on a session that is already a real local login** — see [Accounts and
Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it).
Reaching SDSYS at all means being at the console, or a desktop-sharing view
of it: `sdsys` is denied ssh and network sign-in outright, so there is no
remote session for this to ever apply to.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Sessions and Locks](02-sessions-and-locks.html) ·
[Remote Access and the Machine](05-remote-access-and-the-machine.html).

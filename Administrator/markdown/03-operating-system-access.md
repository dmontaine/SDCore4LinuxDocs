Title: Operating System Access
Subtitle: The `sh` verb, and the per-account switch that decides who may use it.

`sh` runs a Linux command from the SD prompt. (The `!` form, a shorter name for
the same verb, was removed on 28 October 2026: write `sh command`.) **Each
account has its own switch for it, `sh-on`, and a new account does not have
it** — SDSYS turns it on, account by account, with `modify.account`. Without it
the verb refuses.

> **This document is separate so that it can be withheld.** It links to
> nothing outside the administrator set. Where a user-set page is worth naming,
> it is named in words.

**The switch is a wall for an SD *session*.** A person who already has a Linux
shell on the machine does not need it; what such a person can and cannot do to
SD is in [SD installation](08-sd-installation.html), *What this does not
close*.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case.

> **The listings below were produced by running them**, on a build of SD Core
> for Linux made from the tree, in an account that had `sh-on`.

## The verb

```
sh command
```

Everything after the verb is the command. It runs in the account's own
directory, at the account's own Linux permissions:

```
:sh echo hello-from-the-shell
hello-from-the-shell
```

**A bare `sh`, with nothing after it, starts an interactive shell** (the
filter below is for a typed command; until 7 November 2026 it refused an empty
one too, with the same "Error 2"). `exit` brings you back to the SD prompt. It
needs the account's `sh-on` switch like any other `sh`: an account without it is
refused first, with "<name> is not permitted to use the operating system shell".

## One rule about the shape of the command, for everybody

**The verb refuses a command that contains `;`, `|`, `&`, `$`, a backquote,
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

| | `sh` |
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
`micro`. See [Accounts and
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

`sh` is in every account's VOC — there is no tier to withhold it.
**Having the verb is not having the permission**: an account without `sh-on`
has the verb and is refused by it.

## SDSYS's own shell

**SDSYS reaches `sh` the way it reaches everything else — as the `sdsys` Linux
user, on a session that is already a real local login** — see [Accounts and
Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it).
Reaching SDSYS at all means being at the console, a desktop-sharing view
of it, or — only once the administrator has opened that door — an ssh sign-in with the
`sdsys` password (see [Remote Administration over ssh](22-remote-administration-over-ssh.html)):
until then `sdsys` is denied ssh and network sign-in outright.

## The documentation in the shared account

```
docs.install directory
load.help
```

**SD starts no program for an account whose `os-on` and `sh-on` are off: there is no
exception.** The documentation PDFs are files in the `pdf` directory of the shared
account, which every account may read. A person reads one by copying it to their own
computer (`scp`, or any file-copy tool), or, at the machine itself, by opening it with
a reader they run themselves. A help box that has more in the documentation names the
PDF on its last line, exactly as it is named in the `pdf` directory: the book comes first,
then the chapter (`administrator-01-accounts-and-security.pdf`; the books are `user`,
`administrator` and `gettingstarted`).

### Where the documents come from: `docs.install`

The PDFs are generated from the documentation and are not part of the source tree.
**A release package carries them**, in a folder `pdf` beside `installsdcore.sh` (one PDF
for each chapter of the User, Administrator and Getting Started documents, the documents
the help pages name), and **the installer puts them in the shared
account by running `docs.install` on that folder**, then gives the copies to `sdsys`,
group `sdusers`. It checks each document on the shared folder afterwards and, when one
did not arrive, says how many did and prints the command to run. An installer run
without a package (a clone, or the script downloaded alone) finds no folder and says
so. At any other time, or for documents of your own, the administrator runs:

```
docs.install /path/to/the/pdf/files
```

copies every `*.pdf` of that directory into the `pdf` directory of the shared account
(which the installer makes, owned by `sdsys`, group `sdusers`, mode 755: **no SD user
can add a document there**). A file is copied only if its name is lower case letters,
digits and `. _ -`, ends in `.pdf` and does not begin with a dot, and the file begins
with `%PDF-`; anything else is skipped and named. A document already there is replaced;
the copies are mode 0644.

**The changes document comes with the installer.** A release package holds, beside
`installsdcore.sh`, the document that lists what changed in the release as
`sd-core-for-linux-<version>-changes.pdf`, `.html` and `.md`. The installer copies each
of those three into the same `pdf` directory (owner `sdsys`, group `sdusers`, mode 644),
so every account can read it, and the HTML and Markdown copies are there beside it. A file is copied only if it is a regular file (not a link) with a
plain lower case name of the same shape; a file of that kind whose name has a capital
or another character is left, with a note that says so. An installer that was not run
from a package, such as one downloaded alone, finds nothing and says so; the install
goes on.

### The context help: `load.help`

The `[?]` button on the administrator's pages shows help kept in the file `context.help`
of the shared account, one record to a setting. The installer fills it from the text under
`helptext` in the SD system directory; `load.help` does the same by hand, after that text
changes (it enters the shared account, writes the records that differ, and returns to the
account it began in). **It replaces the shipped records and keeps any you added** under
another id (the count says how many). Reading the help is not gated: the text is the
product's own documentation of its screens, so an account whose `shared.read` you withdrew
still gets it, and SDSYS, whose own `OPEN` does not follow `shared`, does too.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Sessions and Locks](02-sessions-and-locks.html) ·
[Remote Access and the Machine](05-remote-access-and-the-machine.html).

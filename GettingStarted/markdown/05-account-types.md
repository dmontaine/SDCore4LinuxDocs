Title: Accounts
Subtitle: Ordinary accounts, SDSYS, Suspended and Group — what each one may do, and how to make one.

**Every ordinary account gets the same VOC.** SD Core used to divide accounts
into three capability tiers — Standard, Programmer, Administrator — each with
a different, smaller VOC. **The tiers are gone**: the only privileged account is SDSYS. An account you create today
gets every verb there is, the same set SDSYS has for running applications and
building them. What it does **not** get is administration — that is not a
verb an account can be given, it is a separate account.

**Suspended** is a state, not a tier — it denies entry and nothing else. Group
accounts are a different thing again: a shared place, not a person.

## SDSYS is the only administrator

**SDSYS is a single Linux user made by the installer, not something
`create.account` can produce.** Administering SD — creating, deleting or
changing an account, changing system-wide state, reaching another account's
files without a grant — means logging in to the **machine itself**, locally,
as `sdsys`, at its own password, and running `sd`. There is no elevation
step because being logged in as `sdsys` already *is* the privilege: `sudo`,
`su`, or any route into the `sdsys` account other than a genuine login is
refused, checked against the kernel's own audit trail (which records who
actually logged in, not which account a shell is currently running as).

> **This matches SD Core for Windows's own model exactly at the result
> level**, even though the mechanism differs (a real login vs. elevation
> checked against the running session). Neither port lets an administrator
> of the underlying operating system pick up SD privilege by virtue of
> that — being a Linux `sudo`er, like being a Windows administrator,
> grants nothing by itself. The reasoning is in the *Administrator* set's
> *Accounts and security* chapter.

**SDSYS's Linux login password** is set once, during installation
(`sudo passwd sdsys`) — that is what you type at the machine's own login
prompt to reach it at all, and changing it afterward is an ordinary Linux
action (`passwd`), not an SD verb. SDSYS also has its own SD credential
(`modify.password`, run from within an SDSYS session, changes its own),
but that credential secures nothing remote: `sdsys` has no ssh access at
all and no API access from another computer, under any setting. The one
thing the credential is for is a program running as `sdsys` on this machine,
which gives it to use the API through the local Unix socket — see
[API access](09-api-access.html). For what an administrator cannot reach
from SD, see [Reaching the operating system](06-administrator-commands.html).

## Creating an account

```
create.account user <name> {ssh | api | both | none} {sh-on} {os-on} {voc-on} {bp-on} {dict-on} {files-on} {no.query}

create.account group <name> {no.query}

create.account other <name> <pathname> {no.query}
```

**Creating an account needs a real SDSYS session.** Creating a Linux user
account needs root, and only a genuine login as `sdsys` carries the
identity SD's own elevation helper checks before granting it — see
[SDSYS is the only administrator](#sdsys-is-the-only-administrator) above.

### A new account starts with every door shut

**A new user account has no ssh, no API, no `sh` and no `OS.EXECUTE`, and it
cannot save a change to a VOC, a program file or a dictionary,** until
SDSYS turns each one on. SD is delivered with the tighter setting and the
administrator loosens it, account by account, for the people who need it:

| word | gives the account |
|---|---|
| `ssh` · `api` · `both` | the remote route(s). `none` is the default |
| `files-on` | the files-only API route: an API login that can open, read, write and select from files and do nothing else (no commands, no subroutine calls, no `logto`). `api` gives the whole API and wins when an account has both |
| `sh-on` | the `sh` verb |
| `os-on` | `OS.EXECUTE`, `micro`, the embedded Python, and files or directories of the operating system named by their path outside the account's own directory |
| `voc-on` | saving a change to the account's VOC |
| `bp-on` | saving a change to a program file (`bp`, `bp.out`, `*.bp`, `*.bp.out`), and compiling and cataloguing. A new account needs it before it can save or compile its first program |
| `dict-on` | saving a change to a dictionary (a file whose name ends `.dic`) |

`sh-on`, `os-on` and the three edit switches are independent of each other
and of the routes. The same words change an account afterwards in
`modify.account` — see [Managing accounts](05a-managing-accounts.html), which
has a section on the edit switches. **No new account is an
exception — not even the one the installer creates for whoever installed
SD on a fresh machine**; the accounts that keep their shell, `OS.EXECUTE` and
edit rights are the user accounts that already exist when the installing user
upgrades. SDSYS has no remote access at all, and that
is not a setting.

### What creating a user account actually does

| | |
|---|---|
| Makes a Linux user account | `useradd -m`, password locked until SD sets it |
| Creates the group `sdu_<name>` | and writes it to the account record, with `root` and the user in it. **The `sdsys` user is not in it as delivered**: `modify.account` *name* `sdsys-on` puts it there, so that SDSYS can change the account's VOC and dictionaries by saving their master records (that gives the `sdsys` user write access to everything the group may write), and `sdsys-off` takes it out. (A group account's group has `root` and `sdsys`: `sdsys` owns its files.) |
| Joins `sdusers` | which is what grants access to the data tree, and is what the ssh boundary matches against |
| Prompts for a password | in SD, masked; it never goes on a command line |

**A user account cannot be created without a password.** Refusing the
prompt creates nothing at all.

**Joining `sdusers` is what makes an account an SD account; the routes are
more groups.** Every `sdusers` member is `ForceCommand`'d into `sd` over
ssh, and an account reaches `sd` over ssh only if it is also in `sdssh`, and
over the API only if it is in `sdapi` — those two memberships are what the
`ssh`, `api`, `both` and `none` words make and take away. A third group,
`sdfiles`, is a narrower API route that reaches files and nothing else; the
`files-on` and `files-off` words make and take it away, and `ssh`, `api`,
`both` and `none` leave it alone. `sdsys` is in
none of them, and is refused at the door on both routes rather than left
ungranted.

### What every account can do

**Every verb, from the moment it is created.** Compile, catalogue, edit,
define files and indexes, run the bulk record editors, inspect processes —
none of that is withheld. What an account cannot do is administer: create,
delete, or suspend another account; change system-wide configuration. And
reaching the operating system — the `sh` verb, `OS.EXECUTE`, `micro`,
the embedded Python, a file or directory of the operating system
by its path outside the account's own directory — takes the switch above:
see
[Security and the operating system](12a-security-and-the-operating-system.html#the-shell-and-operating-system-access-are-per-account-switches).

> **The VOC is the same for every ordinary account and is not the wall.**
> What stops one account reaching another's data is the operating system's
> own file permissions and the ssh confinement, and — for the verbs and
> statements that name an operating-system path — the account's `os-on`
> switch. See the *Administrator* set's *Accounts and security* chapter.

## The `shared` account

**One group account, named `shared`, exists on every installation.** The
installer makes it; you do not create it, and nobody can create or delete an
account of that name. **Its data files can be opened by every account by
file name** — `open "inventory"` finds the file `shared` holds under that
name, with no `logto` and no pointer in your VOC — unless your own account
already has an entry of that name, which always wins.

**Reading is on for every account; writing is off.** Two per-account
switches, `shared-read-on` / `shared-read-off` and `shared-write-on` /
`shared-write-off`, are SDSYS's to change. Without `shared-write-on`, an
attempt to save, delete or clear a record in a shared file is refused, and
changing the *structure* of a shared file (clearing it, configuring it,
indexing it, deleting it) is SDSYS's alone, at a terminal on the machine.
The verbs, programs and catalogue of `shared` are not shared: only its data
files and their dictionaries. **Nobody but SDSYS signs on to `shared`.**
Because every account can read it, put nothing there that is not meant for
everyone.

## Suspended — a state, not a tier

**A suspended account cannot be entered.** It is for an account that should
stop working for a while — somebody on leave, a login being looked into —
and it is refused at all three ways in:

| | |
|---|---|
| ssh, or the console | `Account FRED is suspended` |
| **`logto`** from another account | `Account FRED is suspended` |
| the API | `User not allowed in requested account` |

The API wording is deliberately the same one it gives for an account that
does not exist and for one you are not granted, so the API cannot be used to
find out which accounts exist or what state they are in.

**It takes nothing away, which is why lifting it is free.** The VOC is left
exactly as it is and no group membership moves — suspending sets one
field and unsuspending clears it. Suspending is not a substitute for
deleting: it is reversible on purpose. See
[Changing an account afterwards](05a-managing-accounts.html#changing-an-account-afterwards).

**SDSYS can still `logto` into a suspended account.** That is deliberate —
looking at a suspended account is the usual reason to have one. **What a
suspension denies is the account's own user.**

## Continued in

[Managing accounts](05a-managing-accounts.html) — group accounts, sharing
one, changing an account afterwards, and deleting it.

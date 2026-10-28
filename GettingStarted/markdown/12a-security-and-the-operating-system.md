Title: Security and the operating system
Subtitle: Reaching the machine from inside SD, how privileged work is done, and the audit trail.

This page continues [Security](12-security.html).

## The shell and operating-system access are per-account switches

**SD is delivered with the ways out of SD shut, and the administrator opens
them one account at a time.** A new user account has none of these until
SDSYS turns it on (`modify.account` *name* `sh-on` / `os-on`):

| | What it is | The switch |
|---|---|---|
| **`sh`** and `!` | a shell at the `:` prompt | `sh-on` |
| `OS.EXECUTE` | the operating system from inside a BASIC program | `os-on` |
| **`micro`** | a text editor, running outside SD | `os-on` |
| the embedded Python | arbitrary code in the account's own process | `os-on` |
| a file or directory of the operating system **by its path**, outside the account's own directory | `OPENSEQ` and `OPENPATH` with a path, `DIR()` and `select.dir`, `DELETESEQ` of a path, `!OSCOPY`, `!IOSCOPY` and the `oscopy` verb, `sed` given a `path:` name, printing into a file by path | `os-on` |

`sed` and `ced` are not in the table: they run inside SD, so editing a record of
an SD file needs no switch. `sed` asks the `os-on` question only for a `path:`
name outside the account's own directory (the last row).

The two switches are independent: `sh-off` leaves `OS.EXECUTE` alone, and
the reverse. A change reaches the account the next time it is entered.
**SDSYS is never refused**, and no other account is an exception — the one
the installer makes for whoever installed SD starts off too, and the
installer tells them how to turn it on. When you upgrade, the installer
switches both on, once, for every account that already exists, so nobody
loses a command they were using; you can then turn them off account by
account.

**Without a switch SD says so in words** — "*name* is not permitted to use
the operating system shell", "*name* is not permitted to use OS.EXECUTE", or
"*name* has no OS access, so a file or directory outside its own account
cannot be reached by pathname (SDSYS can give it: `modify.account` *name*
`os-on`)" — and a program is told with status 3035, so `OPEN ... ELSE` and
`DELETESEQ ... ELSE` take their ELSE as for any other refusal.

**What an account without `os-on` still has** is everything that stays
inside SD: every file its VOC names (dictionaries and other SD files
included) and anything inside its own directory. A path is judged by its
**real** path, so `..` and a symbolic link that points out of the account do
not get round it.

**A VOC pointer is held to the same rule.** A file pointer in an account's
VOC must lead inside the account (or be one of the pointers SD itself puts in
every VOC), so a pointer written by hand at `/etc` or at another account's
directory is refused, status 3035, unless the account holds `os-on`. **A
Q-pointer into another account is followed only if you could `logto` that
account** — whether or not you hold `os-on`. The Administrator set's
*Accounts and security* chapter has the full rule.

**What the switches do not do.** They stop SD handing the operating system to
an account that has not been given it. They do not change what the account's
Linux user may do — that stays whatever Linux says, checked by the kernel.

> **When you do turn `sh-on` or `os-on` on, you are giving that person a
> shell on this machine as their own Linux user.** An editor can open any
> file the account may open, in the data tree or outside it. Set the
> account's Linux permissions deliberately, the way you would for any other
> user with a shell — and think twice before giving it to an account that is
> also reachable from outside (`ssh`, `api`), because then the shell is
> behind that account's credential from wherever the route reaches.

**A session with no terminal is refused for the editors regardless** — an API
session or a piped script has nowhere to draw a full screen for an editor;
see [API access](09-api-access.html) for what `sh`/`OS.EXECUTE` do over the
API, which takes the same switches.

## Privileged work is done through a helper, not a raw command line

When SD creates an account, sets a password or edits a group, it does not
build a shell command containing a password or run one as an arbitrary
string. **`sd-elevate`**, a `sudo`-scoped helper installed to
`/usr/local/sbin`, is the only thing an SD session can reach with root's
help — and it re-derives the legality of each request itself (whose
account it is, what the operation actually is) rather than trusting what
SD's own session claims.

**A credential is never an argument.** Where a password has to reach the
helper — setting an account's own SD password, for instance — it goes to
`sd-elevate` on **stdin**, through a file in a private, mode-`0700`
directory that only the calling session can read, never on a command line
where any local user could see it through `ps`.

**If `sd-elevate` is missing or refuses, SD refuses the privileged work**
rather than falling back to doing it unprotected. You see the command
fail rather than quietly running with less protection than intended.

## The audit trail

`/usr/local/sdsys/audit` records **every login, every refused login, every
`logto`, every refused `logto`, and every `modify.account add`/`delete`**,
with date, time and the Linux user it belonged to.

```
2026-10-07 21:07:52 user=don uid=3 pid=353011 login account=sdsys
2026-10-07 21:07:52 user=don uid=3 pid=353011 logto refused account=sdsys reason=sdsys is entered by its own session only
```

Every word before the first `=` is lower case, the event names included
(`login`, `logto`, `logto refused`, `api refused`, `elevation granted`,
`modify.account route api`). What follows an `=` is data and keeps its case:
the account name as it is registered, a `reason=` text, and what a caller
typed in `command=`. Older lines in a file written before 7 October 2026 are
upper case and are not rewritten, so match without regard to case when you
search a long-lived file.

**An account's gates are on the trail whenever they are given.** `modify.account`
writes one line for each word it carries out (`modify.account sh-on account=fred`;
several words in one command give several lines), and, since 19 October 2026,
`create.account` records the gates it granted at creation as well:

```
2026-10-19 15:35:26 user=sdsys uid=1 pid=8326 create.account account=witm1 type=user gates=sh-on,os-on,files-on,files-write-on
2026-10-19 15:35:27 user=sdsys uid=2 pid=8614 create.account account=witm2 type=user gates=none
```

`gates=` lists, in lower case, every access the new account was given, always
in this order whatever order the words were typed: `ssh`, `api`, `sh-on`,
`os-on`, `voc-on`, `bp-on`, `dict-on`, `net-on`, `files-on`, `files-write-on`,
`files-admin-on`, `shared-read-off`, `shared-write-on`. It says `none` when there is none. The
line is written only after the account has been made: a creation that is
refused (an empty password, say) leaves no line. (An older line,
`create.account account=jane type=user`, names none: read the `modify.account`
lines after it.)

**The refusals are the interesting half.** An entry saying somebody who is
not SDSYS asked for SDSYS by name, or asked for an account they have not
been granted, is the thing worth seeing. **Failed API logins are recorded
too, with the reason** — and **before** the three-second wait SD adds to slow
down guessing, so a program that hangs up during the wait is recorded as well.

**This is not the error log and does not behave like it.** The error log
throws away its oldest half when it fills; the audit file is **rotated —
renamed with the date and time and a new one started at boot, so nothing
is ever discarded within a run.** Removing the old ones is your decision —
SD will not do it for you, and they will accumulate.

**The file itself is append-only at the kernel level** (`chattr +a`), lifted
only by root at the one moment a new file starts, so an SD user cannot
remove or edit an entry even with the write permission to add to it — the
protection is a Linux filesystem attribute, not merely a permission bit.

| SD users can | SD users cannot |
|---|---|
| **add** to it | read it, change a record in it, empty it, rename or delete it |

**The kernel refuses the edit or the delete, not SD**, so a user cannot
quietly remove the line that records what they did. SDSYS can read it and
do anything else to it as well — a real login as `sdsys` can lift the
append-only attribute, the same as any root-equivalent action, so this
raises the floor against ordinary users rather than trying to constrain
the machine's own administrator.

## What is still not true

**SD accounts are not isolated from each other's data at the file level
beyond whatever this machine's own Linux permissions provide.** Everyone
who uses SD needs file access to the tree, because their own process does
the I/O. Anyone deploying SD for ten people over ssh should be told that
plainly — see [Security](12-security.html#your-own-accounts-data).

**SD has no file-level access control of its own** on the console and ssh
paths. The one place a path gate does exist is the API, where a session is
confined to the account it stands in — see
[API access](09-api-access.html#a-session-is-confined-to-its-own-account).

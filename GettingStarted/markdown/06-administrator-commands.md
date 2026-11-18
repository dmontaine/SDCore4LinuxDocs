Title: Administrator commands
Subtitle: The verbs only SDSYS has, and how to use them.

**These verbs are not in an ordinary account's VOC at all.** Every ordinary
account gets the same VOC
— see [Accounts](05-account-types.html) — and administration is not a verb
an account can be given. It is SDSYS, a single Linux user the installer
makes, reached by logging in to the machine itself, locally, as `sdsys`,
its own password, and running `sd`. Typing one of these verbs from any
other account says it is not recognized, not that you lack permission for
it.

## Accounts

```
create.account  user <name>
create.account  group <name>
delete.account  <name> {remove.home}
modify.account  <name> add|delete <user>
modify.account  <name> ssh|api|both|none
modify.account  <name> sh-on|sh-off
modify.account  <name> os-on|os-off
modify.account  <name> voc-on|voc-off
modify.account  <name> bp-on|bp-off
modify.account  <name> dict-on|dict-off
modify.account  <name> files-on|files-off
modify.account  <name> suspended|unsuspended
update.accounts {all}
clean.account
```

The `modify.account` lines above are the ones this set describes; it has
more words (`xfer-on`, `ai-on`, `net-on`, `recovery-on`, `shared-read-on`,
`sdsys-on` and others), and typing `modify.account` with an account and no
word prints them all. Covered in full in [Accounts](05-account-types.html) and
[Managing accounts](05a-managing-accounts.html). The points worth repeating
here:

- **A new account has no ssh, no API, no `sh` and no `OS.EXECUTE`, and it
  cannot save a change to a VOC, a program file or a dictionary.**
  `ssh`, `api`, `both`, `sh-on`, `os-on`, `voc-on`, `bp-on` and `dict-on` give
  them, at `create.account` or later with `modify.account`. SDSYS's two remote doors
  are not among these settings and are shut as delivered: its ssh door opens only when the
  administrator runs `remote.sdsys ssh on`, and its API door from another computer only
  when the administrator runs `remote.sdsys api on` *address* (see below).
- **`modify.account add`/`delete`** is the grant — Linux group membership,
  with SD's own audit line on top. There is no separate `grant`/`revoke`
  pair of verbs.
- **`modify.account` says what the access *is*, not what to add.**
  `modify.account fred api` gives Fred the API and takes ssh away; `both` gives both.
- **`modify.account` takes several actions in one command**
  (`modify.account fred sh-on os-on`); it reads and checks them all first and changes
  nothing if any word is refused.
- **`suspended`/`unsuspended`** is a state, not a tier — nothing about the
  VOC moves either way, because every account's VOC is the whole of `newvoc`
  regardless.
- **`update.accounts`** adds the VOC records it finds missing, from a
  release that shipped verbs the account was created before, and removes the
  records on SD's deletion list (the ones a release has stopped shipping),
  saving a copy of each first. Since every
  account already has the whole VOC, this now matters only after an
  *upgrade* — a fresh account never needs it, and **the installer runs
  `update.accounts all` for you** when you keep your accounts.
  **`list.voc.removed`** shows the list and **`restore.voc`** puts a removed
  record back.
- **`delete.account`** keeps the Linux user's home directory unless you
  add `remove.home` — a person's own files and ssh keys live there.

**`clean.account`** tidies an account's workspace. **`update.accounts`** is
the one you run in each account after upgrading SD.

## Passwords

```
modify.password {<account>}
```

**A password cannot be typed on the command line.** **`modify.password`**
refuses one given as an argument. A password on a command line is visible to
any local user through `ps`, so SD prompts for it instead, masked.

Run with no argument it changes your own; from SDSYS, naming an account
changes that account's — every account, including SDSYS's own. The password
matters for **API logins only**. Console and ssh logins ask for nothing —
see [Security](12-security.html).

**SDSYS's *Linux* login password is a different thing entirely** — set
once, during installation, and changed afterward the ordinary Linux way
(`passwd`), not with this verb. See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

## Locks and sessions

```
lock / unlock
list.locks / clear.locks
listu / list.readu
logout
```

**`unlock` is the one to know about.** It clears a record lock left behind
by a session that died holding one. Without it the only way to release such
a lock is to stop and restart SD, which disconnects everybody.

**`listu`** and **`list.readu`** report sessions and read locks; **`logout`**
ends another session.

## System state

```
config
set.date
```

**`config`** reports the configuration parameters in force. **`set.date`**
sets the date *this session* sees, for testing date-dependent programs; the
machine's clock and every other session are untouched.

## The remote doors

```
remote.api on | local | off
remote.ssh on | off
remote.sdsys ssh on | off
remote.sdsys api on <address ...> | off
umask {mask}
```

These set up the machine's own remote-access surface rather than any
one account's — see [ssh access](08-ssh-access.html) and
[API access](09-api-access.html) for what each one does. **`remote.sdsys` opens
or shuts SDSYS's own two doors, and both are shut as delivered.** Opening one
means that nothing but `sdsys`'s password then stands between the computers
allowed in and the administrator: its ssh door is guarded by the Linux password and
its API door, which names the addresses it admits, by SD's own password for SDSYS.
The Administrator set's chapters on remote administration say what each risks. There is no
`ssh.server`/`append.sd.path` pair here: SD Core does not manage an ssh
server as an installable feature (the distribution's own package does that)
and puts `sd` on `PATH` at install time rather than as a toggle.

## The shell — `sh`

**A new account cannot use `sh` or `OS.EXECUTE` until you say so.**
Each is a per-account switch, off at creation, that SDSYS turns on and off
with `modify.account` *name* `sh-on` / `sh-off` (the `sh` verb) and
`os-on` / `os-off` (`OS.EXECUTE`, the editor `micro`, the
embedded Python, and operating-system files by path outside the account's
own directory). The two are independent, and each reports where the account
now stands ("Account fred has SH yes, OS.EXECUTE no"); a change reaches the
account the next time it is entered. **What the shell can then do is exactly
what that account's Linux user may do** — it runs at that user's own Linux
permissions, never as root. SDSYS is never refused. See the *Administrator*
set's *Accounts and security* chapter, "The operating-system switches:
`sh-on` and `os-on`".

**`sh` runs one command at a time, and refuses a command that
contains `;`, `|`, `&`, `$`, a backquote, `<`, `>` or a newline** — "Error 2
executing operating system command", before anything runs. That is a safety
measure against an accidental injection in a one-liner, applied to every
account whether or not it has `sh-on`, SDSYS included. **There is no pipe,
redirection or chaining from the prompt** (a bare `sh`, with nothing after it,
does start an interactive shell for an account that has `sh-on`; `exit` brings
you back); put the work in a script and run the script, `sh ./myscript`.

### Over the API they follow the same switches

**An API session reads the account's `sh-on` and `os-on` when it enters the
account**, as sign-in and `logto` do: an account with `sh-on` has `sh` over the
API, an account without it is refused there too, and a new account has
neither. That makes `sh-on` or `os-on` on an account that also has the API
route a shell behind its credential from wherever the API port is reachable —
weigh that when you turn either on. An administrator who needs a shell uses the
local login. See [API access](09-api-access.html).

## The full list

**`create.account`** · **`delete.account`** · **`modify.account`** ·
**`update.accounts`** · **`clean.account`** · **`backup.account`** ·
**`restore.account`** · **`set.backup.directory`** · **`set.config`** · **`settings.report`** ·
**`unlock`** · **`config`** ·
**`listu`** · **`list.readu`** · **`list.locks`** · **`clear.locks`** ·
**`lock`** · **`logout`** · **`set.date`** · **`remote.api`** ·
**`remote.ssh`** · **`remote.sdsys`** · **`umask`**

**`modify.password` is not on this list** — every account
has it; what SDSYS has that an ordinary account does not is the right to
name a different account with `modify.password`.

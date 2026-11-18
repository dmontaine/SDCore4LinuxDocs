Title: Accounts and Security: Making an Account
Subtitle: create.account and the operating-system and sd switches.

This page continues [Accounts and Security](01-accounts-and-security.html).

## Making an account: `create.account`

```
create.account user <name> {ssh | api | both | none} {ssh-key-on} {sh-on} {os-on} {voc-on} {bp-on} {dict-on} {shared-read-off} {shared-write-on} {net-on} {files-on} {files-write-on} {files-admin-on} {ai-on} {start-menu | start-terminal} {pins-on} {recovery-on} {xfer-on} {no.query}

create.account group <name> {shared-read-off} {shared-write-on} {start-menu | start-terminal} {pins-on} {no.query}

create.account other <name> <pathname> {shared-read-off} {shared-write-on} {start-menu | start-terminal} {pins-on} {no.query}
```

| | |
|---|---|
| **`user`** | an SD account **and** a Linux user account to log in as |
| **`group`** | a shared workspace with no Linux account, reached with `logto`, or directly by a member of its group with `sd -A`*name*. The name `shared` is reserved for the installer's own account (below) and is refused here |
| **`other`** | an SD account over a directory you name |

**A new user account starts with every door shut** (but one: it can read the
files of the `shared` account, below, and not write them). Say nothing and it has
no ssh, no API, no `sh` and no `OS.EXECUTE`, it cannot save a change to
a VOC, a program file or a dictionary, it has no right to use a server
defined for SDNet, no files-only login and no use of the AI; you open each
one by naming it. `ssh`, `api` or `both` give the remote routes (`none` is the default
and is accepted so that a script can say so); `files-on` gives the narrower
files-only API route (below, *The files-only route*); `sh-on` and `os-on` give the
two operating-system switches, and they are independent, so `sh-on os-on`
gives both and neither cancels the other; `voc-on`, `bp-on` and `dict-on`
give the three edit switches (below), each on its own; `net-on` gives the
SDNet switch (below); `ai-on` gives the AI (below, *The AI*). Two words go the other way, because the `shared` account
(below) is open to every account unless you say otherwise: `shared-read-off`
takes away the right to read its files and `shared-write-on` gives the right
to write them. (The two words that restate the defaults, `shared-read-on` and
`shared-write-off`, are for `modify.account` only.) **This is the setting SD is
delivered with, on purpose: it is the tighter one, and you loosen it for the
accounts that need it, one at a time** — the same words change an account
later in `modify.account`, below. When it has made the account SD says
where it stands:

```
fred has no remote access: not ssh, not the API
Account fred has SH no, OS.EXECUTE no
Account fred has VOC.EDIT no, BP.EDIT no, DICT.EDIT no
Account fred has shared.read yes, shared.write no
Account fred has NET no
Account fred has files no
Account fred has files-write no
Account fred keeps a recovery copy of unsaved editor text: no
Account fred may move files over its ssh login (receive / send): no
Account fred may sign in over ssh with a key: no
```

The last line is `ssh-key-on`'s state (see *Signing in over ssh with a key*, below); it is
not said for an account attached to an existing Linux user.

**Two words set up the home screen, in the same command** (they are not gates; *Where a
session starts* and *What the home screen shows*, below): `start-menu` or `start-terminal`
says where the new account starts, and `pins-on` lets the person add programs of their own
to their home screen. Neither is typed, the account follows the system default
(`set.start.default`) and may not add programs of its own. They are the words `modify.account`
takes, and the verb says them back in the same lines (`Account fred starts at: menu`,
`Account fred may add its own programs to the home screen: yes`); **any kind of account may have
them**, a group or an `other` account included. Two different start words in one command are
refused ("start-menu and start-terminal set the same access to different states ... give one of
them") before anything is made, and so is a start word that is neither (a program that calls the
account-making routine itself gets "Unexpected token"): the Linux user, the password and the
directory come after, so a refused word creates **nothing**. The words that restate what an
account has when they are left out, `start-default` and `pins-off`, are for `modify.account`
only, as `shared-read-on` is. The audit line gains `pins-on` in its `gates=` list and, when a
start word was typed, a tail `start=menu` or `start=terminal`:

```
create.account account=fred type=user gates=pins-on start=menu
```

The `gates=` list names every access the command granted, from `ssh`, `api`, `sh-on`,
`os-on`, `voc-on`, `bp-on`, `dict-on`, `net-on`, `files-on`, `files-write-on`,
`files-admin-on`, `ai-on`, `shared-read-off`, `shared-write-on`, `pins-on`,
`recovery-on`, `xfer-on` and `ssh-key-on`, and says `none` when it granted none.

**One more word, for a user account only: `recovery-on`** makes the account's `ide` keep a recovery copy of
text that was not saved (*The recovery copy*, below). It is off when the word is left out, a group or `other`
account is refused it before anything is made, and `recovery-off` is for `modify.account` only. The verb says
it back in a line, `Account fred keeps a recovery copy of unsaved editor text: yes` (`no` when the word was left out).

**And one that opens a door, for a user account only: `xfer-on`** lets the account's person move plain-text
files in and out with an sftp client (*File transfer*, below). It is off when the word is left out, a group or
`other` account is refused it before anything is made, and `xfer-off` is for `modify.account` only.

**The installing user's own account is no exception**: the account the
installer makes so that somebody can sign in starts with all of them off too,
and the installer says so and how to change it; **the installer asks no
question about it and opens nothing**. The accounts that keep their access
are the ones that already exist when you *upgrade* — see *Changing one*,
below.

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
turned on. `modify.account` gives the same two warnings when it grants `ssh`,
`api` or `both`, again with no refusal and nothing undone. Neither checks that
`sshd` is running (Ubuntu starts it on demand).

**`create.account` ends with `@system.return.code` 0 when the account is made**, so
a paragraph that tests the code after it sees success as success.

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
| `ssh`, `api`, `files-on` | say who may **connect**, and by which route |
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
| **`sh-on`** · `sh-off` | the `sh` verb (see [Operating System Access](03-operating-system-access.html)) |
| **`os-on`** · `os-off` | `OS.EXECUTE` in a BASIC program, the screen editors `edit` and `micro`, the embedded Python, **and reaching an operating-system file or directory by its path outside the account's own directory** |

The grant is two fields of the account's own record, so it follows the account,
and a person at the console is held to the limit on paths as well as a session
that arrived over the network.

That last clause of the table is the one that is easy to miss. Without `os-on` an
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
| `OPENTEMP` with a pathname or in the temporary directory, `DIGEST` of a file, and the file keys of `OSPATH()` | the `ELSE` branch, or a null result, with status 3035 (`DIGEST`'s `STATUS()` says the file is outside what the account may reach) |
| `!OSCOPY`, `!IOSCOPY` and the `oscopy` verb | refused, status -4 (the verb says why) |
| printing into a file by path (`setptr ... as pathname`, or the `SETPU` statement) | the verb refuses when the unit is set; for either, the first line printed is refused and the program stops |

The containment is by **real path**: `..` and a symbolic link are resolved
before the test, so neither gets round it. A path inside the account's own
directory always works.

**SD says no in words.** `sh` gives "*name* is not permitted to use the
operating system shell", `OS.EXECUTE` gives "*name* is not permitted to use
OS.EXECUTE", and the path routes give "*name* has no OS access, so outside its
own account it can reach by pathname only a directory the administrator opened
to all (SDSYS can give it: `modify.account` *name* `os-on`)". **SDSYS is never refused.**

### The third switch: `sd-on`, other SD accounts' directories

`os-on` is wide: it reaches any path. `sd-on` is the narrow version, for an
account that has to read or write the **data** of a neighboring SD account
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

**A smaller thing to open than `os-on` is `NETDIRS`** in `sd.conf`: directories outside every
account that every account without `os-on` may read and write by pathname, for a site whose
data lives in a shared directory. It is empty as delivered and filling it is a loosening
for every such account on every route; see *`NETDIRS`* in *Configuration*.

**SDSYS is not affected** — it is never refused. `os-on` implies `sd-on`.
The setting lives in field 9 of the register record and is not carried by an
account archive, so a restored account starts with it off.

## Continued in

[Accounts and Security: The Edit Switches and the NET
Switch](01-accounts-and-security-3-edit-switches.html) — the edit switches and
the NET switch.

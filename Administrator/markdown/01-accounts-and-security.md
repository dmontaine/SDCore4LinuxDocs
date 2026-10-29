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

**SDSYS may be signed on in more than one place, and when it is you can see it**
(owner's decision, 26 Oct 2026). Nothing stops a second terminal window or a
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
member of the Linux group of no user account** (`sdu_`*name*). The administrator
switches it on for one account at a time, `modify.account` *name* `sdsys-on`,
and off again, `sdsys-off` (below): with it on, SDSYS can change the account's
VOC or a dictionary by saving its master record (see
[The master files](19-the-master-files.html)). **While it is on, the `sdsys`
user has write access to everything the account's group may write**, and a VOC
entry or an I-type is code that runs in the account: someone who took over the
`sdsys` login could change what that account runs. It is not reachable from the
network (`sdsys` has no remote access), and a process that is not a real login
as `sdsys` is not an administrator. **Off is a default and a record of your
decision, not a wall against a stolen `sdsys` login**, which has other ways into
an account's code: the global catalogue is the `sdsys` user's to write, and
`sdsys` may run `sudo /usr/local/sbin/sd-elevate` with any arguments. (The
files `root` runs at the next start used to belong to `sdsys` as well; from
1.2-0 they are `root`'s, see [Installation and the daemon](08-sd-installation.html#the-files-root-runs).)
What the default takes
away is the silent route; the switch is an audited act of the administrator and
it can be taken back. Before 1.2-0 the membership was there for every account;
an install that finds it asks once whether to keep it (see
[The master files](19-the-master-files.html)).

### The sdsys user in an account's group: `sdsys-on` and `sdsys-off`

`modify.account` *name* `sdsys-on` puts the `sdsys` user in the account's
Linux group and makes the account's VOC and dictionaries writable by that group;
`sdsys-off` takes the user out. The state is the group membership, as it is for
`ssh` and the API, so nothing is written to the register. The lines printed are
`Account fred: master edits are on. ...` and `Account fred: master edits are
off. ...`; the audit trail has `modify.account sdsys-on account=fred`, and
`sd-elevate` writes a line to the system log. **User accounts only**: a group
account is refused ("is not a user account"), because `sdsys` owns the files of a
group account. `sdsys-on` can be given again to an account that is on, which
repairs the modes and changes nothing else; `sdsys-off` for an account that is
off changes nothing. The two words conflict only with each other. **A session of
SDSYS that is already running keeps the groups it started with**: sign on again
after `sdsys-on`, and after `sdsys-off` that session still has the write until
it ends. `create.account` does not switch it on and neither does the installer.

## Making an account: `create.account`

```
create.account user <name> {ssh | api | both | none} {sh-on} {os-on} {voc-on} {bp-on} {dict-on} {shared-read-off} {shared-write-on} {net-on} {files-on} {files-write-on} {files-admin-on} {ai-on} {start-menu | start-terminal} {pins-on} {recovery-on} {no.query}

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
a VOC, a program file or a dictionary, and it has no right to use a server
defined for SDNet, and no files-only login; you open each one by naming it. `ssh`, `api` or `both` give the remote routes (`none` is the default
and is accepted so that a script can say so); `files-on` gives the narrower
files-only API route (below, *The files-only route*); `sh-on` and `os-on` give the
two operating-system switches, and they are independent, so `sh-on os-on`
gives both and neither cancels the other; `voc-on`, `bp-on` and `dict-on`
give the three edit switches (below), each on its own; `net-on` gives the
SDNet switch (below). Two words go the other way, because the `shared` account
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
```

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

**One more word, for a user account only: `recovery-on`** makes the account's `ide` keep a recovery copy of
text that was not saved (*The recovery copy*, below). It is off when the word is left out, a group or `other`
account is refused it before anything is made, and `recovery-off` is for `modify.account` only. The verb says
it back in a line, `Account fred keeps a recovery copy of unsaved editor text: yes` (`no` when the word was left out).

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
| **`sh-on`** · `sh-off` | the `sh` verb |
| **`os-on`** · `os-off` | `OS.EXECUTE` in a BASIC program, the screen editor `micro`, the embedded Python, **and reaching an operating-system file or directory by its path outside the account's own directory** |

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

### The edit switches: `voc-on`, `bp-on` and `dict-on`

Three more per-account switches, in fields 10 to 12 of the register record,
say whether the person who signed on to the account may **save a change** to
a VOC, to a program file, and to a dictionary. Reading is never stopped. **All
three are off for a new account**, and `modify.account` *name* `voc-on` /
`voc-off`, `bp-on` / `bp-off` and `dict-on` / `dict-off` turn each one on and
off. `create.account user` takes `voc-on`, `bp-on` and `dict-on`. After a
change SD says where the account now stands (if the switch already had the
value asked for, SD says only that the account already had that access and
that nothing changed):

```
:modify.account fred bp-on
Account fred has VOC.EDIT no, BP.EDIT yes, DICT.EDIT no
```

**Which files.** A file is known by the name of the file that is **open**, not
by the name that was typed, so a Q-pointer to somebody's VOC is caught:

| | |
|---|---|
| **a VOC** | a file called `voc` |
| **a dictionary** | any file whose name ends in `.dic`. `voc.dic` is the dictionary of the VOC, so it is a dictionary, not the VOC |
| **a program file** | `bp`, `bp.out` (the object code), or any name ending in `.bp` or `.bp.out` |

Capitals do not matter.

**What stops.** A program's `WRITE`, `WRITEV`, `DELETE` and `CLEARFILE` of
such a file is refused with a message that names the missing switch (or sets
the `ON ERROR` status). The verbs and statements that change a file the
person names ask the same question first, before they lock or change
anything, and give the reason: `sed`, `ide` and `ced` show it in their
message line, and every other verb prints it (the same text as above) and
stops. They are `ed`, `edit` and `copy` into the file or moving
records out of it, `delete`, `clear.file`, `cname` of a record, `delete.file`
of a program file or of a dictionary on its own, `fixdir`, `format`,
`map file` (asked before the "will be cleared and overwritten" question),
`sp.view` (the X key that deletes an item; the reason replaces the prompt
line), `set.trigger` when it installs or removes a trigger (the report form,
with no trigger name, is not asked), `copy.list` into the file or with
`deleting` from it, `delete.list ... in`, `get.list ... deleting in`,
`save.list ... in`, `sort.list ... from`, `reformat ... to` (and the
`Output file:` prompt), `list ... pageseq`, a delimited report written `to` a
pathname, `compile.dict data` (which compiles records of an ordinary file as dictionary
items), `generate` (the `$include` record of a dictionary, and the include
record it writes to the target file), `como on ... in`, and the `.s` and `.d`
stack commands on an existing VOC record. Making a new file is not asked. The private catalogue
directory (`cat`, or whatever `$private.catalog` names) counts as a program
file. For programs, `create.file` and `opentemp` of a new file inside such a
place, `ospath` with keys 5, 13 and 14, and the socket trace file
(`set.socket.mode` with `skt$info.trace`) are refused with status 3035. `cname`
will not take a program file out of its name, or put a file under one, for a
person without the switch, so a rename is not a way round. `OPENSEQ` in such a
place opens the file for reading only and cannot create one; `DELETESEQ`, a
print file made there, and `!OSCOPY` or `!IOSCOPY` into it are refused. For
these operating-system routes the name of the record or file being made counts
only when it is itself a directory or anything but a plain file, so a plain
file called `sample.bp` in an ordinary directory is not held back, while a
file inside the directory `bp` is. Over the API a client's writes, deletes and
file clears, and `SDOpenSeq` for writing, are held to the same rule (an
`SDOpenSeq` of such a place opens read only).

**Compiling is held by `bp-on` too.** Without it `basic`, `catalog`,
`delete.catalog` and `decatalog` are refused ("Programs can only be compiled
or catalogued by an account that has bp.edit"), because compiling is how a
source becomes code that runs: otherwise source could be copied into any file
and compiled there.

**`logto` does not change them.** The switches are those of the account the
person **signed on** to (over the API, the account first entered). A person
with a switch on keeps it in another account; a person without it does not
gain it there. A change takes effect the next time the person signs on. Unlike
`sh-on`, `os-on` and `sd-on`, the three edit switches are read at sign-on
only, not again at `logto`.

**What is not stopped.** What SD writes as a side effect of an ordinary
command — a new pointer made by `create.file`, a new saved sentence, a
compiled I-type, the command stack — and anything done from the shell by an
account that holds `sh-on` or `os-on`. The operating-system routes above
(`OPENSEQ`, `DELETESEQ`, print files, `!OSCOPY`, `!IOSCOPY`, `ospath`) are
not looked at for an account that holds `os-on`, when the path is outside the
account's own directory: `os-on` already trusts it with the whole machine.
The switches are about changing these files by hand or by program, not a
replacement for the operating-system switches above.

**Two VOC records that change what a command line does: `$private.voc` and
`$voc.parser`.** Neither is in a stock VOC and nothing SD ships writes them.
Both are VOC records of type `X`, so writing, changing or deleting one needs
`voc-on` (an account without it is refused with status 3035 and the `voc.edit`
message). What they do, and where `voc-on` stops, was run on a private SD
(Dev tip, 18 October 2026) in ordinary accounts:

* **`$private.voc`** (field 2 a file name) is a second vocabulary. A command
  word that is in no VOC record is looked for in that file, as typed, then in
  lower and upper case, **before** the private and global catalogues. It
  can add a command, and it can replace one that exists only as a catalogued
  program; it cannot replace a command that the VOC holds. Its records run
  under the same switches as VOC records: a verb record in mode `os` was
  refused for an account without `sh-on`. A record that does not work (the
  file missing, a place the account may not open) is ignored without a
  message.
* **The file is not guarded by `voc-on`.** The switches look at the name of
  the file being written, and only a file called `voc` counts as a VOC. A
  private vocabulary called `zzpv` is an ordinary data file, so **an account
  with all three edit switches off could add and replace commands in it** once
  you had pointed `$private.voc` at it. Keep the file where only the people
  you mean can write it. A file of the shared account works for this: an
  account with `shared.read` (on unless you turn it off with
  `shared-read-off`) ran a command from one, and its write to the file was
  refused with status 3035 while `shared.write` was off.
* **`$voc.parser`** (field 2 record type codes, field 3 the names of
  catalogued subroutines) hands a VOC record whose type begins with a code to
  that subroutine **instead of SD's own handling of the type**. A code of `v`
  hands over every verb, including `off`; a blank code matches every record.
  It is read once, at sign-on, and `logto` does not read the new account's
  copy. A handler must already be catalogued, and cataloguing needs `bp-on`;
  but `voc-on` alone is enough to switch on a handler that someone else
  catalogued. So an account with `voc-on` can change what the commands in its
  own VOC mean for every session that signs on to it, by way of a handler that
  you or somebody with `bp-on` put in a catalogue.
* **If a handler locks an account out,** every command in the account,
  yours included, is handed to the handler, so the record cannot be removed
  from inside. It was removed by SDSYS signed on to the `sdsys` account, with
  an ordinary program that opened the account's `voc` by its pathname and
  deleted `$voc.parser`.

**Internal programs run only from the global catalogue.** The gates on files
and on operating-system paths (these three and the shell, `OS.EXECUTE` and
`sd-on` gates before them) do not apply to a program compiled in *internal
mode*, which SD's own commands are. That mark is a bit in the program's own
object file, and SD used to believe it wherever the object came from, so a
user who could put an object file where SD would run it (a directory file with
a `.out` entry in the VOC, or a run file) could set the bit and skip every
gate. SD now honours the bit only for an object from the global catalogue,
which only SDSYS can write, or for the administrator; for any other object the
bit is cleared when the object is loaded. SD's own commands are all in the
global catalogue and are unaffected; a program that SDSYS compiled in internal
mode into a user's account runs there as an ordinary program.

**SDSYS is never refused.** On a terminal or in a batch job the
administrator passes every gate. An API session carries no administrator
flag, so SDSYS over the local API (a process running as `sdsys` entering the
`sdsys` account on the Unix socket) is given all three switches on when it
signs on; `modify.account` refuses SDSYS as a target, so there is nothing to
set for it.

**Group and other accounts.** The three words are accepted for a group or
other account, and they do matter: a member of the account's Linux group can
sign on to it directly with `sd -A`*name*, in a batch job, or over the API,
and the account's own switches then decide, because the account signed on to
is the one that counts (only `logto` leaves the earlier account's switches
alone). The upgrade leaves group and other accounts off on purpose; where
members need to save to a VOC, a program file or a dictionary there, SDSYS
gives it with `modify.account` *name* `voc-on` / `bp-on` / `dict-on`.

**On an existing machine.** When the installer is run by the user whose own
account already exists, the upgrade switches all three on, **once**, for every
*user* account in the register, so that no such account loses what it had;
group and other accounts, and accounts made afterwards, start with all three
off. On a fresh install, the installing user's own account is made with all
three off like any other. If a different OS user runs the installer over
existing accounts (so the installing user's account does not exist yet), the
upgrade walk is not run, and the existing accounts stay off until SDSYS turns
the switches on. The switches are kept in the account archive, but
`restore.account` gives them back only to an account it has to create; an
account that already exists keeps its current switches, group and other
accounts are not in the manifest, and an archive from before the switches
existed carries none and gives none.

### The NET switch: `net-on` and `net-off`

One more per-account switch, in field 15 of the register record, for **SDNet**:
files held on another SD server, which an account opens from its own VOC through
an `N` pointer (see [SDNet](12-sdnet.html)). It is the permission an account needs before it
may use a server, and **it is off for a new account**. `modify.account` *name*
`net-on` / `net-off` turns it on and off, and `create.account user` takes
`net-on`. After a change SD says where the account stands, in a line of its own
(the same wording as the edit switches' line, for one switch):

```
:modify.account fred net-on
Account fred has NET yes
```

**The switch is what lets an account open a remote file.** An account without it
is refused before anything is dialled. It is checked at every sign-on. A blank
field, and every account that existed before the switch did, count as off:
**there is no upgrade step**, and those accounts cannot use SDNet until SDSYS
turns the switch on, which is the delivered state.

**It is read the way `sd-on` is, not the way the edit switches are.** It belongs
to the account the person is *in*: it is read at sign-on, again at `logto` into
another account, and given back when `logto` returns, and the API server reads it
at every entry to an account. A change takes effect the next time the account is
entered. It may be set on a group account, as `sd-on` may (`sh-on` may not).
**SDSYS is never refused**, and an SDSYS session over the local API is given the
switch on when it signs on. If the switch already had the value asked for, SD
says only that the account already had that access and that nothing changed.
The change is written to the audit trail (`modify.account net-on account=fred`).

The switch is kept in the account archive for a user account (`net: 1` or `0` in
its manifest), and `restore.account` gives it back only to an account it has to
create, as for the edit switches; an archive from before the switch carries none
and restores the account with it off.

**Having the switch is not enough, even when SDNet can open files.** An account
must also be named in the *allowed accounts* of the server it wants, and
SDSYS puts it there with `set.server ... accounts` ([SDNet](12-sdnet.html)). Two
lists, both empty until SDSYS writes to them: the switch says the account may use
SDNet at all, the list says which servers it may use.

### The shared account: `shared-read-on`, `shared-read-off`, `shared-write-on` and `shared-write-off`

The installer makes one group account, named `shared`, and **the files in it can be
opened by every account by file name** — `open "inventory"` in any account finds
the file `shared` holds under that name, with no `logto` and no pointer in the
account's own VOC. Two per-account switches, in fields 13 and 14 of the register
record, decide who may. The full description, with the order of the checks and the
cautions, is its own page: [The shared account](13-the-shared-account.html).

| switch | delivered | words | what it allows |
|---|---|---|---|
| `shared.read` | **on, for every account** | `shared-read-off` / `shared-read-on` | opening the files of `shared` by name, and reading them |
| `shared.write` | off | `shared-write-on` / `shared-write-off` | saving, deleting and clearing records in them (a dictionary needs `dict-on` as well) |

**`shared.read` is the one switch in SD whose blank means ON.** It is only off when
the field says `no`: `shared-read-off` writes `no`, and `shared-read-on` writes
`yes`. A blank field — a new group or other account, and every account that
existed before the switch did — reads as on, so **nothing is withdrawn from an
existing account, and nothing needs to be run at an upgrade.** `shared.write` is
the other way: only `yes` is on. **Anything you place in `shared` can be read by
every account you have not taken the right from**, so put nothing there that is not
meant for everyone, and take the right from the accounts that should not have it
before you fill the account.

```
:modify.account fred shared-read-off
Account fred has shared.read no, shared.write no
:modify.account fred shared-write-on
Account fred has shared.read no, shared.write yes
```

`modify.account` *name* `shared-read-on` / `shared-read-off` / `shared-write-on` /
`shared-write-off` change one switch each and say where the account now stands,
both switches in one line. `create.account user` takes `shared-read-off` and
`shared-write-on` (the other two would only restate the delivered state), and so
do `group` and `other`. Asking for what is already so changes nothing and says so.
Each change is written to the audit trail (`modify.account shared-read-off
account=fred`). A switch may be set on a group or other account, as `net-on` may;
**SDSYS is never a target**.

**It belongs to the account the person is in, like `net-on`:** it is read at
sign-on, again at `logto` into another account, and given back when `logto`
returns, and the API server reads it at every entry. `shared.read` is read when a
file is *opened*, so a file already open stays usable after you withdraw it,
until the person's next entry; `shared.write` is tested at every write.

**How SDSYS puts files in `shared`.** Sign on as SDSYS, `logto shared`, and make
files as in any account: `create.file`, `copy`, programs that write. The account's
directory, `/home/sd/group_accounts/shared`, belongs to `sdsys` with the group
`sdusers` (mode 2775, files 664), so every SD user's own process can read the
files through the kernel, and write them when it has `shared.write`. **Only SDSYS
enters `shared`**: its Linux group is `sdg_shared`, whose members are `root` and
`sdsys`, not `sdusers`, so `logto shared`, a Q-pointer to it and `sd -Ashared` are
refused to everybody else. That is what makes taking `shared.read` away a real
wall for an account that has neither `sh` nor `os`.

**A maintainer who is not SDSYS** is made of two things: membership of the group,
`modify.account shared add` *name* (the Linux user can then `logto shared` and
sign on to it directly), and `shared-write-on` **on the account named `shared`**,
which lets those members write records there. Neither lets a maintainer change the
*structure* of a file — see the page for that. The switches on the account `shared`
decide what its members can do inside it; a blank means write off.

**What it does not do.** The verbs, sentences and programs of `shared` are not
shared; only data files and their dictionaries are. The administrator's own `open`
does not follow `shared` (reach it with `logto shared`). `shared` is not copied to
other servers. The name is reserved: `create.account` refuses it, and
`delete.account shared` is refused.

**Upgrading.** The installer makes `shared` when it is run, and keeps it when the
accounts are kept. **It stops before it changes anything if an account named
`shared` already exists that is not its own**, and names the register record: rename
that account by hand and run the installer again. Removing SD together with its
accounts removes the Linux group `sdg_shared` too; keeping the accounts keeps it.

### The files-only route: `files-on` and `files-off`

There are now **two API routes, and the second is narrower.** `api` (the Linux
group `sdapi`) lets a person do everything the API offers: execute commands, call
catalogued subroutines, enter other accounts with `logto`, read and write
sequential files, and work with files. **`files-on` (the Linux group `sdfiles`)
lets a person log in over the API and do files and nothing else.** It exists so
that a login kept for SDNet (see [SDNet](12-sdnet.html)) never needs `sdapi`: the
other server's administrator gives that login `sdfiles`, and whoever steals the
stored login can open and read files on that server and cannot run a command
there. **Changing files there is a further permission, `files-write-on` (the Linux
group `sdfileswrite`)**, given separately and off for a new account (below, *Changing files: `files-write-on`*), and **administering them there - configure, index, create and delete a file, the file's counter - is a third, `files-admin-on` (the Linux group `sdfilesadmin`)**, off for every account (below, *Administering files: `files-admin-on`*).

**Off for a new account, like every other door.** `create.account user` takes
`files-on`; `modify.account` *name* `files-on` / `files-off` turns it on and off.
Membership of `sdfiles` *is* the route, as membership of `sdapi` is for `api`, so
there is no field for it in the register. After a change SD says where the account
stands, **read back from the operating system's group file** rather than taken from
the request, in a line of its own:

```
:modify.account fred files-on
Account fred has files yes
:modify.account fred files-off
Account fred has files no
```

(The word was "FILES" in capitals until 19 October 2026; SD writes a keyword it prints in
lower case, as the line for `files-write` always did.)

Asking for what is already so changes nothing and says so ("fred already had that
access; nothing changed"). The change is made by the same privileged helper as the
`api` word (`sudo /usr/local/sbin/sd-elevate addgroup` or `delgroup`, with the
group `sdfiles`), and written to the audit trail (`modify.account files-on
account=fred`). If the group file does not show the state asked for afterwards, SD
reports the failure ("Unable to change remote access for fred, status: 2") and not
a success.

**The rules, in the order the login applies them.** The API server decides at the
end of the login, after the password has been proved:

1. The person must be in `sdusers`, as for every route.
2. A member of **`sdapi` has the whole API, whether or not they are also in
   `sdfiles`: `sdapi` wins.**
3. Otherwise a member of **`sdfiles`** is let in **files only**. The session is
   marked once, at login, and the mark is never cleared for the life of the
   connection.
4. A person in **neither** group is refused exactly as before: "*name* is not
   permitted to use the API", with the reason `not a member of sdapi or sdfiles` in the
   audit trail (it said only `not a member of sdapi` until 19 October 2026, although the
   decision is made on both groups). If the group file cannot be read the login is refused,
   not guessed, with a reason of its own.
5. `sdsys` is exempt from both groups by name and keeps the doors it has always
   had; it is never made files-only.

**What a files-only session may ask for.** One function, `!apifilesok`, decides, and
it is an *allow list*: a request number that is not in it is refused, including a
number this release has never heard of.

| allowed | request |
|---|---|
| 1, 2 | quit; get the text of the last error |
| **3, once** | set the account. The first one, which is the entry to an account after login, is allowed; a later one would be a `logto` and is refused |
| 4, 5 | open a file; close it |
| 6 | read |
| 7 to 10 | the locking reads (`readl`, `readlw`, `readu`, `readuw`): **only with `files-write-on`** |
| 11 to 15 | select; read the next id; clear a select list; read a saved list; release a lock |
| 16 to 19 | write; write and keep the lock; delete; delete and keep the lock: **only with `files-write-on`** |
| 26 | select on an index. Allowed because it is a select, with 37 to 39 |
| 30 to 34 | lock a record; clear a file; lock and unlock a file; ask whether a record is locked (34, added on 20 October 2026: the answer names the holder by his user number on this server): **only with `files-write-on`** |
| 35, 36 | list the indices |
| 37 to 39 | select a list; select by an index value; select by an index key |
| 40, 41 | file information; read one field (a `readv` that takes a lock is a change and needs `files-write-on`) |
| 42 to 45 | set the left or right end of an index range (`setleft`, `setright`), and select within it (`selectleft`, `selectright`) |
| 46 | the mark mapping |
| 49 | the server's revision |
| 68, 69 | `write` and `writeu ... creating.seqkey` (the file's own counter gives the id): **only with `files-write-on` and `files-admin-on`** |
| 70 | a verb run on this server for the login (`analyze.file`, `configure.file`, `create.index`, `build.index`, `delete.index`, `disable.index`, `create.file`, `delete.file`): **only with `files-write-on` and `files-admin-on`** |
| 71 | `fcontrol`: **only with `files-write-on` and `files-admin-on`** |

| refused | request |
|---|---|
| 20 | call a catalogued subroutine |
| 21, 22, 23 | execute a command; respond to its prompt; end it |
| 24, 25 | the other logins |
| 27, 28 | enter and exit a licensed package (not supported by any route) |
| 29 | open a file on another SDNet server |
| 47, 48 | the SCRAM login itself, which is only possible before the session is logged in |
| 50, 51 | read a variable; `system()` |
| 52, 53 | `trans()` |
| 54 | transactions |
| 55 to 60 | evaluate and the conversions |
| 61 to 67 | sequential files |
| 0, 72 and above, anything else | no such request here |

A refused request is answered with "This login is for files only: request *n* is not
allowed", **the request is not carried out**, and a line goes to the audit trail
(below). The connection stays open, so a client that asks for something it should not
can carry on with files.

**What is not changed.** Everything else about the session applies as it does to any
other: the account must be entered, the account's own switches (the OS-access
gate, the three edit switches, the NET switch) are loaded and enforced, `SDCLIENT` in
`sd.conf` still decides whether a client may open the files it names, and the
API listener must be on (`remote.api`). **`sdfiles` alone is a read-only route**: the
numbers marked above are refused unless the person is also in `sdfileswrite`.

### Changing files: `files-write-on` and `files-write-off`

A files-only login may write, delete, lock and clear **only if the person is also in
the Linux group `sdfileswrite`**, which the administrator of that server gives with
`modify.account` *name* `files-write-on` (or `files-write-on` after `files-on` in
`create.account user`) and takes away with `files-write-off`. It is off for a new
account. The line SD prints after a change is read back from the group file, as for
`files-on`:

```
:modify.account fred files-write-on
Account fred has files-write yes
```

`files-write-on` for a person who is not in `sdfiles` is refused ("Account fred does
not have files access, so it cannot be given files-write: use files-on first"), because
the group on its own gives nothing; `files-off` takes the person out of both groups.
**`files-off` takes the write group away first, then `sdfiles`, and reads each back**, and it
does the work for a person who is in only one of them. A person who is in `sdfileswrite`
and not in `sdfiles` (a removal that stopped half way, or a change made by hand) used to be
told "fred already had that access; nothing changed" and kept the membership, which the next
`files-on` turned into write access nobody had given; that case is now cleaned up, with the
line `Account fred has files-write no` before `Account fred has files no`. If a removal fails
SD says so and stops: a failure of the write group's removal leaves the person as they were, and
a failure of the second removal leaves them in `sdfiles` alone, read access and never write
without read. `files-on` takes a leftover write membership away before it adds `sdfiles`, and
stops with the same message if it cannot. A
refused change is answered "This login cannot change or lock files here: ask the
administrator for files-write-on (request *n*)", is not carried out, and goes to the audit
trail as `api refused request=16 route=sdfiles write=off admin=off user=fred`; the login line says
`write=on` or `write=off` (and `admin=on` or `admin=off`). `sdapi` members are not affected. Like `sdfiles`, the group is
read at login, so a change reaches the person at their next login. The account's manifest
(`backup.account`) records it as `route.files.write`, and `restore.account` gives it back
only to an account that is in `sdfiles`.

### Administering files: `files-admin-on` and `files-admin-off`

A files-only login may configure a file, build and delete its indices, create and delete a file,
set or take the file's counter (`WRITE ... CREATING.SEQKEY`, `FCONTROL`) **only if the person is
in both `sdfileswrite` and the Linux group `sdfilesadmin`**: `modify.account` *name*
`files-admin-on` (needs `files-on` and `files-write-on` first, else "Account fred does not have
files-write, so it cannot be given files-admin: use files-write-on first"), `files-admin-off`, and
`files-admin-on` after `files-on` and `files-write-on` in `create.account user`. **It is off for
every new account, and the installer does not turn it on.** The line printed is `Account fred has files-admin yes`, read back from the group file.
The three groups are a chain, `sdfiles` < `sdfileswrite` < `sdfilesadmin`: `files-write-off` and
`files-off` take the higher groups away first (administration, write, files), each removal read
back, and a failure half way reports the removals that did happen; `files-on` and `files-write-on`
take a stray higher membership away before they add. What the permission allows, what the server
checks and how it is audited is in [SDNet](12-sdnet.html), *The administration group*. A
refused request is answered "This login cannot administer files here: ask the administrator for
files-admin-on (request *n*)" and nothing is carried out. The account's manifest records it as
`route.files.admin`, and `restore.account` gives it back only to an account that is in
`sdfiles` and `sdfileswrite`.

### The AI: `ai-on` and `ai-off`

An account may send text to the AI provider you have chosen (the `ai` verb) **only if the person is in
the Linux group `sdaiusers`**: `modify.account` *name* `ai-on`, `ai-off`, and `ai-on` in
`create.account user`. **It is off for every new account, and the installer
does not turn it on**, because each request is paid for by whoever holds the provider's key.
The line printed is `Account fred has ai yes`, read back from the group file. It stands alone (no
other gate is needed), is for accounts that belong to a person (a group account is refused), and takes
effect at the person's next request. The account's manifest records it as `route.ai`, and
`restore.account` gives it back. Which provider, model and key, what leaves the machine, and the page
that does all of this, `tool.ai`, are in [The AI Helper](20-the-ai-helper.html).

**The route words are not one state.** `ssh`, `api`, `both` and `none` are
absolute about the two routes they name, and **leave `files-on` alone**:
`modify.account fred none` takes away ssh and the API and not the files-only
login. Withdraw it with `files-off`. `sdapi` is never touched by `files-on` or
`files-off`.

**User accounts only.** A group account, which has no Linux user, is refused
`files-on` and `files-off` ("is a group account and has no remote access"), an
`other` account too ("Unable to change remote access ... status: 2"), and
`create.account group` and `create.account other` refuse the word the same way.
`files-on` also refuses a person who is not in `sdusers`, because the login would
refuse them first. If the Linux group `sdfiles` does not exist, `files-on` says
"sdfiles is not a valid Linux Group" and changes nothing, and
`create.account user ... files-on` looks for the group **before** it makes the Linux
user, so nothing is left behind. **An installation made before this release has no
`sdfiles` group, and its helper does not accept it, until the installer is run
again**; the installer makes the group (empty) beside `sdssh` and `sdapi`, and the
helper's list of groups it will touch includes it. Like `sdssh` and `sdapi`, the
group cannot be deleted with the helper's `groupdel`; a full DELETE of SD (not one
that keeps the accounts) removes it with the others.

**A change takes effect at the person's next login.** The group is read when the
login finishes, so a connection already open keeps the route it started with.
To take the route away from somebody who is connected now, `files-off` and end the
connection.

**Audit trail.** A files-only login writes `api login route=sdfiles write=off admin=off user=fred`
(`write=on` for a person in `sdfileswrite`, `admin=on` for one in `sdfilesadmin`; the `admin=` word
has been there since 21 October 2026). Each refusal writes
`api refused request=26 route=sdfiles write=off admin=off user=fred` (the number is the
request; `write` and `admin` are the state of the login, so a refusal with both `on` is a request
no files-only login may make). A user in neither group, as before, has the refused login in the usual
`api refused` form.

**The archive.** For a user account the manifest carries `route.files: 1` or `0`
beside `route.ssh` and `route.api` (not `files:`, which is already the count of files
in the archive), and `restore.account` puts an account it has to create back in
`sdfiles` if the manifest says so. An archive from before this release has no such
line and restores the account out of the group. A manifest that says `1`, restored on
a machine with no `sdfiles` group, fails for that account with the group message
and creates nothing.

**What has and has not been shown.** Checked from the source and by the free
checks that read it as text: the order of the checks in the login, that the gate
sits in the request loop before the dispatch, the table of numbers, the helper's
rules for the group and its refusals (`sd-elevate`, by test as an ordinary user, with
mutants), and the wording of the messages. **Seen on a real installation (18 October 2026,
one machine as server and client over the loopback address):** a real user in `sdfiles`
logging in; the group membership read at login (the same programs refused before
`files-write-on` and working after it); the refusal of requests on a live session with the
audit lines; `create.account ... files-on` and `modify.account ... files-write-on` against
the real `/etc/group`; and the installer making the groups. **Run only against a scratch
group file and a stand-in for the helper (19 October 2026):** `files-off` and `files-on`
with a person in `sdfileswrite`, including a removal that fails. **Not run on a real
installation:** that case, the archive round trip for a person in `sdfileswrite`, and the
refusal of requests 20 to 23, 29, 54 and 61 on a live files-only session. The client that
uses the route is the SDNet client (see [SDNet](12-sdnet.html)), which has also not been
run between two machines.

### VOC pointers: where a file pointer may lead, and which Q-pointers are followed

**A VOC pointer is a way to name a file, so it is held to the same rule.** An
account can write a pointer into its own VOC with `ed`, or make one with
`create.file ... pathname`, and a Q-pointer is what `set.file` makes into
another account. For everybody but SDSYS:

| | |
|---|---|
| **a file pointer (F-type)** | must lead **inside the account's own directory**, or inside the directory of an account a Q-pointer was followed into (below), or be **the pointer SD itself put in the VOC** — the same id, with the same path, as in `newvoc` (`syscom`, `$map`, `dict.dict`, `voc`, `newvoc`, `$acc`). An account that holds `os-on` may go anywhere its Linux user can. Anything else is refused with status 3035 |
| **a Q-pointer** into a **registered account** | is followed only if the user **could `logto` that account**: a member of its Linux group, and the account not suspended — `logto`'s own test — **whether or not the account holds `os-on`**. SD's own Q-pointer, `sd.accounts` (which leads into SDSYS, an account nobody can `logto`), is exempt because it is exactly what SD put there |
| **a Q-pointer** that **names a path** | is an operating-system path, and the `os-on` question |

So `set.file` into somebody else's account works only for a user who may enter
that account, and a hand-made pointer at `/etc` or another account's
directory is refused unless the account holds `os-on`. A refused open takes
the `ELSE` branch with status 3035, like any other refusal here. **SDSYS is
never refused.**

**The API's request 29, "open an SDNet file", asks the same question** (since 20
October 2026; it used to open any such pointer for a caller the `net-on` switch
admitted, and the SDNet page of this set listed that as a limit). It asks it of the
account **named in the request**, from that account's own register record, and not of
the account the API session happens to be in: a file pointer in the named account's VOC
must lead inside that account's own directory (`..` and links resolved, a directory
that merely begins with the account's name is not inside), unless the account holds
`os-on`. SDSYS entering its own account is never refused. It is stricter than the local
rule in one way: the pointers SD itself put in every VOC (`syscom`, `$map`,
`dict.dict`, `newvoc`) lead out of the account and are refused here too,
because a remote caller has no use for them. A refusal is error `ELSE` with status 3035
and a line on the audit trail, `api refused request=29 reason=os gate off user=...
account=... path=...`. The register is read at each request, so `os-off` applies to a
session that is already signed on.

**What this changes on an existing machine.** A Q-pointer that leads into an
account its owner can no longer enter stops opening, and so does a hand-made
file pointer to a directory outside the account in an account that does not
hold `os-on`. The accounts that existed at an upgrade hold `os-on`, so their
own pointers keep working; the Q-pointer rule applies to them too.

There are no `path:name` or `account:name` forms of a file name any more (the
`sd.conf` setting `FILERULE` that turned them on was removed on 28 October 2026): a
name that is in no VOC record is not found. A file outside the account is reached
only through a VOC pointer, which is held to the `os-on` rule and the Q-pointer rule
above.

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
modify.account account voc-on | voc-off
modify.account account bp-on | bp-off
modify.account account dict-on | dict-off
modify.account account recovery-on | recovery-off
modify.account account net-on | net-off
modify.account account shared-read-on | shared-read-off
modify.account account shared-write-on | shared-write-off
modify.account account files-on | files-off
modify.account account files-write-on | files-write-off
modify.account account sdsys-on | sdsys-off
modify.account account start-menu | start-terminal | start-default
modify.account account pins-on | pins-off
modify.account account suspended | unsuspended
```

**More than one action in a command** (from 19 Oct 2026). Any number of the
words above except `add` and `delete` may follow the account, in one command:
`modify.account fred sh-on os-on voc-on bp-on`. SD reads every word first and
then carries out all of them, or none of them:

* **An unknown word, two words that set one access to different states, or
  `add` / `delete` among other words refuses the whole command before anything
  is changed**, and the refusal names the word: `sh-on` with `sh-off`, `ssh`
  with `api` (say `both`), and `files-off` with `files-write-on` are the
  conflicts.
* **The words are carried out in one fixed order whatever order they were
  typed:** the route words, then the register switches in the order of the list
  above, then the files words (`files-on` before `files-write-on`, which needs
  it), and the suspension last. Each is reported and audited exactly as if it
  had been given alone.
* **A command of more than one action ends with a line** saying which were
  carried out, and if one could not be (a refusal such as `sh-on` on a group
  account, or a Linux group change that failed) the others are still carried out
  and the line names the one that was not.

```
:modify.account fred os-on sh-on
Account fred has SH yes, OS.EXECUTE no
Account fred has SH yes, OS.EXECUTE yes
Account fred: 2 actions carried out: sh-on, os-on
:modify.account fred sh-on sh-off
sh-on and sh-off set the same access to different states, and nothing was changed: give one of them
:modify.account fred voc-on bogus
bogus is not a modify.account action, and nothing was changed: give modify.account with an account and no action to see them
:modify.account hr voc-on sh-on
Account hr has VOC.EDIT yes, BP.EDIT no, DICT.EDIT no
hr is a group account and has no Linux user, so it has no shell to permit
Account hr: NOT every action was carried out. Done: voc-on. Not done: sh-on
```

`add` and `delete` take one user name and stand alone: among other words, or
with a word after the user name, they are refused with the message
*add and delete take a user name and stand alone, and nothing was changed: ...*.
The same word twice is one action. (Until 18 Oct 2026 the second word was read
by nobody: `voc-off` was done and `bp-off` dropped without a message; from 18
Oct it was refused with *modify.account does one action at a time*; it is done
since 19 Oct.)

### The accounts on one screen: `tool.accounts`

```
tool.accounts
```

A full-screen page in SDSYS's VOC only (a window of 140 columns by 43 lines or more; in a bigger window this page, like every
administrator page, uses the whole window, with more rows and wider boxes, and follows a resize). The list is every
registered account but SDSYS: its name, its kind (user, group or other), whether it is suspended, **the
gates that are on for it** (read the way `tool.gates` reads them: the register and the Linux groups) and
how many sessions are signed on in it. The box at the foot shows the account under the cursor as the
register and `/etc/group` give it: its path, its Linux user and group, its routes, a group account's
members, the gates that are on and who is signed on in it. **The gate switches are `tool.gates`'s, not
this page's**: a new account has every gate off, as the verb makes it.

| Key | Runs |
|---|---|
| `S` | `modify.account name suspended`, or `unsuspended` when the account is suspended already |
| `A` | `modify.account group add user`, on a group account, for the Linux user you type |
| `R` | `modify.account group delete user`, taking one away |
| `C` | `create.account group name no.query`, `create.account other name path no.query`, or `create.account user name {none\|ssh\|api\|both}` |
| `X` | `delete.account name {remove.home}`, after you type the account's name |

Each shows its command and what it does in a box answered Run or Cancel, **and Cancel is what Enter
chooses**. The verbs ask for the administrator again and write their own audit lines; the page runs
nothing else. **Two of them are not run through the page**: creating a user account and deleting an
account hand the terminal to the verb, because `create.account user` asks for the new person's password
at a prompt of its own that shows nothing, and `delete.account` has no `no.query`, asks once for its own
confirmation and is never to be sent down a pipe. Nothing typed at either prompt passes through the page;
when the verb ends, the page takes the screen again and shows what is registered now. A suspended
account is refused by LOGIN, ssh and the API; sessions already signed on in it keep running until they
end; nothing changes in Linux, so lifting the suspension costs nothing. `F5` reads everything again, `F1`
explains the page and `Ctrl-Q` leaves. Opening the page writes the audit line `tool start app=tool.accounts`.

### Every account against every gate: `tool.gates`

```
tool.gates
```

**The gate matrix** is a full-screen page for the administrator (SDSYS's VOC only; it
is refused, before anything is read, to anyone else: in every other account the same verb
is the account holder's read-only "what my account may do" page, described in the User
set under *What this account may do*). One row for each registered
account but SDSYS, one column for each gate the system has, in the order
`modify.account` carries them out: `ssh api sh os sd voc bp dict net sh-rd sh-wr files
f-wr f-adm ai sock`. A cell says **ON**, **off**, a **dash** (the gate does not apply
to this kind of account: ssh, api, files and ai are routes for a person, and a group or
other account has no Linux user of its own) or **plan** (not built yet; sockets). A star
after a cell is a change you have queued; the cell shows the state it would have.
Under the matrix a box says, for the cell under the cursor, what the gate is: its two
words, what ON allows, what OFF still allows, when a change reaches the person, whether
it reaches beyond SD and what it is as delivered. A second box lists the accounts that
have a gate on which reaches beyond SD, and a third the live sessions of the account
under the cursor.

| Key | What it does |
|---|---|
| arrows, a click | move over the cells |
| Enter or the space bar | queue the opposite state for the cell; again takes it back |
| R | run the queued changes of the account on the cursor's row |
| U | drop them |
| T | queue OFF for every gate of that account that is off as delivered and on now |
| F | change which accounts are shown: all, accounts of persons, accounts with a gate on that reaches beyond SD |
| F5 | read the machine again (a queued change is kept) |
| F1, `?`, a click on the `[?]` | explain the matrix |
| Ctrl-Q | leave |

**The page writes nothing itself.** The queued changes of one account become ONE
command, `modify.account name word word ...`, shown with its effect in a box that is
answered Run or Cancel (Enter alone is Cancel). The verb reads every word before it
changes anything, so a conflict is refused whole. After the command the page reads the
machine again and shows the verb's own words, so a cell changes because the system
changed, never because the page said so. Every change is audited by the verb as if you
had typed it.

* **There is no key that queues everything ON.** **T** is the only
  "all": it queues OFF for what is on and off as delivered (`shared-read`, which is on
  as delivered, is left alone).
* **Turning ON a gate that is off as delivered says so**, and says that leaving it off is
  the tighter choice. **Turning ON a gate that reaches beyond SD** (ssh, api, sh, os,
  sd, net, files, files-write, files-admin, ai) **asks for the account's name to be
  typed**; turning anything OFF does not.
* **ssh and api are one setting** in the verb: the words `ssh`, `api`, `both` and `none`
  SET the pair. The page therefore sends the one word that gives the pair of states you
  queued, and its box says which.
* **files-write needs files, and files-admin needs files-write.** A queue that breaks
  that is refused by the page before the box opens, and the verb refuses it again.
* **A group or other account cannot have `sh` or `os`:** the verb refuses them in both
  directions (a shell granted to a group would be a shell granted to whoever its Linux
  group admits). The page says so instead of queueing them.
* **A change does not reach a session that is already running.** The box says when it
  reaches the person: the next sign-on (voc, bp, dict), the next account entry (sh, os,
  sd, net, shared), the next login (ssh, api, files) or the next request (ai).
* **Home-screen settings are not gates and are not on this page:** `pins-on` / `pins-off`
  and the three start words are managed on the menu management page (`tool.menus`,
  below).

### The other keywords

| | |
|---|---|
| **`ssh`** \| **`api`** \| **`both`** \| **`none`** | what the account's remote access **is**. Absolute: `api` takes ssh away |
| **`sh-on`** \| **`sh-off`** | the `sh` verb |
| **`os-on`** \| **`os-off`** | `OS.EXECUTE`, the screen editors, the embedded Python, and operating-system paths outside the account's own directory (see above) |
| **`sd-on`** \| **`sd-off`** | the directories of other SD accounts the user could `logto` (see above) |
| **`voc-on`** \| **`voc-off`** | saving a change to a VOC (see *The edit switches*) |
| **`bp-on`** \| **`bp-off`** | saving a change to a program file, and compiling and cataloguing |
| **`dict-on`** \| **`dict-off`** | saving a change to a dictionary |
| **`recovery-on`** \| **`recovery-off`** | whether the `ide` keeps a recovery copy of text that was not saved (see *The recovery copy*). Not a gate; **off as delivered**; user accounts only |
| **`net-on`** \| **`net-off`** | the right to use a server defined for SDNet (see *The NET switch*) |
| **`shared-read-on`** \| **`shared-read-off`** | opening the files of the `shared` account by name. **On unless the field says no** (see *The shared account*) |
| **`shared-write-on`** \| **`shared-write-off`** | writing to the files of the `shared` account. Off unless the field says yes |
| **`files-on`** \| **`files-off`** | the files-only API login: membership of the Linux group `sdfiles` (see *The files-only route*). Independent of `ssh`/`api`/`both`/`none`: those words leave it alone |
| **`files-write-on`** \| **`files-write-off`** | the right to CHANGE files over the files-only login: membership of the Linux group `sdfileswrite`, which needs `files-on` first (`files-off` takes both away) |
| **`add`** \| **`delete`** *user* | put a Linux user in, or out of, the account's group |

**The first group is absolute and the second is not.** `ssh`/`api`/`both`/
`none` are four names for one state, so whatever is not named is withdrawn
(of ssh and the API: `files-on` is its own setting and is not withdrawn by them).
`sh-on` and `os-on` are two independent switches over two separate settings,
so **`sh-off` says nothing about `OS.EXECUTE`** and leaves it alone; the
other switches are each their own as well.

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
is read when a session signs in, and for `sh`, `os`, `sd`, `net` and the two
`shared` switches again when it `logto`s into the account (the three edit switches
are read at sign-on only),
so a session already open keeps what it started with. To take a grant away from somebody
who is signed in now, change the setting and then end their session.

**Every one of these words is written to the audit trail** (`modify.account
sh-on account=fred` and its siblings), and **SDSYS is never a target**: the
account name is refused as invalid before the word is read. A group account
is refused too for the `sh-on`/`sh-off`/`os-on`/`os-off` forms: it has no
Linux user to hold the switch.

**Upgrading keeps what accounts have.** The installer switches `sh` and
`OS.EXECUTE` on, once, for every user account that exists when you upgrade
(ssh and the API are left exactly as they were), so that nobody loses a
command they were using, and in the same way `voc-on`, `bp-on` and
`dict-on`, once, for the same user accounts. This happens when the installer
is run by the user whose own account already exists; a different OS user
installing over existing accounts does not run it. Group and other accounts
are left off on purpose. **`net-on` is not part of it**: nothing used SDNet
before, so every existing account has it off. **The `shared` switches are not part
of it either**: a blank field already reads as `shared.read` on and `shared.write`
off, which is how they are delivered, so every existing account can read the
`shared` account's files and none can write them (take the read right away with
`shared-read-off` before you put anything private there). **Neither is `files-on`**: the
`sdfiles` group is made empty, and nobody is in it until you say so. You can then turn them off one account at a time,
and a later install does not turn them back on. Only accounts made after the
upgrade start with everything off.

### The recovery copy: `recovery-on` and `recovery-off`

```
modify.account account recovery-on | recovery-off
create.account user <name> recovery-on
:modify.account fred recovery-on
Account fred keeps a recovery copy of unsaved editor text: yes
```

With `recovery-on` the `ide` of that account copies the text of every record it has changed and not
saved: after a second without typing, before it hands the screen to a program, and when the session
ends. A hung-up terminal, a lost connection or an abort then does not lose the text. **Since 28 October 2026
the copy sits in the person's own Linux home**, in `~/.local/state/sd/recovery/<account>/` (the home the
password database gives their Linux user, never the `HOME` variable), one file per record, readable only by
the person, **outside every account**; it is deleted when the person saves, closes or quits normally, and the
next time the record is opened the `ide` asks whether to use the copy, delete it, or leave the record
unopened (which keeps it). The record itself is never changed until the person saves. `sed` and `ced` keep
no copies.

* **Off as delivered.** `create.account` and an existing account have it off until you say so. `recovery-off`
  is the word for `modify.account` only (as `pins-off` is); `create.account` takes `recovery-on` alone, and
  the audit line of a `create.account` that used it ends `gates=` with `recovery-on` among the words.
* **User accounts only, as the verbs have it.** `recovery-on` for a group or other account is refused
  ("... is not a user account, and a recovery copy is kept only in a user account, for its own person; nothing
  was changed"). That was needed while the copies sat in a directory of the account that several people
  could replace; with the copies in each person's own home the technical reason is gone, and the refusal is
  now only a rule of the two verbs, kept until it is decided to allow the switch for those accounts. The
  administrator is not given a copy either, by the same rule.
* **Where, and when there are none.** The copies are made only when the person's home and every directory
  below it (`.local`, `state`, `sd`, `recovery`, the account's own) are real directories of that Linux user
  that nobody else can write, and every directory **above** the home belongs to root or to that user and
  cannot be written by group or other (a sticky one such as `/tmp` excepted). A home under a group-writable
  directory therefore gets no copies, and the `ide` says the copy could not be written; the text is still in
  the editor. A person who runs SD as root has no home that is trusted and gets none.
* **You cannot read the copies, by design.** `modify.account` runs as `sdsys`; the directories and the files are
  mode 700 and 600 for the person. `recovery-off` stops new copies; copies already made stay and are still
  offered to the person.
* **Copies the first version left.** A copy in the directory `$recovery` of the account (kept there until
  28 October 2026) is still offered once: with `recovery-on` it is moved to the person's home, with the
  switch off it stays where it is until the person answers (use it or delete it; leaving the record
  unopened keeps it).
* **When it reaches a session.** `recovery-off` stops new copies at once. A running `ide` learned at its start
  whether to keep copies, so `recovery-on` reaches it the next time the person starts the `ide`.
* **The copies are not part of the account.** `backup.account` archives do not contain them (they are in the
  person's home, not in the account), so a text that was not saved never ends up in a backup that
  the administrator can read; the person's own backup of their home does contain them. `restore.account`
  puts the account back with the switch it had.

### Where a session starts: `start-menu`, `start-terminal`, `start-default` and `set.start.default`

A session on a terminal starts either in the **home screen** (a screen of tiles: the
account's tools, a terminal, switch account and sign out; the User's guide has the
page `29a`) or at the **command prompt**. **You decide, account by account**, and you
decide what an account with no setting of its own does:

```
modify.account fred start-terminal       fred starts at the prompt, whatever the default is
modify.account fred start-menu           fred starts in the home screen, whatever the default is
modify.account fred start-default        fred follows the default (the register field is made empty)
set.start.default terminal               accounts that follow the default start at the prompt
set.start.default menu                   ... or in the home screen
set.start.default                        says which it is now
```

* **The default is `menu` as delivered.** `set.start.default` writes the word to the
  file `start.default` in the sdsys directory; the file is absent until you use the verb,
  and absent means menu.
* **EVERY EXISTING ACCOUNT HAS NO SETTING OF ITS OWN**, so after an upgrade each follows
  the default and starts in the home screen. To keep the old start for everyone, run
  `set.start.default terminal` (as SDSYS); to keep it for some,
  `modify.account name start-terminal`.
* The setting is **field 16** of the account's register record. `modify.account` writes it;
  nothing else needs to change, and it applies at the person's next sign-on, and when they type
  `logto` at the prompt to enter the account. It may be set on any kind of account.
* **It is not a wall.** Starting in the home screen confines nobody: its *Terminal* tile gives
  the ordinary command prompt (and `exit` comes back). To keep a person from a prompt you would
  need a setting that removes the prompt itself, which SD does not have.
* The screen is never given to a session that cannot use it: a window under 140 by 43, a pipe,
  a phantom, an API server, or a `logto` that a program ran with `execute`. Scripts and
  scheduled jobs are unchanged.
* `modify.account` says `Account fred starts at: menu` (or `terminal`, or `system default`) and
  `fred already starts that way; nothing changed` when the word is the one already set. It is
  audited as `modify.account start-menu account=fred`, and `set.start.default menu` is audited
  as `set.start.default menu`.
* `create.account` takes `start-menu` and `start-terminal` too, so an account can be made
  with its start in one command (see *Making an account*); `start-default` is not a word of
  `create.account` (an account made without a start word follows the default already).

### What the home screen shows: `set.tile`, `pins-on` and the menu management page

```
tool.menus
```

**Menu management** is a full-screen page for the administrator (SDSYS's VOC only; it
is also a tile on the administrator's own home screen). It lists every account but
SDSYS with where it starts, whether it may add its own programs, and the tiles turned
off for it; for the account you select it shows the standard tiles (the seven of the
account, the seven development tiles and the Recent group: 15 rows after the two settings
above them) with `[x]` on and `[ ]` off, and a box that says in plain words what the
settings mean. **It writes
nothing itself:** every change is the command it will run, shown with its effect in a
box you answer *Run* or *Cancel* (Cancel is the button Enter chooses), run by the same
verbs you can type, and the line under the page is the verb's own answer.
**Every setting has a `[?]` at the end of its row** (and one on the accounts list and on
the system default): F1 or `?` on the selected row, or a click on the `[?]`, opens a box
that says what the setting means, with a *Documentation* button that shows the
administrator's guide page in the PDF reader (`pdf`, see *Operating-system access*) and a
*Close* button, which is the one Enter chooses. The text is the record of that setting in
the file `context.help` of the shared account.

```
set.tile                          says which tiles are off, one line for each account that has any
set.tile account tile off         turn a tile off for that account
set.tile account tile on          turn it on again
modify.account account pins-on    the person may add their own programs to their home screen
modify.account account pins-off   they may not (the delivered state)
```

* **Tiles are on as delivered and are turned off one account at a time**; there is no
  setting for every account. The standard tile ids are `editor`, `ide`, `ced`,
  `terminal`, `keys`, `switch` and `signout`, the seven development tiles (`files`, `voc`,
  `dict`, `query`, `bulk`, `catalog` and `test`) and `recent`, which is not a tile but the
  Recent group (below): 15 ids, the ones the page draws and the rows of the *Menu* box of the
  menu management page. **Sign out cannot be turned off**: a person must always be able to
  leave. Any other id is accepted and said not to be standard (it would apply to a tile of
  that name in a page of the account's own).
* **`recent`: the Recent group.** A group at the top of the home screen with the tiles the
  person started last, newest first, six at most. **It is off as delivered, and it is the
  person's to turn on** (the *Recent group* entry of the View menu of their home screen); it
  keeps its list in the person's own file `&menus&`, as the record `recent`, and writes
  nothing while it is off. **`set.tile account recent off` is the administrator's wall:** the
  group is then not on that account's page, nothing is read or written for it, and the View
  entry cannot be chosen; the list the person kept stays in their file, and `set.tile
  account recent on` gives the choice back (it does not turn the group on). The list holds
  tile ids and never a command: each recent tile is built from the page as it is, so a tile
  that is off for the account is not offered, and a record edited by hand cannot make the
  page start anything it does not already offer.
* **Sub-menus.** The home screen can open a second page of tiles from a tile, with a Back
  tile, Esc and the path on the status line (the User's guide, page 29a). The delivered page
  declares none, so there is nothing for you to set; a tile of a page of your own that opens
  one is declared in the page table of the `home` program, not in a file.
* The setting is **field 17** of the account's register record (tile ids separated by
  spaces). A tile that is off is not on the page, its menu entry cannot be chosen, and a
  group with no tile left has no heading. It takes effect when the home screen is next
  built (sign-on, F5, Switch account).
* **The Terminal tile off is a wall for an account that starts in the home screen**: the
  screen never leaves the person at the command prompt, whatever ends it, and signs them
  out instead (a window too small to take the screen ends the session after the message).
  An account that starts at the prompt (`start-terminal`) keeps it. **It is a wall only for
  the prompt the screen gives**: the programs behind the other tiles are the account's own,
  so an account that is to be kept to the screen should have the editor, IDE and record
  editor tiles off as well, and a command that gives a shell needs `sh-on`, which is off as
  delivered.
* **`pins-on` is off as delivered.** An account that has it gets a group *My programs* on
  its home screen and the verb `my.menu`, with which the person adds **their own**
  programs (a label and a command they could type at their prompt): they manage only
  their own list, never the standard tiles, and a program of theirs adds no access. It is
  **field 18** of the register record, and the administrator always may. `pins-off` hides
  the group and `my.menu` refuses; the list stays in the person's file.
* `set.tile` says `Tile ide is now off for fred` (and `... was already off ...; nothing
  changed`) and is audited as `set.tile off tile=ide account=fred`; `modify.account` says
  `Account fred may add its own programs to the home screen: yes`.

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

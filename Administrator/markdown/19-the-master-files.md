Title: The Master Files
Subtitle: How the administrator manages every account's VOC entries, dictionary items and programs from SDSYS, in the account each one belongs to: the page tool.entries, the account-scoped run run.in, and what the sdsys user needs to write into an account.

**The administrator manages every account's VOC entries, dictionary items and programs from one
page, `tool.entries`, and each one is changed in the account it belongs to.** Nothing is copied: the
page reads the accounts' own files, and an edit, a delete, a compile or a debug happens on the real
record, in its own account. That is the purpose of the master files: most accounts can be locked out
of editing their own VOC, dictionaries and programs (the edit gates `voc-edit`, `dict-edit` and
`bp-edit`), and the administrator does that work for them.

> **From 2.0-0 there are no master copies.** The development of 2.0-0 first kept a copy of every
> account's VOC and dictionary records in the SDSYS account (`voc_master`, `dict_master`,
> `master_state` and a journal, with the verbs `sync.masters`, `check.masters`,
> `list.master.pending` and the page `tool.masters`). Those were retired on 2 November 2026, before
> any release had them: see [What went with the copies](#what-went-with-the-copies) below.

> **Read this first: what the grant is, and what it is not.** To write into an account's own VOC,
> dictionaries or programs, **the `sdsys` operating-system user has to be a member of that account's
> Linux group (`sdu_`*name*), and the account's files have to be writable by that group.**
> **As delivered, `sdsys` is a member of every user account's group** (from 1 November 2026; it was
> none from 26 October), so the administrator's edits reach a user account. The administrator can take
> it away **for one account**: `modify.account acme sdsys-off`; `modify.account acme sdsys-on` puts it
> back. The membership gives the `sdsys` user **write access to everything the account's group
> may write** - not only the VOC and the dictionaries (files that SD sessions create are group-writable
> under SD's usual umask, 002) - and it is also, as far as the modes and the group show, what lets SDSYS
> write inside the account in any other way (`logto` and an editor, an interactive `update.accounts`);
> that follows from the modes and the group. A VOC entry or an I-type is code that
> runs in the account, so **while it is on, a compromised `sdsys` login can change what that account
> runs.**
>
> **It is a default and a record of the administrator's decision. It is not a wall.** A person who has
> taken over the `sdsys` login can reach the code of every account without any membership, by two
> routes that this does not change: **the global catalogue is the `sdsys` user's to write**, and every
> session loads programs from it; and **`sdsys` may run `sudo /usr/local/sbin/sd-elevate` with any
> arguments**, which can put `sdsys` back in a group, give it a group account's files, set the first
> password of a user SD made, or add a person to an account's group (from 2.0-0 the helper no longer
> takes a user account's directory, `voc` or `%0`, nor the password of a login SD did not make or that
> already has one; see [The installed scripts](09-the-installed-scripts.html)). (A third route, that the
> files `root` runs - `bin/sd`, `bin/sdlnxd`, `bin/sdidx` and `bin/pcode` - belonged to `sdsys`, is
> closed from 2.0-0: the installer makes them `root`'s, see
> [Installation and the daemon](08-sd-installation.html#the-files-root-runs). The other two are not
> touched by that.) So
> **do not read the switch as protection against a stolen `sdsys` login: it is not tighter against
> one.** What it does is make the choice visible and the administrator's: `sdsys-off` and `sdsys-on` leave
> an audit line (`modify.account sdsys-off account=acme`) and a line in the system log (`sd-elevate`), and
> each can be taken back. How much further protection the machine needs is the administrator's to
> decide (the owner's ruling of 1 November 2026: simplicity first). It is not a route in from the
> network (`sdsys` has no remote access at all), and a process that is not a real `sdsys` login is not
> an administrator.
>
> From 2.0-0 the membership is **on as delivered** for every user account (it was off from 26 to 31
> October of the development). `create.account` puts `sdsys` in a new account's group; an install puts it
> in the group of the accounts that are already there, once, and records that in `/home/sd/$sdsys.access`,
> so a `sdsys-off` you give afterwards stands.

## The entries of every account by pointer: `tool.entries`

**`tool.entries`** is the page that looks at the accounts' own files and copies nothing: it is in the SDSYS VOC only and
refuses anyone else before it reads anything. **It lists the VOC entries, the dictionary items and
the programs, and it edits, deletes, compiles and debugs each in the account it belongs to** (below).

```
tool.entries
```

*Accounts* (left) lists every registered account but SDSYS with **the gates it holds**, shown as
`v d b` or a dash: `voc-edit`, `dict-edit` and `bp-edit`, the rights to save a change to its VOC,
its dictionaries and its programs. A dash is what locks an account out of its own files; an
administrator is not held to them. The next column says whether **the `sdsys` user is in the
account's group** (`modify.account` *name* `sdsys-on` puts it there), and the last whether the
account is suspended. *Entries* (right) lists the VOC of the account under the cursor, in name
order, with each entry's type and what it points at; **`K` switches to the dictionary items** of
the files its VOC points at (the dictionary path of each file pointer), each with its file, id,
type and column heading, **and again to the programs**: the program files of the VOC (a directory
file named `bp`, or ending `.bp`, or with a `.out` file beside it, as `tool.catalog` finds them) and
the record of each, with **Built**, which says `yes` when the compiled program is in the `.out` file
under the same name and `-` when it is not. The `.out` file is the one the VOC names, or else the
one beside the program file. A third `K` is back at the VOC. Under the two lists the entry under the
cursor is shown field by field.

**The VOC of an account is read when the cursor comes to the account**, from the account's own
file by the pathname the register gives, so a system with many accounts is not read as a whole.
`/` keeps the entries whose id holds a part you type; in the dictionary items it also looks in the
column heading, so `/ first name` finds the items headed "First Name" whatever they are called.
**`F` finds a part of an id, or of a heading, in the VOC or the dictionaries of every account**: it
reads them all, so it runs only when you ask, and the box then lists the hits with their accounts;
Enter on a hit goes to that entry in its account. Esc takes the find and the filter off, F5 reads
again, Tab changes box, F1 or `?` explains the box. An account whose VOC cannot be opened is
listed and says so. At most 3,000 entries or hits are listed, and the page says when there were
more.

**A pointer is not followed to change what it points at.** A `>` in the second column marks a
pointer whose target lies **outside the account being listed**: a file pointer whose data or
dictionary is in another directory (the shipped ones lead to `@SDSYS/voc.dic` and the like), a
Q-pointer to another account, a remote item, a program file that lies outside the account. The
test is the kernel's own, so `..` and links do not
make a path look inside. For a VOC entry the pointer is the account's own record and is edited like
any other (change `@SDSYS/voc.dic` to another directory, and it is changed); what it points at is
never edited from this page. A dictionary item marked `>` lives in another account's dictionary,
SDSYS's included, and is only read through this account's pointer: it is edited in the account it
lives in.

**`E` edits the record under the cursor and `N` makes a new one, in the account it belongs to.** In the
VOC view they edit **VOC entries only**: the record of the VOC, as text, never the file a pointer
leads to. In the dictionary view they edit **dictionary items only**, as the item form (the
programs are below). The terminal is
given to the editor on that one record and comes back to the page when the editor ends; `N` asks the
id first (for an item, the dictionary is that of the file the row under the cursor belongs to). An
account with `voc-off`, `dict-off` or `bp-off` is edited all the same, because an administrator is
not held to those gates; that is what they are for. A suspended account is edited too: SD lets
the administrator follow the pointer into it. For the length of the edit SDSYS's VOC holds
one temporary file pointer, `zm`*user number*`.`*account*`.`*file*, which holds the path the page
has just checked and lets the editor reach that file; the page takes it away when the editor ends.
It is not a Q-pointer into the account's VOC: that would be followed again each time the editor
opens the file, after the check, and an account allowed to write its VOC could repoint the file in
between. If the session is killed inside the editor the pointer stays, and the page takes it away
the next time it starts in a session with the same user number.

**The rule is asked before anything is made.** At the keypress the page reads the register and the
account's own VOC again (the list may be old) and asks the kernel whether the file to be edited
lies inside the account, and then asks it again of what the pointer opens, the file's two
subfiles included (a directory of the account's own whose subfiles are links to another
account's is refused), and that file must be a hashed file. A dictionary that lies
outside the account is refused with its reason (`the dictionary of zeesc lies outside ze1: it is
edited in the account it lives in, not from here`), so a VOC pointer written `../other/dict.dic`, a
link to another account's directory, and the shipped system dictionaries cannot be edited from
another account's row; nothing is written, no pointer is made and the audit trail has no line. The
pointer record itself is the account's own record and is edited like any other: a Q-pointer that
leads to another account can have its text changed, and the other account is not touched. The
editor is a general editor; the page decides what it is given first, not what the person opens
next inside it.

Each edit that reaches the editor writes one line to the audit trail, for example
`master edit account=ze1 kind=voc file=voc id=zzonly1 new=0` (`kind=dict` and the file's name for an
item, `new=1` for `N`); the page's other line is `tool start app=tool.entries`.

**`D` deletes the record under the cursor**, a VOC entry in the VOC view or a dictionary item in the
dictionary view, in the account it belongs to. It goes the same way as `E`: the register and the
account's VOC are read again, the rule above is asked, and the file is reached through the same
temporary pointer and judged again with its subfiles, so an item of a dictionary that lies outside
the account is refused with its reason before anything is shown. The record is then read with its
update lock: a record another session holds (someone editing it) is refused, `zz1 in the VOC of acme
is locked by user 12 (an editor holds it): it is not deleted`. Otherwise a box titled `Delete this
record?` names the record, the account and the file's path; `Cancel` is the default, and `Run` asks
for the record's id to be typed. Only the exact id deletes it; Cancel, Esc or a different id leave
it where it is (`nothing was run`). The page deletes that one record itself, through the file it
judged, and runs no command. A delete writes one line to the audit trail, for example
`master delete account=ze1 kind=voc file=voc id=zzdel1`.

**`D` in the programs view deletes the program and its compiled program.** It goes the same way: the
program file and the program's own file must lie inside the account, the program is read with its
update lock, and its id is typed in the box. The compiled program is found by its name, as the
Built column finds it: the record of the same name, in lower case, in the `.out` file the account's
VOC names for the program file (`bp.out` for `bp`), or else in the `.out` file beside the program
file. The same rule holds for it: when that `.out` file, or the compiled program's own file, lies
outside the account (a link to another account's `bp.out`, say) the whole delete is refused with
its reason (`the compiled programs of zeob.bp lie outside ze1: zwob is deleted in the account they
live in, not from here`), before the box and before anything is deleted. The box names the
compiled program, or says there is none; the page deletes the program, then its compiled program,
through the files it judged, and runs no command. **A catalogue entry of the program is left**: it
is the account's (a private catalogue holds its own copy, so the program can still be run by its
catalogue name), and the box says so; remove it in that account, for example
`run.in ze1 delete.catalog prog` for a private catalogue entry or `run.in ze1 decatalog prog` for a
local one. The audit line is `master delete account=ze1 kind=bp file=bp id=prog object=deleted`
(`object=none` when there was no compiled program, `object=failed` when the `.out` file refused the
delete).

**In the programs view, `E` and `N` open the program in the editor and `C` compiles it, in the
account it belongs to.** `E` and `N` go the same way as for a VOC entry: the program file must lie
inside the account (a program file reached through a pointer to another account, marked `>`, is
refused), and so must the program's own file: a program that is a link to a file elsewhere is
refused, and so is a name that is a link leading nowhere, because writing it would create the file
at the other end. The temporary pointer reaches the program file's data only. The editor is told
which account the program belongs to, so its **Compile** (F8) and **Compile and catalogue** (F9)
do not run BASIC in SDSYS through the pointer: they run `run.in` (above) in that account, so the
object goes into the account's own `bp.out`, a `$catalog` line in the source is not acted on, and
the catalogue is the account's. Its **Debug** (F7, and Debug from the first line) compiles the
program for the debugger and runs the debugger in that account, the same way (`run.in … basic …
debugging`, then `run.in … debug …`), and the breakpoints marked in the editor's gutter are handed to
that debugger as they are for any program (F7 runs on to the first of them, and the lines that
still have a breakpoint come back to the editor); **Run** is refused in the editor (run it in its account).
**`B`** on the page debugs the program under the cursor the same way: a compile that fails is shown
as `C` shows it and nothing is debugged; otherwise the terminal goes to the debugger, and when it
ends the page asks you to press Enter and comes back on the same program. The page writes `master
debug account=ze1 file=bp id=prog`. **`C`** on the page compiles the program under
the cursor the same way and shows what the compiler said in a box; the Built column follows. The
page writes `master edit account=ze1 kind=bp file=bp id=prog new=0` for an edit and `master compile
account=ze1 file=bp id=prog result=ok` (or `failed`) for `C`; `run.in` writes its own `run.in begin`
and `run.in end` lines for each compile.

## Running one command inside an account: `run.in`

A program is compiled, catalogued and debugged in its own account: its VOC, its private catalogue,
the files its I-types translate through. An account that is locked out of its own programs
(`bp-off`) cannot do any of that, so the administrator does it for the account.

```
run.in acme basic bp prog
run.in acme basic bp prog debugging no.query
run.in acme catalog bp prog local no.query
run.in acme decatalog prog
run.in acme delete.catalog prog local
run.in acme debug bp prog
run.in acme compile.dict cust total
```

The verb is in the SDSYS VOC only and refuses anyone else ("Command requires administrator
privileges"). It runs **one** command from the list above, in a **registered** account (never
SDSYS itself, never a path), and **it is back in SDSYS when the command ends**. That includes a
command that aborts, a break and a run-time error in a program being debugged: the session is put
back before anything else happens and says so ("run.in: the command did not finish; the session is
back in account acme"). `LOGTO sdsys` is refused for everybody, so without this an administrator
who had gone into an account would have no way back for the rest of the session.

What it checks before it changes anything: the account and every name are one plain word (a-z,
0-9, dot, dash and underscore, a letter or digit first, at most 64 characters, and not a word SD
reads as an option); each option is on that command's own list and is given once; the first name of
`basic`, `catalog`, `debug` and `compile.dict` is a file in **that account's** VOC. **The command
SD runs is built from those words and is never the text you typed.** **`basic` is always given
`no.catalog`**, so a `$catalog` directive in the account's source (or in a file it includes, or in
its `$BASIC.OPTIONS`) is not acted on: without it, compiling the source as the administrator would
catalogue it as the administrator, in the global catalogue if the directive says `global`. To
catalogue a program of an account, say so: `run.in acme catalog bp prog`. `run.in` does not start the
account's `login` paragraph (it would run with the administrator's rights), and it does not nest.

It adds no authority: the administrator can already `logto` into any registered account. What it
adds is the way back and a shorter list. Every use writes `run.in begin account=… command=…` and
`run.in end account=…` (or `run.in revert account=… reason=abort`) to the audit trail, and a
refusal writes `run.in refused …` with the reason.

## Who is in the group, and what the files must say

A write into an account (an edit, a delete or a compile from `tool.entries`, a save in the editor it opens) needs the `sdsys` user in the account's group **and** the account's files writable by that
group. **As delivered both are arranged for a user account** (from 1 November 2026, below). The state
*is* the Linux group membership, as it is for `ssh` and the API (`sdssh`, `sdapi`); nothing is written
to the register, and there is no row for it in the gate matrix (`tool.gates`).

**`modify.account` *name* `sdsys-on` and `sdsys-off`** (a user account only; a group account has no
group of its own for the `sdsys` user and is refused: it owns the files of a group account, so it needs
nothing):

```
modify.account acme sdsys-on
modify.account acme sdsys-off
```

* **`sdsys-on`** puts the `sdsys` user in the account's group (`sd-elevate sdsys-join`) and then makes
  the account's VOC and dictionaries group-writable (`sd-elevate group-write`). It says `Account acme:
  sdsys-on done. The sdsys user is in the group of the account, so SDSYS can write everything that
  group may write. Sign on again as SDSYS; a session already running does not have it`. **It can be
  said again**: for an account that is already on it runs `group-write` again, which repairs a mode (a
  VOC or dictionary that arrived by `restore.account` or a copy at the operating system level) and
  changes nothing else. The state it prints is read back from `/etc/group`: a read back that does not show the
  wanted state is reported as a failure, never as a success (`Account acme: ... failed, status 2`).
* **`sdsys-off`** takes the user out (`sd-elevate sdsys-leave`) and says `Account acme: sdsys-off
  done`. For an account that is already off it says `acme already had that access; nothing changed`.
  **It does not end a session of SDSYS that is already running** (a process keeps the groups it started
  with), so that session keeps its write access until it ends.
* **A session of SDSYS that began before a join does not have the group either.** `tool.entries` shows
  such an account as **`relog`** in its SDSYS column (not `yes`), and refuses **E**, **N**, **D**, **C** and
  **B** on it at once: `SDSYS cannot write inside acme from this session: the sdsys user joined its group
  sdu_acme after the session began. Sign on again as SDSYS`.
* If the group the register names cannot be used, `sdsys-on` and `sdsys-off` say so and change nothing:
  `Account acme: the members of the group sdu_acme could not be read (status 2); nothing was changed`, or,
  for a group name that is not valid, `Account acme: the account register does not name a valid group for
  it; nothing was changed`.
* The two words conflict only with each other (`modify.account acme sdsys-on sdsys-off` is refused,
  nothing changed) and may be given in a command with other words. Both are audited, in lower case:
  `modify.account sdsys-on account=acme`, and `sd-elevate` writes a line of its own to the system log
  (`journalctl -t sd-elevate`).
* **`create.account` and the installer switch it on** for a new account (from 1 November 2026): the
  installing user's account is delivered on like every other. `sdsys-off` takes it away from one.

**What is expected to stop working when an account is off.** An edit, delete or compile from `tool.entries` into it. So
is **SDSYS writing inside the account in any other way**: `logto` the account and make a file, edit a
program, catalogue; an interactive `update.accounts` for it (`update.accounts
all` skips such an account and says so, see [Account maintenance](01a-account-maintenance.html)); `sd -A`*account* from the operating
system. (The installer's own `update.accounts all` runs as root and is not affected.) `create.account`,
`delete.account`, `backup.account`, `restore.account`, and reading the
account (`logto` and a listing, `tool.entries`' lists) are done by the root helper or only read the files, and are expected to
work. Before 2.0-0 that general write was there for every account, because the membership was; switch
the account on for the time SDSYS needs to work inside it.

**A new user account** gets its group `sdu_`*name* from `create.account` with `root` and the user as
members, and `create.account` then puts the `sdsys` user in it (`sd-elevate sdsys-join`; if that fails the
account is still made, and the message says so and names the repair, `modify.account `*name*` sdsys-on`). A **group
account** is made with `root` and `sdsys` in its group `sdg_`*name* and is owned by `sdsys`, so it needs
nothing. **`delete.account` needs nothing**: the group goes with the account.

**The install and every upgrade** make one decision, **once**: they put the `sdsys` user in the group of
every **registered** user account that does not list it - an `sdu_`*name* group whose account the
register holds, with that same group on its record - and make that account's VOC and dictionaries
group-writable at the account's **registered** place (`sd-elevate sdsys-join`, then `group-write`).
**There is no question.** An `sdu_` group that no registered account owns is left alone and named in one
line (`Left alone, no registered SD account owns them: ...`). Each account joined is printed (`the sdsys
user is now in the group sdu_acme`), and then the installer writes the marker `/home/sd/$sdsys.access`,
so that the administrator's later `sdsys-off` or `sdsys-on` stands: with the marker present the installer
does not touch a group. **If a join or a repair the helper was asked to make failed, the install warns
(with the command that repairs it, `modify.account <account> sdsys-on`), goes on, and does not write the
marker**: running the installer again tries again. An account registered **outside**
`/home/sd/user_accounts` and `/home/sd/group_accounts`, with **no path**, or at a path that **does not
exist** is joined but its modes are not repaired (the helper repairs only those two places); it is named,
with the reason, in a warning of its own, and does **not** hold back the marker - set its modes by hand
(`chmod g+rw`, setgid on the directories). The marker is in `/home/sd`, not in the
sdsys directory, because `deletesdcore.sh` removes the sdsys directory in every cycle and would lose it;
`/home/sd` is kept with the accounts and removed with them. (It is a different file from the one the
26 October development used, `$groups.ruled`, so an install made then gets this once too. Only groups
named `sdu_`*name* are looked at; `sdusers` and a group account's group never are.)

**Three `sd-elevate` verbs do the work, each confined**, and none is more than `modify.account` and the
install need. Each leaves a line in the system log (`logger -t sd-elevate`) after it has changed
something:

| `sd-elevate` | does | refuses |
|---|---|---|
| `sdsys-join sdu_`*name* | puts the user `sdsys`, **and no other user**, in that group (`usermod -aG`: it adds, it never replaces) | any group that is not `sdu_`*user* of an SD user who exists (not `sdusers`, not a route group, not `sdg_`, not `sdu_root`, not `sdu_sdsys`), a group that does not exist |
| `sdsys-leave sdu_`*name* | takes the user `sdsys`, **and no other user**, out of that group (`gpasswd -d sdsys`: it removes that one membership and no other); a group that does not list `sdsys` is answered `sdsys is not in sdu_`*name* with exit 0 and left as it is | the same groups as `sdsys-join`, and the same user part; the user is written in the helper, never an argument and never taken from the environment |
| `group-write` *account directory* | gives the account's own group write on its VOC and its dictionaries (g+rwx and setgid on the directories, g+rw on the files in them) | an account directory that is not a direct child of `user_accounts` or `group_accounts`, or whose group is not `sdu_`*name* (`sdg_`*name* for a group account): never `sdusers`, which every account is in |

`sdsys-join` and `sdsys-leave` change one membership of one user and nothing else. `group-write` changes modes only, never owners or groups. It works on file descriptors opened
without following links, so a link a user plants in the tree cannot make root change another file;
it changes only what has the account directory's owner (or `sdsys`) and the account's own group,
leaves the other bits as they are, and does not leave the account directory's filesystem. It says
what it did, and a second run changes nothing.

### The modes of what SD makes

Every session starts with a `umask` of 002, so a VOC or a dictionary made in the ordinary way is
already group-writable (664 files, 775 directories). A user who changes the umask (the `umask`
verb) would make them closed, so **SD gives a VOC or a dictionary that it has just made its group's
write bit, whatever the umask**: the directory g+rwx and setgid, `%0` and `%1` g+rw. It does so
**only where the account's own directory lets that group write** (if the directory is 755, nothing
is added: a group that cannot write the account directory is not given the VOC), **and only where
the `sdsys` user is in that group** (from 2.0-0: where the account is off, group
write on a new VOC or dictionary would serve nobody, and nothing is forced), only to what the
session itself has just made, and it adds group bits and takes nothing away. The data file next to
a dictionary is not touched. A VOC or dictionary that arrives some other way (`restore.account`, a
copy at the operating system level) keeps the modes it came with: `modify.account` *name* `sdsys-on` (`sd-elevate
group-write`) puts them right, the ones made while the account was off included.

## Accounts being made, restored and deleted

* **`create.account`** makes the group of a user account with `root` and the user in it and then puts
  the `sdsys` user in it (above), so the administrator's edits reach the new account at once.
* **`restore.account`** replaces an account's files at the operating system level and does not change
  their modes: a VOC or dictionary that the archive did not keep group-writable is put right by
  `modify.account` *name* `sdsys-on` (`sd-elevate group-write`).
* **`delete.account`** needs nothing: the group goes with the account.
* **`update.accounts`**, like every other writer, needs nothing more.

## What it does not do

* **It is not a wall against a stolen `sdsys` login.** See "Read this first" above.
* **It does not change what a pointer points at from another account.** A pointer record is the
  account's own record and is edited like any other; its target is edited in the account it lives
  in, SDSYS's included.
* **It does not remove a catalogue entry when it deletes a program.** The entry is the account's;
  `run.in` *account* `delete.catalog` or `decatalog` removes it.
* **It does not see a change made outside SD** any differently from SD itself: the page reads the
  accounts' files when it is asked to, so a shell command's change is simply there at the next read.
* **On a machine with one operating-system user there is nothing for the membership to separate.**
  The rule rests on ownership and groups: the group membership and its two verbs, the modes, root
  changing only the account's own files, and the refusal of a write into an account that is off.

## What went with the copies

The copies kept in the SDSYS account during the development of 2.0-0 were **retired on 2 November
2026** (the owner's decision), because `tool.entries` edits the real records and the copies had
nothing left to do. Gone with them:

* the files `voc_master`, `dict_master`, `master_state` (each with its dictionary) and the journal
  `$master.journal` in the SDSYS directory. **The installer removes any of them it still finds**,
  by their exact names (a link among them is removed as a link, and what it points at is left), and
  says how many it removed. An upgrade (`deletesdcore.sh`, then the installer) starts from an empty
  SDSYS directory, so there is normally nothing to remove.
* the verbs **`sync.masters`**, **`check.masters`** and **`list.master.pending`** and the page
  **`tool.masters`**. They are on the VOC deletion list, so the next update of the SDSYS account
  (`update.accounts`, or the sign-on update) takes them out of an old VOC, keeping a copy:
  `list.voc.removed` shows them and `restore.voc` can put one back (it would find no program to run).
  **Use `tool.entries` instead.** The Master files tile of the administrator's home screen opens it.
* the kernel's hook, which noted every write of a VOC or dictionary record for the copies (it cost a
  test on every write), kernel key 150 (`K$MASTERS`) and the status 8910 of a refused save. The key
  and the status are not given to anything else.
* the scheduled-job ids `check-masters` and `sync-masters` of `sd-elevate job-set`, which ran the two
  verbs; `backup-all` and `update-accounts` are left. A job defined with one of the old ids is listed
  as damaged by `sd-elevate job-list`; `sd-elevate job-delete` removes it.

What did **not** go: the `sdsys` user's membership of the account groups and its two verbs, the group
write of a new VOC or dictionary, `run.in`, and the edit gates.

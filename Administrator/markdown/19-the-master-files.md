Title: The Master Files
Subtitle: How the administrator manages every account's VOC entries, dictionary items and programs from SDSYS, in the account each one belongs to: the page tool.entries, the account-scoped run run.in, and what the sdsys user needs to write into an account.

**The administrator manages every account's VOC entries, dictionary items and programs from one
page, `tool.entries`, and each one is changed in the account it belongs to.** Nothing is copied: the
page reads the accounts' own files, and an edit, a delete, a compile or a debug happens on the real
record, in its own account. That is the purpose of the master files: most accounts can be locked out
of editing their own VOC, dictionaries and programs (the edit gates `voc-edit`, `dict-edit` and
`bp-edit`), and the administrator does that work for them.

> **There are no master copies.** SD does not keep a copy of every account's VOC and dictionary
> records in the SDSYS account, and has no verbs `sync.masters`, `check.masters` or
> `list.master.pending` and no page `tool.masters`: see
> [What went with the copies](19c-the-master-files-group-and-modes.html#what-went-with-the-copies) below.

> **Read this first: what the grant is, and what it is not.** To write into an account's own VOC,
> dictionaries or programs, **the `sdsys` operating-system user has to be a member of that account's
> Linux group (`sdu_`*name*), and the account's files have to be writable by that group.**
> **As delivered, `sdsys` is a member of every user account's group**, so the administrator's edits reach a user account. The administrator can take
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
> routes that this does not change: **the global catalog is the `sdsys` user's to write**, and every
> session loads programs from it; and **`sdsys` may run `sudo /usr/local/sbin/sd-elevate` with any
> arguments**, which can put `sdsys` back in a group, give it a group account's files, set the first
> password of a user SD made, or add a person to an account's group (from 2.0-0 the helper no longer
> takes a user account's directory, `voc` or `%0`, nor the password of a login SD did not make or that
> already has one; see [The installed scripts](09-the-installed-scripts.html)). (A third route, that the
> files `root` runs - `bin/sd`, `bin/sdlnxd`, `bin/sdidx` and `bin/pcode` - belonged to `sdsys`, is
> closed from 2.0-0: the installer makes them `root`'s, see
> [Installation and the daemon](08a-sd-installation-file-modes-and-root-files.html#the-files-root-runs). The other two are not
> touched by that.) So
> **do not read the switch as protection against a stolen `sdsys` login: it is not tighter against
> one.** What it does is make the choice visible and the administrator's: `sdsys-off` and `sdsys-on` leave
> an audit line (`modify.account sdsys-off account=acme`) and a line in the system log (`sd-elevate`), and
> each can be taken back. How much further protection the machine needs is the administrator's to
> decide (simplicity comes first). It is not a route in from the
> network (`sdsys` has no remote access at all), and a process that is not a real `sdsys` login is not
> an administrator.
>
> The membership is **on as delivered** for every user account. `create.account` puts `sdsys` in a new account's group; an install puts it
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
again, F6 or Shift-F6 changes box, F1 or `?` explains the box. An account whose VOC cannot be opened is
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
through the files it judged, and runs no command. **A catalog entry of the program is left**: it
is the account's (a private catalog holds its own copy, so the program can still be run by its
catalog name), and the box says so; remove it in that account, for example
`run.in ze1 delete.catalog prog` for a private catalog entry or `run.in ze1 decatalog prog` for a
local one. The audit line is `master delete account=ze1 kind=bp file=bp id=prog object=deleted`
(`object=none` when there was no compiled program, `object=failed` when the `.out` file refused the
delete).

**In the programs view, `E` and `N` open the program in the editor and `C` compiles it, in the
account it belongs to.** `E` and `N` go the same way as for a VOC entry: the program file must lie
inside the account (a program file reached through a pointer to another account, marked `>`, is
refused), and so must the program's own file: a program that is a link to a file elsewhere is
refused, and so is a name that is a link leading nowhere, because writing it would create the file
at the other end. The temporary pointer reaches the program file's data only. The editor is told
which account the program belongs to, so its **Compile** (F8) and **Compile and catalog** (F9)
do not run BASIC in SDSYS through the pointer: they run `run.in` (above) in that account, so the
object goes into the account's own `bp.out`, a `$catalog` line in the source is not acted on, and
the catalog is the account's. Its **Debug** (F7, and Debug from the first line) compiles the
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

## Continued in

[The Master Files: Global Changes](19a-the-master-files-global-change.html) —
the global change of tool.entries.

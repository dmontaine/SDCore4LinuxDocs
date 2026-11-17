Title: Accounts and Security: The Edit Switches and the NET Switch
Subtitle: voc-on, bp-on and dict-on, and net-on and net-off.

This page continues [Accounts and Security: Making an
Account](01-accounts-and-security-2-making-an-account.html).

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
anything, and give the reason: `sed` and `ide` show it in their
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
stack commands on an existing VOC record. Making a new file is not asked. The private catalog
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
or cataloged by an account that has bp.edit"), because compiling is how a
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
message). What they do, and where `voc-on` stops, in an ordinary account:

* **`$private.voc`** (field 2 a file name) is a second vocabulary. A command
  word that is in no VOC record is looked for in that file, as typed, then in
  lower and upper case, **before** the private and global catalogs. It
  can add a command, and it can replace one that exists only as a cataloged
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
  cataloged subroutines) hands a VOC record whose type begins with a code to
  that subroutine **instead of SD's own handling of the type**. A code of `v`
  hands over every verb, including `off`; a blank code matches every record.
  It is read once, at sign-on, and `logto` does not read the new account's
  copy. A handler must already be cataloged, and cataloging needs `bp-on`;
  but `voc-on` alone is enough to switch on a handler that someone else
  cataloged. So an account with `voc-on` can change what the commands in its
  own VOC mean for every session that signs on to it, by way of a handler that
  you or somebody with `bp-on` put in a catalog.
* **If a handler locks an account out,** every command in the account,
  yours included, is handed to the handler, so the record cannot be removed
  from inside. It was removed by SDSYS signed on to the `sdsys` account, with
  an ordinary program that opened the account's `voc` by its pathname and
  deleted `$voc.parser`.

**Internal programs run only from the global catalog.** The gates on files
and on operating-system paths (these three and the shell, `OS.EXECUTE` and
`sd-on` gates before them) do not apply to a program compiled in *internal
mode*, which SD's own commands are. That mark is a bit in the program's own
object file, and SD used to believe it wherever the object came from, so a
user who could put an object file where SD would run it (a directory file with
a `.out` entry in the VOC, or a run file) could set the bit and skip every
gate. SD now honors the bit only for an object from the global catalog,
which only SDSYS can write, or for the administrator; for any other object the
bit is cleared when the object is loaded. SD's own commands are all in the
global catalog and are unaffected; a program that SDSYS compiled in internal
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

## Continued in

[Accounts and Security: The Shared Account and the Files-only
Route](01-accounts-and-security-4-shared-and-files-only.html) — the shared
account's switches and the files-only route.

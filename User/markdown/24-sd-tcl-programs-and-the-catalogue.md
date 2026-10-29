Title: SD TCL - Programs and the Catalogue
Subtitle: Compiling SD BASIC, running it, and giving it a name you can type.

Getting from source to something you can type is three steps: **compile it, put
it in a catalogue, then call it by name.** Only the first is compulsory.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part.

> **Every listing on this page was produced by running it**, on SD Core for
> Linux, against a two-line program in an account's `bp` file.

An account that SDSYS has not given `bp-on` cannot save a program to `bp`, and
`basic`, `catalog`, `delete.catalog` and `decatalog` are refused for it. A new
account starts without it; accounts that existed at an upgrade have it.

## Compiling

```
basic {file} record
```

The file defaults to `bp`. What comes back names the file and record, then the
error count:

```
basic bp zzprog
```

```
Compiling bp zzprog
WARNING: Final END statement is missing
0 error(s)
Compiled 1 program(s) with no errors
```

**A warning is not an error and the program still runs.** The line above is a
warning, the count says `0 error(s)`, and that program ran. **Read the count,
not the presence of output.**

`@system.return.code` is the number of programs compiled, and negative on a
fatal error.

**The object code goes into `bp.out`**, a separate file beside `bp`, one record
per program. **Its name is lower case even when the source record is not** —
a source record `ZZPROG` compiles to an object record `zzprog`. That is this
port's naming, and it is worth knowing before you go looking for the object by
the name you typed.

## Running without cataloguing

```
run {file} record
```

```
run bp zzprog
```

```
ZZPROG OK
```

`run` needs the file and record name every time. It is what you use while you
are still writing the thing.

## The catalogue is what gives a program a name

```
catalog {file {call.name}} {program | *} {local | global | pcode} {no.xref}
```

Catalogue it and the name becomes a command:

```
catalog bp zzprog
zzprog hello
```

```
ZZPROG added to private catalogue
ZZPROG OK
```

**The program sees the whole command line.** `@sentence` in the program above
read `zzprog hello`, so arguments arrive as typed and the program parses them
itself.

**A program run by its catalogue name takes `lptr` and `no.page` as `run`
does.** The words stay in the sentence for the program to see. A word in
quotation marks is not a keyword. This applies to a catalogue name only, not to
the name of a VOC verb.

### Three catalogues, and they are not the same

| | |
|---|---|
| **private** | the account's own. The default when no keyword is given |
| **local** | a VOC entry in the account, so the name works only there |
| **global** | `gcat` in the system account — **every account sees it** |

**Global cataloguing requires administrator privilege, and on this port that
means an SDSYS session** — logged in to the machine locally, as `sdsys`.
Without it you get *"Command requires administrator privileges"*. **The
same gate applies to an implicit global
catalogue** — one chosen by a `!`, `_` or `$` prefix on the call name
rather than by the `global` keyword — so the prefix is not a way round it.
The prefix characters `*` and `-` were removed in 1.2-0: `catalog bp *name` and
`catalog bp -name` are refused.

Private and local cataloguing need none of this and work in a programmer's own
account.

**`catalog ... local` asks before it overwrites.** When the VOC already holds a
local catalogue pointer under that name and it points at a different object
file, you are asked first (Return is no). `no.query` goes ahead without asking,
and cataloguing the same file again does not ask.

### Seeing and removing

```
map {all} {lptr {n}} {file {name}}
```

```
System catalogue map at 23:12:07 on 26 Aug 2026                    Page 1
  Catalogue name..................  Compiled.  Time....  ...Obj  ..Xref  ..Size
  ZZPROG                            26 Aug 26  23:12:07     189       6     195
                                                                Total:      195
```

`Obj` and `Xref` are the object-code and cross-reference sizes in bytes, and
`Size` is the total. An empty one says so:

```
Catalogue is empty
```

```
delete.catalog name... {global | local}
```

```
ZZPROG deleted from the private catalogue
```

```
decatalog {file} name ...
```

**`delete.catalog ... local` removes only the VOC entry**, and leaves the object
code it pointed to lying in the account's object directory. **`decatalog` removes
both** — the local catalogue entry and the compiled program it names:

```
catalog bp zzdocprog local
decatalog zzdocprog
```

```
zzdocprog added to local catalogue
zzdocprog deleted from the local catalogue
```

Several names may be given. A name that is not in the local catalogue is said so
(*zzdocprog is not in the local catalogue*) and the rest are still done; an object
file that cannot be deleted is reported as *Cannot delete the object code* and
the entry is gone all the same. A file name in front of the program name is
accepted and ignored, because the entry already holds the object's pathname.
`decatalog` works on **local** entries only — a private or global catalogue entry
is removed with `delete.catalog`.

> **`map` also takes a `file` option**, which writes the map to a file instead
> of the screen. **It asks before overwriting** — *"File xx will be cleared and
> overwritten. Continue (Y/N)?"* — so it is not usable from a script driving SD
> down a pipe.

## Which copy will run: `find.program`

```
find.program name {detail}
```

For the case where the system seems to run the wrong version of a program
because it is catalogued in more than one place. It looks in the three places a
program is loaded from, **in the order they are searched** — the local catalogue
(a VOC entry that points at the object file), the private catalogue (the
account's `cat` directory, or the directory `$PRIVATE.CATALOGUE` names) and the
global one — and reports every one that has it:

```
Program is in the local catalogue
   Compiled 10/15/26 20:56:03
   Subroutine with 2 arguments
Program is in the private catalogue
   Compiled 10/14/26 09:12:40
   Subroutine with 2 arguments
```

The kind is *Program*, *Subroutine with n arguments*, *Function with n
arguments* or *Class module*. `detail` adds the object code size in bytes and the
flags of the object (`internal`, `debug`, `recursive`, `trusted`, `case sensitive`,
`sdcall`). **SD's object code carries no compiler version and no source
pathname, so those two lines of openQM's `detail` are not there.** A name found
nowhere is *xx is not catalogued*. The name is looked for as typed; a global
program is named with its prefix (`!acc_hold`, `$listphan`).

## Formatting source

```
format {file} {record} {case}
```

`format` rewrites a BASIC source record with standard indentation. **It says
nothing at all when it succeeds** — no output is the success case, which is
worth knowing before you go looking for a confirmation that never comes. `case`
additionally applies case conversion.

With no record name it uses the active select list.

## Compiling dictionaries

```
compile.dict file {i-type}... {no.query} {no.page}
compile.dict local
compile.dict all
compile.dict data file {i-type}...
```

It compiles the A, I
and S-type entries in the dictionary of *file*; with no names it does all of
them, or uses the active select list if there is one. **The dictionary is the
default: write the file's name and nothing before it** (`compile.dict cust dbl`).

| | |
|---|---|
| **`compile.dict local`** | every dictionary in the account |
| **`compile.dict all`** | every dictionary visible from the account |
| **`compile.dict data file`** | reads the records of the file's *data* part as if they were dictionary items, and compiles those that look like one: a record whose first character is `I`, or `A` or `S` with something in field 8. Every other record is skipped without a word. It is for the rare file whose data holds items of that kind; on an ordinary data file a record that happens to begin with `I` is reported as a compilation error. Because it rewrites records it is held back by the edit gates as any change to a VOC, a dictionary or a program file is |

> **Do not put `dict` before the file name.** An older description of this verb
> gave the form `compile.dict dict file`, but the word is not understood as a keyword:
> `compile.dict dict cust dbl` answers *File dict not found*, because `dict` is taken to be
> the name of the file. `compile.dict cust dbl` is the command that compiles the item
> `dbl` of the dictionary of `cust`.

Compiling a dictionary is a performance step, not a correctness one: it is what
a query using those entries runs against.

## Named common blocks

```
list.common {all} {detail}
delete.common name
```

```
No named common blocks present
```

Named common survives between programs in a session, and `list.common` is how
you see what is holding memory. `all` additionally shows the system blocks and
is internal-only. `detail` puts the name of the program that created each block
beside its name, which helps when two programs disagree about the size of a block:

```
list.common detail
SCREEN.DATA  show.screen
SYS.FILES    myprog
```

The names are sorted on their own; the program is the one that executed the
`common` statement first, in this session.

## One screen for the lot: `ide`

```
ide {file {record}}
ide dict file {record}
ide voc {record}
ide path:/full/name
```

Opens a full-screen environment for BASIC programs and the other text records
of an account, built on the screen library. `ide file record` starts on that
record. **`ide dict file record` starts on an item of the file's dictionary and `ide voc record` on a
record of the account's VOC** (since 28 October 2026). A record that does not exist yet opens as a new,
unsaved one, after the account's gate allows it; **`creating.seqkey` in place of the record name takes the
file's next sequential id** (in quotes it is a record of that name). With a select list active,
`ide file` opens the first ten records of the list in tabs and lists them all. It needs a terminal and
**stops in a phantom**.

| part | what it is |
|---|---|
| menu bar | the top row; F10 or Esc opens it, and a click on a title opens that menu (since 19 October 2026; a click on the bar beside the titles does nothing) |
| tree | the account's files on the left (**the entries whose names start with a dollar sign - `$acc`, `$hold`, `$map`, `$release` - are not listed**, since 28 October 2026: they belong to SD itself). Return on a file lists its records (the first 2000, and a message says when there are more; a big file is no longer read whole first), and Return again closes the list. **A file that has a dictionary shows the dictionary as a node of its own under it** (since 28 October 2026), read only when you open it, and its items are listed the same way. Return on a record opens it. A letter jumps to the next entry that starts with it |
| editor | on the right, a tab for each open record. **While it has the focus the character at the cursor is shown in the highlight style** (as well as the terminal's own cursor being put there), so the place shows on a terminal that draws its cursor poorly. It is the text area `screen memo` uses, so its keys are `memo`'s: selection, cut, copy and paste, undo and redo, find, line numbers. Text is coloured as SD BASIC, C, Python, JSON, shell or Markdown **chosen as [SED](27a-sd-tcl-sed.html) chooses** (since 26 October 2026): by the name of the file, then the record id, then the first line - so a script with no suffix that begins `#!/bin/sh` is shell - and then the languages a site added in `&sed.syntax&`. **A horizontal scroll bar runs along its bottom row** (`<` and `>` at the ends, a thumb as long as the visible part is of the longest line; none to speak of when every line fits); clicking an arrow scrolls 8 columns and clicking the track a page |
| table | under the editor: the compiler's errors, or search results |
| pane marks | **`[*]` or `[-]` in the top right corner of each pane that can have the keyboard** (since 19 October 2026): the files (on the frame above the tree), the editor (on the frame above it), the tab strip (at its right end) and the messages (at the right end of their bar). `[*]` is on the pane that has the keyboard, `[-]` on the others; Tab moves it round in that order |
| status line | **the pane that has the focus** first, in brackets (`[Files]`, `[Tabs]`, `[Editor]`, `[Messages]`: Tab goes round them in that order), then the record, the cursor's line and column, and a star when there are unsaved changes |

| key | |
|---|---|
| F8 · Build, Compile | save and compile; the compiler's lines go in the table. Return on one goes to its line, F4 to the next |
| F9 · Build, Compile and catalogue | the build: compile and catalogue. *Catalogued* is said only if `catalog` added the program |
| F5 · Build, Run | compile and run |
| F7 · Build, Debug | compile with debugging and run the debugger |
| Ctrl-S · File, Save | save the record (an untitled buffer asks for its file and name first; an unchanged record says *No changes to save*). **Ctrl-S is the only save key**; F2 no longer saves |
| Ctrl-N · File, New record | a new record: the name form, then a buffer that is not on the disk until it is saved |
| Ctrl-O · File, Open record | the name form, for a record that exists; a file whose name starts with a dollar sign is refused |
| File, Save as | the name form; the tab becomes the new record and it is saved. The old record is as it was on the disk. It has no key |
| File, Write a copy | the name form; the text is written to another record and the editor stays on the record it had. It has no key |
| Ctrl-W · File, Close record | closes the record's tab; with unsaved changes it asks whether to save them, discard them or cancel |
| Ctrl-PageDown · Go, Next tab | the next record tab; Ctrl-PageUp (Go, Previous tab) the one before. **Alt-PageDown and Alt-PageUp do the same** (the second tab keys): GNOME Terminal keeps Ctrl-PageUp and Ctrl-PageDown for its own tabs, so use the Alt keys there |
| F6 · Go, Next pane | the keyboard goes to the next pane, as Tab does. **Shift-F6** (Go, Previous pane) goes to the one before, as Shift-Tab does |
| Go, Files and records | the keyboard goes to the tree. It has no key, because F3 is the text area's find next (below). From the editor, Shift-F6 twice reaches the tree (editor, tabs, tree); so does F6 twice (editor, messages, tree) when the AI pane is not open |
| F3 · Shift-F3 | with the editor focused, **find next** and **find previous** of the text last searched for |
| Ctrl-R · Search, Replace in the record | replace a text through the record |
| Search, Find in the records | find a text in every record of the file the tree is on (the first 2000 records, 500 lines), listed in the table; Return opens the record at the line. It has no key (F11 was it) |
| Ctrl-E · Go, Edit in SED | edit the record in [SED](27a-sd-tcl-sed.html) and come back (below) |
| F12 · Go, Edit as fields | edit the record as a tree of fields, values and subvalues in [CED](27b-sd-tcl-ced.html) and come back (below) |
| Tab · Shift-Tab | in the editor, **indent and outdent** the line or the selected lines (below); in the tree, the tabs, the messages and every form Tab moves to the next control as before |
| Go, Open the include | the record that the `$include` line at the cursor names, in a tab: one name is looked for in the file the tab is in and then in `syscom`, two words name the file; a collection-file record is passed over, and one that is not found says where it looked. It has no key |

**A bare `ide` opens "Untitled 1"** (since 28 October 2026): an editable buffer, coloured as a
program, with the cursor in it and the tree two keys away (Shift-F6 twice) or in the Go menu. Type, then save: **the name form** asks
for the file and the record id together. The file is filled in - the file of the record you are in, else
the file the tree is on, else `bp` - and the cursor
starts on the record id. If the account may not change that file (`bp.edit`, `dict.edit`, `voc.edit` or
`shared.write` is off; the form says which, and what SDSYS can do about it) or a record of that name
already exists, **the form says so and stays open** for you to correct it; Esc leaves it and nothing is
written. A new record or an untitled buffer is not written until you save it, and Compile, Catalogue,
Run and Edit as fields on an untitled buffer name and save it first - so a program can be typed,
compiled, fixed, saved and catalogued without leaving the IDE. **The write is made under the record's
lock**, and if the file refuses it (a trigger, a full disk) the IDE says so and your text stays in the
editor. A refusal by the edit gate on a save is shown whole in a box. **Catalogue reports "Catalogued"
only if `catalog` said it added the program**; otherwise its answer is shown in a box. In the editor the
up and down arrows stop at the first and last line.

**Each tab has a kind** (since 28 October 2026): a program, an item of a file's dictionary, a record
of the VOC, or a record of a data file. The kind decides the marks (below) and the gate that a save
asks: a program asks `bp.edit`, a dictionary item `dict.edit` and a VOC record `voc.edit`, as SED and
`ed` do, and the refusal is shown in a box that says which switch and what the administrator can do.
Compile and Catalogue on a dictionary item say it is not a program. A collection-file record is
refused with a message for now; a dictionary named in the New record form is not yet taken (use
`ide dict`).

**A record open in a tab is locked for as long as the tab is open** (since 28 October 2026), as in
SED. If another session already holds it the tab opens **read-only** and the status line says which
user holds it: it cannot be changed or saved, and Write a copy keeps its text under another name.
Closing the tab, quitting, a lost connection or any other way out gives the locks back; Run, Debug,
SED and CED keep them while they run. **An IDE left open therefore blocks other sessions and batch
writes on those records** until it is closed, AUTOLOGOUT ends it or the administrator's
`tool.sessions` page unlocks them. A new record is locked for its creation, and one that another
session is making is refused. Compile, Run, Debug and Catalogue work on a read-only tab that has no
changes (they save first only when there is something to save).

**A file of the operating system opens in a tab of its own** (since 28 October 2026): `ide
path:/full/name`, or `path:/full/name` typed in the *File* entry of Open (Ctrl-O) - or `path:` there and the
full name in the *Record* entry. **The name is the full path, as you typed it** (its case is not changed):
it starts with a slash, has no `.` or `..` part, no doubled slash and no control character, and a path with
blanks is fine on the command line. The tab strip shows `os` and the last part of the name; the status line
shows the whole path. The file must exist; **New, Save as and Write a copy do not take a path** (they say
so), and **compile, run, debug, catalogue, SED, edit as fields and open the include do not apply to such a
tab** (the IDE says why). How it behaves:

- **The account's gates apply, and the kernel asks them.** An account without the OS gate can open and save
  only files inside its own directory (a link inside the account that leads out of it is outside); an account
  with `os-on`, and SDSYS, can reach what the Linux user can. A file in a VOC, a dictionary, a program file or
  the shared account that the account may not change opens read-only. All of it is done by the program
  `!ide_osfile`, which is **not** an internal program, so the kernel puts the same questions to it that it puts
  to your own `openseq`, `readblk` and `writeblk`; the IDE itself contains no statement that opens a file.
- **It is written where it is.** Saving writes the new text over the file and cuts it to the new length: the
  same inode, owner, mode and links (a file renamed over it would change all four). The IDE reads the file once
  more just before it writes and asks *has been changed by someone else, Overwrite it?* (Cancel is the default)
  when it is not what it read - or is no longer text. If the write fails, a box says the file may be partly
  written and your text stays in the editor.
- **Bytes are not converted.** Lines end with LF, or with CR LF when *every* line does (then they stay CR LF); a
  CR anywhere else is an ordinary character shown as a reverse letter, and a tab is kept as a tab. Whether the
  last line had its line end is remembered: none is added to a file that had none. A file with a **NUL or a
  byte from 248 to 255** (SD's own marks), a file **over 2 MB**, a **directory, device, pipe or socket** is
  refused with a message; a file with **bytes from 128 to 247** (another character set, or UTF-8) opens
  read-only, as a record does.
- **The file is locked while the tab is open**, as a record is: a second session that tries to open it is told
  it is in use, and closing the tab (or any other way out) gives the lock back. A tab for a file you may not
  write (permissions, or an edit gate) opens read-only and says so.
- **No recovery copy is kept** for such a tab, whatever the account's switch: the copy would be kept in your
  home, and the file may be anywhere.

**A record that holds characters outside ASCII (bytes 128 to 247) opens read-only too** (since
28 October 2026): another character set's letters, or UTF-8. The editor shows such a character a byte at a
time and could not be trusted to keep it as it is, so Save, Save as, Write a copy, Replace, Edit as
fields and an AI edit are refused, in a box, and nothing is decoded or changed. The marks 248 to 255
are SD's own and go through the token form below.

**Tab and Shift-Tab indent and outdent in the editor** (since 28 October 2026): Tab puts blanks in up to
the next stop (every 3 columns) or, with lines selected, indents them; Shift-Tab takes the indent out;
each is one undo step and neither ever puts a tab character in. This is the IDE's editor only: a
program's own `screen memo` keeps its Tab. F6 and Shift-F6 move between the panes.

**If `autologout` is set** (the default is off) **the status line counts down the last 60 seconds** before
the session would be signed out: *Idle: signing out in 42 s*, followed by *; unsaved changes will be
lost* when there are any, or *; a recovery copy is kept* when the recovery copy below is on. Any key
stops it. It reads the same inactivity clock that `autologout` uses, so a wait for the AI counts.

Run and debug give the terminal to the program and come back to the IDE when
you press Return. **Nothing runs if the compile failed.** If somebody else has
changed a record since the IDE read it, saving asks before it overwrites;
closing a record, or leaving, with unsaved changes asks whether to save. **If the
IDE's input ends** (a pipe that has been used up; a terminal does not end like this)
it leaves at once and asks nothing, so unsaved text is not saved.

**Ctrl-E hands the record to SED, and SED's save brings you back** (since
18 October 2026). SED edits the record on disk, so a record with unsaved changes
is saved first: the IDE asks *Save them, then edit in SED?* and **Cancel**
leaves everything as it was. In SED you work as you always do; **the first
successful save ends the edit** and the IDE comes back with the new text in the
editor, the compile errors forgotten (they named lines of the old text) and a
line in the status bar, *Back from SED: bp prog is saved*. Leaving SED without
saving (Ctrl-Q) brings you back too, with the record as it was, and a record
that someone else holds locked opens in SED **read only**, with SED's own
message, as it does from the command line. There is no *press Return* pause on
the way back, which Run has because a program may have written something to
read. Ctrl-E is the editor's *end of row* key in other programs that use
`screen memo`; in the IDE it belongs to this and **End** ends a row.

**F12 shows the record as fields, values and subvalues, so that nobody types a mark**
(since 26 October 2026). The record in the open tab goes to [CED](27b-sd-tcl-ced.html) in its
*data mode*: a list of the fields, each field a text or a list of its values, each value a text
or a list of its subvalues. Dive into a field with Return, change a text with Return, add or
delete with **Ins** and **Del**; the value and subvalue marks are put in from the shape of the
tree when the record comes back. **Ctrl-S in CED keeps your changes and Ctrl-Q returns to the
IDE**, which puts the new text in the tab and marks the record changed (*Back from the fields:
bp prog is changed, save it to keep it*). **CED writes nothing and takes no lock: the IDE's
own save (Ctrl-S) does the saving**, with the edit gate and the overwrite question as for any other
change. Leaving CED without keeping anything, or answering *No* to its question, leaves the
tab as it was (*Back from the fields: bp prog is as it was*); if you pressed Ctrl-S and then
changed more, *No* gives you what Ctrl-S kept. With no record open, F12 says so.

**A record that holds marks is shown with the marks written as tokens** (since 26 October 2026), so
that nobody types one. Since 28 October 2026 this follows the tab's kind: **a dictionary item, a VOC record
and a record of a data file are always shown so, even one that had no marks when it was read**, so that a mark
can be typed into it; **a program never is**. A value mark is `@vm`, a subvalue mark `@sm` and a text mark `@tm`, joined to
the text beside them by a colon as in BASIC: the field *Don, Henry, June* with value marks between
is shown as `Don:@vm:Henry:@vm:June`. A mark at the start or the end has no text beside it
(`@vm:Henry`, `Don:@vm`), two together are `a:@vm:@vm:b`, and a text may hold colons
(`10:30:@vm:x`). **Type a token and it is a mark**: add `:@vm:Jules` to the end of that line, press
Ctrl-S, and the record on disk holds a fourth value. Reading accepts upper case (`@VM`); the editor
shows lower case. A token is the word on its own, at the start of the line or after a colon and at
the end of the line or before a colon, so `x@vm` is text. Field marks are the lines, as they always
were. The tab keeps the real record all the time; only the editor's text is converted, and only for
a tab of a dictionary item, a VOC record or a data record (a program tab never is, so a program
that mentions `@vm` in its source is never changed). The status line says *Marks are shown as @vm, @sm and @tm; typed so, they are read
back as marks* when a record opens this way. **A record with a field that holds the text of a token
- a field that is just `@vm` - cannot be shown so, because the text would be read back as a mark.**
It is shown as it is, with the marks drawn as the characters they are, and the status line says
*Marks are shown as characters: field 1 holds the text of a mark token*. Find in the records of a
file looks at the real records, and replace works on the real record, so neither matches a token;
the item mark is not converted.

**The AI in the IDE** (since 24 October 2026). When the AI is on for your account (see
[Asking the AI](29b-sd-tcl-asking-the-ai.html)) the IDE has an **AI** menu before Help and an
**`AI>`** row under the editor and the messages table (the table is one row shorter); without the AI
neither is there and nothing else changes. Tab goes round the panes to the AI row, or click it, or
use the menu:

| | |
|---|---|
| AI, Explain the error | asks the AI to explain the compile message the table has on its line, with the record |
| AI, Explain the selection | the same for the text from the mark (Ctrl-G where it starts) to the cursor; with no mark the status line says to set one and nothing is sent |
| AI, Ask about this record | puts you in the `AI>` row to type what you want |

Whatever you ask, Enter shows **everything that will be sent** first: the provider and model, the
fixed instruction, the record's lines (the whole record when it is under 24,000 bytes, else the
lines round the cursor, and it says which), the line they start at, and your request, with Send and
**Cancel, which is the default**. While the AI answers, Esc gives the request up.

The AI may answer with words and, if it was asked for a change, with **edits**. Each is shown as a
diff in the answer: `Change 1 of 2, at line 5:` and the old lines with `-` and the new with `+`.
**Accept** puts the changes into the editor as **one step** (one Ctrl-Z takes them all back) and
saves **nothing**; **Reject, the default, leaves the editor as it was.** The set is taken whole or
not at all: an old text that is not in the record, is in it twice, or overlaps another edit, more
than 8 edits, or a change that would show more than 30 lines, is ignored with a note and nothing is
offered. If you changed the record while the AI was answering, its change no longer fits and
nothing is applied. The IDE has nowhere to run a command, so a command in the answer is ignored.
Saving, compiling and running stay your own acts.

The other keys follow [SED](27a-sd-tcl-sed.html) where the two do the same:
Ctrl-Q quits, Ctrl-L goes to a line, Ctrl-X, Ctrl-C and Ctrl-V cut, copy and
paste, Ctrl-Z and Ctrl-Y undo and redo, Ctrl-F finds forward and Ctrl-B
backward (Return on the question repeats the last text; **F3 finds the next one and
Shift-F3 the one before**, as in other text areas) and Ctrl-R replaces a text through the record. **Ctrl-W is not SED's write-a-copy
key here: it closes the record**; Save as and Write a copy are in the File menu.
In the text area (the keys are those of `screen memo`; the [screen
library](12a-sd-basic-the-screen-statement.html) page has the list) Ctrl-A selects
everything, Ctrl-D duplicates the line, Ctrl-K cuts the whole line into the
clipboard, and a word back and on are Ctrl-P and Ctrl-U. The editor passes only
Ctrl-E (SED) on to the IDE.

On a UTF-8 terminal (`LC_ALL`, `LC_CTYPE` or `LANG` says UTF-8) the frame, menus
and scroll bars use line-drawing characters; elsewhere `+ - |`. The colours are
the blue theme.

**A recovery copy of text you have not saved** (since 28 October 2026), **if the administrator has turned it
on for your account** (`modify.account` *account* `recovery-on`, for a user account; it is off as delivered). Then
the IDE copies the text of every changed record after a second without typing, before it hands the screen to a
program, and when the session ends. **The copies are in your own Linux home**, in
`~/.local/state/sd/recovery/<account>/` (the home the password database gives your Linux user, never the `HOME`
variable), readable only by you and **outside every account, so `backup.account` never contains them**. They are
made only when your home and every directory below it are a real directory of yours that nobody else can write,
and every directory above the home belongs to root or to you and cannot be written by group or other (a sticky
one such as `/tmp` excepted): a home under a group-writable directory gets no copies. The copy is deleted when
you save, close or quit normally. If the terminal closes, the connection drops or the IDE is aborted, the next
time you open that record the IDE asks whether to **use the copy**, **delete it**, or **not open the record**
(which keeps it); a text typed in an untitled buffer is offered in a new tab. The record itself is not changed
until you save. A copy that the first version left in the directory `$recovery` of your account is still offered:
with the recovery copy on it is moved to your home, with it off it stays where it is until you answer. Turning
the recovery copy off does not delete copies that exist. `sed` and `ced` keep none.

**What it does not do:** it has no replace across records, no project files and no completion, and it does
not yet edit collection-file records, and it opens an operating-system file only by `path:` (it cannot make
one, save under another path or browse directories yet; SED's own `path:` form no longer opens one).

**The IDE is laid out for 140 columns by 43 lines or more** (it was 140 by 42
until 28 October 2026, and 60 by 16 before 18 October); a bigger window is used
whole. **A window smaller than 140 by 43 when the IDE starts is refused**, in words
(*IDE needs a window of at least 140 columns by 43 lines; this one is 100 by 30*),
and nothing is drawn; `ed` is the editor for a small window. The window measured is
the one on the screen, or the display `term w,h` gave if that is smaller. The last
three rows are the IDE's foot, the same as the toolkit pages': the status line, a
border and a row of function keys (Esc menu, F1 help, Ctrl-S save and the build
keys; the row is cut at the right edge of the window, the keys named first
staying).

**If the window is made smaller than that while the IDE runs, the IDE locks**,
whatever the cursor is doing: a warning in reverse video fills the upper left
corner, every key and mouse click is thrown away, and nothing of the IDE is drawn
meanwhile. The warning gives the size of the window and the size the IDE needs,
says that **Ctrl-Q, then y** leaves and that **text you have not saved is lost
unless the recovery copy is on**, and is worded shorter in a very small window so
that it always fits (the sizes are always on its first row). When the window is big
enough again the warning goes by itself and the whole layout, foot included, is
drawn again with everything as it was. [SED](27a-sd-tcl-sed.html) and
[CED](27b-sd-tcl-ced.html) have a different lock, which looks at the cursor, not
at the window.

## The two that are not like the others

**`generate`** builds `$include` token definitions from a dictionary. **It is
interactive** — it asks for the token type, the prefix and several other
things — so it cannot be driven from a script.

**`debug`** runs a program under the debugger, taking the same arguments as
`run`. It needs a terminal and **refuses inside a phantom** with *"Cannot debug
program in a phantom process"*. The debugger itself is covered in
[SD Basic - Debugging](17-sd-basic-debugging.html).

## Who has these verbs

**Every account has all of them now**: `format`, `list.common`, `basic`,
`catalog`, `compile.dict`, `debug`, `delete.catalog`,
`delete.common`, `find.program`, `generate`, `ide`, `map`,
`run`.

**Running a catalogued program never needed any of these anyway** — a
catalogued name runs by being typed, with no VOC record of its own — so an
application deployed this way was always reachable regardless of what
verbs an account had.

## See also

[SD Basic - Program Structure](01-sd-basic-program-structure.html) ·
[SD Basic - Debugging](17-sd-basic-debugging.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html).

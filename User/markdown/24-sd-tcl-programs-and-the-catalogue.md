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
catalogue** — one chosen by a `*`, `!`, `_`, `$` or `-` prefix on the call name
rather than by the `global` keyword — so the prefix is not a way round it.
The hyphen was added on 16 Oct 2026: `catalog bp -name` catalogues the program
`name` globally as `-name`, a program calls it with `call @nm(args)` where `nm`
holds `-name`, and `delete.catalog -name` removes it.

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
cd {dict | data} file {i-type}... {no.query} {no.page}
cd local
cd all
```

`compile.dict` is the same verb under its longer name. It compiles the A, C, I
and S-type entries in a dictionary; with no names it does all of them, or uses
the active select list if there is one.

| | |
|---|---|
| **`cd local`** | every dictionary in the account |
| **`cd all`** | every dictionary visible from the account |

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
ide {file record}
```

Opens a full-screen environment for BASIC programs and the other text records
of an account, built on the screen library. `ide file record` starts on that
record. It needs a terminal and **stops in a phantom**.

| part | what it is |
|---|---|
| menu bar | the top row; F10 or Esc opens it, and a click on a title opens that menu (since 19 October 2026; a click on the bar beside the titles does nothing) |
| tree | the account's files on the left. Return on a file lists its records (the first 2000), and Return again closes the list. Return on a record opens it. A letter jumps to the next entry that starts with it |
| editor | on the right, a tab for each open record. **While it has the focus the character at the cursor is shown in the highlight style** (as well as the terminal's own cursor being put there), so the place shows on a terminal that draws its cursor poorly. It is the text area `screen memo` uses, so its keys are `memo`'s: selection, cut, copy and paste, undo and redo, find, line numbers. Text is coloured as SD BASIC, C, Python, JSON, shell or Markdown by the file and record name. **A horizontal scroll bar runs along its bottom row** (`<` and `>` at the ends, a thumb as long as the visible part is of the longest line; none to speak of when every line fits); clicking an arrow scrolls 8 columns and clicking the track a page |
| table | under the editor: the compiler's errors, or search results |
| pane marks | **`[*]` or `[-]` in the top right corner of each pane that can have the keyboard** (since 19 October 2026): the files (on the frame above the tree), the editor (on the frame above it), the tab strip (at its right end) and the messages (at the right end of their bar). `[*]` is on the pane that has the keyboard, `[-]` on the others; Tab moves it round in that order |
| status line | **the pane that has the focus** first, in brackets (`[Files]`, `[Tabs]`, `[Editor]`, `[Messages]`: Tab goes round them in that order), then the record, the cursor's line and column, and a star when there are unsaved changes |

| key | |
|---|---|
| F7 | save and compile; the compiler's lines go in the table. Return on one goes to its line, F4 to the next |
| F8 | compile and catalogue |
| F5 | compile and run |
| F9 | compile with debugging and run the debugger |
| F2 · Ctrl-S | save the record |
| Ctrl-R | find a text in every record of the file the tree is on (the first 2000 records, 500 lines), listed in the table; Return opens the record at the line |
| F11 | find in all the records of a file |
| Ctrl-E · Go, Edit in SED | edit the record in [SED](27a-sd-tcl-sed.html) and come back (below) |

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

The other keys follow [SED](27a-sd-tcl-sed.html) where the two do the same:
Ctrl-Q quits, Ctrl-L goes to a line, Ctrl-X, Ctrl-C and Ctrl-V cut, copy and
paste, Ctrl-Z and Ctrl-Y undo and redo, Ctrl-F finds forward and Ctrl-B
backward (Return on the question repeats the last text), Ctrl-R replaces a text
through the record and Ctrl-W writes the text to another record. In the text
area of every program that uses `screen memo`, a word back and on are now
Ctrl-P and Ctrl-U; they were Ctrl-B and Ctrl-F, which are SED's find keys.

On a UTF-8 terminal (`LC_ALL`, `LC_CTYPE` or `LANG` says UTF-8) the frame, menus
and scroll bars use line-drawing characters; elsewhere `+ - |`. The colours are
the blue theme.

**What it does not do:** it does not lock records while they are open (the check
at saving is what protects against a second editor), has no replace across
records, no project files and no completion.

**The IDE is laid out for 140 columns by 42 lines or more** (it was 60 by 16
until 18 October 2026); a bigger window is used whole, as before. **A window
smaller than 140 by 42 when the IDE starts is refused**, in words (*IDE needs a
window of at least 140 columns by 42 lines; this one is 100 by 30*), and nothing
is drawn; `ed` is the editor for a small window. The window measured is the one on
the screen, or the display `term w,h` gave if that is smaller. If the window is
made smaller while the IDE runs, the layout does not shrink with it: the IDE shows
the **upper left corner** of its 140 by 42 layout and nothing past the edge, and
draws the whole layout again when the window is made bigger. While the cursor of
the editor, the tree or a question is **off the screen** the IDE does not take
keys, because you would be typing where you cannot see: a warning in reverse
video fills the upper left, every key is thrown away, the warning goes by itself
when the window is big enough, and **Ctrl-Q, then y** leaves the IDE without
saving. [SED](27a-sd-tcl-sed.html) describes all of it; the IDE and
[CED](27b-sd-tcl-ced.html) behave the same way.

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
`catalog`, `catalogue`, `cd`, `compile.dict`, `debug`, `delete.catalog`,
`delete.catalogue`, `delete.common`, `find.program`, `generate`, `ide`, `map`,
`run`.

**Running a catalogued program never needed any of these anyway** — a
catalogued name runs by being typed, with no VOC record of its own — so an
application deployed this way was always reachable regardless of what
verbs an account had.

## See also

[SD Basic - Program Structure](01-sd-basic-program-structure.html) ·
[SD Basic - Debugging](17-sd-basic-debugging.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html).

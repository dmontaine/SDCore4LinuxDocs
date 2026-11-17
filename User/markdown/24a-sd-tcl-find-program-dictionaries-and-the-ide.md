Title: Programs: find.program, Dictionaries and the IDE
Subtitle: find.program, formatting source, dictionaries, named common blocks and the opening of ide.

This page continues [SD TCL - Programs and the
Catalog](24-sd-tcl-programs-and-the-catalogue.html).

## Which copy will run: `find.program`

```
find.program name {detail}
```

For the case where the system seems to run the wrong version of a program
because it is cataloged in more than one place. It looks in the three places a
program is loaded from, **in the order they are searched** — the local catalog
(a VOC entry that points at the object file), the private catalog (the
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
nowhere is *xx is not cataloged*. The name is looked for as typed; a global
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

It compiles the I-type entries in the dictionary of *file*; with no names it does all of
them, or uses the active select list if there is one. **The dictionary is the
default: write the file's name and nothing before it** (`compile.dict cust dbl`).

| | |
|---|---|
| **`compile.dict local`** | every dictionary in the account |
| **`compile.dict all`** | every dictionary visible from the account |
| **`compile.dict data file`** | reads the records of the file's *data* part as if they were dictionary items, and compiles those that look like one: a record whose first character is `I`. Every other record is skipped without a word. It is for the rare file whose data holds items of that kind; on an ordinary data file a record that happens to begin with `I` is reported as a compilation error. Because it rewrites records it is held back by the edit gates as any change to a VOC, a dictionary or a program file is |

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
ide file record record ...
ide file *
ide dict file {record}
ide dict file record /form
ide dict file record /text
ide voc {record}
ide path:/full/name
```

Opens a full-screen environment for BASIC programs and the other text records
of an account, built on the screen library. `ide file record` starts on that
record. **`ide dict file record` starts on an item of the file's dictionary and `ide voc record` on a
record of the account's VOC**. A record that does not exist yet opens as a new,
unsaved one, after the account's gate allows it; **`creating.seqkey` in place of the record name takes the
file's next sequential id** (in quotes it is a record of that name). With a select list active,
`ide file` **asks whether to open it**: Yes opens the first ten records of the list in tabs and lists them all, and
Go, Next record from the list opens the next one that is not already in a tab; No clears the list. **`ide file record record ...`
opens a tab for each record named** (one that is not there is a new record) **and `ide file *` lists the
records of the file as a select list does, the first ten in tabs** (both work after
`dict`; the ids are the words of the command, so an id with a blank in it is opened with Ctrl-O). It needs a terminal and
**stops in a phantom**.

| part | what it is |
|---|---|
| menu bar | the top row; F10 or Esc opens it, and a click on a title opens that menu (a click on the bar beside the titles does nothing). Its right end says *ide* and who you are (*ide  pat@sales*), as the toolkit pages and SED do |
| tree | the account's files on the left (**the entries whose names start with a dollar sign - `$acc`, `$hold`, `$map`, `$release` - are not listed**: they belong to SD itself). Return on a file lists its records (the first 2000, and a message says when there are more; a big file is no longer read whole first), and Return again closes the list. **A file that has a dictionary shows the dictionary as a node of its own under it**, read only when you open it, and its items are listed the same way. Return on a record opens it. A letter jumps to the next entry that starts with it. **An account that has operating system access (the administrator, or `os-on`) also sees an *Operating system files* node after its files**: Return on it lists `/`, Return on a directory lists its entries (directories first, then files, each in the order of the names; 1000 at most) and again closes it, and Return on a file opens it in a tab, as `path:/full/name` does. Names that hold a control character or a byte from 248 to 255 cannot be shown or put in a path; a message says how many entries were left out. A directory the operating system does not let the session read says so, with the operating system's error number (message 11599). An account without the access has no node |
| editor | on the right, a tab for each open record. **While it has the focus the character at the cursor is shown in the highlight style** (as well as the terminal's own cursor being put there), so the place shows on a terminal that draws its cursor poorly. **If a block flashes beside the text as you type** (seen in lxterminal and Xfce Terminal, not in GNOME Terminal or Terminator), set the terminal's cursor style to underline or I-beam in its preferences: the highlighted character and a block cursor on top of it are what some terminals draw badly. It is the text area `screen memo` uses, so its keys are `memo`'s: selection, cut, copy and paste, undo and redo, find, line numbers. Text is colored as SD BASIC, C, Python, JSON, shell or Markdown **chosen as [SED](27a-sd-tcl-sed.html) chooses**: by the name of the file, then the record id, then the first line - so a script with no suffix that begins `#!/bin/sh` is shell - and then the languages a site added in `&sed.syntax&`. **A horizontal scroll bar runs along its bottom row** (`<` and `>` at the ends, a thumb as long as the visible part is of the longest line; none to speak of when every line fits); clicking an arrow scrolls 8 columns and clicking the track a page |
| table | under the editor: the compiler's errors, or search results |
| pane marks | **`[*]` or `[-]` in the top right corner of each pane that can have the keyboard**: the files (on the frame above the tree), the editor (on the frame above it), the tab strip (at its right end) and the messages (at the right end of their bar). `[*]` is on the pane that has the keyboard, `[-]` on the others; F6 moves it round in that order |
| status line | **the pane that has the focus** first, in brackets (`[Files]`, `[Tabs]`, `[Editor]`, `[Messages]`: F6 goes round them in that order, past the messages when there are none), then the record, the cursor's line and column, and a star when there are unsaved changes |

## Continued in

[Programs: The IDE's Keys](24b-sd-tcl-the-ide-keys.html) — the keys of the
IDE.

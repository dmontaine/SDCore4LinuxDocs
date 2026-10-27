Title: SD TCL - The SED Screen Editor
Subtitle: The full-screen editor that runs inside SD — drop-down menus that show the keys, colour for the language, split windows and macros.

```
sed {dict} file record
sed {dict} file
sed
```

`sed` edits one record of one file, using the whole screen. It is written in SD
BASIC and runs **inside** SD, as [ed](25-sd-tcl-ed.html) does, so it is not a
program SD hands the record to: **it needs no operating-system permission** for
a record of an SD file, where [nano](26-sd-tcl-edit.html) and
[micro](27-sd-tcl-micro.html) need the account's `os-on` switch. It draws the
whole screen, so it wants a terminal; for a phantom, an API session or a script
use `ed`.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part.

> **SED was removed once and is back.** It was taken out because its Emacs-style
> keys are hard to remember. It returned with a menu bar on the top line that
> shows the key of every action, and with the keys most editors have. The old
> Emacs layout is still there for anyone who wants it (see *Options*, below).

## Starting it

| | |
|---|---|
| `sed bp myprog` | edit record `myprog` of file `bp` |
| `sed dict customers name` | edit a dictionary item |
| `sed bp creating.seqkey` | edit a new record under the file's next sequential id (the counter `write … creating.seqkey` uses); also with `dict`, and typed at the *Record name* prompt. The id is taken when the edit begins, so a record never filed leaves a gap. A directory file or a file opened read only is refused; in quotes it is an ordinary id |
| `sed` *file* | with a select list active, SED offers to edit its records one after another; with none, it asks for the record names until you give a null one |
| `sed` | asks for the file name, then the record name |
| a file name written `path:/home/pat/notes.txt` | an operating-system file by its path. An account needs `os-on` for a path outside its own directory; without it SED says the account has no OS access |

With a select list, SED shows the first id and asks whether to use the list
(`Y` or `N`). Leaving one record goes on to the next.

**SED is 140 columns by 42 lines, always** — SD's default terminal size, which
SED has followed since 18 October 2026 (it was 120 by 36 before) — whatever the
window is. A bigger window shows SED in its top left corner with the rest blank.
The top row is the menu bar, the bottom two rows say which record is open and how
it is being edited: the number of lines, the line and column, and any of *Macro*,
*Overlay*, *Indent* and the search mode that are in force.

**A window smaller than that when SED starts is refused**, in words
(*SED needs a window of at least 140 columns by 42 lines; this one is 100 by 30*),
and SED draws nothing; `ed` is the editor for a small window. The window it
measures is the one on the screen, or the display `term w,h` gave if that is
smaller, so `term 100,30` typed in a large window is refused too.

### A window made smaller while SED is running

Dragging the corner of the window, or a tiling window manager, can make the
window smaller after SED has started. SED looks at the window about once a second
while it waits for a key, and again every time it draws. When the window has
changed it clears the screen and draws the **upper left corner of its 140 by 42
layout** — the menu bar, the first lines of the record and as much as fits — and
nothing past the edge: nothing wraps and nothing lands on the wrong row. Nothing
pans; the upper left is always the anchor. Make the window bigger and the whole
layout is drawn again. The menus, the *Quit without saving?* box and the other
boxes are placed inside the part that shows.

**While the cursor is off the screen SED does not take keys**, because you would
be typing where you cannot see. The cursor is off the screen when it is on a line
below the window or past its right edge, and also when SED is asking something on
a row the window does not show (the search prompt and the line-number prompt are
on the two bottom rows). SED clears the screen and shows a warning in reverse video
in the upper left corner instead:

> The window is 100 by 30 and SED is laid out for 140 by 42: the cursor is off the
> screen and keys are ignored. Make the window larger to carry on, or press Ctrl-Q
> to leave.

Every key and every mouse click is thrown away. Make the window large enough to
show the cursor and the warning goes by itself — no key is needed — and the whole
layout is drawn again, with the cursor where it was. **Ctrl-Q is the one key that
does anything**: it changes the warning to *Leave? (changes are NOT saved) y/n*
in the same box. **y** leaves SED, with the record unlocked and any change not
saved; any other key goes back to the warning. This question is not SED's own
*Quit without saving?*, which may be on a row you cannot see.

A session that has `autologout` set waits for the keyboard alone, so that the
time-out can still fire: SED notices a new window size at the next key rather
than within a second, and the warning goes at the first key after the window is
big enough.

**If SED's input ends** (a pipe that has been used up, as in a script or a test; a
terminal does not end like this), SED leaves in the same way as after *y* above: the
record unlocked, the screen cleared, nothing asked, and any change not saved. Before
19 October 2026 such a session went on for as long as it was left, using all of a CPU.

## The menus

**F10, or Esc pressed on its own, opens the menu bar.** Left and right move
between the menus, up and down between the items, Return runs the item, Esc
closes the menu, and a letter picks the item whose label has that letter
marked. **Every item shows the key
that does the same thing**, read from the key bindings in use, so the menus
teach the keys. An item that needs an answer (a search string, a line number)
asks on SED's prompt line at the bottom. An item that cannot be used (compile
a dictionary item, say, or expand tabs in a read-only record) is dim and the
cursor goes past it; a mode that is on is checked.

| Menu | Items |
|---|---|
| **File** | Save · Save as · Open record · Import · Export · List records · Quit |
| **Edit** | Undo · Redo · Set mark · Swap mark · Cut region · Copy region · Paste · Delete char · Kill line · Delete word · Close spaces · Upcase word · Lower case word · Capital initial · Upcase region · Downcase region · Align text · Toggle chars · Overlay mode |
| **Search** | Forward search · Backward search · Replace · Query replace · Goto line · View lines · Top · Bottom · Page up · Page down · Case on · Case off · Word search · Basic word search |
| **Buffer** | Next buffer · Previous buffer · Goto buffer · List buffers · Delete buffer · Up to list · Dive |
| **Window** | Split window · Unsplit window · Toggle window · Move split up · Move split down · Refresh screen |
| **Tools** | Compile · Compile and run · Format · Indent mode · Expand tabs · Stamp · Syntax colour · Mouse · Release lock · Keys in use · Run extension · Command · Start macro · End macro · Execute macro |

**Several records can be open at once** — they are *buffers*, and a record
named in a list or opened with *Open record* becomes the next one. *List
records* shows the records of the file and *Dive* opens the one the cursor is
on; *Up to list* goes back. The **window** can be split in two, to look at
two places at once.

**Moving the split point** (*Window*, *Move split up* and *Move split down*, dim
until the window is split) moves the line between the two windows by one row.
On SED's command line **`split.up`** and **`split.down`** move it by the number
of rows given (one without a number). Both windows keep at least two rows, a
number that would take it further stops there, and the cursor stays in the
window that is live.

**Seeing only some of the lines** — *Search*, *View lines*, or **`view`** *text* on
the command line (the prompt asks for the text when it is left out) — opens a
new buffer that holds only the lines of this one that contain the text. The case
of the text matters unless the search mode is `case_off`. The new buffer is
**read-only and is not a record of any file**: nothing can be saved from it, it
is named `--View--` and the text, and the buffer you came from is as it was.
A text that no line holds is said so and no buffer is made. The commands have
no key of their own; reach them from the menus or the command line.

## The keys

The keys are the ones most editors have, with the shell's line keys beside
them. *Keys in use*, on the Tools menu, shows every one, including any you
have rebound.

| | |
|---|---|
| **`Ctrl-S`** | save |
| **`Ctrl-Q`** | quit. A changed record asks *Quit without saving?* in a small box where **No** is the default |
| **`Ctrl-O`** · **`Ctrl-W`** | open a record · write the record under another name |
| **`Ctrl-Z`** · **`Ctrl-Y`** | undo · redo (see *Undo and redo*, below) |
| **`Esc .`** | set the mark |
| **`Ctrl-C`** · **`Ctrl-X`** · **`Ctrl-V`** | copy, cut and paste the text between the mark and the cursor (`Esc W` and `Esc Y` also copy and paste) |
| **`Ctrl-F`** · **`Ctrl-B`** | search forward · search backward (`Esc S` and `Esc R` also) |
| **`Ctrl-R`** · **`Esc %`** | replace · query replace |
| **`Ctrl-L`** | go to a line (`Esc G` also) |
| **`Ctrl-G`** | give up the question being asked |
| **`Ctrl-A`** · **`Ctrl-E`** | start of the line · end of the line |
| **`Ctrl-N`** · **`Ctrl-P`** | next line · previous line (the arrow keys as well) |
| **`Esc F`** · **`Esc B`** | forward a word · back a word |
| **`Esc V`** or **Page Up** · **Page Down** | page up · page down |
| **`Esc <`** · **`Esc >`** | top of the record · bottom |
| **`Ctrl-D`** · **`Esc D`** | delete a character · delete a word |
| **`Ctrl-K`** | kill the rest of the line |
| **`Esc U`** · **`Esc L`** · **`Esc C`** | upcase, lower-case or capitalise the word |
| **`Esc N`** · **`Esc P`** | next buffer · previous buffer |
| **`Esc X`** | the command line (see *Colour for the language* and the commands below) |

`Esc` followed at once by a letter is a command of the editor's own; `Esc` on
its own opens the menu bar. `Ctrl-X` is no longer a prefix, so the old
`Ctrl-X` sequences are gone: the actions that had one (split the window, list
the buffers, import, export and the rest) are reached through the menus, which
show the key of each item that has one.

## Undo and redo

**`Ctrl-Z` undoes the last change and `Ctrl-Y` does it again**, as do *Undo* and
*Redo* at the top of the Edit menu. A **step** is one change: a run of typing (or
of backspaces, or of deletes) on one line is one step, and so is each of the other
edits — a new line, a kill, a cut, a paste, a replace, a command such as *Format* or
*Expand tabs*. Moving the cursor ends a run of typing. The cursor goes back to where
the change began.

- Undo changes the **screen**, not the file: the record on disk is the one last
  saved, and saving writes what is on the screen, undone or not.
- Undoing after a save is allowed, and the record is then different from the saved
  one until it is saved again.
- A new change after an undo ends the redo: what was undone cannot be brought back.
- **It holds 100 steps, or about 8 million characters of them, the oldest going
  first**, and **starts again with each record and when you go to another buffer** —
  coming back to a buffer finds nothing to undo in it. A record that is read-only has
  none.
- With nothing to undo or redo SED says so (*Nothing to undo*, *Nothing to redo*).

## The mouse

SED takes the mouse in a terminal that reports it — xterm and the terminals that
behave like it; the Linux console does not.

| | |
|---|---|
| a click on the text | puts the cursor there (in the other window of a split, it goes there first) |
| a click on a title of the bar | opens that menu; a click on an item chooses it, and a click anywhere else closes the menu |
| the wheel | moves the cursor up or down three lines |

**It is on unless you turn it off.** The command `mouse off` (and `mouse on`, or
`mouse` alone to switch), Tools > *Mouse* (checked while it is on), or the word
`no.mouse` in `&sed.options&` turn it off; with it off a report that arrives is
ignored. **While it is on the terminal's own selection and copy with the mouse do not
work — hold Shift to use them**, which is how a terminal gives the mouse to the program
that asked for it. SED asks the terminal for reports only while it waits for a key and
for the menu, so a prompt, a question or a command SED runs never sees one.

The command line (`Esc X`, or *Command* on the Tools menu) takes these:

| | |
|---|---|
| **`basic`** · **`compile`** | compile the record as a BASIC program with error tracking · save it, then compile |
| **`run`** | run the program in the current buffer |
| **`xeq`** *command* | run an SD TCL command and come back |
| **`format`** · **`fancy.format`** | run the formatter on the record |
| **`indent`** · **`overlay`** | toggle indent mode or overlay mode |
| **`tabs`** *n* · **`expand.tabs`** | set the tab interval · replace tab characters by spaces |
| **`lnum`** | show or hide line numbers |
| **`case_on`** · **`case_off`** · **`word`** · **`bword`** | the search mode |
| **`stamp`** | add a history line |
| **`release`** | release the update lock on the record |
| **`keys`** · **`save.keys`** · **`load.keys`** | show the key bindings in use, save them as a record of `&sed.bindings&`, load a saved set |
| **`syntax`** | colour, see below |
| **`mouse`** · **`mouse on`** · **`mouse off`** | the mouse (above); `mouse` alone switches it |
| **`quit`** | give up a select-list edit |

## Colour for the language

SED can colour the text it shows: comments, strings, keywords, numbers and
the lines that begin with `$`, in SD BASIC and in five other languages. **It is
off until you ask**, and with it off the screen is drawn exactly as it was.

| | |
|---|---|
| **`syntax`** | Turn colour on, or off if it is on. The same item is on the Tools menu, checked while colour is on |
| **`syntax on`** · **`syntax off`** | Turn it on or off |
| **`syntax light`** · **`syntax dark`** | Choose the palette for a light or a dark background (dark is the default); either turns colour on |

Type these on the command line (`Esc X`). A terminal that cannot show colour
says so and goes on without it.

**The language is chosen from the record**, by the name of the file, then the
record id, then the first line. A record of the file `bp` is SD BASIC, and so
is any whose id ends in `.bp`, `.bas` or `.b`.

| Language | A record is taken to be that language when |
|---|---|
| SD BASIC | the file is `bp`, `*.bp`, `bp.*`, `*bp` or `syscom`; or the id ends `.bp`, `.bas` or `.b` |
| C | the id ends `.c`, `.h`, `.cc`, `.cpp`, `.cxx`, `.hpp` or `.hh` |
| JSON | the file or the id ends `.json` |
| Markdown | the id ends `.md` or `.markdown`, or begins `readme` |
| shell | the id ends `.sh`, `.bash`, `.bashrc` or `.profile`, or the first line is `#!` followed by a path with `sh` or `bash` in it |
| Python | the id ends `.py` or `.pyw`, or the first line is `#!` followed by a path with `python` in it |

A comment or a string that goes on to the next line colours the lines below
it, and deleting the line that opened it recolours them.

**A site can add a language, or replace one of these**, with a record in the
file `&sed.syntax&` whose id is the name of the language and whose fields are
its rules, one rule to a field. A rule that does not parse is left out and
named when the editor starts. The rule kinds are `file`, `record` and `first`
(what the language is for), `line`, `mark`, `region`, `words`, `number`,
`label`, `nocase` and `ident`; the styles are `comment`, `string`, `constant`,
`keyword`, `type`, `preproc`, `special`, `error` and `todo`.

## The AI in SED

When the AI is on for your account (see [Asking the AI](29b-sd-tcl-asking-the-ai.html)) the
**Tools** menu has two more items, **Ask the AI...** and **Explain the selection**; without the
AI they are not there. They are also the commands **`AI`** (with the question after it if you like:
`ai make the second line shorter`) and **`AI.SELECTION`**, typed after Esc X.

* **Ask the AI...** takes the question on the message row (`AI>`).
* **Explain the selection** uses the text between the mark (Esc `.`) and the cursor. With no mark
  the message row says to set one, and nothing is sent.

Whichever you use, **Enter shows everything that will be sent** — the provider and model, the
fixed instruction, the record's lines (the whole record up to 24,000 bytes, else the lines round
the cursor, and it says so), the selected text and your question — with Send and **Cancel, the
default**. While the AI answers, Esc gives the request up.

If you asked for a change, the answer shows it as a diff, one change after another: the line it is at,
the old lines with `-`, the new ones with `+`. **Accept** puts the changes into the buffer and
**Reject, the default, leaves it as it was.** Accepting is **one step for Undo (Ctrl-Z)**, and **nothing is saved**:
Save is yours, and the edit gates apply to it as ever. A set of changes is taken whole or not at all: one
whose old text is not in the record, is in it twice, overlaps another, is more than 8, or would
show more than 30 lines, is ignored with a note. A buffer that is read only takes no changes. A command
in the answer is ignored.

## Options

Two records in the account's VOC change SED, and **both are optional**.

**`&sed.options&`** — field 1 begins with `X`; field 2 lists words, separated by
blanks:

| Word | Effect |
|---|---|
| **`indent`** | start in indent mode |
| **`overlay`** | start in overlay mode |
| **`lnum`** | show line numbers |
| **`tabs`** *n* | the tab interval, 1 to 99 (field 5 does the same) |
| **`case_on`** · **`case_off`** | searches match case, or do not |
| **`word`** · **`bword`** | search for whole words, or whole SD BASIC words |
| **`syntax`** · **`no.syntax`** · **`syntax.light`** | colour on or off at the start; light palette |
| **`mouse`** · **`no.mouse`** | the mouse on (the default) or off at the start |
| **`no.invert`** | leave the case of typed letters alone |
| **`scroll1`** | page up and page down move one line less than a page, so one line of the old page stays on the screen |
| **`no.case.explore`** | the list of records (the explore list, `?` at the record prompt) is in order whatever the case of the ids, not capitals first; the list of files is not changed |

**`&sed.bindings&`** is a file of key sets. SED loads the first that exists of:
the record named in field 3 of `&sed.options&`; one named *login*-*terminal
type*; `user.`*login*; one named for the terminal type; the record named in
field 4; and `default`. **If none exists, SED uses its own keys, and `emacs` in
field 3 of `&sed.options&` makes those the old Emacs layout** (`Ctrl-X` is the
prefix of most of the less common actions again). The command line's
`save.keys` writes the keys in use as a record of the file. A word in
`&sed.options&` that SED does not recognise is reported and ignored.

## What SED edits

It edits **a record of any SD file** — program source, a dictionary item, a
record of a data file — and, by `path:`, an operating-system file. It locks
the record while it is open. **A second user who opens a record someone else
holds gets it read-only**, and cannot save it; a record that does not exist yet
and is being created by someone else is refused. *Release lock*, on the Tools
menu, gives your own lock up.

For a program record the Tools menu **compiles** it with error tracking: when
the compile fails, each error is put into the text as a line beginning `!!ERROR:`
(a warning, `!!WARNING:`) just above the line it belongs to, and the cursor
goes to the first. The next compile removes those lines before it starts. It
also compiles and runs the program, or just runs it. To step through a program
as it runs, see [the debugger](17-sd-basic-debugging.html).

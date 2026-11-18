Title: Programs: The IDE's AI Line, Recovery and Window
Subtitle: The AI in the IDE, recovery copies and the window, and debug and generate.

This page continues [Programs: The IDE's Zoom, Fields View and Dictionary
Items](24d-sd-tcl-the-ide-zoom-fields-and-dictionary-items.html).

**The AI in the IDE**. When the AI is on for your account (see
[Asking the AI](29b-sd-tcl-asking-the-ai.html)) the IDE has an **AI** menu before Help and an
**`AI>`** row under the editor and the messages table (the table is one row shorter); without the AI
neither is there and nothing else changes. F6 goes round the panes to the AI row (Shift-F6 the other
way), or click it, or use the menu:

| | |
|---|---|
| AI, Explain the error | asks the AI to explain the compile message the table has on its line, with the record |
| AI, Explain the selection | the same for the text from the mark (Ctrl-G where it starts) to the cursor; with no mark the status line says to set one and nothing is sent |
| AI, Ask about this record | puts you in the `AI>` row to type what you want |

Whatever you ask, Enter shows **what you are sending** first: the provider and model, the size of
all of it (SD's own instruction is sent and counted, not shown), the record's lines (the whole record when it is under 24,000 bytes, else the
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

The other keys: Ctrl-Q quits, Alt-G goes to a line, Ctrl-X, Ctrl-C and Ctrl-V cut, copy and
paste, Ctrl-Z and Ctrl-Y undo and redo, Ctrl-F finds forward and Ctrl-B
backward (Return on the question repeats the last text; **F3 finds the next one and
Shift-F3 the one before**, as in other text areas) and Ctrl-R replaces a text through the record. **Ctrl-W
closes the record**; Save as and Write a copy are in the File menu. The same keys work in
[SED](27a-sd-tcl-sed.html), which is this editor started by itself.
In the text area (the keys are those of `screen memo`; the [screen
library](12a-sd-basic-the-screen-statement.html) page has the list) Ctrl-A selects
everything, Ctrl-D duplicates the line, **Alt-K** cuts the whole line into the
clipboard (Ctrl-K in a text area elsewhere; in the IDE Ctrl-K is the keys, as on every page), and a word back and on are Ctrl-P and Ctrl-U. The editor passes
Ctrl-E (the zoom), Ctrl-T (the theme) and Ctrl-K (the keys) on to the IDE.

On a UTF-8 terminal (`LC_ALL`, `LC_CTYPE` or `LANG` says UTF-8) the frame, menus
and scroll bars use line-drawing characters; elsewhere `+ - |`. The colors are
your own theme if you chose one, else the site's (`SCREENTHEME` in `sd.conf`, paper as delivered), as on the toolkit
pages and in the debugger: paper when neither names one or the name is not
a theme, mono on a terminal with no color. Ctrl-T or View, Theme goes through blue, classic,
mono, night and paper, skipping those the terminal cannot show, and **SD keeps the
choice for you**: the IDE (also when started as `sed`), every page and the debugger start in it
from then on, in this account and in later sessions.

**A recovery copy of text you have not saved**, **if the administrator has turned it
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
until you save. Turning the recovery copy off does not delete copies that exist. The IDE started as `sed` keeps
its copies in the same way.

**What it does not do:** it has no replace across records, no project files and no completion, and it does
edit collection-file records only as JSON text or fields, and an operating-system file is a plain text file in one piece (no NUL, no byte from 248 to 255, 2 MB at
most; a file with content is never replaced by a new one, no directory is made, and there is no rename, delete
or change of mode).

**The IDE is laid out for 140 columns by 43 lines or more**; a bigger window is used
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
drawn again with everything as it was. [CED](27b-sd-tcl-ced.html) has a different
lock, which looks at the cursor, not at the window.

A window made bigger, or smaller and then big enough again, keeps everything you
were doing: the editor's undo and redo steps, the selection,
the text to find (F3), the cursor and the view, the messages table's row, the open
nodes of the tree and a half-typed AI request. The parts of the screen are moved and
sized where they are; if one of them cannot be moved, the IDE builds the screen again,
keeping the text. Coming back from Run or Debug also builds the screen again.

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
`catalog`, `compile.dict`, `debug`, `decatalog`, `delete.catalog`,
`delete.common`, `find.program`, `generate`, `ide`, `map`,
`run`.

**Running a cataloged program never needed any of these anyway** — a
cataloged name runs by being typed, with no VOC record of its own — so an
application deployed this way was always reachable regardless of what
verbs an account had.

## See also

[SD Basic - Program Structure](01-sd-basic-program-structure.html) ·
[SD Basic - Debugging](17-sd-basic-debugging.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html).

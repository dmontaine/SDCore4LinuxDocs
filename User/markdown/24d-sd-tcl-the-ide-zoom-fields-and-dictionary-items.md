Title: Programs: The IDE's Zoom, Fields View and Dictionary Items
Subtitle: Ctrl-E, F12, dictionary items as a form and records with marks.

This page continues [Programs: The IDE and Other Files, Tabs and
Options](24c-sd-tcl-the-ide-other-files-and-options.html).

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

**Ctrl-E zooms the editor.** The list of files and records and the messages
below the editor are hidden and the editor takes the whole screen, with the
tabs above it, the menu bar, the status line (which says *zoomed*) and the
key row as before; Ctrl-E again, or Go > Files and records, brings them back.
Every key, menu and the AI line work the same while zoomed, and F6 goes
between the tabs and the editor only. Anything that fills the messages - a
compile with errors or warnings, a search, Run a command - ends the zoom so
that you can read it; a compile with no errors leaves it as it is.

Ctrl-E is the editor's *end of row* key in other programs that use `screen memo` (and in `sed`); in the
IDE **End** ends a row. Nothing is handed to another editor: [SED](27a-sd-tcl-sed.html) is this editor, started by itself.

**F12 shows the record as fields, values and subvalues, so that nobody types a mark.**
The record in the open tab is shown in the *fields pane* - the editor of
[CED](27b-sd-tcl-ced.html) in its *data mode*, drawn in the editor's rectangle with the tree, the tab
strip and the messages still on the screen: a list of the fields, each field a text or a list of its
values, each value a text or a list of its subvalues. Dive into a field with Return, go up with
**Esc**, **Left** or **Backspace** (Esc at the top is the IDE's own Esc and opens the menu bar), change
a text with Return, add or delete with **Ins** and **Del**, change the type with **Alt-T**, rename with
**F3**, and copy, cut and paste with **Ctrl-C**, **Ctrl-X** and **Ctrl-V**; the value and subvalue
marks are put in from the shape of the tree. **The pane is a part of the tab, not a mode of the IDE**:
the tabs, the menu bar, F6 and every IDE key keep working, each tab remembers whether it shows its
text or its fields, and a resize keeps the pane where it was. **Each change you make is in the tab's
text at once**, so the tab is marked changed (a star on the status line and on the pane's path line),
and **Ctrl-S is the IDE's own save** of that text, with the edit gate and the overwrite question as
for any other change. **F12 again shows the text**; going back and forth without a change touches
nothing, and after a change **one Ctrl-Z in the text area takes the whole visit back** (*Back from the
fields: bp prog is changed, save it to keep it*; *... is as it was* when nothing changed). The pane
writes nothing and takes no lock. **Commands that work on the text of the record** - Replace, the case
changes, Import and Export, Format, Go to line and Open the include - **wait while the pane
is up** (*This works on the text of the record: show the text first (F12), then do it*). **The AI line
works in the pane**: a request typed in the AI entry, and the AI menu's
*explain the selection*, which explains the element the table has selected, send the record as
indented JSON, one element to a line; the preview and the diff come first, and what you accept
changes the fields and so the tab's text. Explaining a compile message does not apply to the pane.
**On the empty top level of a record, Alt-T asks whether it is a collection or an array** (C, A or
Esc); a new record of a collection file starts as an empty collection. If something
else changes the text under the pane (the overwrite question's *Reload*), the pane follows it,
staying in the same container when it can; text that is no longer a record the fields can show ends the
pane and the text is shown, untouched. With no record open, F12 says so.
**A record of an ordinary file whose text is a JSON object or array** (with no
value or subvalue mark in it) is shown as the *tree of the JSON*, as a collection file's record
is, and comes back as the JSON text in the same layout; anything else (marks in the record, text
that does not parse, text that does not begin with `{` or `[`) is shown as fields, as above.

**A dictionary item opens as a form**: `ide dict file record` (a record that is not
there yet opens as a new D item) and **Return on an item in the tree** show the item as a form first, and so
does the **E** of `tool.dict`, which hands the item to the IDE. `ide dict file record /text` opens it as text;
**Cancel** (or **Esc**) in the form leaves the item as text in its tab, and **Go, Dictionary item as
form** (or `/form` on the command line) shows the form for the tab you are in. A record found by a search,
items opened together from a list, Ctrl-O, an item already in a tab, an item another session holds (it is
read-only) and an item the form cannot show open as text. The form takes the body of the
screen (140 by 43) in the same frame as the IDE and the pages, with its own bar, status line and row
of keys, and is **one form**. Its first row is the **Type**, an entry: type `D`, `E`, `I`,
`L`, `PH` or `X` and press Tab, and **the rows of that type appear**, each a label and an entry; a new item
shows nothing but the Type until then, and an item that exists shows its rows with their values filled in, to
be edited. Typing another Type makes the rows of that type and keeps what was typed for the rows the two
types share. The buttons at the foot are **Accept** and **Cancel**.

| type | rows |
|---|---|
| D | Field #, Conversion Cd, Column Heading, Len & Just, Single/Multi, Association (used only when Single/Multi is M), User |
| E | as D, but an Element Path (the element of a [collection](20a-sd-tcl-collection-files.html) record) in place of the Field # |
| I | as D, but an Expression in place of the Field # |
| L | Id Expression, File, File Expression |
| PH | Phrase |
| X | Text (a text area) |

**Len & Just** is one entry for the width of the column, the justification and decimals if any: `30 L`,
`12 R 2` (`30L` is the same). Tab and Down go to the next row, Return presses **Accept**, and **Esc** leaves.
**Each value is checked as you leave its row**, the reason is on the line near the foot and a hint for the
row you are on above it: a field number is a whole number from 0 to 9999 (0 is the record id), Len & Just a
width 1 to 200, then L, R, T or C, then decimals 0 to 9, a column heading and a conversion at most 40
characters, a conversion one SD knows, an association at most 30 letters, digits, dots, dashes and
underscores, an expression one line, and an L item's expressions one expression with no semicolon.
**Accept is refused while a row fails**: the row is named and takes the focus. When every row passes, the
item becomes the tab's text and **the IDE's own save writes it**, with the account's dictionary-edit gate
and the overwrite question as for any other save; the form itself writes nothing.
**Esc after a change asks** *Leave without saving the changes?* (Discard or Keep editing). An item the form
cannot show - a type it does not know, a format that is not a width, one of L, R, T or C and decimals, or
text with characters it cannot hold - **stays text, and the status line says why**. The fields the form
does not show (the compile stamp and object code of an I item, and any field after the eighth) are kept as
they were while the type stays; a changed type starts from the new type's rows. The form is modal: the tabs and
the menu wait until it is left.

**The form has an AI line** when the AI is on for your account: **AI>** on its last
row, reached with **F6** or a click (Shift-F6, or F6 again, goes back to the row you were on; Tab goes from row to row, the AI line among them). Say what the item should be and press Enter there (Enter in that
line asks the AI; it does not accept the form). Everything that will be sent is shown first, Cancel the
default; the values the AI proposes are shown in full, Reject the default; **Accept puts into the rows only
the values that pass the form's own checks** and the line near the foot names any that did not. Nothing is
written until you Accept the form and the IDE saves it. An item of SD's own files is never sent. See
[SD TCL - Asking the AI](29b-sd-tcl-asking-the-ai.html).

**A record that holds marks is shown with the marks written as tokens**, so
that nobody types one. This follows the tab's kind: **a dictionary item, a VOC record
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

## Continued in

[Programs: The IDE's AI Line, Recovery and
Window](24e-sd-tcl-the-ide-ai-and-the-window.html) — the AI in the IDE,
recovery copies and the window.

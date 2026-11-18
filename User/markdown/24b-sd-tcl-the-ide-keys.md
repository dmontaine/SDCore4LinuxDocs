Title: Programs: The IDE's Keys
Subtitle: The keys and menus of ide.

This page continues [Programs: find.program, Dictionaries and the
IDE](24a-sd-tcl-find-program-dictionaries-and-the-ide.html).

| key | |
|---|---|
| F8 · Build, Compile | save and compile; the compiler's lines go in the table. Return on one goes to its line, F4 to the next |
| Shift-F9 · Build, Compile and catalog | the build: compile and catalog. *Cataloged* is said only if `catalog` added the program |
| F9 · Build, Run | compile and run (F5 draws the screen again, as on every page) |
| F7 · Build, Debug | compile with debugging and run the debugger. **Shift-F7** (Build, Toggle breakpoint) marks the cursor's line as a breakpoint for it, Build, Clear breakpoints takes the marks away and Build, Debug from the first line stops at line 1: see [SD Basic - Debugging](17-sd-basic-debugging.html) |
| Ctrl-S · File, Save | save the record (an untitled buffer asks for its file and name first; an unchanged record says *No changes to save*). **Ctrl-S is the only save key**; F2 finds an action, as on every page |
| Ctrl-N · File, New record | a new record: the name form, then a buffer that is not on the disk until it is saved. **`path:/full/name` there makes an empty file of the operating system and opens it in a tab** (below) |
| Ctrl-O · File, Open record | the name form, for a record that exists; a file whose name starts with a dollar sign is refused. **Up and Down in the form bring back the files and records opened in this session** (twenty of each) |
| View, List of tabs | a list of the open tabs: file, record, whether it has changed (`*`), lines; Enter goes to the tab, Esc leaves the list |
| File, Save as | the name form; the tab becomes the new record and it is saved. The old record is as it was on the disk. **With `path:/full/name` the tab becomes a new file of the operating system** (below). It has no key |
| File, Write a copy | the name form; the text is written to another record and the editor stays on the record it had. **With `path:/full/name` the text is written to a new file of the operating system** and no tab or lock is kept. It has no key |
| Ctrl-W · File, Close record | closes the record's tab; with unsaved changes it asks whether to save them, discard them or cancel |
| Ctrl-PageDown · Go, Next tab | the next record tab; Ctrl-PageUp (Go, Previous tab) the one before. **Alt-PageDown and Alt-PageUp do the same** (the second tab keys): GNOME Terminal keeps Ctrl-PageUp and Ctrl-PageDown for its own tabs, so use the Alt keys there |
| F6 · Go, Next pane | the keyboard goes to the next pane (the AI line is one, after the messages, when the AI is on for your account). **Shift-F6** (Go, Previous pane) goes to the one before. These are the only keys that move between the panes, here and on every full-screen page |
| Go, Files and records | the keyboard goes to the tree. It has no key, because F3 is the text area's find next (below). From the editor, Shift-F6 twice reaches the tree (editor, tabs, tree); so does F6 twice (editor, messages, tree) when the AI pane is not open |
| F3 · Shift-F3 | with the editor focused, **find next** and **find previous** of the text last searched for |
| Ctrl-R · Search, Replace in the record | replace a text through the record, **as one undo step** (one Ctrl-Z gives the whole text back). The find options below apply. **In a record shown with `:@vm:` marks it changes the record's own text** (the colon in `10:30` is a colon; a mark's token is never found or changed, and a result that cannot be shown in the token form is refused and leaves the text alone). A text to find is at most **256 characters** |
| Search, List matching lines | **the lines of this record that hold a text, with their numbers, in the table at the bottom**; Return on one goes to it, F4 to the next. It looks at a read-only tab too. It has no key |
| Search, Query replace | each match is shown with its line and asked about: **Yes, No, All, Quit**; the answers are collected and the text is set once at the end, so one Ctrl-Z undoes the lot. A Quit keeps the Yes answers given before it |
| Search, Find options | **C** = match case, **W** = whole words (a letter, a digit, `.`, `_`, `$` or `%` next to the match makes it part of another word); a blank answer is neither. As delivered the case is matched and any word is found. The options are for List matching lines, Replace and Query replace; the text area's own Find (Ctrl-F, F3) ignores case and is not changed |
| Search, Upcase the selection · Downcase the selection | the characters between the mark (**Ctrl-G** sets it where the cursor is) and the cursor change case; the rest of the text does not; one undo step |
| Search, Import a record here | the name form (the record must exist); its lines go in at the cursor, one undo step. A record that holds value, subvalue or text marks or characters outside ASCII and a collection file's record are refused, with the reason. **`path:/full/name` imports a file of the operating system**: from the text of the tab that holds the file, if there is one, else from the file itself, read through the account's gates and closed again; a file the IDE would not open (a NUL or a byte from 248 to 255, over 2 MB, a directory, a device) is refused as Open refuses it |
| Search, Export the selection | the name form (a record that is not there, as Write a copy asks); the selected text is written to it, under the account's edit gate and the record's lock, as the record when the selection is whole lines of a record shown with `:@vm:` marks (the tokens are written as the marks; a part of a line is written as the text shown). It works on a read-only tab, but not on a record that holds characters outside ASCII. **`path:/full/name` writes the selection to a new file of the operating system** (below) |
| Build, Run a command | **a command of the account's TCL, typed in a question**, is run as the prompt would run it - through the same command processor, so with the same gates - and what it printed is in the table at the bottom (500 lines at most). The changed texts' recovery copies are kept first and the tabs' locks taken again after. **A command that aborts (a program with a run-time error, `abort`) is stopped and the IDE stays up**; it prints nothing in the table. A command that asks the keyboard for an answer is not for this, and neither is one that changes the account (`logto`): the IDE goes on in the account the command left |
| Up · Down in a Run a command question | bring back the commands run from either Run a command in this session (twenty) |
| Saving a record | when a subroutine `source.control` is cataloged, every save calls it before the write, as `sed` and `ed` do: it can refuse the write or change the record |
| Build, Run a command at the terminal | for a command that needs the terminal: **the screen is given to the command**, Return brings the IDE back with the tabs as they were. It goes through the same command processor, so with the same gates; a command that aborts gives the IDE back too. A record the command changed is not read again by the tab that holds it |
| Search, Stamp a history line | puts `* Updated by` *who* `(`*login name*`)` and the time and date above the cursor's line; one undo step, nothing saved |
| Search, Expand tabs | every tab character in the text becomes blanks to the next tab stop of the tab width; one undo step |
| Build, Run with arguments | asks for the words to put after the program's name, then compiles and runs it as Run does (`run bp prog words`); the program reads them with `SENTENCE()` |
| Alt-= · View, Character code | the code of the character at the cursor, its name when it is a control character, and its field, value and subvalue, on the status line |
| View, Syntax color · View, Line numbers | switch the color and the line numbers off for every tab, and on again |
| View, Mouse | stops the terminal reporting the mouse, and starts it again; while it is off a click does nothing and the terminal's own selection works. Every command has a key or a menu entry, so nothing needs the mouse |
| Ctrl-Up · Ctrl-Down · View, Scroll the view up a line · Scroll the view down a line | moves the text a line in the editor and leaves the cursor where it is, unless it would leave the window |
| F5, Ctrl-L · View, Refresh | draws the screen again from what the IDE holds |
| Ctrl-T · View, Theme | the next color theme, kept for you (below) |
| Ctrl-K · Help, Keys | the IDE's keys, in a box |
| Edit, Undo · Redo · Cut · Copy · Paste · Select all | the editor's Ctrl-Z, Ctrl-Y, Ctrl-X, Ctrl-C, Ctrl-V and Ctrl-A, from the menu; in the fields pane, the pane's own copy, cut and paste |
| Edit, Delete the word before · Cut to the end of the line · Swap two characters · Word in capitals · Word in small letters · Capital initial of the word · Close a run of blanks · Align with the line above · Swap cursor and mark | the editor's own editing commands, on these keys: Alt-Backspace, Alt-E, Alt-T, Alt-U, Alt-L, Alt-C, Alt-Space, Alt-A and Alt-M; Alt-D deletes the word at the cursor and Ctrl-Up / Ctrl-Down move the view a line. They work on the text, not in the fields pane |
| Go, Filter the records | **which records the tree lists for a file or its dictionary**: a pattern (`abc...`), a text in quotes, or `like` or `with` and a query, as at `sed`'s record name; empty lists them all. A filter sorts the whole file. A list longer than 2,000 records goes by pages: the last row of the list goes on to the next 2,000 and the first row back |
| File, Spool the text | **prints the tab's text as it is now, saved or not**, to print unit 0, and changes nothing. The question takes `at` *printer* (for this job only), `lnum` (line numbers) and `region` (the lines of the selection) |
| Alt-R · Edit, Start or end a macro · Alt-P · Edit, Execute the macro | **Alt-R** records the keys the editor acts on until Alt-R again (the status line says so) and **Alt-P** plays them, each as if typed, stopping at a key the editor refused; a function key, a menu and a paste are not recorded. One macro, kept while the IDE runs |
| Edit, Insert a field · Delete a field · Rename the field · Change the type | the fields pane's Ins, Del, F3 and Alt-T; outside the fields pane they say to show the fields first (F12) |
| Tools, Files · Dictionary · Vocabulary · Queries · Bulk update · Programs · Tests | **opens that development page** (`tool.files`, `tool.dict`, `tool.voc`, `tool.query`, `tool.bulk`, `tool.catalog`, `tool.test`; see [The Development Tools](29c-sd-tcl-the-development-tools.html)) on the whole screen. The IDE gives the terminal to the page as Run gives it to a program: what you typed in the editor stays in its tab, unsaved; leave the page (Ctrl-Q), press Return at *Press Return to go back to the IDE*, and the IDE is back with its tabs, saying *Back from ...*. The page asks your account's gates exactly as when you type its name at the prompt. A record the page changed while it is open in a tab is not read again: close the tab and open it to see the change. The menu has no keys; F10 then T opens it |
| Alt-G · Go, Go to line | **a line; line,column; or, in a record shown with `:@vm:` marks, field,value,subvalue** (the field is the line, the value follows the (v-1)th `:@vm:`, the subvalue the (s-1)th `:@sm:` inside it; the tokens are found in any case, and a value or subvalue past the last goes to the last; **two marks side by side - an empty value - count as one, so use the line and column there**). A number is made whole (`1.5` is 1) and one above 99,999,999 is taken as 99,999,999; a number under 1 or a word is not taken |
| Search, Find in the records | find a text in every record of the file the tree is on (the first 2000 records, 500 lines), listed in the table; Return opens the record at the line. The text is at most 256 characters. It has no key (F11 was it) |
| Ctrl-E · Go, Zoom the editor | the editor fills the screen; Ctrl-E again brings the files and the messages back (below) |
| F12 · Go, Edit as fields | edit the record as a tree of fields, values and subvalues in the IDE's own fields view - the editor of [CED](27b-sd-tcl-ced.html), shown inside the editor's rectangle - and come back (below) |
| Tab · Shift-Tab | in the editor, **indent and outdent** the line or the selected lines (below); in the tree, the tabs, the messages and the fields they do nothing (they never move between the panes: F6 and Shift-F6 do). In a dialog, such as the name form, Tab still goes from field to field |
| Go, Open the include | the record that the `$include` line at the cursor names, in a tab: one name is looked for in the file the tab is in and then in `syscom`, two words name the file; a collection-file record is passed over, and one that is not found says where it looked. It has no key |

**A bare `ide` opens "Untitled 1"**: an editable buffer, colored as a
program, with the cursor in it and the tree two keys away (Shift-F6 twice) or in the Go menu. Type, then save: **the name form** asks
for the file and the record id together. The file is filled in - the file of the record you are in, else
the file the tree is on, else `bp` - and the cursor
starts on the record id. If the account may not change that file (`bp.edit`, `dict.edit`, `voc.edit` or
`shared.write` is off; the form says which, and what SDSYS can do about it) or a record of that name
already exists, **the form says so and stays open** for you to correct it; Esc leaves it and nothing is
written. A new record or an untitled buffer is not written until you save it, and Compile, Catalog,
Run and Edit as fields on an untitled buffer name and save it first - so a program can be typed,
compiled, fixed, saved and cataloged without leaving the IDE. **The write is made under the record's
lock**, and if the file refuses it (a trigger, a full disk) the IDE says so and your text stays in the
editor. A refusal by the edit gate on a save is shown whole in a box. **Catalog reports "Cataloged"
only if `catalog` said it added the program**; otherwise its answer is shown in a box. In the editor the
up and down arrows stop at the first and last line.

**Each tab has a kind**: a program, an item of a file's dictionary, a record
of the VOC, or a record of a data file. The kind decides the marks (below) and the gate that a save
asks: a program asks `bp.edit`, a dictionary item `dict.edit` and a VOC record `voc.edit`, as SED and
`ed` do, and the refusal is shown in a box that says which switch and what the administrator can do.
Compile and Catalog on a dictionary item say it is not a program. A dictionary named in the New
record form is not yet taken (use `ide dict`).

## Continued in

[Programs: The IDE and Other Files, Tabs and
Options](24c-sd-tcl-the-ide-other-files-and-options.html) — the IDE and files
of other kinds.

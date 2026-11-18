Title: Programs: The IDE and Other Files, Tabs and Options
Subtitle: Collection files, locks, operating system files, indenting, the options record.

This page continues [Programs: The IDE's Keys](24b-sd-tcl-the-ide-keys.html).

**A record of a collection file opens as the text of its JSON**, one element to a line, in a tab of its own. You edit the text as any other; **Ctrl-S parses it and
writes the collection to the file**, and the tab keeps the text in the same layout
(the layout `ct` shows) so that a text you typed compact is not "changed" for ever. Text that is not a
JSON object or array is refused in a box that says where the parse stopped, and the record on the disk is
untouched. **Edit as fields (F12) shows the collection in the fields view** (it writes
nothing and takes no lock) and brings the JSON text of what you kept back into the tab; the save is the IDE's.
A record that is not there opens as a new `{}`. Compile, run, debug, catalog, Save as and the include do
not apply to such a tab (the IDE says so); **Write a copy keeps its JSON text in a record of an ordinary
file, and a text cannot be saved into a collection file under a new name** (New record makes a record of
it). A record that is neither an object nor an array (a plain value) is refused, and the lock goes back.
The record is locked while the tab is open, as any record is. Find in the records skips collection
files.

**A record open in a tab is locked for as long as the tab is open.** If another session already holds it the tab opens **read-only** and the status line says which
user holds it: it cannot be changed or saved, and Write a copy keeps its text under another name.
Closing the tab, quitting, a lost connection or any other way out gives the locks back; Run and Debug
keep them while they run. **An IDE left open therefore blocks other sessions and batch
writes on those records** until it is closed, `autologout` ends it or the administrator's
`tool.sessions` page unlocks them. A new record is locked for its creation, and one that another
session is making is refused. Compile, Run, Debug and Catalog work on a read-only tab that has no
changes (they save first only when there is something to save).

**A file of the operating system opens in a tab of its own**: `ide
path:/full/name`, or `path:/full/name` typed in the *File* entry of Open (Ctrl-O) - or `path:` there and the
full name in the *Record* entry. **The name is the full path, as you typed it** (its case is not changed):
it starts with a slash, has no `.` or `..` part, no doubled slash and no control character, and a path with
blanks is fine on the command line. The tab strip shows `os` and the last part of the name; the status line
shows the whole path. Open needs the file to exist (**New, Save as,
Write a copy and Export make one: see *Making a file of the operating system* below**), and **compile, run,
debug, catalog, edit as fields, Save as and open the include do not apply to such a tab** (the IDE says
why). **Write a copy does work on it**: it keeps the tab's text in a record, or in another new file of the
operating system, which is the way out when a save failed or the file was replaced. How it behaves:

- **The account's gates apply, and the kernel asks them.** An account without the OS gate can open and save
  only files inside its own directory (a link inside the account that leads out of it is outside); an account
  with `os-on`, and SDSYS, can reach what the Linux user can. A file in a VOC, a dictionary, a program file or
  the shared account that the account may not change opens read-only. The IDE asks exactly what your own
  `openseq`, `readblk` and `writeblk` would be asked.
- **It is written where it is.** Saving writes the new text over the file and cuts it to the new length: the
  same inode, owner, mode and links (a file renamed over it would change all four). The IDE reads the file once
  more just before it writes and asks *has been changed by someone else, Overwrite it?* (Cancel is the default)
  when it is not what it read - or is no longer text. **A file that was removed, or replaced by another one
  renamed over it** (an editor or `git` may do that) is refused outright: the tab holds the old file, which
  nothing links to, so a write would only appear to work. The file is read back after the write and must be the
  bytes meant; if the write fails, a box says the file may be partly written and your text stays in the editor.
  **A program you run from the IDE that does a bare `release` lets go of the file's lock**; the save still reads
  the file again first.
- **Bytes are not converted.** Lines end with LF, or with CR LF when *every* line does (then they stay CR LF); a
  CR anywhere else is an ordinary character shown as a reverse letter, and a tab is kept as a tab. Whether the
  last line had its line end is remembered: none is added to a file that had none. A file with a **NUL or a
  byte from 248 to 255** (SD's own marks), a file **over 2 MB**, a **directory, device, pipe or socket** is
  refused with a message; a file with **bytes from 128 to 247** (another character set, or UTF-8) is edited
  like any other, as a record is.
- **The file is locked while the tab is open**, as a record is: a second session that tries to open it is told
  it is in use, and closing the tab (or any other way out) gives the lock back. A tab for a file you may not
  write (permissions, or an edit gate) opens read-only and says so.
- **No recovery copy is kept** for such a tab, whatever the account's switch: the copy would be kept in your
  home, and the file may be anywhere.

**Making a file of the operating system**. In the name form of New (Ctrl-N), Save as,
the first save of an untitled buffer, Write a copy and Export the selection, type `path:/full/name` in the
*File* entry (or `path:` there and the full name in the *Record* entry), spelled as for Open. The form asks the
account's operating system access and its edit gate for operating system files first and says a refusal in
the form, which stays open. **The edit gate looks only below the account's own directory.** An account that
holds `os-on` is trusted with the whole machine, so for a name outside its own directory the edit gates
(`voc.edit`, `dict.edit`, `bp.edit`) are not asked, as for `OPENSEQ` and the other operating-system routes
(Administrator, *Accounts and security*); inside its own directory they are.

| from | what is made, and what the tab does |
|---|---|
| New | an **empty** file, opened in a tab of its own |
| Save as, the first save of an untitled buffer | the file, holding the tab's text. **The tab becomes the file**: the record it had is as it was on the disk, its lock is given back and its recovery copy is dropped; the file is locked while the tab is open, as any file of the operating system is |
| Write a copy, Export the selection | the file, holding the text (or the selection). No tab is made and no lock is kept |

- **The file is made before anything else changes.** When it cannot be made, the tab, the record and its lock
  are as they were. The text read back from the disk is what the tab holds afterwards.
- **A file that is there is never replaced.** A name taken by a file with content, by a link that leads nowhere
  or by a file someone else made a moment ago is refused (*was not made: a file with that name is there already*);
  open it to change it. An existing **empty** plain file is filled. A name that is a directory,
  device, pipe or socket says it is not a plain file. **A name another session holds locked** is
  refused in a box and **nothing is made** (the file is made only once its lock is
  held).
- **The directory it goes in must be there**; the IDE never makes one. A missing directory, or a directory the
  operating system or the account's edit gate does not let this session make a file in, is refused with the
  error number.
- **Text with a NUL or a byte from 248 to 255, or more than 2 MB (2,097,152 bytes), is refused before any file
  is touched**; the text stays in the editor.
- **A write that fails** (a full disk) says so in a box: the file was made and an empty or partly
  written one may be there. The text is still in the editor.
- **The new file's mode is 0666 less the session's umask**, the mode `openseq ... creating` gives (the IDE has
  no setting of its own); SD sets the umask to 002 when a session starts, so the mode is 0664 unless the session
  has changed it with `umask`. Its owner is the Linux user the session runs as.
- **Nothing outside the account is reachable without the account's operating system access.** The file is made
  as `openseq ... creating` makes it, so the account's OS gate and the edit gates for a VOC, a dictionary, a
  program file or the shared account apply as for a program of your own. An account without the access can make
  files inside its own directory only.

**A record that holds characters outside ASCII (bytes 128 to 247) can be edited**: SD stores those bytes and
gives them back unchanged. The editor works a byte at a time, so a UTF-8 character takes more than one cell, and
deleting one of its bytes leaves a broken character. The marks 248 to 255 are SD's own and go through the token
form below.

**Tab and Shift-Tab indent and outdent in the editor**: Tab puts blanks in up to
the next stop (every 3 columns) or, with lines selected, indents them; Shift-Tab takes the indent out;
each is one undo step and neither ever puts a tab character in. This is the IDE's editor only: a
program's own `screen memo` keeps its Tab. F6 and Shift-F6 move between the panes, and Tab never leaves a pane.

**Ctrl-Home and Ctrl-End, Ctrl-Left and Ctrl-Right, Ctrl-Del**: the start and the
end of the text, a word back and a word on, and delete the word at the cursor (the blanks before it and
the word; the selection if there is one; at the end of a line it joins the next line, as one undo step).
Again the IDE's editor only. A terminal that sends nothing for these keys, or something SD does not name,
leaves them without effect; Home, End, Ctrl-U and Ctrl-P still move.

**Overwrite mode, auto-indent, tab width and Format**. **Ins**, or *View, Overwrite
mode*, makes a typed character replace the one under the cursor (the status line shows `[overwrite]`; at the end
of a line, and over a selection, typing inserts as ever). *View, Auto-indent* makes Return begin the new line
with the blanks the line begins with (as many as stand before the cursor). *View, Tab width* asks for a number
from 1 to 99 for Tab and Shift-Tab (3 to begin with). *Build, Format the program* lays the program in the tab
out again with the rules of the `format` verb, indenting by the tab width; it changes the text as one undo step
and saves nothing, and leaves a program that has problems, or a record that is not a program, as it is.
None of the three modes is kept between sessions. A cut or a paste of more than 100 lines is done at once.

**An account can set the IDE's defaults in the record `&ide.options&`**. It is an X
record in the account's VOC; field 2 holds words, separated by blanks, and the IDE reads them each time it
starts. **An account that has no `&ide.options&` but has SED's `&sed.options&` gets the IDE's defaults from
that**, so a record kept for SED goes on working.

| Word | What the IDE starts with |
|---|---|
| `CASE_ON` · `CASE_OFF` | the find options' match case on (as delivered) or off |
| `WORD` · `BWORD` | the find options' whole words on; a word is letters, digits and `.` `_` `$` `%` |
| `INDENT` | auto-indent on |
| `OVERLAY` | overwrite mode on |
| `TABS` *n* | a tab width of *n*, 1 to 99 (field 5 can hold the number instead) |
| `LNUM` · `NO.LNUM` | line numbers on (as delivered) or off |
| `SYNTAX` · `SYNTAX.LIGHT` · `NO.SYNTAX` | syntax color on (as delivered) or off; the colors are the theme's |
| `MOUSE` · `NO.MOUSE` | the mouse on (as delivered) or off |
| `NO.CASE.EXPLORE` | the records in the tree in order as if every letter were a capital (`a1` then `_1`, where the delivered order puts `_1` first) |

`SCROLL1` is passed over. Any other word is named on the status line when the IDE starts and is otherwise
ignored. **Fields 3 and 4, which held SED's key bindings, are not read: the IDE's keys cannot be
changed.** The IDE never writes the record. To make one at TCL:

```
ed voc &ide.options&
```

and enter `X` as line 1 and the words as line 2 (for example `INDENT TABS 4 NO.MOUSE`).

## Continued in

[Programs: The IDE's Zoom, Fields View and Dictionary
Items](24d-sd-tcl-the-ide-zoom-fields-and-dictionary-items.html) — zoom, the
fields view and dictionary items.

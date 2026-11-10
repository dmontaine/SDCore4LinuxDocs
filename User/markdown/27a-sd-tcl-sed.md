Title: SD TCL - The SED Screen Editor
Subtitle: SED is the editor of the IDE, by itself: no files pane, the same keys and the same menus.

```
sed
sed file
sed file record
sed file record record ...
sed dict file item
sed file *
sed file creating.seqkey
```

**SED is the IDE's editor, started alone.** Everything [the IDE's page](24-sd-tcl-programs-and-the-catalogue.html) says about the editor is true of SED: the same keys, the same menus, tabs for the records
that are open, compile and run on F8 and F9, find and replace, undo, keyboard macros, Spool, the color for the language and the line numbers. An account's `&ide.options&` record sets how it starts, or
`&sed.options&` when there is no `&ide.options&`. It needs a window of at least 140 by 43.

**What is different from `ide`:**

- There is no files pane and no Tools menu. The editor has the whole width of the screen.
- **`Ctrl-E` is the end of the line.** In `ide` it zooms the editor.
- `sed` with no record named asks **File name?** (when none was named) and **Record name?**. At the record name, **`?`** lists the records of the file to pick one, and **`?`** followed by a filter
  lists those that match: a pattern such as `abc...`, or `like` or `with` and a query. An empty answer ends the editor.
- **File, List records** lists the records of the file the editor is on.
- A compile with errors, a find in the records, List matching lines and Run a command put their results in a table under the editor. **Go, Hide the results** takes it away.
- A dictionary item opens as text. `ide` opens it in its form.
- Closing the last record ends the editor.

**A record id with a blank in it** goes in quotes: `sed bp "my program"`.

**Coming from the SED of earlier releases.** SED was a separate program until L2.0-0. Its extension language, split window, key rebinding (`&sed.bindings&`, `load.keys`, `save.keys`), the Emacs layout, the
repeat count, the quote character and the commands typed at Alt-X (`case_on`, `bword`, `lnum`, `spool` and the rest) are gone; each is a menu entry or a key now, or has no replacement, as the Changes document
lists. The keys that changed most are **Ctrl-A** (select all; Home is the start of the line), **Ctrl-P** and **Ctrl-N** (a word back; a new record; the arrow keys move), **Ctrl-D** (duplicate the line;
Delete deletes a character), **Ctrl-U** (a word on) and **Ctrl-G** (set the mark). Run a command is on the Build menu.

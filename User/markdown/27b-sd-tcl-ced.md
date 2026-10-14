Title: SD TCL - The CED Data Collection Editor
Subtitle: A full-screen editor for a record that is a data collection — one level at a time, with the type of every element shown.

```
ced {dict} file {id ...}
ced {dict} file *
call !ced(collection)
```

A **data collection** is SD's name for a structured value: a set of named
elements, or an array of numbered ones, each of which is a string, a number, a
boolean (`true` or `false`), a null, or another collection or array. It is the
same shape as JSON and converts to and from JSON text. `ced` edits one, a level
at a time, and shows the **type** of every element, which a text editor on the
JSON cannot.

`ced` edits a record of a collection file, or the JSON text held in a record of
an ordinary file. `!ced()` edits a collection held in a BASIC variable. Both use
the same screen. Like [sed](27a-sd-tcl-sed.html), it runs inside SD and needs no
operating-system permission; it needs a terminal, and in a phantom it returns
at once without editing anything.

In the tables, *italics* mark something you supply and **bold** marks a word
typed as it stands; braces mark an optional part.

## Starting it

| | |
|---|---|
| `ced orders 1001` | edit record `1001` of file `orders` |
| `ced orders 1001 1002 1003` | edit each in turn |
| `ced orders *` | edit every record of the file, in id order |
| `ced dict orders` *id* | edit a dictionary item |
| `ced orders` | with a select list active, edit its records; with none, ask for ids until a null one is given |

**A record of a collection file** is a collection already. **A record of an
ordinary file** must hold JSON text for an object or an array, and is written
back as JSON text; one that does not is reported
(*Record 'xx' is not a JSON object or array*) and left alone. **A record that is
not there is a new one**: a small box asks whether it is to be a *Collection* or
an *Array*, and Esc gives up. The record is locked while it is open, and one
that another user holds is reported with the user's name.

## The screen

The top row names what is being edited, with a `*` after it once it has been
changed. Below it, the headings and **one row for each element of the level
being shown**: its name (or its position, in an array), its type, and its value —
or the number of elements, for a collection or an array. A `>` marks the selected
row. The path of the level is on the line near the bottom, and the last line gives
messages. Questions — a new value, a name, a type, *Save changes?* — are asked in
small boxes over the list.

## The keys

| | |
|---|---|
| **Up** · **Down** · **Page Up** · **Page Down** · **Home** · **End** | move |
| **Return** | open a collection or an array; on anything else, change the value (Return keeps the change, Esc gives it up) |
| **Esc** | back to the level above |
| **F3** | rename the element |
| **F4** | change its type — only the types the value can become are offered |
| **F5** or **`Ctrl-C`** | copy the element |
| **F6** or **`Ctrl-X`** | cut it |
| **F7** or **`Ctrl-V`** | paste (it asks for the name, or the position in an array) |
| **Ins** or **`Ctrl-I`** | insert an element: its name, type and value |
| **Del** | delete the element |
| **`Ctrl-S`** | save, and carry on |
| **`Q`** | leave, at the top level only |
| **`Ctrl-Q`** | leave from any level |
| **F1** or **`?`** | list the keys |

**Leaving with changes asks whether to save**, with *Yes*, *No* and *Cancel*.
With several ids, `Q` goes on to the next record and `Ctrl-Q` stops.

**Which types an element can become** depends on what it holds: a string that
looks like a number can become a number, `true` or `false` a boolean, an empty
string a null, and a string that is JSON text for an object or an array can
become that collection or array; a number can become a string. A null cannot be
edited as a value, but F4 changes its type.

**An element whose name is empty, or holds a slash, is shown with `?` for its
type and cannot be changed in the editor**, because a path cannot name it.

**`Ctrl-C` is a key in the editor.** The terminal's break character and the break
key are switched off while it runs and back on when it ends. If its input ends (the
terminal hangs up), it leaves without saving.

## !CED() — a collection in a variable

```
call !ced(c)
```

shows `c` in the same editor. **`c` is changed on return only if the changes
were kept** (`Ctrl-S`, or *Yes* when leaving); otherwise it is as it was. A
string holding the JSON text of an object or an array is taken as the
collection it parses to, and a null string as an empty collection; on return
the variable holds the collection. Anything else is left alone.

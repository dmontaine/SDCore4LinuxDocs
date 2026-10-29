Title: SD TCL - The CED Data Collection Editor
Subtitle: A full-screen editor for a record that is a data collection — one level at a time, with the type of every element shown.

```
call !ced(collection)
```

A **data collection** is SD's name for a structured value: a set of named
elements, or an array of numbered ones, each of which is a string, a number, a
boolean (`true` or `false`), a null, or another collection or array. It is the
same shape as JSON and converts to and from JSON text. The editor edits one, a level
at a time, and shows the **type** of every element, which a text editor on the
JSON cannot.

**There is no `ced` command and no Record editor tile on the home screen.** The editor
is reached two ways: `!ced()` edits a collection held in a BASIC variable, and the
[IDE](24-sd-tcl-programs-and-the-catalogue.html)'s **F12** (Go, *Edit as fields*) edits
the record in the open tab (below). To edit a record of a collection file, open it in the
IDE. Like [sed](27a-sd-tcl-sed.html), the editor runs inside SD and needs no
operating-system permission; it needs a terminal, and in a phantom it returns
at once without editing anything.

In the tables, *italics* mark something you supply and **bold** marks a word
typed as it stands; braces mark an optional part.

## The screen

The top row names what is being edited, with a `*` after it once it has been
changed. Below it, the headings and **one row for each element of the level
being shown**: its name (or its position, in an array), its type, and its value —
or the number of elements, for a collection or an array. A `>` marks the selected
row. The path of the level is on the line near the bottom, and the last line gives
messages. Questions — a new value, a name, a type, *Save changes?* — are asked in
small boxes over the list.

**The screen is laid out for 140 columns by 42 lines or more** (a bigger window
is used whole), and since 18 October 2026 **a window smaller than that is
refused**, before any record is touched, in words (*CED needs a window of at least
140 columns by 42 lines; this one is 100 by 30*); `!ced()` refuses the same way,
prints the message and returns, and the program goes on. If the window is made
smaller while CED is open it shows the **upper left corner** of the layout and
nothing past the edge, and draws everything again when the window is made bigger.
While the selected row is **off the screen** CED does not take keys: a warning in
reverse video fills the upper left, every key is thrown away, it goes by itself
when the window is big enough, and **Ctrl-Q, then y** leaves CED with nothing
kept; the record is unlocked. [SED](27a-sd-tcl-sed.html) describes the lock in
full.

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
`Q` leaves, at the top level only, and `Ctrl-Q` from any level.

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

## Data mode: a record of fields, values and subvalues

CED has a second use, started by the [IDE](24-sd-tcl-programs-and-the-catalogue.html)'s **F12**
(Go, *Edit as fields*; since 26 October 2026). The thing edited is an ordinary multivalue **record** shown as an array of its fields:
a field is a text, or - if it holds value marks or subvalue marks - a list of its values; a
value is a text, or a list of its subvalues; a subvalue is always a text. The top level is
the record (the positions are the field numbers), **Return** on a list dives into it, and the
path line shows `/2/1` for subvalue 1 of the first value of field 2. Nobody types a mark: they
are put back from the shape of the tree.

The keys are the ones above, with these differences:

- **Only two types exist: string and array.** F4 turns a string into a list of one value (where a
  list is allowed) and a list of nothing or of one string back into a string; Ins offers the
  same two. **A list is never allowed below the second level** - a subvalue is always a string.
- **Paste** is refused (*A record holds only text, and lists of values and subvalues: this is
  not one*) when the copied element would make a list below a subvalue, as a field pasted into
  the level of values would.
- **Ctrl-S** makes the record from the tree and keeps it; if the tree cannot be a record (for
  instance after an AI edit that put a number in a field) it says so, in the same words, and keeps
  nothing. The IDE passes no file, so CED writes nothing and holds no lock; the IDE does the saving.
- Rename (F3) does nothing: an array has no names.

Text is shown exactly as stored: a text mark or an item mark inside a text is part of the text
(the editor shows control characters as dots, as it always has).

## The AI in CED

When the AI is on for your account (see [Asking the AI](29b-sd-tcl-asking-the-ai.html)) **F2** opens a
menu of three; without the AI F2 does nothing.

| | |
|---|---|
| Explain the selected element | asks the AI about the element the cursor is on (its path and, for a container, its contents) |
| Ask the AI about this record | takes a question |
| Undo the AI's last change | puts the record back as it was before the AI's last accepted change (one level) |

The AI sees the record as **indented JSON, one element to a line**. As everywhere, Enter shows
**everything that will be sent** first, with Send and Cancel (the default). The answer may propose
changes to that text; they are shown as a diff, with Accept and Reject (the default). **A set of
changes is accepted only if the result is still a JSON object or array**; otherwise it is ignored
with a note and the record is not touched. Accepting marks the record changed — the usual quit
question applies — and **saves nothing**: Ctrl-S is yours, and the edit gates apply to it as ever.
After an accepted change you are back at the top level of the record. A command in the answer is ignored.

## !CED() — a collection in a variable

```
call !ced(c)
```

shows `c` in the same editor. **`c` is changed on return only if the changes
were kept** (`Ctrl-S`, or *Yes* when leaving); otherwise it is as it was. A
string holding the JSON text of an object or an array is taken as the
collection it parses to, and a null string as an empty collection; on return
the variable holds the collection. Anything else is left alone.

Title: SD Basic - The Screen Statement
Subtitle: Menus, dialogues, forms, colour and the mouse, from BASIC.

`print`, `crt` and `input` talk to a terminal one line at a time. The `screen`
statement talks to it a screen at a time: it draws text and boxes where you say,
asks the user a question in a dialogue box, runs a whole form of entry fields,
check boxes, lists and buttons, shows a menu bar, and takes clicks of the mouse.
It needs no extra package and no change to the rest of the program: it is one
statement word followed by a verb.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

```
screen open clear else crt 'This needs a terminal.' ; stop
screen form title 'Customer' at 10,3 size 56,12 returning f
screen label  f, 'l1', 'Name:'       at 2,2
screen entry  f, 'name'              at 12,2 width 30 value 'Smith'
screen check  f, 'vip', '&VIP'       at 12,4 value 1
screen button f, 'ok',     '&OK'     at 18,8 default
screen button f, 'cancel', '&Cancel' at 28,8 cancel
screen run f returning pressed then
   screen get f, 'name' returning name
   crt 'You pressed ' : pressed : ' for ' : name
end
screen close
```

## How a screen statement is written

```
screen verb {value {, value}} {clause value {, value}} ... {returning variable} {then ... else ...}
```

- **One new statement word, `screen`.** The verb that follows says what to do:
  `msgbox`, `form`, `theme` and so on. The verbs and the clauses are not
  reserved words: a program may still have variables called `title`, `buttons`,
  `default` or even `screen`, and they keep their meaning everywhere else.
- **Values first, then clauses.** A verb takes a fixed number of values
  straight after its name (the form it works on, a widget's name, a text).
  Then come clauses, each a keyword and its values, **in any order and all
  optional**: `title 'Confirm'`, `at 10,4`, `size 20,5`, `default 2`. A clause
  left out takes the verb's default.
- **`returning`** names the variable that receives the answer.
- **`then` and `else`.** `then` is taken when the user finished the dialogue
  (a button, a choice, Return); `else` when the user cancelled (Esc), the input
  ended, or there is no terminal. Both are optional:
  `screen msgbox 'Done.'` is a complete statement.
- **No terminal, no harm.** A phantom, the API and any other session that has
  no terminal take the `else` branch of every verb and draw nothing, so a
  program that calls `screen` does not hang when run unattended.
- **Everything is passed by value.** A variable you give a verb is not changed
  by it, except the one named after `returning`. A *form* is the exception that
  proves the rule: it is a data collection, one object however many variables
  hold it, so the verbs that add widgets change your form without anything
  being handed back.

Coordinates are character cells counted from 0, as in `@(x, y)`: `at 0,0` is the
top left corner of the terminal.

## The screen

A dialogue covers the text under it, and the terminal cannot be asked what it was
showing. So once a program has said `screen open`, the library keeps a **shadow**:
its own record of every cell it has drawn and in what style. A dialogue saves what
is under it from the shadow and puts every character back when it closes.

**Text the program writes with `print` or `crt` is not in the shadow.** Draw what
must survive a dialogue with `screen text`, or `screen refresh` will not bring it
back. Before `screen open` a dialogue still works, but it leaves blanks where it
was.

| | |
|---|---|
| `screen open {clear} {nocursor} {minsize w,h} {nomouse} {lines}` | Takes the screen. `clear` clears it (to the theme's desktop colour); `nocursor` hides the cursor; `minsize` gives `else` on a smaller terminal; `nomouse` leaves mouse reporting off (see below); `lines` draws every border in the line-drawing characters of Unicode (see *Borders*). `else` also when there is no terminal. |
| `screen close` | Gives the screen back: the shadow is forgotten, the cursor shown, mouse reporting off, the clip taken off, borders plain again, the theme back to mono, and the cursor moved to the first column of the last line. A coloured desktop is cleared. |
| `screen clip {at x,y size w,h}` | Keeps everything the library draws inside the rectangle: text, boxes, forms and dialogues that reach outside it are cut at its edge, cell by cell, and the cut part is neither drawn nor remembered. With no rectangle the clip is taken off. `else` when the library does not own the screen (no `open`) or there is no terminal. |
| `screen clear {at x,y} {size w,h} {attr style}` | Blanks the whole screen, or a rectangle of it, in the style given (default `desktop`). |
| `screen text string {at x,y} {attr style} {width n}` | Draws one line. Left out, `at` is where the last `screen text` ended. `width` cuts or pads the text to exactly that many cells. Text past the right edge is cut, not wrapped. |
| `screen box {at x,y} {size w,h} {title t} {attr style} {fill}` | Draws a border (`+`, `-`, `|`, or the line-drawing characters after `screen open lines`) and, with `fill`, blanks the inside. |
| `screen cursor {at x,y} {on} {off}` | Moves the cursor, shows it or hides it. The library puts it back there after each command that draws. |
| `screen refresh` | Clears the terminal and draws the shadow again. `returning` holds `resized` if the terminal's size has changed since `open`; the program then draws everything again. |
| `screen size returning v` | The width, a field mark and the height, as the terminal is now. |
| `screen key {timeout s} returning k` | Waits for one key. `k` is `up down left right home end pgup pgdn ins del bs tab btab enter esc f1` to `f12`, `ctrl-a` to `ctrl-z`, `mouse`, or the character itself. `else` on timeout or end of input. |
| `screen mouse returning m` | What the last mouse event was (below). |

Styles are named, not coloured: see *Styles and themes*.

## Dialogues

A dialogue asks one thing, waits, puts the screen back and gives the answer.

### message box

```
screen msgbox text {title t} {buttons list} {default n} {at x,y} {returning n}
```

| | |
|---|---|
| *text* | The message. A field mark or value mark ends a line. |
| `title` | Shown in the top border. |
| `buttons` | The captions, as values; a string with commas and no value mark is split at the commas (`'&Yes,&No'`). An `&` makes the letter after it the button's key. No `buttons` gives one, OK. |
| `default` | The button the box starts on (1). |
| `at` | The top left cell; centred if left out, and moved to fit. |
| `returning` | The number of the button chosen, 0 for Esc. `then` is taken when a button was chosen. |

Left and right move between the buttons, Return presses the one that has the
focus, a button's letter presses it at once, and a click of the mouse on a
button presses it.

### menu

```
screen menu items {at x,y} {default n} {returning code}
```

*items* are values (or fields), each *label* `@sm` *shortcut* `@sm` *code*. The
shortcut is text shown beside the entry; the program acts on the key itself. The
code is what comes back; without one the entry's number does. An entry of `-` is
a line across the menu. An `&` in a label marks its key.

A **fourth subvalue** holds flags: `D` makes the entry *disabled* (it is drawn dim, the
cursor keys go past it, Return and its letter choose nothing) and `C` makes it *checked*
(a `*` in its first cell, for a setting that is on):

```
items = 'Open':@vm:'Save':@sm:'':@sm:'save':@sm:'D':@vm:'Autosave':@sm:'':@sm:'auto':@sm:'C'
```

### menu bar

```
screen menubar menus {row r} {draw} {returning code}
```

*menus* has one **field** for each menu: its title, then its entries as values,
each as for `screen menu`. With `draw` the bar is drawn and the statement returns;
without it the first menu opens at once. Left and right move between menus, up
and down between entries, Return chooses, Esc leaves, a letter chooses the entry
that has it. Clicking a title opens that menu; clicking an entry chooses it;
clicking anywhere else closes the menus. Entries take the same `D` and `C` flags as
those of `screen menu`.

**Submenus.** A menu whose title begins with `>` is not on the bar: it is a submenu. An
entry whose *code* is that title opens it beside the entry, with a `>` at its right edge;
Right or Return opens it, Esc or Left closes it, and what is chosen in it is the code the
statement returns. Submenus may be three deep.

```
menus = '&File':@vm:'&Open':@sm:'':@sm:'open':@vm:'&Recent':@sm:'':@sm:'>Recent':@vm:'E&xit':@sm:'':@sm:'exit'
menus<2> = '>Recent':@vm:'one.txt':@sm:'':@sm:'r1':@vm:'two.txt':@sm:'':@sm:'r2'
screen menubar menus returning code
```

### pick list

```
screen pick items {title t} {at x,y} {size w,h} {default n} {multi} {returning v}
```

A box with a list of values. Up, down, home, end and the page keys move, a letter
jumps to the next entry that starts with it, Return chooses. With `multi` the space
bar picks or unpicks the current entry and `returning` holds the numbers picked,
as values. With more entries than rows the last column is a scroll bar. A click on
an entry chooses it (with `multi` it picks it); a click outside the box cancels.

### input box

```
screen ask prompt {value v} {width n} {title t} {at x,y} {mask} {returning text}
```

One line of input. `mask` shows a `*` for each character. The keys are those of
an entry field (below).

## Forms

A form holds widgets and the focus, and routes the keys. You build it with
statements, then run it, or wait on it for events.

```
screen form {title t} {at x,y} {size w,h} returning f
```

`f` is a data collection: `jbuild(f)` writes the form out as JSON and `jparse`
reads it back, so a screen can be kept as a record. A form left without a size is
as big as its widgets need; without a place it is centred.

### Adding widgets

Every widget verb takes the form and the widget's **id** first, and `at x,y`, the
place of the widget from the form's top left corner (0,0 is the corner of the
border; the default is 1,1). The id is the widget's name: not null, not used
before, and with no `/` or `*` in it. `else` is taken if a widget cannot be added.

| verb | what it adds |
|---|---|
| `screen label f, id, text {at x,y} {attr style} {width n}` | Text. A label that will be changed with `screen set` needs `width` for its longest text: a status line is a label with a width. |
| `screen frame f, id {at x,y} {size w,h} {title t}` | A border (it draws only the border; widgets added after it sit over it). |
| `screen entry f, id {at x,y} {width n} {value v} {mask} {maxlen n}` | One line of text; a longer text scrolls. |
| `screen check f, id, text {at x,y} {value 0 or 1}` | `[x] text`. |
| `screen radio f, id, items {at x,y} {value n} {across}` | One choice of several, one to a row (or side by side with `across`). |
| `screen list f, id, items {at x,y} {size w,h} {value n} {multi}` | A list of values to choose from; `multi` lets several be picked. |
| `screen combo f, id, items {at x,y} {width n} {value v}` | An entry field with a `[v]` that opens a list of choices. |
| `screen button f, id, text {at x,y} {default} {cancel}` | `[ text ]`. `default`: Return in any other widget presses it. `cancel`: pressing it, like Esc, ends the form with `else`. An `&` marks its key. |
| `screen progress f, id {at x,y} {width n} {value v}` | `[#####     ] 60%`, 0 to 100. It cannot take the focus. |
| `screen tabs f, id, labels {at x,y} {value n}` | A strip of tabs; the chosen one is the form's page (below). |
| `screen memo f, id, text {at x,y} {size w,h} {readonly} {wrap}` | A text area of several lines, one line to a field. `readonly` makes it a viewer; `wrap` wraps long lines at a blank instead of panning sideways. |
| `screen table f, id, columns, rows {at x,y} {size w,h} {value n} {multi}` | A heading and rows of cells (below). `multi` lets rows be marked. |
| `screen tree f, id, nodes {at x,y} {size w,h} {value n} {expanded}` | A tree of nodes, some open to show what is under them (below). |
| `screen scrollbar f, id, total {at x,y} {size w,h} {visible n} {value n}` | A scroll bar of its own, for content the program draws itself (below). |

#### The keys of the widgets

Tab and Down go to the next widget that can have the focus, Shift-Tab and Up to
the one before, round the ring (Down and Up only where the widget that has the focus
has no use for them: a list uses them to move through its entries). Return presses the
form's default button wherever the focus is. Esc cancels. A letter that no text widget
took presses the button that has it as its key. A widget that is disabled, or on
another page, is passed over.

| widget | keys |
|---|---|
| entry | left, right, home or Ctrl-A, end or Ctrl-E, backspace, delete or Ctrl-D, Ctrl-U (empty), Ctrl-K (cut to the end), Ctrl-W (cut the word before the cursor), and any printable character |
| check | the space bar |
| radio | up and down (left and right when `across`) move and choose as they go; the space bar chooses the one the cursor is on |
| list | up, down, home, end, page up, page down; a letter jumps; with `multi` the space bar picks |
| combo | as an entry field; down or F4 opens the list |
| tabs | left, right, home, end |
| memo | the arrow keys, home, end, page up and down; typing, Return (splits the line), backspace, delete (both join lines at the ends), Ctrl-K; Ctrl-A and Ctrl-E go to the ends of the row; Ctrl-B and Ctrl-F a word back and on; Ctrl-G the mark, Ctrl-X cut, Ctrl-C or Ctrl-O copy, Ctrl-V paste; Ctrl-Z undo, Ctrl-Y redo; Ctrl-T find, Ctrl-N the next one |
| table | up, down, home, end, page up, page down; left and right the current column; F3 sorts by it; `<` and `>` its width; a letter jumps to the next row whose first cell starts with it; with `multi` the space bar marks the row |
| tree | up, down, home, end, page up, page down; right opens a node (or goes to the first one under it); left closes it (or goes to the node it is under); the space bar opens or closes; a letter jumps |
| scrollbar | up and down (left and right when it is horizontal), page up, page down, home, end |

### Tabs and pages

```
screen tabs f, 'tabs', 'General':@vm:'Address':@vm:'Notes' at 2,1
screen page f, 1
screen entry f, 'name' at 10,3 width 20
screen page f, 2
screen entry f, 'street' at 10,3 width 20
screen page f, 0
screen button f, 'ok', '&OK' at 10,11 default
```

`screen page f, n` says that the widgets added **from now on** belong to tab *n*;
`screen page f, 0` ends it. A widget on a page is drawn, can take the focus and
answers keys only while that tab is the chosen one; one with no page, such as the
strip itself and the buttons, is on every page. The widgets of the other pages
keep their values and `get`, `set` and `values` still reach them. A form with no
strip shows every widget.

### The text area

`screen memo` serves as an editor and, with `readonly`, as a viewer. The last column is
a scroll bar. Page up and page down scroll by a page less one row with the cursor
keeping its row on the screen.

**Wrapping.** Without `wrap` a long line pans sideways as the cursor moves. With `wrap`
(or `screen set f, id wrap 1`) a line is broken after the last blank that fits, or in
the middle of a word that is longer than the width; the blank stays at the end of its
row and the text itself is not changed. Up, down, home, end, page up and page down then
work by *row*, so a wrapped line is several rows.

**Selection and the clipboard.** The selection runs from the *mark* to the cursor.
Ctrl-G sets the mark where the cursor is (and takes it away again); the selected text
is drawn in the `highlight` style. Ctrl-X cuts it, Ctrl-C or Ctrl-O copies it, Ctrl-V
puts what was cut or copied in at the cursor. The clipboard belongs to the library, so
it passes from one text area to another. Typing, Return, backspace and delete on a
selection replace or delete it. A `readonly` area can select and copy, and nothing else.

**Undo.** Ctrl-Z undoes and Ctrl-Y does it again, for up to 100 steps. A run of typed
characters (or of backspaces, or of deletes) is one step, and so is replacing a
selection by typing over it.

**Find.** Ctrl-T asks for text on the bottom row of the area and selects the first
place it is found from the cursor on; Ctrl-N finds the next one. Case is ignored and the
search goes on past the end of the text to its start. A bell means there is none.

Ctrl-B and Ctrl-F move a word back and on.

### The table

```
cols = 'Name':@sm:'10L':@vm:'Qty':@sm:'4R':@vm:'City'
rows = 'Smith':@vm:'12':@vm:'Albany'
rows<2> = 'Jones':@vm:'7':@vm:'Boston'
screen table f, 'people', cols, rows at 2,1 size 36,6
```

*columns* has one value for each column: the heading, and as a subvalue a width and
then `L`, `R` or `C` (left, right, centred): `'20L'`, `'6R'`. A column with no width
is as wide as its heading and the widest cell among its first 200 rows, at most 30.
*rows* has one row to a field and one cell to a value. The first row of the widget is
the heading and the last column a scroll bar. A click on a row makes it the current
one; a second click on the row the last click chose is Return.

**Sorting.** F3 sorts by the current column: ascending, then descending, then the order
of *rows* again. A column in which every cell is a number is sorted by value, any other
by its text without regard to case; the sorted column's heading shows `^` or `v`. A
click on a heading makes that column current and sorts by it in the same way. The
current row stays the same row through a sort. Sorting changes what is *shown*, never
`rows`: **`screen get` answers the number of the current row in `rows`**, whatever order
it is shown in.

**Columns.** Left and right move the current column (the heading of the current column
is in the `highlight` style once a key or a click has used the columns) and the table
scrolls sideways to show it when the columns are wider than the widget; at the first or
last column the keys are left for the form. `<` and `>` make the current column one cell
narrower or wider.

**Marked rows.** With `multi` the space bar marks or unmarks the current row (a click
does too); a marked row has a `*` in front of it. `screen get` and a Return then give the
numbers of the rows marked, in `rows`, as values (the current row if none is marked), and
the marks stay with their rows through a sort.

### The tree

```
nodes = 'Colours':@sm:1:@sm:'c'
nodes<2> = 'Red':@sm:2:@sm:'c1'
nodes<3> = 'Green':@sm:2:@sm:'c2'
nodes<4> = 'Shapes':@sm:1:@sm:'s'
screen tree f, 'tr', nodes at 2,1 size 20,6
```

*nodes* has one value for each node, in the order they are shown with everything open:
its label, as a subvalue its **depth** (1 for a root, 2 for what is under a root; 1 if
left out, never more than one deeper than the node before it), and as a second subvalue
the **code** the program gets for it (its number if left out). A node that has a deeper
node after it can be opened. The tree starts closed, or with every such node open under
`expanded`.

Each row is indented two cells for each level and shows `+` for a closed node with
something under it, `-` for an open one, and a blank for one with nothing under it. Up
and down move over the rows shown; right opens a closed node (or, on an open one, goes
to the first node under it); left closes an open node (or goes to the node this one is
under); the space bar opens or closes; a letter goes to the next node shown whose label
starts with it; Return is a *done* event of the form. A click on a node makes it
current, a click on its `+` or `-` opens or closes it, a second click on the node is
Return, and the wheel moves three rows. With more rows than room the last column is a
scroll bar. `screen get` answers the code of the current node, and each move of the
current node is a `change` event.

### The scroll bar

```
screen scrollbar f, 'sb', 200 at 40,1 size 1,10 visible 10
```

A scroll bar of its own, for a program that draws content itself (labels it changes with
`screen set`, say) and wants the user to scroll it. *total* is how many lines there are,
`visible` how many show at a time (the length of the bar if left out) and `value` the
number of the first line shown (1). `size w,h` makes it vertical (one cell wide, *h* long)
or, when *w* is the greater, horizontal; it is at least three long. The keys of its
direction, page up, page down, home and end move it, a click on an arrow moves one and a
click on the track either side of the thumb a page, and the wheel three. **Each move is a
`change` event whose data is the number of the first line shown**; the program redraws
its content from it. `screen set f, id value n` moves the bar and `screen get` answers
where it is.

### Running a form

```
screen run f {returning id} {then ... else ...}
```

Draws the form over the screen (what is under it is kept and put back), starts with
the focus on the first widget that can have it, and reads keys until a button is
pressed. `returning` holds the id of the button; `then` is taken for a button, `else`
for Esc, the form's cancel button, or the end of the input. **What the user typed
stays in the widgets**, so the program can check it and run the form again: the
second run starts where the first one left off.

```
loop
   screen run f returning pressed else exit
   screen get f, 'name' returning name
   if name = '' then
      screen msgbox 'The name is required.'
      screen focus f, 'name'
      continue
   end
   exit
repeat
```

### Waiting for events

`screen run` is for a form that is a dialogue. A program that must react between
key strokes (fill one list from another, validate a field when the user leaves it)
asks for **one event at a time**:

```
screen wait f {timeout s} returning ev {then ... else ...}
```

The first call draws the form and it **stays on the screen between calls**; each call
returns one event. `ev` is a dynamic array: field 1 the type, field 2 the widget's id,
field 3 its data.

| type | when | id | data |
|---|---|---|---|
| `button` | a button was pressed | its id | |
| `change` | a check box, radio group, list, combo, tab strip, table, tree or scroll bar changed its value | its id | the new value |
| `focus` | the focus moved | the widget it went to | the one it left |
| `key` | a key the form had no use for (a function key, a Ctrl key) | | its name |
| `resize` | the terminal's window changed size; the form has been drawn again at the new size | | the width, a value mark and the height |
| `cancel` | Esc, or the form's cancel button | the button, if any | |
| `timeout` | no key came in time | | |
| `end` | the input ended | | |

`then` is taken for `button`, `change`, `focus`, `key` and `resize`; `else` for `cancel`,
`timeout` and `end`. Esc does **not** close the form here: the program decides. An
entry field reports no event for each key typed; ask for its text with `screen get`
on a `focus` or `button` event. `screen hide f` puts the screen back.

### Reading and changing a form

| | |
|---|---|
| `screen get f, id returning v` | An entry or combo: the text. A check: 1 or 0. A radio: the number of the choice. A list: the number of the current item (with `multi`, the numbers picked, as values). Tabs: the tab. A table: the number of the current row in the rows given (with `multi`, the numbers of the rows marked). A tree: the code of the current node. A scroll bar: the number of the first line shown. A memo: the text, one line to a field. A label: its text. |
| `screen set f, id {value v} {text t} {items i} {enabled e} {wrap b} {readonly b} {visible b}` | `value` sets what `get` answers (a memo: replaces the text; tabs: chooses a tab; a scroll bar: moves it). `text` is a caption. `items` replaces the choices of a radio or list, or the rows of a table (the order of rows comes back). `enabled 0` takes a widget out of the focus ring. `wrap` and `readonly` (1 or 0) change a memo. `visible 0` hides any widget - it is not drawn and takes no focus - and `visible 1` shows it again. A form that is on the screen is redrawn at once. |
| `screen focus f, id` | The next `run` starts with the focus there. |
| `screen values f returning c` | A collection with the value of every entry, check, radio, list, combo, progress, tabs and table, named by id: `c{'name'}`. A memo is left out (ask for it with `get`). |
| `screen hide f` | Puts the screen back under a form shown by `wait`. |

## Styles and themes

Everything the library draws is drawn in a **named style**, and a **theme** says what
each style looks like. A program asks for styles and never for colours, so one program
works on a terminal with colour and one without.

| style | what it is for |
|---|---|
| `normal` | the terminal's own look |
| `reverse`, `underline`, `both` | the raw ones, the same in every theme |
| `bold` | bold text on the desktop (in `classic`, bright white on the blue desktop) |
| `window` | the body of a dialogue or form, and what is drawn in it |
| `highlight` | the selected entry, the button or field that has the focus |
| `bar` | a menu bar and the body of a menu |
| `barsel` | the selected entry of a bar |
| `hotkey`, `hotkey.bar` | a key letter, in a menu and on the bar |
| `field` | an entry field that has not the focus |
| `disabled` | an entry that cannot be chosen |
| `bar.disabled` | a disabled entry of a menu (dim, on the menu's own background) |
| `desktop` | what `screen clear`, `text` and `box` draw on |
| `text` | the text of a memo or a table |
| `header` | the heading row of a table |

```
screen theme name {returning current} {then ... else ...}
screen style name, foreground, background, flags
```

Three themes ship: **`mono`**, which uses only reverse video and underline and so reads
on any terminal; **`classic`**, dark text on light dialogues over a blue desktop; and
**`blue`**, white on blue dialogues. **A program that never asks gets `mono`**, unless
the administrator has set `SCREENTHEME=` in `sd.conf` to the theme the site wants; a
program that asks for a theme gets the one it asked for.
`screen theme` gives `else` for a name that is not a theme, on a terminal that cannot
show colour and in a phantom, and leaves the theme as it was; `returning` holds the name
in force. A null name only answers. If the library owns the screen it is drawn again in
the new theme, from the shadow. `screen close` puts the theme back to `mono`.

`screen style` changes one style of the theme in force. The colours are `black`,
`blue`, `green`, `cyan`, `red`, `magenta`, `brown` (or `yellow`) and `white`, or null for
the terminal's own; the flags are any of `bold`, `dim`, `reverse` and `underline`,
separated by spaces. It gives `else`, and changes nothing, for `normal` and the raw
styles, a name that is not a style, or a colour or flag it does not know. Choose the theme first, then
change its styles.

There are eight colours; `bold` makes the text bright. Colour comes from the terminal's
`setf` and `setb` capabilities, which the shipped `xterm`, `linux` and `ansi` entries
have. On a terminal that scrolls when its bottom right cell is written (`ansi`) the
library leaves that one cell of the desktop alone.

## Borders

Borders (`screen box`, a form's frame, a message box) are drawn with `+`, `-` and `|`,
which every terminal shows. `screen open ... lines` draws them with the line-drawing
characters of Unicode instead (`┌ ─ ┐ │ └ ┘`). It needs a terminal set to UTF-8 with a
font that has the characters, which is why it is asked for and not the default; on a
terminal without them the borders are unreadable, so a program should offer it as a
setting. A `+`, `-` or `|` that the program writes itself with `screen text` is left as
it is. `screen close` puts the plain borders back.

## The mouse

`screen open` asks an xterm-compatible terminal to report the mouse: buttons,
dragging and the wheel, in the form of xterm's modes 1000, 1002 and 1006. `screen close`
turns the reporting off. A terminal that does not know the modes, such as the Linux
console, ignores the request and sends nothing.

With reporting on, **forms and dialogues take clicks without any help from the
program**:

- a click on a button presses it; on a check box ticks or unticks it; on a radio
  button chooses it; on a row of a list or table makes it the current one (and a second
  click on that row is Return); on a tab chooses it; in an entry field or a memo puts
  the cursor under the pointer; on a combo's `[v]` opens its list;
- on a tree's node makes it current (a click on its `+` or `-` opens or closes it); on a
  table's heading sorts by that column; on a scroll bar's arrow or track moves it;
- the wheel scrolls a list, table, tree, memo or scroll bar three lines;
- in a message box a click on a button presses it; in a menu a click on an entry
  chooses it and a click elsewhere cancels it; in a pick list a click on an entry
  chooses it and a click outside the box cancels;
- a click of any button but the left, a release and a drag change nothing.

A program that reads keys itself with `screen key` sees `mouse` as the key, and
`screen mouse returning m` says what happened: field 1 the kind (`press`, `release`,
`drag` or `wheel`), 2 the button (1 left, 2 middle, 3 right, 4 for a drag with none held,
`up` or `down` for the wheel), 3 the column and 4 the row of the cell, from 0, and 5 any
of `s`, `a` and `c` for the shift, alt and control keys that were down.

`screen open nomouse` leaves the reporting off. **A program that stops without
`screen close` (a break, an error) leaves the terminal reporting**, and the mouse then
types garbage at the prompt until the terminal is reset (`reset`, or the terminal's own
reset command).

## What it does not do

- **A resize keeps only what the library drew.** SD reads the size of the terminal's
  window when the session starts and again when the window is resized; the library makes
  its picture the new size, keeps every cell of its shadow that still fits and draws it
  again, and a form being waited on gives a `resize` event. Text written with `print` or
  `crt` is lost, as for `screen refresh`, and a program that placed things by the old
  size must lay them out again (`screen refresh returning` says `resized`).
- A table sorts what it *shows*, never the rows you gave it, and a tree is the list of
  nodes you gave it with the depths you gave it: neither is a database view.
- It has no widget for editing a record with the editor's own commands: `screen memo` has
  selection, undo and find, and SED and the debugger keep their own screens.
- It draws nothing in a phantom or over the API: every verb takes `else`.
- Text written with `print` or `crt` is not in the shadow.

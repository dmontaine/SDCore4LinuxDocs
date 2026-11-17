Title: SD BASIC - The SCREEN Statement: Tabs, Tables and Containers
Subtitle: Tabs, the text area, the table, the tree, the scroll bar, and containers and viewports.

This page continues [SD BASIC - The SCREEN Statement:
Forms](12b-sd-basic-the-screen-statement-forms.html).

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

**Color for a language.** `syntax` *name* colors the text as the language *name*:
`sd.basic`, `c`, `json`, `markdown`, `sh`, `python`, or one a site added in the file
`&sed.syntax&` (the same languages and rules as [SED](27a-sd-tcl-sed.html)'s color). The colors
are the **theme's**, so the program chooses one that has them (`paper`, `night`, `classic` or `blue`;
`mono` has none, and the text is plain in it). A name that is not a language is not an error: the
text is drawn plain. The text is colored as it is edited — typing `*` at the start of an SD BASIC
line makes it a comment as it goes in. A text of some thousand lines is slower to draw for it, because
the color of a line depends on the lines above it.

```
screen theme 'night' returning th else crt 'no colour here'
screen memo f, 'src', text at 2,2 size 40,8 syntax 'sd.basic' lnum
```

**Line numbers.** `lnum` puts the number of each line down the left, as wide as the last
number needs and one blank more; the `size` includes them. A wrapped line has its number on
its first row only. The numbers are not part of the text: `screen get` answers the lines as they
are, and a click on the text counts from the first character, not from the numbers.

**Wrapping.** Without `wrap` a long line pans sideways as the cursor moves. With `wrap`
(or `screen set f, id wrap 1`) a line is broken after the last blank that fits, or in
the middle of a word that is longer than the width; the blank stays at the end of its
row and the text itself is not changed. Up, down, home, end, page up and page down then
work by *row*, so a wrapped line is several rows.

**Selection and the clipboard.** The selection runs from the *mark* to the cursor.
Ctrl-G sets the mark where the cursor is (and takes it away again); the selected text
is drawn in the `highlight` style. **Ctrl-A selects all the text** (Home is the start of the row). Ctrl-X cuts the selection, Ctrl-C copies it (Ctrl-O does not:
a program may use it for opening a record), Ctrl-V
puts what was cut or copied in at the cursor. The clipboard belongs to the library, so
it passes from one text area to another. Typing, Return, backspace and delete on a
selection replace or delete it. A `readonly` area can select and copy, and nothing else.

**Undo.** Ctrl-Z undoes and Ctrl-Y does it again, for up to 100 steps. A run of typed
characters (or of backspaces, or of deletes) is one step, and so is replacing a
selection by typing over it.

**Lines.** **Ctrl-D duplicates the line** the cursor is on, below it, and **Ctrl-K cuts the
whole line** into the clipboard. **Alt-K** does the same, for a program that keeps
Ctrl-K for itself through `passkeys`, as the IDE does. Ctrl-V at the start of a line puts a cut line back above it. Delete
joins lines.

**Find.** Ctrl-F or Ctrl-T asks for text on the bottom row of the area and selects the first
place it is found from the cursor on; Ctrl-B asks and looks backward. **F3 finds the next one and Shift-F3 the one before**
(Ctrl-N is left to a program, which may use it for a new record), and so does
Return on the question, which starts with the last text. Case is ignored and the
search goes on past the end of the text to its start. A bell means there is none.

Ctrl-P and Ctrl-U move a word back and on.

### The table

```
cols = 'Name':@sm:'10L':@vm:'Qty':@sm:'4R':@vm:'City'
rows = 'Smith':@vm:'12':@vm:'Albany'
rows<2> = 'Jones':@vm:'7':@vm:'Boston'
screen table f, 'people', cols, rows at 2,1 size 36,6
```

*columns* has one value for each column: the heading, and as a subvalue a width and
then `L`, `R` or `C` (left, right, centered): `'20L'`, `'6R'`. A column with no width
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

### Containers and viewports

```
screen form title 'Orders' at 0,0 size 140,42 returning f
screen viewport f, 'sheet' at 1,1 size 138,38 content 200,60 title 'Sheet'
screen in f, 'sheet'
for r = 0 to 29
   screen label f, 'l':r, 'Row ':r at 0, r*2
   screen entry f, 'e':r at 12, r*2 width 20
next r
screen in f, ''
screen button f, 'ok', '&OK' at 2,40 default
```

A **container** owns widgets. `screen in f, id` says that the widgets added **from now on**
are inside that container, as `screen page` does for a tab (`screen in f, ''` ends it).
A widget inside a container has its `at x,y` counted from **the first cell inside the
container's border** (0,0 is the cell right of and under the corner), not from the form's
corner. The widgets move with their container (`screen move`), are hidden, disabled or
put on a tab page with it (`screen set f, id visible 0`, `enabled 0`), and are taken out
with it (`screen delete`). What a widget draws, and where a click reaches it, is cut at
the edge of the container's inside: a long label stops at the border, an entry that
starts left of the inside shows only its right part. A container named while another is
current is inside that one, so containers nest to any depth; `screen in f, 'outer'` goes
back to an outer one. `noborder` leaves out the border: the inside is the whole rectangle,
and a widget at x,y is where it would be in the form at the container's corner plus x,y.

A **viewport** is a container whose inside is a window on a **sheet** `content cw,ch` cells
big (the default is no larger than the window, and then nothing scrolls). The widgets are
placed on the sheet, `at 0,0` being its top left cell, and only the part in the window is
drawn. When the sheet is higher than the window a scroll bar appears in the right column
of the inside, when it is wider one appears in the bottom row (so the window is one
column or row smaller than the inside). The viewport can take the focus (it is in the
Tab ring, ahead of its widgets), and then the arrow keys, page up and down, home and end
scroll it. The wheel scrolls it three rows, Shift and the wheel three columns, wherever the
pointer is over it, even over a widget in it that has no use for the wheel (a list, memo,
table, tree and scroll bar keep it for themselves) - and the wheel never moves the focus.
A click on a bar's arrow moves one, on the track a page, and the thumb can be dragged: the
sheet follows the pointer, which may leave the bar sideways and go past its ends. **A
widget that takes the focus (Tab, a click, or `screen focus` before the form is shown) is
scrolled into view**, as little as it takes; a widget bigger than the window gets its top
left corner shown.

```
screen scroll f, id {to x,y} {by dx,dy} returning v
screen move f, id {at x,y} {size w,h} {content cw,ch}
screen delete f, id returning n
```

`screen scroll` scrolls a viewport from the program (`to` first, then `by`): *x* is the
first column of the sheet to show and *y* the first row, from 0. It never goes past the
sheet's edge, and `returning` says where it ended up: the column, a value mark, the row.
`screen get f, id` of a viewport answers the same. `screen move` gives a widget a new
place, counted as it was given; a container, viewport, frame, text area, table or tree a
new size (`size`; a label or an entry field takes a width and stays one row high); and a
viewport a new sheet (`content`). Everything in a container goes with it, and a text area or
table keeps what it holds.
`screen delete` takes a widget out of the form (and a container everything in it, at any
depth) and says how many went; the id may be used again. `else` is taken when the form or
the widget is not there, or a size is asked of a widget that has none.

A scroll is a **`change` event** of the viewport's id whose data is the column, a value
mark and the row; if the same key also moved the focus the `focus` event is returned
instead. A scroll made by `screen scroll` is not an event.

Things to know:

- **The cursor.** While the focused widget is not wholly in view (scrolled out, cut by the
  edge, or taller than the window) the cursor is hidden; it comes back when the widget
  does. A viewport has no cursor of its own. So give a memo or a table a size that fits
  the window.
- **Pop-ups are not cut.** The list of a combo box is drawn over the whole screen, not
  inside the viewport.
- A viewport is not a window of its own: it is drawn into the form, and a later widget
  placed over it is drawn over it (a scroll draws it again too).
- Scrolling 200 by 60 of sheet (630 widgets) in a window of 138 by 40 takes about a tenth
  of a second a step, measured. The cost is the widgets in the window.

## Continued in

[SD BASIC - The SCREEN Statement: Running a Form, Styles and the
Mouse](12d-sd-basic-the-screen-statement-events-and-styles.html) — running a
form, styles, borders and the mouse.

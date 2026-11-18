Title: SD BASIC - The SCREEN Statement: Running a Form, Styles and the Mouse
Subtitle: Running a form, events, styles and themes, borders and the mouse.

This page continues [SD BASIC - The SCREEN Statement: Tabs, Tables and
Containers](12c-sd-basic-the-screen-statement-widgets.html).

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

`screen run` is for a form that is a dialog. A program that must react between
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
| `change` | a check box, slider, selector, radio group, list, combo, tab strip, table, tree or scroll bar changed its value, or a viewport was scrolled by the user | its id | the new value (a viewport: its first column, a value mark and its first row) |
| `focus` | the focus moved | the widget it went to | the one it left |
| `key` | a key the form had no use for (a function key, a Ctrl key) | | its name |
| `resize` | the terminal's window changed size; the form has been drawn again at the new size | | the width, a value mark and the height |
| `cancel` | Esc, or the form's cancel button | the button, if any | |
| `timeout` | no key came in time | | |
| `end` | the input ended, whether or not the statement has a `timeout` | | |

`then` is taken for `button`, `change`, `focus`, `key` and `resize`; `else` for `cancel`,
`timeout` and `end`. Esc does **not** close the form here: the program decides. An
entry field reports no event for each key typed; ask for its text with `screen get`
on a `focus` or `button` event. `screen hide f` puts the screen back.

### Reading and changing a form

| | |
|---|---|
| `screen get f, id returning v` | An entry or combo: the text. A check: 1 or 0. A radio: the number of the choice. A list: the number of the current item (with `multi`, the numbers picked, as values). Tabs: the tab. A table: the number of the current row in the rows given (with `multi`, the numbers of the rows marked). A tree: the code of the current node. A scroll bar: the number of the first line shown. A viewport: its first column and first row, from 0, with a value mark between. A memo: the text, one line to a field. A label: its text. |
| `screen set f, id {value v} {text t} {items i} {enabled e} {wrap b} {readonly b} {visible b}` | `value` sets what `get` answers (a memo: replaces the text; tabs: chooses a tab; a scroll bar: moves it). `text` is a caption. `items` replaces the choices of a radio or list, or the rows of a table (the order of rows comes back). `enabled 0` takes a widget out of the focus ring. `wrap` and `readonly` (1 or 0) change a memo. `visible 0` hides any widget - it is not drawn and takes no focus - and `visible 1` shows it again. A form that is on the screen is redrawn at once. **If `enabled 0` or `visible 0` (or a change of tab) takes the focus from the control that has it, the focus moves on to the next control that can have it, round the ring, or to none if there is none (the cursor is then hidden); a control that cannot have the focus takes no key.** **A clause written empty is not a clause left out:** a written `value`, `text` or `items` of `''` empties the control (an empty `value` on a check box, slider, radio group or list counts as 0); a clause left out changes nothing; and a written `''` on `enabled`, `wrap`, `readonly` or `visible` changes nothing, so an empty `readonly` cannot make a read-only memo editable. A program compiled before this rule must be compiled again. |
| `screen focus f, id {else}` | The next `run` starts with the focus there. On a form that is on the screen (between `wait`s) the focus moves for real: the control that had it and the control that has it are drawn, and the cursor goes to the new one. The control must be on the page the form shows, not hidden, not disabled and not inside a container that is hidden or disabled; otherwise the statement takes its `else` and nothing moves. The control that already has the focus is no move. A focus move made by the program is not reported as a `focus` event. |
| `screen values f returning c` | A collection with the value of every entry, check, radio, list, combo, progress, tabs and table, named by id: `c{'name'}`. A memo is left out (ask for it with `get`). |
| `screen hide f` | Puts the screen back under a form shown by `wait`. |

## Styles and themes

Everything the library draws is drawn in a **named style**, and a **theme** says what
each style looks like. A program asks for styles and never for colors, so one program
works on a terminal with color and one without.

| style | what it is for |
|---|---|
| `normal` | the terminal's own look |
| `reverse`, `underline`, `both` | the raw ones, the same in every theme |
| `bold` | bold text on the desktop (in `classic`, bright white on the blue desktop) |
| `window` | the body of a dialog or form, and what is drawn in it |
| `highlight` | the selected entry, the button or field that has the focus |
| `bar` | a menu bar and the body of a menu |
| `barsel` | the selected entry of a bar |
| `hotkey`, `hotkey.bar`, `hotkey.sel` | a key letter: in a menu, on the bar, and on the selected entry |
| `field` | an entry field that has not the focus |
| `disabled` | an entry that cannot be chosen |
| `bar.disabled` | a disabled entry of a menu (dim, on the menu's own background) |
| `desktop` | what `screen clear`, `text` and `box` draw on |
| `text` | the text of a memo or a table |
| `header` | the heading row of a table |
| `error` | an error message (in `mono`: reverse and bold) |
| `warning`, `success` | a warning, and a success message |
| `readonly` | a control that can be read but not changed |
| `busy` | a screen that is waiting for something |
| `focus` | the control that has the keyboard focus |

Every theme gives `warning`, `success`, `readonly`, `busy` and `focus` a look; in `mono`
they use only bold, underline and reverse. A program that includes `sl.h` must be compiled
again to use them (a normal install does this).

```
screen theme name {returning current} {then ... else ...}
screen style name, foreground, background, flags
```

Five themes ship: **`mono`**, which uses only reverse video and underline and so reads
on any terminal; **`paper`**, black and dark blue text on light gray, with the menu bar
and menus the other way round (light gray on black, their letters yellow and underlined);
**`night`**, white and yellow text on black, its menus black on light gray; **`classic`**, dark text on light dialogs over a blue desktop;
and **`blue`**, white on blue dialogs. All but `mono` have the **syntax colors** (the colors that
`screen memo ... syntax` and SED's color for the language use). **A program that never asks gets `mono`**, unless
you have chosen a theme with Ctrl-T on one of SD's own pages (SD keeps that choice, and
`screen open` starts in it) or the administrator has set `SCREENTHEME=` in `sd.conf` to the
theme the site wants (the shipped `sd.conf` says `SCREENTHEME=paper`; with neither it stays
`mono`, and a terminal with no color is `mono` whatever the line says); a
program that asks for a theme gets the one it asked for.
`screen theme` gives `else` for a name that is not a theme, on a terminal that cannot
show color and in a phantom, and leaves the theme as it was; `returning` holds the name
in force. A null name only answers. If the library owns the screen it is drawn again in
the new theme, from the shadow. `screen close` puts the theme back to `mono`.

`screen style` changes one style of the theme in force. The colors are `black`,
`blue`, `green`, `cyan`, `red`, `magenta`, `brown` (or `yellow`) and `white`, or null for
the terminal's own; the flags are any of `bold`, `dim`, `reverse` and `underline`,
separated by spaces. It gives `else`, and changes nothing, for `normal` and the raw
styles, a name that is not a style, or a color or flag it does not know. Choose the theme first, then
change its styles.

There are eight colors; `bold` makes the text bright. Color comes from the terminal's
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
console, ignores the request and sends nothing; **on a Linux text console SD also asks the
gpm daemon for the mouse** (only for the terminal type `linux` and
only when the input is a text console, and not with `nomouse`), and the program is given the
same reports (see the terminfo page, *The Linux text console*). Without a daemon there is no mouse.

With reporting on, **forms and dialogs take clicks without any help from the
program**:

- a click on a button presses it; on a check box ticks or unticks it; on a slider or selector sets the word clicked (a slider slides the other way, a selector goes to the next word, if the text is clicked); on a radio
  button chooses it; on a row of a list or table makes it the current one (and a second
  click on that row is Return); on a tab chooses it; in an entry field or a memo puts
  the cursor under the pointer; on a combo's `[v]` opens its list;
- on a tree's node makes it current (a click on its `+` or `-` opens or closes it); on a
  table's heading sorts by that column; on a scroll bar's arrow or track moves it;
- the wheel scrolls a list, table, tree, memo or scroll bar three lines; over a viewport
  it scrolls the viewport three rows (Shift: three columns), and a press on the thumb of
  its bar followed by moves of the pointer with the button held drags the sheet along;
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
- **It imposes no window size and no lock on your program.** Ask for the size you need with
  `minsize`; a window that becomes smaller later cuts what falls outside it (cells outside the
  window are dropped, not wrapped) and your program keeps its keys. SD's own full-screen
  programs are laid out for 140 by 43: CED, when its cursor is off the screen, takes the
  keyboard behind a warning until the window is made bigger or you press Ctrl-Q, y; the IDE,
  SED and the toolkit pages do it whenever the window is smaller than that, wherever the cursor
  is; the library routines that do it are SD's own and are not a statement.
- A table sorts what it *shows*, never the rows you gave it, and a tree is the list of
  nodes you gave it with the depths you gave it: neither is a database view.
- It has no widget for editing a record with the editor's own commands: `screen memo` has
  selection, undo, find and keyboard macros (Alt-R, Alt-P), but not the tabs, the menus or the
  compile and run keys of the IDE and [SED](27a-sd-tcl-sed.html), which are those programs' own.
  The IDE, SED, [CED](27b-sd-tcl-ced.html) and
  [the debugger](17-sd-basic-debugging.html) are drawn with the library.
- It draws nothing in a phantom or over the API: every verb takes `else`.
- Text written with `print` or `crt` is not in the shadow.

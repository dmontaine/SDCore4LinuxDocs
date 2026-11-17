Title: SD BASIC - The SCREEN Statement: Forms
Subtitle: Forms and the widgets that go on them.

This page continues [SD Basic - The Screen
Statement](12a-sd-basic-the-screen-statement.html).

## Forms

A form holds widgets and the focus, and routes the keys. You build it with
statements, then run it, or wait on it for events.

```
screen form {title t} {at x,y} {size w,h} {fill} returning f
```

**A form that follows the window.** With `fill` the form takes the whole window and is laid
out again whenever the window changes. Its size (given with `size`, or worked out from what
is in it) is the smallest window the program is laid out for. A text area or table added with
`stretch` takes the spare room, and whatever lies to its right or below it moves over by what
it grew; nothing else changes. Several stretching widgets on the same rows share the room.
Below the form's own size the keyboard is held behind one warning until the window is made
larger, and the form then comes back by itself. A program needs no code for a resize:

```
screen open clear else stop
screen form title 'Notes' size 60,18 fill returning f
screen memo f, 'n', text at 2,1 size 56,12 stretch 'both'
screen button f, 'ok', '&OK' at 2,15 default
screen run f returning pressed then null else null
screen close
```

`f` is a data collection: `jbuild(f)` writes the form out as JSON and `jparse`
reads it back, so a screen can be kept as a record. A form left without a size is
as big as its widgets need; without a place it is centered.

### Adding widgets

Every widget verb takes the form and the widget's **id** first, and `at x,y`, the
place of the widget from the form's top left corner (0,0 is the corner of the
border; the default is 1,1). The id is the widget's name: not null, not used
before, and with no `/` or `*` in it. `else` is taken if a widget cannot be added.

Most controls take `color fg,bg` as their last clause (a label, entry, check box, slider, radio group, list, combo box, button and progress bar; not a memo, table, tree or the tab strip, which have their own styling). The colors are black, blue, green, cyan, red, magenta, brown and white, for example `color 'black','green'`; either may be left out for the terminal's own. A pair of colors is one of sixteen spare styles the program shares, however many controls use it, and a seventeenth different pair, or a word that is no color, makes the statement take its `else`. The colors survive `screen theme`. A colored **entry or combo box keeps its colors while it has the focus** (the cursor and an underline show where it is); every other control draws its colors until it has the focus and then the focus style. On a terminal that cannot show color the clause is ignored.

**Accelerator keys.** An entry, combo box, check box, slider, selector, radio group, list, button, tab strip, memo, tree and table take `accel key` as their last clause: `accel 'alt-s'`, `'ctrl-g'`, `'f5'`. The key is f1 to f12, ctrl-a to ctrl-z (not ctrl-h, ctrl-i, ctrl-j or ctrl-m, which a terminal sends as Backspace, Tab and Return) or alt-a to alt-z and alt-0 to alt-9, in either case with a `-` or a `+` (`Alt+S`, `alt-s` and `ALT-S` are one key); any other word makes the statement take its `else`. The key reaches the control **wherever the focus is, even inside a text field**, before the focused control sees it. What it does: a button is pressed; a check box is ticked or unticked, a slider slid and a selector moved to its next word, each with a `change` event (not only a `focus` one); every other control takes the focus (a `focus` event). A control that is disabled or on another tab's page does not answer. Two controls given the same key: the first one added answers. The same applies to a letter marked with `&` in the text of a **button, check box, slider, selector or label** (`'&Shell'`, Alt+S): that letter is also the control's Alt-letter, and it is drawn underlined (in the `hotkey` style of the theme: underline in the mono theme, a color in the color themes) while the control does not have the focus and is not disabled. A label has no focus of its own, so its Alt-letter takes the focus to the next control that can have it: put `&Name` before the entry it names. A label reads the `&` only when it is created, so `screen set ... text` leaves an ampersand where it is. A button still also answers its plain letter when no field takes it, as before. Alt-letters reach the program only if the terminal sends Alt+x as Esc and x (most do: gnome-terminal, konsole, kitty, xterm with `metaSendsEscape`, PuTTY; macOS Terminal needs "Use Option as Meta key"), and some terminals or window managers keep a few for themselves (a menu on Alt+F, tabs on Alt+1 to 9), so pick an `f` key or a ctrl-letter where that matters. Ctrl-c, ctrl-q, ctrl-s and ctrl-z may be taken by the terminal itself. An Esc followed by a letter within a fifth of a second is read as an Alt-letter; an Esc on its own is still Esc (a cancel).

| verb | what it adds |
|---|---|
| `screen label f, id, text {at x,y} {attr style} {width n} {color fg,bg}` | Text. A label that will be changed with `screen set` needs `width` for its longest text: a status line is a label with a width. `color` wins over `attr`. |
| `screen frame f, id {at x,y} {size w,h} {title t}` | A border (it draws only the border; widgets added after it sit over it). |
| `screen entry f, id {at x,y} {width n} {value v} {mask} {maxlen n} {color fg,bg} {accel key}` | One line of text; a longer text scrolls. `color 'black','green'` draws the field in those colors, also while it has the focus. |
| `screen check f, id, text {at x,y} {value 0 or 1} {place where} {color fg,bg} {accel key}` | `text [x]`: the label, then the box. `place` says where the label is in relation to the box: `left` (the default), `right` (`[x] text`), `above` or `below` (the control is two rows high). A click on the box or on the label checks or unchecks it. |
| `screen slider f, id, text {at x,y} {value 0 or 1} {attr style} {words w1,w2} {place where} {color fg,bg} {accel key}` | An on / off switch with its label (`place` as for a check box; left by default): `text [off | ON]` when it is on and `text [OFF | on]` when it is off. `words 'left','right'` chooses the two words (the first is the off state, the second the on state): `[left | RIGHT]` and `[LEFT | right]`. The word in force is in capitals and in the style `attr` (any style of the theme: `bold`, `highlight`, `header`, `error`, `underline` ...; bold when you give none, which is a color in a color theme; `window` leaves it as the form's own, so that only the capitals show the state). Space slides it the other way, Left sets it off, Right sets it on; a click on a word sets that state and a click on the label slides it the other way. `screen get` answers 1 or 0 and `screen set f, id value v` sets it (any value but 0 is on). |
| `screen selector f, id, text, words {at x,y} {value n} {attr style} {place where} {color fg,bg} {accel key}` | One word of several in a row: `text [blue | green | RED | black]`, with `words` a dynamic array (`'blue':@vm:'green':@vm:'red':@vm:'black'`) of any length (an empty one makes the statement take its `else`). The word in force is in capitals and in the style `attr` (as for a slider: bold by default, `window` for the capitals alone), the others in lower case; `place` and `color` are as for a check box. Left and Right choose the previous and the next word and stop at the ends, Home and End the first and the last, Space the next word (the first after the last); a click on a word, the space after it or either bracket chooses it, a click on the label the next word. `screen get` answers the number of the word in force counted from one (3 for RED), `screen set f, id value n` chooses one (a number outside the words is brought into range) and `screen set f, id items words` gives it other words (the first is chosen). A change is a `change` event with the number. |
| `screen radio f, id, items {at x,y} {value n} {across} {color fg,bg} {accel key}` | One choice of several, one to a row (or side by side with `across`). |
| `screen list f, id, items {at x,y} {size w,h} {value n} {multi} {color fg,bg} {accel key}` | A list of values to choose from; `multi` lets several be picked. |
| `screen combo f, id, items {at x,y} {width n} {value v} {color fg,bg} {accel key}` | An entry field with a `[v]` that opens a list of choices. |
| `screen button f, id, text {at x,y} {default} {cancel} {color fg,bg} {accel key}` | `[ text ]`. `default`: Return in any other widget presses it. `cancel`: pressing it, like Esc, ends the form with `else`. An `&` marks its key. |
| `screen progress f, id {at x,y} {width n} {value v} {color fg,bg}` | `[#####     ] 60%`, 0 to 100; `color` draws the filled part. It cannot take the focus. |
| `screen tabs f, id, labels {at x,y} {value n} {accel key}` | A strip of tabs; the chosen one is the form's page (below). |
| `screen memo f, id, text {at x,y} {size w,h} {readonly} {wrap} {syntax name} {lnum} {accel key} {stretch how}` | A text area of several lines, one line to a field. `readonly` makes it a viewer; `wrap` wraps long lines at a blank instead of panning sideways; `syntax` *name* draws the text in the syntax colors of a language; `lnum` puts line numbers down the left; `stretch` `'w'`, `'h'` or `'both'` makes it grow with the window in a `fill` form (any other word takes `else`). |
| `screen table f, id, columns, rows {at x,y} {size w,h} {value n} {multi} {accel key} {stretch how}` | A heading and rows of cells (below). `multi` lets rows be marked; `stretch` as for a text area. |
| `screen tree f, id, nodes {at x,y} {size w,h} {value n} {expanded} {accel key}` | A tree of nodes, some open to show what is under them (below). |
| `screen scrollbar f, id, total {at x,y} {size w,h} {visible n} {value n}` | A scroll bar of its own, for content the program draws itself (below). |
| `screen container f, id {at x,y} {size w,h} {title t} {noborder}` | A rectangle that owns the widgets added after `screen in` (below). |
| `screen viewport f, id {at x,y} {size w,h} {content cw,ch} {title t} {noborder}` | A container whose inside is a window on a larger sheet of widgets, with scroll bars (below). |

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
| memo | the arrow keys, home, end, page up and down; typing, Return (splits the line), backspace, delete (both join lines at the ends); Home and Ctrl-E go to the ends of the row; Ctrl-P and Ctrl-U a word back and on; Ctrl-A selects all, Ctrl-G the mark, Ctrl-X cut, Ctrl-C copy, Ctrl-V paste; Ctrl-D duplicates the line, Ctrl-K (or Alt-K) cuts the whole line into the clipboard; Ctrl-Z undo, Ctrl-Y redo; Ctrl-F or Ctrl-T find, Ctrl-B find backward, F3 the next one; and SED's editing commands: Alt-Backspace and Alt-D delete the word before or at the cursor, Alt-E cuts to the end of the line, Alt-T swaps two characters, Alt-U, Alt-L and Alt-C put the word in capitals, in small letters or with a capital initial, Alt-Space closes a run of blanks into one, Alt-A indents the line as the line above, Alt-M swaps the cursor and the mark, and Ctrl-Up and Ctrl-Down move the view a line (not in a memo that wraps) |
| table | up, down, home, end, page up, page down; left and right the current column; F3 sorts by it; `<` and `>` its width; a letter jumps to the next row whose first cell starts with it; with `multi` the space bar marks the row |
| tree | up, down, home, end, page up, page down; right opens a node (or goes to the first one under it); left closes it (or goes to the node it is under); the space bar opens or closes; a letter jumps |
| scrollbar | up and down (left and right when it is horizontal), page up, page down, home, end |
| viewport | up, down, left, right (one row or column), page up, page down, home (the top), end (the bottom); at the edge the key goes on to the widget before or after |

## Continued in

[SD BASIC - The SCREEN Statement: Tabs, Tables and
Containers](12c-sd-basic-the-screen-statement-widgets.html) — tabs, tables,
trees and viewports.

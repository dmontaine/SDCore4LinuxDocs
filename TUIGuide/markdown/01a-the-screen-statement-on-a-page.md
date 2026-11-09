Title: SD Text User Interface - The Screen Statement on a Page
Subtitle: Which part of the screen statement a page uses, which part belongs to the library, and how the two work together.

The library draws the frame of a page. Everything inside the frame - the boxes,
the lines of text, a table, a form, a question - your program draws with the
`screen` statement. This page says how the two share one screen. The statement
itself is defined in the page "The Screen Statement" of the User set, which gives
every clause and every key. The first section below describes the statement as a
whole, so that this guide can be read on its own; the rest of the page says how a
page uses it.

## The screen statement

`print`, `crt` and `input` talk to a terminal a line at a time. The `screen`
statement talks to it a screen at a time: it draws text and boxes where you say,
asks a question in a dialog box, runs a form of entry fields, lists, tables and
buttons, and reads keys and clicks of the mouse. It is one statement word followed
by a verb:

```
screen verb {value {, value}} {clause value {, value}} ... {returning variable} {then ... else ...}
```

* **The verb says what to do**: `text`, `box`, `msgbox`, `form`, `wait`, `theme` and
  so on. The verbs and clauses are not reserved words; a program may still have a
  variable called `title` or `screen`.
* **Values first, then clauses.** A verb takes a fixed number of values after its
  name, then clauses - a keyword and its values - in any order and all optional:
  `at 10,4`, `size 20,5`, `title 'Total'`, `width 30`. A clause left out takes the
  verb's default.
* **`returning`** names the one variable the statement sets: the key, the button,
  the text typed, the event.
* **`then` and `else`.** `then` when the person finished (a button, a choice,
  Return); `else` when they canceled (Esc), the input ended, or there is no
  terminal. A phantom or an API session takes `else` on every verb and draws
  nothing, so a program that uses `screen` does not hang when run unattended.
* **Coordinates** are character cells from 0, as in `@(x, y)`: `at 0,0` is the top
  left corner. On a page the body starts at column 1, row 1.
* **Styles, not colors.** Everything is drawn in a named style - `window`,
  `highlight`, `bar`, `field`, `error`, `desktop` and others - and the **theme** says
  how each style looks, so one program works on a terminal with color and one
  without.
* **The shadow.** Once the screen is open, the library keeps its own picture of
  every cell it drew. A dialog saves what is under it from that picture and puts
  it back when it closes. Text written with `print` or `crt` is not in it.

The verbs, by what they are for:

| Group | Verbs | |
|---|---|---|
| The screen | `open`, `close`, `clip`, `refresh`, `size` | Take and give back the screen (on a page, `!tkopen` and `!tkclose` do this), keep drawing inside a rectangle, draw everything again, read the window's size. |
| Drawing | `clear`, `text`, `box`, `cursor` | Blank a rectangle, write one line, draw a border, place or hide the cursor. `text` takes `width` to cut or pad; `box` takes `title` and `fill`. |
| Keys and the mouse | `key`, `mouse` | Wait for one key (`up`, `f1`, `ctrl-q`, `alt-x`, `resize`, `mouse` or the character), with an optional `timeout`; then, for `mouse`, what the event was: the kind, the button, the column, the row. |
| Dialogs | `msgbox`, `ask`, `pick`, `menu`, `menubar` | A message with buttons; one line of input (`mask` for a password); a list to choose from (`multi` for several); a pop-up menu; a menu bar (on a page, `!tkmenubar` draws the bar). Each saves what is under it and puts it back. |
| Forms | `form`, then `label`, `entry`, `check`, `slider`, `selector`, `radio`, `list`, `combo`, `button`, `progress`, `tabs`, `page`, `memo`, `table`, `tree`, `scrollbar`, `frame`, `container`, `viewport`, `in` | A form is a data collection that holds widgets. Each widget verb takes the form, the widget's id and its place inside the form. A `memo` is a text area (an editor, or a viewer with `readonly`); a `table` has headings, columns and sorting; a `tree` has nodes that open and close. |
| Running a form | `run`, `wait`, `hide` | `run` reads keys until a button ends the form, as a dialog. `wait` returns one event at a time - `button`, `change`, `focus`, `key`, `resize`, `cancel`, `timeout`, `end` - and leaves the form on the screen between calls; `hide` takes it away. |
| Reading and changing a form | `get`, `set`, `focus`, `values`, `move`, `delete`, `scroll` | Read a widget's value, change its value, text, items or whether it is enabled or visible, move the focus, read every value at once, move or take out a widget, scroll a viewport. |
| The look | `theme`, `style` | Choose a theme - `mono`, `classic`, `blue`, `dark`, `light` - or change one style of it. `else` on a terminal that cannot show color. |

The example at the head of the User page, a form run as a dialog without the
library:

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

It writes its answer with `crt` once `screen run` has put the screen back; a page
would put the same message on its status line instead.

On a page the same verbs are used inside the frame the library draws: the program
says neither `screen open` nor `screen close`, and the form stands in a pane.

## Who owns what

| Part of the screen | Drawn by | |
|---|---|---|
| Taking and giving back the screen | `!tkopen`, `!tkclose` | `!tkopen` says `screen open clear` (with `lines` when the terminal says UTF-8); `!tkclose` says `screen close`. **Your program never says `screen open` or `screen close` itself.** |
| Row 0, the menu bar | `!tkmenubar` | Made from the key table. Do not use `screen menubar` on a page. |
| The status line, the border, the row of keys | `!tkframe` | The last three rows. |
| The body | your program | From `TK.C.YBODY` to the row above `TK.C.YSTAT`, in the panes `!tklayout` gives. |
| A confirm box, a form, a pick list | `!tkconfirm`, `!tkform`, `!tkpickrec` | Drawn over the page and taken away again. |

So a page draws in the body only, and only with the `screen` statement.

## The verbs a page uses

**In the body:**

| Verb | What a page uses it for |
|---|---|
| `screen clear at x,y size w,h` | Blank the body, or one pane, before drawing it again. |
| `screen box at x,y size w,h title t {fill}` | The border of a pane. `fill` blanks its inside as well. |
| `screen text s at x,y width n` | One line of a pane. `width` cuts or pads it, so a shorter text leaves no tail of the longer one. |
| `screen cursor` | Where the cursor stands, and whether it shows. |
| `screen form`, the widget verbs, `screen wait`, `screen get`, `screen set`, `screen hide` | A form in a pane: a table, a list, a tree, entries, check boxes. [A Form in the Body](05b-a-form-in-the-body.html) is the example. |

**For keys and the mouse:**

| Verb | |
|---|---|
| `screen key returning nm` | The page's wait when its body has no form. Every example but `stock` uses it. |
| `screen wait f returning ev` | The page's wait when its body is a form: the form answers its own keys, and the keys it has no use for come back as `key` events for the menu bar and your program. |
| `screen mouse returning m` | What the click was, after the key `mouse`; give it to `!tkmenubar('click', ...)`. |
| `screen size returning v` | The window's size, if a program needs it outside the layout. |

**Over the page:** `screen msgbox`, `screen ask`, `screen pick` and `screen menu`
are dialogs. Each saves what is under it, asks, and puts the page back, so a page
may use them as they are.

**The look:** `screen theme` and `screen style` work on a page; the page is drawn
again in the new theme. `!tkclose` gives back the screen, and with it the theme,
which `screen close` puts back to `mono`.

## A page draws by difference

On a screen taken by `!tkopen`, `screen text`, `screen box` and `screen clear`
change the library's picture of the screen (its **shadow**) and write to the
terminal only the cells that are not already there. They are written when the
program next waits - at `screen key` or `screen wait` - so a program may clear a
pane and draw it again without the pane flickering.

Three things follow:

* **Draw again freely.** Redrawing a whole pane after every change costs only the
  cells that changed. `browse` and `stock` redraw a pane on every move of the
  cursor.
* **Do not `print` or `crt` on a page.** Text written that way is not in the
  shadow: the page neither keeps it nor knows it is there. Show a message with the
  `msg` of `!tkframe`, a line in the output pane (`!tkout`), or a `screen msgbox`.
* **F5 and Ctrl-L repaint.** When `screen key` reads either of them on a page, the
  whole screen is written again from the shadow at the next wait, and the key is
  still given to the program. A program that waits with `screen wait` gets the key
  as a `key` event and nothing more.

## A pane is drawn from its place

Every place in the body comes from `!tklayout('pane', ctx, id, r)`: `r<1,1>` and
`r<1,2>` are the column and row of the pane's top left corner, `r<1,3>` and
`r<1,4>` its width and height. Draw each pane from those four numbers, never from
fixed numbers, and the same code draws the page in any window the floor allows.
After the key `resize`, `!tklayout('refresh', ...)` gives the panes their new
places; the program clears the body, draws every pane again and raises
`ctx<TK.C.GEN>` by one, so that the frame is written whole.

The two calls side by side, from [A Bare Page](02-a-bare-page.html):

```
   r = ''
   call !tklayout('pane', ctx, 'main', r)
   screen box at r<1,1>,r<1,2> size r<1,3>,r<1,4> title 'Hello'
   screen text s at r<1,1> + 2,r<1,2> + 1 width r<1,3> - 4
```

The text stands two columns inside the border and one row under it, and is cut two
columns short of the right border.

## Where each example uses it

| Example | `screen` verbs | With the routines |
|---|---|---|
| `hello` | `clear`, `box`, `text`, `key` | `!tklayout('pane')` for the place, `!tkframe` around it |
| `menus` | `clear`, `box`, `text`, `key`, `mouse` | `!tkmenubar('key')` and `('click')` take the key and the click first |
| `notes` | `clear`, `box`, `text`, `key` | `!tkform` and `!tkconfirm` over the body, `!tkout` for its pane |
| `browse` | `clear`, `box`, `text`, `key` | two panes and the focus marks of `!tkframe`, `!tkwrap` for the text |
| `stock` | `form`, `table`, `wait`, `set`, `hide`, `box`, `text`, `clear`, `ask`, `msgbox`, `theme`, `mouse` | the menu bar and the finder take the `key` events of the form |

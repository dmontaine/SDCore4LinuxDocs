Title: SD Basic - The Screen Statement
Subtitle: Menus, dialogs, forms, color and the mouse, from BASIC.

`print`, `crt` and `input` talk to a terminal one line at a time. The `screen`
statement talks to it a screen at a time: it draws text and boxes where you say,
asks the user a question in a dialog box, runs a whole form of entry fields,
check boxes, lists and buttons, shows a menu bar, and takes clicks of the mouse.
It needs no extra package and no change to the rest of the program: it is one
statement word followed by a verb.

This page is the reference for the statement. A guide to building a whole
full-screen page with it and SD's own `!tk` routines, with worked examples, is the
separate *SD Text User Interface - Programmer's Guide* set of this documentation.

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
- **`then` and `else`.** `then` is taken when the user finished the dialog
  (a button, a choice, Return); `else` when the user canceled (Esc), the input
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

A dialog covers the text under it, and the terminal cannot be asked what it was
showing. So once a program has said `screen open`, the library keeps a **shadow**:
its own record of every cell it has drawn and in what style. A dialog saves what
is under it from the shadow and puts every character back when it closes.

**Text the program writes with `print` or `crt` is not in the shadow.** Draw what
must survive a dialog with `screen text`, or `screen refresh` will not bring it
back. Before `screen open` a dialog still works, but it leaves blanks where it
was.

**A form on a screen opened with `clear` writes only what has changed.** The terminal is then known to show the shadow, so when a form is
drawn again, or one of its widgets is, the text that is already there in the same style
is left out; choosing a record in the IDE wrote 6,635 characters to the terminal
before and about 780 now. Two things follow. A form does not repair what the program
printed over it with `print` or `crt`, only `screen refresh` does; and a screen opened
*without* `clear` is written in full, as before, because the terminal may show what the
program printed there. `screen text`, `screen box` and the dialogs always write what
they are told.

| | |
|---|---|
| `screen open {clear} {nocursor} {minsize w,h} {nomouse} {lines}` | Takes the screen. `clear` clears it (to the theme's desktop color); `nocursor` hides the cursor; `minsize` gives `else` on a smaller terminal; `nomouse` leaves mouse reporting off (see below); `lines` draws every border in the line-drawing characters of Unicode (see *Borders*). `else` also when there is no terminal. |
| `screen close` | Gives the screen back: the shadow is forgotten, the cursor shown, mouse reporting off, the clip taken off, borders plain again, the theme back to mono, and the cursor moved to the first column of the last line. A colored desktop is cleared. |
| `screen clip {at x,y size w,h}` | Keeps everything the library draws inside the rectangle: text, boxes, forms and dialogs that reach outside it are cut at its edge, cell by cell, and the cut part is neither drawn nor remembered. With no rectangle the clip is taken off. `else` when the library does not own the screen (no `open`) or there is no terminal. |
| `screen clear {at x,y} {size w,h} {attr style}` | Blanks the whole screen, or a rectangle of it, in the style given (default `desktop`). |
| `screen text string {at x,y} {attr style} {width n}` | Draws one line. Left out, `at` is where the last `screen text` ended. `width` cuts or pads the text to exactly that many cells. Text past the right edge is cut, not wrapped. |
| `screen box {at x,y} {size w,h} {title t} {attr style} {fill}` | Draws a border (`+`, `-`, `|`, or the line-drawing characters after `screen open lines`) and, with `fill`, blanks the inside. |
| `screen cursor {at x,y} {on} {off}` | Moves the cursor, shows it or hides it. The library puts it back there after each command that draws. |
| `screen refresh` | Clears the terminal and draws the shadow again. `returning` holds `resized` if the terminal's size has changed since `open`; the program then draws everything again. |
| `screen size returning v` | The width, a field mark and the height, as the terminal is now. |
| `screen key {timeout s} returning k` | Waits for one key. `k` is `up down left right home end pgup pgdn ins del bs tab btab enter esc f1` to `f12`, `ctrl-a` to `ctrl-z`, `alt-a` to `alt-z` and `alt-0` to `alt-9` (an Alt-letter, always in lower case), `mouse`, or the character itself. `else` on timeout or end of input. |
| `screen mouse returning m` | What the last mouse event was (below). |

Styles are named, not colored: see *Styles and themes*.

## Dialogs

A dialog asks one thing, waits, puts the screen back and gives the answer.

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
| `at` | The top left cell; centered if left out, and moved to fit. |
| `returning` | The number of the button chosen, 0 for Esc. `then` is taken when a button was chosen. |

Left and right move between the buttons, Return presses the one that has the
focus, a button's letter presses it at once, and a click of the mouse on a
button presses it.

The box is never taller than the screen. A text with more lines than fit
scrolls: PgUp and PgDn move a box at a time, Home and End go to the first and
the last lines, and the bottom border says which lines are shown
(`lines 1-30 of 75, PgUp PgDn`). The buttons stay on the screen. A text that
fits is shown as before.

### menu

```
screen menu items {at x,y} {default n} {returning code}
```

*items* are values (or fields), each *label* `@sm` *shortcut* `@sm` *code*. The
shortcut is text shown beside the entry; the program acts on the key itself. The
code is what comes back; without one the entry's number does. An entry of `-` is
a line across the menu. An `&` in a label marks its key.

**A menu with more entries than there are rows** under its top (a short window; the menu bar
cannot move up, a pop-up and a submenu first move up as far as they can) **shows the rows
that fit and scrolls** as the cursor moves: a `^` in the last cell of the first row says there
are entries above it and a `v` in the last cell of the last row says there are more below. The
cursor keys, Home, End, a letter and a click work as ever on the entries that are in view or
scrolled to.

A **fourth subvalue** holds flags: `D` makes the entry *disabled* (it is drawn dim, the
cursor keys go past it, Return and its letter choose nothing) and `C` makes it *checked*
(a `*` in its first cell, for a setting that is on):

```
items = 'Open':@vm:'Save':@sm:'':@sm:'save':@sm:'D':@vm:'Autosave':@sm:'':@sm:'auto':@sm:'C'
```

### menu bar

```
screen menubar menus {row r} {draw} {click x} {returning code}
```

*menus* has one **field** for each menu: its title, then its entries as values,
each as for `screen menu`. With `draw` the bar is drawn and the statement returns;
without it the first menu opens at once. Left and right move between menus, up
and down between entries, Return chooses, Esc leaves, a letter chooses the entry
that has it. Clicking a title opens that menu; clicking an entry chooses it;
clicking anywhere else closes the menus. Entries take the same `D` and `C` flags as
those of `screen menu`.

**`click x`** is for a program that has been told of a click on a bar that is not open
(`screen key` gave `mouse` and `screen mouse` says where; a form gives it the same way
for a click on no widget when the program has asked for those): *x* is the column of the
click, and the menu whose title is over it opens instead of the first. A column with no
title over it (the space to the right of the titles) opens nothing, and the statement
takes `else`. A title is its label with a blank on each side, from column 0.
A program compiled by an older version that uses `screen menubar` must be compiled
again.

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
screen ask prompt {value v} {width n} {title t} {at x,y} {mask} {history list} {returning text}
```

One line of input. `mask` shows a `*` for each character. The keys are those of
an entry field (below). `history` gives earlier answers, newest first, as fields:
Up shows the next older one and Down the next newer, and Down past the newest gives
back what had been typed. Ctrl-R shows the newest whatever is shown. Your program keeps the list
and adds to it; `screen ask` never changes it. A `mask` question recalls nothing.

To ask for a change to a value without putting the value in the field, open the field empty and
give the value as the history: `screen ask 'Directory (now: ' : cv : ')' value '' history cv returning
nd`. Ctrl-R or Up puts it in to be edited. The full-screen pages of SD ask this way.

## Continued in

[SD BASIC - The SCREEN Statement:
Forms](12b-sd-basic-the-screen-statement-forms.html) — forms and adding
widgets.

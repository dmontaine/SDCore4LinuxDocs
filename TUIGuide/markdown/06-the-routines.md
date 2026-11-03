Title: SD Text User Interface - The Routines
Subtitle: Every routine of the library, its arguments and its operations.

Every routine is called with **exactly** the number of arguments shown; pad what you
do not use with `''`. An argument marked *returned* is set by the routine. An
operation marked *(not used in the examples)* is described as the routine's own
header describes it.

## !tkopen

```
call !tkopen(app, ctx, err, floorw, floorh)
```

| Argument | |
|---|---|
| `app` | The program's name: the right end of row 0, and the messages. |
| `ctx` | *Returned*: the context. Give it to every other routine. |
| `err` | *Returned*: null when the program may go on; otherwise the message to print before it stops. Nothing has been drawn. |
| `floorw`, `floorh` | The smallest window the program is laid out for. Null for 140 by 43; never less than 100 by 30. |

It refuses a window smaller than the floor and one larger than 500 by 300, turns the
break key off - **Ctrl-C** comes to the program as the key `ctrl-c` - and takes the
screen.

## !tkclose

```
call !tkclose(ctx)
```

Gives the screen and the break key back. Call it on every way out.

## !tkkeys

```
call !tkkeys(op, keys, a, b, c, d, e)
```

`keys` is the key table, one row (field) to a key; start it as `''`. **The table
runs nothing**: no operation performs an action, opens a file or writes to the
screen.

| `op` | Arguments | |
|---|---|---|
| `add` | `a` key, `b` label, `c` action, `d` panes, `e` | Adds a row. `a` is a key name as `screen key` gives it (`f1`, `ctrl-q`, `tab`, `esc`); null makes an action reached only from a menu. `d` is the panes that use the key, as subvalues; null is every pane. `e` 0 takes the row out of use; 1 or null leaves it in. |
| `menu` | `a` action, `b` title, `c` entry | Puts the action in a menu. `&` marks the letter that chooses the title or the entry. |
| `why` | `a` action, `b` reason | Takes the action out of use and keeps the reason, which `keylist` shows. |
| `action` | `a` key, `b` pane, `c` *returned* | The action of the first row in use for that key and pane, or null. |
| `keyof` | `a` action, `b` pane, `c` *returned* | The key of the action in that pane, or null. *(not used in the examples)* |
| `name` | `a` key, `b` *returned* | The key as the row at the foot writes it: `F1`, `^S`, `Tab`. *(not used in the examples)* |
| `keylist` | `a` pane, `b` *returned* | One line for each keyed action the pane uses, the reason after one that is not available. |
| `menus` | `a` order of titles, `b` *returned*, `c` pane | The menus as the bar draws them. The bar calls it; a program does not need to. *(not used in the examples)* |

## !tkframe

```
call !tkframe(ctx, keys, pane, msg)
```

Draws the status line (`[pane]` and `msg`), the border, the row of keys made from
`keys`, and the program's name and `name@account` at the right end of row 0. Each
part is written only when it has changed, so call it on every pass of the loop. When
`ctx<TK.C.FOCI>` names the panes that take the focus, it marks the box of the pane
with the focus `[*]` and the others `[-]`.

## !tkmenubar

```
call !tkmenubar(op, ctx, keys, pane, a, b, c)
```

The bar is made from the key table, and **it runs nothing**: a choice comes back to
the program.

| `op` | Arguments | |
|---|---|---|
| `draw` | `a`, `b`, `c` null | Draws row 0 when it has changed. Call it before `!tkframe`. A table with no menu entries has no bar. |
| `key` | `a` key, `b` busy, `c` *returned* | Takes **F10**, **Alt** and a letter, **F2**, **Shift-F10**, and **Esc** when `b` is 0. Any other key is not the bar's. |
| `click` | `a` mouse event, `b` null, `c` *returned* | Takes a left click on row 0 and a right click anywhere. `a` is what `screen mouse` returned. |
| `open` | `a` menu number, `b` null, `c` *returned* | Opens that menu, for a program with a key of its own for it. *(not used in the examples)* |
| `palette` | `a`, `b` null, `c` *returned* | Opens the finder. *(not used in the examples; `key` opens it for F2)* |
| `context` | `a` mouse event or null, `b` null, `c` *returned* | Opens the context menu at the pointer, or in the middle. *(not used in the examples; `key` and `click` open it)* |

`c` is null when the bar did not take the key or click. Otherwise `c<1>` is `none`
(nothing was chosen) or `act`; `c<2>` is the action; `c<3>` the key it is bound to
in this pane; and `c<4>` the name to act on: the key, `act:` and the action when it
has no key, or null when nothing was chosen.

## !tklayout

```
call !tklayout(op, ctx, arg, ret)
```

| `op` | `arg` | `ret` |
|---|---|---|
| `declare` | the pane declaration ([The Tables](06a-the-tables.html)) | *returned*: null, or why it was refused (the context then holds no panes). Declaring again replaces the declaration. |
| `pane` | a pane's id | *returned*: x, y, width, height and shown, as five values; shown is 0 for a pane collapsed in a small layout. Null for no such pane. |
| `body` | null | *returned*: `XBODY`, `YBODY`, `BODYW`, `BODYH`, as four values. *(not used in the examples)* |
| `refresh` | null | *returned*: 1 when the layout changed. Call it after the key `resize`. |

## !tkconfirm

```
call !tkconfirm(sentence, lines, typed, res, msg, boxtitle, btns)
```

| Argument | |
|---|---|
| `sentence` | What is about to be done, exactly as the program will do it. Wrapped at spaces, never altered. |
| `lines` | The explanation, one line to a field; may be null. |
| `typed` | Null, or a name the person must type after choosing the first button. |
| `res` | *Returned*: `run` when the first button was chosen (and the name typed exactly); `cancel`; `wrong` when the name typed was another. |
| `msg` | *Returned*: null for `run`, otherwise a line for the status line. |
| `boxtitle` | The title; null is `Run this command?`. |
| `btns` | Two or three button labels, comma-separated, with `&` letters; null is `&Run,&Cancel`. **The last is Cancel and is the default.** The middle one of three returns `alt`. *(three buttons not used in the examples)* |

It runs nothing and changes nothing.

## !tkform

```
call !tkform(op, ctx, a, b, c)
```

| `op` | Arguments | |
|---|---|---|
| `open` | `a` spec, `b` starting texts, `c` *returned* | Draws the form and returns at once. `c` is `no` when nothing was drawn. |
| `run` | `a`, `b`, `c` *returned* | `a` is `ok` or `cancel`, `b` the texts one to a field, `c` the id of the entry with the focus. |
| `say` | `a` text, `b` entry id, `c` null | Writes a refusal or a note under the entries; the focus goes to the entry. |
| `close` | `a`, `b`, `c` null | Puts back what was under the form. |

The spec: `<1>` title, `<2>` the default button's label, `<3>` the hint line (null:
the library's), then one field per entry: id, label, width, longest text, and 1 for a
masked entry. One form at a time. **It validates nothing.**

## !tkpickrec

```
call !tkpickrec(ctx, mode, file, id, res, newtext)
```

| `mode` | `file` | `id` | `res` |
|---|---|---|---|
| null | *returned*: the file chosen | *returned*: the record | `ok`, `new` or `cancel` |
| `file` | *returned*: the file chosen | null | `ok` or `cancel` *(not used in the examples)* |
| `record` | the file, given | *returned*: the record | `ok`, `new` or `cancel` |
| `list` | the entries, one to a field | in: the window's title; *returned*: the number of the entry | `ok` or `cancel` |

`new` is **Ctrl-N** in the list of records: `newtext` is what had been typed into the
filter. `cancel` is Esc, or a file that could not be opened. In `list` mode, each
entry's value 1 is its name and value 2 its description, `newtext` on the way in is
the entry to start on, and `mode<2>` and `mode<3>` may give column headings and
widths, as values. **The picker never writes**: it opens a file for reading, takes no
lock, and opens only what the account's own `open` may.

## !tkout

```
call !tkout(op, ctx, a, b, c)
```

| `op` | Arguments | |
|---|---|---|
| `add` | `a` kind, `b` text | Keeps a line: `ok`, `refuse`, `out` or `info`. |
| `toggle` | `c` *returned* | Opens or closes the pane; `c` is 1 when it is open now. |
| `draw` | `a` pane id (null: `output`), `c` *returned* | Draws the history, newest first, in that pane of the layout when the pane is open. |
| `key` | `a` key, `c` *returned* | Up, Down, Page Up, Page Down, Home and End scroll the pane: `handled`. Every other key, Esc too, is `unhandled`. *(the examples pass the keys; a history long enough to scroll was not shown)* |
| `open`, `close`, `state`, `mouse`, `focus`, `progress`, `poll`, `clear` | | *(not used in the examples)* |

The history is in memory and starts empty at each `!tkopen`.

## !tkwrap

```
call !tkwrap(text, width, out)
```

`out` is the text cut into pieces, one to a field, each ending at the last space that
keeps it within `width`; a width under 20 is taken as 20.

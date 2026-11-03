Title: SD Text User Interface
Subtitle: Programmer's Guide

SD's own full-screen pages - the home screen, `tool.files`, `tool.query` and the
rest - are built from one library. Its public part lets a program of your own, in
any account, draw a page that looks like those pages and answers the same keys: the
menu bar on the top row, **F2** to find an action, the context menu, the status line,
the border and the row of keys at the foot, the box that asks before something is
done, the form, the pick lists and the output pane.

The public part is eleven catalogued subroutines whose names begin `!tk`, and one
header, `tkpub.h`, that names their constants:

```
$include tkpub.h
```

The library draws the frame of the page and its pop-ups. The **body** of the page -
your boxes, lists, text and forms - your program draws itself with the `screen`
statement. [The Screen Statement on a Page](01a-the-screen-statement-on-a-page.html)
says which part of the statement a page uses and how it works with the routines;
the page "The Screen Statement" in the User set describes every verb. The person using
your page sees what the page "Using the Full-Screen Pages" in the User set
describes; this guide is the programming half of that page and uses its words.

## What the library does not do

* **It adds no right.** It runs with the rights and the access gates of the account
  that runs your program. A gate that is off for the account stays off.
* **It runs nothing and writes nothing.** No routine runs a command, writes or
  deletes a record, or opens a file for writing. A menu entry, a key, the **Run**
  button of a confirm box and a record chosen in a picker each come back to your
  program as an answer; your program does the work, in its own code, with its own
  checks.
* **The record picker opens only what the account may open.** It opens a file the
  way the account's own `open` does. In the examples, a VOC pointer the account's
  own `open` refused (status 3035) was refused by the picker too: it answered
  *cancel* and listed nothing.
* **The page is always the user's page.** The right end of the top row names the
  program and the person, as `name@account`. There is no way to open an
  administrator page through this library.
* **There is no AI line.** The `AI>` row of SD's own pages is not part of the
  library, and nothing your program does draws it.
* **The form validates nothing.** It hands back what was typed; your program checks
  it.

## The routines

Each routine is called with `call`, and **always with the number of arguments
shown**. Pad an argument you do not use with `''`.

| Call | What it does |
|---|---|
| `call !tkopen(app, ctx, err, floorw, floorh)` | Takes the screen. `ctx` comes back as the context every other routine is given; `err` is null, or the message to print before you stop. |
| `call !tkclose(ctx)` | Gives the screen back. Call it on **every** way out. |
| `call !tkkeys(op, keys, a, b, c, d, e)` | Builds and reads the **key table**: the keys, their labels, the menus. |
| `call !tkframe(ctx, keys, pane, msg)` | Draws the status line, the border, the row of keys and the right end of the top row. |
| `call !tkmenubar(op, ctx, keys, pane, a, b, c)` | The menu bar, the finder (**F2**) and the context menu (**Shift-F10**, a right click). |
| `call !tklayout(op, ctx, arg, ret)` | The body and its panes: declare them, read a pane's place, lay out again after a resize. |
| `call !tkconfirm(sentence, lines, typed, res, msg, boxtitle, btns)` | The box that shows what is about to be done and asks; **Cancel is the default**. |
| `call !tkform(op, ctx, a, b, c)` | A form of labelled entries: open, run, say, close. |
| `call !tkpickrec(ctx, mode, file, id, res, newtext)` | Pick a file and a record, a record of a file, or one entry of a list you give. |
| `call !tkout(op, ctx, a, b, c)` | The output pane: what your program did and what was refused. |
| `call !tkwrap(text, width, out)` | Cuts a sentence into pieces that fit a width. |

[The Routines](06-the-routines.html) gives every argument and every operation.

## The shape of a program

Every example in this guide has the same shape:

1. `call !tkopen(...)`. If `err` is not null, print it and stop: nothing has been
   drawn.
2. Build the key table with `!tkkeys` - `add` a row for each key, then `menu` to
   put actions in the menu bar.
3. Declare the panes of the body with `!tklayout('declare', ...)` and draw the body.
4. Loop: `!tkmenubar('draw', ...)`, then `!tkframe(...)`, then
   `screen key returning nm`; give the key to `!tkmenubar('key', ...)`; act on it
   in a `begin case`. A page whose body is a form waits with `screen wait` instead
   ([A Form in the Body](05b-a-form-in-the-body.html)).
5. Leave the loop on **Ctrl-Q**, on the key `guardquit` and at the end of input,
   and call `!tkclose(ctx)` after it.

The key `resize` comes from `screen key` when the window changes size. The program
then calls `!tklayout('refresh', ...)`, raises `ctx<TK.C.GEN>` by one and draws
its body again; raising that slot makes `!tkframe` and the menu bar write all of
the frame again on their next call.

## Rules every program must keep

**Every call has all of its arguments.** A call with fewer stops the program. This
was run with three arguments to `!tkopen`:

```
000000BD: Argument count mismatch calling !tkopen (Call=3, subr=5) at line 3 of <account>/bp.out/zzargs
```

(`<account>` stands for the account's directory, which the message names in full.)

The same mistake inside a page is worse: a call of `!tkform('say', ...)` with four
arguments instead of five, made while a form was open, stopped the program with the
form still on the screen, and the message and the command prompt were written over
the page.
Count the arguments of every call against [The Routines](06-the-routines.html).

**BASIC does not short-circuit `and` or `or`.** Both sides are always worked out.
This program stopped at its second line:

```
   crt 'SHORT begin'
   if 1 or q = 1 then crt 'SHORT the if was true'
   crt 'SHORT end'
end
```

```
SHORT begin
000000B7: Unassigned variable Q at line 2 of <account>/bp.out/zzshort
```

So `if mr<1> # '' and mr<4> = 'quit'` is safe, but a test that would fail on its
second half when the first is false must be written as two `if` statements.

**Give the screen back on every way out.** `!tkopen` turns the break key off - on
the page, **Ctrl-C** is the key `ctrl-c` - and takes the screen; `!tkclose` gives
both back. The loop of every example leaves on
**Ctrl-Q**, on `guardquit` and at the end of input (`screen key` gives a null key
and `status()` is `ER$EOF`, from `$include err.h`), and calls `!tkclose` after
the loop.

**Handle your keys yourself.** Choosing a menu entry gives your program the key
the entry is bound to, as if it had been pressed. Your program's own `case` for
that key is the one place the action is done, so the key, the menu entry, the
finder and the context menu all do exactly the same thing, under the same checks.

## The window

A page needs a window of at least **140 columns by 43 lines**. In a smaller window
`!tkopen` draws nothing and returns, in `err`:

```
hello needs a window of at least 140 columns by 43 lines; this one is 120 by 40
```

**A floor.** A program laid out to work in less can say so with the last two
arguments of `!tkopen`, its **floor**: the smallest window it is laid out for. Null
is 140 by 43; the smallest floor is **100 by 30** (`TK.LEASTW`, `TK.LEASTH`). Above the
floor the page is laid out at the window's own size, up to **500 by 300**
(`TK.MAXW`, `TK.MAXH`); a bigger window is refused the same way:

```
hello needs a window of at most 500 columns by 300 lines; this one is 501 by 43
```

**When the window becomes smaller than the floor** while the page is up, the page
stops taking keys and shows a warning that names both sizes:

```
The window is 90 by 25 and hello is laid out for 100 by 30 or larger:
part of the screen is outside the window and keys are ignored. Make
the window larger to carry on, or press Ctrl-Q to leave; text not
saved is lost unless a recovery copy is on.
```

**Ctrl-Q** asks `Leave? (changes are NOT saved) y/n`; **y** makes `screen key`
give your program the key `guardquit`, and your program leaves without saving. Making the window big enough again gives the
keys back.

## The rows of the page

The library lays out the page from the bottom: the last three rows are always the
frame. At 140 by 43:

| Row | What is there | Slot of `ctx` |
|---|---|---|
| 0 | The menu bar; at its right end the program's name and `name@account` | `TK.C.YMENU` |
| 1 to 39 | The body, columns 1 to 138 | `TK.C.YBODY`, `TK.C.BODYH`, `TK.C.XBODY`, `TK.C.BODYW` |
| 40 | The status line: the pane with the focus in brackets, then the message | `TK.C.YSTAT` |
| 41 | The border | `TK.C.YBORD` |
| 42 | The row of keys, made from the key table | `TK.C.YKEYS` |

The screens in this guide were captured on a terminal whose locale is not UTF-8, so
the borders are drawn with `+`, `-` and `|`. On a terminal that says UTF-8 the
library opens the screen with line-drawing characters, and `ctx<TK.C.UTF8>` is 1.
Reverse video and colour - the highlighted row, the status line - do not show in a
copy as text.

## The examples

Each example is a complete program. Each was put in the `bp` file of an ordinary
account, compiled with `basic bp name` and run with `run bp name` on a terminal of
140 by 43; the screens shown are what that terminal showed.

| Page | Program | What it adds |
|---|---|---|
| [A Bare Page](02-a-bare-page.html) | `hello` | the frame, one pane, the keys `resize` and `guardquit`, a floor |
| [Menus and the Finder](03-menus-and-the-finder.html) | `menus` | the key table and its menus, F1, F2, Esc, the context menu, the mouse, an action that is not available |
| [A Form and a Confirm Box](04-a-form-and-a-confirm-box.html) | `notes` | a form with the program's own checks, a confirm box, a record the program writes, the output pane and the Esc rule |
| [Panes and Pickers](05-panes-and-pickers.html) | `browse` | two panes and the focus, wrapped text, a pick list, the record picker |
| [A Form in the Body](05b-a-form-in-the-body.html) | `stock` | a `screen form` with a table as a pane, `screen wait` with the menu bar and the finder, `screen ask`, `screen msgbox` and `screen theme` over the page |

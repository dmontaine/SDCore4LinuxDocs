Title: SD Text User Interface - A Bare Page
Subtitle: The first example: the frame, one pane, the keys resize and guardquit, and a page laid out for a smaller window.

`hello` is the smallest page: one pane that fills the body, one key, and a loop that
says which key was pressed. It shows the parts every page has.

## The program

Put it in the `bp` file of your account as `hello`, then `basic bp hello` and
`run bp hello`.

```
* hello - the smallest page: the frame, one box, and Ctrl-Q to leave
$include tkpub.h
$include err.h

   prompt ''
   call !tkopen('hello', ctx, err, '', '')
   if err # '' then
      crt err
      stop
   end

   keys = ''
   call !tkkeys('add', keys, 'ctrl-q', 'quit', 'quit', '', 1)

   d = ''
   d<1, TK.P.ID> = 'main'
   d<1, TK.P.BAND> = 1
   d<1, TK.P.COL> = 1
   d<1, TK.P.H> = 39
   d<1, TK.P.W> = 138
   d<1, TK.P.VKIND> = 'stretch'
   d<1, TK.P.HKIND> = 'stretch'
   d<1, TK.P.MINH> = 10
   d<1, TK.P.MINW> = 40
   perr = ''
   call !tklayout('declare', ctx, d, perr)
   if perr # '' then
      call !tkclose(ctx)
      crt perr
      stop
   end

   gen = 0
   msg = 'Press any key; Ctrl-Q leaves'
   gosub draw.all
   loop
      call !tkframe(ctx, keys, 'Main', msg)
      nm = ''
      screen key returning nm
      begin case
         case nm = ''
            if status() = ER$EOF then exit
         case nm = 'guardquit' or nm = 'ctrl-q'
            exit
         case nm = 'resize'
            call !tklayout('refresh', ctx, '', chg)
            gen += 1
            ctx<TK.C.GEN> = gen
            gosub draw.all
         case 1
            msg = 'You pressed ' : nm
      end case
   repeat
   call !tkclose(ctx)
   stop

draw.all:
   r = ''
   call !tklayout('pane', ctx, 'main', r)
   screen clear at 0,0 size ctx<TK.C.W>,ctx<TK.C.YSTAT>
   screen box at r<1,1>,r<1,2> size r<1,3>,r<1,4> title 'Hello'
   s = 'The page is ' : ctx<TK.C.W> : ' by ' : ctx<TK.C.H> : ' and its body ' : ctx<TK.C.BODYW> : ' by ' : ctx<TK.C.BODYH> : '.'
   screen text s at r<1,1> + 2,r<1,2> + 1 width r<1,3> - 4
   return
end
```

## What it draws

After **x** was pressed, at 140 by 43:

```
 0                                                                                                                              hello  don@zzhd
 1   +- Hello --------------------------------------------------------------------------------------------------------------------------------+
 2   | The page is 140 by 43 and its body 138 by 39.                                                                                          |
 3   |                                                                                                                                        |
    (rows 4 to 38 are the same as row 3)
39   +----------------------------------------------------------------------------------------------------------------------------------------+
40  [Main]  You pressed x
41  --------------------------------------------------------------------------------------------------------------------------------------------
42  ^Q quit
```

The number at the left of each row is the row of the screen; it is not part of
the page. A run of rows that are all alike is written as one line.

* **Row 0** has no menus, because no action of this page is in a menu. Its right
  end is the program's name, as given to `!tkopen`, and `name@account` of the
  person running it.
* **Row 40**, the status line, starts with the pane name given to `!tkframe` in
  brackets, then the message.
* **Row 42** is made from the key table: each key that has a label, written the
  way the row writes it (`^Q` for `ctrl-q`), then its label.
* **Ctrl-Q** left the page, and the command prompt came back on a cleared screen.

## How it works

**The key table** has one row: the key `ctrl-q`, the label `quit` and the action
`quit`. A row for a key is what puts the key on the row at the foot.

**The pane declaration** is one field per pane, its values the attributes named
`TK.P.*` in `tkpub.h`. Sizes are written for the reference layout, 140 by 43, whose
body is 138 by 39. This pane fills the body, stretches both ways in a bigger window
(`stretch`), and may shrink to 10 rows by 40 columns in a smaller one
(`TK.P.MINH`, `TK.P.MINW`). `!tklayout('pane', ctx, 'main', r)` gives its place:
`r<1,1>` to `r<1,4>` are x, y, width and height, and `r<1,5>` is 0 when the pane
was collapsed in a small layout.

**`draw.all` clears rows 0 to the status line, not only the body.** This page has
no menu bar, and the menu bar is what writes row 0 whole. Without the clear, the
right end of row 0 written at the old width stayed on the screen after the window
was made wider, and the top row then read `hello  don@zzhd` twice. A page with a
menu bar does not need it.

**`resize`** is the key `screen key` gives when the window changes size.
`!tklayout('refresh', ...)` lays the page out again; raising `ctx<TK.C.GEN>` tells
`!tkframe` that the screen under the frame was cleared, so it writes the whole
frame again.

## A page that works in a smaller window

With one change - the floor given to `!tkopen` - the same program runs in a window
as small as 100 by 30:

```
   call !tkopen('hello', ctx, err, 100, 30)
```

In a window of 120 by 34 the page was laid out at that size, and the pane shrank
with the body:

```
 0                                                                                                          hello  don@zzhd
 1   +- Hello ------------------------------------------------------------------------------------------------------------+
 2   | The page is 120 by 34 and its body 118 by 30.                                                                      |
 3   |                                                                                                                    |
    (rows 4 to 29 are the same as row 3)
30   +--------------------------------------------------------------------------------------------------------------------+
31  [Main]  Press any key; Ctrl-Q leaves
32  ------------------------------------------------------------------------------------------------------------------------
33  ^Q quit
```

The window was then made 140 by 43: the program received `resize`, and the page
was drawn again as in the first screen, with the body 138 by 39. Made 90 by 25, it
was smaller than the floor: the warning shown in
[The Window](01-sd-text-user-interface.html#the-window) took the screen, **Ctrl-Q**
and **y** gave the program `guardquit`, and it left.

In a second run the window was made 90 by 25 and then 140 by 43 again without
Ctrl-Q: the page had its keys back, and **x** gave `You pressed x`.

**The least size.** A pane can be made smaller than its declared size only down to
its least size (`TK.P.MINH`, `TK.P.MINW`); left null, the least size is the declared
size, and whatever then passes the edge of the body is cut off at that edge. With
the two least-size lines taken out, this program drew the same screen at 120 by 34:
its one pane fills the body, so cutting it at the edge and shrinking it come to the
same. A page of several panes gives each the least size its floor can hold, so that
none is cut off.

**A bigger window.** At 180 by 55 the first line of the box read
`The page is 180 by 55 and its body 178 by 51.`: the pane stretched with the body.

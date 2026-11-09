Title: SD Text User Interface - A Form in the Body
Subtitle: The fifth example: a screen form with a table as one pane, a box of text beside it, and the dialogs of the screen statement over the page.

`stock` keeps a short list of items in memory. Its body is two panes: a **form**
holding a table, made with `screen form` and `screen table` and run with
`screen wait`, and a box beside it drawn with `screen box` and `screen text`. The
menu bar, the finder, the status line and the row of keys are the library's, as on
every page. It asks for a name with `screen ask`, shows a total with
`screen msgbox` and changes the theme with `screen theme`. It writes no record.

[The Screen Statement on a Page](01a-the-screen-statement-on-a-page.html) says
which part of the statement a page uses; this page shows the parts together.

## The program

Put it in the `bp` file of your account as `stock`, then `basic bp stock` and
`run bp stock`.

```
* stock - a form with a table in the body, a box of text beside it, and the
*         dialogues of the screen statement over the page
$include tkpub.h
$include err.h

   prompt ''
   call !tkopen('stock', ctx, err, '', '')
   if err # '' then
      crt err
      stop
   end

   keys = ''
   call !tkkeys('add', keys, 'ctrl-q', 'quit', 'quit', '', 1)
   call !tkkeys('add', keys, 'ctrl-n', 'add', 'add', '', 1)
   call !tkkeys('add', keys, 'f6', 'total', 'total', '', 1)
   call !tkkeys('add', keys, 'ctrl-t', 'theme', 'theme', '', 1)
   call !tkkeys('menu', keys, 'add', '&Item', '&Add an item', '', '')
   call !tkkeys('menu', keys, 'total', '&Item', '&Total', '', '')
   call !tkkeys('menu', keys, 'quit', '&Item', '&Quit', '', '')
   call !tkkeys('menu', keys, 'theme', '&View', '&Theme', '', '')

   d = ''
   d<1, TK.P.ID> = 'list'
   d<1, TK.P.BAND> = 1
   d<1, TK.P.COL> = 1
   d<1, TK.P.H> = 39
   d<1, TK.P.W> = 90
   d<1, TK.P.VKIND> = 'stretch'
   d<1, TK.P.HKIND> = 'stretch'
   d<2, TK.P.ID> = 'info'
   d<2, TK.P.BAND> = 1
   d<2, TK.P.COL> = 2
   d<2, TK.P.H> = 39
   d<2, TK.P.W> = 47
   d<2, TK.P.GAP> = 1
   d<2, TK.P.VKIND> = 'stretch'
   perr = ''
   call !tklayout('declare', ctx, d, perr)
   if perr # '' then
      call !tkclose(ctx)
      crt perr
      stop
   end

   rows = 'Bolts':@vm:120:@vm:'Shelf A'
   rows<2> = 'Nuts':@vm:300:@vm:'Shelf A'
   rows<3> = 'Washers':@vm:75:@vm:'Shelf B'
   cur = 1
   th = ''
   screen theme '' returning th
   pane = 'Stock'
   gen = 0
   msg = 'Up and Down choose an item; F10 or Esc opens the menus'
   gosub draw.all
   loop
      call !tkmenubar('draw', ctx, keys, pane, '', '', mr)
      call !tkframe(ctx, keys, pane, msg)
      ev = ''
      screen wait f returning ev else null
      nm = ''
      begin case
         case ev<1> = 'end'
            exit
         case ev<1> = 'cancel'
            nm = 'esc'
         case ev<1> = 'key'
            nm = ev<3>
         case ev<1> = 'resize'
            nm = 'resize'
         case ev<1> = 'change'
            if ev<2> = 'tbl' then
               cur = ev<3>
               gosub draw.info
            end
            continue
         case 1
            continue
      end case

      mr = ''
      if nm = 'mouse' then
         mev = ''
         screen mouse returning mev else mev = ''
         call !tkmenubar('click', ctx, keys, pane, mev, '', mr)
         if mr<1> = '' then continue
      end else
         call !tkmenubar('key', ctx, keys, pane, nm, 0, mr)
      end
      if mr<1> # '' then
         if mr<4> = '' then continue
         nm = mr<4>
      end
      if nm = 'guardquit' then exit
      if nm = 'resize' then
         call !tklayout('refresh', ctx, '', chg)
         gen += 1
         ctx<TK.C.GEN> = gen
         screen hide f
         screen clear at 0,ctx<TK.C.YBODY> size ctx<TK.C.W>,ctx<TK.C.BODYH>
         gosub draw.all
         continue
      end

      act = ''
      call !tkkeys('action', keys, nm, pane, act, '', '')
      begin case
         case act = 'quit'
            exit
         case act = 'add'
            name = ''
            screen ask 'Name of the item:' width 30 title 'Add an item' returning name else name = ''
            name = trim(name)
            if name = '' then
               msg = 'Nothing was added'
            end else
               rows<-1> = name : @vm : 0 : @vm : 'not yet shelved'
               cur = dcount(rows, @fm)
               screen set f, 'tbl' items rows
               screen set f, 'tbl' value cur
               gosub draw.info
               msg = 'Added ' : name
            end
         case act = 'total'
            t = 0
            for i = 1 to dcount(rows, @fm)
               t += rows<i, 2>
            next i
            screen msgbox 'There are ' : t : ' pieces in ' : dcount(rows, @fm) : ' items.' title 'Total'
            msg = 'The total was shown'
         case act = 'theme'
            if th = 'blue' then want = 'mono' else want = 'blue'
            screen theme want returning th then
               msg = 'The theme is ' : th
            end else
               msg = 'This terminal shows no colour; the theme is ' : th
            end
         case 1
            msg = nm : ' does nothing on this page'
      end case
   repeat
   call !tkclose(ctx)
   stop

draw.all:
   r = ''
   call !tklayout('pane', ctx, 'list', r)
   screen form title 'Stock' at r<1,1>,r<1,2> size r<1,3>,r<1,4> returning f
   f{'bgclick'} = 1
   cols = 'Item':@sm:'30L':@vm:'Qty':@sm:'6R':@vm:'Where':@sm:'20L'
   screen table f, 'tbl', cols, rows at 1,1 size r<1,3> - 2,r<1,4> - 2 value cur
   gosub draw.info
   return

draw.info:
   r = ''
   call !tklayout('pane', ctx, 'info', r)
   x = r<1,1>
   y = r<1,2>
   w = r<1,3>
   screen box at x,y size w,r<1,4> title 'Item' fill
   screen text 'Item:  ' : rows<cur, 1> at x + 2,y + 2 width w - 4
   screen text 'Qty:   ' : rows<cur, 2> at x + 2,y + 3 width w - 4
   screen text 'Where: ' : rows<cur, 3> at x + 2,y + 4 width w - 4
   return
end
```

## What it draws

After **Down** twice, at 140 by 43:

```
 0   Item  View                                                                                                                 stock  don@zzhd
 1   +- Stock --------------------------------------------------------------------------------+ +- Item --------------------------------------+
 2   | Item                              Qty Where                                            | |                                             |
 3   | Bolts                             120 Shelf A                                         ^| | Item:  Washers                              |
 4   | Nuts                              300 Shelf A                                         || | Qty:   75                                   |
 5   | Washers                            75 Shelf B                                         || | Where: Shelf B                              |
 6   |                                                                                       || |                                             |
    (rows 7 to 37 are the same as row 6)
38   |                                                                                       v| |                                             |
39   +----------------------------------------------------------------------------------------+ +---------------------------------------------+
40  [Stock]  Up and Down choose an item; F10 or Esc opens the menus
41  --------------------------------------------------------------------------------------------------------------------------------------------
42  ^Q quit  ^N add  F6 total  ^T theme
```

* **The left pane is the form.** Its border and title are the form's own, at the
  place `!tklayout` gave the pane `list`. Inside it the table: the heading row, the
  rows, and its scroll bar in the last column (`^`, `|`, `v`). The current row,
  `Washers`, is drawn in the style `highlight`, which a copy as text cannot show.
* **The right pane is drawn with `screen box` and `screen text`.** When **Down** moved
  the table's current row, `screen wait` gave a `change` event and the program drew
  the pane again: it shows the item the table is on.
* **Row 0, row 40 and row 42** are the library's, made from the key table as on
  every page.

## How it works

**The form is a pane.** `draw.all` asks `!tklayout` where the pane `list` is and
makes the form exactly there, at `r<1,1>,r<1,2>` and of size `r<1,3>,r<1,4>`. The table
stands at `1,1` inside the form's border and is two columns narrower and two rows
shorter than the form, so it fills it. The pane `info` is drawn from its own place
in the same way.

**`screen wait` is the page's wait.** A page whose body has no form waits with
`screen key`. Here the form must answer the keys it uses - Up, Down, the page keys,
**F3** to sort, a letter to jump - so the program waits with `screen wait`, and the
form gives back one event at a time. The program turns each into what the rest of
the loop expects:

| Event | What the program does |
|---|---|
| `change` of `tbl` | The table's current row moved: `ev<3>` is its number in `rows`; draw `info` again. |
| `key` | A key the form has no use for - **F10**, **F2**, **F6**, **Ctrl-N**, **Ctrl-T**, **Ctrl-Q**: `ev<3>` is its name, given to `!tkmenubar('key', ...)` first, then looked up in the key table. |
| `cancel` | **Esc**. The form does not close on it; the program gives the menu bar the key `esc`, which opens the menus. |
| `resize` | The window changed size. |
| `end` | The input ended: leave. |

**A click on the menu bar.** Row 0 is not a widget of the form, and a form takes a
click only on its widgets. `f{'bgclick'} = 1` asks it to give back a press of the left
button on anything that is not a widget as a `key` event whose name is `mouse`; the
program then reads it with `screen mouse` and gives it to `!tkmenubar('click', ...)`,
as `menus` does. A click on **Item** in row 0 opened the Item menu. A press of any
other button is not given back.

**F10 and F2 over the form.** The menus and the finder are drawn over the page, and
the form is put back when they close:

```
 0   Item  View
 1   Add an item    ^N -----------------------------------------------------------------------+ +- Item --------------------------------------+
 2   Total          F6                   Qty Where                                            | |                                             |
 3   Quit           ^Q                   120 Shelf A                                         ^| | Item:  Washers                              |
 4   | Nuts                              300 Shelf A                                         || | Qty:   75                                   |
```

```
17   |                                             +- Find an action ---------------------------+                                             |
18   |                                             | filter:                              4 of 4|                                             |
19   |                                             | Item > Add an item  ^N                     |                                             |
20   |                                             | Item > Total        F6                     |                                             |
21   |                                             | Item > Quit         ^Q                     |                                             |
22   |                                             | View > Theme        ^T                     |                                             |
23   |                                             | ? shows help for the highlighted entry     |                                             |
24   |                                             +--------------------------------------------+                                             |
```

**The dialogs of the screen statement.** **Ctrl-N** asks with `screen ask`, a
dialog of the statement, not of the library:

```
19   |                                                   +- Add an item ------------------+  || |                                             |
20   |                                                   | Name of the item:              |  || |                                             |
21   |                                                   |                                |  || |                                             |
22   |                                                   +--------------------------------+  || |                                             |
```

After `Pins` and **Enter**, the program added a row to `rows`, gave the table the new
rows and the new current row with `screen set` while the form was on the screen, and
drew `info` again:

```
 3   | Bolts                             120 Shelf A                                         ^| | Item:  Pins                                 |
 4   | Nuts                              300 Shelf A                                         || | Qty:   0                                    |
 5   | Washers                            75 Shelf B                                         || | Where: not yet shelved                      |
 6   | Pins                                0 not yet shelved                                 || |                                             |
    ...
40  [Stock]  Added Pins
```

**F6** shows the total with `screen msgbox`:

```
18   |                                                 +- Total ----------------------------+|| |                                             |
19   |                                                 | There are 495 pieces in 4 items.   ||| |                                             |
20   |                                                 |                                    ||| |                                             |
21   |                                                 |               [ OK ]               ||| |                                             |
22   |                                                 |                                    ||| |                                             |
23   |                                                 +------------------------------------+|| |                                             |
```

**Enter** closed it, and the page under it was as it had been, with
`The total was shown` on the status line. Every dialog saves what is under it
from the library's picture of the screen and puts it back, so a page uses them as
they are.

**The theme.** `screen theme '' returning th` only asks which theme is in force.
**Ctrl-T** chose `blue`; the page was drawn again in it and the status line said
`The theme is blue`. On a terminal that cannot show color `screen theme` takes its
`else` and the theme stays as it was. `!tkclose` gives the screen back with
`screen close`, which puts the theme back to `mono`.

**A resize.** `screen wait` gives `resize` once the form has been drawn again, still
at its old place. The program lays the page out again (`!tklayout('refresh', ...)`, raise
`ctx<TK.C.GEN>`), takes the old form away with `screen hide`, clears the body and
makes the form again at the pane's new place, starting on the row it was on. Both
panes stretch down and only `list` stretches across, so at 160 by 50 the form took
the 20 extra columns and both panes the 7 extra rows:

```
 0   Item  View                                                                                                                                     stock  don@zzhd
 1   +- Stock ----------------------------------------------------------------------------------------------------+ +- Item --------------------------------------+
 2   | Item                              Qty Where                                                                | |                                             |
 3   | Bolts                             120 Shelf A                                                             ^| | Item:  Pins                                 |
 4   | Nuts                              300 Shelf A                                                             || | Qty:   0                                    |
 5   | Washers                            75 Shelf B                                                             || | Where: not yet shelved                      |
 6   | Pins                                0 not yet shelved                                                     || |                                             |
 7   |                                                                                                           || |                                             |
    (rows 8 to 44 are the same as row 7)
45   |                                                                                                           v| |                                             |
46   +------------------------------------------------------------------------------------------------------------+ +---------------------------------------------+
47  [Stock]  The theme is blue
48  ----------------------------------------------------------------------------------------------------------------------------------------------------------------
49  ^Q quit  ^N add  F6 total  ^T theme
```

Made 140 by 43 again, the page was as in the first screen, and **Up** chose
`Washers`.

**Leaving.** **Ctrl-Q** comes from the form as a `key` event, is looked up as the
action `quit`, and the loop ends; `!tkclose` gave the screen back and the command
prompt came back on a cleared screen.

## Things to keep

* **One wait.** Wait with `screen wait` on the form or with `screen key`, not both:
  a key read by one is not seen by the other.
* **Draw outside the form with `screen box` and `screen text`, and never over it.**
  The form draws its own rectangle; a pane beside it is the program's.
* **Make the form from the pane's place**, and make it again after a resize, so it
  moves with the layout.
* **Keep the data in the program.** The table shows `rows`; `screen get` and the
  `change` event give the row's number in `rows`. What is typed or chosen is
  checked and acted on by the program, as everywhere in the library.

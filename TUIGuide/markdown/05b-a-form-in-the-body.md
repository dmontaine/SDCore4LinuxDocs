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

It is already in your account, compiled: `run examples.bp stock`. To change it, put it in the
`bp` file of your account as `stock` (`copy from examples.bp to bp stock`), then `basic bp stock`
and `run bp stock`.

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

## Continued in

[SD Text User Interface - How the Form in the Body
Works](05c-how-the-form-in-the-body-works.html) — how the fifth example works,
line by line, and the things to keep

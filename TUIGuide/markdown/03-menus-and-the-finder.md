Title: SD Text User Interface - Menus and the Finder
Subtitle: The second example: the key table and its menus, F1, F2, Esc, the context menu, the mouse, and an action that is not available now.

`menus` has no data. It shows how one key table makes the row of keys, the menu bar,
the finder, the context menu and the help list, and how a program takes the answer
of each with the same code it uses for a key.

## The program

```
* menus - the key table, the menu bar, F1, F2, Esc, the context menu and the mouse
$include tkpub.h
$include err.h

   prompt ''
   call !tkopen('menus', ctx, err, '', '')
   if err # '' then
      crt err
      stop
   end

   keys = ''
   call !tkkeys('add', keys, 'f1', 'help', 'help', '', 1)
   call !tkkeys('add', keys, 'ctrl-q', 'quit', 'quit', '', 1)
   call !tkkeys('add', keys, 'f5', 'count', 'count', '', 1)
   call !tkkeys('add', keys, 'ctrl-s', 'save', 'save', '', 1)
   call !tkkeys('add', keys, 'esc', 'menu', 'menu', '', 1)
   call !tkkeys('add', keys, '', '', 'about', '', 1)
   call !tkkeys('menu', keys, 'quit', '&File', '&Quit', '', '')
   call !tkkeys('menu', keys, 'save', '&File', '&Save', '', '')
   call !tkkeys('menu', keys, 'count', '&View', '&Count', '', '')
   call !tkkeys('menu', keys, 'help', '&Help', '&Keys of this page', '', '')
   call !tkkeys('menu', keys, 'about', '&Help', '&About', '', '')
   save.why = 'there is nothing to save'
   call !tkkeys('why', keys, 'save', save.why, '', '', '')

   d = ''
   d<1> = 'main' : @vm : 1 : @vm : 1 : @vm : 39 : @vm : 138 : @vm : '' : @vm : 'stretch' : @vm : 1 : @vm : 'stretch' : @vm : 1
   perr = ''
   call !tklayout('declare', ctx, d, perr)

   pane = 'Main'
   gen = 0
   counted = 0
   shown = ''
   msg = 'F10 or Esc opens the menus; F2 finds an action'
   gosub draw.all
   loop
      call !tkmenubar('draw', ctx, keys, pane, '', '', mr)
      call !tkframe(ctx, keys, pane, msg)
      nm = ''
      screen key returning nm
      if nm = '' then
         if status() = ER$EOF then exit
         continue
      end
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
         gosub draw.all
         continue
      end

      act = ''
      if nm[1, 4] = 'act:' then
         act = nm[5, 99]
      end else
         call !tkkeys('action', keys, nm, pane, act, '', '')
      end
      begin case
         case act = 'quit'
            exit
         case act = 'help'
            call !tkkeys('keylist', keys, pane, shown, '', '', '')
            msg = 'The keys of this page'
            gosub draw.all
         case act = 'count'
            counted += 1
            msg = 'Counted ' : counted : ' time(s)'
         case act = 'about'
            msg = 'menus: an example page'
         case nm = 'ctrl-s'
            msg = 'Save: ' : save.why
         case 1
            msg = nm : ' does nothing on this page'
      end case
   repeat
   call !tkclose(ctx)
   stop

draw.all:
   r = ''
   call !tklayout('pane', ctx, 'main', r)
   screen clear at 0,ctx<TK.C.YBODY> size ctx<TK.C.W>,ctx<TK.C.BODYH>
   screen box at r<1,1>,r<1,2> size r<1,3>,r<1,4> title 'Menus'
   for i = 1 to dcount(shown, @fm)
      screen text shown<i> at r<1,1> + 2,r<1,2> + i width r<1,3> - 4
   next i
   return
end
```

## The key table makes everything

Each `add` is one row: the key, the label for the row at the foot, the action, the
panes that use it (null: every pane) and 1 to leave it in use. `menu` puts an
action in a menu: the title and the entry text, each with `&` before the letter
that chooses it. The key an entry shows is taken from the table, never typed, so
the menus and the keys cannot disagree. The last `add` has no key: **About** is
reached only from the menu.

`why` takes an action out of use and gives the reason. **Save** stays in its menu,
dimmed, its key leaves the row at the foot, and `!tkkeys('action', ...)` no longer
gives `save` for **Ctrl-S** - so the page's own `case nm = 'ctrl-s'` says why:
`Save: there is nothing to save`.

The page as it opened:

```
 0   File  View  Help                                                                                                           menus  don@zzhd
 1   +- Menus --------------------------------------------------------------------------------------------------------------------------------+
 2   |                                                                                                                                        |
    (rows 3 to 38 are the same as row 2)
39   +----------------------------------------------------------------------------------------------------------------------------------------+
40  [Main]  F10 or Esc opens the menus; F2 finds an action
41  --------------------------------------------------------------------------------------------------------------------------------------------
42  F1 help  ^Q quit  F5 count  Esc menu
```

The menus are in the order of the table, except that **File** is always first and
**Help** last. Inside a menu the entries are in the order of the table, except
that the entry of the action `quit` is always last.

## The menu bar

`!tkmenubar('draw', ...)` draws row 0, and only when something in it changed, so
call it on every pass of the loop, **before** `!tkframe`. `!tkmenubar('key', ...)`
is given every key. It takes the ones that are the bar's:

* **F10** opens the first menu; **Alt** and a menu's marked letter opens that menu.
* **Esc** opens the first menu whose first entry is not **Quit**, so that Esc and
  then Enter never leaves the page. Here File begins with Save, so Esc opened File:

  ```
   0   File  View  Help
   1   Save    ^S ------------------------------------------------------------------------------------------------------------------------------+
   2   Quit    ^Q                                                                                                                               |
  ```

  While a menu is open the right end of row 0 is blank; the next `!tkframe`
  writes it again.
* **F2** opens the finder and **Shift-F10** the context menu (below).

Inside a menu an entry's marked letter chooses it (**a** chose **Help > About**), and
Esc closes the menu. A click on a title opens that menu: `!tkmenubar('click', ...)`
is given the event of `screen mouse`.

**What comes back.** `mr` is null when the bar did not take the key. Otherwise
`mr<1>` is `none` (the person left the menu, nothing was chosen) or `act`; `mr<2>`
is the action; `mr<4>` is **the name your program acts on**: the key the action is
bound to, or `act:` and the action when it has no key, or null when nothing was
chosen. So the loop sets `nm = mr<4>` and goes on as if that key had been pressed;
choosing **View > Count** runs exactly the `case` that **F5** runs.

`!tkkeys('action', keys, nm, pane, act, '', '')` turns a key into its action, or
null when the key is not bound or not available now. Dispatching on the action, as
this program does, keeps every key and entry of one action in one `case`.

## F2: find an action

The finder lists every entry of every menu, `Menu > Entry`, with its key; an entry
that cannot be used now says `(not now)`:

```
17   |                                             +- Find an action ---------------------------+                                             |
18   |                                             | filter:                              5 of 5|                                             |
19   |                                             | File > Save               ^S (not now)     |                                             |
20   |                                             | File > Quit               ^Q               |                                             |
21   |                                             | View > Count              F5               |                                             |
22   |                                             | Help > Keys of this page  F1               |                                             |
23   |                                             | Help > About                               |                                             |
24   |                                             | ? shows help for the highlighted entry     |                                             |
25   |                                             +--------------------------------------------+                                             |
```

Typing narrows the list: `cou` left `View > Count` alone, and Enter gave the program
the key **F5**; the status line said `Counted 1 time(s)`. Choosing **File > Save**
gave nothing to the program: a box said only

```
19   |                                                | That action is not available now.   |                                                 |
```

and not the reason given to `why`. The reason is in the list of keys (F1, below).

## The context menu

**Shift-F10**, or a right click, opens the actions of the pane that has the focus:
the entries of every menu but File and Help whose action that pane uses, a line, and
**Find an action...**, which opens the finder. Here that is **View > Count**:

```
20   |                                                        Count                F5                                                         |
21   |                                                       -------------------------                                                        |
22   |                                                        Find an action...    F2                                                         |
```

A right click opened the same menu where the pointer was. A page with two panes
names them in `ctx<TK.C.FOCI>` ([Panes and Pickers](05-panes-and-pickers.html)).

## F1: the keys of the page

`!tkkeys('keylist', keys, pane, shown, '', '', '')` gives one line for each keyed
action the pane uses, with the reason after one that is not available. The program
draws the lines in its box:

```
 2   | F1  Keys of this page                                                                                                                  |
 3   | ^Q  Quit                                                                                                                               |
 4   | F5  Count                                                                                                                              |
 5   | ^S  Save  (not available: there is nothing to save)                                                                                    |
 6   | Esc  menu                                                                                                                              |
```

## The Esc row

The row `add ... 'esc', 'menu', 'menu'` puts `Esc menu` on the row at the foot. Its
action is `menu`, and the bar still takes Esc for it. A page that holds something
Esc should close first tells the bar so ([The Esc rule](04-a-form-and-a-confirm-box.html#the-esc-rule)).

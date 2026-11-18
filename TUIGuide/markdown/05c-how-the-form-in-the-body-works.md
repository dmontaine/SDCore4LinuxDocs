Title: SD Text User Interface - How the Form in the Body Works
Subtitle: The fifth example, line by line: how the form, the table, the box and the dialogs are made and how a keystroke reaches them.

This page continues [SD Text User Interface - A Form in the
Body](05b-a-form-in-the-body.html).

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

Title: SD Text User Interface - The Tables
Subtitle: The context, the key table and the pane declaration: the slots and attributes named in tkpub.h.

Each table is one dynamic array, and `tkpub.h` names its positions. Use the names,
not the numbers.

## The context: ctx

`!tkopen` makes it; every other routine is given it. A program reads these slots and
writes one, `TK.C.GEN`; the others are the library's.

| Name | | |
|---|---|---|
| `TK.C.W`, `TK.C.H` | 1, 2 | The size the page is laid out at: the window's, or the floor's while the window is smaller. |
| `TK.C.UTF8` | 3 | 1 when the screen was opened with line-drawing characters. |
| `TK.C.APP` | 5 | The program's name, as given to `!tkopen`. |
| `TK.C.AUD` | 6 | `name@account`. |
| `TK.C.YSTAT`, `TK.C.YBORD`, `TK.C.YKEYS` | 7, 8, 9 | The rows of the status line, the border and the row of keys: H - 3, H - 2, H - 1. |
| `TK.C.GEN` | 10 | **Raise it by one** after the program cleared or drew the screen again under the frame; the frame and the bar are then written whole. |
| `TK.C.FLOORW`, `TK.C.FLOORH` | 12, 13 | The floor. |
| `TK.C.XBODY`, `TK.C.YBODY`, `TK.C.BODYW`, `TK.C.BODYH` | 16 to 19 | The body: from column 1 and row 1, W - 2 columns, YSTAT - 1 rows. |
| `TK.C.YMENU` | 22 | The row of the menu bar, 0. |
| `TK.C.FOCI` | 29 | Set by the program: the panes that take the focus, a value each, the pane's id and, as the second subvalue, the name the program gives `!tkframe` for it. Null: no focus marks. |

Slots 11 and 28 belong to the AI line of SD's own pages; `!tkframe`, `!tkmenubar`
and `!tklayout` clear them on every call.

## The key table

One row (field) per key; its values:

| Name | | |
|---|---|---|
| `TK.K.KEY` | 1 | The key, as `screen key` names it. |
| `TK.K.LABEL` | 2 | What the row at the foot says it does. |
| `TK.K.ACT` | 3 | The action. |
| `TK.K.PANES` | 4 | The panes that use the key, as subvalues; null is every pane. |
| `TK.K.ON` | 5 | 0: out of use. |
| `TK.K.MENU`, `TK.K.ENTRY` | 6, 7 | The menu and the entry, set by `menu`. |
| `TK.K.WHY` | 8 | Why the action is not available now, set by `why`. |
| `TK.K.ROW` | 9 | 0: bound, but not shown on the row at the foot; no operation sets it. *(not used in the examples)* |

Build it with `!tkkeys('add', ...)`, `menu` and `why` rather than by hand.

## The pane declaration

One field per pane, given to `!tklayout('declare', ...)`; its values:

| Name | | |
|---|---|---|
| `TK.P.ID` | 1 | The pane's id: a plain word, unique in the declaration. |
| `TK.P.BAND` | 2 | Its band, from 1 at the top. |
| `TK.P.COL` | 3 | Its column in the band, from 1 at the left (null: 1). |
| `TK.P.H`, `TK.P.W` | 4, 5 | Its height and width at 140 by 43, borders included. |
| `TK.P.GAP` | 6 | Columns left empty before its column (null: 0). |
| `TK.P.VKIND`, `TK.P.VWT` | 7, 8 | `stretch` to take rows the window has beyond 43, and its weight (null: fixed, weight 1). |
| `TK.P.HKIND`, `TK.P.HWT` | 9, 10 | The same for columns beyond 140. |
| `TK.P.MINH`, `TK.P.MINW` | 11, 12 | The least size it may be given in a smaller layout (null: its declared size). |
| `TK.P.PRIO` | 13 | Collapse priority in a small layout: null or 0 never; otherwise the highest number collapses first. *(not used in the examples)* |

**Every size is written for 140 by 43**, whose body is 138 by 39 at column 1, row 1:
at that size every pane has exactly its declared size. The body is split into bands
stacked from the top; a band into columns side by side; a column into the panes of
that band and column, stacked in the order declared. A band is as tall as its tallest
column, and a column as wide as its widest pane. In `browse`, two panes of band 1 -
`list` 40 wide and `text` 97 wide with a gap of 1 - fill the 138 columns.

In a bigger window the extra rows and columns go to the panes that stretch, shared by
weight. In a smaller one (a page with a floor), rows and columns are taken from the
panes that stretch, then from the fixed ones, down to their least size; then a pane
with a collapse priority is collapsed; what still does not fit is cut at the body's
edge.

Title: SD TCL - The Home Screen: my.menu and the AI Line
Subtitle: Your own programs, the Recent group, sub-menus and the AI line.

This page continues [SD TCL - The Home
Screen](29a-sd-tcl-the-home-screen.html).

## Your own programs: `my.menu`

```
my.menu
```

**Only if the administrator has allowed it for your account** (`pins-on`; it is off as
delivered). Your home screen then has a group **My programs**, with a tile **Add a
program** that opens `my.menu`, and a tile for each program you have added. A program
is a **label** (up to 21 characters), a **command** (what you would type at your
prompt), an optional three-character **glyph**, and whether the screen should **wait
for Enter** when the command has finished printing.

| key | does |
|---|---|
| Ctrl-N | add a program (it asks for the label, the command, the glyph and the wait) |
| Enter | change the selected one |
| Del | remove it (asks first; Cancel is the default) |
| U, D | move it up or down the list |
| / | go to the next program whose label or command holds a text you type (any case; round to the top) |
| Esc, F10 | open the menu bar (its menus Program, File and Help): the same actions by name; with no program in the list, Change, Remove and the moves are shown dimmed |
| F1, `?`, a click on the `[?]` | help on this page; the Help menu has the same |
| Ctrl-Q | leave; the home screen is built again and shows the list |

In a window bigger than 140 by 43 the list takes the extra rows and the command column
the extra width.

**It manages only your own list.** The standard tiles are the administrator's and
are not touched. A program of yours runs the command exactly as you would type it,
so it adds no access: the gates apply as at the prompt. The list is the record
`home` of the file `&menus&` in your own account. If the administrator takes the
permission away (`pins-off`) the group disappears from your screen and `my.menu`
says it is not allowed; the list stays in your file.

## The Recent group

```
View > Recent group
```

A group of **the tiles you started last**, newest first, at the top of the page: six at
most. **It is off as delivered.** Turn it on in the **View** menu (*Recent group on or off*,
or Ctrl-R; the same entry turns it off, and the status line says which it is now). The first time it is on, SD makes the
file `&menus&` in your own account if it is not there, as `my.menu` does, and keeps the
list in its record `recent`; the list is one word `on`, then one id for each tile.

* **What is kept is an id, never a command.** The group is built from the page as it is
  now: a tile that the administrator has turned off, or that is not on your page, is not
  shown, and a record that someone edited by hand cannot make the page offer a tile it does
  not have. Starting a tile of the group runs the command of that tile, exactly as the tile
  in its own group would, and puts it first.
* **The tiles you added yourself (`my.menu`) are not kept here**: they are your own list
  already.
* **Turning it off forgets the list** (the record is deleted), and **while it is off nothing
  is written**: starting a tile leaves your file as it was.
* **The administrator can turn it off for your account** (`set.tile account recent off`, or
  the *Menu management* page): the group is then not on your page, nothing is read or written
  for it, and the View entry cannot be chosen. What you had kept stays in your file.
* If the file `&menus&` cannot be made or written, turning the group on says so (*The
  Recent group could not be turned on*) and leaves nothing behind. `my.menu` makes the file
  the same way and meets the same limit.

## Pages inside pages: sub-menus

A tile can open a **second page of tiles**. The new page has a **Back** tile at the left of
the header (your name moves right to make room), and the status line shows where you are:
`[Home > Develop]`. **Esc**, **Backspace**, the Back tile and the *Back* entry of the Go menu (Esc or Backspace)
each go back one page, with the tile you left selected.
Pages can be nested **eight deep**; a page that is already open above cannot be opened again
(*... is already open above this page*), and a menu none of whose tiles is on your page has no
tile to open it. Switch account starts the other account at its top page.

**No tile of the delivered page opens a sub-menu yet.** The tiles you start inside a
sub-menu are kept by the Recent group like any other.

## The AI line

When the AI is on for your account (the administrator has chosen a provider, given it a
key, **and allowed your account**; see [Asking the AI](29b-sd-tcl-asking-the-ai.html))
the home screen has a row that starts **`AI>`**, and under it a horizontal rule that keeps it
apart from the status line. Without the AI there are no such rows and nothing on this page changes.

**Press F6, choose AI > Ask the AI, or click the row**, type
what you want in your own words, and press Enter:

```
AI> open the ide
AI> show me who I am
```

Enter does not send anything. It shows the provider, the model, the size of all that will be
sent, and **your request**. SD's own text that goes with it (one fixed instruction, the list of
what this page can do, what the page says about itself) is sent and counted, but not shown. **Cancel is the default button**,
so Enter alone sends nothing; choose **Send** (press `s`) to send. While the AI answers the row
says so and **Esc gives the request up**.

The answer comes in a popup. It says what the AI said, and it may *propose* one thing:

| The AI proposes | What you see | What happens |
|---|---|---|
| a **tile** that opens a tool (Editor, IDE, Keys, and the administrator's tiles) | `The AI proposes: IDE - programs and files`, with **Accept** and Reject | **Accept** starts the tile exactly as a click on it would. Enter alone accepts, because the tile only opens a tool you could open anyway. |
| the **Terminal** tile, or one of **your own programs** on the page | the same, with **Accept** and Reject | **Accept** starts it as a click would. **Enter alone rejects**: the Terminal tile leaves the screen for the command prompt and a program of yours runs a command you wrote, so neither starts unless you choose Accept. This is decided for the proposal: having a program of your own on the page does not change what Enter does for the other tiles. |
| a **command** | the command on a line of its own, with **Run** and Cancel | **Run** runs it as the Terminal tile's prompt would, and waits for Enter. **Enter alone cancels**: a command never runs unless you choose Run. |
| nothing | only what it said, with Close | nothing |

What it cannot do: it is never offered **Sign out** or **Switch account**; a tile that is not on
your page is ignored, with a note; a command with a control character in it or of more than 200
characters is not shown; anything that is not one JSON object is shown as words, with a note, and
nothing is proposed. The accepted tile or command runs with **your** rights: the gates of your
account apply as they would if you had typed it.

The audit trail records that you asked (`ai request account=... program=tk_ai bytes.out=...`),
never what you asked or what came back.

## Not yet

An AI line in the IDE, with proposals as edits, is built (see [Programs and the
catalog](24e-sd-tcl-the-ide-ai-and-the-window.html)), and so are the AI in [SED](27a-sd-tcl-sed.html),
[CED](27b-sd-tcl-ced.html) and [the debugger](17-sd-basic-debugging.html). The AI line is also on
every page of the toolkit (see [Asking the AI](29b-sd-tcl-asking-the-ai.html)).

Programs the administrator assigns to an account, a menu builder for the holder
(grouping one's own programs into sub-menus) and a live line on the account holder's tiles
are planned and not built; today the page is the table above plus your own programs and, if
you turn it on, the Recent group.

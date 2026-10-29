Title: SD TCL - The Home Screen
Subtitle: A start screen of tiles that every account can open: its tools, a terminal, switch account and sign out.

```
home
menu
exit
```

**`home`** opens a full-screen start screen for the account you are signed in to:
a page of **tiles**, each of which starts something. **`menu`** does the same (it is
the plain word for "bring up the full-screen menu", at the prompt or in the terminal
the screen gave you), and **`exit`** is the way back to it from that terminal.
Your administrator decides, account by account,
whether a session **starts** here or at the command prompt (see *Where a session
starts*, below); you can always type `home` or `menu` at the prompt to open it.

It needs a window of at least **140 columns by 43 lines** (the same as the other
full-screen tools) and a real terminal. In a smaller window it says so, with the
size it found, and leaves you at the prompt; in a session with no terminal (a
pipe, a phantom, a script) it says `home needs a terminal` and reads nothing, so
a script is never taken for someone typing. **In a bigger window the tiles spread over
the whole window** (since 28 October 2026): as many columns of tiles as fit, each tile a little
wider, and the page follows the window when it is resized; at 140 by 43 it looks as it always did.
If the window is made smaller than 140 by 43 while the home screen is up, it holds the keyboard
behind a warning that gives both sizes until the window is big enough again.

## What is on it

```
 File  Go  View  AI  Help                                                       home  alice@sales

   alice @ sales                                                  <> Switch account   -> Sign out
   Thursday 22 Oct 2026  -  18:52

   My tools
     [=]                  </>
     Editor               IDE
     edit a record        programs and files

   Everyone
     >_                                          ^K
     Terminal                                    Keys
     type exit to come back                      test your keyboard
```

| tile | what it does |
|---|---|
| **Editor** | runs `sed` (it asks which file and record) |
| **IDE** | runs `ide` |
| **Terminal** | leaves the screen for the ordinary command prompt (below) |
| **Keys** | runs `tool.keys`, the terminal and keyboard diagnostic |
| **Switch account** | a list of the accounts you may enter; then the home screen of the one you pick |
| **Sign out** | asks `Sign out of SD?` and ends the session |

**A tile starts a command exactly as you would have typed it.** It adds no
access: if the command needs a switch your account does not have, you get the same
refusal you would at the prompt. A command that takes the screen (the editors,
`tool.keys`) gives it back when you leave it, and the home screen is drawn again;
a command that only prints waits for Enter before the screen returns.

The **administrator's page** has the same tools in a group called *Tools*, and
shows `administrator` at the top and at the right end of the menu bar; an account
holder's page says `My tools` and `name @ account`. The two are built from one
table and differ only in what is in it. The tools that other parts of SD add (the
account manager, the gate matrix and the rest) each add their own tile when they
are built.

**The page scrolls.** It is laid out at its full height and only the rows that fit
are drawn, with a scroll bar in the last column when there is more than fits, so
the number of tiles can pass the height of the screen. The header (your name, the
date and time, Switch account and Sign out) stays where it is.

## Keys and the mouse

| key | does |
|---|---|
| the arrow keys | move to the nearest tile in that direction (a tile in the same row or column comes first) |
| Tab, Back-tab | the next and previous tile, in reading order |
| Home, End | the first and the last tile |
| Page Down, Page Up | the first tile of the next and of the previous group |
| a letter | the next tile whose label begins with it |
| Enter, the space bar | start the tile |
| Esc, Backspace | back one page, when you are in a sub-menu (below); on the top page Esc opens the menu bar, as F10 does, and Backspace does nothing |
| F1 | help on the home screen |
| F5 | build the page again |
| F10 | open the menu bar (File, Go, View, AI, Help): **Go** has Terminal, Switch account and Back (Back can be chosen only in a sub-menu); **View** has Refresh and the Recent group; **AI** has *Ask the AI*, which moves the focus to the AI line, when the AI is on, and a dimmed *AI is off* when it is not |
| Ctrl-Q | sign out (asks first; **Cancel** is the button Enter chooses, so a stray Enter signs nobody out) |

A **click** starts a tile; the **wheel** scrolls the page three rows; a click on the
menu bar opens the menu under it. The foot of the screen is the same as the
other full-screen tools: a hint line, the status line, a border and the row of
function keys.

On a terminal with colour the tiles are filled in the colour of their group; on one
without, each tile is a box and the one with the focus is in reverse video, so
nothing depends on colour.

## The terminal, and `exit`

The **Terminal** tile gives the screen back and shows

```
Terminal - type exit to return to the home screen
:
```

That is the ordinary command prompt, with all of its features (the command stack,
paragraphs, select lists, everything you can type at a prompt that did not come
from the home screen). **`exit`** brings the home screen back. At a prompt that
*did not* come from the home screen, `exit` does what `quit` does and ends the
session. The home screen remembers that you left by the Terminal tile for the rest
of the session, so `exit` goes on coming back to it.

## Switch account and sign out

**Switch account** lists the accounts you may enter, by the rule `logto` uses
(an administrator may enter any account; anyone else the accounts whose Linux group
they belong to), never a suspended account and never SDSYS. Pick one and you are
in that account: its LOGIN paragraph has run, and **the home screen of that account
is shown**. Picking the account you are already in says so and changes nothing.
SD runs as one operating-system user, so this moves you between the accounts that
user belongs to; it cannot make you someone else. To be another person, sign out
and connect again.

**Sign out** (the tile, the File menu, or Ctrl-Q) asks first and then ends the
session as `quit` does.

## Where a session starts

The administrator sets this for each account (`modify.account name start-menu`,
`start-terminal` or `start-default`, in the Administrator's guide), and sets what
accounts with no setting of their own do with `set.start.default menu` or
`terminal`. **It is menu as delivered.** The setting is read when you sign on, and
when you type `logto` at the prompt to enter an account. Starting in the menu does
not confine anyone: the Terminal tile is always there.

The screen is never given to a session that cannot use it: a window under 140 by 43
or over 500 by 300, a pipe, a phantom, an API server, or a `logto` that a program ran with `execute`
(the home screen runs its own `logto` itself and shows the new account's page).

## Tiles the administrator turns off

Every tile is on as delivered, and the administrator can turn a tile off **for your
account** (`set.tile`, or the *Menu management* page): it is then not on your page,
and its menu entry cannot be chosen. If the **Terminal** tile is off and your account
starts in the home screen, you are never given the command prompt: when the screen
ends (a window too small, an error, the cursor lock) you are signed out. An account
that starts at the prompt keeps it. Sign out cannot be turned off.

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
| Esc, F10 | open the menu bar (File, Program): the same actions by name; with no program in the list, Change, Remove and the moves are shown dimmed |
| Ctrl-Q | leave; the home screen is built again and shows the list |

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
most. **It is off as delivered.** Turn it on in the **View** menu (*Recent group (off)*; the
same entry turns it off, and says what it is now). The first time it is on, SD makes the
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
`[Home > Develop]`. **Esc**, **Backspace**, the Back tile and the *Back* entry of the Go menu
each go back one page, with the tile you left selected.
Pages can be nested **eight deep**; a page that is already open above cannot be opened again
(*... is already open above this page*), and a menu none of whose tiles is on your page has no
tile to open it. Switch account starts the other account at its top page.

**No tile of the delivered page opens a sub-menu yet**: the mechanism is in the page table
of the `home` program, and the delivered table has not used it. The tiles you start inside a
sub-menu are kept by the Recent group like any other.

## The AI line

When the AI is on for your account (the administrator has chosen a provider, given it a
model and a key, **and allowed your account**; see [Asking the AI](29b-sd-tcl-asking-the-ai.html))
the home screen has one more row, just above the status line, that starts **`AI>`**. Without
the AI there is no such row and nothing on this page changes.

**Press Tab from the last tile (Sign out), or Back-tab from the first, or click the row**, type
what you want in your own words, and press Enter:

```
AI> open the ide
AI> show me who I am
```

Enter does not send anything. It shows **everything that will leave the machine**: the
provider and the model, one fixed instruction, the list of what this page can do (the names of
its tiles), what the page says about itself, and your request. **Cancel is the default button**,
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
catalogue](24-sd-tcl-programs-and-the-catalogue.html)), and so are the AI in [SED](27a-sd-tcl-sed.html),
[CED](27b-sd-tcl-ced.html) and [the debugger](17-sd-basic-debugging.html). The AI line on the
administrator's pages other than this one is planned and not built.

Programs the administrator assigns to an account, a menu builder for the holder
(grouping one's own programs into sub-menus) and a live line on the account holder's tiles
are planned and not built; today the page is the table above plus your own programs and, if
you turn it on, the Recent group.

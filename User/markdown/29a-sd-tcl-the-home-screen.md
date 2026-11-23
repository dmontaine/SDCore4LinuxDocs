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

The keys, menus, boxes and pick lists that every full-screen page shares are described once in
[Using the Full-Screen Pages](29d-sd-tcl-using-the-full-screen-pages.html); this page adds what is
particular to the home screen.

It needs a window of at least **140 columns by 43 lines** (the same as the other
full-screen tools) and a real terminal. In a smaller window it says so, with the
size it found. If you typed `home` at the prompt, you stay at the prompt; if your
account starts in the home screen, you are **signed out** (*This account starts at
the home screen, which could not open, so the session is signed out*), whether or not
the Terminal tile is on: a small window is never a way to the prompt. SDSYS, the
administrator, is the one exception: it always starts at the prompt, whatever the
system's default, and opens the home screen only when `home` is typed. In a session with no terminal (a
pipe, a phantom, a script) it says `home needs a terminal` and reads nothing, so
a script is never taken for someone typing. **In a bigger window the tiles spread over
the whole window**: as many columns of tiles as fit, each tile a little
wider, and the page follows the window when it is resized; at 140 by 43 each tile has its standard width.
If the window is made smaller than 140 by 43 while the home screen is up, it holds the keyboard
behind a warning that gives both sizes until the window is big enough again.

## What is on it

```
 File  Go  View  AI  Help                                                       home  alice@sales

   alice @ sales                                                  <> Switch account   -> Sign out
   Thursday 22 Oct 2026  -  18:52  -  SD Core for Linux LC2.0-0

   My tools
     [=]                  </>
     Editor               IDE
     edit a record        programs and files

   Everyone
     >_                                          [K]
     Terminal                                    Keys
     type exit to come back                      test your keyboard

   Develop
     [F]                  [V]                    [D]                    [Q]
     Files                Vocabulary             Dictionary             Queries
     files and indices    verbs and pointers     items and indices      build a report
     ...
```

| tile | what it does |
|---|---|
| **Editor** | runs `sed` (it asks which file and record) |
| **IDE** | runs `ide` |
| **Example programs** | runs `load.examples`, which puts SD's example programs into your account's `examples.bp`, compiled (*SD Example Programs*), then waits for Enter so you can read its summary; it needs `bp-on`, and without it the tile is dimmed and says why |
| **Receive files** | runs `receive` (*Moving files in and out*), then waits for Enter so you can read what came; it is there only when a transfer can be opened: the system allows file transfer, you are in your own account, and your account has the `xfer` gate |
| **Terminal** | leaves the screen for the ordinary command prompt (below) |
| **Keys** | runs `tool.keys`, the terminal and keyboard diagnostic |
| **Switch account** | a list of the accounts you may enter; then the home screen of the one you pick |
| **Files** · **Vocabulary** · **Dictionary** · **Queries** · **Bulk update** · **Programs** · **Tests** | the group *Develop*: each opens a development page (`tool.files`, `tool.voc`, `tool.dict`, `tool.query`, `tool.bulk`, `tool.catalog`, `tool.test`; see [The Development Tools](29c-sd-tcl-the-development-tools.html)) |
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
are built. **A tile for one of SD's own pages (a `tool.` verb) is left off when that verb is
not in your account's VOC**, so choosing a tile never ends in an unknown-verb error; when
the verb arrives (an update of the account's VOC) the tile appears. A pinned program's
tile, the Editor and IDE tiles are not hidden by this.

**The page scrolls.** It is laid out at its full height and only the rows that fit
are drawn, with a scroll bar in the last column when there is more than fits, so
the number of tiles can pass the height of the screen. The header (your name, the
date and time, the product and its version, Switch account and Sign out) stays where it is.

## Keys and the mouse

| key | does |
|---|---|
| the arrow keys | move to the nearest tile in that direction (a tile in the same row or column comes first) |
| Tab, Back-tab | the next and previous tile, in reading order, round the tiles (they never go to the AI line) |
| Home, End | the first and the last tile |
| Page Down, Page Up | the first tile of the next and of the previous group |
| a letter | the next tile whose label begins with it |
| / | find a tile: a window of the page's tiles; type any part of a tile's name (or of its group) to narrow the list; Enter moves the focus to the tile chosen (Enter on the page then starts it), Esc leaves the focus where it was |
| Enter, the space bar | start the tile |
| Esc, Backspace | back one page, when you are in a sub-menu (below); on the top page Esc opens the menu bar, as F10 does, and Backspace does nothing |
| F1 | help on the home screen |
| F5 | build the page again |
| F6, Shift-F6 | move to the AI line, and from it back to the tile you were on, when the AI is on for the account (when it is not, the status line says so); the same keys move between the boxes of every page |
| F10, Alt and a title's letter, a click on the top row | open the menu bar (File, Go, View, AI, Help). Every entry shows its key and does what the key does: **File** Sign out (Ctrl-Q, or no key when you typed `home` at the prompt) and, in that case, Back to the prompt (Ctrl-Q); **Go** Back (Esc or Backspace, only in a sub-menu), Terminal (Alt-T), Switch account (Ctrl-W), Find a tile (/), Start the tile (Enter); **View** Refresh (F5), Recent group on or off (Ctrl-R), Theme (Ctrl-T); **AI** Ask the AI (F6), dimmed when the AI is not on for the account; **Help** Help on this page (F1), Keys (Ctrl-K: the keys of the home screen). An entry whose tile the administrator turned off for your account is dimmed, and its key only says so. The Keys tile still opens the keyboard and terminal page `tool.keys` |
| Ctrl-T | the next color theme, kept for you: every page, the IDE, SED and the debugger start in it from then on (see *Using the full-screen pages*) |
| Ctrl-K | the keys of the home screen, in a box |
| F2 | find an action: every entry of the menus in one list (*Go > Terminal*, with its key); type part of a name to narrow it, Enter chooses. An entry that cannot be used now says *(not now)* and only explains why |
| a right click, Shift-F10 | the menu of the page's actions at the pointer (Shift-F10: in the middle), ending with *Find an action...* (F2). The home screen has one box, so the right click does not move anything first |
| Ctrl-Q | sign out (asks first; **Cancel** is the button Enter chooses, so a stray Enter signs nobody out). **When you typed `home` at the prompt, Ctrl-Q goes back to that prompt instead** and does not ask; the row then reads *^Q prompt* |
| Alt-T | the Terminal tile (Ctrl-T is the theme on every page) |

Backspace, Alt-T, Ctrl-W, Ctrl-R, Ctrl-T and Ctrl-K are not on the row of keys at the foot of
the screen (F1 lists every key). The row shows Enter, F1, F5, Ctrl-Q and /, Esc in a
sub-menu, and F6 when the AI is on for the account.

**Which Ctrl-Q you have.** A screen your session started in (the account's start setting is
the home screen) is the session's own: Ctrl-Q signs out. `exit` after the Terminal tile
brings back the same kind of screen you left. A screen you typed `home` for at the prompt is a visit: Ctrl-Q
leaves it for the prompt, and the session goes on. An account whose Terminal tile the
administrator turned off has no prompt to go back to, so Ctrl-Q signs out for it
whichever way the screen was started.

A **click** starts a tile; the **wheel** scrolls the page three rows; a click on the
menu bar opens the menu under it. The foot of the screen is the same as the
other full-screen tools - the status line, a border and the row of function
keys - with a hint line above it for the keys the row does not show: the
arrows, a letter and PgDn.

On a terminal with color the tiles are filled in the color of their group; on one
without, each tile is a box and the one with the focus is in reverse video, so
nothing depends on color.

## The terminal, and `exit`

The **Terminal** tile gives the screen back and shows

```
Terminal - type exit to return to the home screen
:
```

That is the ordinary command prompt, with all of its features (the command stack,
paragraphs, select lists, everything you can type at a prompt that did not come
from the home screen). **`exit`** (or **`menu`**) brings the home screen back. At a prompt that
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

**Sign out** (the tile, the File menu, or Ctrl-Q when your session started at the home
screen) asks first and then ends the session as `quit` does.

## Where a session starts

The administrator sets this for each account (`modify.account name start-menu`,
`start-terminal` or `start-default`, in the Administrator's guide), and sets what
accounts with no setting of their own do with:

```
set.start.default
set.start.default menu | terminal
```

**It is menu as delivered.** The setting is read when you sign on, and
when you type `logto` at the prompt to enter an account (not when the administrator does: an administrator's `logto` always leaves the prompt). Starting in the menu does
not confine anyone: the Terminal tile is always there.

The screen is never given to a session that cannot use it: a window under 140 by 43
or over 500 by 300, a pipe, a phantom, an API server, or a `logto` that a program ran with `execute`
(the home screen runs its own `logto` itself and shows the new account's page).

## Tiles the administrator turns off

Every tile is on as delivered, and the administrator can turn a tile off **for your
account** (`set.tile`, or the *Menu management* page): it is then not on your page,
and its menu entry cannot be chosen. The tile ids are `editor`, `ide`,
`terminal`, `keys`, `switch`, `signout`, the seven development tiles `files`,
`voc`, `dict`, `query`, `bulk`, `catalog` and `test`, and `recent` (the Recent
group, which is not a tile); **sign out cannot be turned off**. `set.tile` alone
says what is off. If the **Terminal** tile is off and your account
starts in the home screen, you are never given the command prompt: when the screen
ends (an error, the cursor lock) you are signed out. A window too small for the
screen signs you out whatever the tiles say. An account
that starts at the prompt keeps it. **It is a wall only for the prompt the screen
gives**: the programs behind the other tiles (`sed`, `ide` and the rest) are the
account's own, so to keep an account to the tiles it is given, turn those off too.
A shell needs the account's `sh` switch, which is off as delivered.

## Continued in

[SD TCL - The Home Screen: my.menu and the AI
Line](29a-sd-tcl-the-home-screen-2-my-menu-and-the-ai-line.html) — my.menu,
sub-menus and the AI line.

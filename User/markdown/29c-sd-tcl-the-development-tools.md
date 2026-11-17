Title: SD TCL - The Development Tools
Subtitle: Full-screen pages for the work in your own account: its files, and the verbs that make and change them.

```
tool.files
tool.voc
```

These pages are for **the account you are signed in to**. They work in every account (they are in
everybody's vocabulary), they need a real terminal of at least **140 columns by 43 lines** (and no bigger than **500 by 300**:
a larger window is refused at once, in a line that gives the size it found, because taking such a screen
costs time that grows with the square of its height), and they add no
access: every change they make is a command you could have typed, run for you after a box that shows the
exact command. A gate that is off for your account is met as the command's own refusal; the page shows
the gates you hold, and never tries an operation to find out.

**In a window bigger than 140 by 43 the pages use the whole window**: the lists show
more rows, the boxes are wider, a long explanation is wrapped at the width of its box instead of being cut,
and a page follows the window when it is resized, also while a question or a menu is open. At 140 by 43 each
page looks exactly as it did. 140 by 43 is still the smallest window: if the window is made smaller while a
page is up, the page holds the keyboard behind a warning that gives both sizes, until the window is big enough
again (Ctrl-Q, then y, leaves). The administrator's pages and the home screen do the same.

The keys, menus, boxes and pick lists that all these pages share - F1, F2, Esc, F6, the right-click
menu, the confirm box, the AI line - are described once in
[Using the Full-Screen Pages](29d-sd-tcl-using-the-full-screen-pages.html); each section below adds only
what is particular to its page.

The box that asks before a command is titled *Run this command?*. The few changes that are not commands -
a record the page writes or deletes itself - say what they are about to do instead: *Write this record?*
(an item of a dictionary in `tool.dict`, a saved query in `tool.query`), *Delete this record?* (a saved
query), *Update these records?* and *Put these records back?* (`tool.bulk`). The default button is still
Cancel. When a page hands the terminal to a command and asks *Press Enter to return*, Enter brings back
the page.

The home screen has a tile for each of them, in the group *Develop*.

**On a page with more than one box the keyboard can be in** (the query page, the bulk change page and the
test page here; on the administrator's side the sessions, menus and AI pages), the box that has it
is marked **`[*]`** in its top right corner and the others **`[-]`**, as the IDE marks its panes. **F6** moves the keyboard and the marks to the next box and **Shift-F6** back, round and
round, with the AI line as the stop after the last box when the AI is on for your account (the same keys on every page and in the IDE; Tab does not move between boxes). On the test page F6 goes
from the list to what the test under the cursor printed, and back. A box the keyboard never goes to has no mark.

**Every page has a menu bar on its top row**, made from the page's own key table, so
the bar, the key row at the foot and the keys cannot disagree. **F10**, **Alt and the letter** marked in a
title, or a **click** on a title opens a menu; **Esc** opens the first menu that does not begin with Quit
(so Esc and Enter never leave a page by accident; F10 opens *File*) when the page has nothing of its
own that Esc closes first (a name filter, a sub-view, the Indices pane of `tool.dict`, a result list: Esc
closes that, and the next Esc opens the bar). Up, Down, Left and Right move, Enter chooses, Esc leaves. An
entry is shown dimmed when the page cannot do it now, and **Quit is the last entry of any menu that has
other entries**. Choosing an entry does exactly what its key does, through
the page's own checks and boxes: the bar adds no access and runs no command by itself.

**F2 finds an action by its name.** It opens a list of every entry of the page's
menus, written *Menu > Entry* with its key beside it (*Query > Run the query   R*). Type part of a name to
narrow the list, Up and Down move, Enter chooses, Esc leaves. An entry the page cannot do now says *(not
now)*; choosing it shows why in a box and does nothing. Choosing any other entry does what its key does,
exactly as the menu bar's entry would.

**A right click on a box opens that box's menu**, at the pointer. If the box did not
have the keyboard, the right click first gives it the keyboard, as a click does (its mark becomes `[*]`), and
then opens its menu. A right click outside the boxes, and **Shift-F10** from the keyboard (in the middle of the
screen), open the menu of the box marked `[*]`. The menu lists that box's actions with their keys, dimmed when
they cannot be used now, and ends with *Find an action...*, which opens the F2 list. A letter, or Up, Down and
Enter, chooses (the action runs in that box, as its key does); Esc or a click outside closes it.
F1's list of keys names F2 and Shift-F10 on every page that has a menu bar.

## tool.files - the files of the account

```
tool.files
```

**`tool.files`** lists every file the account's VOC points at, one row each, in name order:

| column | what it says |
|---|---|
| Name | the file's name in the VOC |
| Kind | `dynamic` (records in groups, the usual data file), `directory` (each record is a file in a directory of the operating system), `sequential`, `server` (a file on another SD server) |
| Records | the file's own approximate count of records |
| Modulus | how many groups a dynamic file has now |
| Bytes | the size on disk of a dynamic file without its indices |
| Idx | how many alternate-key indices it has |
| Trigger | the name of its trigger, if it has one |
| Case | `any` when record ids ignore case (**as delivered**: jack and JACK are one record), `exact` when they do not |
| Dict | whether it has a dictionary |
| Open | `yes` when another session has the file open |

The box under the list describes **the file under the cursor**: where it is on disk, how many records it
holds, its modulus and group size and how full the groups are, the size of the primary and overflow parts,
whether ids ignore case, whether it can be written, its indices and its trigger, and who else has it
open. The line between the boxes shows the **gates your session holds** (`voc-edit`, `dict-edit`,
`bp-edit`), asked of the system.

### What the keys do

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **N** | make a file: asks for a name, then *dynamic* or *directory*, then shows `create.file name` in a box |
| **C** | clear the file under the cursor (`clear.file name`) |
| **D** | delete it (`delete.file name no.query`) |
| **A** | run `analyze.file` on it: the terminal is handed to the verb, which prints its report; Enter brings the page back |
| **I** | run `list.index` on it (its indices, in full), the same way |
| **T** | run `list.triggers` on it, the same way |
| **/** | show only the names that hold some text (empty shows them all) |
| Esc | clear the filter |
| F5 | read the files again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**Every change goes through a box.** The box shows the exact command, says what it does, and has two
buttons, *Run* and *Cancel*; **Cancel is the one Enter chooses**, so a stray Enter runs nothing. *Clear* and
*Delete* then ask for **the file's name, typed**; a wrong name does nothing. The command is the ordinary
verb, so its own checks are the checks: a file open in another session cannot be cleared or deleted, and
what the verb says is what the status line shows.

**A name the page does not give to a command.** The page hands a command only names of letters a-z,
digits, dot, dash and underscore. A file whose name has anything else (a capital, an `&`, a `$`) is listed and
described, and the page says which verb to type at the prompt for it instead.

**A VOC keyword is not a file name.** A name that the VOC holds as a keyword,
`all` for one, is refused as the name of a file to make, clear, delete or report on, with the words *... is a
keyword of the VOC, which a command would read as that keyword and not as a name: this page does not give it
to a command*. The verb would read the word as the keyword, not as your file (`delete voc all` empties the
VOC), and the question it asks would go to the output the page captures, where nobody reads it.

**Gates.** Making a new file, and clearing or deleting an ordinary data file, are not held back by the
edit gates: the new VOC pointer is a side effect of an ordinary command. The gates matter for the
protected kinds: clearing or deleting a **program file** (such as `bp`) needs `bp-edit`, and a
**dictionary** on its own needs `dict-edit`. The page shows which of the three gates your session holds
(`voc-edit`, `dict-edit`, `bp-edit`); if one is off, the verb's own refusal is what you get, shown on the
status line, and the file is left as it was. The administrator turns a gate on for an account with
`modify.account` (see *Accounts and Security*). Files of the **shared account** are not in your VOC as
files and are never changed from here.

## tool.voc - the vocabulary of the account

```
tool.voc
```

**`tool.voc`** lists every entry of the account's VOC, the file that tells SD what each word on a command line
means, one row each, in name order:

| column | what it says |
|---|---|
| Name | the entry's id |
| Type | `V` verb, `K` keyword, `F` file, `Q` pointer to a file in another account, `R` pointer to a record, `PA` paragraph, `S` stored sentence, `X` text |
| Points at | what it leads to, in a few words: the program a verb runs, the path of a file, the account and file of a Q-pointer |
| Works | for a file or a Q-pointer, whether the file it names can be opened (`yes`, `NO`); the page opens it to see |
| Against the shipped VOC | `same` as NEWVOC, the vocabulary every account was copied from; `changed` from it; or `added` in this account |

The box under the list shows **the entry under the cursor**, field by field. The line between the boxes shows
the **gates your session holds**, as `tool.files` does.

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **E** | edit the entry in the [IDE](24a-sd-tcl-find-program-dictionaries-and-the-ide.html) (`ide voc name`): the terminal is handed to the IDE, and leaving it brings the page back at the same entry |
| **D** | delete the entry (`delete voc name`) after a box that shows the command, with the id typed |
| **T** | choose the type shown: all, verbs, files, pointers, paragraphs and sentences, other |
| **S** | choose the state shown: all, only the entries that differ from the shipped VOC, only broken pointers |
| **/** | show only the ids that hold some text |
| Esc | clear the filter |
| F5 | read the VOC again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**The page writes nothing itself.** A record is changed by the IDE, which the page starts, or by `delete`, which
it runs; both are ordinary commands with their ordinary checks. Writing the VOC by hand needs the
**`voc-edit`** gate: without it the IDE's save and the delete are refused and the entry is left as
it was (the IDE says why, in a box). A VOC pointer made by an ordinary command such as `create.file` is not held back by the gate.

**An id the page does not give to a command.** As in `tool.files`, only ids of letters a-z, digits, dot,
dash and underscore are put into a command. A VOC id may have much else (a capital, `$`, `%`, `&`); such an
entry is listed and shown, and the page says which command to type for it instead. **Delete does not offer a
keyword either**: an entry of type K, `all` for one, is refused with the page's
words, because `delete voc all` would not delete that entry but ask to empty the VOC. Type the command at the
prompt if you mean it.

## Continued in

[SD TCL - The Development Tools: tool.dict](29c1-sd-tcl-tool-dict.html) —
tool.dict.

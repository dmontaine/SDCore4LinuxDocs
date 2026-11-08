Title: SD TCL - Using the Full-Screen Pages
Subtitle: How to move around, choose, answer and get help on every full-screen page of SD: one set of keys for all of them.

Every full-screen page of SD - the home screen, the development tools (`tool.files`, `tool.voc`, `tool.dict`,
`tool.query`, `tool.bulk`, `tool.catalog`, `tool.test`), the administrator's pages, `sp.view` and the dictionary form -
is built the same way and answers the same keys. Learn them once here; each page's own help (F1) adds only what is
particular to that page. What the pages are *for* is on their own pages: [The Home Screen](29a-sd-tcl-the-home-screen.html),
[The Development Tools](29c-sd-tcl-the-development-tools.html), [Asking the AI](29b-sd-tcl-asking-the-ai.html).

## The window

A page needs a terminal of at least **140 columns by 43 lines**. In a bigger window it uses the whole window: the
lists show more rows and the boxes are wider. If the window is made smaller while a page is up, the page waits behind a
warning that gives both sizes until the window is big enough again (Ctrl-Q, then y, leaves). A window that is too small
when you start a page is refused in one line that says the size it found.

A session with no terminal size (a script, a pipe) is given 140 by 43, so the pages still open there.

## What is on the screen

| Where | What it is |
|---|---|
| The top row | The **menu bar**: File first, Help last, and the page's own menus between. At the right end, the page's name and who you are (`administrator`, or `name@account`). |
| The middle | The page's **boxes**: lists, a form, a text pane. When a page has two or more boxes that can take the keyboard, the one that has it is marked. |
| The `AI>` row | Only when the AI is on for your account: the line where you ask the AI (below). |
| The last three rows | A **status line** (what just happened, or why a key is not in use now), a border, and the **row of keys**: the page's main keys and what they do. |

On a terminal without colour, nothing depends on colour: the box that has the keyboard and the chosen row are shown in
reverse video.

## The keys every page has

| Key | Does |
|---|---|
| **F1** | Help on this page: what it is for, and every key it answers, including the ones not on the row at the foot. The help names the page of this guide that describes it. |
| **F2** | **Find an action**: a list of every entry of every menu, written `Menu > Entry` with its key. Type any part of a name to narrow the list, then Enter to do it, or Esc to close the list and do nothing. An entry that cannot be used now is marked *(not now)*; choosing it only tells you why. |
| **F10**, Alt and a menu's letter, a click on the top row | Open the menu bar. |
| **Esc** | Close what the page has open - a filter, a sub-view, the output pane, a sub-menu. When nothing is open, Esc opens the menu bar on its first menu, so Esc and then Enter never leaves a page by accident. |
| **Tab**, **Back-tab** (Shift-Tab) | Move the keyboard to the next and the previous box, on every page that has more than one. |
| **Shift-F10** | The **action menu** of the box that has the keyboard, in the middle of the screen (see below). |
| **F5** | Read everything again and draw the page again. |
| **Ctrl-L** | Draw the whole page again, as it is, without reading anything. |
| **F6** | Move to the AI line, when the AI is on for your account (when it is not, the status line says so). |
| **Ctrl-O** | Show or hide the output pane: the results, refusals and command output of this visit to the page. |
| **Ctrl-Q** | Leave the page. |

Inside a list, the arrow keys, Page Up, Page Down, Home and End move as you would expect; a letter usually jumps to the
next row that begins with it, or narrows the list where the page says so.

## Menus

Every action of a page is in its menu bar, and **every entry shows its key**: choosing the entry does exactly what the
key does, so the menus are also a way to learn the keys. An entry that cannot be used now is dimmed, and cannot be
chosen; its key is out of use too, and the status line says why when you press it.

**The action menu** is the same idea for one box. **A right click on a box moves the keyboard to that box and opens its
actions where you clicked**; Shift-F10 opens the actions of the box that already has the keyboard. The
last entry is always *Find an action...*, which opens the F2 list.

## The mouse

A click chooses a row, presses a button or opens a menu; the wheel scrolls the list under the pointer; a right click
opens the action menu (above). On a bare Linux console with no desktop, the mouse works through **gpm**, which the
installer installs. `tool.keys` shows which keys your terminal sends.

## Boxes that ask before anything happens

A page never changes anything without asking first.

- **Before a command runs**, a box titled *Run this command?* shows **the exact command** - the same one you could have
  typed at the prompt. **Cancel is the button Enter chooses**, so a stray Enter runs nothing; press **r** or click **Run**
  to run it.
- **Something that cannot be undone, or that reaches beyond SD**, also asks you to **type a name** (the file, the
  account, the record) before Run takes effect.
- **A change a page makes itself** (a record it writes or deletes) says what it is about to do: *Write this record?*,
  *Delete this record?*.
- **A refusal** is the command's own refusal, shown in the output pane. A page adds no access: a gate that is off for
  your account stays off, and the page never tries an operation just to find out.

## Forms

A form is a list of labelled fields. Move between fields with Tab and Back-tab or the arrow keys, type to change one,
and press Enter (or choose Accept) when it is complete. The page checks the values when you accept, and says in the
status line which field is wrong and why; nothing is saved until the page's own save.

## Picking from a list

Where a page asks you to pick a file, a record or a saved query, it opens a **pick list**: a window with a heading row and
columns. **Type to narrow the list**, move with the arrow keys, **Enter** takes the row and **Esc** closes the list
taking nothing. A list that can delete (tool.query's saved queries, for example) deletes the chosen row with **Del**, after
you type its name to confirm.

## The AI line

When the administrator has allowed the AI for your account, every page has an **`AI>`** row above the status line. Press
**F6** (or click the row), type what you want in your own words and press Enter. Nothing is sent yet: a box shows
**everything that will leave the machine**, with **Cancel** as the default; press **s** for Send.

The answer comes in a box. It can *propose* an action of the page - you choose Accept or Reject, and anything that runs a
command or changes something defaults to Reject. It never runs anything by itself, and it works with your account's
rights only.

**Follow up**: the last button of an answer box asks a follow-up question. Your next question on the same page, within
ten minutes, then carries up to the last three questions and answers with it, once - and the preview shows them in
full before you send.

On the **dictionary form** the AI line can also propose values for the item's fields: each proposed value is shown in
full, Reject is the default, and an accepted value goes into its field only if the form accepts it. Nothing is written
until you accept the form and save.

The AI line never sees SD's own programs or system files; [Asking the AI](29b-sd-tcl-asking-the-ai.html) says exactly
what is sent.

## The IDE's Tools menu

In the IDE, **F10 then T** opens the **Tools** menu: Files, Dictionary, Vocabulary, Queries, Bulk update, Programs and
Tests. Each opens that page; when you leave it (Ctrl-Q, then Enter) you are back in the IDE with your unsaved text as you
left it.

## When something looks wrong

- **A key does nothing**: look at the status line - a key that is out of use says why. F1 lists every key of the page.
- **The page looks cut off**: make the window at least 140 by 43, or press F5 to draw it again.
- **Something is left on the screen that does not belong to the page** (a message another program wrote, say): press Ctrl-L.
  A page sends the terminal only what changed, so text written over it from outside stays until the page is drawn whole.
- **The colours are hard to read**: the site's colours are the administrator's choice (`SCREENTHEME`; the delivered `paper`
  is dark text on light grey, and `night` is light text on black); `tool.keys` shows what your terminal can display, and which
  keys it sends.

Title: SD TCL - The Terminal and the Session
Subtitle: Screen size, terminal behavior, silence, the inactivity timer, and writing to the error log.

Two different things are called the terminal. **`term` is the page** — how wide
and how deep SD thinks your screen is, which decides where output wraps and when
it pauses. **`pterm` is the wire** — how bytes are treated on the way in and out.
They are set separately and are almost never confused once you have seen both.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
something you type as it stands.

## The page: `term`

```
term                             display the settings
term {width} {, lines} {type}    set them
term color {bgc}{,fgc}           set display color
term default                     back to the defaults
term display                     show the terminfo bindings
```

```
:term
Page width: 200
Page depth: 9999
Device    : windows
```

**Depth is what decides paging.** A listing longer than the page pauses; set the
depth very large and it does not. That is why scripts driving SD open with
something like `term 200,9999` — a script has nobody to press a key at a
`Press any key` prompt, and a paged listing down a pipe stops for ever.

**Width sets only the width**, and the two are independent:

```
:term 132
:term
Page width: 132
Page depth: 9999
```

The depth stayed at 9999 because only the width was given.

### The page is the terminal's own size, and SD's default is 140 × 43

**SD asks the terminal how big it is.** When a session starts on a terminal, and
again each time the window is resized, SD reads the size of the window and makes
it the page: `@crtwide` and `@crthigh` follow it, and so does `term`. A program
that draws a screen — the SCREEN statement — sees an 80 × 24 window as 80 × 24.
(**SD's own full-screen programs are the exception: SED, the IDE, CED and the
full-screen pages are laid out for 140 × 43 or more**, SD's default size; they
refuse a window smaller than that, and the debugger's
full-screen display says so and is line by line instead. If the window is made smaller while one of them runs, it shows the
upper left corner and stops taking keys while the cursor is off the screen — see
[the IDE and the window](24e-sd-tcl-the-ide-ai-and-the-window.html). A `screen open` program of your own asks for the size it needs
with `minsize`, and SD asks nothing more of it.)

**SD's default is 140 columns by 43 lines, not 80 × 24.** It is what a session gets when there is no terminal to
ask — a phantom, a piped script, a service — and a report that looks wrapped or
truncated on a narrow window is usually the window, not the report.

**Where the number comes from**, in order, when a session starts:

| | |
|---|---|
| 1 | **the terminal's own window size**, as the terminal reports it |
| 2 | when there is no terminal to ask: the `LINES` and `COLUMNS` environment variables, if they are numeric |
| 3 | otherwise the terminfo entry's `lines` and `cols` |
| 4 | **otherwise 43 and 140** |

and whatever comes out is then raised to the minimum of 10 lines by 20 columns
if it is smaller. **`term` with a size typed by hand sets the page from then on,
until the next time the window is resized**, and it is taken as typed: any width
from 20 to 32767 and any depth from 10 to 32767, larger or smaller than the
default, with no other ceiling.

> **`term default` puts the 140 × 43 pair back, and it prints nothing when it
> does.** The verb sets the same 140 × 43 that is the fallback, whatever size
> the window is, then returns without a message — so the way to see that it
> worked is a bare `term` after it, not the command itself:
>
> ```
> :term default
> :term
> Page width: 140
> Page depth: 43
> ```
>
> `term 120,36` does the same thing by hand and is worth knowing for the cases
> where you want some other size back, the old default included.

**`Device`** is the terminfo entry in use. If a terminal type has no terminfo
entry SD falls back rather than failing: to `xterm` for a terminal of the xterm
family (`xterm-256color`, `gnome`, `konsole`, `tmux`, `screen` and the like) and
to `linux` otherwise, so this line is worth reading when screen handling
misbehaves.

### Which terminal types SD knows: `list.term.types`

```
list.term.types {lptr {n}}
```

Lists the terminal types SD has a definition for — the names of the entries under
`terminfo` in the SD directory, which is what the type in `term` and in the `TERM`
setting is looked up in — and how many there are. `lptr` sends it to a print unit.

```
list.term.types
```

```
ansi            ansi-generic    dec-vt100       dec-vt220       dec-vt330       dec-vt340
...
wy50            wy60            wyse50          wyse60          xterm
36 terminal type(s)
```

(The list is cut short here: it is 36 names in rows of six, and the count depends
on the release.) **A type that is not on it has no definition of its own**, and SD
substitutes one for it.

### What a key does: `tool.keys`

```
tool.keys
```

A full-screen diagnostic for the terminal and the keyboard, for anyone: it changes
nothing and reads nothing private (it shows the terminal type, the window and the
locale, which the session already knows). It needs a window of at least **140
columns by 43 lines** and says so, with the size it found, if the window is
smaller (or bigger than 500 by 300, which it also refuses before it draws). Use it when a function key does nothing, an arrow prints `^[[A`, color
looks wrong or the mouse does not answer.

| box | what it shows |
|---|---|
| **Terminal** | the terminal type SD is using (`TERM (SD)`, what `term` sets) and the one in the environment (`TERM (env)`), the window and the layout, the locale and whether the borders are line characters (UTF-8) or `+ - \|`, whether the terminal can show color, the theme, how many mouse events have arrived, how keys are being read, and how many of the 52 keys in the grid have been seen |
| **Last keys** | the 25 newest keys, newest first. **Names** (the start): the name the screen library reports for the key — `up`, `f5`, `ctrl-g`, `alt-s`, `mouse`, or the character itself with its code. **Raw** (Ctrl-R): the bytes the terminal sent, the first eight, in hex, with the characters beside them |
| **Keys seen** | the arrows, home, end, paging, insert, delete, backspace, tab, back-tab, Enter, Esc, the twelve function keys, the control keys, an Alt-letter, a printable character and the mouse; a key is ticked, and drawn bold, once it has been pressed |
| **Mouse** | the last mouse event (press, release, drag, wheel), where it was, and the counts |
| **Box drawing** and **Styles** | the borders the library draws with, and the library's sixteen styles each drawn in itself, so the theme in force can be seen on this terminal |

Every key is shown **before** the program acts on it. The program uses five:
**Ctrl-L** clears what has been seen (it uses no function key, so every function key can be tested), **Ctrl-R** switches between names and raw
bytes, **Ctrl-T** takes the next theme and keeps it for you, as on every page (a terminal that cannot
show color keeps mono and says so), **Ctrl-K** lists these keys and **Ctrl-Q** leaves, so a key that ends the
program can only be tested by leaving. `tool.keys` has no menu bar, so that Esc and F10 can be
tested here like any other key.

**A key that makes the terminal beep and shows nothing in names mode is one SD
has no name for.** SD understands the usual keys of every terminal in both
cursor-key modes (the arrows, Home, End, Insert, Delete, Page Up and Down,
Shift-Tab, F1 to F12, and the Ctrl, Shift and Alt forms of them such as
`ctrl-left` and `ctrl-pgup`), then adds those of the terminfo entry for the type
in force. A control sequence it has no name for is ignored whole: it is not
typed into your text. A byte of 128 or more is never a key. Press **Ctrl-R**,
then press the key again: the bytes it sent are shown, which is what a terminfo
entry needs. An Alt-letter shows as `alt-x` on a terminal that sends Alt+x as Esc
and x. Pasted text arrives as one `paste` key, however long it is.

Make the window smaller while it runs and the cursor lock takes the keyboard
with the message that the window is too small; make it larger again and the
screen comes back. Ctrl-Q, then `y`, leaves from the lock. If the input ends (a
piped session) the program ends.

### What this account may do: `tool.gates`

```
tool.gates
```

A full-screen page, for anyone, that answers "why can I not do that?" — it shows every
**gate** the system has, the switches the administrator turns on or off for an account
(`sh`, `os`, `sd`, `voc`, `bp`, `dict`, `net`, the shared account's read and write, and the
routes `ssh`, `api`, `files`, `files-write`, `files-admin` and `ai`, and `ssh-key`, whether
you may sign in over ssh with a key as well as with your password; it is off as delivered
for an account SD made, and a dash for a Linux user SD did not make, whose keys are its
own), each **ON** or **off for this session**. It needs a window of at least **140 columns by 43 lines**. (For the
administrator the same verb is the gate matrix of every account; this is the page every
other account gets.)

The row under the cursor is explained in plain words: what ON lets you do, what you can
still do with it off, whether it reaches beyond SD, as it is delivered, when a change
reaches you, and the `modify.account` word the administrator would use to give it or
withdraw it (for a gate that reaches beyond SD the administrator is asked to type your
account's name first). Up and Down, PgUp, PgDn, Home and End move; **F5** asks the system
again; **F1**, `?` or a click on the `[?]` explains the page; **Ctrl-Q** leaves.

* **The page changes nothing, and has nothing that could.** It asks the system what the
  session may do; it writes no file, runs no command and leaves no audit line. Only the
  administrator changes a gate, with `modify.account`.
* **It reports what the session holds, not what the register says now.** `sh`, `os`, `sd`,
  `net` and the shared account were loaded when you entered this account, and `voc`, `bp`
  and `dict` when you signed on (`logto` does not reload them): after the administrator
  changes one, sign off and on again to see it. The route gates (and `ssh-key`) are membership of a Linux
  group by your **login name**, read from the system each time (F5 shows a change).
* **Every account starts with every gate off, except the right to read the shared
  account.** A gate that is `plan` (raw sockets) is not built yet.

## The wire: `pterm`

```
:pterm display
Break trapping: On  (char ^C)
Input newline:  CR
Output newline: CRLF
Binary mode (client to server): Off
Binary mode (server to client): Off
Telnet negotiation: Off
```

**`pterm` with no keyword prints nothing.** It is not a display verb that has
gone quiet — it takes a keyword and `display` is one of them. The full set:

| | |
|---|---|
| **`pterm display`** | the settings above |
| **`pterm lptr`** | send them to the default printer |
| **`pterm break on`** \| **`off`** \| *c* | enable, disable, or set the break character |
| **`pterm newline cr`** \| **`lf`** \| **`crlf`** | the output line ending |
| **`pterm return cr`** \| **`lf`** | the input line ending |
| **`pterm binary on`** \| **`off`** | pass bytes through untranslated |
| **`pterm telnet on`** \| **`off`** | recognize `TN_IAC` |
| **`pterm reset`** *string* | the terminal reset string |
| **`pterm prompt`** `":"` `"::"` | change the command prompt and the continuation prompt |

**Input `CR`, output `CRLF` is the shipped setting** and it matches what SD
writes to everything else externally readable on this port.

**`pterm break off` disables the break key for the session.** It is the right
thing before a job that must not be interrupted and the wrong thing to leave
set, because it is also how you stop a runaway program.

## Silence: `hush`

```
hush on
hush off
hush expression
```

**`hush on` discards output entirely** — it does not redirect it, and nothing is
kept. With no argument it toggles.

**It suppresses the command echo as well as the output**, which is more
thorough than people expect. Below, `who` is typed **twice** — once inside the
silence and once after it — and the transcript contains one:

```
:hush on
:who
14 DON
:term 132
```

The first `who`, and `hush off` itself, produced no line at all. **If you are
debugging a script that has gone quiet, an unmatched `hush on` looks exactly
like a hang.**

## Continued in

[SD TCL - The Terminal and the Session: Timers, Dates and
Logging](29-sd-tcl-the-terminal-and-the-session-2-timers-dates-and-logging.html)
— the bell, timers, dates and logging.

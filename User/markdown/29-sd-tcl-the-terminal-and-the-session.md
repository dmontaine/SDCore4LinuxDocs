Title: SD TCL - The Terminal and the Session
Subtitle: Screen size, terminal behaviour, silence, the inactivity timer, and writing to the error log.

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

### The page is the terminal's own size, and SD's default is 140 × 42

**SD asks the terminal how big it is.** When a session starts on a terminal, and
again each time the window is resized, SD reads the size of the window and makes
it the page: `@crtwide` and `@crthigh` follow it, and so does `term`. A program
that draws a screen — the SCREEN statement — sees an 80 × 24 window as 80 × 24.
(**SD's own full-screen programs are the exception: SED, the IDE and CED are
laid out for 140 × 42 or more**, SD's default size, and refuse a window smaller
than that; the debugger's full-screen display says so and is line by line
instead. If the window is made smaller while one of them runs, it shows the
upper left corner and stops taking keys while the cursor is off the screen — see
the SED page. A `screen open` program of your own asks for the size it needs
with `minsize`, and SD asks nothing more of it.)

**SD's default is 140 columns by 42 lines, not 80 × 24** (it was 120 by 36
until 18 October 2026). It is what a session gets when there is no terminal to
ask — a phantom, a piped script, a service — and a report that looks wrapped or
truncated on a narrow window is usually the window, not the report.

**Where the number comes from**, in order, when a session starts:

| | |
|---|---|
| 1 | **the terminal's own window size**, as the terminal reports it |
| 2 | when there is no terminal to ask: the `LINES` and `COLUMNS` environment variables, if they are numeric |
| 3 | otherwise the terminfo entry's `lines` and `cols` |
| 4 | **otherwise 42 and 140** |

and whatever comes out is then raised to the minimum of 10 lines by 20 columns
if it is smaller. **`term` with a size typed by hand sets the page from then on,
until the next time the window is resized**, and it is taken as typed: any width
from 20 to 32767 and any depth from 10 to 32767, larger or smaller than the
default, with no other ceiling.

> **`term default` puts the 140 × 42 pair back, and it prints nothing when it
> does.** The verb sets the same 140 × 42 that is the fallback, whatever size
> the window is, then returns without a message — so the way to see that it
> worked is a bare `term` after it, not the command itself:
>
> ```
> :term default
> :term
> Page width: 140
> Page depth: 42
> ```
>
> `term 120,36` does the same thing by hand and is worth knowing for the cases
> where you want some other size back, the old default included.

**`Device`** is the terminfo entry in use, `windows` on this port. If a terminal
type has no terminfo entry SD falls back to `windows` rather than failing, so
this line is worth reading when screen handling misbehaves.

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
ansi            ansi-generic    dec-vt100       dec-vt330       dec-vt340       dec-vt400
...
wy50            wy60            wyse50          wyse60          xterm
51 terminal type(s)
```

(The list is cut short here: it is 51 names in rows of six, and the count depends
on the release. The Data General, MDC Prism, Prime and Televideo 910 definitions that
were once on it were removed in 1.2-0.) **A type that is not on it has no definition of its own**, and SD
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
| **Terminal** | the terminal type SD is using (`TERM (SD)`, what `term` sets) and the one in the environment (`TERM (env)`), the window and the layout, the locale and whether the borders are line characters (UTF-8) or `+ - \|`, whether the terminal can show colour, the theme, how many mouse events have arrived, how keys are being read, and how many of the 52 keys in the grid have been seen |
| **Last keys** | the 25 newest keys, newest first. **Names** (the start): the name the screen library reports for the key — `up`, `f5`, `ctrl-g`, `alt-s`, `mouse`, or the character itself with its code. **Raw** (Ctrl-R): the bytes the terminal sent, the first eight, in hex, with the characters beside them |
| **Keys seen** | the arrows, home, end, paging, insert, delete, backspace, tab, back-tab, Enter, Esc, the twelve function keys, the control keys, an Alt-letter, a printable character and the mouse; a key is ticked, and drawn bold, once it has been pressed |
| **Mouse** | the last mouse event (press, release, drag, wheel), where it was, and the counts |
| **Box drawing** and **Styles** | the borders the library draws with, and the library's sixteen styles each drawn in itself, so the theme in force can be seen on this terminal |

Every key is shown **before** the program acts on it. The program uses four:
**Ctrl-L** clears what has been seen, **Ctrl-R** switches between names and raw
bytes, **Ctrl-T** changes the theme (mono, classic, blue; a terminal that cannot
show colour keeps mono and says so) and **Ctrl-Q** leaves, so a key that ends the
program can only be tested by leaving.

**A key that makes the terminal beep and shows nothing in names mode is one SD
has no name for.** SD understands the usual keys of every terminal in both
cursor-key modes (the arrows, Home, End, Insert, Delete, Page Up and Down,
Shift-Tab, F1 to F12, and the Ctrl, Shift and Alt forms of them such as
`ctrl-left` and `ctrl-pgup`), then adds those of the terminfo entry for the type
in force. A control sequence it has no name for is ignored whole: it is no longer
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
routes `ssh`, `api`, `files`, `files-write`, `files-admin` and `ai`), each **ON** or **off
for this session**. It needs a window of at least **140 columns by 43 lines**. (For the
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
  changes one, sign off and on again to see it. The route gates are membership of a Linux
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
| **`pterm telnet on`** \| **`off`** | recognise `TN_IAC` |
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

## The bell

```
bell on
bell off
```

Sets or clears the character SD sends to sound the terminal bell. **Neither form
prints anything**, and `bell` with no keyword is an error rather than a toggle:
*Mode keyword missing or invalid*.

## Clearing type-ahead and stored prompts

```
clear.input
clear.prompts
```

**`clear.input`** discards anything typed ahead but not yet read.
**`clear.prompts`** discards the inline prompt and response text a previous
command left behind. Neither prints anything.

(The run-together spellings `clearinput` and `clearprompts` were second names
for the same verbs and were removed in 1.2-0.)

> **Neither can be demonstrated down a pipe, and `clear.input` should not be
> sent down one at all.** In a piped session the input stream *is* the script,
> so discarding unread input discards the commands that have not run yet —
> including the `off` that would have ended the session. **A run that did this
> hung, was killed, and left a session in the user table that only `sd
> -cleanup`, run as SDSYS, could clear.** Both verbs are for a person at a
> terminal.

## The inactivity timer

```
autologout
autologout n
```

```
:autologout
Autologout is disabled
```

which is the shipped state. Setting a timer ends a session that has been idle
too long — useful on a machine where people walk away from a prompt, and worth
thinking about before enabling on a machine where a long-running interactive job
is normal.

*n* is minutes and 0 turns it off. **It applies to an API session too**: a client that
executes `autologout 10` (`SDExecute("AUTOLOGOUT 10")`) has its server session ended after
ten minutes in which it sent nothing, and its next request fails at once
(see [SD Client API](37-sd-client-api.html)). The setting belongs to the one session that gave it.

## The command echo: `echo`

```
echo on
echo off
echo
```

**`echo off` stops SD echoing what you type**; with no keyword it toggles.
Neither form prints anything, and `echo off` suppresses its own confirmation
along with everything else.

```
:echo off
:28 DON
:who
28 DON
```

That is one `who` under `echo off` and one after `echo on`. **The first has no
`:who` line above it** — its output ran straight on after the prompt — and
`echo on` produced no line of its own either, because the echo it restores does
not apply to the command that restores it.

**It is not `hush`, and confusing the two wastes time.** `echo` decides
whether your **input** is shown back; `hush` decides whether SD's **output** is
shown at all. A session that has gone completely silent has `hush on` set; one
where the commands vanish but the answers still appear has `echo off`.

## Dates and times

```
date                    today, spelled out
date internal           today as SD's internal day number
date n                  day number n, spelled out
date some-date          that date's day number
time                    the time and the date
time internal           seconds since midnight
```

```
:time
14:10:34 27 AUG 2026
:date
Thursday, 27 August 2026  02:10pm
```

**`date` prints the time and `time` prints the date.** Both print both, in
different formats and a different order, and neither name says so. `date` is
the long spelled-out form and `time` is the short one.

**`internal`** on either gives the raw number a program would see:

```
:date internal
21424
:time internal
51088
```

the day number and seconds since midnight. **`date` with an argument is a
converter, and which way it converts depends on what you give it** — a bare
number is read as a day number and comes back as a date, anything else is read
as a date and comes back as a day number:

```
:date 20000
Monday, 03 October 2022
:date 4 jul 2026
21370
:date zznotadate
Invalid date format
```

`time` takes no argument other than `internal`.

### Which way round a date is read: `date.format`

```
date.format on | off | display
```

```
:date.format display
European date format is off
```

**`on`** selects European (day-first) date format for the session, **`off`**
returns to the default, and **`display`** reports which is in force. If a default
conversion code other than `D` is set, `display` names that too.

**`date.format` with no keyword prints nothing** — like `pterm`, it wants one.

**Setting the machine's date is a different thing entirely** — it is an
administrator verb, it changes the clock for the whole installation rather than
for your session, and it is in the **administrator documentation** under
*Accounts and Security*.

## Waiting

```
sleep n
sleep hh:mm{:ss}
```

A number is seconds; a time is *until* that time, rolling over midnight if it
has already passed. **`sleep` with no argument returns immediately** rather than
sleeping for ever — the argument parses as zero.

## A log of the commands a session runs: `command.logging`

```
command.logging {on | off}
```

`on` starts a log of every command this session runs and where it came from;
`off` stops it; with neither word it says whether it is on and where the file
is. The log is a file named `clog.`*user number*`.log` **in the account
directory**, mode 0600 (nobody but its owner can read it), added to and never
emptied. A line is tab separated: the time as an epoch value, the user number,
the login name, the origin and the command.

| origin | |
|---|---|
| `User` | typed at the prompt |
| `Cmd` | the command line `sd` was started with |
| `PA` | a line of a paragraph |
| `Exec` | any other command a program or a menu runs, such as `execute` |

The `command.logging on` itself is not in the log, because the log starts after
it; `command.logging off` is. **openQM writes the file in `TEMPDIR` and has a
`CMDLOG` parameter that logs every session into one directory; SD has neither.**
`TEMPDIR` is `/tmp` unless `sd.conf` says otherwise, a directory anyone can
write to, where another user could create the file first and be handed the log.
A symbolic link left where the file would be made is refused (*The command log
could not be started*). Logging belongs to the session and is off in the next.

## Writing to the error log

```
logmsg text
```

Everything after the verb is the message. It prints nothing, and what it writes
is a stamped, attributed entry in the system error log:

```
27 Aug 26 13:13:31 User 11 (pid 1786, don):
   nightly run finished
```

**The user number, the process id and the account name are added for you**, so
a message does not need to say who wrote it. The log is
`/usr/local/sdsys/errlog`, shared by every session, which makes `logmsg`
the right way for a phantom or a scheduled job to report something a person will
read later — there is no terminal to print to and no transcript kept.

## Reading the documentation: `pdf`

```
pdf
pdf name
```

`pdf` alone lists the documents (the PDF files the administrator has put in the
shared account's `pdf` directory, without the `.pdf`), and `pdf name` shows one in
the PDF reader installed on the computer you are sitting at. **It works in any
account**, including one that is not allowed to run programs, because the reader it
starts is one the administrator has allowed for this one purpose and the document
is always one of those files, never a path you type.

It needs two things from the administrator and one from you:

* **a reader the administrator has allowed** (`set.viewer`). If none has been, `pdf`
  says `No viewer has been allowed for documents`; it starts nothing;
* **the documents installed** (`docs.install`); with none, `pdf` says there are no documents;
* **a graphical session**: the reader opens on the display of the session you are
  in. Over plain ssh, which has no display, `pdf` says so and does nothing.

`pdf guide.pdf` is the same as `pdf guide`. A name that is not a lower case name of
letters, digits, dot, dash and underscore, or is not in the list, is refused in words.
The administrator's guide, *Operating-system access*, says what is checked each time a
reader is started and why an allowed reader is not a shell.

## See also

[SD TCL - The Command Processor](19-sd-tcl-command-processor.html) ·
[SD TCL - Printing and Spooling](28-sd-tcl-printing-and-spooling.html) ·
[SD Basic - Terminal Input and Output](12-sd-basic-terminal-input-and-output.html).

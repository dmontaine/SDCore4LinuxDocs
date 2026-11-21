Title: SD BASIC - Debugging: The Full-screen Debugger
Subtitle: The debugger on the full screen and line by line, asking the AI, and pdump.

This page continues [SD Basic - Debugging](17-sd-basic-debugging.html).

## Full screen on a terminal, line by line everywhere else

**On a terminal that can address a cell and clear itself, the debugger takes the
whole screen.** Its test is that the session is a real terminal (SD can read its
window size) and that the terminal definition has `cup` and `clear`: xterm, the
Linux text console, vt100, vt102, vt220, ansi, and the terminals that behave like
them. `dumb` and `unknown` have no `cup` and stay line by line. Then:

- the top row is the **title bar**: the program and the line about to run at
  the left, and at the right end `debugger` and who is signed on, as on the
  other full-screen pages;
- below it is the **source**. Each row has a two-cell **gutter** — `>` marks the
  line about to run and `*` a line with a breakpoint (a breakpoint wins when the
  line about to run has one) — then the line number and the text. The line about
  to run is highlighted from end to end. When the site's theme is `paper`, as
  delivered (or `night` or `blue`), the text is colored as SD BASIC: comments, strings,
  constants and the statements. In the plain `classic` theme, which the debugger
  uses when the site names none, the source has no syntax color;
- to the right of the source, from column 93, is the **Autos** pane: the
  variables the line about to run uses come first, in the order the line names
  them; then those of the line the debugger last stopped at, when it is a line of
  the same program; then the variable you are watching; then the other variables
  of the program in the order it declares them, until the pane is full. It is empty
  only for a program that has no variable. Each row is `name = value`, short: a
  string is cut, and a matrix or a collection says what it is (`/name` shows more).
  The pane is drawn again at every stop and after every command, so `set n=7` shows
  at once. The names are the program's own spelling in the symbol table (upper case
  unless the program is case sensitive);
- under a rule come the **messages** (what a command printed; five rows, `window` *n*
  changes that), and the **command line**, where you type the commands on this page;
- below the command line the **foot** has three rows, as the other full-screen pages
  have: a **status line** in reverse video (`[Command]`, how many breakpoints there are
  and the variable being watched), a line across the screen, and the **function-key row**:
  `F1 help  F2 find  F3 stop  F4 screen  F5 refresh  F7 step  F8 line  F9 run  F10 menu  ^F7 parent  ^F8 program`;
- **F1** shows the help in a box, **F4** shows the program's own screen until
  you press a key, and Page Up and Page Down move the source. The commands are as
  they were.
- **The top row is a menu bar**: **Esc** on its own or **F10** opens
  it. **Run** has Run to a breakpoint (F9), Step (F7), Step a line (F8), Run to the parent
  (Ctrl-F7), Run to the parent program (Ctrl-F8), Stop the program (F3 or Ctrl-Q) and Abort;
  **View** the program's screen (F4), Theme (Ctrl-T) and Refresh (F5); **Help** Help (F1),
  Keys (Ctrl-K) and Find an action (F2). The program and its line follow the titles.
- **F2 finds an action and Ctrl-Q stops the program and leaves**, as on every page. F2 lists every entry of the menus; type part of a
  name to narrow the list, Enter to do it, Esc to close it. **Abort has no key on this screen**:
  it is on the Run menu and in the F2 list. In line mode (a terminal too small or with no
  cursor addressing), which has no menu bar, F2 still aborts.
- **The keys every page has**: **F9 runs**, **F5** and
  **Ctrl-L** draw the screen again, **Ctrl-T** takes the next color theme and keeps it for
  you, **Ctrl-K** lists the keys. On the command line, delete to the end of the line and swap
  two characters are **Alt-K** and **Alt-T** (or Esc, then K or T).

**The full-screen display is laid out for 140 columns by 43 lines or more**
(a bigger window is used
whole, and the extra width goes to the source). **On a window smaller than that the
debugger does not refuse: it says why, once, and is line by line for the session** —
*The debugger needs a window of at least 140 columns by 43 lines for its full-screen
display; this one is 100 by 30, so it is using line mode* — because a small window
is no reason to take away the way to debug a program. The window measured is the one
on the screen, or the display `term w,h` gave if that is smaller. The choice is made
at the first stop of a session.

If the window is made smaller **while the full-screen display is up**, the debugger
lays itself out again within a second and shows the **upper left corner** of its
140 by 43 layout and nothing past the edge, and draws everything again when the
window is made bigger. The command line is on row 40 of 43 (the foot is below it), so
a window of 39 lines or fewer does not show where you type: the debugger then does not
take keys. A warning in reverse video fills the upper left, every key is thrown away,
it goes by itself when the window is big enough, and **Ctrl-Q, then y** leaves the
debugger the way F3 (Stop) does. A window narrower than 140 but 40 lines or more
high shows the left part of the lines and works as usual.

The program's own screen is kept by the terminal (that is what the alternate
screen is): when you let the program run, the debugger gives the terminal back
and the program's output is on its own screen, and it is on the alternate
screen again at the next stop. The colors are the screen library's: if the
program asked for no theme, the debugger uses the theme you chose with Ctrl-T,
else the site's theme (`SCREENTHEME` in `sd.conf`, `paper` as delivered)
while it is up, and the `classic` one when neither names one; and whatever the program asked for otherwise. When the
debugger lets the program go, the program's theme is given back, whether or not the
window was resized or `window` *n* was typed on the way.

**What the program's own screen becomes depends on the terminal.** A terminal
with an alternate screen (`smcup` and `rmcup`: xterm and its kin) keeps the
program's screen aside, and gives it back untouched when the debugger lets go.
A terminal without one (the Linux console, vt100, vt220, ansi) has only the one
screen, so the debugger clears it when it comes up and clears it again when it
lets go. A program that owns the screen library's screen (it ran `SCREEN OPEN`)
gets everything the library knows drawn again: its forms, its cursor, its theme.
**What the program printed with `PRINT` or `CRT`, and what was on the screen
before, is not given back** — a terminal cannot be asked what it shows, and
the line-by-line debugger, which does not clear anything, keeps that text. For
the same reason `F4` (or `v`) on such a terminal shows an owned screen again
until a key is pressed, and says *"There is no second screen to show on this
terminal"* for any other program.

To keep the line-by-line debugger on a terminal that would otherwise get the
full screen, put the word `LINE.MODE` on a line of the VOC record
`$debug.options` of the account (the same record that holds `WINDOW` *n*).
Nothing about this gives the debugger more reach than before: the AI line,
for instance, which the full-screen debugger offers when the AI is on for the
account, is the same gated line it already was.

**In a session that is not a terminal, on `dumb`, `unknown` or `null`, and in a
window smaller than 140 by 43, the debugger is line by line.** Every command works, as the
transcripts on this page show, and there is a real gain: because it is
line-oriented it can be **driven from a script**. A whole debugging session can
be fed down a pipe.

`@tty` reads empty in a piped session, and the debugger works there anyway.

(The full-screen display does not use AccuTerm, which SD does not support.)

## Asking the AI

In the full-screen display, when the AI is on for your account (see
[Asking the AI](29b-sd-tcl-asking-the-ai.html)), the command **`AI`** — or `AI` and a question, such as
`ai why is y empty` — asks it about the stop. The AI is told the program and the line, the call stack
and about fifty lines of the source round the stop. As everywhere, **Enter shows your request and the size
of all that will be sent first** (SD's own instruction is sent but not shown), with Send and Cancel (the default); the answer is words in a box, and the debugger's
screen is drawn again after it. Nothing in your program or the debugger is changed, and a command in
the answer is ignored. Line mode and a phantom do not have it.

## Who has it

Read out of an account's own VOC:

| VOC entry | record | |
|---|---|---|
| `debug` | a `V` verb, `IN`, internal command 29 | run a program in debug mode |
| `debugging` | a `K` keyword, 53 | the compiler keyword |
| `pdebug` | a `V` verb, `CA $PDEBUG` | the phantom debugger |

**Every account has `debug` and `pdebug`.** `debugging` is a keyword rather
than a verb, and every account has it.

## A process dump from inside the program: `pdump`

```
pdump
```

The statement writes a process dump of the session it runs in and **the program carries
on** at the next line; nothing is stopped. The dump is the same file the `pdump` command
writes for a session number (see [SD TCL - Processes and
Phantoms](30-sd-tcl-processes-and-phantoms.html), which says where it goes): the program's
variables, each string with its length, the call stack, open files, and the environment,
with the value of any name that looks like a secret (a key, a token, a password) left out.

Use it to take a picture of a program's state at one point without stopping it. **The dump
holds the program's data**, so remove it when you have read it.

## What is not here

**`trace` does not exist.** In an
ordinary account it is *"Unrecognized statement"*.

**The programmatic debug statements are restricted.** `debug.on`,
`debug.off`, `debug.set`, `breakpoint` and `watch` are internal-only, and all
five are *"Unrecognized statement"* in an ordinary account. They are
what the debugger itself is built from. **`debug` — the plain statement — is
not restricted**, and it is the one you want.

`debug.info()` is internal-only for the same reason.

**No conditional breakpoints, no data breakpoints beyond the single watch, and
no remote attach.** The debugger runs in the session that runs the program.

## See also

[SD Basic - System and Environment](16-sd-basic-system-and-environment.html) ·
[SD Basic - Program Structure](01-sd-basic-program-structure.html) ·
[SD Basic - Program Control](02-sd-basic-program-control.html) ·
[SD Basic - Locks and Transactions](14-sd-basic-locks-and-transactions.html).

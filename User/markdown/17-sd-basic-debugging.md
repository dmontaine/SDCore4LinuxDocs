Title: SD Basic - Debugging
Subtitle: Stopping a program where you want it, and looking at what it thinks is true.

SD has a real source-level debugger. It stops on a line, shows you the source,
prints any variable with its type, changes one, sets breakpoints, watches a
variable for change, and shows the call stack. It is worth ten minutes of
learning and it replaces most of the `crt` statements people leave behind.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

> **The transcripts below are the debugger's own output, reproduced exactly as
> it prints them** — including the `help` screen. What you see on your own
> screen should match character for character.

## Nothing works until you compile with DEBUGGING

```
basic bp MYPROG debugging
```

**The `debugging` keyword is what makes every other thing on this page
possible.** Without it the compiler emits no per-line debug information, and
the debugger has nothing to stop on. It shows in three ways:

| | |
|---|---|
| a `debug` statement in a program compiled **without** it | *"WARNING: DEBUG statement ignored - Not compiling in debug mode"*, **0 errors**, and the program **ran straight through** |
| the same program started with the `debug` **verb** | ran straight through — no prompt, no message |
| the same source compiled **with** `debugging` | stopped, and the prompt appeared |

The warning is a warning, not an error: the program compiles and runs. **A
`debug` statement in production code is therefore harmless but useless**, and
the tell that you forgot the keyword is that nothing happens.

**Recompile without `debugging` when you are finished.** The extra information
is per line, and the debugger becomes reachable by anyone who can run the
program.

## Two ways in

```
debug bp MYPROG          ;* the verb: stop on the FIRST line
```

The verb stops before line 1 has run:

```
:DEBUG BP ZZDBG
 1:       crt 'ZZDBG.START'

>
```

```
      debug                ;* the statement: stop where you put it
```

The statement stops on the **next** line, the one that has not run yet:

```
ZZDBG.START
 4:       n = n + 1

>
```

Use the verb when you want the whole program, and the statement when you want a
particular place — inside an `if` that is only true for one record, for
example. The statement is the only way to stop on a condition, because there is
no conditional breakpoint.

`>` is the prompt. `pdebug` is the same debugger for a phantom; the `debug`
verb refuses a phantom outright with *"Cannot debug program in a phantom
process"*.

In `pdebug` an `@variable` you ask for (`/@user0`, `/@tty`) is the value in the
phantom being debugged, not in your own session: the request is sent to the
phantom, which answers with its own. In the phantom `@tty` is `phantom`. The
`@variables` the debugger can show now include `@bpv`, `@conv`, `@ds`,
`@exception` and its three companions, `@file.name`, `@filename`, `@lpv`, `@nd`,
`@ni`, `@ns`, `@nv`, `@option`, `@pstat`, `@seqno`, `@system.return.code`,
`@transaction.id`, `@transaction.level` and `@trigger.return.code`, as well as
those it showed before.

## The commands, as this port prints them

Typing `help` at the `>` prompt gives:

```
BRK n           Set breakpoint on line n
CLR {n}         Clear all or specific breakpoint
DUMP var path   Dump variable to given pathname
HELP            Display this screen
ABORT or Quit   Abort program
EXit            Exit subroutine
EP              Exit program
Goto n          Goto line n
Run {n}         Free run or to line n
SRC {n}         Display line n, current line if n omitted
SRC {m,n}       Display n lines starting at line n.
STACK           Display call stack
Step .n         Step n debug elements
Step n          Step n lines
STOP            Stop program
Watch var       Watch for changes to named variable
UnWatch         Cancel Watch action
```

**The capital letters are the abbreviation** — `S` for `Step`, `R` for `Run`,
`G` for `Goto`, `W` for `Watch`, `UW` for `UnWatch`, `EX` for `EXit`, `Q` for
`Quit`. `?` is a synonym for `/` below, not for `help`.

## Looking at a variable

```
/name
```

A slash and the name, on three kinds of variable:

```
>/N
Integer: 41

>/K
String (9 bytes): "some text"

>/ARR(1)
String (5 bytes): "first"
```

**The type is part of the answer, and it is often the answer.** `Integer: 41`
and `String (2 bytes): "41"` are different bugs, and so are `Integer: 1` and
`Float: 1.500000`. The rest of the shapes:

| | |
|---|---|
| a variable that has not been assigned yet | `Unassigned` — **not** an empty string |
| a name the program never mentions | `Variable not defined` |
| a floating point variable | `Float: 1.500000` |

The difference between the first two matters: `Unassigned` means the variable
is yours and has no value yet, and *"Variable not defined"* means you have
mistyped the name.

A matrix element takes its subscripts: `/ARR(1)` for one dimension,
`/ARR(2,3)` for two. `/` on its own repeats the last variable you looked at,
printing the same answer again.

```
set name = value
```

changes it. `SET N = 100` then `/N` gives `Integer: 100`, and the program
carries on with the new value.

`dump var path` writes a variable to an operating system file, which is the way
to look at something too long for the screen.

**A data collection** is shown with its kind, the number of elements and its
JSON text, the names in order; a long one is cut off with dots:

```
>/C
Collection (3 elements): {"a":[1,2,{"k":"v"}],"name":"Acme","on":true}

>/C{name}
String (4 bytes): "Acme"

>/C{a/3/k}
String (1 bytes): "v"

>/C{on}
Boolean: true
```

(That is a collection of three elements, one of which is an array whose third
element is itself a collection.) Name an element with its path in braces, the
names separated by slashes (a number picks an element of an array, counting
from 1). Names are case sensitive. The answer is the element's own type — `String`,
`Integer`, `Array`, `Collection`, `Boolean` or `Null` — and a path that leads
nowhere says *Element not found in the collection*. **`dump c{sub} path`
writes the JSON of one element, and `dump c path` the whole collection**, as
`dump` does for any variable. A collection that contains itself is shown as
*(cannot be shown)* and does not stop the debugger.

## Stepping and running

| | |
|---|---|
| `s` | one line — the debugger prints the next one, `5:  crt 'ZZDBG.N=' : n` |
| `s `*n* | *n* lines — `s 3` from line 4 lands on line **7** |
| `s .`*n* | *n* debug elements — finer than a line |
| `r` | run on |
| `r `*n* | run on until line *n* |
| `g `*n* | jump to line *n* **without running the lines in between** |
| `ex` | run to the end of this subroutine |
| `ep` | run to the end of this program |
| `stop` | stop the program |
| `q` | abort — prints `ABORT : Debugging terminated` |

An `s` in the middle of an assignment sequence:

```
>/N
Integer: 41

>S
 5:       m = n * 2

>/N
Integer: 42
```

— the step executed line 4, `N` moved from 41 to 42, and the debugger is now
sitting on line 5.

## Breakpoints

```
brk 9        set one on line 9
clr 9        clear that one
clr          clear all of them
```

`brk 9` then `r`:

```
>BRK 9

>R
 9:       crt 'ZZDBG.N=' : n : ' M=' : m : ' K=' : k
```

`src` shows you the line numbers to aim at. `src 1,4`:

```
>SRC 1,4
 1:       crt 'ZZDBG.START'
 2:       n = 41
 3:       debug
 4:       n = n + 1
```

Breakpoints are on a **line number in the source**, so the source record has to
still match the compiled object. The debugger checks the modification time and
refuses with *"Unable to find source record"* if the source has moved on;
recompile rather than trying to work around it.

**There is no conditional breakpoint.** Put a `debug` statement inside the `if`
instead, and recompile.

## Equate tokens

A program compiled with `$mode debug.equates` (and for the debugger, `basic ...
debugging`) keeps its `equate` and `$define` tokens in the object. The
debugger then takes a token for what it stands for, wherever it takes a
variable name:

```
>/cust.name          the variable the token was equated to
>/limit              LIMIT = 100        a $define or an equate of a constant
>set tot = 9         sets the variable behind the token
>w tot > 10          watches it
```

A token equated to a **variable**, an **element of a matrix** or a **field of
a dynamic array variable** shows, `set`s and `watch`es the thing it stands
for. A token of a **number, a string or `char(n)`** is not a variable: it
shows as `name = value`, and `set` and `watch` refuse it with *Variable not
defined*. Without the mode a token is not known to the debugger, as it
never was.

**A token may also be the value** of a `set` (16 Oct 2026): `set tot = numc`
gives the variable the number the token stands for, and a token of a string or
of `char(n)` gives it that. A token of a **variable** is not a value, and is
refused with *Illegal value* as before.

## Every variable, control characters, the size of the screen

**`/*`** shows every variable of the program, one to a line, the name first and
then what `/name` shows: the locals, then the common blocks the program names.
(In the full-screen debugger the lines are paged with *---more---*; the manual's
list you can move about in and open with Return is not built. Use `/name` to go
into an array, a collection or a string.)

**`^`** switches the way a control character in a string is shown: as `?`, as it
always was, or as `^9` (a caret and the decimal number) after the first `^`; a
second `^` puts the `?` back. The length shown does not change.

**`window` *n*** sets the number of rows of the data area (messages and
replies) of the **full-screen** debugger, 5 to 15; the source above it takes
what is left. `window 3` is refused (*The data area must be 5 to 15 lines*) and
in line-by-line mode the command is a format error. A `window` *n* line in the
VOC record **`$debug.options`** (the record that already holds
`no.source.warning`) sets it at the first stop of a session.

**A stop at every `case` condition.** A program compiled for the debugger stops
before each `case` of a `begin case` is tried, so stepping by line shows the
condition being tried (`case x = 1`, then `case x = 2` when that was false) and
not only the statements of the case that was chosen. A condition and a
statement on one line are two elements of the line.

## Watching a variable

```
w m          stop when M changes
uw           stop watching
```

**A watch is the one thing that finds "who is setting this".** A watch set at
line 4, then `r`:

```
>W M

>R
 6:       k = 'some text'
Watched variable M has changed
Integer: 84
```

It ran on, and stopped **after** the line that changed `M`, telling you what it
changed to. That is the whole answer to the commonest hard bug in a long
program.

There is **one** watch at a time; `w` on another variable replaces it.

### Stopping only for a value

```
w n > 7
w s = stop
w code matches '3a0n'
```

`w` *variable* *operator* *value* stops only when the value just assigned meets
the condition; otherwise the program goes on and the debugger shows nothing.
The operators are `=` `#` `<` `>` `<=` `>=`, the words `eq` `ne` `lt` `gt` `le`
`ge`, and `matches`. A value in quotes is that text; a number compares as a
number and anything else as text. With `n` set to 1 to 10 in a loop, `w n > 7`
stops three times, for 8, 9 and 10.

A plain `w n` stops at every assignment as before, a new `w` replaces the old
watch **and its condition**, and `uw` clears both. An operator that is not in
the list, or no value after it, gives *Unrecognised command* and watches
nothing. `like` and `unlike` are not supported. The variable is found by its
number in the program that set the watch, so a condition on a local variable
works while that program is the one running.

## The call stack

```
stack
```

From inside a program run from the command prompt:

```
>STACK
1: /home/sd/user_accounts/don/bp.out/zzdbg @ 9
Command processor
```

The object path and the line, then whatever called it. From a program a
program can ask the same question without the debugger:

| | |
|---|---|
| `system(1002)` | the call stack as a dynamic array — one field per level |
| `system(1029)` | internal subroutine depth — `0` at the top, `1` inside a `gosub` |

## Full screen on a terminal, line by line everywhere else

**On a terminal that has an alternate screen — xterm and the terminals that
behave like it — the debugger takes the whole screen.** Its test is that the
session is a real terminal (SD can read its window size) and that the terminal
definition has `smcup` and `rmcup`. Then:

- the top row is the **title**: the program and the line about to run;
- below it is the **source**, with line numbers; the line about to run is
  highlighted and a line with a breakpoint has its number marked;
- then five lines of **messages** (what a command printed), and the **command
  line** at the bottom, where you type the commands on this page;
- **F1** shows the help in a box, **F4** shows the program's own screen until
  you press a key, and Page Up and Page Down move the source.

**The full-screen display is laid out for 140 columns by 42 lines or more**
(since 18 October 2026; a bigger window is used whole). **On a window smaller
than that the debugger does not refuse: it says why, once, and is line by line
for the session** — *The debugger needs a window of at least 140 columns by 42
lines for its full-screen display; this one is 100 by 30, so it is using line
mode* — because a small window is no reason to take away the way to debug a
program. The window measured is the one on the screen, or the display `term w,h`
gave if that is smaller. The choice is made at the first stop of a session.

If the window is made smaller **while the full-screen display is up**, the debugger
lays itself out again within a second and shows the **upper left corner** of its
140 by 42 layout and nothing past the edge, and draws everything again when the
window is made bigger. The command line is on the last row, so a window under 42
lines does not show where you type: the debugger then does not take keys. A
warning in reverse video fills the upper left, every key is thrown away, it goes
by itself when the window is big enough, and **Ctrl-Q, then y** leaves the
debugger the way F3 (Stop) does. A window narrower than 140 but 42 lines or more
high shows the left part of the lines and works as usual.

The program's own screen is kept by the terminal (that is what the alternate
screen is): when you let the program run, the debugger gives the terminal back
and the program's output is on its own screen, and it is on the alternate
screen again at the next stop. The colours are the screen library's: the
`classic` theme while the debugger is up if the program asked for none, and
whatever the program or the site chose otherwise.

**On a terminal with no alternate screen, and in a session that is not a
terminal, the debugger is line by line.** Every command works, as the
transcripts on this page show, and there is a real gain: because it is
line-oriented it can be **driven from a script**. A whole debugging session can
be fed down a pipe.

`@tty` reads empty in a piped session, and the debugger works there anyway.

(Until 13 October 2026 the full-screen display needed AccuTerm, which kept the
screen pictures; SD no longer supports AccuTerm.)

## Asking the AI

In the full-screen display, when the AI is on for your account (see
[Asking the AI](29b-sd-tcl-asking-the-ai.html)), the command **`AI`** — or `AI` and a question, such as
`ai why is y empty` — asks it about the stop. The AI is told the program and the line, the call stack
and about fifty lines of the source round the stop. As everywhere, **Enter shows everything that will
be sent first**, with Send and Cancel (the default); the answer is words in a box, and the debugger's
screen is drawn again after it. Nothing in your program or the debugger is changed, and a command in
the answer is ignored. Line mode and a phantom do not have it.

## Who has it

Read out of an account's own VOC:

| VOC entry | record | |
|---|---|---|
| `debug` | a `V` verb, `IN`, internal command 29 | run a program in debug mode |
| `debugging` | a `K` keyword, 53 | the compiler keyword |
| `pdebug` | a `V` verb, `CA $PDEBUG` | the phantom debugger |

**Every account has `debug` and `pdebug`** — there is no longer a tier that
would withhold them. `debugging` is a keyword rather than a verb, and always
was available regardless.

## What is not here

**`trace` is gone.** It was removed from the compiler in July 2024. In an
ordinary account it is *"Unrecognised statement"*.

**The programmatic debug statements are restricted.** `debug.on`,
`debug.off`, `debug.set`, `breakpoint` and `watch` are internal-only, and all
five are *"Unrecognised statement"* in an ordinary account. They are
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

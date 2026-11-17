Title: SD TCL - The Development Tools: tool.catalog and tool.test
Subtitle: The programs of the account and their catalogs, and the account's tests.

This page continues [SD TCL - The Development Tools:
tool.bulk](29c3-sd-tcl-tool-bulk.html).

## tool.catalog - the programs of the account

```
tool.catalog
```

**`tool.catalog`** lists the records of the account's program files, one row each, file by file and in name order. A program file is a directory file called `bp`, a file whose name ends in `.bp`, or a file that has a file of the same name and `.out` beside it (where the compiler puts the compiled programs). The page also lists the entries of the private and the local catalog that no program record accounts for, under the file name `(private)` or `(local)`, so that they can be taken out.

| column | what it says |
|---|---|
| File | the program file, or `(private)` / `(local)` for a catalog entry on its own |
| Program | the record's name (the entry's name for a catalog entry on its own) |
| Kind | `program`, `subroutine`, `function` or `class`, read from the compiled program; `include`, `screen` or `options` for a record that is not compiled by itself; `-` for a record not compiled yet |
| Compiled | when the compiled program was made |
| Object | the size of the compiled program in bytes |
| State | `current`: the source has not been changed since it was compiled; `stale`: the source's file is newer than the compiled program's, so B compiles it again; `?`: the page could not read one of the two times (the box says why); `-`: not compiled |
| Cataloged | where the program is cataloged under its own name: `private` (a record of the account's `cat` file; `(older)` or `(newer)` when it is a copy of another compile than the one in the `.out` file), `local` (a VOC entry that points at the compiled program; `as name` when the entry has another name), `global` (SDSYS's catalog has an entry of that name: the page only reports it, and cannot tell whether it is this program) |

The box under the list describes the row under the cursor: the paths of the source and of the compiled program, their sizes and times, current or stale, and the three catalogs in words. The line between the boxes shows the gate **bp-edit**, asked of the system, and the number of programs, compiled programs and catalog entries.

### What the keys do

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **B** | compile the program (`basic file name no.query`) and show the compiler's lines, errors and warnings, in a box |
| **C** | catalog it privately (`catalog file name no.query`): a copy of the compiled program goes into the account's `cat` file |
| **L** | catalog it locally (`catalog file name local no.query`): a VOC entry that points at the compiled program |
| **X** | take a local entry out **and delete the compiled program it points at** (`decatalog name`) |
| **D** | take a private or a local entry out (`delete.catalog name`, or `delete.catalog name local`); the compiled program stays. With both, the page asks which |
| **/** | show only the rows whose program or file name holds some text |
| Esc | clear the filter |
| F5 | read the programs and the catalogs again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**Every change goes through a box.** The box shows the exact command and what it does, and has two buttons, *Run* and *Cancel*; **Cancel is the one Enter chooses**. **X** and **D** then ask for the entry's name, typed; so does **C** or **L** when the program is already cataloged somewhere else under the same name, because `no.query` makes `catalog` take that other entry out without asking, and the box names it. The page adds `no.query` to `basic` and `catalog` because a question they would ask could not be shown on this screen; a source with a `$catalog` line is therefore cataloged by its compile without being asked about an entry of the same name elsewhere. What the verb says is what the status line shows. A compile that ran has its lines in a report box; a compile or command the verb refuses shows the refusal on the status line and nothing opens.

**Gates.** `basic`, `catalog`, `decatalog` and `delete.catalog` need the **bp-edit** gate (message 11408 from the verb). The page shows whether your session has it, asked of the system, warns in each box when it is off, and leaves the refusal to the verb; nothing changes then. The administrator always has the gate (the line says `on (administrator)`); for anyone else the administrator turns it on with `modify.account`. **X** is not run on a local entry whose pointer leads outside your account: `decatalog` deletes the file the entry points at without asking whether the account may reach it, so the page says which command to type instead. `catalog` looks for an entry of the same name by name: the box names a local entry of that name even when it points at another program, and asks for the name typed. **Global cataloging is the administrator's own command and is not offered here**; a global entry is shown, never changed.
**A name the page does not give to a command.** Only names of letters a-z, digits, dot, dash and underscore that begin with a letter or a digit are put into a command (a name beginning with a dot, dash or underscore would be read by the verbs as a global name). A record with a capital, a `$` or another character, or called like an option of the verbs (`local`, `global`, `pcode`, `no.query` ...), is listed and described, and the page says which verb to type, or that it must be renamed.

**Stale.** The page reads the modification times of the source and of the compiled program, which are operating-system files; it asks the account's OS gate about each path first and shows `?` with the reason if the gate refuses. The shared account's programs and programs in other accounts' files are not listed.

## tool.test - the tests of the account

```
tool.test
```

**`tool.test`** is the test runner for the programs of the account. It lists the **tests** - BASIC programs whose record id starts with `test.` in one of the account's program files - runs them, and says for each whether it passed, failed or gave no verdict. It needs a window of 140 columns by 43 lines or more.

### What a test is

A test is a program whose record id starts with `test.` (`test.sort`, `test.invoice.totals`) in a program file of the account: `bp`, a file whose name ends `.bp`, or a directory file with a file of the same name and `.out` beside it (the place the compiler puts the object code). The program prints what it checks, and the **last non-empty line it prints** says how it went:

```
3 passed, 0 failed
```

A name and a colon may come first (`mytest: 12 passed, 0 failed`). The page runs the test with `run FILE ID` and judges that line:

| the last non-empty line | the page says |
|---|---|
| `N passed, 0 failed`, with N above 0 | **pass** |
| `N passed, M failed`, with M above 0 | **fail** |
| the run **aborted** (an error stopped the program) | **fail**, and the box gives the abort message |
| anything else: no such line, nothing printed at all, `0 passed, 0 failed` | **no verdict** |

### The list

| column | what it says |
|---|---|
| Test | the record id of the program |
| Program file | the file it is in |
| Object | `yes` when its object code is in the `.out` file beside the program file |
| Result | `pass`, `fail`, `fail: abort`, `no verdict`, `not run` (not run yet in this session), `no object` (cannot be run until it is compiled), `by hand` (a name the page does not give to a command), or `running` |
| Passed, Failed | the numbers in the last line |
| Secs | whole seconds the run took |
| Ran | the time of day it finished |
| Lines | how many lines it printed |

The line between the boxes counts the results of the session and shows the **bp-edit** gate your session holds, asked of the system. The box under the list describes the test under the cursor: its result in words, the command that ran, and the end of what it printed.

### What the keys do

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **R** | run the test under the cursor |
| **A** | run every test shown, one after another, in the order shown, after a box that gives the number and the first commands (Cancel is what Enter chooses); **Esc** stops after the test that is running |
| **F** | run again the tests that failed (an abort counts as a fail), after the same box |
| **B** | compile a test that has no object code: `basic FILE ID`, after a box that shows the command (Cancel is what Enter chooses) |
| **Enter**, F6 or Shift-F6 | show what the test printed in the lower box, which then has the keyboard (`[*]`), scrolling with Up, Down, PgUp, PgDn, Home and End; **Esc**, F6 or Shift-F6 comes back to the list (F6 by way of the AI line when the AI is on for your account) |
| **/** | show only the tests whose name or program file holds some text; **Esc** clears it |
| F5 | read the program files again (the results are kept) |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

### How a test is run

R, A and F run `run FILE ID` through the toolkit's command runner, which lets through only the words `run` and `basic` and names made of letters a-z, digits, dot, dash and underscore. **A and F ask first**, because one key starts up to 500 programs, some of which another member of a group account may have put in a shared program file; **R**, one test, is the same as typing `run FILE ID` and has no box. The page changes nothing itself: the test is the account's own object code, run as typing the command would, and it needs no `sh` and no `os` gate. (What a test does to the account's files is what the program does.) A test with no object code is not run: **B** compiles it, which needs the **bp-edit** gate; without it the compiler's own refusal is shown on the status line and nothing is compiled.

What a test prints is collected, not shown. Only the first 360 and the last 39 lines of a very long output are kept (the result says so), but the verdict is judged on all of it. A test that **asks for input** is given 50 empty answers instead of waiting, the leftovers are thrown away, and the result says how many it used. The system throws away what a program printed if it **aborts**, so an aborted test shows 0 lines and the box gives the abort message instead (for example `Unassigned variable X at line 2 of ...`).

### No time limit

BASIC has no time limit for a program and the page has none either: a test that does not end waits for ever. The page turns the break key on while a test runs, so **Ctrl-C and then Q** at the prompt SD shows (`A to abort, Q to Quit, G to continue, X to exit`) stops it and gives the page back; the break key is turned off again afterwards. A test stopped this way shows as *no verdict*, as a test that printed nothing does.

### Limits

- Results live in memory for the session and are written nowhere. The first 500 tests are listed.
- A name with a capital, an ampersand or a dollar is listed as `by hand`; the page says which command to type.
- A test that catches an error of its own and prints nothing is also told as an abort.
- The shared account's programs are not in your VOC as files, so its tests are not listed.

Title: Migrating to SD: mode words
Subtitle: Every name that $mode accepts, and the lines of a $basic.options record.

This page continues [Migrating to SD](15-migrating-to-sd.html). A mode changes how **one
program** is compiled: `$mode` *name* `{, name ...}` in the source, or a `mode` line in
a `$basic.options` record. **All are off unless asked for.** A name SD does not have stops the
compile with *Unrecognised mode name*; `$mode default` turns every mode off, `$mode -name` one.
Seven names that existed to imitate other products were removed on 27 October 2026 and are
refused now: `conditional.statements` (it did nothing: the file statements may always be the
condition of `while` and `until`), `exception.save.stack` (write `saving.stack` on the `catch`),
`implied.stop` (end a program with `stop`), `no.case.invert` (give `input` the `nocaseinvert`
clause), `optional.then.else` (a `read` takes a `then` or an `else`), `prclose.default.0`
(`printer close on` *unit*) and `unassigned.common` (a common variable starts as zero).
The last column names the page of the User set that also describes the word; **here** means this
page is where it is described. Some modes also work at the start of an I-type, which is
described in *SD Dictionaries - Formats and Expressions*.

## Searching and reading

| mode | what it does | also described in |
|---|---|---|
| `uv.locate` | the `locate` of UniVerse: the array reference names the item that holds the list, so `a` searches the fields, `a<f>` the values of field f and `a<f,v>` the subvalues; it may be left out, and a start position may follow it after a comma. Without the mode the reference is required and says where the search starts | here |
| `string.locate` | an `ar` or `dr` locate no longer compares numbers as numbers: the values are compared as right-aligned text, so a list holding -5, 3 and 10 is in order as numbers but not as text | here |
| `composite.readnext` | `readnext` on a list made with `by.exp` returns the whole entry (the id followed by the positions the list carries) instead of the id alone | here |
| `pick.read` | `read`, `readu`, `readl`, `readv`, `readvu` and `readvl` leave the variable as it was when the record is not found, instead of making it null | here |
| `pick.readnext` | a `readnext` that takes its `else` leaves the id variable as it was | *SD Basic - Program Structure* |
| `selectv` | `select` builds a select list variable, as `selectv` does, and the list variable is optional | *SD Basic - Select Lists* |
| `pick.select` | `selectv` moves an active default select list to the variable instead of making a new selection | *SD Basic - Program Structure* |
| `execute.clearlist` | the default select list is cleared before each `execute`, unless it has a `passlist` clause | *SD Basic - Program Structure* |
| `stdfil` | the default file variable: `open`, `read`, `write`, `delete`, `select` and the other file statements may be written without naming a file variable | *SD Basic - Program Structure* |
| `stdfil.shared` | `stdfil` with one variable for the whole command level, shared by a program and the subroutines it calls | *SD Basic - Program Structure* |
| `open.fail.zero.fvar` | a failed `open` or `openpath` leaves 0 in the file variable, not an unassigned one | *SD Basic - Program Structure* |
| `write.delete.then.else` | `write`, `writeu`, `matwrite`, `matwriteu`, `delete` and `deleteu` take `then` and `else`; a trigger that refuses a write takes `else` | *SD Basic - Program Structure* |
| `autolock` | `write`, `matwrite` and `delete` lock a record they do not already hold a lock on, for that statement. Not recommended: it hides the explicit locking SD's own programs use | *SD Basic - Program Structure* |
| `non.durable.txn` | a `commit` of a nested transaction writes nothing but hands its records, deletions and locks to the enclosing transaction | *SD Basic - Locks and Transactions* |

## Strings and names

| mode | what it does | also described in |
|---|---|---|
| `pick.substr` | a substring assignment whose region starts beyond the end of the string pads the string with spaces to reach it; without the mode it does nothing | here |
| `pick.substr.assign` | the region is replaced by the whole value whatever its length, and a negative start puts the value in front followed by that many spaces; overrides `pick.substr` | here |
| `compatible.append` | appending with `<-1>`, `ins` or `insert()` to a string that already ends with the mark the append would add does not add a second one | here |
| `pick.convert` | `convert(string, from, to)` in place of `convert(from, to, string)`, from the line where the mode is turned on | *SD Basic - Program Structure* |
| `count.overlap` | `count` and `counts` find overlapping occurrences: `aa` in `aaaaaaaaa` is found 8 times, not 4 | *SD Basic - Program Structure* |
| `index.overlap` | `index` and `indexs` count overlapping occurrences when finding the nth | *SD Basic - Program Structure* |
| `change.no.overlap` | `change`, `ereplace` and `swap` given a starting occurrence pass over the earlier occurrences whole, not one character at a time | *SD Basic - Program Structure* |
| `case.sensitive` | names of variables and labels are case sensitive: `abc` and `ABC` are two variables, `lab:` and `LAB:` two labels | here |

## Program flow

| mode | what it does | also described in |
|---|---|---|
| `for.store.before.test` | `for` stores the new value of the loop variable before it tests the end condition, so after `for i = 1 to 3` the variable holds 4 | here |
| `pick.jump.range` | `on ... goto` and `on ... gosub` with an index out of range go on to the next statement, instead of jumping to the last label | here |
| `pick.enter` | `enter` hands control to the named program for good, casting off the programs that called it down to the command processor. Without the mode `enter` is a `call` | here |
| `optional.final.end` | no warning when the final `end` is missing | here |
| `partial.expressions` | `a and b` and `a or b` stop evaluating as soon as the answer is known | *SD Basic - Program Structure* |
| `default.unass.args` | an argument with a default value takes it also when the caller passed the argument unassigned | *SD Basic - Program Structure* |

## Declarations and compiler warnings

| mode | what it does | also described in |
|---|---|---|
| `pick.matrix` | matrices have no zero element: `m(0)` is out of range | here |
| `explicit` | every scalar must be named in a `dim` before it is used, or the compile fails with *Variable x has not been declared* | *SD Basic - Program Structure* |
| `trap.unused` | the compiler warns of a variable that is given a value and never used | here |
| `trap.unused.main` | as `trap.unused`, but only for variables given a value in the program itself, not in an include record | *SD Basic - Program Structure* |
| `strict.equate` | warns when `equate` or `$define` gives a name that is also a statement or function name | here |
| `debug.equates` | an object compiled for the debugger also keeps its `equate` and `$define` tokens | *SD Basic - Debugging* |

## Terminal, printer and time

| mode | what it does | also described in |
|---|---|---|
| `heading.no.eject` | `heading` behaves as `heading no.eject`: setting a heading does not start a new page | here |
| `no.echo.data` | an `input` that takes its answer from the data queue does not echo it | here |
| `time.ms` | `time()` returns the seconds since midnight to the millisecond, with a fraction | *SD Dictionaries - Formats and Expressions* |

## The `$basic.options` record

A record named `$basic.options`, whose first line is `x`, gives every program compiled from
one file its defaults. SD looks first in the file that holds the source and, failing that, in
the VOC; the first one found is used. One entry to a line.

| line | what it does | also described in |
|---|---|---|
| `catalogue` {`local`\|`global`} {`no.query`} | a program that compiles with no errors is catalogued under its own name, as the `catalog` verb would, in the mode given; `no.query` leaves out the question about replacing. `catalog` is accepted too | here |
| `no.catalogue` | cancels an earlier `catalogue` line | here |
| `define` *name* {*value*} | defines a token as `$define` does, for `$ifdef` and for use in the source; the value is a number or a quoted string | here |
| `debugging` | every program is compiled for the debugger | here |
| `include` *file* *record* | an automatic `$include` of the record at the top of every program; line numbers stay as written | here |
| `listing` | writes a listing of each program, in the object file, in a record named after the program with `.LIS` added | here |
| `xref` | as `listing`, with a cross reference of the variables and labels | here |
| `noxref` | leaves the cross-reference tables out of the object code, so a run-time error names the program but no line | here |
| `mode` *names* | modes for every program: the names of `$mode`, comma separated, `-name` to turn one off | here |
| `nocase.strings` | every program compiles with case-insensitive string operations, as `$nocase.strings` does | here |
| `search` *files* | the files an `$include` with no file name looks in, in order; `@` is the file the source is in | *SD Basic - Program Structure* |
| `warnings.as.errors` | a compiler warning counts as an error | here |

Title: Migrating to SD: mode words
Subtitle: Every name that $mode accepts, and the lines of a $basic.options record.

This page continues [Migrating to SD](15-migrating-to-sd.html). A mode changes how **one
program** is compiled: `$mode` *name* `{, name ...}` in the source, or a `mode` line in
a `$basic.options` record. **All are off unless asked for.** A name SD does not have stops the
compile with *Unrecognised mode name*; `$mode default` turns every mode off, `$mode -name` one.
Seven names that existed to imitate other products were removed on 27 October 2026 (and an eighth, below) and are
refused now: `conditional.statements` (it did nothing: the file statements may always be the
condition of `while` and `until`), `exception.save.stack` (write `saving.stack` on the `catch`),
`implied.stop` (end a program with `stop`), `no.case.invert` (terminal case inversion is gone altogether), `optional.then.else` (a `read` takes a `then` or an `else`), `prclose.default.0`
(`printer close on` *unit*) and `unassigned.common` (a common variable starts as zero). An eighth, `pick.enter`, went the same
day with the `enter` statement it switched on (use `call`, or `chain` to hand control on for good).
Three more went later that day, each doing without the mode what it did with the mode off: `execute.clearlist`
(the default select list is no longer cleared before an `execute`; `clearselect 0` does it), `open.fail.zero.fvar`
(the file variable of a failed `open` stays unassigned) and `pick.readnext` (a `readnext` that takes its `else`
sets the id variable to the null string).
Twenty-two more went on 27 October 2026, each doing without the mode what it did with the mode off, and are refused now: `string.locate`, `composite.readnext`, `pick.read`, `selectv`, `pick.select`, `stdfil`, `stdfil.shared`, `write.delete.then.else`, `autolock`, `pick.substr`, `pick.substr.assign`, `compatible.append`, `pick.convert`, `count.overlap`, `index.overlap`, `change.no.overlap`, `case.sensitive`, `for.store.before.test`, `pick.jump.range`, `optional.final.end`, `pick.matrix` and `heading.no.eject` (for the last, write `heading no.eject`; the others have no replacement, because the behaviour they switched on is not offered at all). `selectv` is still a statement: `selectv` *file* `to` *var*.
The last column names the page of the User set that also describes the word; **here** means this
page is where it is described. Some modes also work at the start of an I-type, which is
described in *SD Dictionaries - Formats and Expressions*.

## Searching and reading

| mode | what it does | also described in |
|---|---|---|
| `uv.locate` | the `locate` of UniVerse: the array reference names the item that holds the list, so `a` searches the fields, `a<f>` the values of field f and `a<f,v>` the subvalues; it may be left out, and a start position may follow it after a comma. Without the mode the reference is required and says where the search starts | here |
| `non.durable.txn` | a `commit` of a nested transaction writes nothing but hands its records, deletions and locks to the enclosing transaction | *SD Basic - Locks and Transactions* |

## Program flow

| mode | what it does | also described in |
|---|---|---|
| `partial.expressions` | `a and b` and `a or b` stop evaluating as soon as the answer is known | *SD Basic - Program Structure* |
| `default.unass.args` | an argument with a default value takes it also when the caller passed the argument unassigned | *SD Basic - Program Structure* |

## Declarations and compiler warnings

| mode | what it does | also described in |
|---|---|---|
| `explicit` | every scalar must be named in a `dim` before it is used, or the compile fails with *Variable x has not been declared* | *SD Basic - Program Structure* |
| `trap.unused` | the compiler warns of a variable that is given a value and never used | here |
| `trap.unused.main` | as `trap.unused`, but only for variables given a value in the program itself, not in an include record | *SD Basic - Program Structure* |
| `strict.equate` | warns when `equate` or `$define` gives a name that is also a statement or function name | here |
| `debug.equates` | an object compiled for the debugger also keeps its `equate` and `$define` tokens | *SD Basic - Debugging* |

## Terminal, printer and time

| mode | what it does | also described in |
|---|---|---|
| `no.echo.data` | an `input` that takes its answer from the data queue does not echo it | here |
| `time.ms` | `time()` returns the seconds since midnight to the millisecond, with a fraction | *SD Dictionaries - Formats and Expressions* |

## The `$basic.options` record

A record named `$basic.options`, whose first line is `x`, gives every program compiled from
one file its defaults. SD looks first in the file that holds the source and, failing that, in
the VOC; the first one found is used. One entry to a line.

| line | what it does | also described in |
|---|---|---|
| `catalog` {`local`\|`global`} {`no.query`} | a program that compiles with no errors is catalogued under its own name, as the `catalog` verb would, in the mode given; `no.query` leaves out the question about replacing | here |
| `no.catalog` | cancels an earlier `catalog` line | here |
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

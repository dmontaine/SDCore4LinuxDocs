Title: SD Basic - Program Control
Subtitle: Conditions, loops, jumps, and handing control to another program or to the command processor.

This page covers the statements that decide what runs next: conditional
execution, loops, jumps, and the several ways one program starts another.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## Conditions

```
if expression then statement {else statement}

if expression then
   statements
end else
   statements
end
```

The single-line and block forms can be mixed — `then` on one line and `end
else` opening a block is legal — but a block that starts on one line must end
with `end` before the `else`.

**An empty branch still needs a statement.** Use `null`:

```
read rec from f, id then null else stop 'missing'
```

> **`and` and `or` have the same precedence and are applied left to right.**
> `a or b and c` means `(a or b) and c`, not `a or (b and c)`. This is not what
> C, Python, Java or SQL do, and it is the single most common way a condition
> in ported code changes meaning. **Parenthesise anything that mixes them.**
> The full precedence table is in [SD Basic - Math Functions](03-sd-basic-math-functions.html).

### `begin case`

```
begin case
   case expression
      statements
   case expression
      statements
   case 1
      statements
end case
```

**The first matching case runs and the rest are skipped** — with two
identical `case n = 2` branches, only the first executes. There is no
fall-through and no `break`.

`case 1` is the conventional default, because the constant 1 is always true.
If no case matches and there is no default, nothing runs.

## Loops

### Counted

```
for variable = start to limit {step increment}
   statements
next variable
```

| Loop | Values taken |
|---|---|
| `for i = 1 to 10 step 3` | `1 4 7 10` |
| `for i = 1 to 2 step 0.5` | `1 1.5 2` |
| `for i = 3 to 1` | **none — the body never runs** |

**The limit is tested before the first pass**, so a loop whose start is
already past its limit does nothing rather than running once. A fractional
`step` is allowed, but a fractional step that cannot represent the limit
exactly may stop one iteration early — count with integers and scale if it
matters.

`step` may be negative, in which case the loop runs while the variable is
greater than or equal to the limit.

### Conditional

```
loop
   statements
while expression
   statements
repeat
```

`while` continues the loop when the expression is true; `until` continues when
it is false. Either may appear anywhere in the body, more than once, and a
`loop` with neither runs until something in the body leaves it.

`loop / k += 1 / r := k / while k < 3 / repeat` produces `1 2 3` —
the test happens where it is written, so the body before it always runs at
least once.

```
continue
exit
```

`continue` starts the next pass; `exit` leaves the loop. Both apply to the
innermost loop only.

## Jumps

```
goto label
go to label
gosub label
return
return to label
```

Labels end with a colon at their definition and are written without one in the
jump. A label must be in the same program.

### `on ... goto` and `on ... gosub`

```
on expression goto label1, label2, label3
on expression gosub label1, label2, label3
```

Jumps to the *n*-th label, counting from 1.

> **An out-of-range value does not fall through — it is clamped to the nearest
> end.** This is the opposite of what most MultiValue documentation says. On
> this port, with two labels:
>
> | Expression | Where it went |
> |---|---|
> | `on 0 goto a1, a2` | **label 1** |
> | `on 3 goto a1, a2` | **label 2** |
> | `on -1 goto a1, a2` | **label 1** |
>
> **So there is no "none of the above" branch.** A value of zero — which is
> what an empty or non-numeric variable evaluates to — silently runs the first
> case. **Range-check the expression yourself before the statement**, or use
> `begin case`, which has a real default.

## Stopping

```
stop {message}
abort {message}
quit
```

| | |
|---|---|
| `stop` | ends the program and returns to whatever called it |
| `abort` | ends the program **and everything that called it**, returning to the command processor |
| `quit` | leaves the current command level |

`set.exit.status value` sets the value a caller can read, which is how a
program run from a script reports success or failure.

## Exceptions: `try`, `catch` and `throw`

```
try {statement}
   statements
catch name {, name ...} {dumping} {saving.stack}
   statements
{catch name ...
   statements}
end

throw name {, data}
caught(name {, modes})
```

`throw` gives up the statements it is in, and every `gosub` and `call` between
it and the nearest `try` that has a `catch` for the name, and carries on in that
`catch` clause. If the `try` clause finishes without a throw, the `catch`
clauses are skipped. A name is not case sensitive and may be up to 63
characters. Names beginning `SYS.` and names containing `$` are SD's: use
neither for your own.

```
try
   call process.account(id)
catch account.invalid
   display 'Account ' : id : ' is not valid'
end
```

**Names are paths, and a `catch` takes everything below the name it writes.**
`catch account` takes `account.invalid` and `account.invalid.closed`; `catch
account.invalid` takes `account.invalid.closed` but not `account`; `catch acc`
takes neither, because a name is compared a whole component at a time. When
one `try` has several clauses, the first that covers the name is the one used,
in the order written. Put the specific name before the group:

```
catch account.invalid.closed
   ...
catch account
   ...
```

| | |
|---|---|
| `catch sys$any` | takes any exception no earlier clause named |
| `catch sys$unhandled` | takes one that no `try` anywhere up the stack names, and no `sys$any` takes either |

**What the clause can read:**

| | |
|---|---|
| `@exception` | the name as it was thrown (its case too) |
| `@exception.data` | the second argument of `throw`; for a run time error, the message |
| `@exception.origin` | the program (its object path), a field mark and the line the exception was thrown from, or -1 where the program has no line table |
| `@exception.stack` | the call stack as `system(1002)` gives it, innermost first; filled only when the clause says `saving.stack` |

`dumping` makes a process dump file, showing the call stack as it was, before the
stack is unwound.

`caught(name, modes)` is 1 if a `throw` of that name from here would find a
handler. *modes* adds the special handlers: 1 for `sys$any`, 2 for
`sys$unhandled`, 3 for both; with 0 or nothing only a handler that names it, or a
group above it, counts.

**A transaction begun inside the `try` clause and still open when the exception
leaves it is rolled back.** One that was already open when the `try` was
entered is left alone, and carries on. Locks taken inside the rolled back
transaction go with it.

**Limits, and what it will not do:**

- Up to 64 `try` constructs may be active at once. Leaving a `try` clause by
  `goto`, `exit` or `continue` is not allowed; the handler stays until its
  program level returns. A `return` from a `gosub` or a `call` made inside the
  clause is fine.
- A throw does not reach past an `execute`, a trigger, a recursive call or a
  dictionary expression. Thrown inside one and not handled inside it, it is
  unhandled there: the program aborts as a run time error does, with the
  message `Unhandled exception name`.
- A `throw` inside a `catch` clause goes to the `try` outside it.

### Run time errors as exceptions

Many errors that would abort the program are thrown as exceptions in the `SYS`
group, so a program can deal with them where it chooses:

```
zz = 0
try
   y = 1 / zz
catch sys.program.div_zero
   display 'Zero: ' : @exception.data
end
```

When nothing can catch the exception (no `try` for it, or one the throw cannot
reach) **the error aborts exactly as it always did, with the same message**. When
something does catch it, nothing is displayed, logged or dumped; the message is
the `@exception.data` and also `@abort.message`. `catch sys` takes every system
exception, `catch sys.program` the ones in that group, and so on down.

| Name | The error |
|---|---|
| `sys.program.datatype.unassigned` | an unassigned variable was used |
| `sys.program.datatype.not_numeric` | a non-numeric value where a number is needed |
| `sys.program.datatype.invalid` | data of the wrong type for the operation (also a value that cannot be a string) |
| `sys.program.datatype.not_file` · `not_matrix` · `not_image` · `not_object` · `not_socket` · `not_sort` · `not_collection` | a variable that is not a file, matrix, screen image, object, socket, sort or data collection |
| `sys.program.datatype.null_string` | a null string where one is not allowed |
| `sys.program.div_zero` | divide by zero |
| `sys.program.invalid_matrix_index` | a subscript out of range |
| `sys.program.invalid_matrix_size` | an argument matrix too small for the subroutine |
| `sys.program.invalid_argct` | the wrong number of arguments in a `call` |
| `sys.program.invalid_call_name` | a call name that cannot be a program name |
| `sys.program.not_found` | the subroutine is not in the catalog, or cannot be loaded |
| `sys.program.load_error` · `load_error.read_error` | object code that is damaged or cannot be read |
| `sys.program.invalid_data_size` | a string or element over its limit |
| `sys.program.invalid_in_txn` | a file operation a transaction does not allow |
| `sys.program.not_txn` | `end transaction` with none open |
| `sys.program.range` · `invalid_key` · `invalid_name` · `invalid_itype` · `resize_error` | a value out of range for the function; an unknown key; a bad collection element name; a bad I-type; a failed resize |
| `sys.program.limit.gosub_depth` · `call_depth` · `max_breakpoints` | `gosub`s or `call`s nested too deeply; too many breakpoints |
| `sys.program.is_class` | a class module used as an ordinary program |
| `sys.program.no_pdebug` | a phantom reached the debugger and no `pdebug` is waiting (below) |
| `sys.locks.deadlock` · `limit` · `task_lock.invalid` | a deadlock; the `maxrlock` limit; a bad task lock number |
| `sys.filesys.invalid_file_type` · `invalid_record_id` · `lock_required` | the wrong kind of file for the statement; a bad record id; a write in a transaction with no lock on the record |
| `sys.filesys.creation_error` · `open_error` · `io_error` · `permissions.read_only` · `trigger` | a file that cannot be made, opened, read or written; a read only file; a trigger that cannot be run |
| `sys.printer.invalid_unit` · `invalid_key` · `invalid_operation` · `invalid_region` · `io_error` | print unit and screen errors |
| `sys.select.invalid_list_no` | a select list number out of range |
| `sys.sort.invalid_key_count` · `invalid_operation` · `io_error` | sort errors |
| `sys.kernel.no_memory` | out of memory |

**Not every error has a name.** An error with no row here still aborts, whatever
handlers there are, and a few that could be caught are left alone on purpose:
the failure of a transaction's commit, and the refusal of a path or an operating
system command by the account's gates. **Catching an error does not undo what
caused it**: a refused operation stays refused, and a write that failed has not
been made.

**A phantom that reaches the debugger with no one to debug it** (a `debug`
statement, say, with no `pdebug` command waiting for it) normally ends. If
the program has a handler for `sys.program.no_pdebug`, for a group above it,
for `sys$any` or for `sys$unhandled`, the exception is thrown instead, with
the message "Phantom debugger not active", and the phantom goes on from the
handler.

## Running something else

```
execute expression {capturing variable} {returning variable} {passlist variable} {rtnlist variable} {stacklist}
chain expression
```

| | |
|---|---|
| `execute` | runs a command **at a new level**; the current program resumes afterwards |
| `chain` | replaces the current program; **nothing comes back** |

`execute 'WHO' capturing cap` puts the command's output in `cap`
rather than on the screen, one field per line — `dcount(cap, @fm)` is `1` for
a single-session `WHO`.

**A command that does not exist is not an error you can catch.**
`execute 'ZZNOSUCHVERB' capturing out` completes, and `@system.return.code`
reads **-1**. The program carries on. **Test `@system.return.code` after any
`execute` whose command name came from data.**

| clause | |
|---|---|
| **capturing** *var* | the command's output goes to *var* instead of the terminal |
| **returning** *var* | error messages go to *var* |
| **passlist** *var* | the select list held in *var* (made by `formlistv`, `getlistv`, `selectv` and the like) becomes the command's default select list. The variable is always named: `passlist` alone is refused |
| **rtnlist** *var* | the command's select list comes back |
| **stacklist** | the default select list is kept as it was, the place `readnext` had reached included, and put back when the command returns. The command is given the list as usual and may read, change or replace it. It cannot be combined with **passlist** or **rtnlist** (the compiler refuses it) |

Without **stacklist**, whatever the command leaves in the default select list
is what the program finds afterwards. Note that a `select` command that
meets an active list selects *from that list* (an intersection): a command that
means to replace the list must `clear.select` first.

> **`chain` discards unnamed common.** (The option `chain.keep.common`, which
> kept it, was removed in 1.2-0: pass what the next program needs in named common
> or in the data queue.)

## Waiting

```
sleep {seconds}
nap milliseconds
pause {timeout}
wake user.number
```

| | |
|---|---|
| `sleep` | wait a number of seconds, or until a time of day |
| `nap` | wait a number of **milliseconds** |
| `pause` | wait until another process calls `wake`, or until the timeout expires |
| `wake` | release a process that is paused |

`pause` and `wake` are how two SD sessions coordinate without polling. The user
number `wake` needs is the one `@userno` reports in the waiting process.

## Interrupting

```
break {key} {on | off}
break {key} clear
set.break.handler name
remove.break.handler
```

`break off` prevents the user interrupting the program; `break on` restores it.
**Every `break off` needs a matching `break on`** — they nest, and a program
that aborts between the two leaves the session with interrupts disabled.

`set.break.handler` names a subroutine to run instead of entering the debugger,
which is how a program cleans up rather than dying at an arbitrary point.

> **`break off` around a whole program is a trap, not a safety measure.** It
> also disables the interrupt during any `execute` the program performs, so a
> runaway query started from inside it cannot be stopped either. Turn it off
> around the critical section — the write, the transaction — and back on
> immediately.

## Doing nothing

```
null
rem text
* text
```

`null` is a statement that does nothing, for branches that must be present but
empty. `rem` and a leading `*` are comments; so is anything after
`;*` on a line.

**`rem` is also a function.** `rem(a, b)` is the remainder — see
[SD Basic - Math Functions](03-sd-basic-math-functions.html). The compiler tells them apart by the bracket: a
`rem` immediately followed by `(` is the function, anything else is a comment.
**`rem (a + b) is wrong` is a comment**, and `x = rem (a, b)` is a syntax
error, because the space changes what it is.

## What is not here

These existed in OpenQM or earlier SD releases and **are not in SD Core**
(checked directly in `bcomp`'s own statement table, shared source with SD
Core for Windows). A program using one will not compile.

| | |
|---|---|
| `aborte` · `abortm` | abort with a message number or text |
| `stope` · `stopm` | stop with a message number or text |
| `rsd` | |
| `enter.package` · `exit.package` · `package` | |
| `trace` | |
| `errmsg` | |
| `procread` · `procwrite` · `@pib` · `@sib` · `@pob` · `@sob` | the PROC interface |

**`errmsg` is not in the compiler's statement table, and has not been since
July 2024.** `errmsg 1000` is rejected with *"Unrecognised statement"*, the
same message as for any word the compiler does not know (`foobarbaz 1000` gets
it too). An earlier version of this page said the name was still in the table
with nothing behind it. That was wrong: `BCOMP` removed the table entry on
28 July 2024 and left the name only in a comment beside the line that was
changed, and a tool that read the table by matching quoted names picked it up
from the comment.

`procread` and `procwrite` are gone as well, with the PROC language they
served, and so are the variables `@pib`, `@sib`, `@pob` and `@sob`. A program
using one will not compile. (The 1.2-0 programme removed them; earlier versions
of this page said they compiled.)

## See also

[SD Basic - Program Structure](01-sd-basic-program-structure.html) · [SD Basic - Math Functions](03-sd-basic-math-functions.html) ·
[SD Basic - File Handling](07-sd-basic-file-handling.html) · [SD Basic - Select Lists](08-sd-basic-select-lists.html).

Title: SD Basic - Program Structure
Subtitle: Programs, subroutines and functions; variables, matrices, common blocks and how a program is called.

This page covers the shape of an SD BASIC program: how it is declared, how it
is called, what its variables are, and the declarations that have to appear
before anything else.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## The three kinds of program

```
program {name}
subroutine name {(argument, ...)} {var.args}
function name {(argument, ...)} {var.args}
```

| | |
|---|---|
| **program** | runs on its own. Started by `run`, by its catalogued name, or from another program with `execute` |
| **subroutine** | called by `call`, and returns nothing. Its arguments carry values back |
| **function** | called inside an expression, and returns a value with `return` |

A source record with no declaration at all is a program. `end` closes it.

```
program hello
   print 'hello'
end
```

**`var.args`** allows the caller to pass fewer arguments than are declared;
`arg.count()` then says how many actually arrived, and reading one that was not
passed is an unassigned-variable error rather than a silent empty string.

### Local subroutines and functions

```
local subroutine name {(arguments)}
local function name {(arguments)}
```

These live inside the program that uses them rather than in the catalogue, and
they can declare `private` variables of their own — which is how you get a
routine whose working variables do not collide with the rest of the program.

**They are not called the way external ones are.** A local subroutine is
reached with `gosub name(…)` and not `call`; a local function must be declared
with `deffun … local` before it is used; and both need an explicit `return`,
because falling into the closing `end` stops the program. All of that, with the
scope rules and the errors each mistake produces, is on
[SD Basic - Modern Program Structure](18-sd-basic-modern-program-structure.html).

### Internal subroutines

```
gosub label
...
label:
   ...
   return
```

`gosub` is not a call to another program — it jumps within the current one, and
shares all its variables. The nesting limit is **256 levels**.

## Calling

```
call name {(argument, ...)}
call @variable {(argument, ...)}
subr(name {, argument, ...})
```

| | |
|---|---|
| `call name` | the name is fixed at compile time |
| `call @variable` | the name is taken from the variable at run time |
| `subr()` | the function form — use it where you want the result in an expression |

**Arguments are passed by reference, not by value.** A subroutine that
assigns to one of its parameters changes the caller's variable. That is how a
subroutine returns anything at all, and it is also how a subroutine that uses a
parameter as scratch space quietly corrupts its caller's data. **If you do not
intend to return a value through an argument, copy it into a local variable
first.**

Passing an expression rather than a variable — `call sub(a + 0)` — forces a
copy, because there is no variable to write back to.

```
catalogued(name)
```

reports whether a name can be called. `catalogued('ZZNOSUCH')` is
`0`. Use it before a `call @variable` whose name came from data, because an
uncatalogued name is a runtime abort rather than a testable failure.

## Variables

Variables are not declared and have no type. A variable holds whatever was last
assigned to it, and its type follows the value.

```
assigned(variable)
unassigned(variable)
vartype(variable)
```

| Expression | Result |
|---|---|
| `assigned(neverset)` | `0` |
| `assigned(zz)` after `zz = 1` | `1` |
| `unassigned(neverset)` | `1` |

**The compiler warns about a variable that is never assigned** — *"WARNING:
NEVERSET is not assigned a value"* — but it still compiles, and using the
variable is an error only when the line is reached.

### `vartype()`

Returns the internal type code:

| Value | Code | |
|---|---|---|
| unassigned | `0` | |
| an integer | `2` | |
| a floating-point number | `3` | |
| a string | `5` | |

The remaining codes exist for things a program does not usually inspect: `1`
address, `4` subroutine reference, `6` file variable, `7` array, `8` common
block, `9` image, `11` select list, `13` socket, `15` object.

> **`vartype()` tells you how the value is held, not what it means.** `'12'`
> read from a file is a string (`5`) even though it is a number everywhere it
> is used; the same value after arithmetic is an integer (`2`). **Use `num()`
> to ask whether something is numeric** — see [SD Basic - Math Functions](03-sd-basic-math-functions.html) —
> and keep `vartype()` for telling an unassigned variable from an empty one.

`set.unassigned` returns a variable to the unassigned state, which is how you
make `assigned()` false again after using it.

## Constants

```
equate name to value
equ name to value
```

`equate` is resolved at compile time and costs nothing at run time. It can name
a literal, another variable, or a matrix element:

```
equate true to 1
equate esc to char(27)
equate cust.name to record<3>
```

**An `equate` is a substitution, not a variable.** You cannot assign to one,
and it is replaced wherever the name appears. `equate cust.name to record<3>`
means `cust.name` reads field 3 of whatever `record` holds at that moment.

```
$include file.name record.name
include file.name record.name
```

pulls in another source record at compile time. The system definitions live in
`syscom` — `$include syscom keys.h` for the key numbers used by `fileinfo()`,
`selectinfo()` and the rest.

## Matrices

```
dim name(rows {, columns})
dimension name(rows {, columns})
mat name = expression
mat name = mat other.name
```

A matrix is a fixed set of numbered variables, not a dynamic array. `dim` must
appear before any use, and the bounds are fixed at that point.

```
dim m(3)
mat m = 7          ;* every element becomes 7
```

After `mat m = 7`, `m(1)`, `m(2)` and `m(3)` all read `7`.

**A matrix has a zero element and it is not counted in the dimension.**
`dim m(3)` gives `m(0)` through `m(3)`. `m(0)` is where `matparse` puts
anything left over, and it is easy to forget it exists.

### Between a matrix and a string

```
matbuild variable from matrix {, start {, end}}
matparse matrix from string, delimiter
inmat({matrix})
```

| | |
|---|---|
| `matbuild` | joins the elements into one string |
| `matparse` | splits a string across the elements |
| `inmat()` | after `matparse`, how many elements were filled |

With `m` holding `7`, `7`, `7`:

| | |
|---|---|
| `matbuild bs from m` | the three elements joined with **field marks** |
| `matbuild bs from m, 1, 2` | the first two only |
| `matparse m from 'x' : @vm : 'y' : @vm : 'z', @vm` then `m(1)`…`m(3)` | `x y z` |
| `inmat()` after that | `3` |

> **The `using` clause of `matbuild` does not work, in either case.**
> The documented syntax `matbuild var from mat using delimiter` compiles the
> keyword as a **variable name** and the program aborts at run time with
> *"Unassigned variable USING"*, with both `using` and `USING`.
>
> **This is inherited, not introduced by this port** — the `st.matbuild` block
> in `BCOMP` is byte-identical to the one in the upstream `sdb64` tree. **The
> delimiter is always a field mark.** If you need another one, use `matbuild`
> and then `change()`, or build the string with a `for` loop.

`matparse` splits on the delimiter you give and stops when the matrix is full;
anything left over goes into element zero.

## Common blocks

```
common {/name/} variable, ...
clearcommon
delete.common name
```

Variables in a common block survive `chain` and are shared between programs
that declare the same block. An **unnamed** common block — `common // a, b, c`
— belongs to the program run and is cleared when it ends; a **named** one
persists for the session.

**`//` is the unnamed common marker, which is why it is not an integer-divide
operator.** See [SD Basic - Math Functions](03-sd-basic-math-functions.html).

`clearcommon` sets every unnamed common variable to zero. `delete.common`
discards a named block entirely, which is the only way to reclaim it within a
session.

> **A common block is matched by name and position, not by variable name.** Two
> programs declaring the same block with different variable lists will read each
> other's data at the wrong offsets, silently. **Put the declaration in an
> include record and `$include` it everywhere**, so there is one copy.

## Class modules and objects

SD BASIC has class modules with member variables, methods, properties,
constructors, destructors and inheritance. **They have their own page**, because
they are a different way of writing a program rather than a feature of this one:
[SD Basic - Modern Program Structure](18-sd-basic-modern-program-structure.html).

The short form:

```
class name {inherits base}
private variable, ...          public variable, ...
public subroutine name(...)    public function name(...)
get name                       set name(value)
end
```

```
o = object('CLASSNAME')
o->method(args)
o->property = value
```

**SD's own client library is a class module.** `gpl.bp/SDCLIENT` is 1,040
lines with 33 members and both lifecycle hooks — connecting to another SD server
from BASIC means instantiating it. *(An earlier version of this page said
nothing in SD used class modules. That was wrong.)*

## Arguments

```
arg.count()
arg(n)
set.arg n, value
```

These read the arguments of the **command line** that started the program, not
the arguments of a subroutine call. `arg(1)` is the first word after the verb.

## Arguments that may be left out

```
subroutine name(a, b = 7, c = 'none') var.args
function name(a, flag = @true) var.args
arg.present(name)
reusing(name)
```

An argument may be given a **default value**: a number (a minus sign allowed),
a string in single or double quotes (not one that holds both kinds), `@true` or
`@false`. The program then needs `var.args`, or `$mode default.unass.args`, or the
compiler refuses it (*Default argument values need the VAR.ARGS option or $MODE
DEFAULT.UNASS.ARGS*); a default that is anything else, such as a variable or an
expression, is *A default argument value must be a number, a string, @TRUE or
@FALSE*. When the caller passes fewer arguments than there are, the missing ones
take their defaults; with `$mode default.unass.args` one that was passed
**unassigned** takes it too. `arg.count()` is still the number the caller passed,
not what the defaults make of the rest. The program's own lines keep their line
numbers.

`arg.present(name)` is true if the caller passed that argument, whether or not
it has a default now. It names an argument of the subroutine or function it is
in; any other name, or use outside one, is a compile error (*xx is not an
argument of this subroutine or function*). `reusing(name)` is true if the caller
passed the argument with `reuse()`, and does not clear it.

## Case sensitivity of strings: `casing`

```
casing on
casing off
casing expression
```

Switches case sensitivity of string comparisons and the string functions for the
rest of the running program, the way `$nocase.strings` does for the whole of it.
`system(1086)` says which is in effect. A `casing` with nothing after it is a
compile error.

## Discarding a result

```
void expression
```

Calls a function and throws the answer away. It exists because SD BASIC has no
statement form for a function call — `void kernel(...)` is the idiom you will
see throughout `gpl.bp`.

## Compiler modes: `$mode`

```
$mode name {, name …}
$mode -name
```

A mode changes how one program is compiled. **Every mode is off unless the
program asks for it**, and a program that does not ask sees no change. A name
with a minus in front turns the mode off again. The ones below are the 1.2-0
additions; each is described by what it does and does **not** do.

| mode | what it does |
|---|---|
| **`partial.expressions`** | `A and B` does not evaluate `B` when `A` is false, and `A or B` does not evaluate `B` when `A` is true. That makes `if idx matches '1-2N' and s<idx> # 0` safe, and a function with a side effect on the right-hand side runs only when it is needed. **The value of every expression is the same as without the mode**; only what is evaluated changes |
| **`execute.clearlist`** | clears the default select list (list 0) before the command of each `execute` runs, so the command does not pick up a list the program happened to have active. An `execute` with a **passlist** clause, with or without a variable, still passes the list in |
| **`pick.readnext`** | a `readnext` that takes its `else` clause (the list is exhausted, or none is active) leaves the id variable as it was instead of setting it to the null string, so a program can read the last id after the loop. **Only the plain forms**; the forms that return value and subvalue positions are unchanged |
| **`open.fail.zero.fvar`** | an `open` or `openpath` that fails leaves the integer `0` in the file variable, where it is otherwise unassigned and a test of it stops the program with a run-time error. The `else` clause is taken as always, and an `open` that works is not touched |
| **`stdfil`** | the default file variable: `open`, `read`, `matread`, `write`, `matwrite`, `delete`, `close`, `clearfile`, `filelock`, `fileunlock`, `release` and `select` may be written without a file variable and use one the program does not name |
| **`write.delete.then.else`** | `write`, `writeu`, `matwrite`, `matwriteu`, `delete` and `deleteu` take `then` and `else` clauses. A trigger that refuses the write or delete takes `else`, and the trigger is told it is being called with an error trap set. A statement with neither clause is as it was |
| **`change.no.overlap`** | `change`, `ereplace` and `swap` count occurrences without overlap: when a starting occurrence is given, the ones before it are passed over whole, not one character at a time. A replace-all is the same with or without the mode |
| **`count.overlap`** | `count` and `counts` find occurrences that overlap: `aa` in `aaaaaaaaa` is found 8 times, not 4. `dcount` is not changed, a delimiter never overlapping |
| **`index.overlap`** | `index` and `indexs` take the *n*th occurrence counting the ones that overlap, so the 3rd `aa` in `aaaaaaaaa` starts at character 3, not 5 |
| **`pick.convert`** | `convert(string, from, to)`: the string first, as Pick has it, in place of `convert(from, to, string)`. It applies from the line where the mode is turned on; the `convert` statement is not changed |
| **`pick.select`** | `selectv` moves an active default select list (list 0) to the variable instead of making a new selection |
| **`explicit`** | every scalar has to be named in a `dim` statement before it is used, or the compiler refuses the program with *Variable xx has not been declared* |
| **`default.unass.args`** | an argument that has a default value (see *Arguments that may be left out* above) also takes it when the caller passed the argument unassigned, not only when it was left out |
| **`trap.unused.main`** | like `trap.unused`, but it warns only about a variable that is assigned a value in the program itself, not in an include record |
| **`conditional.statements`** | accepted, and it changes nothing: `read`, `readu`, `readv`, `readnext`, `readseq`, `readblk`, `readcsv`, `matread`, `open`, `openpath`, `openseq`, `writeseq`, `writeblk`, `writecsv`, `seek`, `send`, `filelock`, `fileunlock`, `flush`, `getlist`, `locate`, `find` and `findstr` may always be the condition of `while` and `until` |

## Options that change how SD runs a program

`option` on its own lists every option and its state; `option` *name* `on` or
`off` sets one (see [SD Basic - Numeric Tests and Formatting](03a-sd-basic-numeric-tests-and-formatting.html)).
**All of these are off by default.**

| option | what it does |
|---|---|
| **`chained.select`** | a `get.list`, `qselect`, `search`, `select`, `sselect` or `selectindex` that leaves an active select list takes the first line of the data queue and runs it as the next command, as a `chain` would: `data 'LIST STOCK'` followed by `execute 'SELECT SALES'` lists the selected records. **When the select finds nothing the queue is cleared**, so the commands waiting for a list do not run on nothing. Without the option the data queue is left alone |
| **`pick.ml.conv.mask`** | a left bracket in an `ML` or `MR` conversion code no longer asks for negative values in round brackets: it starts a format mask enclosed in round brackets, as in `MR2(#10)` or `ML2,(%8)`. The mask is read as if the brackets were not there, in output and in input conversion. The other negative-value styles (`+ - < C D`) and the `P`, `Z` and `T` options are as they were |
| **`force.reload`** | an unload event (compiling or cataloguing a program) also refreshes the subroutine links a running program holds, so the next `call` loads the current object code |
| **`numeric.exponent`** | numbers in exponent form, such as `123.45E-2`, are numeric |
| **`paginate.on.heading`** | with `run ... no.page`, a heading or a footing still turns pagination on |
| **`query.footer.pause`** | a report with a page footer waits for Return after its last footer |
| **`inherit.mfile.path`** | `create.file` puts a new subfile of a multifile in the directory of the default subfile |
| **`git`** | a directory file keeps `.gitignore` and `.gitattributes` under their own names on the disk. Without it the leading dot of every such name is replaced by `%D`, which git does not read. **Only these two names**: any other name with a leading dot is mapped as ever |
| **`dir.dtm`** | writing a record to a directory file moves the directory's date and time modified. The system moves it only when a name is added or removed, so a replaced record leaves it as it was. **Closing a written sequential file does not do this** |
| **`keep.old.object`** | a compilation that fails leaves the previous object code in place, where it would otherwise be deleted before the compiler starts. The listing of the failed compile is not put back |
| **`no.phantom.notify`** | set inside a phantom, it stops the message the phantom sends to its parent when it ends (*Phantom nn : Normal termination.*) |
| **`spool.command`** | shows the operating system command that prints a job, just before it runs; a diagnostic aid |
| **`correlative.nocase`** | string operations in a correlative or an I-type ignore case. The option is read when the correlative runs, not when it was compiled |
| **`correlative.reuse`** | the array operators of a correlative or an I-type act as if `reuse()` had been applied to each operand: the last value of a shorter array is used again for the missing ones, where otherwise they count as zero. Read when the correlative runs |
| **`assoc.all`** | the query processor ignores the associations in the dictionary and treats every field as one association. With `by.exp` on one multivalued field, each line then shows the matching value of the other fields, where fields in other associations show all of theirs on every line |
| **`clear.select`** | the command processor clears the default select list (list 0) when a command ends **if the list was already active when the command began**: a list the command made itself is kept, so `select` followed by `list` still works. A program that was meant to use what is left of a list and leave it says **`keep.select`**, and then the list stays (below) |

### `keep.select`

```
keep.select
```

A program that finds a select list active, takes some of it and ends leaves the
rest behind, where the next command may take it up by accident. With `option
clear.select` on, the command processor clears list 0 as the command ends. A
program that **means** to leave what is left of the list for the next command
says `keep.select` and it stays. The word belongs to the command that ran it and
is forgotten when that command ends, so a second command that does not say it
loses the list. **Without `option clear.select` the statement does nothing**,
since nothing was going to clear the list.

## What is not here

Nothing in the program-structure group has been removed from this port. The
`package` statements — `enter.package`, `exit.package` and `package` — went
before SD Core, and `varset` is present but is an internal debugging aid rather
than something application code uses.

## See also

[SD Basic - Program Control](02-sd-basic-program-control.html) · [SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html) ·
[SD Basic - File Handling](07-sd-basic-file-handling.html) · [SD Basic - Math Functions](03-sd-basic-math-functions.html).

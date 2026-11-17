Title: SD Example Programs
Subtitle: The file examples.bp in every account: the TUI guide's five pages and a first course in programming, compiled and ready to run.

Every account has a file **`examples.bp`** that holds example programs, already compiled.
Nothing has to be copied or set up to try one: at the prompt, type

```
run examples.bp cs01.hello
```

The file is the account's own, and SD fills it: the installer puts it into every account, a new
account gets it when it is made, and an upgrade refreshes the programs SD ships. It is a program
file like `bp`, so whether you may change it is the account's `bp-on` setting, which is off as
delivered: you can list, read and run every program in it, but not change them there.

**To change a program, copy it to your own `bp` file first.** An upgrade puts the shipped
programs back, so a change made in `examples.bp` itself would not last. Saving and compiling in
`bp` needs `bp-on` (the administrator gives it: `modify.account <account> bp-on`):

```
copy from examples.bp to bp cs06.fizzbuzz
basic bp cs06.fizzbuzz
run bp cs06.fizzbuzz
```

`list examples.bp` names them all; `ct examples.bp cs10.recursion` shows one.

## A first course in programming

Twenty-three short programs, in the order a first course in computer science takes the ideas.
Each begins with a few comment lines that say what it shows. Read one, run it, then copy it to
`bp` and change it.

| Program | What it shows |
|---|---|
| `cs01.hello` | output, comments, the end of a program |
| `cs02.variables` | variables, numbers and strings, arithmetic and the order it is done in |
| `cs03.input` | asking the person at the terminal for values with `input` |
| `cs04.decisions` | `if` / `then` / `else`, and `begin case` for a choice among several |
| `cs05.loops` | `for` / `next`, `step`, and `loop` with `while` or `until` |
| `cs06.fizzbuzz` | the classic exercise: a loop, `mod` and a choice |
| `cs07.tables` | a loop inside a loop, and lining up columns with `fmt` |
| `cs08.temperature` | a formula, decimals and rounding |
| `cs09.subroutines` | `gosub` and local subroutines with arguments and private variables |
| `cs10.recursion` | a routine that calls itself, and the same work done with a loop |
| `cs11.arrays` | a dimensioned array: sum, average, highest, lowest |
| `cs12.dynamic.arrays` | SD's own data structure: fields, values, `ins`, `del`, `dcount` |
| `cs13.strings` | length, case, parts, searching, and a palindrome check |
| `cs14.words` | counting words in order with `locate ... by` |
| `cs15.primes` | the sieve of Eratosthenes |
| `cs16.gcd` | Euclid's algorithm, the greatest common divisor and the least common multiple |
| `cs17.sorting` | bubble sort, and insertion into a list kept in order |
| `cs18.searching` | linear and binary search, counting how many items each looks at |
| `cs19.stack.queue` | a stack and a queue in a dynamic array |
| `cs20.files` | a file of records: make it, write, read, select, change, delete |
| `cs21.guess` | a guessing game: random numbers, input and a count |
| `cs22.dates` | dates and times stored as numbers, shown with `oconv` |
| `cs23.bank` | a small program put together: transactions, a rule and a report |

`cs03.input` and `cs21.guess` wait for you to type. `run examples.bp cs21.guess 42` starts the
game from seed 42, so the same game can be played again. `cs20.files` makes a file called
`cs20.data` in your account and removes it when it ends.

## The full-screen pages

Five programs are the examples of the separate *SD Text User Interface - Programmer's Guide*,
one for each of its chapters; the guide prints each one whole and explains it line by line.

| Program | Chapter | What it adds |
|---|---|---|
| `hello` | A Bare Page | the frame, one pane, the keys `resize` and `guardquit` |
| `menus` | Menus and the Finder | the key table and its menus, F1, F2, Esc, the mouse |
| `notes` | A Form and a Confirm Box | a form, a confirm box, a record the program writes, the output pane |
| `browse` | Panes and Pickers | two panes and the focus, wrapped text, a pick list, the record picker |
| `stock` | A Form in the Body | a `screen form` with a table, `screen wait`, `screen ask` and `screen msgbox` |

They need a terminal of at least 140 columns by 43 lines. `notes` and `browse` use a file called
`notes` in your account: make it once with `create.file notes`.

```
run examples.bp hello
```

## See also

- [SD Programming 101](40-sd-programming-tutorial.html) - the same ground as a tutorial, with
  each program explained as it is built
- [SD BASIC Program Structure](01-sd-basic-program-structure.html)

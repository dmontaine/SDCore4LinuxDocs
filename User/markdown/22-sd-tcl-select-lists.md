Title: SD TCL - Select Lists
Subtitle: Choosing a set of records once and then using it, saving it, and combining it with another.

A select list is a list of record ids that SD is holding for you. You build one
with `select`, and **the next command you type works on those records instead of
the whole file**. That one sentence is most of this page.

SD folds case, so a command may be typed in either case. Commands and keywords
are shown here in lower case. In the tables, *italics* mark something you supply
and **bold** marks a word typed as it stands; braces mark an optional part.

> **Every listing on this page was produced by running it**, on SD Core for
> Linux, in an administrator account. The file being queried is `voc`,
> because it is the one file every account has.

## The one thing to understand first

```
select voc with dispatch = "OS"
```

```
2 record(s) selected to list 0
```

Now the file has 418 records and the list has 2. **The next command sees 2:**

```
count voc
```

```
2 record(s) counted
```

**That is the point of select lists and it is also the trap.** A list you
built and forgot about silently narrows the next thing you do, and nothing
about the answer says so — `2 record(s) counted` is not obviously wrong. **A
surprisingly small answer is very often a leftover list.**

**The list is consumed by the command that uses it.** Run `count voc` again and
you get 418, because the list is gone.

### The prompt tells you

While a list is active the command prompt gains a second colon:

```
:select voc with dispatch = "OS"
2 record(s) selected to list 0
::
```

**`::` means a list is waiting.** `:` means there is not one. This is the
quickest way to answer *why did that only find two records* before you go
looking for a bug.

`clear.select` throws lists away without using them:

| | |
|---|---|
| **`clear.select`** {*n*} | discard list *n* |
| **`clear.select all`** | discard all of them |

```
clear.select all
```

```
Cleared all numbered select lists
```

`clearselect` is the same verb, spelled without the dot.

## Building a list

| | |
|---|---|
| **`select`** *file* {*selection*} | the records that match |
| **`sselect`** *file* {*selection*} | the same, sorted |
| **`show`** *file* {*selection*} | choose records interactively |
| **`qselect`** {**dict**} *file* {**saving** *n*} | a list of **field values** rather than record ids |
| **`nselect`** *file* | keep only the ids of the active list that are **not** in *file* |
| **`form.list`** {**dict**} *file* *record* | take the list from a record's contents |
| **`select.dir`** *pathname* {**to** *n*} | the names in an operating system directory |
| **`selectindex`** {**dict**} *file* *index* {*value*} {**to** *n*} | the values of an alternate key index, or the ids of the records that have one value (see [Alternate Key Indexes](23-sd-tcl-alternate-key-indexes.html)) |

`select` and `sselect` take the whole selection language of the query processor
— `with`, the operators, `by` — so anything you can list you can select. See
[SD TCL - The Query Processor](21-sd-tcl-query-processor.html).

**`qselect` reads a field out of each record and makes a list of those values.**
It is how you follow a reference from one file into another: select the orders,
`qselect` the customer number, and the list you are left with is customers.

> **`qselect` does not tell you which list it filled.** Its completion message
> ends after the words *select list* with no number:
> `14 record(s) selected to select list`. **The list is there** — it is list 0
> unless you gave `to` *n*. `select` and `nselect` both print the number
> correctly, so do not read this as the list being missing.

### The names in a directory: `select.dir`

```
select.dir pathname {to n}
```

Makes a list (0, or `to` *n*) of the names of the files and subdirectories in an
**operating system** directory, in the order the operating system returns them,
which is no order in particular — `sort.list` below puts them in one.

```
select.dir /home/pat/reports
```

```
4 record(s) selected to select list 0
```

There is no option to keep only files or only directories. The directory is read
**as you**, with your own permissions. A path outside the account's own directory
needs the `os-on` switch, as `oscopy` does; without it the verb says *name has no
OS access, so a file or directory outside its own account cannot be reached by
pathname*. A directory that cannot be read is *Cannot read directory* and the
pathname; a missing pathname is *Directory pathname required*. A `to` with no
number, or a bad one, is *Select list number missing or invalid*.

## Numbered lists

There are **eleven**, numbered **0 to 10**. List 0 is the default and the one
every verb uses when you do not say otherwise. `to` *n* puts the result
somewhere else, which is how you keep two lists at once:

```
select voc with dispatch = "OS" to 3
select voc with dispatch = "IN" to 4
```

```
2 record(s) selected to list 3
45 record(s) selected to list 4
```

**A list in 1 to 10 does not affect the next command.** Only list 0 does. That
is what makes the numbered lists a safe scratch area, and it is why the prompt
above stayed `:` rather than becoming `::`.

### Moving a list: `move.list`

```
move.list 3 to 0
move.list 0 to 5 keep
```

Moves the ids of list *n* that have not been read to list *m*, replacing what
*m* held; list *n* is then empty. **`keep`** leaves the source as it was, so
both lists hold the ids. A list moved onto itself, and an empty list, are left
as they are. A number outside 0 to 10, a missing number, or a word other than
`to` and `keep` is refused (*Select list number missing or invalid*,
*Unexpected token (xx)*) and nothing is moved. `move.list 3 to 0` is how a
list kept in 3 is made the one the next command uses.

### A command for each id: `execute.list`

```
select voc with type = 'F'
execute.list analyse.file () ; pause
```

Runs its commands, separated by semicolons, for each id of list 0 in turn: the
pair of empty round brackets in a command is replaced by the id, as many times
as it appears. Every id is taken out of the list before the first command runs,
so a command that itself uses list 0 does not take ids from the loop, and the
list is empty afterwards. With no active list nothing is run and nothing is
said; with no command at all the verb stops with *A command is needed after
EXECUTE.LIST*.

## Choosing from a list: `show.list`

```
show.list {n}
```

Shows the items of active select list *n* (list 0 if no number is given) a page
at a time, each with its number and an asterisk. **All items start starred.**
When you quit, the list is made again from the items that still carry an
asterisk.

| | |
|---|---|
| **`s`** *items* | star the items. Just the number does the same |
| **`c`** *items* | clear the asterisks of the items |
| **`t`** | top of the list |
| **`n`** · Return | next page |
| **`p`** | previous page |
| **`q`** | quit, keeping the asterisks |
| **`qc`** | quit, keeping nothing |
| **`?`** | help |

*Items* is a number, a range `a-b` with no spaces round the hyphen, `visible`
(the items on this page) or `all` (`v` and `a` will do); several may be given
separated by spaces or commas, as `1,4,8-11`. The space after `s` and `c` is
optional. **`show.list` changes only the list in memory** — it does not save it;
use `save.list` for that.

## Saving a list by name

Numbered lists last as long as your session. A **saved** list is a record in the
account's `$savedlists` file and outlives it.

| | |
|---|---|
| **`save.list`** {*name*} {**from** *n*} | save list *n* as *name* |
| **`get.list`** {*name*} {**to** *n*} | load it back into list *n* |
| **`delete.list`** *name* | delete the saved list |
| **`copy.list`** *name* {`,`*new*} {**from** *file*} {**to** *file*} | copy one, or `*` for all |
| **`sort.list`** *name* {**from** *file*} | sort a saved list, in place |
| **`copy.listp`** {{**dict**} *file*} {*name* ... \| `*`} {`(`*options*} | the Pick form of `copy.list`: show a saved list, or copy it to another file |

Both default to list 0, and `save.list` defaults the name to the list number.
**`save.list`** takes **`keep`** to leave the active list as it was (it has always
emptied it) and **`count.sup`** to leave out the count of records, and **`get.list`**
takes **`deleting`** to delete the saved list once it is loaded and `count.sup`
too. With the name left out, a list is called after its number: `save.list` saves
list 0 as `0`, and `get.list 0` brings it back.

```
select voc with dispatch = "OS"
save.list zzos
```

```
2 record(s) selected to list 0
2 records saved to select list 'zzos'
```

```
get.list zzos
delete.list zzos
```

```
2 record(s) selected to select list 0
Deleted saved select list 'zzos'
```

**`copy.list` moves a saved list between accounts**, because `from` and `to` name
the `$savedlists` file to read and write. Within one account it renames or
duplicates.

### `sort.list`

```
sort.list name {from file}
```

Sorts a saved list into ascending order, **as strings**, in place, and says how
many it saved. `from` names another file of saved lists. There is no descending or
numeric order (the list `9 10 100` sorts as `10 100 9`).

```
select.dir /home/pat/reports
save.list reports
sort.list reports
```

```
4 record(s) selected to select list 0
4 records saved to select list 'reports'
4 records saved to select list 'reports'
```

A list that is not there is *Saved select list 'name' not found*, and no name is
*Source list name required*.

### `copy.listp`

```
copy.listp {{dict} file} {name ... | *} {(options}
```

The Pick form of `copy.list`, and the **same program as `copyp`**: its options and
its `To:` question are `copyp`'s (`d` delete the source, `i` leave out the id, `n`
no pagination, `o` overwrite, `p` to the printer, `s` leave out field numbers, `t`
to the terminal). What differs is that the source file is **`$savedlists`**, where
saved lists are kept, unless one is named. `*` is every saved list.

```
copy.listp reports (t
```

```
Item reports
0001 a.txt
0002 b.txt
0003 c.txt
0004 subdir
1 record(s) copied.
```

With `copy.listp *` and `t`, every saved list is shown. **When two or more words come
before the options, the first is the source file if it opens as a file, and
every word is a list name if it does not**; a file and a list with the same name
are told apart by writing the file first (`copy.listp $savedlists reports`). After
`dict` the next word is always the file. `copyp` itself still needs a file name.

## Combining two lists

**There are two sets of verbs and they take different things. this is the
easiest mistake on the page.**

| | takes | |
|---|---|---|
| **`list.union`** · **`list.inter`** · **`list.diff`** | **saved list names** | reads and writes `$savedlists` |
| **`merge.list`** | **list numbers** | works on the numbered lists in your session |

All four commands find a key of one list in the other without scanning it
(since 16 Oct 2026), so lists of tens of thousands of keys merge in seconds
where the time used to grow with the product of the two lengths. The result
is what it always was: a union keeps the first list and adds each new key of
the second once; an intersection gives the keys of the second list that are in
the first, a key repeated in the second repeated; a difference takes away one
occurrence in the first list for each key of the second.

Giving a number to `list.union` does not do the numbered thing — it looks for a
saved list with that name and fails:

```
list.union 3 4 5
```

```
First source list does not exist
```

### By name

```
list.union zzos zzin zzboth
list.inter zzos zzin zzover
```

```
47 records saved to select list 'zzboth'
0 records saved to select list 'zzover'
```

Both write a **saved** list, not a numbered one, so `get.list` is how you pick
the result up. The two answers above check each other: the sources hold 2 and 45
records with nothing in common, so the union is 47 and the intersection is 0.

### By number

```
merge.list 3 union 4 to 5
merge.list 3 intersect 4 to 6
```

```
47 record(s) selected to select list 5
0 record(s) selected to select list 6
```

The operator words are **`union`**, **`intersect`** (or `intersection`) and
**`diff`** (or `difference`). `to` *n* names the target, defaulting to list 0,
and `count.sup` suppresses the count line.

`list.diff` and `merge.list ... diff ...` give the records in the first list that
are not in the second, so **the order of the two arguments matters** where it
does not for union and intersection.

## Who has these verbs

**All of them are in every account.** Building, saving and combining lists
is reading, and nothing on this page changes a record. (`select.dir` reads an
operating system directory, and that is where the `os-on` switch comes in.)

## See also

[SD TCL - The Query Processor](21-sd-tcl-query-processor.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html) ·
[SD Basic - Select Lists](08-sd-basic-select-lists.html).

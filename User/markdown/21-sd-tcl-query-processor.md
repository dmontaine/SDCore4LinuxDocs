Title: SD TCL - The Query Processor
Subtitle: Choosing records, sorting them, and printing a report, without writing a program.

The query processor is how you ask a file a question from the command line. It
selects records, sorts them, formats them into columns and totals them, and it
does all of that from one line of typing.

**Thirteen verbs on this page are the same program.** `list`, `sort`, `count` and
the rest are one cataloged program reached through fifteen VOC records, each
carrying a number that says which verb was typed. Two of the fifteen —
`select` and `sselect` — build a list instead of printing one and are covered in
[SD TCL - Select Lists](22-sd-tcl-select-lists.html).

SD folds case, so a query may be typed in either case. Commands and keywords are
shown here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

> The file queried in the listings is `voc`, because it is the one file
> every account has and it is interesting enough to ask real questions of.

## The shape of a query

```
verb {dict} file {selection} {sort} {output fields} {modifiers}
```

Everything after the file name is optional, and the parts may be given in
almost any order. The shortest useful query is a verb and a file:

```
count voc
```

```
418 record(s) counted
```

**That number is particular to the account it was run in.** Every account has
a `voc`, and no two need hold the same records — every ordinary account
starts with the same set as every other, but local additions can differ, and
`SDSYS`'s is larger to begin with. The counts on this page came from SDSYS.

## The verbs

| | |
|---|---|
| **`list`** | print the records |
| **`sort`** | print them in order |
| **`count`** | print how many there are, and nothing else |
| **`sum`** | total a field across the records |
| **`list.item`** · **`sort.item`** | print whole records, field by field, rather than in columns |
| **`list.label`** · **`sort.label`** | print in label format |
| **`search`** · **`scan`** | select records by looking for text inside them; `scan` also shows the lines that hold it |
| **`show`** | build a select list interactively |
| **`reformat`** · **`sreformat`** | write the selected fields out to another file |

`sort` is `list` with an order imposed; every other pair works the same way, the
`sort` half being the ordered one.

## Choosing records

`with` introduces a selection clause:

```
count voc with dispatch # ""
```

```
144 record(s) counted
```

That one counts the verbs in the account, because `dispatch` is a dictionary
entry that is empty for anything that is not a verb.

### The operators, and their synonyms

**SD accepts several spellings of each operator** and they are exactly
equivalent — the same token underneath. Each row below was run, and the
spellings in a row returned identical counts on the same data.

| | |
|---|---|
| equal | `=` · `eq` |
| not equal | `ne` · `not` |
| less than | `<` · `lt` |
| less or equal | `<=` · `le` |
| greater than | `>` · `gt` |
| greater or equal | `>=` · `ge` |
| matches a pattern | `like` |
| does not match | `unlike` |
| sounds like | `said` |
| is in a list | `in` |
| is not in a list | `not.in` |

All three spellings of *not equal* returned **331** on the same query, and
`<` and `lt` both returned **381**. (The words `before`, `after`, `equal`,
`greater`, `less`, `matches`, `matching`, `not.matching` and `spoken` were removed in 2.0-0:
in a query they are taken as record ids.)

### Joining clauses

`and` and `or` join clauses. **Each clause repeats `with`:**

```
count voc with dispatch ne "" and with dispatch ne "CA"
```

```
47 record(s) counted
```

### Patterns

`like` takes the same pattern language as SD BASIC's `matches` — `0x` for any
number of characters, `1a` for one letter, `3n` for three digits, quoted text
for a literal. It is set out in
[SD Basic - String Functions](04-sd-basic-string-functions.html).

```
count voc with f1 like "V0X"
```

```
140 record(s) counted
```

> **A pattern that is not valid selects nothing and does not complain.**
> Writing that same query as `like "V]"` returns **0 record(s) counted** — not
> an error, not a warning. **Always prove a pattern against a case you know
> matches** before believing a small answer, and be especially careful of a
> query that returns zero when you expected few.

### Is it in a list: `in` and `not.in`

```
list myfile with color in colors @id
list myfile with color not.in colors @id
list myfile with color in "myfile allow" @id
list myfile with color in no.case "myfile allow" @id
list myfile with every tags in tags.list @id
```

`in` selects the records whose field has a value that is one of the values of a
list; `not.in` selects the others. The list is named after the operator in one
of two ways:

| Written as | The list is |
|---|---|
| a bare word, `colors` | the saved select list of that name, from `$savedlists` |
| a quoted *file* and *id*, `"myfile allow"` | the fields of record *id* of *file*, one value to a field |

The first word of a quoted name is the file and the rest is the record id. A
quoted name with no space in it is a saved list. The match is exact, and
**is case sensitive unless `no.case` comes before the list**. With `every`, a
multi-valued field is chosen only when all of its values are in the list
(with `not.in`, when none of them is); without it, one value is enough. `when`
shows only the values that satisfy the test, as it does for the other
operators.

An empty list contains nothing, so `in` selects no record and `not.in` selects
every one. A file or record that cannot be read stops the command, with *File
not found* or *Record "name" not found*, and an empty name (`in ""`) stops it
with *A saved list name, or a quoted file and record id, is needed after in or
not.in*. These two operators never use an alternate key index.

The values in the list are compared with the field as it is stored. Unlike a
value typed in the sentence, they are not run through the field's input
conversion first, so for a field with a conversion (a date, say) the list must
hold the stored form: a list of day numbers selects the records for those days,
a list of the same dates written as `12/31/2023` selects none. *(Tried on a
field with the `D4/` conversion.)*

**`in` and `not.in` are now keywords.** After `=` or another comparison an
unquoted `in` is still an ordinary value: `with state = in` finds the records
whose state is IN. But after `or` or `and`, where the field and the operator are
left out and repeated for you, an unquoted `in` or `not.in` is the operator, so
`with state = "oh" or in` asks for a list name. Quote the value there:
`with state = "oh" or "in"`. A dictionary item called `in` still wins over the
keyword, and a quoted value is never taken for one. An account whose VOC
predates this change has no `in` or `not.in` record; the query processor knows
the two words anyway (tried, with both records deleted from the account's VOC),
and `update.accounts` adds the records.

These are the query processor's own. The paragraph `if` has an `in` of its
own, which compares a word with a list of words; the two are not connected.

### Other ways to choose

| | |
|---|---|
| **`every`** | apply the test to every value of a multi-valued field |
| **`when`** | select values within a record rather than whole records |
| **`no`** *field* | records where the field is null |
| **`unique`** | one record per distinct value |
| **`no.case`** | compare without regard to case |

## Looking for text inside records: `search` and `scan`

```
search {dict} file {selection} {ids} {all} {no.case} {all.match | no.match} for "text" {"text" ...} {display}
scan   {dict} file {selection} {ids} {all} {no.case} {all.match | no.match} for "text" {"text" ...}
search {dict} file ... strings file record
```

`search` selects the records that **contain** a text string, as select list 0, and
says how many:

```
search stock for "Boston"
```

```
1 record(s) selected to list 0
```

**`scan` is `search ... display`**: for each record it selects it prints the record
id, then every line (field) of the record that holds a string, with the line number.
The value, subvalue and text marks inside a line are shown as `]`, `\` and `[`.

```
scan stock for "Albany"
```

```
1001
0003: Albany
1 record(s) selected to list 0
```

| word | meaning |
|---|---|
| **`for`** *"text"* ... | the strings to look for, one or more quoted strings; up to 100 are used. With no `for` or `strings` it asks for strings until you answer with a blank line |
| **`strings`** *file* *record* | take the strings from a record, each field one string, a null field ignored; it adds to any given with `for`. A file or record that is not there is reported and nothing is searched |
| **`all`** | look at the record **id** as well as the record |
| **`no.case`** | ignore case |
| **`all.match`** | select a record only if it holds **every** string; the default is any one of them |
| **`no.match`** | select the records that hold **none** of them (and show no lines) |
| **`display`** | the `scan` listing, for `search` |

A selection clause (`with ...`) and record ids narrow what is searched, as they
do for `list`. **An active select list is searched instead of the whole file**, so
two `scan`s one after the other, the second without a `select` between, search
only what the first found. A record of a data collection file is searched as its
JSON text.

With `all.match`, `scan` still shows the lines that hold *any* one of the strings.

## Sorting

`by` sorts ascending, `by.dsnd` descending. Both take a field name, and both
may be repeated for a second and third key.

```
sort voc with dispatch = "OS" by @id dispatch processor
```

```
@ID.................   Dsp   Processor...............
sh                     OS
1 record(s) listed
```

`@id` is the record id, and it is a field name like any other.

## What gets printed

**Name the fields you want after the selection**, and they become the columns
in the order you name them. With no fields named, the file's default listing is
used — for `voc` that is a description built by the dictionary.

The column heading, its width and its format all come from the **dictionary**
entry for the field, not from the query. `Dsp` above is the display name of the
dictionary entry called `dispatch`.

| | |
|---|---|
| **`id.sup`** | leave the record id out |
| **`col.hdg`** *"text"* | override a column heading |
| **`fmt`** *"code"* | override the format |
| **`conv`** *"code"* | override the conversion |
| **`as`** *name* | use another dictionary entry's formatting |
| **`col.spaces`** *n* | change the gap between columns |
| **`vertically`** | one field per line instead of columns (see *A vertical report*) |
| **`dbl.spc`** | a blank line between records |
| **`col.sup`** · **`col.hdr.sup`** · **`hdr.sup`** | suppress column headings, both, or the page heading |
| **`count.sup`** | suppress the trailing record count |
| **`det.sup`** | suppress the detail lines, leaving totals |

## A vertical report

`vertically` prints one field to a line, the name of the field, a
colon and the value. **A second value of a multivalued field repeats the colon**;
a line that wrapped because the value was longer than the column has none, so
the two can be told apart:

```
list sales vertically
name....... : Ann
lines...... : one
           : two
text....... : a long value that
              wrapped here
```

The name column is 12 wide, the heading cut to fit it. Both can be changed:

| | |
|---|---|
| **`vertically fmt "25l"`** | the whole heading, in a column of that format |
| **`vertically fmt "fit"`** | a column as wide as the longest heading in the report |
| **`vertically fmt ,"20l"`** | a data format for the values: every item that is **not right justified in its dictionary entry** and has no `fmt` of its own takes it |

**The same, as a default for a dictionary or the whole account:** a record
**`$vlist`** in the dictionary (or, failing that, in the VOC) with `x` in field 1,
the name format in field 2 (or `fit`) and the data format in field 3. What the
command line gives wins over the record.

## Defaults for a file's queries: `$query.defaults`

A record **`$query.defaults`** in a dictionary, with `x` in field 1, holds words
added to the query before it is read: field 2 for `list` and `sort`, **field 3
for `select`, `sselect` and `search`**, and **field 4 the format of the id column the
query processor makes up when the dictionary has no `@id`** (a width and `l`, `r`,
`t` or `c`, as `10r`; anything else is ignored with a message and the default
`12l` is used). A line that ends with `_` continues on the next.

## Selecting some of the values: `when`

`when` takes the values of a multivalued field, not the record, and may be used
with the same operators as `with`. **`when field` with no operator keeps the values that are
not null**; `between` is checked against **every** value of the field; and
`unlike no.case` takes the case of the pattern as no matter.

## More than one exploded sort

`by.exp` and `by.exp.dsnd` may each be given **more than once, provided the fields are in the
same association** (the later ones decide the order of values that the earlier ones leave
equal). A field outside the association is refused with a message.

## Continued in

[SD TCL - The Query Processor: Headings, Totals and
Output](21a-sd-tcl-query-processor-headings-and-output.html) — headings,
totals and the forms of output.

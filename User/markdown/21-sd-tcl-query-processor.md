Title: SD TCL - The Query Processor
Subtitle: Choosing records, sorting them, and printing a report, without writing a program.

The query processor is how you ask a file a question from the command line. It
selects records, sorts them, formats them into columns and totals them, and it
does all of that from one line of typing.

**Twelve verbs on this page are the same program.** `list`, `sort`, `count` and
the rest are one catalogued program reached through fourteen VOC records, each
carrying a number that says which verb was typed. Two of the fourteen —
`select` and `sselect` — build a list instead of printing one and are covered in
[SD TCL - Select Lists](22-sd-tcl-select-lists.html).

SD folds case, so a query may be typed in either case. Commands and keywords are
shown here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

> **Every listing on this page was produced by running it**, on SD Core for
> Linux. The file being queried is `voc`, because it is the one file
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
| not equal | `#` · `ne` · `not` |
| less than | `<` · `lt` · `before` |
| less or equal | `<=` · `le` |
| greater than | `>` · `gt` · `after` |
| greater or equal | `>=` · `ge` |
| matches a pattern | `like` · `matches` · `matching` |
| does not match | `unlike` · `not.matching` |
| sounds like | `said` · `spoken` |
| is in a list | `in` |
| is not in a list | `not.in` |

`before` and `after` read well on dates and are the same operators as `<` and
`>`. All three spellings of *not equal* returned **331** on the same query, and
`<`, `lt` and `before` all returned **381**.

### Joining clauses

`and` (or `&`) and `or` join clauses. **Each clause repeats `with`:**

```
count voc with dispatch # "" and with dispatch # "CA"
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
!                      OS
sh                     OS
2 record(s) listed
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
| **`vert`** · **`vertically`** | one field per line instead of columns (see *A vertical report*) |
| **`dbl.spc`** | a blank line between records |
| **`col.sup`** · **`col.hdr.sup`** · **`hdr.sup`** | suppress column headings, both, or the page heading |
| **`count.sup`** | suppress the trailing record count |
| **`det.sup`** | suppress the detail lines, leaving totals |

## A vertical report

`vert` (or `vertically`) prints one field to a line, the name of the field, a
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

## Headings and footings

By default the page heading is **the query you typed**, followed by a page
number — which is genuinely useful on a printed report, because it says how the
report was produced. `heading` replaces it:

```
sort voc with processor = "$QPROC" by @id dispatch processor heading "QP verbs"
```

```
QP verbs
@ID.................   Dsp   Processor...............
count                  CA    $QPROC
list                   CA    $QPROC
list.item              CA    $QPROC
list.label             CA    $QPROC
reformat               CA    $QPROC
search                 CA    $QPROC
select                 CA    $QPROC
show                   CA    $QPROC
sort                   CA    $QPROC
sort.item              CA    $QPROC
sort.label             CA    $QPROC
sreformat              CA    $QPROC
sselect                CA    $QPROC
sum                    CA    $QPROC
14 record(s) listed
```

**That is the query processor listing itself** — all fourteen VOC records that
reach it, including `count`, which is a keyword record that doubles as a verb.

`footing` does the same at the bottom of the page. Both accept the usual
options inside the text for page number, date and time.

## Totals, averages and breaks

| | |
|---|---|
| **`total`** *field* | a column total |
| **`average`** · **`avg`** | the mean |
| **`median`** | the middle value: **the mean of the two in the middle when there is an even number**, a null counted as zero (left out with `no.nulls`), and a value that is not a number left out. At a break it is the median of that group, at the end of the report of every value. Where the values 150, 40, 30, 20 and 10 have an `average` of 50, their `median` is 30 |
| **`mode`** | the value that comes most often, at the end of the report and at each breakpoint; **if several come as often, the first one is shown**. A null is a value (left out with `no.nulls`), and the values need not be numbers |
| **`range`** | the largest value less the smallest, numbers only (a value that is not a number is left out, a null counts as zero unless `no.nulls`) |
| **`rpt`** | repeats a single valued field on every line of a report on a multivalued one, in place of printing it on the first line only |
| **`max`** · **`min`** | the largest and smallest value |
| **`enum`** · **`enumerate`** | count the values rather than total them |
| **`percent`** · **`pct`** · **`%P`** | express as a percentage |
| **`calc`** | evaluate an I-type against the totals |
| **`break.on`** *field* | start a new subtotal group when the field changes |
| **`break.sup`** *field* | break on a field without printing it |
| **`grand.total`** *"text"* · **`caption`** | label the final total line |

`break.on` is what turns a flat listing into a report with subtotals; the field
it breaks on almost always wants to be a sort key as well, or the groups come
out scattered.

**An `X` among a break field's control codes saves the field's previous value.**
The I-types of that line can read it as `@bpv`: the value the field had on the
last record before the break. It is empty on a field without `X`.

A report sent to the default printer (`lptr`) closes a printer that was already
active when the report began — a program's own `printer on`, say — so the report and
the program's output are **two print jobs**. (`option query.merge.print`, which kept them
as one, was removed in 1.2-0, as were `query.footer.pause` and `paginate.on.heading`.)

## Taking only some of the records

| | |
|---|---|
| **`sample`** *n* · **`first`** *n* | the first *n* records |
| **`sampled`** *n* | every *n*th record |

A sampled listing says so in its trailing line — `Sample of 3 record(s) listed`
rather than `3 record(s) listed` — so a partial report cannot be mistaken for a
whole one.

> **`sample` TAKES THE FIRST RECORDS FOUND AND THEN SORTS THEM. IT IS NOT THE
> FIRST *n* IN SORTED ORDER.** Adding `sample 3` to the sorted listing above
> returns `count`, `show`, `sort` — not `count`, `list`, `list.item`, which is
> what the first three of that report actually are. **The sample is taken during
> selection and the sort happens afterwards, on the sample.** Use it to see the
> shape of a report cheaply; do not use it to find the top three of anything.

## Where the output goes

| | |
|---|---|
| **`lptr`** {*n*} | to print unit *n*, 0 by default |
| **`crt`** | to the screen, overriding a default of print |
| **`no.page`** · **`nopage`** | do not pause at the end of each screen |
| **`file`** | to a file rather than a device |

Printing, print units and `$hold` are in
[SD TCL - Printing and Spooling](28-sd-tcl-printing-and-spooling.html).

## A report as CSV or delimited text

```
csv {mode} {"delimiter"} {to pathname | as file id} {no.query | appending}
delimiter "string" {to pathname | as file id} {no.query | appending}
```

`csv` makes the report comma separated values, one line for each record; `delimiter` puts
your own string between the cells and does no quoting. Neither prints a page heading; the
column headings are the first line unless `col.sup` is given, and on the screen the
"n record(s) listed" line follows the report.

| `csv` *mode* | a cell is put in double quotes when |
|---|---|
| **1** (the default) | it holds a double quote or the delimiter (RFC 4180); a quote inside is doubled |
| **2** | it is not empty and not a number |
| **3** | always, an empty cell too |

The delimiter of `csv` is one character other than a double quote. In either keyword the string
may hold `<tab>` for a tab and `^nnn` for the character whose three digit ASCII number is *nnn*.

### Where it goes: `to` and `as`

| | |
|---|---|
| **`to`** *pathname* | an operating system file. It is a path, so the account's OS access gate applies (a file outside the account's own directory needs `os` on) and so do the edit gates |
| **`as`** *file id* | a **record** of a **directory file**: the file's name and the record's id |
| **`no.query`** | replace what is there without asking |
| **`appending`** | add to what is there |

If the file or record is already there the report asks `... already exists. Overwrite(y/<n>)?`
(Enter is no), unless `no.query` or `appending` was given. **The two words may not be used
together**: the command says so and stops before it has opened anything. `to` or `as` also means
`hdr.sup`, since the output is not paginated, and one command takes only one of the two.

```
list sales by @id name qty price csv as exports r1001 no.query
```

writes the record `r1001` of the directory file `exports`. **`as` is a write like any other.**
The edit gates are asked of the file you named (a directory file that is a program file needs
`bp.edit`), and the record is locked while the report is written, so a record another session
holds is not waited for: the command names the holder (`Record 'r1001' is locked by user 5`)
and writes nothing. The lock is given back when the command ends. `as` needs a directory
file; a hashed file is refused (`AS needs a directory file, and sales is not one`).

An `as` straight after a field is the old **synonym** (`name as who`) and stays that; the
report's own `as` comes after `csv` or `delimiter` and its options.

### A multivalued field is split over lines

A field the dictionary calls multivalued (or `multi.value` makes one) gives **one line for
each value**, and the other columns are **blank on the continuation lines**:

```
list sales by @id name qty price csv
```

```
sales,name,qty,price
r1,Ann,1,1.50
,,2,2.00
,,3,3.00
r2,"Bob ""B"", Jr",5,3.25
r3,Cy,,
```

A record has as many lines as its longest multivalued field has values, and a shorter field
leaves blank cells. `rpt` after a single valued field repeats it on every line and `repeating`
does that for all of them, the id too. A field that is **single valued** in the dictionary, or
`single.value` after it, stays **one cell whatever its data holds**: the value marks are data
and are written as they are. Total and break lines are a line each, as they always were.

> **`encoding` is not here.** openQM lets `csv` and `delimiter` name a character encoding for the
> file. SD has no character sets, so the word is not accepted.

## A report as XML

```
list sales sale date cust item qty price xml
```

`xml` makes the report an XML document: the declaration, a root element
`<ROOT>`, and one element for each record, named for the file. A single
valued field is an attribute of it, and each row of an **association**
(fields the dictionary puts in the same association) is a tag named for the
association, a value in each attribute. A multivalued field that is in no
association is one tag for each value, named for the field with `_MV` added.
A field with no value is left out. The characters XML reserves (`&` `<` `>`
and `"`) become entities.

```
<?xml version="1.0" encoding="UTF-8"?>
<ROOT>
<sales sale = "12140" date = "14 Oct 07" cust = "1056">
  <line item = "003" qty = "1" price = "1.70"/>
  <line item = "122" qty = "3" price = "44.50"/>
</sales>
</ROOT>
```

| | |
|---|---|
| **`elements`** | every field is an element of its own, and an association row is an element that holds one element for each field, in place of attributes |
| **`with.dtd`** | the DTD, as a `DOCTYPE` for `ROOT`, before the data |
| **`dtd.only`** | the declarations of the DTD and no data |
| **`with.schema`** | an XML Schema document before the data (the data document follows it, with its own declaration) |
| **`schema.only`** | the schema and no data |

**What it does not do.** An XML report cannot have breakpoints, totals or any
other arithmetic on a field (it says so and stops), and `heading`, `footing`,
`det.sup` and the page layout are ignored. The `elements`, `with.dtd`,
`dtd.only`, `with.schema` and `schema.only` words are accepted only with `xml`.
The text of the DTD and of the schema is SD's own: the openQM manual shows the
data but not them. A character in a field name that is not a letter, digit,
underscore, dot or dash becomes an underscore, and the tags are in the case
the file and the dictionary give them.

## A report as JSON

```
list sales sale date cust item qty price json
list sales sale date cust item qty price json.lines
```

`json` makes the report a **JSON array** with one object for each record, and
`json.lines` the same objects as **JSON Lines**: one object to a line, no brackets,
no commas — the form `readjson` reads and `import.json` takes. The objects are
made as the `xml` report groups its fields: a single valued field is a member
(its text, in double quotes, with the characters JSON reserves escaped); a
multivalued field that is in no association is an array of its values; and the
fields of an **association** are an array of row objects, named for the
association. A field with no value is left out. Nothing is made a number: a
value is the text the field has.

```
[
{"cust":"1056","date":"14 Oct 07","lines":[{"item":"003","price":"1.70","qty":"1"},{"item":"122","price":"44.50","qty":"3"}],"sale":"12140"}
]
```

Like the `xml` report, a JSON report goes to the screen or the printer — **not** to
`to` or `as` (use `list ... csv as` for a file of text, or `convert.data` to
turn a CSV report into JSON) — and it cannot have breakpoints, totals or other
arithmetic on a field. `json` and `json.lines` may not be combined with `xml`,
`csv` or `delimiter` (the command says "Multiple use of DELIMITER or CSV
options"), and the XML words `elements`, `with.dtd`, `dtd.only`, `with.schema` and
`schema.only` are refused with them.

## Querying a dictionary

Put `dict` between the verb and the file name and the query runs against the
dictionary instead of the data. It is the quickest way to find out what field
names a file will accept:

```
list dict voc sample 14
```

```
@ID.................   TYPE   LOC...........   CONV..   NAME........   FORMAT   S/M
@ID                    D      0                         @ID            20L      S
NAME                   D      0                         NAME           16L      S
F1                     D      1                         F1             5L       S
DATA.NAME              D      2                         DATA Pathname  18L      M
...
Sample of 14 record(s) listed
```

`D` entries name a field by position, `I` entries compute a value, and `PH`
entries are phrases — stored fragments of query that expand where they are
named.

## Who has these verbs

| | |
|---|---|
| **standard** | `count` `list` `list.item` `list.label` `search` `show` `sort` `sort.label` `sum` |
| **programmer** | `reformat` `sreformat` `sort.item` |

Reading and reporting are available to every account; the two verbs that
**write** their result into another file are not.

## See also

[SD TCL - Select Lists](22-sd-tcl-select-lists.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html) ·
[SD Basic - String Functions](04-sd-basic-string-functions.html).

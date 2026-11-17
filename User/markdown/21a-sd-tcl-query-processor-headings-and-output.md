Title: SD TCL - The Query Processor: Headings, Totals and Output
Subtitle: Headings and footings, totals and breaks, and CSV, XML and JSON reports.

This page continues [SD TCL - The Query
Processor](21-sd-tcl-query-processor.html).

## Headings and footings

By default the page heading is **the query you typed**, followed by a page
number — which is genuinely useful on a printed report, because it says how the
report was produced. `heading` replaces it:

```
sort voc with processor = "$qproc" by @id dispatch processor heading "QP verbs"
```

```
QP verbs
@ID.................   Dsp   Processor...............
count                  CA    $qproc
list                   CA    $qproc
list.item              CA    $qproc
list.label             CA    $qproc
reformat               CA    $qproc
scan                   CA    $qproc
search                 CA    $qproc
select                 CA    $qproc
show                   CA    $qproc
sort                   CA    $qproc
sort.item              CA    $qproc
sort.label             CA    $qproc
sreformat              CA    $qproc
sselect                CA    $qproc
sum                    CA    $qproc
15 record(s) listed
```

**That is the query processor listing itself** — all fifteen VOC records that
reach it, including `count`, which is a keyword record that doubles as a verb.

`footing` does the same at the bottom of the page. Both accept the usual
options inside the text for page number, date and time.

## Totals, averages and breaks

| | |
|---|---|
| **`total`** *field* | a column total |
| **`average`** | the mean |
| **`median`** | the middle value: **the mean of the two in the middle when there is an even number**, a null counted as zero (left out with `no.nulls`), and a value that is not a number left out. At a break it is the median of that group, at the end of the report of every value. Where the values 150, 40, 30, 20 and 10 have an `average` of 50, their `median` is 30 |
| **`mode`** | the value that comes most often, at the end of the report and at each breakpoint; **if several come as often, the first one is shown**. A null is a value (left out with `no.nulls`), and the values need not be numbers |
| **`range`** | the largest value less the smallest, numbers only (a value that is not a number is left out, a null counts as zero unless `no.nulls`) |
| **`rpt`** | repeats a single valued field on every line of a report on a multivalued one, in place of printing it on the first line only |
| **`max`** · **`min`** | the largest and smallest value |
| **`enumerate`** | count the values rather than total them |
| **`percentage`** | express as a percentage |
| **`calc`** | evaluate an I-type against the totals |
| **`break.on`** *field* | start a new subtotal group when the field changes |
| **`break.sup`** *field* | break on a field without printing it |
| **`grand.total`** *"text"* | label the final total line (`caption` was a second name and was removed in 2.0-0) |

`break.on` is what turns a flat listing into a report with subtotals; the field
it breaks on almost always wants to be a sort key as well, or the groups come
out scattered.

**An `X` among a break field's control codes saves the field's previous value.**
The I-types of that line can read it as `@bpv`: the value the field had on the
last record before the break. It is empty on a field without `X`.

A report sent to the default printer (`lptr`) closes a printer that was already
active when the report began — a program's own `printer on`, say — so the report and
the program's output are **two print jobs**. (`option query.merge.print`, which kept them
as one, was removed in 2.0-0, as were `query.footer.pause` and `paginate.on.heading`.)

## Taking only some of the records

| | |
|---|---|
| **`sample`** *n* | the first *n* records |
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
| **`no.page`** | do not pause at the end of each screen (`nopage` was a second spelling and was removed in 2.0-0) |
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
| **standard** | `count` `list` `list.item` `list.label` `scan` `search` `show` `sort` `sort.label` `sum` |
| **programmer** | `reformat` `sreformat` `sort.item` |

Reading and reporting are available to every account; the two verbs that
**write** their result into another file are not.

## See also

[SD TCL - Select Lists](22-sd-tcl-select-lists.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html) ·
[SD Basic - String Functions](04-sd-basic-string-functions.html).

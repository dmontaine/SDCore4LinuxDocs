Title: SD Basic - CSV Files
Subtitle: Reading and writing comma-separated data without hand-rolling the quoting.

SD has statements that read and write CSV directly, and they handle the two
things that make hand-written CSV code wrong: a separator inside a field, and a
quote inside a field. This page covers them.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## Writing

```
writecsv value1, value2, ... to file.variable {delimiter d} {quote q} {escape e} then ... else ...
printcsv {on print.unit} value1, value2, ... {:}
```

`writecsv` writes one line to a **sequential** file — see
[SD Basic - Sequential Files](10-sd-basic-sequential-files.html) for opening
one. `printcsv` sends the same thing to the terminal or a print unit.

The three optional clauses, in any order, come **after the file variable** and
name the dialect of that one statement: the character between the fields, the
character that encloses a field, and an escape character. Each takes an
expression and uses its first character; one that is left out is what
`csv.mode` has set for the program (see below). `writecsv 'a;b', 'c' to f
delimiter ';'` writes `"a;b";c`. A field that holds a line break is enclosed in
quotes, as RFC 4180 asks.

**The quoting is done for you, and it is conformant.** For three values, one
containing a comma and one containing quotes:

```
writecsv 'a', 'b,c', 'say "hi"' to f
```

the file receives, byte for byte:

```
a,"b,c","say ""hi"""
```

A field is quoted only when it needs to be, an embedded quote is doubled, and
the result is what RFC 4180 specifies. **Do not build this by hand** — the
common mistakes are quoting nothing, quoting everything, and escaping a quote
with a backslash, and each produces a file that opens wrongly in a spreadsheet
rather than failing visibly.

A trailing colon on `printcsv` suppresses the line terminator, so several
statements can build one row.

```
matwritecsv matrix to file.variable {delimiter d} {quote q} {escape e} then ... else ...
```

`matwritecsv` is `matreadcsv` the other way: **one line**, made of every element
of a dimensioned matrix in storage order, each quoted as `writecsv` quotes, joined
with the separator `csv.mode` has set (or the one the `delimiter` clause names). A matrix of one empty element writes a
blank line. `on` may be written for `to`, and one of `then` and `else` is
needed; a failed write takes `else`. **openQM's `encoding` clause and `on error`
are not supported**: SD has no character encodings of files, and the write is
the same `writeseq` it always is.

## Reading

```
readcsv from file.variable {delimiter d} {quote q} {escape e} to variable1, variable2, ... then ... else ...
inputcsv variable1, variable2, ...
matreadcsv matrix from file.variable {delimiter d} {quote q} {escape e} then ... else ...
```

| | |
|---|---|
| `readcsv` | one row from a sequential file into named variables |
| `inputcsv` | the same, from the terminal |
| `matreadcsv` | one row into a dimensioned matrix, one field per element |

`readcsv` and `matreadcsv` take the same three clauses as `writecsv`, after the
file variable, to read a file in another dialect: `readcsv from f delimiter ';'
to a, b, c`. A reader's default is a comma, a double quote and no escape
character, **whatever `csv.mode` says** — the clauses are how a reader names its
dialect. With an escape character `e`, `e` followed by a quote inside an
enclosed field is that quote; a doubled quote is read either way.

**A row may be more than one line.** A quoted field can hold a line break, and
`readcsv` and `matreadcsv` read on to the next line of the file while a quote is
still open, so `x,"line1` and `line2",y` is **one** row of three fields, the
break kept as a line feed. A quote that is never closed gives the row as far as
the end of the file, and the next read takes `else`. A quote in the middle of
an unquoted field is not an opening quote.

The line written above, read back with `readcsv from f to v1, v2, v3`, gives
exactly

| | |
|---|---|
| `v1` | `a` |
| `v2` | `b,c` |
| `v3` | `say "hi"` |

— a clean round trip, with the quoting removed and the embedded comma and
quotes restored.

`readcsv`'s `else` branch is end of file, as `readseq`'s is.

**The number of variables is fixed at compile time and the data is not.**
A row with more fields than you named loses the extras silently; one with fewer
leaves the trailing variables empty, which is indistinguishable from a row that
genuinely had empty fields. If the width varies, use `csvdq()` below and count
what came back.

## Splitting a line you already have

```
csvdq(line {, delimiter {, quote {, escape}}})
dparse.csv line, delimiter, variable1, variable2, ...
```

**`csvdq()` is a de-quoter, not a quoter. the name reads the other way.**
It takes one CSV line and returns its fields separated by **field marks**,
honouring the quoting:

| Call | Result |
|---|---|
| `csvdq('plain')` | `plain` — one field, unchanged |
| `csvdq('has,comma')` | `has` and `comma` — **two fields** |
| `csvdq('has"quote')` | `hasquote` — the quote was consumed as quoting |
| `csvdq('a;b', ';')` | `a` and `b` |
| `csvdq("a;'b;c';d", ';', "'")` | `a`, `b;c` and `d` — the quote is the apostrophe |

The third and fourth arguments name the quote and escape characters of another
dialect (a null string is the double quote and no escape character).

So it is the function to reach for when a line arrived from somewhere else and
you want it as a dynamic array:

```
fields = csvdq(line)
n = dcount(fields, @fm)
for i = 1 to n
   ...
next i
```

**There is no function that quotes a single field.** To produce CSV a line at a
time, use `writecsv` or `printcsv`, which do it as part of writing; to produce
the text of a whole file, use `csvbuild()` below.

`dparse.csv` does the same split but assigns straight into named variables.
`dparse.csv 'x,"y,z",w', ',', p1, p2, p3` gives `x`, `y,z` and `w` — the
quoted comma correctly kept inside the second field.

## The separator

Every statement here defaults to a comma. `csvdq()` and `dparse.csv` take the
separator as an argument, for a file that uses something else — some systems
write a semicolon. `writecsv` and `printcsv` take theirs from `csv.mode`.

### `csv.mode`

```
csv.mode mode {, delimiter {, quote {, escape}}}
```

Sets how `writecsv`, `printcsv` and `matwritecsv` build a line, and the
character between the fields, the character that encloses a field and the
escape character. *mode* is 1, 2 or 3:

| mode | a field is put in double quotes when |
|---|---|
| 1 (the default) | it holds the quote character, the delimiter, the escape character, a carriage return or a line feed — the RFC 4180 rule |
| 2 | it is not empty and not a number |
| 3 | always, an empty one too |

The quote character inside a quoted field is written twice in every mode, or,
when an escape character is set, once with the escape character before it (the
escape character itself is escaped the same way). The delimiter replaces the
comma and the quote replaces the double quote; a null string is the default,
and only the first character of a longer string is used. The escape character
is none unless it is given. A mode outside 1 to 3 is ignored.
`system(1043)` and `system(1046)` give the current mode and delimiter, and
`system(1090)` and `system(1091)` give the quote and the escape character.

```
csv.mode 2, ';'
printcsv 'x', 7, 'a;b'      ;* "x";7;"a;b"
```

The setting goes with the program: a subroutine you call starts with yours, a
change it makes is undone when it returns, and a command started with `execute`
starts at the defaults and gives yours back afterwards. `readcsv`, `inputcsv`
and `dparse.csv` are not affected.

> **A file whose separator is a semicolon is still called CSV by the program
> that produced it.** Look at a line before assuming the separator, and take it
> from configuration rather than hard-coding it.

## A whole CSV text: `csvparse()`, `csvbuild()` and `csvopen()`

```
csvparse(text {, mode {, dialect}})
csvbuild(data {, mode {, dialect}})
csvopen(line {, delimiter {, quote {, escape}}})
```

`csvparse()` reads the **text of a whole CSV file** (one string, from `osread`
or a socket) into a [data collection](05b-sd-basic-data-collections.html)
in one call, and `csvbuild()` writes one back. *dialect* is a string of up to
three characters: the delimiter, the quote and the escape character; a
character left out is a comma, a double quote and none. Line ends in the text
may be CRLF, LF or a lone CR, a quoted field may hold a line break, and a blank
line is skipped.

*mode* adds the numbers below together:

| Constant | Value | For | Meaning |
|---|---|---|---|
| `csv$header` | 1 | both | `csvparse`: the first row names the columns. `csvbuild`: write a header row |
| `csv$number` | 2 | parse | a field that is a number becomes a number (`007`, `.5`, `+4` and an empty field stay text) |
| `csv$dynamic` | 4 | both | a dynamic array (rows by field mark, fields by value mark) instead of a collection |
| `csv$keepblank` | 8 | parse | a blank line is a row of one empty field |
| `csv$noheader` | 16 | build | no header row even for rows that have names |
| `csv$crlf` | 32 | build | end each line with CR and LF (the default is LF) |
| `csv$quote2` | 64 | build | enclose every field that is not a number |
| `csv$quote3` | 128 | build | enclose every field |

(The constants are in `keys.h`; `$include keys.h` to use them.)

Without a header, `csvparse()` gives an **array of rows**, each row an array of
strings. With `csv$header` it gives an object with **`columns`** (the names, in
the order of the file; a column with no name, or a field beyond the header, is
named `_` and its number, and a column used twice keeps the later value) and
**`rows`** (an array of objects, one for each row):

```
$include keys.h
text = 'id,name,qty' : char(10) : '1,"Smith, A",3' : char(10) : '2,Jones,'
t = csvparse(text, csv$header + csv$number)
crt inmat(t{'rows'})                   ;* 2
crt t{'rows', 1, 'name'}               ;* Smith, A
crt jtype(t{'rows', 1, 'qty'})         ;* number
crt jbuild(t{'columns'})               ;* ["id","name","qty"]
```

`csvbuild()` takes an array of arrays, an array of objects (the header row, if
asked for, is the names in order of first appearance, each object listing its
names in order of name), or `{columns, rows}` (the columns in the order you give
them); with `csv$dynamic` it takes a dynamic array. A number is written as a
number, `true` and `false` as those words and `null` as an empty field. It
quotes as `csv.mode` says, and takes its delimiter, quote and escape character from `csv.mode`
unless *dialect* names them; `csvparse()` does **not** read `csv.mode`.

Both functions give a null string on an error and say why in `status()`:

| `status()` | Meaning |
|---|---|
| 1020 | (`csvparse`) a quote is never closed; `inmat()` is the position of the quote that opened it |
| 1019 | (`csvbuild`) the data is not a collection, or a value in it is itself a collection |

`csvopen(line, ...)` is 1 when a quoted field is still open at the end of
*line*, which is how `readcsv` knows to join the next line on; use it when you
read a CSV file with `readseq` and build the rows yourself.

## Line endings

CSV written by SD is documented as following **RFC 4180**, which specifies
CRLF. **Unlike SD Core for Windows, this port's sequential-file writing —
which `writecsv` shares — uses LF only**, the platform's own convention
(see [SD Basic - Sequential Files](10-sd-basic-sequential-files.html)); if
another program's CSV reader is strict about RFC 4180's CRLF, check it
against real output rather than assume the pair is there. Reading accepts
either.

## What is not here

Nothing in the CSV group has been removed from this port. The whole group is
**new relative to the OpenQM 2.6.6 documentation** — none of the first seven
names appears in its by-type list, so the old help is no guide to them, and the
three functions of the section on whole texts are SD's own.

Two behaviours were fixed in this port and are worth knowing if you are moving
files across from the Linux original:

| | |
|---|---|
| **reading** | a conformant CRLF file used to lose its last field on every row, because the stray CR stayed attached to it |
| **writing** | output is now CRLF, so a file SD produced conforms to the RFC its own documentation claims |

## See also

[SD Basic - Sequential Files](10-sd-basic-sequential-files.html) ·
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html) ·
[SD Basic - String Functions](04-sd-basic-string-functions.html) ·
[SD Basic - JSON and Collection Files](05c-sd-basic-json-and-collection-files.html) ·
[SD Basic - XML](05d-sd-basic-xml.html) ·
[SD TCL - The Query Processor](21-sd-tcl-query-processor.html) (the `csv` and `delimiter` keywords) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html) (`import.csv` and `convert.data`).

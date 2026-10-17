Title: SD Dictionaries - Structure
Subtitle: The dictionary file: every record type, and every field of each one.

A dictionary is a file that describes a data file. It holds the field
names, the field numbers they point at, the format in which they print,
and the expressions that compute values that are not stored. Every
`LIST`, `SELECT`, `SORT` and `COUNT` command reads the dictionary to find
out what to read and how to display it. This page is about the record
types in a dictionary, their fields, and how they relate to the data file.

SD folds case, so a field name may be typed in either case. In the
tables, *italics* mark something you supply and **bold** marks a word
typed as it stands; braces mark an optional part.

> **Every record on this page was read from the system dictionaries on SD
> Core for Linux.** The `voc.dic` dictionary — the dictionary of
> the VOC — is a stock file whose records illustrate every type.

## What a dictionary is

Every data file has a dictionary. The VOC record for a file of type `F`
carries two paths: field 2 is the data path, field 3 is the dictionary
path. If field 3 is empty, the file has no dictionary and cannot be used
by the query processor — `LIST` on it fails with *"no dictionary"*.

The dictionary is itself a hashed file. Its operating-system name is the
file name with `.dic` appended — `bp.dic`, `voc.dic`, `stock.dic`. The
`dict` verb opens it: `dict` *file.name* is the same as opening
`DICT` *file.name* from BASIC.

The system file `dict.dic` in `@SDSYS` is the dictionary *of* the
dictionary — its own dictionary, which describes the fields a dictionary
record has. It is what `dict dict.dic` reads.

## The dictionary record types

Field 1, character 1, is the type. The rest of field 1 is free text and
is ignored, so a record whose field 1 reads `D Data for stock qty` is
type `D` and the rest is a comment.

| Type | Name | What it does |
|---|---|---|
| `D` | direct | references a field number in the data record |
| `E` | element | like `D`, but field 2 is the **path** of an element of a **data collection** record instead of a field number — see [SD TCL - Data Collection Files](20a-sd-tcl-collection-files.html) |
| `I` | indirect | an expression that returns a value — a virtual field |
| `C` | calculated | like I but compiled with the BASIC compiler and returning via `@ANS` |
| `A` | A-type | Pick-style data definition, with a different field layout |
| `S` | S-type | identical to `A` in SD — kept for compatibility |
| `L` | link | names another file and how to find the record in it, so that a query or an I-type can use its fields as `link%item` |
| `PH` | phrase | a stored fragment substituted into a query command line |
| `X` | text | miscellaneous data — not a field definition |

**`A` and `S` are the Pick layout, not the SD layout.** They carry the
same information as `D` but in different fields — field 3 holds the
display name, field 7 the conversion, field 8 the correlative, field 9
the justification, field 10 the width. SD supports them because
applications imported from Pick use them. New dictionaries should use
`D` and `I`.

## The D record — a direct field reference

```
001  D
002  2
003
004  F2
005  5L
006  S
```

This is `F2` from `voc.dic`. Field 1 is `D`, field 2 is the field number
in the data record, and the remaining fields control how it appears in a
query.

| Field | Name | What it holds |
|---|---|---|
| `1` | type | `D`, optionally followed by a comment |
| `2` | location | the field number in the data record |
| `3` | conversion | a conversion code, or empty |
| `4` | display name | the column heading; `\` for none; `'R'` prefix right-justifies |
| `5` | format | width and justification — see below |
| `6` | S/M | `S` for single-valued, `M` for multivalued |
| `7` | association | a name grouping multivalued fields, or empty |
| `8` | user | free for the application — SD does not read it |

### Pseudo-fields

Field 2 is not always a literal field number. Three values have special
meaning:

| Location | What it reads |
|---|---|
| `0` | the record id (`@ID`) |
| `9998` | `@NI` — the number of items in a multivalued field set |
| `9999` | the record length in bytes (`@NB`) |

A dictionary record with location `0` is how the record id appears in a
query. The `@ID` record in `voc.dic` has location `0` and display name
`@ID`.

### The format field

Field 5 is the format specification — the column width and justification
the query processor uses when it prints the field. It is a compact
syntax:

| Syntax | Meaning |
|---|---|
| *n*`L` | left-justified, *n* characters wide |
| *n*`R` | right-justified, *n* characters wide |
| *n*`T` | text — left-justified, wrapping at word boundaries |
| *n*`C` | centred, *n* characters wide |
| *n*`L`*d* | left-justified with *d* decimal places (numeric) |
| *n*`R`*d* | right-justified with *d* decimal places (numeric) |

`5L` means five characters, left-justified. `20L` means twenty
characters, left-justified. `10R2` means ten characters, right-justified,
two decimal places. The format field is also what `FMT()` uses in BASIC.

### Single and multivalued

Field 6 is `S` or `M`. A single-valued field holds one value per record;
a multivalued field holds many, separated by value marks. The query
processor prints each value of a multivalued field on its own line
unless the field is in an **association**.

### Associations

Field 7 names an association — a group of multivalued fields whose
values are parallel. If `qty` and `price` are both multivalued and both
carry association `LINE.ITEM`, the query processor prints them side by
side: `qty` value 1 next to `price` value 1, and so on.

**An association is a name, not a structure.** The fields that share
one are linked by having the same name in field 7, not by anything stored
separately. There is no association record.

## The I record — an indirect field

```
001  I
002  IF DATA.NAME # '' THEN SUBR("!FTYPE",DATA.NAME) ELSE ''
003
004  FType
005  8L
006  S
```

This is `FTYPE` from `voc.dic`. Field 1 is `I`, field 2 is an expression
in SD BASIC syntax, and the remaining fields are the same as for a
D-record. The expression is compiled to object code, which is stored in
field 16 onward, and executed when the query processor needs the value.

### What an I-type expression can use

An I-type expression is a single BASIC expression — not a program. It can
use:

| Variable | What it holds |
|---|---|
| `@ID` | the record id |
| `@RECORD` | the entire data record as a dynamic array |
| *n* or `F`*n* | field *n* of the data record — `F2` is field 2 |
| `@NI` | the number of values in the longest multivalued field |
| `@NB` | the record length in bytes |
| `@FILE.NAME` | the name of the file being queried |
| `@USER.NO` | the user number of the session |
| `@PATH` | the account path |

It can call `SUBR()` to invoke a catalogued subroutine, use `TRANS()` to
read from another file, and use any BASIC function — `LEN()`, `FIELD()`,
`RAISE()`, `OCONV()`, `ICONV()`, `COUNT()`, `SUM()`, `DATE()`, `TIME()`
and the rest. It cannot run loops or call statements that take a
variable number of arguments.

### Compilation

An I-type is compiled the first time it is used after it is written or
edited. The compiled object is stored in field 16 onward of the same
dictionary record, and a stamp in field 15 tells the query processor
whether the object is current. **Editing field 2 invalidates the
object.** The next query recompiles it. If the expression has a syntax
error, the query reports it and the field appears empty.

### The field 15 stamp

Field 15 is the system information field. SD stores a hash of the
expression source there when it compiles the I-type. When a query opens
the dictionary, it compares the hash to the source — if they differ, the
I-type is recompiled. This is why field 15 has a large number in a stock
I-type record and is empty in a D-type record.

## The C record — a calculated field

A C-type is like an I-type but is compiled with the full BASIC compiler
rather than the I-type expression compiler. The expression in field 2 is
a complete BASIC program that returns its result in `@ANS`. C-types are
rare in stock dictionaries — I-types cover most computed fields — but
they exist for compatibility with applications that use them.

## The A record — a Pick-style field

An A-type (or S-type) uses a different field layout:

| Field | Name | What it holds |
|---|---|---|
| `1` | type | `A` or `S`, optionally followed by a comment |
| `2` | location | the field number in the data record |
| `3` | display name | the column heading |
| `4` | association | a name grouping multivalued fields |
| `5`-`6` | | not used |
| `7` | conversion | a conversion code |
| `8` | correlative | a correlative code — like a mini I-type |
| `9` | justify | `L` or `R` |
| `10` | width | column width |

The correlative in field 8 is a Pick-style expression — a short code
that transforms the field value before display. SD compiles
correlatives the same way it compiles I-types, storing the object in
field 16 onward. **Field 8 may also begin with an `if` expression**
(`if 3 > "5" then "big" else "small"`), which is taken as an A-correlative
without the `a;` in front; anything else that does not begin `a` or `f` is
a conversion code, as before.

## The PH record — a phrase

```
001  PH
002  GRAND.TOTAL "'L'"
```

A phrase is a stored fragment substituted into a query command line
wherever its name appears. `PH` records in a dictionary work the same
way as `PH` records in the VOC — the difference is that a dictionary
phrase is scoped to the file whose dictionary holds it.

## The L record — a link

An L-type names another file and says how to find the record in it, so
that fields of the other file can be used in a query or in an I-type
without writing a `TRANS()` for each one.

| Field | What it holds |
|---|---|
| `1` | `L`, optionally followed by a comment |
| `2` | the **id expression**: an I-type expression that gives the id (or ids) of the record in the other file, from the record being listed |
| `3` | the **file name**: the file whose dictionary is searched for the item named after the link, and, unless field 4 says otherwise, the file read |
| `4` | the **file expression**, optional: an I-type expression that gives the name of the file actually read, for a set of files that share one dictionary (sales kept in a file for each region, say). Field 3 still names the one whose dictionary is used |

A book file whose record ids are a title id and a copy number, `T1-2`,
with the titles in another file:

```
001  L
002  FIELD(@ID, "-", 1)
003  TITLES
```

kept as the record `TTL` of the book file's dictionary, is used as
`TTL%TITLE`, the link, a percent sign and the name of an item in the
dictionary of `TITLES`:

```
LIST BOOKS TTL%TITLE TTL%AUTHOR
```

The same name is a field of an I-type of the book file's dictionary: an I-type whose
expression is `TTL%TITLE`, or `UPCASE(TTL%AUTHOR)`, or `COPY : "/" : TTL%TITLE`, works
as the same expression written with `TRANS()`:

```
TRANS("TITLES", FIELD(@ID, "-", 1), TITLE, "X")
```

The item may be a D, I, C, A, S or E item of the other file. It takes the column
heading, format, conversion and association that item has, unless the I-type or the
query says otherwise. A query treats the result as multivalued, because the id
expression may give several ids.

**A link can reach through another link.** If the file the link names has a link of its
own, the two names are joined: with `OUT`, a link from `READERS` to `BOOKS` whose id
expression is `LOANS`, the titles on loan are `OUT%TTL%TITLE`:

```
LIST READERS OUT%TTL%TITLE
```

At most ten links may follow one another.

**What to know.** A link is worked out when an I-type is compiled, not each time it
is used: the compiled I-type has the `TRANS()` in it. **After a link is changed, the
I-types that use it must be compiled again** (`cd`, on page 24, does it). A query that
names a link directly is compiled each time it is run and is not affected. A link's
expressions cannot be compound (no semicolons), the item name after the percent sign
must be a name as it would be written in an I-type (a name with a hyphen in it is not),
and **a dictionary record whose id has a percent sign in it is found first**:
`TTL%TITLE` is that record if there is one, and a link only if there is not. An item that
is not in the other file's dictionary, a link with no file or no id expression, an
expression with a semicolon, or an item of a type that holds no data, are refused with a
message that names the link or the item.

## The X record — text

An X-record in a dictionary is miscellaneous data — not a field
definition. It can hold anything the application wants to store by name
in the dictionary.

## Continued in

[SD Dictionaries - Using and Creating](33a-sd-dicts-in-use.html) — how the
query processor uses a dictionary, the system dictionaries, and creating one.

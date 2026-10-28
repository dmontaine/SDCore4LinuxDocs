Title: SD TCL - Data Collection Files
Subtitle: A file whose records are collections: describing their elements in the dictionary, and listing, selecting, indexing, copying and editing them from the command prompt.

A **data collection file** holds records that are
[data collections](05b-sd-basic-data-collections.html) — named elements, arrays and
nested collections — instead of fields, values and subvalues. On disk each record is JSON
text. Everything underneath is an ordinary hashed file, so locking, transactions,
`configure.file`, `clear.file`, `delete`, `count`, `list.item` and `dump` work on it as
they do on any file. This page is about the commands; a program reads and writes such a
record with `read` and `write` (see
[SD Basic - JSON and Collection Files](05c-sd-basic-json-and-collection-files.html)).

SD folds case, so a command may be typed in either case. Commands are shown here in lower
case. In the tables, *italics* mark something you supply and **bold** marks a word typed
as it stands; braces mark an optional part.

## Making the file

```
create.file name collection
```

```
Created DICT part as stock.dic
Created DATA part as stock
Added default '@id' record to dictionary
```

The **dictionary is an ordinary one** (there is an `@id` item, as always). `fileinfo(f,
fl$collection)` is 1 for the file from a program. A collection file is not a different place to
keep things from the rest of SD — its records are simply read as collections.

## Describing an element: the E-type dictionary item

A record has no field numbers, so a dictionary item names an element by its **path**. The new
item type is **E**: a D-type item whose field 2 is an element path instead of a field number.

| Field | Contents |
|---|---|
| 1 | `E` |
| 2 | the **path** of the element: names and array positions separated by `/` |
| 3 | conversion |
| 4 | heading |
| 5 | format, such as `10L` or `5R` |
| 6 | `S` single-valued, `M` multivalued |
| 7 | association |

**A path may have one or two asterisks** (`orders/*/item`): an asterisk stands for every
element of an array, and the item is **multivalued** — one value for each element, and with a second
asterisk a subvalue for each element of the array below. An element that is not there is a
null value, not an error.

For the record `{"name":"Smith","address":{"city":"Albany"},"orders":[{"item":"bolt","qty":4},
{"item":"nut","qty":9}]}`, items made like this:

| Item | Path | Format | S/M |
|---|---|---|---|
| `name` | `name` | `10L` | `S` |
| `city` | `address/city` | `10L` | `S` |
| `items` | `orders/*/item` | `10L` | `M` |
| `qty` | `orders/*/qty` | `5R` | `M` |

give

```
list stock name items qty
```

```
stock......   Name......   Items.....   Qty..
1001          Smith        bolt             4
                           nut              9
1002          Jones        gear             2
1003          Green
```

**The query commands use E-type items as they use D-type ones** — `list`, `sort`, `select`,
`count`, `search` and the rest, in headings, in `with` and `by` clauses, and in conversions:

```
list stock with city = "Boston" name
```

```
stock......   Name......
1002          Jones
```

```
sort stock by element "name" name
```

```
stock......   Name......
1003          Green
1002          Jones
1001          Smith
```

A **D-type item with a field number above 0 is refused** on a collection file, with a message that says to
use an E-type item, and an **E-type item is refused on any other file**. `@id` works as always. An
**I-type** item can read an element too: `@record{'address/city'}`, or `trans(stock, @id, name, 'X')` with the
item name unquoted.

## The `element` keyword: no dictionary needed

```
list file element "detail/*/prodno" ...
list file ... with element "ship" = "Dock B"
sort file ... by element "n"
```

`element` names an element of a collection file by its path, the way `a` *n* or `f` *n* names a field, so a query does not need
a dictionary item for every element it touches. It can be used wherever a field name can: in the display list, in `with` and `when`
clauses, with `by`, `by.dsnd` and `by.exp`, with `sum`, `total` and `break.on`, and in `count` and `select`. The usual
qualifiers (`as`, `col.hdg`, `fmt`, `conv`, `multi.value`, `single.value`) work on it.

```
list stock element "orders/*/item" element "address/city"
```

```
stock......   orders/*/item   address/city
1001          bolt             Albany
              nut
1002          gear             Boston
1003
```

```
count stock with element "address/city" = "Albany"
```

```
1 record(s) counted
```

The path is the one a program uses. **A name is case sensitive** and keeps the case it is typed
in; quotes are needed only around a path that holds a blank or a character the command parser splits on.
With no `fmt` the item is **10 characters, left justified, and its heading is the path.** Left justified means that
a sort or a test on a number compares characters — `by element "n"` puts 10 before 3 — so add `fmt "5R"` (and `as`, to
sort by the formatted item) for numbers.

```
list stock element "orders/*/qty" fmt "5R" as qty
```

Used on any file that is not a collection file, `element` says *ELEMENT can only be used with a data collection
file*, and with no path after it *ELEMENT path not found where expected*. **`element` is a keyword**, so a dictionary
item that happens to be called `element` should be given another name.

## Looking at and changing a record

```
ct stock 1001
```

```
{
  "address": {
    "city": "Albany"
  },
  "name": "Smith",
  "orders": [
    { ...
```

| | |
|---|---|
| `ct` | the record as **JSON, one element to a line**, indented (the `jb$pretty` layout) |
| `list.item` | the record as its compact JSON text |
| `ed` file id · `edit` | the record shown as `ct` shows it, **a line to an element**, filed back as JSON text. The file makes a collection of what comes back, and refuses it — *Write error 1020 - Data not saved* — if it is not a JSON object or array, leaving the stored record as it was |
| [`ced`](27b-sd-tcl-ced.html) | a full-screen editor that shows the elements of one level and their **types** |
| `copy` | between two collection files the collection is copied; **from** a collection file **to a file that is not one**, the record's JSON text is written (in the compact form the file holds); **to** a collection file, the JSON text of a record is made into a collection |
| `compare.files` | collection records are compared **as their JSON text**, in which the names are always in order, so two equal collections are the same |
| `search` · `scan` | look at the JSON text of the record |

**Text that is not JSON copied into a collection file is refused** — *Error 1020 writing record* — and stops the
copy, as any write error does (with `deleting` the source record that was not copied is not deleted).
`unload` into a collection file is the same, and `load` of lines from a collection record gives the lines of its JSON.
**OpenQM's rule is that a copy goes between two collection files or between two files that are not.** SD **also copies between the two
kinds**, a deliberate addition, so that a collection file can be exported to, and loaded from, text files, which a directory
file holds as files on disk.

## Indexes on an element

An E-type item can be indexed as a D-type item can, **including one whose path has an asterisk** (every element becomes a
key). The index is kept up to date as records are written and deleted, and a query with a `with` clause on the item uses it.

```
create.index stock city
build.index stock city
selectindex stock city Boston
list stock city
```

```
Added index for city
Building index 'city'...
3 records processed
Populating index...
1 record(s) selected to select list 0
stock......   City......
1002          Boston
```

See [SD TCL - Alternate Key Indexes](23-sd-tcl-alternate-key-indexes.html) for `selectindex`. A D-type item with a
field number cannot be indexed on a collection file, and an E-type item cannot be indexed on any other file.

## Triggers, the API and the debugger

**A read or write trigger on a collection file is always given the collection**, and what a pre-write trigger
changes is what is stored; a trigger that refuses a write (a non-zero `@trigger.return.code`) stops it as usual, and the
post-write trigger does not run. **The API server sends a client the JSON text of a record it reads from a collection file**
(this has been compiled but not yet run against a live API server). **The debugger** shows a collection variable as its JSON,
and `/c{path}` shows one element: see [SD Basic - Debugging](17-sd-basic-debugging.html).

## What does not work, and what was not tried

`readv` and `writev` of a field number have no meaning on a collection file, and `matread` is refused. **`analyze.file` does not
say that a file holds collections**, and `micro` was not tried on a collection record: use `ced` or `ed`.

## See also

[SD Basic - Data Collections](05b-sd-basic-data-collections.html) ·
[SD Basic - JSON and Collection Files](05c-sd-basic-json-and-collection-files.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html) ·
[SD TCL - The Query Processor](21-sd-tcl-query-processor.html) ·
[SD Dictionaries - Structure](33-sd-dicts-structure.html).

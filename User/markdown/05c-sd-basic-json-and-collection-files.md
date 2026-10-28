Title: SD Basic - JSON and Collection Files
Subtitle: Turning a collection into JSON text and back, keeping collections in files, and joining a record that another record points to.

This page continues [SD Basic - Data Collections](05b-sd-basic-data-collections.html).
It covers the two functions that convert a collection to and from text, JSON Lines files,
the functions that merge, patch, search and check a JSON document, the kind of
file whose records **are** collections, and the functions that join one record to
another. The commands that work on such a file from the command prompt are on
[SD TCL - Data Collection Files](20a-sd-tcl-collection-files.html).

SD folds case, so a program may be written in either case. Keywords are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part.

## JSON: `jparse()` and `jbuild()`

```
c = jparse(text {, mode})
text = jbuild(c {, mode})
```

`jparse()` reads **a JSON object or array**; `jbuild()` writes one. An object becomes a
collection and an array an array. A string is a string; a number is an integer when it
is whole and fits in 32 bits, and a floating point number otherwise; `true`, `false`
and `null` are kept as such, so that `jbuild()` writes them back as they were (read
from the collection they are 1, 0 and a null string, as in the previous page).

```
p = jparse('{"b": [1, 2, {"c": true}], "a": null, "n": 3.5, "s": "xA"}')
crt jbuild(p)
crt jtype(p{'b'}) : ' ' : jtype(p{'b/3/c'}) : ' ' : p{'b/3/c'} : ' [' : p{'a'} : '] ' : jtype(p{'n'})
```

```
{"a":null,"b":[1,2,{"c":true}],"n":3.5,"s":"xA"}
array boolean 1 [] number
```

**`jbuild()` writes compact text with no spaces, and the names in order**, so two equal
collections give the same text. Strings are escaped; the mark characters, control
characters and 8-bit characters become `\u00XX`, which `jparse()` reads back as the same
byte.

What `jparse()` takes: spaces, tabs, returns, line feeds and all five mark characters between
elements are ignored. Names and strings may be in single or double quotes. `\uXXXX` is the
single byte XX when it is 255 or less (so marks and 8-bit characters come back as they
went out) and UTF-8 above that. Nesting is limited to 500 levels. A name that appears twice takes
the later value.

**When it cannot,** `jparse()` returns a null string, `status()` is **1020** and `inmat()` is the
position of the character where it gave up. `jbuild()` of a value with no JSON form (a file
variable, say) or of a collection that contains itself returns a null string and `status()` is
**1019**. Both numbers are in the `err.h` include (`ER$PARSE.ERROR`, `ER$BUILD.ERROR`).

```
q = jparse('this is not json')
crt '[' : q : '] status ' : status() : ' at ' : inmat()
```

```
[] status 1020 at 1
```

### The modes

A mode is a number made by **adding** the names below; they are in the `keys.h` include and
the values are SD's own.

| | `jparse()` | |
|---|---|---|
| `jp$null` | 1 | a JSON null is read as a null string |
| `jp$unquoted.name` | 2 | names may have no quotes |

| | `jbuild()` | |
|---|---|---|
| `jb$invalid` | 1 | a value with no JSON form is written as `null` instead of failing |
| `jb$null` | 2 | a null string is written as `null` |
| `jb$num` | 4 | a string that is a JSON number is written as one |
| `jb$squote.name` | 8 | names in single quotes |
| `jb$noquote.name` | 16 | names with no quotes |
| `jb$squote.value` | 32 | string values in single quotes |
| `jb$noquote.value` | 64 | string values with no quotes |
| `jb$pretty` | 128 | one element to a line, indented — SD's own, the layout `ct` shows |

```
crt jbuild(jparse("{'a':1,'b':'x'}"), jb$squote.name + jb$squote.value)
```

```
{'a':1,'b':'x'}
```

A collection that holds a **file variable** is written to a file with the element stored as a
null, and `jbuild(c, jb$invalid)` asks for the same; without the mode it fails with 1019.

### The indent of the pretty layout

```
text = jbuild(c, jb$pretty, indent)
```

`jb$pretty` puts one element to a line and indents each level by **two spaces**. A third
argument names the text put in front of an element once for each level — up to 16 spaces
and tabs, `char(9)` for a tab. Naming an indent asks for the pretty layout even when the
mode does not say `jb$pretty`. An indent that is not white space, or a null string, is the two
spaces.

```
c = jparse('{"a":[1,{"b":2}]}')
crt jbuild(c, jb$pretty, '    ')
```

```
{
    "a": [
        1,
        {
            "b": 2
        }
    ]
}
```

## JSON Lines: `readjson` and `writejson`

```
readjson variable from file.variable then ... else ...
writejson collection to file.variable then ... else ...
```

A **JSON Lines** file has one JSON value on each line. `readjson` reads the next line of a
sequential file ([opened with `openseq`](10-sd-basic-sequential-files.html)) and puts it, as
`jparse()` would, in *variable*; `writejson` writes a collection as one compact line, a line
feed inside a string written as `\n`, so that it is one line. `to` may be written `on`.

`readjson` skips a blank line. Its `else` branch is the end of the file (`status()` is 3006) or
a line that is not JSON (`status()` is 1020, and the next `readjson` reads the line after it).
`writejson`'s `else` branch is a value that is not an object or an array (`status()` 1020), a
value with no JSON form (1019), or a failed write. The OS-access gate and the edit gates were
asked at `openseq`, as for every sequential file.

```
openseq 'orders.jsonl' to f else stop
loop
   readjson o from f else exit
   crt o{'id'} : ' ' : o{'total'}
repeat
close f
```

## Changing, searching and checking a document

Four functions take a document that is already a collection, or **JSON text**, which is parsed
first. The root of a document is an object or an array, as `jparse()` has it; a bare number or
string is refused (a null string, `status()` 1020). None of them changes its argument.

### `jmerge()` — RFC 7396 merge patch

```
result = jmerge(target, patch)
```

The patch is merged into a copy of the target: a name in the patch whose value is `null` takes
that name out of the target; an object in the patch merges into the object of the same name; any
other value (an array too) replaces. This is the way to apply a partial update:

```
doc = jparse('{"a":"b","c":{"d":"e","f":"g"}}')
crt jbuild(jmerge(doc, '{"a":"z","c":{"f":null}}'))
```

```
{"a":"z","c":{"d":"e"}}
```

A patch that is not JSON gives a null string and `status()` 1020. A merge patch cannot set a
value to `null` (that is what it uses for "remove"); use `jpatch()` for that.

### `jpatch()` — RFC 6902 patch

```
result = jpatch(document, operations)
```

*operations* is an array of objects, applied in order to a copy of the document: `{"op": "add",
"path": "/a/b", "value": 1}` and likewise `remove`, `replace`, `move` and `copy` (these two with
a `"from"`) and `test` (the value at the path must equal `"value"`). A path is a JSON Pointer
(RFC 6901): `/` between the steps, `~1` for a `/` and `~0` for a `~` in a name, **array
elements numbered from 0**, and `-` the place after the last element; the empty path is the
whole document. It is **all or nothing**: if an operation fails the result is a null string,
`status()` is **1023** and `inmat()` is the number (from 1) of the operation that failed.

### `jpath()` — JSONPath (RFC 9535)

```
matches = jpath(document, query)
```

The matches, copied, as an array (empty when nothing matches). The query starts with `$` and
may use `.name` and `['name']`, `*`, `..` (every level below), indexes **from 0** (negative
ones from the end), slices `[1:3]` and `[::-1]`, unions `[0,1]` and filters:

| Query | Matches |
|---|---|
| `$.store.book[*].author` | the author of every book |
| `$..author` | every `author`, at any depth |
| `$..book[-1].title` | the title of the last book |
| `$..book[:2].price` | the prices of the first two books |
| `$..book[?@.price<10].title` | the titles of the books under 10 |
| `$..book[?@.isbn]` | the books that have an `isbn` |
| `$..book[?@.category=='fiction' && @.price>10]` | `&&`, `||` and `!` combine tests |
| `$..book[?length(@.title) > 15]` | the functions are `length()`, `count()`, `match()` and `search()` |

A query that is not well formed gives a null string, `status()` **1024** and `inmat()` the
place it went wrong. **The index numbers are the RFC's, from 0**; the `c{'a/2'}` paths of a
collection (previous page) count from 1.

### `jvalidate()` — JSON Schema

```
faults = jvalidate(document, schema)
```

Checks a document against a JSON Schema (draft 2020-12) and gives an array of the faults found,
**empty when the document is valid**. Each fault is an object with `path` (a JSON Pointer to the
place, empty for the whole document), `keyword` (the schema keyword that failed) and `message`.
The keywords it checks are `type`, `enum`, `const`, `minimum`, `maximum`, `exclusiveMinimum`,
`exclusiveMaximum`, `multipleOf`, `minLength`, `maxLength`, `pattern`, `minItems`, `maxItems`,
`uniqueItems`, `prefixItems`, `items`, `contains`, `minContains`, `maxContains`, `required`,
`properties`, `patternProperties`, `additionalProperties`, `propertyNames`, `minProperties`,
`maxProperties`, `dependentRequired`, `allOf`, `anyOf`, `oneOf`, `not`, `if` with `then` and
`else`, `$ref` (into the same schema: `#` or `#/...`) and a `true` or `false` where a schema is
expected. Every other keyword, `format` included, is let be. A length is a number of bytes: SD
has no character sets.

```
schema = '{"type":"object","required":["name","age"],"properties":{"age":{"type":"integer","minimum":0}}}'
faults = jvalidate('{"name":"Ann","age":-1}', schema)
for i = 1 to inmat(faults)
   crt faults{i, 'path'} : ' ' : faults{i, 'keyword'}
next i
```

```
/age minimum
```

Pattern matching (`pattern`, `patternProperties`, `match()` and `search()` in `jpath()`) uses
POSIX extended regular expressions.

## Collection files

```
create.file name collection
```

A **data collection file** is an ordinary hashed file whose records are collections, held as JSON
text — so locking, transactions, file sizing and everything else underneath work as for any
file. The dictionary of the file is an ordinary one. `fileinfo(f, fl$collection)` is 1 for such a
file (`keys.h`).

| | |
|---|---|
| `read c from f, id` | `c` is a collection (`readu` and `readl` too) |
| `write c on f, id` | the collection is written as JSON text (`writeu` too) |
| `write text on f, id` | text is **accepted if it is a JSON object or an array**, and made into its collection first |

```
execute 'create.file zzcf collection' capturing j
open 'zzcf' to f else stop
w = collection()
w{'name'} = 'Smith'
w{'orders'} = mat()
w{'orders', 1} = collection()
w{'orders', 1, 'item'} = 'bolt'
write w on f, '1001'
write '{"name":"Green"}' on f, '1003'
read r from f, '1001' then crt jtype(r) : ' ' : r{'name'}
write 'not json at all' on f, '1006' on error crt 'refused ' : status()
```

```
collection Smith
refused 1020
```

**Text that is not a JSON object or array is refused** with `status()` 1020 and the stored record is left
as it was. A collection that contains itself cannot be written (1019). **`matread` is refused**
(*This operation cannot be used on a data collection file*), and `readv` or `writev` of a field number
does not make sense — a collection has no fields — and stops the program with *Data cannot be
converted to a string*. A **read or write trigger** is always given the collection: text written to the file is
made into its collection before the trigger runs, so text that is not JSON never reaches it, and what a
pre-write trigger changes is what is stored. The file holds the compact JSON of the collection, whatever layout
the text had.

## Joining a record that another record points to

A **link** is a string in a collection of the form `filename:id`, or `:id` when a file variable is given.
`expand()` reads that record and **puts the collection it gives where the link was**:

```
ok = expand(c{'path'})
ok = expand(c{'path'}, filevar)
```

```
w2 = collection()
w2{'owner'} = 'zzcf:1002'
ok = expand(w2{'owner'})
crt ok : ' ' : w2{'owner/name'}
```

```
1 Jones
```

It returns **1** if the element is now a collection (including when it already was) and **0** if it is not a link, the
file or the record is missing, or the record is not a collection; the element is then left as it was.
The file name is up to the first colon, so an id may have colons in it. **What is joined on is a copy**: writing the
parent back is up to the program.

## Reading a collection with `trans()` and in an I-type

On a collection file `trans()` accepts an **E-type** dictionary item (the next page) for its third argument,
and a program may name any D or E-type item as a string:

```
crt trans('zzcf', '1001', 'name', 'X')
```

```
Smith
```

A multivalued (asterisk) path comes back as it does from any `trans()`, with the marks lowered one
level. A D-type item with a field number gives a null string on such a file, and field -1 gives the whole
record as JSON. In an **I-type** dictionary item, a name that is an E-type item gives that element, and a
collection reference can be written after any value — `@record{'address/city'}`, `@record{'orders', 1, 'item'}`,
and `trans(zzcf, @id, name, 'X')`, with the item name unquoted. The query commands keep the collection as
`@record` for a collection file, so an I-type sees it whole.

## See also

[SD Basic - Data Collections](05b-sd-basic-data-collections.html) ·
[SD TCL - Data Collection Files](20a-sd-tcl-collection-files.html) ·
[SD Basic - File Handling](07-sd-basic-file-handling.html) ·
[SD Basic - XML](05d-sd-basic-xml.html) ·
[SD Basic - CSV Files](11-sd-basic-csv-files.html) ·
[SD TCL - The Query Processor](21-sd-tcl-query-processor.html) (the `json` and `json.lines` keywords) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html) (`import.json` and `convert.data`) ·
[SD TCL - The CED Data Collection Editor](27b-sd-tcl-ced.html).

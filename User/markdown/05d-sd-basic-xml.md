Title: SD Basic - XML
Subtitle: Reading an XML document into a collection, looking in it with XPath, and writing one back.

This page continues [SD Basic - JSON and Collection Files](05c-sd-basic-json-and-collection-files.html).
It covers three functions that turn XML text into a
[data collection](05b-sd-basic-data-collections.html), search it, and turn a collection back into XML
text. To write a **query report** as XML, see the `xml` keyword on
[SD TCL - The Query Processor](21-sd-tcl-query-processor.html); to read a document in the shape
that report writes into the records of a file, see `import.xml` on
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html).

SD folds case, so a program may be written in either case. Keywords are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part.

## An element is a collection

```
x = xparse(text {, mode})
text = xbuild(element {, mode {, indent}})
nodes = xpath(element, query)
```

`xparse()` gives the **root element** of the document as a collection with up to four members:

| Member | Holds |
|---|---|
| `name` | the tag, prefix and all: `svg:rect` |
| `attributes` | an object: the attributes by name. An `xmlns` or `xmlns:p` attribute is an attribute like the rest |
| `text` | the text directly inside the element: entities and character references read, CDATA sections included, line ends made line feeds |
| `children` | an array of the child elements, in the order of the document |

A member that would be empty is left out. White space **between** child elements is not text and is
let go; text that stands alone in an element is kept as it is, spaces and all (`xml$trim`, below,
takes the spaces off). Text around a child element (`<a>x<b/>y</a>`) is kept together: `xy`.
Comments, processing instructions, the XML declaration and a DOCTYPE are read past and kept
nowhere. A byte order mark at the start is let past.

```
x = xparse('<order id="7"><item sku="a1">Bolt &amp; nut</item><item sku="b2"/></order>')
crt x{'name'} : ' ' : x{'attributes', 'id'}
crt inmat(x{'children'}) : ' ' : x{'children', 1, 'text'} : ' ' : x{'children', 2, 'attributes', 'sku'}
```

```
order 7
2 Bolt & nut b2
```

Because an element is an ordinary collection, `jbuild(x)` writes it as JSON and `jparse()` makes
one, and a collection built by hand with `name`, `attributes`, `text` and `children` is an element
`xbuild()` will write. **The attributes of an element come in order of name**, as every
collection's members do, not in the order of the document.

### What it refuses

A document that is not well formed gives a **null string**, `status()` is **1020** and `inmat()` is
the position where it gave up: a start tag that does not match its end tag, a repeated attribute, an
element or a CDATA section that is never closed, two root elements, text outside the root, an
attribute value with no quotes, an entity other than the five (`&lt;` `&gt;` `&amp;` `&quot;`
`&apos;`) and character references (`&#65;`, `&#x41;`). **No DTD is read**: an entity a DTD declares is
an error, so a document cannot make the parser read a file or grow without bound. Nesting is limited
to 500 levels.

### The modes of `xparse()`

| | |
|---|---|
| `xml$trim` (1) | white space is taken off both ends of the text of an element |

## `xbuild()`

`xbuild(element)` writes the text. The five characters XML reserves are escaped in text and in
attribute values, an element with nothing in it is `<b/>`, and the text is on **one line** unless
you ask otherwise. The modes are added together:

| | |
|---|---|
| `xml$decl` (1) | the declaration `<?xml version="1.0" encoding="UTF-8"?>` first |
| `xml$pretty` (2) | one element to a line, indented two spaces for each level |
| `xml$nocheck` (4) | a prefix need not have been declared by an `xmlns` attribute |

The third argument is the indent (up to 16 spaces and tabs) of `xml$pretty`:

```
x = xparse('<a><b><c>x</c></b><d/></a>')
crt xbuild(x, xml$pretty)
```

```
<a>
  <b>
    <c>x</c>
  </b>
  <d/>
</a>
```

`xbuild()` gives a null string and `status()` **1019** for something it cannot write as XML: a value
that is not an element (an array, a bare string), a name XML cannot have (a space in it), or a
prefix, on an element or an attribute, that no `xmlns` attribute on it or on an element above it
declares — unless `xml$nocheck`. A number or `true` in an attribute or in `text` is written as text.
The constants are in `keys.h`.

## `xpath()`

`xpath(element, query)` runs an **XPath 1.0** query. The context is the root element, and `/` is the
document. The answer is whatever the query is:

* a **node set** is an array of the nodes found, in document order: an element comes back as its
  collection, an attribute or a text as a string;
* a query that is a number, a string or a truth value gives that (`count(//book)` is `2`).

```
doc = '<catalog><book id="b1"><title>A</title><price>12.50</price></book>'
doc := '<book id="b2"><title>B</title><price>8</price></book></catalog>'
x = xparse(doc)
r = xpath(x, '//book[price>10]/@id')
crt jbuild(r)                           ;* ["b1"]
crt xpath(x, 'count(//book)')           ;* 2
crt xpath(x, 'sum(//price)')            ;* 20.5
```

What it takes:

| | |
|---|---|
| Paths | `/a/b`, `//b`, `.`, `..`, `*`, `@id`, `@*`, `text()`, `node()`, relative and absolute |
| Axes | `child`, `descendant`, `descendant-or-self`, `parent`, `ancestor`, `ancestor-or-self`, `following`, `following-sibling`, `preceding`, `preceding-sibling`, `self`, `attribute` |
| Predicates | `[2]`, `[last()]`, `[position()=2]`, `[@id="b1"]`, `[price>10]`, `[@lang]`, `[not(@lang)]`, with `and`, `or` |
| Operators | `=` `!=` `<` `<=` `>` `>=` `+` `-` `*` `div` `mod` and the union `\|` |
| Functions | `position()`, `last()`, `count()`, `sum()`, `true()`, `false()`, `not()`, `boolean()`, `string()`, `number()`, `string-length()`, `normalize-space()`, `contains()`, `starts-with()`, `substring-before()`, `substring-after()`, `concat()`, `name()`, `local-name()`, `floor()`, `ceiling()` and `round()` |

**Namespaces are names, not resolved addresses**: `//p:note` finds an element whose tag is written
`p:note`, and `local-name()` leaves the prefix off. A query that is not well formed gives a null
string, `status()` **1024** and `inmat()` the place; an argument that is not a collection (JSON text,
a string) gives a null string and `status()` 1020.

## What is not here

XSLT, XQuery and validation against an XML Schema or a DTD are not provided. No file or network
is ever read by these functions: they work on text you give them.

## See also

[SD Basic - Data Collections](05b-sd-basic-data-collections.html) ·
[SD Basic - JSON and Collection Files](05c-sd-basic-json-and-collection-files.html) ·
[SD Basic - CSV Files](11-sd-basic-csv-files.html) ·
[SD TCL - The Query Processor](21-sd-tcl-query-processor.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html).

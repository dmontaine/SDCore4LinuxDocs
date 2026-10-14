Title: SD Basic - Data Collections
Subtitle: Structured values with named elements and arrays, held in a variable, nested as deeply as you like, and written to a file as JSON.

A **data collection** is a set of named values — like a dynamic array whose
elements are found by **name** instead of by position. The value of an element
may be a number, a string, a true or false, a null, an **array**, or **another
collection**, so collections nest as deeply as memory allows. It is the same shape
as a JSON object, and it converts to and from JSON text (see
[SD Basic - JSON and Collection Files](05c-sd-basic-json-and-collection-files.html)).

Use one where a record has outgrown fields, values and subvalues: an order with
a customer, an address and a list of lines, each with its own parts. A dynamic
array is still the right thing for a flat record, and a collection can be read
from and written to a file as one record.

SD folds case, so a program may be written in either case. Keywords are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part. **The names of the
elements are not folded: `'Name'` and `'name'` are two elements.**

## Making one, and reading and writing it

| | |
|---|---|
| `c = collection()` | a new, empty collection |
| `d = collection(c)` | an **independent copy** of `c`, nested collections and all |
| `c{'name'} = value` | put an element in, or replace it |
| `value = c{'name'}` | read it back |
| `del c{'name'}` | take it out |
| `element.exists(c, 'name')` | 1 if it is there, else 0 |
| `enumerate(c)` | its names, as a dynamic array with a field for each, in simple left-to-right order — capitals before lower case |

```
c = collection()
c{'name'} = 'Acme'
c{'address/city'} = 'Boston'
c{'address', 'zip'} = '02110'
crt c{'name'}
crt c{'address'}{'city'}
crt c{'address/zip'}
crt element.exists(c, 'address/city') : ' ' : element.exists(c, 'nothing')
n = c{'nothing'}
crt '[' : n : '] status ' : status()
crt convert(@fm, ',', enumerate(c))
```

```
Acme
Boston
02110
1 0
[] status 1004
address,name
```

**Reading an element that is not there gives a null string and sets `status()` to
1004.** It is not an error that stops the program, so test `element.exists()`
when a null string would be a real value.

**Assigning a collection does not copy it.** `d = c` makes two names for the one
collection, as with a file variable; a change made through `d` is seen through `c`.
`collection(c)` is the copy:

```
d = c
d{'name'} = 'Other'
crt c{'name'}                     ;* Other: the same collection
e = collection(c)
e{'name'} = 'Copy'
crt c{'name'} : ' ' : e{'name'}   ;* Other Copy
```

## Paths

The braces take a name, several names, or a **path**. These are one element:

```
c{'address', 'city'}
c{'address'}{'city'}
c{'address/city'}
```

and they may be mixed. **Setting an element creates every level that is missing on
the way** — `c{'address/city'} = 'Boston'` makes `address` — and `del` of a level
removes everything below it.

**A name that holds a slash cannot be written in a path**, because the slash is
taken for a level. Write the name with `oconv(name, 'HU')`, which turns everything but
letters, digits and `- . _ ~` into `%xx` (lower case hex), so that a URL can be a
name; `iconv(name, 'HU')` undoes it, and leaves a `%` not followed by two hex
digits, and a `+`, as they are:

```
crt oconv('http://x/y z', 'HU') : ' ' : iconv('a%2fb', 'HU')
```

```
http%3a%2f%2fx%2fy%20z a/b
```

## Changing an element in place

`+=`, `-=`, `*=`, `/=` and `:=` work on an element: they read it, apply the operator and
store the result. An element that is not there is a null string to start from, so `+=`
starts at 0 and `:=` at nothing, and the levels of the path are made as for any assignment.

```
c{'count'} = 0
c{'count'} += 5
c{'count'} *= 3
c{'note'} := 'a'
c{'note'} := 'b'
crt c{'count'} : ' ' : c{'note'}
```

```
15 ab
```

## Arrays

An **array** inside a collection is numbered from 1 and has **no gaps**.

| | |
|---|---|
| `c{'list'} = mat()` | an empty array |
| `c{'list'} = mat(matrix)` | a copy of a dimensioned matrix (a two-dimensional one is copied row by row) |
| `c{'list'} = mat(matrix, 10)` | at most 10 elements of it |
| `c{'list', n} = value` | set element *n*, or **add** it when *n* is one past the end |
| `c{'list', -1} = value` | add on the end |
| `ins value as c{'list', n}` | open a gap at *n* and put the value in; the rest move up |
| `del c{'list', n}` | take element *n* out; the rest move down |
| `mat target = mat c{'list'}` | copy it into a dimensioned matrix |
| `inmat(c{'list'})` | how many elements it has |

```
c{'list'} = mat()
c{'list', 1} = 'red'
c{'list', 2} = 'green'
c{'list', -1} = 'blue'
crt inmat(c{'list'}) : ' ' : c{'list', 2} : ' ' : c{'list/3'}
ins 'amber' as c{'list', 2}
crt c{'list', 1} : ',' : c{'list', 2} : ',' : c{'list', 3} : ',' : c{'list', 4}
del c{'list', 1}
crt inmat(c{'list'}) : ' ' : c{'list', 1}
```

```
3 green blue
red,amber,green,blue
3 amber
```

**Element *n* can be set only when elements 1 to *n* - 1 exist.** Reading a position that is
not there gives a null string and 1004, as for a name. A position of 0, or a path that goes
through an element that is not there, **stops the program** with *Invalid data collection
element name or array position*. **An element of an
array that is itself to hold a collection must be made first**, with `collection()`:

```
c{'orders'} = mat()
c{'orders', 1} = collection()
c{'orders', 1, 'qty'} = 4
c{'orders', 2} = collection()
c{'orders', 2, 'qty'} = 6
```

A matrix element nobody assigned becomes a null string when the matrix is copied into an
array. `ins` on a collection that is not an array just puts the element in, and
`ins mat() as c{'list'}` puts in an empty array. **`as` is a reserved word in expressions**
(it ends the value in `ins value as ...`), so a variable called `as` can no longer follow a
value as a format.

**An asterisk in a path stands for every element of an array.** The answer is a
dynamic array with one **value** for each element; a second asterisk gives a **subvalue**
for each element of the array below. An element that does not have the item leaves
its place empty. At most two asterisks, and **only to read** — setting or deleting
through one is refused.

```
v = c{'orders/*/qty'}
```

`v` is `4|6|` — two values, and a third, empty, for the third order, which has an `item` and no `qty`.

## Booleans, nulls and the kind of a value

SD has no boolean or null **variable**; they are ordinary values that carry a mark.

| | |
|---|---|
| `jboolean(x)` | 1 or 0 and marked as a boolean: false for 0, for a null string and for the text `0` or `false` in any case; true for anything else |
| `jnull()` | a null string, marked as a JSON null |
| `jtype(value)` | `boolean`, `null`, `number`, `string`, `collection`, `array`, or `other` |

```
c{'on'} = jboolean(1)
c{'off'} = jboolean(0)
c{'none'} = jnull()
crt jtype(c{'on'}) : ' ' : jtype(c{'none'}) : ' ' : jtype(c{'name'}) : ' ' : jtype(c{'count'}) : ' ' : jtype(c{'address'}) : ' ' : jtype(c{'list'})
crt c{'on'} : ' ' : c{'off'} : ' [' : c{'none'} : ']'
x = jboolean(1) + 1
crt x : ' ' : jtype(x)
```

```
boolean null string number collection array
1 0 []
2 number
```

An element stored from one of them **keeps its kind**: `jbuild()` writes `true`, `false` or
`null` for it, and reading it back gives 1, 0 and a null string, with the mark, so that
`jtype()` can tell. **The mark is lost the moment you do anything to the value** —
`jboolean(1) + 1` is just 2.

## What a collection cannot hold, and what to know about memory

A collection can hold a **file variable** in a program, which a file has no way to
keep; written to a collection file it is stored as a null (see the next page). **A
collection that contains itself is never freed** — and cannot be written to a file or
turned into JSON text.

## See also

[SD Basic - JSON and Collection Files](05c-sd-basic-json-and-collection-files.html) ·
[SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html) ·
[SD TCL - Data Collection Files](20a-sd-tcl-collection-files.html) ·
[SD TCL - The CED Data Collection Editor](27b-sd-tcl-ced.html) ·
[SD Basic - Debugging](17-sd-basic-debugging.html), for looking at a collection
while a program runs.

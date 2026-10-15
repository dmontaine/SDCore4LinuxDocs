Title: SD Basic - Operating on Whole Arrays
Subtitle: Walking an array, changing the mark level, the s functions, sorting and mark mapping.

This page continues [SD Basic - Dynamic
Arrays](05-sd-basic-dynamic-arrays.html).

## Walking an array

```
remove variable from array setting delimiter
```

`remove` takes the next element off the front of *array* and reports which mark
followed it. It is much faster than repeated `extract()` on a long record,
because it does not rescan from the start each time.

**The delimiter code is the mark's level, and zero means the end.** For
`p^q|r\s`:

| Code | Meaning |
|---|---|
| `0` | end of the string — this was the last element |
| `2` | a field mark followed |
| `3` | a value mark followed |
| `4` | a subvalue mark followed |

```
s = record
loop
   remove element from s setting mark
   ...
while mark
repeat
```

**`remove` consumes the variable it reads.** Work on a copy — `s = record` —
or the record is gone by the end of the loop. The functions that follow depend
on an internal pointer into that variable:

| | |
|---|---|
| `getrem(string)` | how far through the string the pointer has reached |
| `setrem offset on string` | move the pointer |

After one `remove` from `aaa^bbb`, `getrem()` is `4`.

**Changing the string resets the pointer.** A loop that both `remove`s from a
string and assigns to it will restart from the beginning, silently.

### `rmvd()`: only three marks end an element

```
element = rmvd(array, delimiter)
```

The same as `remove()` as a function, and sharing its pointer, but **only a
field, value or subvalue mark ends an element** (codes 2, 3 and 4). A text mark
or an item mark is part of the data. `remove()` ends an element at those too,
with the codes 5 and 1. Once the end is reached `rmvd()` gives a null string
and 0 until the string is assigned again.

### `revremove`: the same, going backwards

```
revremove variable from array setting delimiter
```

Takes the element that **ends at the remove pointer** and moves the pointer
back past the mark in front of it. The delimiter is that mark's code (2, 3, 4,
and also 1 and 5), and **0 for the first element of the string**. The pointer
has to be put in place first: `setrem len(s) on s` before the first
`revremove` walks the whole string from the end, and `setrem 5 on s` starts
with the elements that lie in the first five characters. Without a `setrem` the
pointer is at the start and there is nothing before it: a null string and 0.

```
s = 'a' : @fm : 'b' : @vm : 'c'
setrem len(s) on s
loop
   revremove element from s setting mark
   crt element : ' ' : mark          ;* c 3, then b 2, then a 0
while mark
repeat
```

A null element is given as a null string with its mark, and a string that
begins with a mark ends on a null first element, as a forward `remove` would
begin on one.

## Changing the mark level

```
raise(string)
lower(string)
```

`raise` promotes every mark one level — subvalues become values, values become
fields. `lower` demotes them. `lower('x' : @fm : 'y')` has one field
and two values; `raise('x' : @vm : 'y')` has two fields.

These are how you move a nested structure between levels without walking it —
for example turning a multivalued field into a record.

## Working across an array

### `vslice`

```
vslice(array, value.number)
```

Takes the *n*-th value of **every** field and returns them as fields. On
`a1|a2^b1|b2`, `vslice(h, 2)` gives `a2^b2`.

That is the idiom for pulling one column out of a set of associated multivalued
fields.

### `substrings`, `fieldstore` and `splice`

| | |
|---|---|
| `substrings(array, start, length)` | the substring operator applied to every element |
| `fieldstore(string, delimiter, start, count, replacement)` | replace or insert delimited fields — a *count* of zero inserts |
| `splice(array1, string, array2)` | joins the arrays element by element with *string* between |

`splice('a' : @vm : 'b', '-', '1' : @vm : '2')` gives `a-1|b-2`.

### `substitute`

```
substitute(array, old.list, new.list {, delimiter})
```

Replaces whole **elements** that match. Substituting `b` with `Z` in
the values `a`, `b`, `c` gives `a|Z|c`.

### `reuse`

```
reuse(expression)
```

Makes a single value behave as though it repeated for every element of the
other operand. **Without it, arithmetic only reaches the first element.**

| Expression | Result |
|---|---|
| `(1\|2\|3) + 10` | `11\|2\|3` |
| `(1\|2\|3) + reuse(10)` | `11\|12\|13` |

The first line is almost never what was intended, and it produces a plausible
number rather than an error.

## The `s` functions

Most string and arithmetic functions have a partner ending in `s` that applies
the operation to every element instead of to the whole string:
`abss()`, `negs()`, `mods()`, `nums()`, `lens()`, `counts()`, `fields()`,
`trims()`, `trimbs()`, `trimfs()`, `indexs()`, `soundexs()`, `spaces()`,
`strs()`, `fmts()`, `iconvs()`, `oconvs()`, `folds()`, `cats()`.

**When two Arrays are different lengths, the shorter is treated as empty, not
truncated.** With `1|2|3` and `10|20`:

| Call | Result | |
|---|---|---|
| `cats(p, q)` | `110\|220\|3` | the third pairs with nothing |
| `mods(p, q)` | `1\|2\|3` | `mod(3, 0)` is `3` — no error |

So a mismatch produces a full-length answer with quietly wrong elements in the
tail. **Compare `dcount()` on both operands before relying on the result.**

## Logical functions

These take true/false values element by element. In SD, zero and the null
string are false and anything else is true.

| | |
|---|---|
| `not(expression)` | logical negation of a single value |
| `nots(array)` | of every element |
| `ands(a, b)` · `ors(a, b)` | element-by-element AND and OR |
| `eqs` · `nes` · `gts` · `ges` · `lts` · `les` | element-by-element comparison, giving 1 or 0 |
| `ifs(control, true.values, false.values)` | picks from one array or the other per element |

| Call | Result |
|---|---|
| `not(0)`, `not(1)`, `not('')` | `1`, `0`, `1` |
| `nots(1\|0\|'')` | `0\|1\|1` |
| `ands(1\|0\|1, 1\|1\|0)` | `1\|0\|0` |
| `ors(1\|0\|0, 0\|1\|0)` | `1\|1\|0` |
| `eqs(1\|2\|3, 1\|20\|3)` | `1\|0\|1` |
| `ifs(1\|0, 'yes'\|'yes', 'no'\|'no')` | `yes\|no` |

## Sorting

```
sortinit {order}
sortadd key, data
sortclear
```

`sortinit` starts a sort, `sortadd` feeds it a key and a record, and reading it
back drains it. The order codes are the same `al` / `ar` / `dl` / `dr` as
`locate`. For sorting a whole file, `sselect` is faster — see
[SD Basic - Select Lists](08-sd-basic-select-lists.html).

### `sort.compare()` and `compares()`

```
sort.compare(a, b, mode {, no.case})
compares(a, b {, justification})
```

`sort.compare()` answers -1, 0 or 1 as *a* comes before, equal to or after *b*
under the rule in *mode*. The names are in `syscom keys.h`.

| Mode | Name | Rule |
|---|---|---|
| 0 | `srt$left` | character by character from the start (so `10` is before `9`) |
| 1 | `srt$right` | right justified: two whole numbers, with an optional sign, compare as numbers |
| 2 | `srt$compound` | alternating number and text parts: `GC5` is before `GC41`; a leading number comes before text |
| 3 | `srt$right.float` | as 1, but any number, not only a whole one, compares as a number |
| 4 | `srt$strict` | as 2, but `28` and `028` differ, the one with fewer characters first |
| + 16 | `srt$descending` | the answer is reversed |
| + 64 | `srt$nocase` | case is ignored; a true fourth argument does the same |

`compares()` is `compare()` over two arrays, with an answer of the same shape;
the justification is that of `compare()` (`'R'`, `'LI'` and so on).

`mergelist(list1, list2, modes)` merges two lists that are in order by the
same rules: *modes* is `ml$inter` (8), `ml$union` (16) or `ml$diff` (24) added
to a sort rule and, if the lists are not in order, `ml$unsorted` (32). Either
list may be a select list variable. **The values 8, 16, 24 and 32 are SD's
own**: the openQM manual names the four but does not number them. `call
!mergelist` is the older subroutine with its own mode words, and is unchanged.

### `nv()` and `ns()`

`nv(array {, repeat})` puts each value's position number in its field in place
of the value, and `ns(array)` each subvalue's position number in its value in
place of the subvalue. The marks stay where they were, so the answer has the
shape of the argument. With *repeat* true `nv()` numbers the subvalues of a
value with the number of the value, and without it a value's subvalues are
dropped. For `111 vm 121 sm 122 sm 123 vm 131 sm 132 fm 211 sm 212 vm 221`:

| Expression | Result |
|---|---|
| `nv(s, 0)` and `nv(s)` | `1 vm 2 vm 3 fm 1 vm 2` |
| `nv(s, 1)` | `1 vm 2 sm 2 sm 2 vm 3 sm 3 fm 1 sm 1 vm 2` |
| `ns(s)` | `1 vm 1 sm 2 sm 3 vm 1 sm 2 fm 1 sm 2 vm 1` |

## Mark mapping

```
mark.mapping file.variable, on | off | expression
```

Controls whether SD translates mark characters when reading and writing a
**directory** file, whose records are ordinary operating-system files. With
mapping on, field marks become newlines on the way out and back again on the
way in; with it off, the bytes pass through unchanged.

**It has no effect on a dynamic file**, where records are stored in SD's own
format.

## What is not here

Nothing in the dynamic-array group has been removed from this port.

`dcount()`, `fieldstore()`, `substrings()`, `splice()`, `substitute()` and the
whole `s` family are also described in [SD Basic - String Functions](04-sd-basic-string-functions.html), where they
are used on text rather than on structure.

## See also

[SD Basic - String Functions](04-sd-basic-string-functions.html) · [SD Basic - File Handling](07-sd-basic-file-handling.html) ·
[SD Basic - Select Lists](08-sd-basic-select-lists.html) · [SD Basic - Math Functions](03-sd-basic-math-functions.html).

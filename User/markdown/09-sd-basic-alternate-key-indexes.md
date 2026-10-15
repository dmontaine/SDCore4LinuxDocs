Title: SD Basic - Alternate Key Indexes
Subtitle: Building an index on a field, selecting through it, and the three steps that report success while doing nothing useful.

An alternate key index lets you find records by the contents of a field instead
of by record id. This page covers creating one, keeping it, and reading it from
BASIC.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## Creating an index takes three steps, and skipping any of them is silent

**This is the whole of this page's warning, so it is first.** Each step
reports success on its own, and a program that stops after the first or second
gets an index that exists and finds nothing.

```
create.index file.name field.name        ;* at the command line
```

then **close the file in every session that has it open**, then

```
build.index file.name field.name
```

then reopen the file.

### What each step actually does

A dynamic file with three records, `TOWN` being field 2, holding `LONDON`,
`LEEDS` and `LONDON`:

| | |
|---|---|
| `create.index ZZAK TOWN` | *"Added index for TOWN"*, `@system.return.code` **0** |
| `indices(f)` on the **already-open** file variable | **empty** |
| `fileinfo(f, 13)` on it | **0 — no indexes** |
| after `close f` and reopening | `indices(f2)` is `TOWN`, `fileinfo(f2, 13)` is `1` |
| `selectindex 'TOWN', 'LONDON'` at that point | **0 ids** |
| `build.index` **with the file still open** | *"Cannot gain exclusive access to file"*, `@system.return.code` **3021** |
| `build.index` after `close` | *"Building index 'TOWN'... 3 records processed / Populating index..."*, `@system.return.code` **0** |
| `selectindex 'TOWN', 'LONDON'` after reopening | **`C1` and `C3`** |

> **An open file variable never learns about a new index.** The handle
> carries the index list it had when it was opened. So a program that creates
> an index and then uses it in the same run finds nothing, and neither
> `indices()` nor `fileinfo()` gives it a hint — both report the state of the
> handle, not of the file. **Close and reopen.**

> **And `create.index` makes an empty index.** It records the definition; it
> does not walk the existing records. Until `build.index` runs, the index is
> there, is reported by `indices()`, and matches nothing. A file that was
> indexed before it had data does not need building; one indexed afterwards
> always does.

> **`build.index` needs exclusive access and your own session counts.**
> With the file open in the same program, it refuses with
> *"Cannot gain exclusive access to file"* and `@system.return.code` **3021**.
> **Test that return code** — the message goes to the capture variable, not to
> the screen, so a program that does not look at it carries on with an unbuilt
> index.

## Once it is built, it maintains itself

After `build.index`, writing a fourth record with `TOWN` of `LONDON`
made `selectindex 'TOWN', 'LONDON'` return **3** ids without any further
action. Ordinary `write` and `delete` keep every index on the file up to date.

That is also the cost: each index makes every write a little more expensive.
Index the fields you select on, not every field.

## Selecting through an index

```
selectindex index.name {, value} from file.variable {to list}
```

**With and without a value it returns completely different things, and
neither form says so.** On the file above:

| Call | What comes back |
|---|---|
| `selectindex 'TOWN', 'LONDON' from f to 4` | **the record ids** — `C1`, `C3` |
| `selectindex 'TOWN' from f to 4` | **the distinct index values** — `LEEDS`, `LONDON` |

So the no-value form is how you ask *"what towns are there?"* and the
with-value form is how you ask *"who is in London?"*. A program that drops the
value argument by accident gets a list of values where it expected ids, reads
them as record ids, and finds nothing — with no error at any point.

```
selectindexv index.name {, value} from file.variable to list.variable
```

The same, into a **select list variable** instead of a numbered list: read it
with `readnext id from list.variable`. **Numbered list 10 is the statement's
scratch list**: the selection goes through it and it is empty afterwards, so a
program that keeps something in list 10 must keep it elsewhere. An index the file
does not have leaves `status()` at 1, as `selectindex` does, and the variable
holds an empty list.

## Walking an index in order

```
setleft index.name from file.variable
setright index.name from file.variable
selectleft index.name from file.variable {setting variable} {to list}
selectright index.name from file.variable {setting variable} {to list}
```

`setleft` positions before the first index value, `setright` after the last.
`selectright` then moves to the next value and selects its ids; `selectleft`
moves back.

**`setting` receives the index value the scan landed on.** After
`setleft 'TOWN' from f`, a `selectright` returns **1 id** with `setting`
holding **`LEEDS`** — the first value in order.

> **These four take no `then` or `else` clause.** Writing one is a compile
> error — *"Unrecognised statement"* — because the parser expects `setting` or
> `to` and finds a keyword it has no use for. To detect the end of the index,
> read the select list they build: an empty one means there was nothing
> further.

Walking with `selectright` is how you produce a report in index order without
sorting, and how you page through a large file a value at a time rather than
selecting all of it.

### Into a select list variable: `selectleftv` and `selectrightv`

```
selectleftv index.name from file.variable {setting variable} to list.variable
selectrightv index.name from file.variable {setting variable} to list.variable
```

The same step, but the ids come back in a **select list variable** — read it with
`readnext id from list.variable` — instead of a numbered list. **Numbered list 10
is the statement's scratch list**: the step goes through it, and anything a
program kept in list 10 is lost. `status()` is the step's: **3030** past the end
of the index and **3019** for an index the file does not have. With `selectindexv`
(above), every statement that fills a numbered list now has a form that fills a
variable.

## Scanning an index the Pick way: `root`, `key` and `bscan`

Three statements for programs written for other multivalue systems. They are made of
`setleft`, `setright`, `selectindex`, `selectleft` and `selectright`, and
they work on **dynamic hashed files only** (a directory file gives `status()` 3).
**Numbered list 10 is their scratch list** here too.

```
root file.name, index.name to scan.variable then ... else ...
key(operator, scan.variable, index.key, item.id) then ... else ...
bscan indexed.value {, ids} from file.variable {, value} using index.name {reset} {by a | d} then ... else ...
```

**`root`** checks that the file opens and has the index (it looks for the name as
typed, then in lower and in upper case) and makes the **scan variable**, an ordinary
string holding the file name and the index name. Where openQM also takes an
A-correlative expression in place of an index name and looks for an index built from
it, SD takes the **name of an index only**. The `else` branch has `status()` the error of
the open, or 3019.

**`key`** takes one step of a scan. An entry is an indexed value and **one** record id;
the ids of one value come in the order `selectindex` gives them. Nothing is kept
between calls except `index.key` and `item.id`, the entry last returned: each call
opens the file and finds its place again. The brackets are optional. `key` is a
statement unless the program has a matrix called `key`, in which case `key(1) = x` is
still the assignment it looks like.

| operator | the step |
|---|---|
| `c` | the first entry at or beyond `index.key`, left to right |
| `n` | the entry after (`index.key`, `item.id`): the next id of the same value, else the first id of the next value; with both null, the first entry of the index |
| `p` | the entry before; with both null, the last entry |
| `l` | with a null `index.key` the rightmost entry, otherwise as `p` |
| `r` | the first id of the value `index.key` |
| `x` | `item.id` becomes the field-mark list of **all** the ids of the value `index.key` |
| `v` | does the entry (`index.key`, `item.id`) exist |

The `then` branch means the step found something. In the `else` branch `status()` is
**3030** for no entry beyond or before, **1** for no entry for that value or pair,
**3019** for an index that is not there and **2** for an operator that is not one of these.

**`bscan`** scans with its position kept for you, per file variable and index: a scan
goes on from the entry the last `bscan`, `selectindex`, `selectleft` or `selectright` on
that file variable returned. `reset` goes to the extreme left (the extreme right with
`by d`) and returns the entry there; `value` positions at that value, or at the
nearest entry in the direction of the scan when the index has none, with `status()` 2;
with neither it moves one entry in the direction of the scan. `indexed.value` and the
`ids` (field-mark delimited, all the ids of the value) are returned. In the `else`
branch `status()` is **0** when the scan has run off the end of the index (both
variables null), **3** for a file that is not a dynamic hashed file, **4** for an index that
is not there, **5** for a `by` that is not `a` or `d`, and **10** for anything else.

## Asking what indexes a file has

```
indices(file.variable)
indices(file.variable, index.name)
```

| | |
|---|---|
| one argument | the index names, as a dynamic array |
| two arguments | the definition of one index |

`indices(f2, 'TOWN')` returns a **nine-field** definition whose
field 2 is the **field number** the index is built on — `2` for a `TOWN` in
field 2. Field 1 holds the dictionary-style definition the index was made from.

`fileinfo(file.variable, 13)` is the quick yes/no: `1` if the file has any
index, `0` if not — subject to the open-handle caveat above.

## Maintaining an index from BASIC

```
akread variable from file.variable, index.name, key then ... else ...
akwrite variable to file.variable, index.name, key
akdelete file.variable, index.name, key
akclear file.variable, index.name
akenable file.variable, index.name
akrelease file.variable, index.name
create.ak file.variable, index.name, ...
delete.ak file.variable, index.name
```

These reach into the index directly rather than letting SD maintain it. They
exist for the case an ordinary index cannot express — an index whose key is
computed by a program rather than taken from a field.

**They are not the normal route and they will let you corrupt an index.**
Writing an index entry that does not match the record it points at produces a
`selectindex` that returns ids whose records do not have the value you asked
for. Nothing detects that except `build.index`, which rebuilds from the data
and throws away whatever you put there. **Use the ordinary statements and let
SD maintain the index unless you have a reason you can write down.**

`akenable` and `akrelease` turn maintenance off and on around a bulk load,
which is the one common reason to touch these at all: loading a million
records with three indexes live is far slower than loading them and building
the indexes afterwards.

## `listindex()`

```
listindex(list, delimiter, item)
```

Picks one entry out of a delimited list — it has nothing to do with alternate
key indexes despite the name, and belongs with the list functions in
[SD Basic - Select Lists](08-sd-basic-select-lists.html).

## What is not here

Nothing in the index group has been removed from this port.

## See also

[SD Basic - Select Lists](08-sd-basic-select-lists.html) · [SD Basic - File Handling](07-sd-basic-file-handling.html) ·
[SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html).

Title: SD TCL - The Development Tools
Subtitle: Full-screen pages for the work in your own account: its files, and the verbs that make and change them.

```
tool.files
tool.voc
```

These pages are for **the account you are signed in to**. They work in every account (they are in
everybody's vocabulary), they need a real terminal of at least **140 columns by 43 lines** (and no bigger than **500 by 300**:
a larger window is refused at once, in a line that gives the size it found, because taking such a screen
costs time that grows with the square of its height), and they add no
access: every change they make is a command you could have typed, run for you after a box that shows the
exact command. A gate that is off for your account is met as the command's own refusal; the page shows
the gates you hold, and never tries an operation to find out.

The box that asks before a command is titled *Run this command?*. The few changes that are not commands -
a record the page writes or deletes itself - say what they are about to do instead: *Write this record?*
(an item of a dictionary in `tool.dict`, a saved query in `tool.query`), *Delete this record?* (a saved
query), *Update these records?* and *Put these records back?* (`tool.bulk`). The default button is still
Cancel. When a page hands the terminal to a command and asks *Press Enter to return*, Enter brings back
the page.

The home screen has a tile for each of them, in the group *Develop*.

## tool.files - the files of the account

```
tool.files
```

**`tool.files`** lists every file the account's VOC points at, one row each, in name order:

| column | what it says |
|---|---|
| Name | the file's name in the VOC |
| Kind | `dynamic` (records in groups, the usual data file), `directory` (each record is a file in a directory of the operating system), `sequential`, `server` (a file on another SD server) |
| Records | the file's own approximate count of records |
| Modulus | how many groups a dynamic file has now |
| Bytes | the size on disk of a dynamic file without its indices |
| Idx | how many alternate-key indices it has |
| Trigger | the name of its trigger, if it has one |
| Case | `any` when record ids ignore case (**as delivered**: jack and JACK are one record), `exact` when they do not |
| Dict | whether it has a dictionary |
| Open | `yes` when another session has the file open |

The box under the list describes **the file under the cursor**: where it is on disk, how many records it
holds, its modulus and group size and how full the groups are, the size of the primary and overflow parts,
whether ids ignore case, whether it can be written, its indices and its trigger, and who else has it
open. The line between the boxes shows the **gates your session holds** (`voc-edit`, `dict-edit`,
`bp-edit`), asked of the system.

### What the keys do

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **N** | make a file: asks for a name, then *dynamic* or *directory*, then shows `create.file name` in a box |
| **C** | clear the file under the cursor (`clear.file name`) |
| **D** | delete it (`delete.file name no.query`) |
| **A** | run `analyse.file` on it: the terminal is handed to the verb, which prints its report; Enter brings the page back |
| **I** | run `list.index` on it (its indices, in full), the same way |
| **T** | run `list.triggers` on it, the same way |
| **/** or F11 | show only the names that hold some text (empty shows them all) |
| Esc | clear the filter |
| F5 | read the files again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**Every change goes through a box.** The box shows the exact command, says what it does, and has two
buttons, *Run* and *Cancel*; **Cancel is the one Enter chooses**, so a stray Enter runs nothing. *Clear* and
*Delete* then ask for **the file's name, typed**; a wrong name does nothing. The command is the ordinary
verb, so its own checks are the checks: a file open in another session cannot be cleared or deleted, and
what the verb says is what the status line shows.

**A name the page does not give to a command.** The page hands a command only names of letters a-z,
digits, dot, dash and underscore. A file whose name has anything else (a capital, an `&`, a `$`) is listed and
described, and the page says which verb to type at the prompt for it instead.

**Gates.** Making a new file, and clearing or deleting an ordinary data file, are not held back by the
edit gates: the new VOC pointer is a side effect of an ordinary command. The gates matter for the
protected kinds: clearing or deleting a **program file** (such as `bp`) needs `bp-edit`, and a
**dictionary** on its own needs `dict-edit`. The page shows which of the three gates your session holds
(`voc-edit`, `dict-edit`, `bp-edit`); if one is off, the verb's own refusal is what you get, shown on the
status line, and the file is left as it was. The administrator turns a gate on for an account with
`modify.account` (see *Accounts and Security*). Files of the **shared account** are not in your VOC as
files and are never changed from here.

## tool.voc - the vocabulary of the account

```
tool.voc
```

**`tool.voc`** lists every entry of the account's VOC, the file that tells SD what each word on a command line
means, one row each, in name order:

| column | what it says |
|---|---|
| Name | the entry's id |
| Type | `V` verb, `K` keyword, `F` file, `Q` pointer to a file in another account, `R` pointer to a record, `PA` paragraph, `S` stored sentence, `X` text |
| Points at | what it leads to, in a few words: the program a verb runs, the path of a file, the account and file of a Q-pointer |
| Works | for a file or a Q-pointer, whether the file it names can be opened (`yes`, `NO`); the page opens it to see |
| Against the shipped VOC | `same` as NEWVOC, the vocabulary every account was copied from; `changed` from it; or `added` in this account |

The box under the list shows **the entry under the cursor**, field by field. The line between the boxes shows
the **gates your session holds**, as `tool.files` does.

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **E** | edit the entry in SED (`sed voc name`): the terminal is handed to SED, and Enter brings the page back at the same entry |
| **D** | delete the entry (`delete voc name`) after a box that shows the command, with the id typed |
| **T** | choose the type shown: all, verbs, files, pointers, paragraphs and sentences, other |
| **S** | choose the state shown: all, only the entries that differ from the shipped VOC, only broken pointers |
| **/** or F11 | show only the ids that hold some text |
| Esc | clear the filter |
| F5 | read the VOC again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**The page writes nothing itself.** A record is changed by SED, which the page starts, or by `delete`, which
it runs; both are ordinary commands with their ordinary checks. Writing the VOC by hand needs the
**`voc-edit`** gate: without it SED's save and the delete are refused by the kernel and the entry is left as
it was. A VOC pointer made by an ordinary command such as `create.file` is not held back by the gate.

**An id the page does not give to a command.** As in `tool.files`, only ids of letters a-z, digits, dot,
dash and underscore are put into a command. A VOC id may have much else (a capital, `$`, `%`, `&`); such an
entry is listed and shown, and the page says which command to type for it instead.

## tool.dict - the dictionary of a file

```
tool.dict
tool.dict customers
```

**`tool.dict`** shows the dictionary of one data file of the account: the items a query can name, what each
one is and how it prints, and the file's indices. With a file named after the verb it opens that file's
dictionary at once (the name is put in lower case). With none it first lists the files the account's VOC points
at, with the kind of each, whether it has a dictionary, how many items it holds and how many indices it has;
Enter opens the dictionary of the file under the cursor. A name that is not one of the account's files, a name
with a character other than a-z, 0-9, dot, dash and underscore, and a file with no dictionary are each said
politely, and the list of files is shown.

### The items pane

One row for each item of the dictionary, in id order:

| column | what it says |
|---|---|
| Id | the item's id |
| Type | `D` data, `A` and `S` the Pick layout, `I` computed, `C` calculated, `E` an element of a data collection, `L` a link, `PH` a phrase, `X` text; any other type is shown as its first character |
| Field | the number of the field a `D`, `A` or `S` item shows (0 is the record id), or `computed` |
| Heading | the column heading |
| Format | width and justification, such as `10R` |
| Conversion | the conversion code for display |
| S/M | `S` single valued, `M` multivalued |
| Association | the name that makes multivalued items line up |
| Expression, correlative or text | an I item's expression, an A item's correlative, the text of an X item |

The box under the list says **in words** what the item under the cursor shows (which field, what heading,
how wide and how justified, what its conversion is, single or multivalued), the expression of a computed item
and whether it has been compiled, and the record as it is stored.

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **N** | make an item: asks the id, then the type (data, A-type or indirect) and the fields that type needs, one at a time, checking each answer |
| **E** | edit the item in SED (`sed dict file item`): the terminal is handed to SED, and Enter brings the page back at the same item |
| **D** | delete the item (`delete dict file item`) after a box, with the item's id typed |
| **C** | compile an A, S, I or C item (`compile.dict file item`) after a box |
| **T** | try the item on a record of the file: asks the record's id and shows the value the query processor would compute for it, and the same value as a query prints it |
| **I** or Tab | the indices pane |
| **F** | back to the list of files |
| **/** or F11 | show only the ids that hold some text |
| Esc | clear the filter |
| F5 | read the dictionary again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**Making an item.** N asks for the id (letters a-z, digits, dot, dash and underscore, starting with a letter or a
digit; capitals are put in lower case; an id that already exists in any case is refused), then the kind of item. For a data item it asks the
number of the field (0 to 9999), the heading, the justification (L, R or T), the width (1 to 200), the
conversion (checked against the conversions SD knows), single or multivalued and, for multivalued, the
association. An A-type item is asked in the Pick layout (field, heading, association, conversion, correlative,
justification, width) and an indirect item starts with its expression. A wrong answer is refused with the
reason and the question is asked again; Esc leaves the question and nothing is written. Then **one box shows
the whole record, field by field**, with *Run* and *Cancel* (Cancel is what Enter chooses). After Run **the page
writes the record itself**, as an ordinary record write to the dictionary - it is the only thing the page
writes. Before it writes, the page asks the system whether this session may change that dictionary, as SED and
the IDE do, and when it may not it shows the system's own words and writes nothing.

**Trying an item.** T asks the id of a record of the data file. A D item gives its field; an I or C item, and an
A or S item that has a correlative, must have been compiled first (C does it), and T says so, before it asks for
a record, if it has not. The page shows the value (several values are shown between bars) and, for a D, I or C
item with a conversion or a format, the value as a query prints it: the conversion first, then the format. An
item that holds no value (text, a link, a phrase) is refused with its type. The page writes nothing and runs no
command of its own, but an item that calls a subroutine of the account runs that subroutine, as a query would.

### The indices pane

One row for each alternate key index of the file: its name, whether it is **built**, the type of item it is on,
whether records with an empty value are indexed, single or multivalued, how its keys are justified (`R` orders
numbers by value), whether case matters, and the field or expression. An index that is defined but not built
finds nothing, and the box under the list says so.

| key | does |
|---|---|
| **N** | make an index: pick an item of the dictionary from a list; `create.index file item` defines the index and then `build.index file item` builds it |
| **B** | build the index under the cursor again from the records (`build.index file index`) |
| **D** | delete it (`delete.index file index`) after a box, with its name typed |
| **L** | list it in full (`list.index file index detail`): the terminal is handed to the verb, which prints its report; Enter brings the page back |
| **I**, Tab or Esc | back to the items pane |

N runs both verbs after one box, because an index that is defined and not built is a trap;
B builds one that is left over. Building and deleting need the file to themselves: if another session has the
file open the verb says so and nothing changes. The page itself keeps no file open while it waits.

**Every change goes through a box.** The box shows the exact command and says what it does, with *Run* and
*Cancel*; **Cancel is the one Enter chooses**, so a stray Enter runs nothing. Deleting an item and deleting an
index then ask for the id or name, **typed**; a wrong one does nothing. The commands are the ordinary verbs, so
their checks are the checks, and what the verb says is what the status line shows.

**Gates.** Writing a dictionary needs the **`dict-edit`** gate: without it the page's own write (N), SED's save
(E) and the `delete` verb (D) are refused, and the record is left as it was. Compiling an item (C) and making,
building and deleting indices are not held back by it. The page shows whether you hold `dict-edit`, asked of the
system, and the box for N and D says when the change is expected to be refused. The administrator turns the gate
on for an account with `modify.account` (see *Accounts and Security*). The dictionaries of the **shared account**
follow the shared account's own rules and are not changed from here.

**Limits.** The page makes data, A-type and indirect items; other kinds (links, phrases, text, collection
elements, S and C types) are listed, described, tried where they hold a value, and edited in SED. It does not copy
items between files, and it does not edit the master dictionary (that is the administrator's). Indices are made
with the verb's defaults (`no.nulls`, `no.case` and `pathname` are typed at the prompt), and the list of files
counts indices only for dynamic files. A dictionary of more than 3,000 items shows the first 3,000 and says so.

**An id the page does not give to a command.** Only ids and names of letters a-z, digits, dot, dash and
underscore are put into a command. An item whose id has anything else (a capital, `@`, `$`, `%`) is listed and
described, and the page says which verb to type for it at the prompt; a file whose name has such a character
can be opened and read but not changed from the page. An index made in capitals is given to the verbs in lower
case, which they accept.

**An id or an index name that SD reads as a keyword.** A word the VOC holds as a keyword (`all`, `no.query`,
`detail`, `lptr`, `data`, `dict`, `local` and the like) is read by a verb as that keyword, whoever's item it is:
`delete dict customers all` asks to delete every item, and `delete.index customers all` removes every index. An
item or index with such a name is listed, but the page does not give it to a verb: it says which command to type,
and typing it at the prompt is then your own act. Making an item (N) with such an id is refused, and the question says why.

**Which lines are boxes.** Deleting, compiling, and making, building and deleting an index show the exact command
in a box. Making an item (N) shows the record the page writes, which no verb takes. Editing in SED (E) and listing
an index (L) hand the terminal over with no box.

## tool.query - the query and report builder

```
tool.query
tool.query zq
```

**`tool.query`** builds a `list`, `sort`, `count` or `sum` sentence on one of your files in five boxes. It shows the sentence all the time, runs it and shows what it printed in a box of its own, and saves the query in your file `&queries&` so it can be loaded again. `tool.query zq` opens the file `zq` directly. The page needs no gate: it runs a query as you could and writes only its own file `&queries&`. It offers the files of your VOC that open, are dynamic or directory files and have a dictionary. A sequential file, a file on another server and the shared account's files are not offered.

| box | what it holds |
|---|---|
| 1 File | the files; Enter chooses one (choosing starts a new query); **/** shows only the names that hold some text |
| 2 Columns | the items of the file's dictionary, `@id` first; **Space** marks a column (the order marked is the order printed); **B** breaks on it (`break.on`), **T** totals it (`total`); **X** takes every mark off |
| 3 Conditions | up to six rows of item, operator and value; **Enter** edits the row, **J** switches `and` / `or`, **D** clears it. The sentence in the box at the foot shows how the rows are joined |
| 4 Sort | up to four levels; **Enter** picks the item, **Space** turns the level to `by.dsnd`, **D** clears it |
| 5 Options | list, count or sum; a heading and a footing; leave out the record id (`id.sup`) or the detail lines (`det.sup`); `no.page`; only the first *n* records (`sample`, taken before any sort) |

The operators are `=` `#` `<` `>` `<=` `>=` `like` and `unlike`. A value is plain text, typed as the query processor reads it for the item (see the query documentation). `like` takes a pattern (`0X` any text, `1A` a letter, `3N` three digits); put `0X` on both sides to find text inside a value. A value, a heading and a footing hold no quote, backslash, backquote or semicolon, and no character that is not plain ASCII; a heading that needs a quote (the page-number codes) is typed at the prompt.

| key | does |
|---|---|
| Tab, Shift-Tab | next and previous box |
| **R** | run the sentence; the output is shown in the Results box and nowhere else |
| **E** | edit the sentence as text; a change in any box writes it again from the boxes |
| **S** | save the query; asks a name (a-z, 0-9, dot, dash, underscore; at most 40) |
| **L** | the saved queries (up to 100): Enter loads one, **X** deletes one |
| F5 | read the files and the dictionary again; what no longer fits is dropped |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

In the Results box Up, Down, PgUp, PgDn, Home and End scroll, Left and Right move 20 columns sideways, and Esc goes back to the boxes. The box keeps 2000 lines and says how many there were. A query on a big file is run in full and cannot be stopped from here: use the first-*n* option for a trial. A select list that is waiting narrows the query, and the box says so.

**Everything that is run is checked first.** A sentence the page runs starts with `list`, `sort`, `count` or `sum`, names the chosen file, and then holds only words from a fixed list, numbers, the items of that file's dictionary and values in double quotes. A word that sends the output somewhere else or writes (`to`, `saving`, `lptr`, `csv`, `as`, `file` and others) is refused, even when it is the name of a dictionary item. So is a semicolon, a single quote and a word the page does not know. The sentence the boxes make, a sentence you edit and a sentence a saved query holds are checked again by the same routine just before they run. An item whose name has a character the page does not use, or is also a word of the query language or a VOC keyword, is listed but cannot be marked. A phrase (`PH`) is not listed.

**Saved queries** are records of the file `&queries&` in your account. The page makes the file when you save the first query, after a box that shows `create.file &queries& dynamic`. Every save is a box too, and replacing a saved query asks its name typed. A saved query is data: when it is loaded every part is checked against the file's dictionary, the operator table and the quoting rule, and what does not pass is dropped and counted in the status line. Deleting one with X also asks its name typed.

**Limits.** One file at a time. No run-time prompts, no VOC paragraph, no printing (`lptr`) and no output to a file or a list. The phrases and the `$query.defaults` record of a dictionary belong to the account and are expanded by the query processor; the page does not list a phrase and cannot see the defaults.

## tool.bulk - a bulk update of one data file

```
tool.bulk
```

**`tool.bulk`** changes many records of one data file of your account in one go, and shows you what it will do
before it does it. You choose the file, say which records, say what is to be done to them, look at a **dry run**,
and only then apply it; if it was wrong, **U** puts the records back. It is a front end: it adds no access, and
the checks of the system are the checks it meets.

The page has four boxes:

| box | what it holds |
|---|---|
| File | the file chosen, and the gates your session holds (`voc-edit`, `dict-edit`, `bp-edit`) |
| Which records | the way the records are chosen, and how many that selects now |
| What to do to them | up to ten operations, in order |
| Result | the dry run, the last run, the last run's undo, and before and after of the first twenty records that would change |

### The file

**F** lists every file your VOC points at, with the reason beside each one this page will not update, and lets
you type a name. The page updates **dynamic data files only**. It refuses, up front and by what the file is and
by its name: a directory file, a sequential file, a file on another server, the **VOC**, a **dictionary** (a
name ending `.dic`) and a **program file** (`bp`, `bp.out`, any `.bp` or `.bp.out`). It also asks the system
whether your session may save a change to the file, and when the system says no, **the system's own words** are
what you see (a dictionary or a program file in an account without `dict-edit` or `bp-edit`, or a file of the
shared account without `shared-write`). A read-only file is refused. Choosing another file clears the
selection and the operations.

### Which records

**M** chooses how: **conditions**, **a saved list** or **every record**. After every change the page counts what
the choice selects.

* **Conditions** are up to four rows of *item*, *operator* and *value* (**N** adds one, **E** changes the one
  under the cursor, **X** takes it out, **J** switches between *all of them must hold* and *any of them may*).
  The item is picked from the file's own dictionary (or `@id`); the operator is one of *equal to*, *not equal
  to*, *less than*, *less than or equal to*, *greater than*, *greater than or equal to*, *matches the pattern*
  and *does not match the pattern* (a pattern the query processor cannot read selects nothing and says nothing,
  so the count is 0). The value is one to sixty letters, digits, spaces and the characters
  `. , : + - _ / @ ( ) % *`, with no space at either end. The conditions become one `select` command made only
  of words the page picked itself, so **a value cannot carry a quote or a second command**: anything else is
  refused with the reason. For a selection the page cannot build, type the `select` at the prompt, keep it with
  `save.list` and choose the saved list here.
* **A saved list** (**L**) is chosen by name from the account's saved lists. A name that is in the list twice is
  taken once. At most 20000 ids.
* **Every record** takes the whole file.

One run takes at most 100000 records; a bigger selection is counted and refused. The page uses the session's
default select list (list 0) for the count, so a list you had active is not kept.

### What to do to them

**N** adds an operation, **E** changes it, **X** takes it out. Each works on one attribute, given as a
number from 1 to 999 or picked from the D items of the file's dictionary, and on the **attribute as a
whole**:

| operation | does |
|---|---|
| set to a constant | puts the text in the attribute |
| set to null | empties the attribute |
| append text | adds the text at the end |
| prepend text | adds the text at the start |
| replace text | replaces every occurrence of one text with another (an empty second text takes it out) |
| add a number | adds a number (a negative one takes away); the attribute must hold a number, and the sum is kept to 4 decimals, so a number or an amount with more decimals (or more than 15 characters) leaves the record alone |
| upper case, lower case | changes the case of the letters |
| copy from another attribute | puts another attribute's value in this one |

Text is printable ASCII, at most 120 characters. There are no expressions. An operation that changes nothing
writes nothing (an attribute past the end of the record is not padded for nothing); two values that look like numbers are compared as text, so putting `007` over `7` is a change. A record where **add a
number** meets an empty attribute, text or too many decimals is **not touched at all**: the dry run counts it as one it cannot work
out and apply leaves it alone.

### The dry run

**R** makes the dry run, and **it writes nothing**. It reads every selected record, works out the new one and
tells you how many were *selected*, *would change*, *would stay as they are*, *cannot be worked out* and *were not
found*, with before and after of the first twenty that would change (the page moves to the Result box; Up and
Down read the list). **A is on the function-key row only while a dry run of exactly the settings on the screen
stands**; any edit of the file, the selection or an operation makes it stale.

### Apply

**A** shows a box with the operations in words and the number of records, and asks for **the file's name,
typed**. Cancel is what Enter chooses. Then, for each record the dry run found would change:

1. the record is read for update; one that **another session holds locked is skipped and counted**;
2. if it is **no longer exactly what the dry run read** (someone changed it since, or it is gone), it is skipped
   and counted;
3. the record as it is goes to `&bulk.undo&`, then the new record is written, then the lock is released;
4. the **first write error stops the run**.

The Result box says how many were to change, changed, skipped because locked, skipped because they were not as
the dry run read them, and errors. One line goes to the audit trail: `bulk update file=<file> records=<n>`,
with no data. After a run the dry run is spent: **R** makes another.

### Undo

`&bulk.undo&` is a file of your own account, made the first time through a box that shows
`create.file &bulk.undo&`. The page uses it only if it is a dynamic file with that name standing in your own
account directory that the system lets you change: a VOC name pointed at a program file, a dictionary or a file
elsewhere is refused, and nothing is applied or put back. It holds **the last run only** (a new run replaces it): a header and, for each
record changed, its id, a digest of what the run wrote and the record as it was. **U** puts the last run back,
after a box that asks the file's name typed. A record is put back **only if it is still exactly what the run
wrote**: one changed since, one gone, one another session has locked, is left alone and counted (a locked one can
be put back by another **U** once it is free). Undo writes one audit line, like a run: `bulk undo file=<file> records=<n>`, with no data.

### What the keys do

| key | does |
|---|---|
| Tab | changes the list (Selection, Operations, Result) |
| **F** | choose the file |
| **M**, **L**, **J** | how the records are chosen, a saved list, all or any (Selection) |
| **N**, **E**, **X** | add, change, remove a condition or an operation |
| **R** | dry run |
| **A** | apply (only after a dry run of these settings) |
| **U** | undo the last run |
| F5 | read the file, the count and the undo file again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**Gates.** Nothing is added to what your session may do. The edit gates are the system's: a dictionary or a
program file is refused here whatever the gates say, and an account without the gate meets the system's own
refusal. The page shows the gates it holds and never tries a write to find out. A file of the shared account is
judged by the system the same way (its records need `shared-write`).

## tool.catalog - the programs of the account

```
tool.catalog
```

**`tool.catalog`** lists the records of the account's program files, one row each, file by file and in name order. A program file is a directory file called `bp`, a file whose name ends in `.bp`, or a file that has a file of the same name and `.out` beside it (where the compiler puts the compiled programs). The page also lists the entries of the private and the local catalogue that no program record accounts for, under the file name `(private)` or `(local)`, so that they can be taken out.

| column | what it says |
|---|---|
| File | the program file, or `(private)` / `(local)` for a catalogue entry on its own |
| Program | the record's name (the entry's name for a catalogue entry on its own) |
| Kind | `program`, `subroutine`, `function` or `class`, read from the compiled program; `include`, `screen` or `options` for a record that is not compiled by itself; `-` for a record not compiled yet |
| Compiled | when the compiled program was made |
| Object | the size of the compiled program in bytes |
| State | `current`: the source has not been changed since it was compiled; `stale`: the source's file is newer than the compiled program's, so B compiles it again; `?`: the page could not read one of the two times (the box says why); `-`: not compiled |
| Catalogued | where the program is catalogued under its own name: `private` (a record of the account's `cat` file; `(older)` or `(newer)` when it is a copy of another compile than the one in the `.out` file), `local` (a VOC entry that points at the compiled program; `as name` when the entry has another name), `global` (SDSYS's catalogue has an entry of that name: the page only reports it, and cannot tell whether it is this program) |

The box under the list describes the row under the cursor: the paths of the source and of the compiled program, their sizes and times, current or stale, and the three catalogues in words. The line between the boxes shows the gate **bp-edit**, asked of the system, and the number of programs, compiled programs and catalogue entries.

### What the keys do

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **B** | compile the program (`basic file name no.query`) and show the compiler's lines, errors and warnings, in a box |
| **C** | catalogue it privately (`catalog file name no.query`): a copy of the compiled program goes into the account's `cat` file |
| **L** | catalogue it locally (`catalog file name local no.query`): a VOC entry that points at the compiled program |
| **X** | take a local entry out **and delete the compiled program it points at** (`decatalog name`) |
| **D** | take a private or a local entry out (`delete.catalog name`, or `delete.catalog name local`); the compiled program stays. With both, the page asks which |
| **/** or F11 | show only the rows whose program or file name holds some text |
| Esc | clear the filter |
| F5 | read the programs and the catalogues again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**Every change goes through a box.** The box shows the exact command and what it does, and has two buttons, *Run* and *Cancel*; **Cancel is the one Enter chooses**. **X** and **D** then ask for the entry's name, typed; so does **C** or **L** when the program is already catalogued somewhere else under the same name, because `no.query` makes `catalog` take that other entry out without asking, and the box names it. The page adds `no.query` to `basic` and `catalog` because a question they would ask could not be shown on this screen; a source with a `$catalog` line is therefore catalogued by its compile without being asked about an entry of the same name elsewhere. What the verb says is what the status line shows. A compile that ran has its lines in a report box; a compile or command the verb refuses shows the refusal on the status line and nothing opens.

**Gates.** `basic`, `catalog`, `decatalog` and `delete.catalog` need the **bp-edit** gate (message 11408 from the verb). The page shows whether your session has it, asked of the system, warns in each box when it is off, and leaves the refusal to the verb; nothing changes then. The administrator always has the gate (the line says `on (administrator)`); for anyone else the administrator turns it on with `modify.account`. **X** is not run on a local entry whose pointer leads outside your account: `decatalog` deletes the file the entry points at without asking whether the account may reach it, so the page says which command to type instead. `catalog` looks for an entry of the same name by name: the box names a local entry of that name even when it points at another program, and asks for the name typed. **Global cataloguing is the administrator's own command and is not offered here**; a global entry is shown, never changed.
**A name the page does not give to a command.** Only names of letters a-z, digits, dot, dash and underscore that begin with a letter or a digit are put into a command (a name beginning with a dot, dash or underscore would be read by the verbs as a global name). A record with a capital, a `$` or another character, or called like an option of the verbs (`local`, `global`, `pcode`, `no.query` ...), is listed and described, and the page says which verb to type, or that it must be renamed.

**Stale.** The page reads the modification times of the source and of the compiled program, which are operating-system files; it asks the account's OS gate about each path first and shows `?` with the reason if the gate refuses. The shared account's programs and programs in other accounts' files are not listed.

## tool.test - the tests of the account

```
tool.test
```

**`tool.test`** is the test runner for the programs of the account. It lists the **tests** - BASIC programs whose record id starts with `test.` in one of the account's program files - runs them, and says for each whether it passed, failed or gave no verdict. It needs a window of 140 columns by 43 lines or more.

### What a test is

A test is a program whose record id starts with `test.` (`test.sort`, `test.invoice.totals`) in a program file of the account: `bp`, a file whose name ends `.bp`, or a directory file with a file of the same name and `.out` beside it (the place the compiler puts the object code). The program prints what it checks, and the **last non-empty line it prints** says how it went:

```
3 passed, 0 failed
```

A name and a colon may come first (`sandbox-x: 12 passed, 0 failed` - the line the project's own test suites end with). The page runs the test with `run FILE ID` and judges that line:

| the last non-empty line | the page says |
|---|---|
| `N passed, 0 failed`, with N above 0 | **pass** |
| `N passed, M failed`, with M above 0 | **fail** |
| the run **aborted** (an error stopped the program) | **fail**, and the box gives the abort message |
| anything else: no such line, nothing printed at all, `0 passed, 0 failed` | **no verdict** |

### The list

| column | what it says |
|---|---|
| Test | the record id of the program |
| Program file | the file it is in |
| Object | `yes` when its object code is in the `.out` file beside the program file |
| Result | `pass`, `fail`, `fail: abort`, `no verdict`, `not run` (not run yet in this session), `no object` (cannot be run until it is compiled), `by hand` (a name the page does not give to a command), or `running` |
| Passed, Failed | the numbers in the last line |
| Secs | whole seconds the run took |
| Ran | the time of day it finished |
| Lines | how many lines it printed |

The line between the boxes counts the results of the session and shows the **bp-edit** gate your session holds, asked of the system. The box under the list describes the test under the cursor: its result in words, the command that ran, and the end of what it printed.

### What the keys do

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **R** | run the test under the cursor |
| **A** | run every test shown, one after another, in the order shown, after a box that gives the number and the first commands (Cancel is what Enter chooses); **Esc** stops after the test that is running |
| **F** | run again the tests that failed (an abort counts as a fail), after the same box |
| **B** | compile a test that has no object code: `basic FILE ID`, after a box that shows the command (Cancel is what Enter chooses) |
| **Enter** | show what the test printed in the lower box, scrolling with Up, Down, PgUp, PgDn, Home and End; **Esc** comes back |
| **/** or F11 | show only the tests whose name or program file holds some text; **Esc** clears it |
| F5 | read the program files again (the results are kept) |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

### How a test is run

R, A and F run `run FILE ID` through the toolkit's command runner, which lets through only the words `run` and `basic` and names made of letters a-z, digits, dot, dash and underscore. **A and F ask first**, because one key starts up to 500 programs, some of which another member of a group account may have put in a shared program file; **R**, one test, is the same as typing `run FILE ID` and has no box. The page changes nothing itself: the test is the account's own object code, run as typing the command would, and it needs no `sh` and no `os` gate. (What a test does to the account's files is what the program does.) A test with no object code is not run: **B** compiles it, which needs the **bp-edit** gate; without it the compiler's own refusal is shown on the status line and nothing is compiled.

What a test prints is collected, not shown. Only the first 360 and the last 39 lines of a very long output are kept (the result says so), but the verdict is judged on all of it. A test that **asks for input** is given 50 empty answers instead of waiting, the leftovers are thrown away, and the result says how many it used. The system throws away what a program printed if it **aborts**, so an aborted test shows 0 lines and the box gives the abort message instead (for example `Unassigned variable X at line 2 of ...`).

### No time limit

BASIC has no time limit for a program and the page has none either: a test that does not end waits for ever. The page turns the break key on while a test runs, so **Ctrl-C and then Q** at the prompt SD shows (`A to abort, Q to Quit, G to continue, X to exit`) stops it and gives the page back; the break key is turned off again afterwards. A test stopped this way shows as *no verdict*, as a test that printed nothing does.

### Limits

- Results live in memory for the session and are written nowhere. The first 500 tests are listed.
- A name with a capital, an ampersand or a dollar is listed as `by hand`; the page says which command to type.
- A test that catches an error of its own and prints nothing is also told as an abort.
- The shared account's programs are not in your VOC as files, so its tests are not listed.

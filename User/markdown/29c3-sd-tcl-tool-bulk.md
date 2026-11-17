Title: SD TCL - The Development Tools: tool.bulk
Subtitle: A bulk update of one data file: a dry run first, then apply, and undo.

This page continues [SD TCL - The Development Tools:
tool.query](29c2-sd-tcl-tool-query.html).

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
| F6, Shift-F6 | changes the list (Selection, Operations, Result) |
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

## Continued in

[SD TCL - The Development Tools: tool.catalog and
tool.test](29c4-sd-tcl-tool-catalog-and-tool-test.html) — tool.catalog and
tool.test.

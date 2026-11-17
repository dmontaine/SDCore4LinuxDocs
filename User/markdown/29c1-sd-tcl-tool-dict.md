Title: SD TCL - The Development Tools: tool.dict
Subtitle: The dictionary of a file: its items, what each one shows, and its indices.

This page continues [SD TCL - The Development
Tools](29c-sd-tcl-the-development-tools.html).

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
| Type | `D` data, `I` computed, `E` an element of a data collection, `L` a link, `PH` a phrase, `X` text; any other type (an old `A` or `S` item, which SD no longer reads, among them) is shown as its first character |
| Field | the number of the field a `D` item shows (0 is the record id), or `computed` |
| Heading | the column heading |
| Format | width and justification, such as `10R` |
| Conversion | the conversion code for display |
| S/M | `S` single valued, `M` multivalued |
| Association | the name that makes multivalued items line up |
| Expression or text | an I item's expression, the text of an X item |

The box under the list says **in words** what the item under the cursor shows (which field, what heading,
how wide and how justified, what its conversion is, single or multivalued), the expression of a computed item
and whether it has been compiled, and the record as it is stored.

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **N** | make an item: asks the id, then hands the terminal to the [IDE](24a-sd-tcl-find-program-dictionaries-and-the-ide.html) on a new item, shown as the dictionary form |
| **E** | edit the item in the [IDE](24a-sd-tcl-find-program-dictionaries-and-the-ide.html) (`ide dict file item`): the terminal is handed to the IDE, and leaving it brings the page back at the same item |
| **D** | delete the item (`delete dict file item`) after a box, with the item's id typed |
| **C** | compile an I item (`compile.dict file item`) after a box |
| **T** | try the item on a record of the file: asks the record's id and shows the value the query processor would compute for it, and the same value as a query prints it |
| **I** or F6 | the indices pane |
| **F** | back to the list of files |
| **/** | show only the ids that hold some text |
| Esc | clear the filter |
| F5 | read the dictionary again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**Making an item.** N asks for the id (letters a-z, digits, dot, dash and underscore, starting with a letter or a
digit; capitals are put in lower case; an id that already exists in any case is refused). A wrong id is refused with
the reason and the question is asked again; Esc leaves the question and nothing is written. Then the terminal is
handed to the [IDE](24a-sd-tcl-find-program-dictionaries-and-the-ide.html) on a **new** item, which it shows as the
dictionary form (described with the IDE): the Type first, then the rows that type needs (a data item has its
field number, conversion, column heading, length and justification, single or multivalued and association; an
indirect item starts with its expression), each checked as you leave it. **Accept** writes the record and
**Cancel** (or Esc) leaves nothing behind. **The page writes nothing itself**: the IDE asks whether your account
may change the dictionary (`dict-edit`) and, when it may not, says so in the system's own words and writes nothing.
Ctrl-Q leaves the IDE and brings the page back with the cursor on the new item.

**Trying an item.** T asks the id of a record of the data file. A D item gives its field; an I item
must have been compiled first (C does it), and T says so, before it asks for
a record, if it has not. The page shows the value (several values are shown between bars) and, for a D or I
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
| **I**, F6 or Esc | back to the items pane (F6 goes to the AI line first when the AI is on for your account) |

N runs both verbs after one box, because an index that is defined and not built is a trap;
B builds one that is left over. Building and deleting need the file to themselves: if another session has the
file open the verb says so and nothing changes. The page itself keeps no file open while it waits.

**Every change goes through a box.** The box shows the exact command and says what it does, with *Run* and
*Cancel*; **Cancel is the one Enter chooses**, so a stray Enter runs nothing. Deleting an item and deleting an
index then ask for the id or name, **typed**; a wrong one does nothing. The commands are the ordinary verbs, so
their checks are the checks, and what the verb says is what the status line shows.

**Gates.** Writing a dictionary needs the **`dict-edit`** gate: without it the page's own write (N), the IDE's save
(E) and the `delete` verb (D) are refused, and the record is left as it was. Compiling an item (C) and making,
building and deleting indices are not held back by it. The page shows whether you hold `dict-edit`, asked of the
system, and the box for N and D says when the change is expected to be refused. The administrator turns the gate
on for an account with `modify.account` (see *Accounts and Security*). The dictionaries of the **shared account**
follow the shared account's own rules and are not changed from here.

**Limits.** The page makes data and indirect items; other kinds (links, phrases, text, collection
elements) are listed, described, tried where they hold a value, and edited in the IDE. It does not copy
items between files, and it does not edit another account's dictionaries (that is the administrator's, on `tool.entries`). Indices are made
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
in a box. Making an item (N) shows the record the page writes, which no verb takes. Editing in the IDE (E) and listing
an index (L) hand the terminal over with no box.

## Continued in

[SD TCL - The Development Tools: tool.query](29c2-sd-tcl-tool-query.html) —
tool.query.

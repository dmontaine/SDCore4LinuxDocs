Title: SD TCL - The Development Tools: tool.query
Subtitle: The query and report builder: a list, sort, count or sum sentence built in five boxes, run and saved.

This page continues [SD TCL - The Development Tools:
tool.dict](29c1-sd-tcl-tool-dict.html).

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
| F6, Shift-F6 | next and previous box |
| **R** | run the sentence; the output is shown in the Results box and nowhere else |
| **E** | edit the sentence as text; a change in any box writes it again from the boxes |
| **S** | save the query; a form asks the name (a-z, 0-9, dot, dash, underscore; at most 40; capitals are made lower case) |
| **L** | the saved queries (up to 100) in a pick window: type to narrow it, **Enter** loads one, **Del** deletes one, Esc closes it |
| F5 | read the files and the dictionary again; what no longer fits is dropped |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**Every question is a small form**: the file filter, a condition's value, the heading, the footing, the first-*n* sample, the sentence edited by hand and the name a query is saved under. The form explains what it wants. An answer the page refuses (a quote or a semicolon in a value, a sample that is not a whole number from 1 to 99999, a sentence with a word that sends the output elsewhere, a name with a character other than those above) is explained inside the form, with the form's explanation kept under the reason, and the form stays open with what you typed so you can correct it; Esc or Cancel leaves it and changes nothing.

In the Results box Up, Down, PgUp, PgDn, Home and End scroll, Left and Right move 20 columns sideways, and Esc goes back to the boxes. The box keeps 2000 lines and says how many there were. A query on a big file is run in full and cannot be stopped from here: use the first-*n* option for a trial. A select list that is waiting narrows the query, and the box says so.

**Everything that is run is checked first.** A sentence the page runs starts with `list`, `sort`, `count` or `sum`, names the chosen file, and then holds only words from a fixed list, numbers, the items of that file's dictionary and values in double quotes. A word that sends the output somewhere else or writes (`to`, `saving`, `lptr`, `csv`, `as`, `file` and others) is refused, even when it is the name of a dictionary item. So is a semicolon, a single quote and a word the page does not know. The sentence the boxes make, a sentence you edit and a sentence a saved query holds are checked again by the same routine just before they run. An item whose name has a character the page does not use, or is also a word of the query language or a VOC keyword, is listed but cannot be marked. A phrase (`PH`) is not listed.

**Saved queries** are records of the file `&queries&` in your account. The page makes the file when you save the first query, after a box that shows `create.file &queries& dynamic`. Every save is a box too, and replacing a saved query asks its name typed. A saved query is data: when it is loaded every part is checked against the file's dictionary, the operator table and the quoting rule, and what does not pass is dropped and counted in the status line. **L** shows them in a pick window: a row a query with its name, its file, its kind (list, count or sum) and the sentence it was saved with, under a heading row; typing narrows the list to the queries that hold the text in any column. **Enter** loads the query under the cursor, **Del** deletes it after a box that asks its name typed, Esc closes the window and loads nothing. After a load, a refusal or a delete the page is shown again with what happened on the status line; L opens the list again. **Before every save and every delete the page checks the file**: `&queries&` must be an ordinary data file standing in your own account directory under that name, of no protected kind, and one your gates allow you to change. An entry `&queries&` in your VOC that leads somewhere else, to the program file `bp` for example, is refused (*nothing was saved* / *nothing was deleted*, with the reason). A record that is not a saved query (its first field is not `query1`) is never written over or deleted from here: *... is not a query this page saved ...: it was not changed*. `tool.bulk` makes the same check of its undo file.

**Limits.** One file at a time. No run-time prompts, no VOC paragraph, no printing (`lptr`) and no output to a file or a list. The phrases and the `$query.defaults` record of a dictionary belong to the account and are expanded by the query processor; the page does not list a phrase and cannot see the defaults.

## Continued in

[SD TCL - The Development Tools: tool.bulk](29c3-sd-tcl-tool-bulk.html) —
tool.bulk.

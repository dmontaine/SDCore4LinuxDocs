Title: SD Text User Interface - The Pickers
Subtitle: The fourth example, continued: a pick list the program makes, the record picker, the file and record picker, and menus that start with Quit.

These are the three pickers of `browse`, whose program is on
[Panes and Pickers](05-panes-and-pickers.html). Each picker is a window over the
page; it puts back the screen under it when it closes.

## A pick list the program makes

Mode `list` picks one entry of a list the program gives; the picker opens and reads
nothing. Each field of `items` is one entry: value 1 its name, value 2 the texts of
its other columns. `mode<2>` names the columns and `mode<3>` gives their widths. On
the way in `pid` is the window's title and `pstart` the entry to start on; on the
way out `pid` is the number of the entry chosen. **Ctrl-P** opened it:

```
17   |                           +- Jump to a note ---------------------------------------------------------------+                           |
18   |                           | filter:                                                                  3 of 3|                           |
19   |                           | Note              Begins                                                       |                           |
20   |                           | garden            Tomatoes, beans and the old roses by the fence.              |                           |
21   |                           | phone             Call the plumber about the kitchen tap.                      |                           |
22   |                           | reading           Read the chapter on dictionaries again, then try the example |                           |
23   |                           | ? shows help for the highlighted entry                                         |                           |
24   |                           +--------------------------------------------------------------------------------+                           |
```

Typing narrowed the list; **pho** left one entry:

```
18   |                           | filter: pho                                                              1 of 3|                           |
19   |                           | Note              Begins                                                       |                           |
20   |                           | phone             Call the plumber about the kitchen tap.                      |                           |
```

Enter answered `ok` with entry 2, and the status line said `Jumped to phone`. With
a filter that matched nothing the list said `nothing matches`, and Enter chose
nothing.

## The record picker

Mode `record` lists the records of the file given, by the account's own rights.
**Ctrl-R** opened it:

```
18   |                                      | |   +- Pick a record in notes (Ctrl-N: a new one) -+                                            |
19   |                                      | |   | filter:                               3 shown|                                            |
20   |                                      | |   | garden                                       |                                            |
21   |                                      | |   | phone                                        |                                            |
22   |                                      | |   | reading                                      |                                            |
23   |                                      | |   | ? shows help for the highlighted entry       |                                            |
24   |                                      | |   +----------------------------------------------+                                            |
```

Enter answered `ok` and `garden`. **Ctrl-N**, after `xyz` was typed into the filter,
answered `new` with `newtext` = `xyz`: the status line said
`Ctrl-N in the picker: a new record would be xyz`. The picker makes no record; a
program that offers one writes it in its own code, as the third example does.

## A file, then a record

Mode null lists the files of the account's VOC first, then the records of the file
chosen. **Ctrl-F** opened it:

```
15   |                                      | |    +- Pick a file ------------------------------+                                             |
16   |                                      | |    | filter:                              8 of 8|                                             |
17   |                                      | |    | bp                                         |                                             |
18   |                                      | |    | bp.out                                     |                                             |
19   |                                      | |    | dict.dict                                  |                                             |
20   |                                      | |    | newvoc                                     |                                             |
21   |                                      | |    | notes                                      |                                             |
22   |                                      | |    | syscom                                     |                                             |
23   |                                      | |    | voc                                        |                                             |
24   |                                      | |    | zzout                                      |                                             |
25   |                                      | |    | ? shows help for the highlighted entry     |                                             |
26   |                                      | |    +--------------------------------------------+                                             |
```

**notes**, then **phone**, answered `ok`; the program opened the file itself and read
the record: `notes phone: 39 characters`.

`zzout` is a VOC pointer to a directory outside the account, which the account's own
`open` refuses. Chosen, it answered `cancel` at once, with no list of records, and
the status line said `Nothing picked (cancel)`. **The picker reaches nothing the
account cannot reach.**

## Menus that start with Quit

File holds only **Quit** here, so **Esc** opened **Go**, the first menu whose first
entry is not Quit. **F10** opened File, and **Alt-G** opened Go:

```
 0   File  Go
 1   +- No Jump to a note              ^P *]+ +- Text -------------------------------------------------------------------------------------[-]+
 2   | gar Pick a record               ^R   | | Tomatoes, beans and the old roses by the fence.                                               |
 3   | pho Pick a file and a record    ^F   | |                                                                                               |
```

The open menu is drawn over the boxes; each entry shows the key it is bound to.

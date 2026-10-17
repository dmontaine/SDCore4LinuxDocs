Title: SD TCL - The ed Line Editor
Subtitle: The editor that runs inside SD, needs no terminal, and can be driven from a script.

SD has four editors for a record and they are all installed with it. **`ed` is
the one that needs no terminal**: it is written in SD BASIC and runs *inside*
SD, draws nothing, and needs neither a terminal nor operating-system permission.
That is what makes it the editor for a phantom, an API session, a session driven
down a pipe, and anything you want to automate.

The other three are full-screen. [sed](27a-sd-tcl-sed.html) is also written in SD
BASIC and runs inside SD, so it needs no operating-system permission either;
[nano](26-sd-tcl-edit.html) and [micro](27-sd-tcl-micro.html) hand the record to a
full-screen program. Use one of those when you are sitting at a terminal and want
to see the whole record at once. A record that is a data collection has an editor
of its own, [ced](27b-sd-tcl-ced.html).
**`edit` is not another program** — it is a second name for `ed` itself,
since there is no Linux program to alias it to the way SD Core for
Windows aliases it to Microsoft Edit.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part. **`ed`'s own
commands are shown in upper case**, which is how `ed`'s `HELP` prints them; it
folds case too.

> **Every listing on this page was produced by running it**, on SD Core for
> Linux, against a scratch record in an account's `bp` file.

## Starting it


```
ed {dict} file {record...} {no.query}
```

Naming the record opens it straight away:

```
ed bp zzed
```

```
bp zzed
New record
----:
```

`----:` is the prompt. A record that exists reports its length instead:

```
bp zzed
3 line(s)
```

**`creating.seqkey` in the place of a record name** edits a new record under the
file's next sequential id, the counter that `write … creating.seqkey` uses:
`ed bp creating.seqkey`. The id is taken when the edit begins and shown like any
record id, so a record that is never filed leaves a gap in the sequence, and an id
that a record already holds is skipped. A file that is not a hashed file, such as a
directory file, is refused with a message, as is a file opened read only. In
quotes, `'creating.seqkey'` is an ordinary record id.

**Omit the record name and `ed` asks for one**, and asks again after each edit
until you give it an empty answer. **Give several names and it works through
them in order** — the record after the current one is reached by filing or
quitting the one you are on:

```
ed bp zzed zzedb
```

```
bp zzed
3 line(s)
----: Q
bp zzedb
New record
----:
```

**A file name is tried as typed, then lower case, then upper.** A file that
matches none of the three stops the verb before the editor starts:

```
ed nosuchfile zzed
```

```
File not found
```

`dict` edits the file's dictionary rather than its data. It is the same
addressing as everywhere else, and a dictionary with no such entry is a new
record like any other:

```
ed dict voc who.am.i
```

```
DICT voc who.am.i
New record
```

## The commands

### Making a record from nothing

`I` inserts one line after the current one. At the top — where a new record
starts — it inserts at line 1:

```
ed bp zzed
I * ZZED - a scratch record for the SD TCL editing page
I crt 'ZZED OK'
I end
T
P20
FI
```

```
bp zzed
New record
----: I * ZZED - a scratch record for the SD TCL editing page
Bottom at line 1
----: I crt 'ZZED OK'
Bottom at line 2
----: I end
Bottom at line 3
----: T
Top
----: P20
0001: * ZZED - a scratch record for the SD TCL editing page
0002: crt 'ZZED OK'
0003: end
Bottom at line 3
----: FI
'zzed' filed in bp
```

`I` **with no text** starts a multi-line insert instead, prompting `0001= ` for
each line until you enter an empty one. `IB` is the same as `I` but inserts
before the current line rather than after it.

### Moving about

| | |
|---|---|
| **`T`** | to the top — *before* line 1, so `I` inserts at 1 |
| **`B`** | to the last line |
| *`n`* | to line *n* |
| **`+`**n*, **`-`**n* | *n* lines forward or back |
| **`G`**n*, **`PO`**n* | to line *n*, the long ways round |
| **`G<`**, **`G>`** | to the first or last line of the block |

### Looking

| | |
|---|---|
| **`P`**n* | display *n* lines from the current line |
| **`PL`**{**`-`**}*n* | *n* lines relative to the current line |
| **`PP`**n* | *n* lines centred on the current line |
| **`PB`** | the block |
| **`L`** *string* | the next line **containing** *string* |
| **`F`**{*col*} *string* | the next line with *string* **at** column *col*, default 1 |
| **`M`** *pattern* | the next line matching a pattern |
| **`COL`** | a column ruler |
| **`?`** | where you are and what is set |

**`P` leaves the current line at the last line it printed, and that is what
the next command acts on.** It is the one thing on this page that catches
people, because "display" does not sound like a move. `P20` on a three-line
record, then `DE`, and it is **line 3** that goes:

```
----: P20
0001: * ZZED - a temporary record for the SD TCL editing page
0002: crt 'ZZED OK'
0003: end
Bottom at line 3
----: DE
Bottom at line 2
```

`?` is worth knowing before you ask anyone else:

```
----: ?
File name           = bp
Record name         = zzed
Current line        = 3
No block defined
OOPS will undo 'I end'
Searches are case-sensitive
Expansion of non-printing characters : Disabled
Non-printing character entry         : Disabled
Verification of block actions        : Enabled
```

**Searches are case-sensitive until you say otherwise** — `CASE OFF` makes `L`
and `F` insensitive, `CASE ON` puts it back.

### Changing

| | |
|---|---|
| **`I`** {*text*}, **`IB`** {*text*} | insert after, insert before |
| **`R`** *text* | replace the current line |
| **`A`** {*text*} | append to the end of the current line |
| **`C/`**old**`/`**new**`/`{*n*}{**`G`**}{**`B`**} | change *old* to *new* in *n* lines. `G` every occurrence, `B` over the block |
| **`R/`**old**`/`**new**`/`… | the same, without moving |
| **`D`**n*, **`DE`**n* | delete *n* lines from the current one |
| **`DUP`** {*n*} | duplicate the current line |
| **`CAT`** {*string*} | join the next line onto this one |
| **`FORMAT`** | re-indent BASIC source |

The delimiter of a `C` command is whatever character follows the `C`, so a
change involving `/` can use `,` or `:` instead.

### `OOPS` undoes the last thing that changed the record

One step, and it names what it is undoing:

```
----: OOPS
Undoing 'DE'
```

`?` tells you in advance what it would undo, which is the line above reading
`OOPS will undo 'I end'`.

### Blocks

`<` sets the start of a block at the current line, `>` the end, `<>` makes the
current line a one-line block. Then `COPY` copies it after the current
position, `MOVE` copies and deletes the original, `DROP` deletes it, and `PB`
displays it. `<` at the top clears the block.

### Values on a line

A field is a line, so `ed` handles fields on its own. **A value mark and a
subvalue mark are single unprintable characters**, and a line holding them
displays as one run with a stray glyph in it. `EV` opens the current line as if
its values were lines:

```
----: EV
Editing values. Use SV to save changes or QV to discard changes
----: P20
1.0001: NAME
1.0002: Smith
1.0003: Jones
Bottom at line 3
----: QV
EV mode changes discarded
Returned from EV mode
```

`SV` leaves `EV` keeping the changes, `QV` discards them. Three levels are
available: values, subvalues, and the elements of a compound I-type.

**In `EV` a line number carries the positions above it** (16 Oct 2026): the
example edited field 1, so its values are `1.0001`, `1.0002`, `1.0003`; one
level down, in the subvalues of value 2 of field 1, a line is `1.2.0001`.
`NO.EV.POSITION` in the `$ed.options` record of the VOC leaves the prefix out
and numbers the lines as before.

**A mark is typed as `^` and its character code**: `^253` for a value mark,
`^252` for a subvalue mark, `^^` for a literal `^`. The line above was made
with `I NAME^253Smith^253Jones`.

**Text marks (`^251`), subvalue marks and value marks can be typed without
`NPRINT`.** The field mark (`^254`) and the item mark (`^255`) still need it,
because one in a line would split the line without showing it.

`EV` on an I-type that holds quoted text, brackets and semicolons no longer
corrupts the expression; a quoted string used to be cut at the wrong place.

### Leaving

| | |
|---|---|
| **`FI`** | write the record and end the edit |
| **`FIB`** | file it, then `basic` it |
| **`FIBR`** | file it, compile it, and `run` it |
| **`SAVE`** | write it and **stay in the editor** |
| **`Q`**, **`QUIT`** | end the edit, **discarding changes** |
| **`X`** | abandon the whole run when a select list is in use |
| **`FD`**, **`DELETE`** | delete the record from the file and end the edit |

```
----: FI
'zzed' filed in bp
```

**`Q` asks only If you changed something**, and it asks on the same line:

```
----: Q
Record changed - OK to quit? Y
```

Anything but `Y` and you are still in the editor. On an unchanged record `Q`
says nothing at all and returns to TCL.

> **`SAVE` and `FI` with a different file or record name ask before they
> overwrite**, and so do `FD` and `DELETE`. Written back to their own record
> they ask nothing at all, which is what lets `ed` be driven from a script.

### `XEQ` runs a TCL command without leaving the editor

`@FILE`, `@ID` and `@LINE` are substituted, so a command can be about whatever
you are editing:

```
----: XEQ ct @FILE @ID
bp zzed
1: * ZZED - a scratch record for the SD TCL editing page
2: crt 'ZZED OK'
3: end
```

**And what it showed there was the filed record, not the one on the screen.**
The buffer at that moment read *"a temporary record"* — the change had not been
filed. `XEQ` runs outside the editor and sees the file, which is the answer you
want from `basic` and the wrong one from `ct`.

### `HELP`

`HELP` alone prints every command. `HELP` with a topic prints one:

```
----: HELP FI
FIle [[filename] record.id]
                Write record and end edit
```

### External commands: a catalogued subroutine as an ED command

**You can add commands to `ed`** (16 Oct 2026) by writing a subroutine and naming
the commands it handles in the `$ed.options` record of the VOC. A line of that
record such as

```
EXTERNAL zzedx1 WHERE DUMP UPCASE "'ADD 'A0X"
```

says that the catalogued subroutine `zzedx1` handles the commands `WHERE`,
`DUMP`, `UPCASE`, and any command that matches the template `'ADD 'A0X`.
After the subroutine's name come one or more patterns, one after another, with
no quotes needed; a pattern with a space in it is put in double quotes. A
pattern is a `MATCHES` template or a plain word, and the match ignores case.
The patterns are tried **before** the standard commands, so an external command
can replace one: `EXTERNAL myb B` makes your subroutine the `B` command.

The subroutine is called with two arguments:

```
subroutine zzedx1(mat info, error)
   dim info(8)
```

| `info(1)` | the file name, with `DICT` if that was given |
|---|---|
| `info(2)` | the record id |
| `info(3)` | the data being edited, a field mark between lines (in `EV` the level you are editing) |
| `info(4)` | the current line, 0 at the top |
| `info(5)`, `info(6)` | the block start and end lines, 0 if not set |
| `info(7)` | the command, in the case you typed it |
| `info(8)` | the `EV` depth: 0 normally, 1 in values, 2 in subvalues |

Set `error` to true if the command fails: the editor says *External command
`name` failed* and changes nothing. Otherwise it takes `info(3)` as the new
data and `info(4)` to `info(6)` as the new positions, which it keeps inside the
record (999 becomes the last line, -3 the top). `OOPS` undoes what the
subroutine did. The subroutine must be catalogued where the user can reach it.

**What this does not do:** the editor does not check that the subroutine exists
until a command that names it is typed; a missing one then stops the editor with
the run time's usual message. An unrecognised option in `$ed.options` is
ignored, as before.

### The command stack, and prestored sequences

Every command you type is kept. `.L` lists the stack, `.R`*n* recalls line *n*
to the top, `.X`*n* executes it again, and `.A`, `.C`, `.I` and `.D` append to,
change, insert and delete stack lines.

`.X` **with a file and record instead of a number** runs a *prestored edit
sequence* — a record holding one `ed` command per line:

```
ed bp zzseq
I ED
I L scratch
I C/scratch/altered/
I FI
FI
```

```
ed bp zzed
.X bp zzseq
```

```
bp zzed
3 line(s)
----: .X bp zzseq
0001: * ZZED - a scratch record
0001: * ZZED - a altered record
'zzed' filed in bp
```

**Field 1 is a marker, not a command. it must begin with `E`** — `ED` is the
usual thing to write — and `ed` refuses a record that does not with *"Record is
not a prestored edit sequence"*. Nothing was run for it above, and the
line numbers in error messages count it: an unrecognised command in **field 2**
is reported as line 2.

`PAUSE` inside a sequence stops it and `.XR` resumes, `.XK` abandons it;
`LOOP` repeats from a given line.

> **A prestored sequence is not an unattended mechanism.** One bad command
> **abandons the rest of the sequence and then asks a question**, and
> the answer is read from wherever the session's input comes from.
>
> ```
> ----: .X bp zzs2
> Error - Unrecognised command at line 2 of prestored commands
> Did you mean to insert this text (Y/N)? N
> ```
>
> The same is true of a multi-line `I`, which is refused outright inside a
> sequence. **If you are driving `ed` down a pipe, give every command its
> arguments** — `I` with text, `FI` with no name, never `FD` — and it runs
> through without stopping.


## Who has it

**Every account has `ed`, `edit`, `nano` and `micro`, and all of them
simply run** — unlike SD Core for Windows, there is no permission behind
`nano`/`micro` to grant first. See [The nano Screen
Editor](26-sd-tcl-edit.html).

## See also

[SD TCL - The nano Screen Editor](26-sd-tcl-edit.html) ·
[SD TCL - The micro Screen Editor](27-sd-tcl-micro.html) ·
[SD TCL - Programs and the Catalogue](24-sd-tcl-programs-and-the-catalogue.html).

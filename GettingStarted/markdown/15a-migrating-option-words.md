Title: Migrating to SD: option words
Subtitle: Every word of the option command, what it changes, and where else it is described.

This page continues [Migrating to SD](15-migrating-to-sd.html). The words are the
thirty-nine that `option` lists. (Twenty-two words that existed only to imitate other
products were removed on 27 October 2026; see the last section of
[Migrating to SD](15-migrating-to-sd.html).) **All are off in a new session.** `option` *name* turns one
on, `option` *name* `off` turns it off, `option` *name* `display` shows it. The last column
names the page of the User set that also describes the word; **here** means this
page is where it is described.

## Queries: list, sort, select and the rest of the query processor

| word | what it does | also described in |
|---|---|---|
| `assoc.all` | the query processor ignores the associations in the dictionary and treats every field as one association | *SD Basic - Program Structure* |
| `default.mv` | a C, D or I-type dictionary item whose single/multivalue flag is blank counts as multivalued, not single valued | here |
| `query.sort.no.case` | sorts ignore case (selection tests are left as they are) | here |
| `query.str.comp.all` | data in a right-aligned item is compared as strings in every relation, so with `amt > 50` the value 9 is selected and 100 is not | here |
| `query.string.comp` | `=` and `ne` always compare as strings: `with amt = "10.0"` no longer finds 10 | here |
| `query.footer.pause` | a report with a page footer waits for Return after its last footer | *SD TCL - The Query Processor* |
| `query.merge.print` | a report sent to the default printer does not close a printer that was already active, so report and program output are one print job | *SD TCL - The Query Processor* |
| `$query.debug` | lets a query take the `debugging` keyword; a development aid, shown by `option` only while it is on. Do not use it in an application | here |

## Output and conversion

| word | what it does | also described in |
|---|---|---|
| `numeric.exponent` | numbers in exponent form such as `123.45e-2` count as numeric | *SD Basic - Program Structure* |
| `pick.ml.conv.mask` | a left bracket in an `ml` or `mr` code starts a format mask, as in `mr2(#10)`, instead of asking for negatives in round brackets | *SD Basic - Program Structure* |

## Errors and diagnostics

| word | what it does | also described in |
|---|---|---|
| `unass.warning` | an unassigned variable is reported as a warning and read as null, or as zero in arithmetic, and the program goes on | here |
| `div.zero.warning` | a divide by zero is a warning and gives zero | *SD Basic - Math Functions* |
| `non.numeric.warning` | a non-numeric value where a number is needed is a warning and counts as zero | *SD Basic - Numeric Tests and Formatting* |
| `dump.on.error` | a fatal run-time error writes a process dump file (`sddump.`*n*) in the dump directory | here |
| `show.stack.on.error` | a fatal run-time error also prints the call stack: program, line and object address | here |
| `suppress.abort.msg` | `abort` prints its own message but not the line saying where it was executed | here |
| `no.user.aborts` | the A (abort) answer is removed from the prompts that offer it: pause, the end-of-page prompt, the break key menu and the query processor's page prompt | here |
| `spool.command` | shows the operating system command that prints a job, just before it runs; a diagnostic aid | *SD Basic - Program Structure* |

## Commands, programs and select lists

| word | what it does | also described in |
|---|---|---|
| `backslash.not.quote` | a backslash in a command line is an ordinary character, not a string quote: `with name = a\b` | here |
| `catalogue.local` | `catalog` and `delete.catalog` use the local catalogue by default, not the private one | here |
| `chain.keep.common` | `chain` keeps the unnamed common block | *SD Basic - Program Control* |
| `chained.select` | a select that finds records runs the first command in the data queue, as `chain` would; if it finds none the queue is cleared | *SD Basic - Program Structure* |
| `clear.select` | the command processor clears select list 0 when a command ends, if the list was already active when it began; `keep.select` in a program keeps it | *SD Basic - Program Structure* |
| `command.level.locks` | a file variable that goes keeps its locks until the program is back at the command processor | *SD Basic - Program Structure* |
| `force.reload` | compiling or cataloguing a program also refreshes the subroutine links a running program holds | *SD Basic - Program Structure* |
| `inherit` | a phantom starts with the option settings of the process that started it | *SD TCL - Processes and Phantoms* |
| `keep.old.object` | a compile that fails leaves the previous object code in place | *SD Basic - Program Structure* |
| `no.phantom.notify` | set in a phantom, it stops the message sent to its parent when it ends | *SD Basic - Program Structure* |
| `no.sel.list.query` | commands that can work through an active select list, such as `copy`, `delete`, `ct` and `ed`, do not ask *Use active select list?* first | here |
| `paginate.on.heading` | with `run` and `no.page`, a heading or footing still turns pagination on | *SD Basic - Program Structure* |
| `run.no.page` | `run`, `debug` and a catalogued program started by name begin with screen pagination off | here |
| `stacked.account` | an `execute` of a command that does a `logto` leaves the process in the account it began in | *SD Basic - Program Structure* |

## Files

| word | what it does | also described in |
|---|---|---|
| `dir.dtm` | writing a record to a directory file moves the directory's date and time modified, even when the record already existed | *SD Basic - Program Structure* |
| `dir.sel.omit.hidden` | selecting a directory file leaves out names that begin with a dot | here |
| `git` | a directory file keeps `.gitignore` and `.gitattributes` under their own names on disk; without it the leading dot becomes `%D` | *SD Basic - Program Structure* |
| `inherit.mfile.path` | `create.file` puts a new multifile subfile in the directory of the default subfile | *SD Basic - Program Structure* |
| `inherit.ownership` | `create.file` gives a new file the owner and group of the account directory. Turn it on for an account only as an administrator's decision | *SD Basic - Program Structure* |

## Correlatives and I-types

| word | what it does | also described in |
|---|---|---|
| `correlative.nocase` | string operations in a correlative or an I-type ignore case; read when the item runs | *SD Basic - Program Structure* |
| `correlative.reuse` | the array operators of a correlative or an I-type reuse the last value of a shorter array, as `reuse()` does | *SD Basic - Program Structure* |

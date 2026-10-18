Title: Migrating to SD: option words
Subtitle: Every word of the option command, what it changes, and where else it is described.

This page continues [Migrating to SD](15-migrating-to-sd.html). The words are the
sixty-one that `option` lists. **All are off in a new session.** `option` *name* turns one
on, `option` *name* `off` turns it off, `option` *name* `display` shows it. The last column
names the page of the User set that also describes the word; **here** means this
page is where it is described.

## Queries: list, sort, select and the rest of the query processor

| word | what it does | also described in |
|---|---|---|
| `assoc.all` | the query processor ignores the associations in the dictionary and treats every field as one association | *SD Basic - Program Structure* |
| `assoc.unassoc.mv` | multivalued fields with no association in the dictionary count as one association: under `by.exp` their values line up position by position | here |
| `default.mv` | a C, D or I-type dictionary item whose single/multivalue flag is blank counts as multivalued, not single valued | here |
| `pick.breakpoint` | the text of a `break.on` or `break.sup` follows the field name (`break.on city "text"`) instead of coming before it | here |
| `pick.breakpoint.u` | the line of hyphens above a subtotal is printed only when the break text carries `u`; normally `u` leaves it out | here |
| `pick.explode` | a field with a single value is not exploded in a `by.exp` listing, as Pick treats it | here |
| `pick.grand.total` | the text of `grand.total` is printed on the same line as the totals, not on the line above | here |
| `pick.implied.eq` | a double-quoted value with no operator in front of it means equals: `with city "Reno"` is `with city = "Reno"` | here |
| `pick.wildcard` | in an equality test, a value that ends in `]` means "begins with", one that starts with `[` means "ends with", both together mean "contains", and `^` stands for any one character: `with city = "R]"` | here |
| `qualified.display` | a display item may carry a test of its own: `list customers city = "Reno" name` lists only the records where city is Reno | here |
| `query.no.case` | selection tests ignore case, and so do sorts: `with city = "reno"` finds Reno | here |
| `query.priority.and` | `and` binds tighter than `or`: `a or b and c` means `a or (b and c)`. Without it the clauses are combined from left to right | here |
| `query.sort.no.case` | sorts ignore case (selection tests are left as they are) | here |
| `query.str.comp.all` | data in a right-aligned item is compared as strings in every relation, so with `amt > 50` the value 9 is selected and 100 is not | here |
| `query.string.comp` | `=` and `ne` always compare as strings: `with amt = "10.0"` no longer finds 10 | here |
| `with.implies.or` | several `with` clauses are joined by `or`, not by `and` | here |
| `query.footer.pause` | a report with a page footer waits for Return after its last footer | *SD TCL - The Query Processor* |
| `query.merge.print` | a report sent to the default printer does not close a printer that was already active, so report and program output are one print job | *SD TCL - The Query Processor* |
| `$query.debug` | lets a query take the `debugging` keyword; a development aid, shown by `option` only while it is on. Do not use it in an application | here |

## Output and conversion

| word | what it does | also described in |
|---|---|---|
| `ampm.upcase` | the time conversions write `AM` and `PM`, not `am` and `pm` | here |
| `crdb.upcase` | the `md` conversions write the `cr` and `db` suffixes as `CR` and `DB` | here |
| `no.date.wrapping` | converting a date with too large a day number, such as 31 February, is refused instead of rolling into the next month | here |
| `numeric.exponent` | numbers in exponent form such as `123.45e-2` count as numeric | *SD Basic - Program Structure* |
| `pick.ml.conv.mask` | a left bracket in an `ml` or `mr` code starts a format mask, as in `mr2(#10)`, instead of asking for negatives in round brackets | *SD Basic - Program Structure* |
| `pick.null` | `ml`, `mr` and `fmt()` of a null string return null, not zero | here |
| `space.mct` | `mct` capitalises only the first letter and letters that follow a space; without it, letters after any non-letter, such as a hyphen, are capitalised too | here |

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
| `lock.beep` | the terminal beeps about once a second while the session waits for a lock (not in a phantom or an API session) | here |
| `spool.command` | shows the operating system command that prints a job, just before it runs; a diagnostic aid | *SD Basic - Program Structure* |
| `debug.rebind.keys` | accepted and does nothing; reserved | here |
| `proc.a` | accepted and does nothing; PROC is gone | here |

## Commands, programs and select lists

| word | what it does | also described in |
|---|---|---|
| `backslash.not.quote` | a backslash in a command line is an ordinary character, not a string quote: `with name = a\b` | here |
| `catalogue.local` | `catalog` and `delete.catalog` use the local catalogue by default, not the private one | here |
| `chain.keep.common` | `chain` keeps the unnamed common block | *SD Basic - Program Control* |
| `chained.select` | a select that finds records runs the first command in the data queue, as `chain` would; if it finds none the queue is cleared | *SD Basic - Program Structure* |
| `clear.select` | the command processor clears select list 0 when a command ends, if the list was already active when it began; `keep.select` in a program keeps it | *SD Basic - Program Structure* |
| `command.level.locks` | a file variable that goes keeps its locks until the program is back at the command processor | *SD Basic - Program Structure* |
| `ed.no.query.fd` | the `fd` command of `ed` deletes the record without asking | here |
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
| `create.file.upcase` | `create.file` names the file on disk in the case you typed instead of lower case (and its dictionary `.DIC` instead of `.dic`). The lower-case rule then no longer holds for files made this way | here |
| `dir.dtm` | writing a record to a directory file moves the directory's date and time modified, even when the record already existed | *SD Basic - Program Structure* |
| `dir.sel.omit.hidden` | selecting a directory file leaves out names that begin with a dot | here |
| `git` | a directory file keeps `.gitignore` and `.gitattributes` under their own names on disk; without it the leading dot becomes `%D` | *SD Basic - Program Structure* |
| `inherit.mfile.path` | `create.file` puts a new multifile subfile in the directory of the default subfile | *SD Basic - Program Structure* |
| `inherit.ownership` | `create.file` gives a new file the owner and group of the account directory. Turn it on for an account only as an administrator's decision | *SD Basic - Program Structure* |
| `select.keep.case` | has no effect on Linux: it keeps the case of names on a file system that ignores case, which a Linux file system does not | here |

## Correlatives and I-types

| word | what it does | also described in |
|---|---|---|
| `correlative.nocase` | string operations in a correlative or an I-type ignore case; read when the item runs | *SD Basic - Program Structure* |
| `correlative.reuse` | the array operators of a correlative or an I-type reuse the last value of a shorter array, as `reuse()` does | *SD Basic - Program Structure* |

Title: Changes in L1.2-0
Subtitle: What was added, changed and removed since L1.1-3 (9 October 2026), by section and in alphabetical order.
Columns: 23 11 66

**This is the list of what changed between L1.1-3 (9 October 2026) and L1.2-0.** It is kept up to date as the
release is built. It was started on 24 October 2026 from the feature spreadsheet (its Fixes, QM4 Gaps and Subsystems
tabs) and the release changelog (`sdsys/changelog`, section "Next release"), which has the full story of each
change: what it does, why, and what it does not do. This document is the short form.

## How to read it

- Every row is one thing that was **added**, **changed** or **removed**. A fix is a change.
- The rows are grouped into sections, and **within each section they are in alphabetical order**.
- A row is one or two lines. The User and Administrator manuals have the detail; so does the changelog.
- Names are in lower case as SD writes them. `$mode` words, options and BASIC keywords are written the same way.
- Everything that lets something reach beyond a program's own account, or leave the machine, is **off as delivered**.
  The administrator turns it on, account by account, and can turn it off again.
- A comment at the end of a row, `<!--s` then item numbers then `-->`, names the spreadsheet items the row covers. It is
  for whoever maintains this document and does not show on the page.

## Read this first: changes that alter what an existing system does

| Name | Change | What |
|---|---|---|
| A keep-the-accounts upgrade | Changed | could switch the shell and `os.execute` back on; now **never** loosens a gate that is off |
| A new account | Changed | had ssh and the API on, and the shell and `os.execute` available; now has **no shell, no `os.execute`, no ssh and no API**, and every gate is closed until SDSYS opens it (`modify.account`) |
| A silent remote server | Changed | could be waited for without limit; now it is given up on after `netreply` seconds |
| A sort that uses work files | Changed | gave equal keys in an order that depended on `sortmem` and `sortmrg`; it now gives the order the sort gives in memory (equal keys newest first, the first duplicate kept) |
| AccuTerm and SDTerm | Removed | were supported; use terminal type `xterm` or `vt100` |
| An index after many deletions | Changed | in a large index (three levels) deleting records could take a whole branch out of the index, so lookups missed records that were still there; fixed, and an index damaged earlier is put right by `build.index` |
| An index and a record id | Changed | an index kept an upper-case copy of the id; now it follows the id **as the file holds it**, so rebuild an index that was built on L1.1-3 |
| Dictionary divide by zero | Changed | stopped the report; now gives zero |
| `fileinfo(f, 1021)` | Changed | gave text such as `12 (don), 14 (ann)`; now the user numbers of the other sessions that have the file open, and the text form is key **1100** |
| `intprec` and `sortmem` | Changed | were 13 and 1024; now **11** and **4096** (set the old values in `sd.conf` if you need them) |
| Removed features | Removed | words and modes that existed to imitate other products (so far 55 `option` words, 35 `$mode` words, and the second spellings and forms of statements, clauses, functions, conversions, TCL verbs and query keywords, each listed in [REMOVED](#removed)), and other things: see [REMOVED](#removed) |
| `sed` keys | Changed | were Emacs keys with Ctrl-X sequences; now the keys most editors have (Ctrl-PageDown / Ctrl-PageUp, and Alt-PageDown / Alt-PageUp for a terminal that keeps the Ctrl keys for its own tabs, switch buffers), and `emacs` in `&sed.options&` keeps the old layout |
| `sed`, `ide`, `!ced()` | Changed | were 120 by 36 or less; now need a window of at least **140 by 42** (the `ide` **140 by 43**), and `ed` is the editor for a smaller one |
| `select file field` | Changed | a field not otherwise used was ignored; now it is `saving multivalued field`, so the list holds the values |
| The default terminal | Changed | was 120 columns by 36 lines; now **140 by 42** (a LIST fills 41 lines before it pauses) |
| The group size of a new file | Changed | was 2 KB (1 KB when `sd.conf` did not say); now **4 KB** on a new installation. An installed system keeps its `sd.conf`, and so its 2, and a file keeps the size it has |
| `when field` with no operator | Changed | kept the null values; now keeps the values that are **not** null |
| Where a session starts | Changed | was the command prompt; now the **home screen** of tiles, and `set.start.default` chooses the prompt for an account |

## Sections

**Built from the openQM list** (each row is an item on the feature spreadsheet): [ADMIN](#admin) · [API](#api) ·
[BASIC](#basic) · [DATA](#data) · [FILES](#files) · [QUERY](#query) · [SYSTEM](#system) · [TCL](#tcl) · [TOOLS](#tools).

**[REMOVED](#removed)**: what SD no longer has, and what to write instead.

**[New Features Unique to SD Core](#new-features-unique-to-sd-core)**, not part of openQM and not on the spreadsheet:
[Administration](#administration) · [AI](#ai) · [API and client library](#api-and-client-library) ·
[Commands](#commands) · [Data formats](#data-formats) · [Encryption](#encryption) · [Files](#files-1) ·
[Installer](#installer) · [Screen library](#screen-library) · [SDNet](#sdnet) · [Security](#security) · [System](#system-1) ·
[Tools and the home screen](#tools-and-the-home-screen).

**[NO CHANGE](#no-change)**: openQM items that needed nothing.

## ADMIN

Administrator commands from the openQM list.

| Name | Change | What |
|---|---|---|
| `config()` name limit | Changed | a parameter name may be up to sixteen characters (was eight), so `config('SCREENTHEME')` finds the setting; a longer name is not found |
| `inhibit.login` | Added | administrator only: stops new sessions while maintenance is done; a killed backup no longer locks everybody out <!--s 387 g46--> |
| `lock.tracer` | Added | administrator only: logs every lock taken and released, with program and line, to the file `locktrace` <!--s g57--> |
| `logout` | Changed | `logout n group` also ends the phantoms n started; `logout` of a session whose process has gone clears the entry and its locks <!--s 386--> |
| `newvoc.mods` | Changed | applied to SDSYS's own VOC and kept across an upgrade that keeps the accounts <!--s 501--> |
| `SCREENTHEME` | Changed | readable with `config()`; the shipped `sd.conf` says `SCREENTHEME=blue` and the installer adds that line to a restored `sd.conf` that has none (an existing line, `mono` included, is kept); a terminal with no colour stays `mono` |

## API

The server side of the API, the client library and the language headers.

| Name | Change | What |
|---|---|---|
| `autologout` | Changed | reaches an API session; a client hang found while testing it is fixed <!--s 474--> |
| client library headers | Added | C# (`sdclient.cs`) and PHP (`sdclient.php`) beside the six already there; neither has been run against a runtime <!--s g200--> |
| client library: connections | Changed | the number of simultaneous connections is no longer limited <!--s 134--> |
| client library: detailed error | Changed | the BASIC class `sdclient` returns the detailed status when it cannot connect <!--s 571--> |
| client library: dictionary | Added | `sdevaluate`, `sdevalconv`, `sdiconv`, `sdoconv`, `sdiconvs`, `sdoconvs` <!--s 247 409--> |
| client library: files | Added | `sdopenseq`, `sdreadseq`, `sdreadblk`, `sdwriteseq`, `sdwriteblk`, `sdseek`, `sdweofseq` <!--s 441--> |
| client library: fixes | Changed | `sdlogto`, `sdchange`, `sddcount` and a second `sdconnect` were checked and found correct, with tests <!--s 260 261 262 272 281--> |
| client library: more functions | Added | `sdrevision`, `sdgetvar`, `sdsystem`, `sdindices`, `sdtrans`, `sdrtrans`, `sdtxn` <!--s 89 195 410 499 442--> |
| client library: python | Added | a Python wrapper for the library <!--s 457--> |
| client library: `sdcallx` | Added | `sdcallx` and `sdgetarg`: calls with arguments of any size from the C client library <!--s 194--> |
| client library: threads | Added | each thread has its own session, transfer buffer and arguments; several threads may use the library <!--s 456--> |
| client library: tls | Changed | the network session is always encrypted (TLS), so SD meets the QMClient encryption items <!--s 88 133--> |
| `master.login` | Changed | the paragraph runs for API connections as for interactive and phantom sessions <!--s 170--> |

## BASIC

Statements, functions, `$mode` words and compiler directives.

| Name | Change | What |
|---|---|---|
| `~=` | Added | comparison that ignores case <!--s 430--> |
| `account.path()`, `vocpath()` | Added | the pathname of an account and of a file named in the VOC, told only where the account may open it <!--s g107 g193 86--> |
| `arg.present()`, `reusing()` | Added | whether the caller passed an argument, and whether with `reuse()` <!--s g108 g169--> |
| `$basic.options` | Changed | a `mode` line takes a list and a minus turns a mode off; an `include` line names records or files that every program includes <!--s 406 407 290--> |
| `bool()` and friends | Added | `bool()`, `is.null()`, `numeric()`: Boolean, SQL-null and numeric conversions <!--s g109 g144 g161 451--> |
| `@build.time`, `@line` | Added | the time the program was compiled and the source line it stands on <!--s 506 211--> |
| `casing on` and `off` | Added | case sensitivity of string comparisons for the rest of the program <!--s g111 g274--> |
| `ceil()` and `floor()` | Added | `ceil()`, `floor()`, `roundup()`, `rounddown()`: whole numbers above and below, and rounding in steps <!--s g112 g129 g174 g175--> |
| `child()`, `signal()` | Added | whether a user number is a running phantom of this process; raises a signal in another process <!--s g113 g182 301--> |
| `class ... inherits as` | Added | the inherited class's object variable can be named; an empty `()` is accepted after a method name <!--s 374 237--> |
| `class` initial values | Added | a `public` or `private` variable may start with a value; `inherits` passes constants to the inherited class <!--s 356 565--> |
| `class` lookup | Changed | a class with 32 names or more is searched through an index, many times faster <!--s 13--> |
| `class`: `restricted` | Added | a name for the class and the classes that inherit it, and no one else <!--s g168--> |
| `class`: `run` | Added | `run` of a class module or its catalogue name makes the object, runs its `main` and lets it go <!--s 484--> |
| `clearcommon name` | Added | sets the variables of the named common block to zero <!--s 52--> |
| `compare()` | Changed | an `i` after `l` or `r` in the justification compares ignoring case; `compares()` does it over two arrays <!--s 307 g114--> |
| `convert()` | Changed | `mcn-`, `mc/n-`, `mcs`, `mcp` with a quoted replacement character, `mt` with `m`, `md` options in any order <!--s 23 183 198 298 488--> |
| `dir()` | Changed | includes the size of each file; lists a plain file as `F` and a directory as `D` only, so a socket is no longer a file and a block device no longer a directory <!--s 366--> |
| `fix()` | Added | a number with a fixed number of decimals, rounded or cut off <!--s 472--> |
| exceptions | Added | `try`, `catch`, `throw`, `caught()` and `@exception`; many run time errors are caught under openQM's `sys.` names; `dumping` and `saving.stack` <!--s 353 354 355 295 309--> |
| `execute ... stacklist` | Added | keeps the default select list and puts it back when the command returns <!--s 61--> |
| `execute.list` | Added | runs commands for each id of list 0 in turn <!--s g38--> |
| `fcontrol()` | Added | the openQM function: next sequential key, valid id, minimum modulus, line terminator modes, forced writes <!--s 452 102--> |
| `field()` and `vslice()` | Changed | take an asterisk for the number of elements and a subvalue slice <!--s 212 132--> |
| `flush.dh.cache` | Added | makes every process close the dynamic files it keeps cached <!--s 83 123--> |
| `for` with a list | Added | a loop over a list of values, and over the elements of a delimited string, with a delimiter <!--s 84 300--> |
| `get var from device` | Added | reads from a FIFO, port, character device or `openseq` file a character at a time, with a timeout <!--s 583--> |
| `getlocks()`, `testlock()` | Added | information about file and record locks; the owner of a task lock <!--s 508 42--> |
| `getpu()` | Added | the `pu$pathname` key (`pu$form.queue` was added and removed again, see REMOVED) <!--s 214--> |
| `groupstore` and `revremove` | Added | `groupstore`, `revremove`, `setrem`, `rmvd()`: statements and functions over delimited strings <!--s g136 g170 g172--> |
| `$ifdef`, `$ifndef` | Changed | accept `and` and `or` between token names <!--s 219--> |
| `inmat()` | Changed | after `matches` or `matchfield()` it is the number of the pattern that matched; after `matbuild` and `matwrite` it is the element count; a collection array is accepted <!--s 315 454 591--> |
| `input ... fill` | Added | shows a fill character in every empty cell of the field <!--s 389--> |
| `input ... no.echo` | Added | shows nothing as the user types <!--s 168 363--> |
| `input ... raw` | Added | reads exactly the number of characters given, as they arrive <!--s 548--> |
| `inputif` | Added | reads a line only if one is already there, else takes `else` <!--s 584--> |
| `inputnull`, `inputtrap` | Added | a single character typed alone makes the answer null, or sends the program to a label <!--s 408--> |
| `last()` and more | Added | `last()`, `lasts()`, `nv()`, `ns()`: the final element of a delimited string; value and subvalue position numbers (`left()` and `right()` were added and removed again, see REMOVED) <!--s g171 g162--> |
| `locate ... by` | Added | `c` forces a case-sensitive search and `n` a case-insensitive one <!--s 419--> |
| `matchess` and `trimws` | Added | `matchess`, `matchfields`, `trimws`, `trimw()`: `matches`, `matchfield` and `trimw` over a dynamic array; `trimw` trims white space <!--s 302 g152 g153 g189--> |
| matrix arguments | Changed | a matrix passed as an argument needs no `dim` in the receiving subroutine; `if mat a = mat b` compares two matrices; the compiler no longer reports an undimensioned argument <!--s 44 111 519--> |
| `matstr()` | Added | converts a two dimensional matrix to a dynamic array <!--s 509--> |
| `matwritecsv` | Added | one CSV line of every element of a matrix <!--s g154--> |
| `digest()` | Added | the md5, sha1, sha256, sha384 or sha512 digest of a string or a file (`md5()` was added and removed again, see REMOVED) <!--s 63 g118--> |
| `mergelist()` | Added | merges two lists by a mode; a mode for lists not in order; fixed for an empty list <!--s 420 539 566 g155--> |
| `$mode debug.equates` | Added | keeps `equate` and `$define` tokens in the object so the debugger can show, set and watch them <!--s g218 246 239--> |
| `$mode explicit` | Added | a variable must be named in a `dim` statement before it is used <!--s g220 234--> |
| `$mode` lists | Changed | `$mode` takes several names separated by commas, each with an optional minus <!--s 105--> |
| `$mode non.durable.txn` | Added | a committed nested transaction writes nothing until the outer one commits <!--s g221 442--> |
| `$mode partial.expressions` | Added | `a and b` and `a or b` stop evaluating as soon as the value is known <!--s 417--> |
| `$mode strict.equate` | Added | warns when a name given to `equate` or `$define` is also a statement or function name <!--s 582--> |
| `$mode trap.unused.main` | Added | `trap.unused` for the program's own variables <!--s g227--> |
| `no.query` on cataloguing | Added | the `basic` command, the `$catalogue` directive and the `catalogue` line of `$basic.options` take `no.query`, which stops the compiler asking before it removes an older entry <!--s 27 191--> |
| `open ... non.transactional` | Added | a write through that file variable is not undone by a rollback <!--s 64--> |
| `open.socket()` | Changed | takes a connect timeout <!--s 174--> |
| `openseq` | Added | `creating` makes the file at once; `shared` lets several processes append; a block device can be opened <!--s 485 397 112--> |
| `openseq creating` | Changed | makes a name that is free exclusively: a name taken in the meantime, or a link that leads nowhere, is refused with `status()` 6032 and nothing is made (`shared` refuses a link that leads nowhere the same way, and otherwise still opens or creates); the `openseq file, record` form does the same, and an `openseq` of such a link without `creating` gives a file that cannot be written |
| `opentemp` | Added | makes a temporary dynamic file that is deleted when its variable is closed; in the temporary directory when no path is given <!--s 431 440--> |
| operating system files | Added | `oscopy`, `osread`, `oswrite`, `osdelete`, `!oscopy`, `!ioscopy`: copy, read, write and delete operating system files by name, held to the account's OS gate <!--s 369 517 g163 g164 g165--> |
| `option()` | Added | reads and sets the state of an option <!--s 224 473--> |
| `ospath()` | Added | keys `os$fullpathx`, `os$info`, `os$parent`, `os$uid`, `os$gid`, `os$modes`, `os$is.file` and `os$is.dir` <!--s 293 432 233--> |
| `parse()` and `ttyget()` | Added | `parse()`, `sort.compare()`, `ttyget()`, `ttyset`: split by a pattern; compare by a sort rule; the terminal modes as an array <!--s g166 g183 g187 g190 g191--> |
| `phantom` statement | Added | starts a phantom from a program; the log name may be a variable <!--s 390 351--> |
| `precision inherit` | Added | takes the precision of the calling program <!--s 201--> |
| `@pstat` | Added | text a program leaves for `pstat` to show <!--s 492--> |
| `quotes()` family | Added | `quotes()`, `squotes()`: enclose every element of a dynamic array in quotes <!--s 11--> |
| `read` etc. as a condition | Added | `read`, `readnext`, `open` and the like may be the condition of `while` or `until` <!--s 206--> |
| `recordlocku` | Changed | fixed: it did not always trap an illegal record id <!--s 528--> |
| `redim` | Added | resizes a matrix passed to a subroutine as an argument <!--s 215--> |
| `regex()` | Added | regular expression matching <!--s 510--> |
| `seek` | Changed | fixed: a negative offset from the end of a sequential file was refused <!--s 259--> |
| select list variables | Added | `formlistv`, `getlistv`, `writelist`, `movelist`, `movelistv`: select list variables and numbered lists <!--s 291 g134 g135 g195 g156--> |
| `select.socket()` | Added | waits on the sockets held in a matrix <!--s 161 g176--> |
| `selectindexv` family | Added | `selectindexv`, `selectleftv`, `selectrightv`: index scans into a select list variable <!--s g177--> |
| `send` | Added | `writeseq`, or with a colon `writeblk`, to a file opened with `openseq` <!--s g178--> |
| `set.socket.mode` trace | Added | `skt$info.trace` logs the data sent and received on a socket to an owner-only file <!--s 162--> |
| `socket.info()` | Changed | fixed: `skt$info.open` on a number, a string or an unassigned variable stopped with a fatal error <!--s 249--> |
| `!sort` | Changed | sorts a select list variable; the internal sort is open to programs <!--s 274 371--> |
| `sselectv`, `sselectn` | Added | sorted selects into a select list variable; `right.aligned` and `descending` <!--s 209 243 367--> |
| `status()` after a transaction | Added | 0 if it committed, 1021 if it rolled back <!--s 19--> |
| string arithmetic | Added | `sadd`, `ssub`, `smul`, `sdiv`, `scmp`: exact string arithmetic on numbers of any length and any decimals <!--s 391 468--> |
| substring assignment | Added | `s[3] = "xy"` overwrites the last three characters <!--s 41 325--> |
| `trans()` family | Changed | `trans()`, `rtrans()`: accept `a`, `s` and `c` items and an `l` link; a file that will not open takes the error action of the call <!--s 43 182 7--> |
| variable names | Changed | a name with two or more underscores together (`a__b`) is valid <!--s 336--> |
| `watch` | Changed | the debugger's `watch variable operator value` stops only when the condition is met <!--s 45--> |

## DATA

Data collections, JSON, XML, CSV and the verbs that import them.

| Name | Change | What |
|---|---|---|
| `!ced()` | Added | full-screen editor for a collection held in a variable (the editor is also reached from `ide` F12; there is no `ced` command) |
| collection arrays | Added | `mat()`, `c{list, n}`, `ins ... as`, `del`, `inmat()` on an array |
| collection file verbs | Added | `ed`, `copy`, `compare.files`: work on a collection file; the post-write trigger no longer crashes the process |
| collection files | Added | `create.file name collection`; records are collections stored as JSON; `read` and `write` them whole; `ct` shows JSON <!--s 304--> |
| `collection()` and `c{name}` | Added | a collection is a set of named values read and written by name; `enumerate()`, `element.exists()` <!--s 311 518 529 339--> |
| `csv.mode` | Added | how `printcsv`, `writecsv` and `formcsv()` quote, with a delimiter, quote and escape character <!--s 173 200--> |
| `csvdq()`, `dparse.csv` | Changed | `csvdq()` takes a quote and an escape character as a third and a fourth argument; fixed: a return code was corrupted when used with `execute ... returning` <!--s 526--> |
| `element` keyword in queries | Added | names an element of a collection file by its path, in a display list, `with`, `by`, `sum` and the like |
| `expand()` and links | Added | a link `"file:id"` is followed; `trans()` of an `e` item |
| file variable in a collection | Changed | a collection holding a file variable is written to a collection file as a null |
| `hu` conversion | Added | `oconv` and `iconv` escape and unescape |
| `indices` on `e` items | Added | a data collection element can be indexed; a query with `with` on it uses the index |
| `jboolean()` and `jtype()` | Added | `jboolean()`, `jnull()`, `jtype()`: true, false and null in collections, and the type of a value; a Boolean type <!--s 312--> |
| `jbuild()` | Changed | the pretty-print mode names an indent of up to 16 spaces or tabs; marks in a string are written as hex Unicode <!--s 453--> |
| `jparse()`, `jbuild()` | Added | JSON text into a collection and back |
| operators on an element | Added | `+=`, `-=`, `*=`, `/=`, `:=` change an element in place |
| the debugger and collections | Added | `/c`, `/c{path}` and `dump c{sub} pathname` show and write a collection; diving in with `/*` no longer crashes <!--s 530--> |
| `xml` keyword for queries | Added | `list ... xml` writes the report as XML, with an optional DTD or schema <!--s g211 g202--> |

## FILES

File handling: opening, indexes, triggers, print files, sorting, sequential files.

| Name | Change | What |
|---|---|---|
| `analyse.file` | Changed | `statistics` shows a histogram of group utilisation <!--s 360--> |
| `analyse.index` | Added | every index with its number of values and spread <!--s g9--> |
| `catalog -name` | Added | a hyphen is a global catalogue prefix; `delete.catalog -name` removes it <!--s 217--> |
| `clear.file` | Changed | fixed: a `no.resize` file keeps its modulus <!--s 590--> |
| `configure.file ... reporting` | Added | shows how many records have been converted <!--s 172--> |
| `create.file` | Added | `comment`, `multifile` and a relative `pathname` kept relative in the VOC <!--s 383 522 278--> |
| `create.index` | Added | `no.case`: keys that differ only in case are one key; `deleting` replaces an index; a default location in `$index.path` <!--s 54 424 184--> |
| `dir_dict` | Added | three items for a directory file's dictionary: `days`, `dtm` and `owner` <!--s 181--> |
| directory file line ends | Added | line terminator modes (`l`, `c`, `b`, `x`) and triggers <!--s 177--> |
| `directory files` ids | Changed | the record ids may hold bytes 128 to 247 <!--s 34--> |
| `disable.index` | Added | stops an index being kept up to date for a large load; `build.index` switches it on <!--s g28--> |
| exclusive access | Changed | a command that needs a file to itself names the user holding it when it cannot get it <!--s 107--> |
| `file.stat` | Added | one line per file: type, modulus, records, bytes and flags; limited to named files; with dictionaries <!--s 109 152 g40--> |
| `find.file`, `find.program` | Added | what a file is; the catalogue entries of a program <!--s g42 g43--> |
| `fixdir` | Added | takes the carriage returns out of directory file items that came from a Windows system <!--s 458--> |
| hashed files | Changed | a split that finds the disk nearly full stops before the file's size is changed; `sdfix -z` clears dead space <!--s 329 33--> |
| `hold.file.logger` | Added | a catalogued subroutine called when a hold file print unit opens and closes <!--s 56--> |
| `l-type` dictionary links | Added | usable in an `i`-type; links may follow links, up to ten, and reach `a`, `s` and `e` items <!--s 7 204 544--> |
| `list.common detail` | Added | shows where each common block was created <!--s 362--> |
| `list.index` | Changed | the report may go to a printer <!--s 73--> |
| `list.triggers` | Added | every trigger subroutine used by the files of an account, multifiles, dictionaries and directory files included <!--s 74 187 321--> |
| `listf`, `listfl`, `listfr` | Changed | list a multifile line by line, and take `with` and `without trigger`, `encryption` and `replication` <!--s 3 185--> |
| print unit mode 3 | Changed | takes an update lock on the `$hold` item while it is written <!--s 53--> |
| `rebuild.all.indices` | Added | rebuilds the indices of every file in the account <!--s 58--> |
| `select` of a directory file | Changed | fixed: at the open-file limit it closes the oldest cached file and goes on <!--s 279--> |
| `set.file` | Changed | the target may be a `q`-pointer; a `q`-pointer with no file name points at the VOC <!--s 32 435--> |
| `set.mode` | Added | the permission bits of records of a directory file <!--s g81--> |
| `set.trigger` | Changed | fixed: refused every function name; takes `all`; no longer needs exclusive access <!--s 388 157--> |
| sort of long records | Changed | the disk sort handles records and keys over 32 KB <!--s 455--> |
| trigger on a read | Changed | fixed: a locally catalogued read trigger could end the process <!--s 317--> |
| `vocname` letters | Added | `r` opens a file read-only, `n` non-transactionally, `s` with forced writes, from field 6 of its VOC entry <!--s 197 380 102--> |

## QUERY

The query processor and the dictionary.

| Name | Change | What |
|---|---|---|
| `a;nocase` correlative | Added | makes the string operations of one correlative case insensitive <!--s 103--> |
| `absent.ignore` | Added | do not print the `not found` list for ids that are not in the file <!--s 25--> |
| `break.on "'n'"` | Added | starts a new page and numbers it 1 again <!--s 16--> |
| `by.exp` | Changed | more than one `by.exp` in the same association is sorted <!--s 572--> |
| `csv ... as file id` | Added | writes the report as a record of a directory file; a multivalued field is split over lines <!--s 159--> |
| `csv 3` | Added | every item quoted, numbers too <!--s 26--> |
| dictionary expressions | Changed | divide by zero is zero (an `if` with a part missing, a format after a value and hyphens in names were added and removed again, see REMOVED) <!--s 36 48 270 271 423 547 564--> |
| `for`, `from none` | Added | `search file for "text"`; `from none` ignores an active list 0 <!--s 190 378--> |
| `if` in a dictionary item | Added | field 8 of an `a` or `s` item may hold an `if` expression <!--s 104--> |
| `in`, `not.in` | Added | test a value against a saved list or a file record <!--s 94--> |
| `median`, `mode`, `range` | Added | figures at the end of a report and each breakpoint <!--s 231 g209--> |
| `$mode` in an `i`-type | Added | an `i`-type may begin with `$mode` for a few of the compiler modes <!--s 489--> |
| `no.page` | Changed | accepted on any query command <!--s 379--> |
| options | Added | (`query.sort.no.case`, `clear.select`, `query.string.comp`, `query.str.comp.all` and `default.mv` were added and removed again, see REMOVED) <!--s 140 299 412 205 403--> |
| `$query.defaults` | Changed | field 3 holds default words for `select`, `sselect` and `search`; field 4 the format of the id column <!--s 122 405--> |
| `reformat ... @record` | Added | appends the whole source record <!--s 546--> |
| `reporting` | Added | `n record(s) examined` for every thousand records <!--s 416--> |
| `rpt` | Added | repeats a single valued field on each line of a report on a multivalued one <!--s g210--> |
| `scan`, `search ... display` | Added | show the lines of a record that hold the strings; `search all` searches the id too; strings may come from a file <!--s 437 447 221 141--> |
| `select file field` | Changed | a field no clause uses is `saving multivalued field` <!--s 39--> |
| `show` | Changed | `b` goes to the bottom; `sort.sup`; a missing record is listed and the command ends <!--s 477 495 524--> |
| `sorted.sample n` | Added | counts the records after the sort <!--s 438--> |
| `vertically` | Changed | `fmt` for the name and data format; `$vlist` sets them for the file; multivalued data and a wrapped line are told apart <!--s 160 579 580--> |
| `when field` | Changed | with no operator keeps the values that are not null <!--s 543 343--> |
| `x` breakpoint control | Added | captures the previous value of a break field in `@bpv` <!--s 232--> |

## SYSTEM

The kernel, `sd.conf`, and the numbered keys.

| Name | Change | What |
|---|---|---|
| `cleanup=n` | Added | seconds between the checks that clear sessions that ended without logging out <!--s 98 g283--> |
| `config` | Changed | lists the new settings; `config()` reads them |
| `deadlock=2` | Added | saves the lock tables when a deadlock is found <!--s 500--> |
| `fileinfo()` | Added | the keys 1022 to 1040 as the openQM manual numbers them; `fl$seqtype`, `fl$locks`; 1021 now answers the user numbers <!--s 62 113 498 337--> |
| `intprec` | Changed | default 11 <!--s 6--> |
| lock table | Changed | the time each lock was taken and each wait began is noted; more than 65,535 locks in a file work; a program that filled the table can be logged out <!--s 487 344 532--> |
| `numlocks` | Changed | range checked, 1 to 32767 |
| `phantoms=u,n` | Added | keeps user numbers for phantoms started with `user` <!--s 31 g296--> |
| process dump | Changed | shows the length of each string, the variables of objects and the environment <!--s 22 125 569 439--> |
| `pterm` keys | Added | `pterm erase`, `ctrl.filter`, `mark`: which key erases; control characters filtered; control keys that type the marks <!--s 155 253 254--> |
| `-quiet` | Changed | `sd -quiet` suppresses the VOC update question <!--s 533--> |
| `sd.conf` parameters | Added | `dhcache`, `lgnwait`, `maxrlock`, `pwdelay`, `userpool`: `sd.conf` parameters, each optional with the old fixed number as the default <!--s 90 46 313 106 551--> |
| `sortmem` | Changed | default 4096 <!--s 535-->|
| `status` | Changed | file times are in the user's time zone; field 27 is the file pathname <!--s 96 585--> |
| `-status` | Added | `sd -status` shows the version, start time and process counts <!--s 511--> |
| `system()` keys | Added | 14, 19, 20, 21, 33, 35, 45, 1016, 1036, 1037, 1040, 1045, 1047, 1048, 1049, 1051, 1062, 1065, 1067, 1071, 1073, 1083, 1086, 1088 <!--s 65 66 114 192 225 244 206 294 307 308 326 421 433 586 587 g252 g253 g254 g255 g256 g260 g261 g265 g266 g267 g270 g271 g274 g276--> |
| terminfo | Changed | `eblink`, `eprot`, `edim`, `erev`, `ebold` capabilities; `xmc#1` in the two ADDS 4000 entries <!--s 47 545--> |
| the call name | Changed | can be as long as 128 characters (the lower of 128 and `maxidlen`) <!--s 241-->|
| the startup process | Changed | its `@tty` is `startup` <!--s 91--> |
| time zone and `epoch()` | Added | `epoch()`, `mvdate()`, `mvtime()`, `mvdate.time()`, `mvepoch()`; `set.timezone` and `config timezone` <!--s 69 124 g126 g157 g158 g159 g160 g181 g310--> |
| `usplit=1` | Added | interactive users take the lowest user number, phantoms and API sessions the highest <!--s g312--> |

## TCL

Commands and VOC verbs that every account has, and the command language.

| Name | Change | What |
|---|---|---|
| `autologout` | Changed | works in the full-screen programs (the screen library, `ide`, the home screen, the tool pages): idle time is counted across their short timed waits, and only a typed key (or the break key) starts the period again; a program that polls with very short timed `keyin`s and works between them counts as waiting |
| `block.print`, `block.term` | Added | print text, or show it on the terminal, in letters seven rows high <!--s g11 g12--> |
| `catalog ... local relative` | Added | stores the object file's path relative to the account <!--s 131--> |
| `catalog` overwrite | Changed | pointing a local catalogue entry at a different object file asks first <!--s 490--> |
| `catalog` prefix | Added | a prefix separate from the call name; `$private.catalog` or `$private.catalogue` <!--s 210 93--> |
| catalogue name as a command | Changed | a program run by its catalogue name takes `lptr`, `no.page` and the like <!--s 146--> |
| command stack | Changed | `.c-` undoes a `.0`; the stack is kept in the account the user entered <!--s 296 396--> |
| `command.logging` | Added | a log of every command this session runs, in the account directory, mode 0600 <!--s 444 g16--> |
| `como` | Added | `append`, `in file`; `$como` ids pass the same name transform <!--s 8 361 9--> |
| `compare.files` | Added | counts the records only in one, only in the other, in both but different <!--s 534--> |
| `ct` | Changed | `id.sup`, `num.sup`; lower case file names; the object code of a compiled dictionary item is not shown <!--s 242 347 373--> |
| `decatalog` | Added | deletes a local catalogue entry and its object code <!--s 576--> |
| `delete` | Changed | a record another user holds locked is reported and skipped <!--s 50--> |
| `delete.account` | Changed | not stopped by a file it cannot open when it looks for references <!--s 348--> |
| `delete.common all except` | Added | deletes every named common block but those listed <!--s 425--> |
| `ed` | Changed | `l` with no text as the first command works; marks typed in input; `ev` on a compound `i`-type; line numbers show positions in edit values mode; `spool` closes the printer; external commands; automatic ids <!--s 264 268 320 331 375 446 523 305--> |
| `fstat` | Changed | wider columns <!--s 55--> |
| `fstat.user` | Added | file activity of each session <!--s g44--> |
| `git` option | Added | a directory file keeps `.gitignore` and `.gitattributes` under their own names <!--s g238--> |
| `hot spot monitor` | Changed | counts opens, reads, writes and deletes of each program <!--s 491--> |
| `if` in a paragraph | Added | `exists`, `not.exists`, `in` and `not.in`, with `no.case` <!--s 28 230 426 476--> |
| inline prompts | Changed | largely case insensitive; may use quoted prompt strings <!--s 171 377--> |
| `k` entry in the VOC | Changed | fixed: a `k` entry over a locally catalogued program stopped with "Unable to load" <!--s 263--> |
| list merges | Changed | `merge.list` finds a key without scanning, so large lists merge in seconds <!--s 414--> |
| `list.item` | Changed | numbers lines beyond 999 with as many digits as needed <!--s 349--> |
| `list.readu`, `pstat`, `getlocks()`, `system(1083)` | Changed | another session's text (a lock's record id, file path or user name, a command, a program name, `@pstat`) shows a control character, `del`, bytes 128-159 and a mark character as `?` and cannot send a code to your terminal; the locks and `fileinfo(f, 1039)` are unchanged |
| `listu`, `who`, `pstat` | Changed | `!listu` too: show the account and the login name; `listu detail`; the blocking user and when a wait began <!--s 12 24 29 38 77 121 289 427 577--> |
| `logto reset all` | Added | discards all programs, menus and paragraphs at every command level <!--s 30--> |
| `map local`, `map no.page` | Added | list the locally catalogued programs; heading once <!--s 153 287--> |
| `move.list` | Added | the command form of `movelist` <!--s g62--> |
| `multisort` | Added | `!multisort` sorts several related lists by one of them <!--s 568--> |
| `option` words | Added | `dir.dtm`, `git`, `inherit.ownership` and `spool.command` (twenty more were added and removed again, see REMOVED) <!--s 288 79 314 428 461 445 37 57 154 165 404 429 49 g230 g231 g232 g233 g237 g239 g240 g241 g242 g245 g247 g248--> |
| `oscopy` | Added | copy an operating system file; `overwrite`, `append` <!--s 369 517--> |
| `phantom` | Added | `no.msg`, `data`, `log`, `group` and `user` options; `!phlog` gives a phantom's log record; a phantom started while SD is suspended gives back its place <!--s 87 137 364 483 31 385 280--> |
| phantom and terminal lists | Added | `list.phantoms`, `list.term.types`: the phantoms and no one else; the terminal types <!--s 381 g49--> |
| `private vocabulary` | Added | `$private.voc`: a file of commands searched after all other command sources <!--s 1--> |
| `profiler` | Added | records what the programs of a session do and where <!--s g66 g203-->|
| `redo` | Added | runs a command again and again, `times` and `every` <!--s 188--> |
| saved list verbs | Changed | `save.list`, `get.list`, `delete.list`: `keep`, `deleting`, `count.sup`, a default name, a name left out, `in file` <!--s 2 384 387 401 494--> |
| `selectindex` | Added | the command form of the statement <!--s 119--> |
| `setptr` | Changed | `form.feed`, `inform`, `eject`, `as ... in file`; the digits of `next` <!--s 51 59 70 139 448--> |
| `show.list` | Added | a page at a time, starring and clearing items <!--s 449-->|
| `sort.list`, `select.dir` | Added | sort a saved list; select the files of a directory <!--s 158 465--> |
| `sp.view` | Changed | `by field`; `x` deletes the item shown; shows where output goes for every print unit mode <!--s 450 560--> |
| `term` | Changed | takes two numbers for the default printer; `term default` goes to 140 by 42 <!--s 466--> |

## TOOLS

The debugger and the editors, from the openQM list. The full-screen tools that are SD's own are under New Features Unique to SD Core.

| Name | Change | What |
|---|---|---|
| `debugger` | Changed | full-screen display on a terminal with an alternate screen; `/*` for every variable; `^`; `window n`; `set v = token`; a stop before each `case`; a blank line repeats the last command; `brk` lists the breakpoints <!--s 21 67 97 142 193 203 327 335 513 550--> |
| `debugger` phantom | Changed | an `@variable` is read from the process being debugged <!--s 251-->|
| `sed` | Changed | the full-screen editor takes `creating.seqkey` in place of a record id, like `ed` <!--s 446-->|
| `sed` option `no.case.explore` | Added | in `&sed.options&`: the list of records is in order whatever the case of the ids, not capitals first <!--s 376-->|
| `sed` option `scroll1` | Added | in `&sed.options&`: page up and page down move one line less than a page, so one line of the old page stays <!--s 463-->|
| `sed` split point | Added | Window > Move split up / Move split down, and the commands `split.up` and `split.down` with a number of rows, move the line between the two windows <!--s 578-->|
| `sed` view | Added | Search > View lines, or `view` and a text: a new read-only buffer holding only the lines of this one that contain the text <!--s 138-->|


## REMOVED

These were in L1.1-3 - or were added and taken out again during L1.2-0 - and **SD no longer has them**. Since 27 October 2026
this is the one place where a removal is listed (the owner's instruction), whatever the area it belonged to. Most were removed
on his instruction of that day because they existed only to make SD behave like another MultiValue product, or gave a second
way to do something SD already does one way. **A program, a login paragraph or a `$basic.options` record that uses one has to
be edited**; the last column says what to write instead. A program that was compiled with a removed mode keeps what it was
compiled with until it is compiled again. More rows are added as the removal goes on.

| Name | Change | What |
|---|---|---|
| AccuTerm terminal types | Removed | the eleven `-at` terminal types and AccuTerm's escape sequences |
| `$mode` words that imitated other products | Removed | `prclose.default.0` (write `printer close on` *unit*), `unassigned.common` (a common variable starts as zero), `no.case.invert` (give `input` the `nocaseinvert` clause) and `optional.then.else` (a `read` takes a `then` or an `else`) are refused now with *Unrecognised mode name*; `conditional.statements`, `implied.stop` (end a program with `stop`) and `exception.save.stack` (write `saving.stack` on the `catch`) were added and removed within 1.2-0, so they never shipped <!--s 206 434 81 355--> |
| `option` words that imitated other products | Removed | `option pick` and 22 words, refused now with *Option name not recognised*: `assoc.unassoc.mv`, `pick.breakpoint`, `pick.breakpoint.u`, `pick.explode`, `pick.grand.total`, `pick.implied.eq`, `pick.null`, `pick.wildcard`, `qualified.display`, `with.implies.or`, `query.no.case`, `query.priority.and`, `ampm.upcase`, `crdb.upcase`, `no.date.wrapping`, `space.mct`, `lock.beep`, `ed.no.query.fd`, `create.file.upcase`, `select.keep.case`, `debug.rebind.keys`, `proc.a`. SD does what it did with them off: write `with city = "Reno"`, use `like` for wildcards, brackets and `or` for the order of tests, `no.case` after an operator or `option query.sort.no.case` for case; times and amounts are `am`, `pm`, `cr`, `db`; a date such as 31 February rolls into the next month; a lock wait is silent; `fd` in `ed` asks first; `create.file` names a file in lower case <!--s 60 322--> |
| screen save and restore | Removed | `save.screen()` and `restore.screen`: still exist and do nothing the terminal could see |
| `sdterm` terminal type | Removed | with SDTerm and SDConsole, and the `term display` line about them |
| `term 120,36` at login | Removed | `login` no longer sends it |
| second names for statements | Removed | `$insert` (write `$include`), `include` without the `$` (write `$include`), `com` (write `common`), `dimension` and `redimension` (write `dim` and `redim`), `enter` with `$mode pick.enter` (write `call`, or `chain` to hand control on for good), `perform` (write `execute`), `printerr` (write `inputerr`), `remark` (write `rem`), `rqm` (write `sleep`), `sub` (write `subroutine`, also after `local`, `private` and `public`) and `tclread` (read `@sentence`): the compiler refuses each <!--s 215--> |
| second forms of statement clauses | Removed | `execute ... setting` (write `returning`), `execute ... passlist` with no variable (it did nothing: name the variable, or leave the clause out), `input ... for` and `input ... timeout` (write `waiting`), `opentemp ... ecs` (a word that was read and ignored: it is an ordinary name now, so the compiler warns that it is never assigned a value) and the bracketed Pick form `locate(expr, array, f, v; position; order)` (write `locate expr in array<f, v> setting position`) |
| second names for functions and variables | Removed | `ereplace()` (write `change()`, which takes -1 for every occurrence), `sentence()` (read `@sentence`), `swapmarks()` (it returned its argument), `terminfo.ex()` (write `terminfo()`) and `@system.set` (write `@system.return.code`) <!--s 238 472 g186--> |
| `mcd`, `mcdx`, `mcx` and `mcxd` conversions | Removed | second spellings of `mx`: an invalid conversion code now, STATUS 2 |
| second spellings of query keywords | Removed | `col.spcs` (write `col.spaces`), `display.name` (`col.hdg`), `evaluate` (`eval`), `calculate` (`calc`), `intersection` and `difference` (`intersect` and `diff`, also in `merge.list`), `margin` (`left.margin`), `stats` (`statistics`), `supp` (`hdr.sup`) and `only` (`id.only`): **a new account does not have their VOC records**, and the next `update.accounts` removes them from existing accounts, through the deletion list (saved copy first; a record of your own with the same name is kept; `restore.voc` puts one back) |
| `only` and `id.only` before the file name | Removed | `list only customers` is refused: write `list customers id.only` |
| `=>`, `=<` and `><` | Removed | the mirrored spellings of `>=`, `<=` and `<>`; as for the keyword synonyms, a new account has no record for them and an old account keeps its own |
| eleven `option` words | Removed | `run.no.page` and `paginate.on.heading` (a run is paginated unless `run ... no.page` says not), `pick.ml.conv.mask` (a left bracket in `ml` / `mr` is the round-bracket negative style), `chained.select` (a select does not run the data queue), `default.mv` (a blank S/M flag is single valued), `query.string.comp` and `query.str.comp.all` (`=` and `ne` compare as BASIC does), `assoc.all` (the dictionary's associations are used), `query.footer.pause` (no pause after a page footer), `query.merge.print` (a report closes printer 0) and `keep.old.object` (a failed compile leaves no object code). Each behaves as it did with the option off; their numbers stay reserved |
| `dquote()`, `dquotes()`, `swap()`, `xlate()` | Removed | second names of `quote()`, `quotes()`, `change()` and `trans()`: write those |
| `caption`, `nopage`, `col.hdr.space` | Removed | `caption` and `nopage` were second names of `grand.total` and `no.page`; `col.hdr.space` (a blank line under the column headings) was added and taken out again: end a heading with a blank line <!--s 467--> |
| `listdict`, `edit.list` | Removed | write `list dict` *file*, and `ed $savedlists` *name* <!--s 10 75--> |
| loose forms of a dictionary expression | Removed | an `if` with no `then` or no `else` is refused again (messages 2950 and 2951), a hyphenated item name such as `cust-no` is read as a subtraction, and a format string straight after a value needs its operator <!--s 36 423 564--> |
| `$mode execute.clearlist`, `open.fail.zero.fvar`, `pick.readnext` | Removed | added and taken out again in this release: the default select list is not cleared before an `execute` (use `clearselect 0`), the file variable of a failed `open` stays unassigned, and a `readnext` that takes its `else` sets the id variable to the null string. Their mode bits stay reserved <!--s 521 514 418--> |
| three more `option` words | Removed | `chain.keep.common` (`chain` always discards the unnamed common), `backslash.not.quote` (a backslash always opens a quoted string in a command line) and `correlative.reuse` (a shorter array's missing values count as zero unless an operand says `reuse()`) |
| `inputclear` | Removed | write `clearinput`; the file type constant `FL$TYPE.SH` (a static hashed file SD never had) is gone too |
| `@am`, `@svm`, `@user`, `@user.no`, `@filename` | Removed | second names of variables that stay: write `@fm`, `@sm`, `@logname`, `@userno` and `@file.name` (a dictionary item of your own that says `@filename` stops compiling until changed) |
| `go`, `go to`, and `#` before a compiler directive | Removed | write `goto` (also in `on ... goto`) and `$ifdef`, `$define`, `$include` |
| second spellings of query words | Removed | `avg`, `enum`, `vert`, `percent`, `pct`, `%`, `header`, `footer`, `first`, `#` and `&`: write `average`, `enumerate`, `vertically`, `percentage`, `heading`, `footing`, `sample`, `ne` and `and`; a `break.on` control `l` is no longer ignored when `u` is given too; and a name that is `f` and a number is a field only if the dictionary has an item of that name <!--s 40 547--> |
| terminal case inversion | Removed | `pterm case invert` / `noinvert` (and the line in `pterm display`), `input ... nocaseinvert`, the `invcase` setting of `sd.conf` (a kept `sd.conf` is cleaned by the installer), `system(1001)`, `pterm(PT$INVERT)` and the `no.invert` option of `sed`; `keyinc()` is now the same as `keyin()`, and field 2 of `ttyget()` is always 0. Type in the case you want <!--s 399--> |
| `nano` | Removed | the second external editor, with its syntax file and the page about it (the shared parts moved to the `micro` page): write `micro`, `sed` or `ed` |
| `set.queue`, `sp.assign`, `getpu(pu$form.queue)`, `system(1066)` | Removed | Pick style form queues were added and taken out again in this release: use `setptr` with the settings you want <!--s g83 g88 18 189 502--> |
| `copyp`, `copy.listp` | Removed | the Pick-style copy and its saved-list form (`copy.listp` was added and removed again in this release): write `copy` and `copy.list` <!--s 72--> |
| `make.index` | Removed | write `create.index` and then `build.index` (the `tool.dict` page runs both after one box) |
| `list.union`, `list.inter`, `list.diff` | Removed | the saved-list twins of `merge.list`: `get.list` the two lists and `merge.list 1 union 2 to 3` (or `intersect`, `diff`) |
| `cd` | Removed | the short name of `compile.dict`: write `compile.dict` |
| `md` | Removed | the Pick name for the VOC (a Q-pointer to `voc`): write `voc` |
| `create.file ... no.case` and `... case` | Removed | every file is case insensitive, so neither word means anything; `configure.file ... no.case` stays for converting an old file |
| `catalogue`, `$catalogue`, `no.catalogue` | Removed | the British spellings: write `catalog` (the verb, and the `$basic.options` word), `$catalog` and `no.catalog` |
| `bscan`, `root`, `key()` | Removed | added and taken out again in this release: scan an index with `selectindex`, `selectleft` / `selectright` and `setleft` / `setright` <!--s g110 g173--> |
| `call "file name"` | Removed | the Pick style call was added and taken out again in this release: catalogue the program and call it by name <!--s 208--> |
| `is.alnum()`, `is.alpha()`, `is.digit()`, `is.graph()`, `is.mark()`, `is.space()`, `left()`, `right()`, `md5()` | Removed | added and taken out again in this release: use `alpha()`, `num()` and `matches` for the character tests, `s[1, n]` and `s[n]` for the ends of a string, and `digest(s, 0, 'md5')` <!--s 223 g138 g139 g140 g142 g143 g145 g150 g151 63--> |
| `adds()`, `subs()`, `muls()`, `divs()` | Removed | added and taken out again in this release: the operators `+ - * /` work element by element on dynamic arrays <!--s 207--> |
| four more `option` words | Removed | `no.sel.list.query` (`no.query` alone skips the question *Use active select list?*), `catalogue.local` (`catalog` and `delete.catalog` with no word work on the private catalogue; say `local`), `inherit.mfile.path` (a new multifile subfile goes in the directory named for the file unless `pathname` says otherwise) and `correlative.nocase` (a correlative is case blind through its own `A;NOCASE;` flag or an I-type's `$mode nocase.strings`) |
| `analyse.file` | Removed | the British spelling: write `analyze.file` (the American one stays) |
| `cleardata`, `clearinput`, `clearprompts`, `clearselect` | Removed | the run-together second names of `clear.data`, `clear.input`, `clear.prompts` and `clear.select` (the BASIC statements of the same names are not affected) |
| `cs` | Removed | second name of `clr`: write `clr` |
| `delete.catalogue` | Removed | the British spelling: write `delete.catalog` |
| a hyphen for a dot in a verb name | Removed | `clear-select` is not found: write `clear.select` |
| `rename` | Removed | second name of `cname`: write `cname`. (`cname` still takes the comma form, `cname old, new`.) |
| `sp.open` and `sp.close` | Removed | write `printer keep.open` and `printer close` |
| `sd -l` | Removed | "apply new licence": SD has no licence, and it set a flag nothing read; `sd -l` is an unrecognised option now |
| terminal types of old hardware | Removed | the Data General, MDC Prism, Prime and Televideo 910 definitions: `dg210 dg-ansi dg-generic dg6053-old dg100 prism2 prism4 prism5 prism7 prism8 prism9 prism12 prism14 p4 p5 p7 p8 p9 p12 p14 pt100 pt200 wren fenix pt100w pt200w wrenw fenixw pt250 pt250w tvi910` (31 of the 82 names `list.term.types` showed). Use `ansi`, `vt100` or `xterm` |
| `system:account:file` file names | Removed | bit 2 of `FILERULE` and a Q-pointer's fourth field named a file on another system and opened nothing; the name form is gone and a Q-pointer with a fourth field is refused (3003) |
| eleven `sd.conf` settings, `sd -<n>`, and the `gdi` and `raw` words of `setptr` | Removed | `apilogin`, `codepage`, `creatusr`, `exclrem`, `fixusers`, `gdi`, `jnldir`, `jnlmode`, `portmap`, `ringwait` and `txchar` (the first two groups did nothing; `fixusers` and `portmap` gave a connection a fixed user number): a line naming one stops SD from starting, so the installer takes it out of a kept `sd.conf`; `config('...')` no longer answers them and `config` no longer lists them; `tool.config` has no `inert` or `retired` status left; `sd -<n>` (start with a given user number) is gone; `setptr` always uses its raw mode, and its `gdi` and `raw` words are no longer keywords |
| six `option` words and `keep.select` | Removed | `unass.warning`, `div.zero.warning` and `non.numeric.warning` (with the shortcut `sdbasic.warnings`): an unassigned variable, a divide by zero and a non-numeric value are always errors, so test the value first; `inherit`: a phantom starts with every option off; `query.sort.no.case`: a sort is by case (`sp.view ... by field no.case` still ignores it, by sorting the list itself); `clear.select` and the `keep.select` statement: a select list left active is left for the next command, and `clear.select` clears it <!--s 14 140 412 403 g148--> |
| twenty-two `$mode` words | Removed | `string.locate`, `composite.readnext`, `pick.read`, `selectv`, `pick.select`, `stdfil`, `stdfil.shared`, `write.delete.then.else`, `autolock`, `pick.substr`, `pick.substr.assign`, `compatible.append`, `pick.convert`, `count.overlap`, `index.overlap`, `change.no.overlap`, `case.sensitive`, `for.store.before.test`, `pick.jump.range`, `optional.final.end`, `pick.matrix` and `heading.no.eject`: each is refused with *Unrecognised mode name*, and the program does what it did with the mode off (the `keep.select` statement went in the same way with `option clear.select`); write `heading no.eject` for the last, and name the file variable for `stdfil`. `selectv` *file* `to` *var* stays a statement. The programs that used `$mode stdfil` and `$mode selectv` had no replacement; an I-type may no longer say `$mode count.overlap`, `index.overlap`, `change.no.overlap` or `compatible.append` <!--s 17 85 368 496 507 g213 g214 g215 g216 g222 g223 g225-->
| seven more `option` words | Removed | `numeric.exponent` (`123.45E-2` is not numeric), `suppress.abort.msg` (`abort` always says where it ran), `dir.sel.omit.hidden` (a select of a directory file includes dot files), `no.phantom.notify` (a phantom always tells its parent), `force.reload`, `stacked.account` (an `execute` of `logto` stays in the account it went to) and `command.level.locks` (a file variable that goes closes its file and its locks) |
| `$mode time.ms` and `$mode default.unass.args` | Removed | write `system(1020) / 1000` for milliseconds; a default argument value needs `var.args` |
| `closeseq` and `equ` | Removed | write `close` and `equate` |
| `extract()`, `replace()`, `insert()`, `delete()` and `subr()` | Removed | write `a<f,v>`, `a<f,v> = x`, `ins x before a<f,v>`, `del a<f,v>` and `call` or `deffun` |
| `procread`, `procwrite`, `@pib`, `@sib`, `@pob`, `@sob` | Removed | leftovers of PROC, which went earlier |
| `!` (the shell verb) | Removed | write `sh command` |
| the global catalog prefixes `*` and `-` | Removed | `!` and `$` stay, and `_` names a recursive pcode program |
| the word forms of query operators | Removed | `equal`, `greater`, `less`, `before`, `after`, `matches`, `matching`, `not.matching` and `spoken`: write `eq`, `gt`, `lt`, `like`, `unlike` and `said` (the word `not` stays) |
| `colour`, `without`, `no.grand.total` | Removed | write `color`, `with no` and `grand.total "'L'"` |
| fourteen dead query keywords | Removed | `verify`, `verify.sup`, `exclusive`, `creating`, `inquiring`, `portrait`, `odd`, `even`, `mark`, `space`, `no.label`, `no.object`, `static` and `encrypt` were read by nothing; `group` stays |
| `setptr` print mode 5 and the `version` keyword | Removed | the terminal's auxiliary printer port; a file is made in the current format |
| old terminal definitions | Removed | `addsviewpoint`, `viewpoint`, `adds4000`, `viewpoint60`, `vp60`, `vp`, `vpa2`, `vt52`, `hpgeneric`, `hp`, `ibm-pc`, `ibm5051`, `5051`, `glasstty` and `kermit`: use `ansi`, `vt100` or `xterm` (`wyse50` and `wyse60` stay) |
| VOC record type M (menu) | Removed | the home screen is the menu system |
| `FILERULE` | Removed | the sd.conf parameter and the `account:file` and `path:pathname` forms of file name; write a Q-pointer, an F-pointer or `logto` |
| `listf`, `listfl`, `listfr`, `listk`, `listpa`, `listph`, `listq`, `listr`, `lists`, `listv` | Removed | `list voc with type = "F"` (and `and is.remote = ""` / `and is.remote` for local / remote files), `"K"`, `"PA"`, `"PH"`, `"Q"`, `"R"`, `"S"`, `"V"` for the other types; add `ftype desc data.name dict.name` after `voc` for the file columns |
| `sd.voclib` | Removed | nothing: the file held only the ten sentences above, and its VOC pointer is removed from every account |
| C dictionary item type (and the compiler's C-type mode, @ANS return) | Removed | write the calculation as an I-type; it may call a catalogued subroutine with SUBR(); compile.dict says message 11993 for a C item |
| create.file name,part | Removed | create each part as an ordinary file (create.file part) and share the dictionary with create.file part using dict name |
| create.file ... multifile | Removed | create an ordinary file; the word is now an unexpected token |
| delete.file name,part | Removed | delete.file part (each part is an ordinary file); the multifile cancel question (6133) is gone |
| open "name,part" (BASIC) and file,part in TCL verbs | Removed | open the part by its own VOC name; a comma is part of the name, so "a,b" is only found if a VOC record is called a,b |
| VOC field 4 (multifile component list) | Removed | none; the field is ignored and the record is read as an ordinary F-pointer |
| PARSER$MFILE (!parser key 5) | Removed | PARSER$GET.TOKEN |
| error 3031 (component not found) and 3032 (no component name) | Removed | none; the numbers are retired |
| the Pick style matrix in the run-time system | Removed | nothing could make one since `$mode pick.matrix` went; the matrix descriptor type, its opcode (reserved), its flag and their branches in the kernel, the debugger and the process dump are gone, with messages 1136 and 1139, `readnext` mode 0, the wait path of a remote `write`/`delete` under `autolock`, and the option-flags field of a phantom's start-up record and its seal. No program changes |
| dictionary field numbers 9998 and 9999 | Removed | a `d`, `a` or `s` item whose location was 9998 gave the item count and one whose location was 9999 the record length in bytes; they are ordinary field numbers now. Write an I-type with `@ni` or `len(@record)` |

## New Features Unique to SD Core

Everything in this section is SD Core's own. None of it is on the openQM list, so none of it has a row in the
feature spreadsheet: the administrator's pages and gates, the AI features, the master files and the shared
account, SDNet, the screen library and the full-screen tools, the installer's additions, and the fixes to
SD's own code. The sections above are the openQM items that were built, with the changes they made.

### Administration

| Name | Change | What |
|---|---|---|
| `bp-on` and `bp-off` | Added | per-account switch for saving a change to a program file (source or object code) |
| `check.masters` | Added | compares every account's VOC and dictionary records with the master copy SDSYS keeps and reports each difference |
| `check.masters` accounts off | Changed | says once how many accounts have master edits switched off; `nonwritable` and `norights` are said only of accounts that are on; `tool.masters` shows the count |
| `create.account` | Changed | a user account's group is made with `root` and the user; the `sdsys` user is no longer put in it |
| `create.account` audit line | Changed | the audit line ends `gates=` with every access the command granted, or `gates=none` |
| `create.account group` | Changed | fixed: the four record files of a new group account now get the account's own group (they were left in `sdusers`) |
| `create.account` recovery word | Added | `create.account user <name> recovery-on` makes the account's `ide` keep a recovery copy of unsaved text; off as delivered, user accounts only (`recovery-off` is for `modify.account`) |
| `create.account` start and pins words | Changed | takes `start-menu`, `start-terminal` and `pins-on` on any kind of account; a refused word makes nothing; the audit line gains `pins-on` and a `start=` tail |
| `dict-on` and `dict-off` | Added | per-account switch for saving a change to a dictionary |
| `docs.install` | Added | SDSYS puts a directory of PDFs into the shared account's `pdf` directory |
| `files-admin-on` | Added | third remote permission: the login may configure, index, create and delete files on this server (group `sdfilesadmin`) |
| `files-on` and `files-off` | Added | per-account switch for the files route SDNet uses (group `sdfiles`) |
| `files-write-on`, `-off` | Added | per-account switch for changing files over the files route (group `sdfileswrite`); `files-off` removes it first |
| `list.master.pending` | Added | shows the journal lines of master-file changes not yet applied |
| `list.voc.removed` | Added | administrator only: the VOC records SD no longer ships, with the release each went in and what to write instead; given an account, what the next `update.accounts` would do in it (changes nothing) |
| `load.help` | Added | SDSYS loads the text of the `[?]` help buttons into the shared account; keeps records the administrator added |
| `master files` | Added | SDSYS keeps a copy of every account's VOC and dictionary records (`voc_master`, `dict_master`) current by a journal |
| `master files` access | Changed | fixed: they were readable and writable by every SD user; they are owner sdsys, mode 0600 and 0700 |
| `master files` saving | Added | saving an account's master copy writes it into the account at once, or refuses with the reason and changes nothing |
| `master files` saving | Changed | an account whose group does not list `sdsys` (the delivered state) is refused with a message that names `modify.account <name> sdsys-on`; nothing is changed |
| `modify.account` | Changed | takes more than one action in a command (`modify.account fred sh-on os-on voc-on`), all carried out or none |
| `modify.account files-off` | Changed | fixed: deals with a leftover `sdfileswrite` membership instead of making it live at the next `files-on` |
| `modify.account recovery-on` and `recovery-off` | Added | per-account switch for the `ide`'s recovery copy of unsaved text; off as delivered; refused for a group or other account (message 11771) |
| `net-on` and `net-off` | Added | per-account switch for SDNet, off as delivered |
| new account defaults | Changed | a new account has no ssh, no API, no shell and no `os.execute`; SDSYS opens each, account by account |
| `restore.account` | Changed | fixed: no longer overwrites a different global program of the same name; restoring the `shared` account puts it back in the group `sdusers` (it had been given `sdg_shared`, which no ordinary user is in) |
| `restore.voc` | Added | administrator only: puts back the newest saved copy of a VOC record the update removed, or all of an account's; never overwrites a record the account holds, and audits what it puts back |
| `sd-elevate` | Changed | new verb `sdsys-leave`, and `conf-set` (see `set.config`); `sdsys-join`, `sdsys-leave` and `group-write` write a line to the system log |
| `sd-elevate akpath-set` | Changed | takes only a hashed file's directory (a plain `%0` with no second link) and an existing directory, both in one account |
| `sd-elevate chown-account` | Changed | the `sdsys` shape takes only a group account's files, in that account's own group (`sdg_`*name*; `sdusers` for `shared`); the `root` shape takes only a directory or plain file the `sdsys` user owns, and a real run chowns through the open file; a user account's directory, `voc` and record files, `/etc/shadow` and the like are refused |
| `sd-elevate environment` | Changed | fixes its `PATH`, runs its python isolated, and reads its test settings only on `--dry-run` or from a process that is not root |
| `sd-elevate groupadd` | Changed | an `sdu_`*user* group is made only for an SD user that exists, with only `root` and that user in it |
| `sd-elevate restore-place` | Changed | a group account is put back only in its own group, `sdg_`*name* |
| `sd-elevate setpw`, `passwd` and `userdel` | Changed | act only on a user carrying the `SD account` comment, as `userdel-home` always did; `setpw` sets a first password only |
| `sd-on` and `sd-off` | Added | per-account switch: programs may reach files under the directory of any SD account the user could `logto` |
| `sdsys` operating system user | Changed | a member of no user account's group as delivered (a release before 1.2-0 put it in every one); `sdsys-on` puts it in one |
| `sdsys-on` and `sdsys-off` | Added | per-account switch for the `sdsys` user's membership of the account's group (master edits, and SDSYS writing inside the account); off as delivered |
| `set.config` | Added | changes one of 14 tuning parameters of `sd.conf` (administrator, through the root helper): a name on the helper's list and a whole number inside the range SD enforces; the old file is kept as `sd.conf.bak` |
| `set.start.default` | Added | chooses where accounts start: the home screen or the command prompt |
| `set.tile` | Added | switches a home screen tile on or off for an account; `set.tile` alone lists what is off |
| `set.tile` standard ids | Changed | the seven development tiles and `recent` are standard ids (15 in all); the Back tile of a sub-menu cannot be turned off |
| `set.viewer` | Added | allows one PDF reader for the `pdf` verb; none is allowed as delivered |
| `sh` and `os` switches | Added | `sh-on`, `sh-off`, `os-on`, `os-off`: per-account switches for the shell and for `os.execute`, off for a new account |
| `shared` account | Added | a group account whose files every account opens by name, with no `logto` or pointer; made by the installer |
| `shared-read-off` | Added | withdraws the shared account's files from one account (on for every account as delivered) |
| `shared-write-on` | Added | lets one account change the shared account's files (off as delivered) |
| `ssh` and `api` | Changed | a new account gets neither; `create.account user name ssh`, `api` or `both` and `modify.account` change it |
| `sync.masters` | Added | makes the first copy of every account's VOC and dictionary records and repairs a difference |
| `tool.accounts` | Added | full-screen page of every account: its kind, suspension, the gates that are on and who is signed on; suspends or lifts, adds or takes away a person of a group account, creates (the verb asks for a password on the terminal) and deletes (after the name is typed) |
| `tool.audit` | Added | full-screen page that reads the audit trail from its end, a screen at a time: filters by time, event, account, user and text, go to a time, follow, the rotated files, and the lines shown saved to a record; it changes nothing else |
| `tool.backups` | Added | full-screen page for backups and restores: the saved directory, the archives in it with each manifest, who else is signed on (a backup and a restore need everyone else out), and `backup.account`, `restore.account` and `set.backup.directory` behind a box |
| `tool.config` | Added | full-screen page that shows every `sd.conf` parameter with what SD is running with, what the file says, the default and when a change takes effect, and names a line SD does not know; `E` changes one of 14 tuning parameters through `set.config` behind a box answered Run, and shows why and the line to add by hand for the rest |
| `tool.gates` | Added | full-screen matrix of every account against every gate; changes go through `modify.account`, never by themselves; in any other account the same verb is a read-only page of what that session may do |
| `tool.masters` | Added | full-screen page for the master files: set-up state, journal, each account against its copy; runs `sync.masters` |
| `tool.menus` | Added | full-screen page for the home screen: where each account starts, which tiles are on, who may add programs |
| `tool.menus` | Changed | a row for each development tile and the Recent group (17 rows in the Menu box) |
| `tool.remote` | Added | full-screen page for everything that reaches SD from outside: the API and ssh doors as the machine reports them (changed after a box, and the word OPEN to turn one on), the routes of each user account, the SDNet servers (delete, define with the terminal given to `set.server`), who is connected and this machine's TLS identity |
| `tool.sessions` | Added | full-screen page of sessions and locks; logs a session out, releases a lock, stops new logins |
| `update.accounts` deletion list | Changed | after the copy from `newvoc` it removes from the account's VOC the records on SD's deletion list (`sdsys/voc_removed`), but only the record SD shipped (not one of your own, not a `[locked]` one unless it is a verb), after saving a copy, and audits it; before `newvoc.mods` |
| `update.accounts all` by SDSYS | Changed | an account whose VOC SDSYS cannot write (the `sdsys` user is not in its group) is skipped with a line that says so, and the command goes on and ends with the counts, where it stopped with error 3018 at the first one; the administrator's own VOC is updated from `voc_template` |
| `voc-on` and `voc-off` | Added | per-account switch for saving a change to a VOC |

### AI

| Name | Change | What |
|---|---|---|
| `agent-pack` | Added | a guide (examples compiled and run), a generated reference of 3,932 entries and a Claude Code skill, in the source and installed under `/usr/local/sdsys/agent-pack` |
| `ai` gate | Added | per-account switch, `ai-on` and `ai-off` (also on `create.account`); off as delivered |
| `ai` in the editors | Added | the debugger, `sed` and the collection editor: ask about what you are looking at; a preview of everything sent; proposed changes shown as diffs and never saved by the AI |
| `ai` proposal box | Changed | shows every line of a proposed change, command or request in full, not cut at the box edge; a proposed change that would take more than 30 rows to show is not offered |
| `ai` row in the home screen | Added | type what you want, see what will be sent, accept one proposed tile or command |
| `ai` row in the ide | Added | explain an error or a selection, ask about the record, accept or reject proposed edits as a diff |
| `ai` verb | Added | asks an AI one question; shows exactly what will be sent and sends only on `y` or `yes` |
| `sdai` operating system user | Added | system user made by the installer for the AI feature: own group, no shell, no home, no SD group |
| `set.ai` | Added | SDSYS chooses the provider, model and key from the prompt |
| `tool.ai` | Added | SDSYS page: Anthropic, OpenAI, DeepSeek or custom, one provider for every account, each account's gate |

### API and client library

| Name | Change | What |
|---|---|---|
| api request 29 | Changed | fixed: opened any account's file for any login; now asks the `logto` rules, the `net` gate and `sdclient`, and the OS question for a pointer out of the account |
| api requests 32 and 33 | Changed | fixed: file lock and unlock acted on the last file opened, not the file named |
| api server loop | Changed | fixed: a client that hung up before its first request left a server process using 100% of a processor |
| api server, last reply | Changed | fixed: a refused login (any reply sd sends as it ends) could be lost when systemd killed the TLS relay as sd exited; sd now waits up to two seconds for the relay to deliver it |
| client library: restricted | Changed | fixed two faults under `sdclient 1` and `2`: a heap overrun on a refusal, and a refused call that still ran |
| client library: `sdchecksum` | Added | a checksum computed on the client |
| `creating.seqkey` over the API | Added | the server's record-id counter gives the id, over the API |
| `sdfiles` route | Added | a second, narrower API login that reaches files and nothing else (Linux group `sdfiles`); `sdapi` still wins |
| `sdfilesadmin` group | Added | the files route may also configure, index, create and delete files |
| `sdfileswrite` group | Added | a files-only login is read-only on that server unless it is also in this group |

### Commands

| Name | Change | What |
|---|---|---|
| `menu` | Added | opens the full-screen menu (the home screen) from any account; `home` and `exit` stay |
| `pdf` | Added | shows a document in the PDF reader the administrator has allowed, even for an account that may not run programs |
| `tool.bulk` | Added | full-screen bulk update of one data file: records chosen by conditions, a saved list or all, up to ten operations, a dry run first, apply under record locks after a box that asks the file's name typed, and undo of the last run; for every account |
| `tool.catalog` | Added | full-screen list of the account's program records (kind, compile time, size, current or stale, private / local / global catalogue) with compile (basic), catalogue privately or locally (catalog) and take an entry out (delete.catalog, decatalog), each the ordinary verb after a box; for every account, behind the bp-edit gate |
| `tool.dict` | Added | full-screen dictionary of a file (items by type and what they show; make, edit, delete, compile and try an item; the file's indices: make, build, delete, list); for every account |
| `tool.files` | Added | full-screen list of the account's files (kind, records, modulus, size, indices, trigger, case, dictionary) with make, clear and delete (each the ordinary verb, after a box) and analyse and the index and trigger lists (the terminal is handed to the verb); for every account |
| `tool.files` | Changed | refuses a VOC keyword (such as `all`) as the name of a file to make, clear, delete or report on |
| `tool.keys` | Added | full-screen diagnostic for the terminal and the keyboard, for everyone |
| `tool.query` | Added | full-screen query and report builder: file, columns (break and total), up to six conditions, four sort levels and options make a list / sort / count / sum sentence that is shown, checked, run into a results box (2000 lines), and can be saved to and loaded from the file `&queries&`; every sentence is checked again before it runs; for every account |
| `tool.query` | Changed | before every save and delete it checks that `&queries&` is an ordinary data file in your own account that your gates let you change, and deletes only saved queries (`tool.bulk`'s undo file has the same check) |
| `tool.test` | Added | full-screen test runner: lists the `test.*` programs of the account's program files, runs one, all of those shown or the failed ones (after a box) with `run`, and judges each by its last line `N passed, M failed` (pass, fail, no verdict; an abort is a fail); shows what a test printed; compiles a test that has no object code through `basic` after a box; for every account |
| `tool.voc` | Added | full-screen list of the account's VOC (type, what each entry points at, whether a pointer works, how it differs from the shipped VOC) with edit in SED and delete after a box; for every account |
| `tool.voc` | Changed | Delete no longer offers `delete voc all` or any other VOC keyword as an entry name |

### Data formats

| Name | Change | What |
|---|---|---|
| `convert.data` | Added | converts a file between formats |
| CSV functions | Added | `csvparse()`, `csvbuild()`, `readcsv`, `matreadcsv`: read and write whole CSV texts and rows with another delimiter, quote and escape, including a field with a line break |
| `import.*` verbs | Added | `import.csv`, `import.json`, `import.xml`: read a CSV, JSON or XML file into the records of an SD file |
| `json` keyword | Added | queries can write JSON |
| JSON merge, patch, path | Added | `jmerge()`, `jpatch()`, `jpath()`: RFC 7396 merge, RFC 6902 patch and JSONPath (RFC 9535) |
| `readjson`, `writejson` | Added | read and write JSON Lines through `openseq` |
| XML functions | Added | `xparse()`, `xbuild()`, `xpath()`: XML into a collection and back, and a path query <!--s 515--> |

### Encryption

Three simple layers, with no vault and nothing on by default.

| Name | Change | What |
|---|---|---|
| `encrypt.key` | Added | asks for a key on a hidden prompt and puts it in the key ring; `set` refuses a passphrase of fewer than 12 characters (`sdkey()` takes any that is not empty) |
| key ring subroutines | Added | `!keyset`, `!keyclear`, `!keylist`: fill, empty and list the session's key ring, kept in the memory of its own process |
| `sdkey()` and friends | Added | `sdsalt()`, `sdkey()`, `sdrandkey()`: a salt, a key from a passphrase, and a random key for `sdencrypt()` and `sddecrypt()`, open to every program; every `sdencrypt()` uses a fresh random nonce <!--s 504 g116 g123--> |
| `xe` conversion | Added | a dictionary item with `xe` (or `xe;name`) shows a field decrypted for a session that holds the key and the cipher text for one that does not; `iconv` encrypts |

### Files

| Name | Change | What |
|---|---|---|
| group size of a new file | Changed | `grpsize` is 4 (kb) in the shipped `sd.conf`, and the built-in value when it is absent; it was 2 and 1. 200,000 records had 5 to 11 percent of their groups overflowed at 2 kb and under 2 percent at 4 kb; writes 5 percent faster, reads 5 percent slower |
| `index` and the record id | Changed | fixed: an index followed an upper-case copy of the id; it now follows the id as the file stores it |
| index, deleting many records | Changed | fixed: in an index of three levels, removing the last value of a block took its whole branch out of the index (lookups missed records that were there, deleted values stayed listed), and a branch left with one block left its neighbours pointing at a freed block |
| record id counter | Changed | fixed: `write ... creating.seqkey` could give an id out twice after another write of the file header |
| `sdfix`, `sdidx`, `sdconv` | Changed | fixed several faults (see the changelog); `sdidx -m` says why it cannot make the directory |
| sort of equal or ordered keys | Changed | fixed: a long run took minutes; 100,000 equal keys took 168 seconds, now a fraction of one |
| sort that uses work files | Changed | fixed: equal keys came out in an order that depended on `sortmem` and `sortmrg`, and a `srt$unique` sort could keep a duplicate that was not the first to arrive; it now gives what the same sort gives in memory |

### Installer

| Name | Change | What |
|---|---|---|
| agent pack | Added | the guide and the knowledge pack are copied to `/usr/local/sdsys/agent-pack`, only when they match the installed version |
| changes document | Added | a release package carries it beside the installer as `sd-core-for-linux-<version>-changes.pdf`, `.html` and `.md`, and the installer copies the three into the shared account's `pdf` directory, where `pdf` lists the PDF |
| group account files | Changed | an upgrade puts the four record files of every kept group account back in the account's group |
| immutable `bin` | Changed | `deletesdcore.sh` lifts the attribute before it removes the system directory |
| installer: the `sdsys` user's groups | Changed | an install that keeps the accounts leaves the `sdsys` user in the group of each group account (`sdg_shared` among them); it used to take it out of all of them |
| installer source message | Changed | says which source it is downloading, the release tag or `main` |
| `sdsys` user in kept groups | Changed | an install that keeps accounts and finds the `sdsys` user in their groups asks once whether to keep it there (no unless `y`, and no with no terminal), takes it out on no, and records the decision in `/home/sd/$groups.ruled` so a later install leaves what the administrator did |
| `sdai` user | Added | made by the installer; removed with the accounts |
| shared account | Added | made by the installer; its help text and `pdf` directory are loaded |
| stored SDNet logins | Changed | the uninstaller removes `/var/lib/sd-net` when the accounts or the configuration are deleted |
| `upgrade_gates` | Changed | fills only a blank setting, so a kept `no` stays |

### Screen library

| Name | Change | What |
|---|---|---|
| accelerator keys | Added | `accel 'alt-s'` on a control; `&` marks the Alt-letter and the letter is drawn underlined |
| bracketed paste | Added | the library asks the terminal for it: pasted text arrives as one `paste` event and runs nothing; a text area takes it as one undo step, an entry its first line |
| break key | Changed | Ctrl-C comes back after an abort inside a full-screen page (the setting a page took is kept and given back at the next prompt) |
| check and slider labels | Changed | the label goes where `place` says, on the left by default |
| `color fg,bg` | Added | on the controls of a screen: label, entry, combo, check, slider, radio, list, button, progress |
| key decoding | Changed | a graphical terminal's F1 to F12, arrows, Home, End and the modified keys (`ctrl-left`, `shift-up`, `ctrl-pgup` ...) are read in both cursor-key modes; an unknown control sequence is ignored, not typed; a byte of 128 or more is never a command; a cut-short mouse report is ignored, not taken as the end of the input |
| containers and viewports | Added | `screen container`, `screen viewport`: a form bigger than its window: nesting, clipping, scrolling by keys, wheel and bars |
| redraw | Changed | the library writes only the text that changed, so a screen no longer flashes |
| resize inside a dialog | Changed | a resize that arrives while a question, a menu or the AI box is open is kept and given to the page afterwards; it used to be lost |
| `screen selector` | Added | a choice of one word among several |
| `screen set` | Changed | a `value`, `text` or `items` clause written as `''` empties the control, a clause left out changes nothing, and a written `''` on `enabled`, `wrap`, `readonly` or `visible` changes nothing; programs compiled before need compiling again |
| `screen slider` | Added | an on and off switch with words of your choice |
| `screen` statement | Added | menus, dialogues and forms from BASIC; colour; tabs, text areas, tables; the mouse |
| terminal type at sign-on | Changed | taken from the terminal's `TERM`: xterm, xterm-256color, VTE, Konsole, tmux, screen, alacritty, kitty, foot, rxvt and st are `xterm`, the console is `linux`; the account's login paragraph no longer forces `TERM LINUX` |
| text area keys | Changed | `screen memo` and the IDE's editor: Ctrl-A selects all (Home is the start of the row), Ctrl-O no longer copies (Ctrl-C does), F3 finds the next and Shift-F3 the one before (Ctrl-N found the next), Ctrl-D duplicates the line (Delete joins lines) and Ctrl-K cuts the whole line into the clipboard, where it cut to the end of the row |
| text area undo | Changed | `screen memo`: Ctrl-Z gives back exactly what was there; a record holding value, subvalue or text marks came back changed |
| text from data | Changed | the library never sends a control character to the terminal: one in a record, a record id, a file name or an AI answer is drawn as a reverse letter (ESC as `[`), one cell each; UTF-8 text and line drawing are unchanged |
| theme roles | Added | five new styles, `warning`, `success`, `readonly`, `busy` and `focus`, with a look in every theme (bold, underline and reverse only in `mono`), and `error` gets a `mono` look; programs that include `sl.h` need compiling again |
| themes | Added | `mono`, `classic` and `blue`; colour works on the Linux console terminal type |
| window size | Changed | SD reads the terminal's window size at the start and when it is resized; `@crtwide` and `@crthigh` follow it |

### SDNet

| Name | Change | What |
|---|---|---|
| `list.servers`, `delete.server` | Added | the administrator's list of defined servers, and removal of one <!--s g52 g26--> |
| `net` gate | Added | per-account switch, off as delivered: `net-on` and `net-off` |
| `netwait`, `netreply` | Added | `sd.conf` settings, 1 to 3600 seconds, for a connection and a reply; a silent server is given up on <!--s 235 g291--> |
| remote file administration | Added | for a login in `sdfilesadmin`; `create.file ... server` and `delete.file` of a pointer |
| remote files, a pointer | Added | a VOC entry whose first field is `n` points to a file on another server |
| remote files, cache | Added | a short record cache; `logto` closes the connections |
| remote files, index | Added | `indices`, `selectindex`, `setleft`, `setright`, `selectleft` and `selectright`; a query uses the other machine's index |
| remote files, query | Added | `list`, `count`, `sort`, `select`, `list.item`, `list dict` on a remote file; `fileinfo` type 7 |
| remote files, refusal | Changed | the server's own words are shown, not `status 0`; a lost connection is an error <!--s 256--> |
| remote files, reply checked | Changed | a reply that cannot be true is a lost connection at once |
| remote files, write | Added | for a server defined `write`: `write`, `delete`, `clearfile`, the locking reads and release |
| remote lock functions | Added | `recordlocked()`, `getlocks()`, `filelock`, `fileunlock`: work on a remote file |
| remote `select` | Changed | fixed: a server error stopped the program with an abort |
| SDNet logins | Added | `set.netlogin`, `delete.netlogin`: a person's login on a server, kept as derived values and never the password |
| `set.server` | Added | defines a server; `connect` shows its key hash for you to confirm <!--s g84 147--> |
| tls reads | Changed | fixed: a half record or a late ticket made a read wait without limit |

### Security

Fixes that close a way round a gate, and what the gates now ask.

| Name | Change | What |
|---|---|---|
| account directory parents | Changed | the installer leaves `/home/sd`, `/home/sd/user_accounts` and `/home/sd/group_accounts` 755 (they were 775), so one SD user cannot rename another account's directory and put one of their own in its place; an install made before this is fixed by installing again |
| API per-connection server unit | Changed | `sdclient@.service` sets ten of systemd's sandbox settings (`ProtectKernelTunables`, `ProtectKernelModules`, `ProtectKernelLogs`, `ProtectControlGroups`, `ProtectClock`, `ProtectHostname`, `RestrictRealtime`, `RestrictNamespaces`, `LockPersonality`, `SystemCallArchitectures=native`) on the stage of a connection that runs as root before login; not `NoNewPrivileges`, a capability bound, `ProtectSystem`, `ProtectHome` or `PrivateTmp`, which would stop `sudo sd-elevate` and the writes a session makes; a fresh install has them, an upgrade that keeps the unit files keeps the old unit |
| API Unix socket | Changed | `/tmp/sdsys/sdclient.socket` is mode 0660, group `sdusers` (systemd made it 0666, so the group restricted nothing and anybody on the machine could reach the first stage of an API connection, which runs as root); the installer adds `SocketMode=0660` to an existing unit that has none and leaves a value that is there |
| audit daemon restart | Added | `sdlnxd` runs as its own `systemd` unit, `sd-lnxd.service`, which starts it again two seconds after it fails (`kill -9`, a crash); a stop (`sd -stop`, exit 0) is not a failure and is not restarted; a daemon that fails five times in a minute is given up on; `sd.service` runs `sd -start -nodaemon` and wants it; a second daemon ends at once |
| audit trail copy in the journal | Added | every audit record is also sent to the system journal (`sd_Log`, facility `authpriv`), where the journal's daemon stamps the sender's real uid and pid, so a line added to the trail by a person with a shell can be told from one SD wrote |
| audit trail rate bound | Added | the audit daemon takes at most 600 records from one operating-system user in 60 seconds and drops the rest (the journal copy is not limited); the end of that window writes one line, `audit rate limit dropped=N taken=600 limit=600 window=60`, and the error log counts what was dropped |
| audit trail rotation | Changed | the audit daemon rotates the trail by size as it writes (1 MB, to `audit.<date>-<time>`, new file with the old owner, mode and append-only flag), so a machine that never restarts SD still rotates; `sd -start` uses the same code |
| audit trail writer | Changed | `sdlnxd` (root) writes the audit trail: a session sends each record over the Unix socket `/run/sd/audit.sock` and the daemon stamps `user=` and `pid=` from the kernel's credentials of the sender, so a person with a shell can no longer add a line that names someone else; the file is mode 0600 (it was 0620); with no daemon a session appends itself, which only `sdsys` and root can do, and the journal copy is then the only one |
| control codes in data | Changed | text from data (a record, a lock id another user made, a file name, a command shown by `pstat`) cannot send escape sequences to a terminal: the screen library draws control characters as reverse letters, the kernel's lock list, `getlocks()`, `pstat`, the `profiler` and `hsm` displays and `check.masters` show them as `?`; `kernel(k$show.safe, text)` gives a program the kernel's rule |
| error log mode | Changed | `errlog` is 664 (it was 775): every session appends to it and nothing runs it |
| files root runs | Changed | the installer makes `/usr/local/sdsys/bin` and every file in it `root:root` with no group or other write, and makes `bin` immutable (`chattr +i`), so the `sdsys` user cannot replace `sd`, `sdlnxd`, `sdidx` or `pcode`, or rename `bin` away and put its own in its place; a failure to seal is warned about in the closing summary too |
| global catalogue modes | Changed | the kernel refuses to load a global catalogue object that others or the group `sdusers` can write (message 11930), and the installer leaves everything in `gcat` 0755 after its last compile (a fresh install left `gcat/$cproc` 0664) |
| `$ipc` mode | Changed | directories 2770 and files 0660, `sdsys:sdusers` (it was 775): an operating-system user outside `sdusers` can no longer read the commands, `DATA` lines and messages that every SD user's process leaves in it |
| operating system paths | Changed | `dir()`, `select.dir`, `oscopy`, `!oscopy`, `!ioscopy`, `deleteseq` of a path, `setptr ... as pathname`, `setpu` and a VOC pointer out of the account each ask the account's `os` switch, and `sd-on` for another SD account |
| `ospath()` in the shared account | Changed | the keys to delete (5), make a directory (13) and make a path (14) are refused inside the shared account for anybody but SDSYS (false, `status()` the permission error); the `$internal` opcode already did, the function every other program uses did not |
| p-code a session runs | Changed | each session reads `bin/pcode` itself, and refuses a file that others or the group `sdusers` can write; the copy in the shared segment, which any SD user with a shell could change, is no longer run |
| phantom start-up records | Changed | a phantom runs the command, `DATA` lines and log file name of its start-up records in `$ipc` only if the process that started it sealed them (HMAC-SHA256 under a secret given only to the new process, in its environment); a record that does not check is refused, audited as `phantom refused` and reported to the parent; the phantom debugger's conversation is not sealed |
| print file refusal | Changed | outside the account: the message names the account instead of printing `%1` |
| privileges of a session | Changed | the administrator, `sh`, `os.execute` and `sd.accounts` bits and the gates are held in the process; the copy in the shared segment, which any SD user with a shell could change, is only shown by `listu` |
| `sd.conf` | Changed | every new session reads it: an edit to `SH`, `SPOOLER`, `USRDIR` and the other per-session settings reaches sessions started after it, and a bad line stops new sessions from starting until it is repaired (SD and running sessions are not affected) |
| `sdlnxd` | Changed | the root daemon finds the system directory from its own path instead of the shared segment, and starts `sd -cleanup` with `execl`, no shell |
| SDSYS in more than one place | Added | SDSYS may be signed on at two terminals, and it is now visible: the audit line `sdsys second session others=<n>`, `sdsys x<n>` on those rows of `tool.sessions` with `SDSYS in <n> places` in its counts line, and `<m> signed, <n> sdsys` on the home screen's Sessions and locks tile; a phantom, an API process and a session with no terminal are not counted |
| `setptr ... spooler`, `setpu` | Changed | fixed: the spooler string ran as a shell command for any account; only a session with the `os` switch may set it |
| shared memory modes | Changed | the shared segment and the semaphores are 0660 and given to the group `sdusers`; they were 0666, open to every local user |
| `show ... eval` | Changed | compiles its expression in memory; it no longer writes a temporary I-type into the file's dictionary (no edit gate saw it, and a session holding that record made `show` wait) |
| system directory | Changed | a session takes it from `SDSYS=` in `sd.conf`, not from the shared segment, which any SD user with a shell could change (the global catalogue, the register, the messages, the audit trail and the errlog follow it) |
| `u` conversion names | Changed | `iconv` and `oconv`: fixed: a name that begins with a dollar sign called an internal subroutine from an ordinary program; it is refused now |

### System

| Name | Change | What |
|---|---|---|
| default terminal | Changed | 140 by 42 |
| `sd -status` | Changed | fixed an overrun on a server that recorded no start time |

### Tools and the home screen

| Name | Change | What |
|---|---|---|
| 140 by 42 layout | Changed | `sed`, the collection editor and the debugger: 140 by 42, refused below it, survive a window made smaller, take no keys while the cursor is off the screen (the `ide` is 140 by 43, see its window lock) |
| `!ced()` data mode | Added | edits a multivalue record as a tree of fields, values and subvalues (a text or a list; a list never below the second level), so that nobody types a mark; started by `ide` F12 |
| `debugger` full-screen display | Added | on a terminal with an alternate screen the debugger takes the whole screen: source, breakpoints, messages and the command line; F1 help, F4 the program's screen |
| home screen | Added | every account starts in a screen of tiles; arrows, Tab, letters, mouse, F5, F10 |
| home screen `ai` line | Changed | Enter alone accepts a proposal that only opens one of the delivered tools but rejects a proposal of one of your own programs or of the Terminal tile (decided for the proposal, not for the page); it cannot run a command when the account's Terminal tile is off |
| home screen Recent group | Added | `View > Recent group`: the tiles started last, newest first, six at most; off as delivered, the person's own record in `&menus&`; `set.tile account recent off` is the administrator's wall |
| home screen at the same time | Changed | fixed: a session at the home screen kept the next session waiting at sign-on (the absent `start.default` file was read with a lock the program never let go); `osread` of a missing file left a lock too |
| home screen refused tile | Changed | a tile whose command is refused shows its message until a key is pressed, and the home screen no longer ends |
| home screen sub-menus | Added | a tile can open a second page of tiles with a Back tile, Esc and the path on the status line; eight deep; the delivered page declares none yet |
| `ide` | Added | tree, tabs, compile errors table, find, run, catalogue and debug; Ctrl-E hands a record to `sed` |
| `ide` autologout countdown | Added | with `autologout` set, the status line counts down the last 60 seconds before the session is signed out and says whether unsaved changes will be lost; any key stops it; it reads the inactivity clock `autologout` itself uses |
| `ide` collection-file records | Added | a record of a data collection file opens as the text of its JSON (one element to a line) and Ctrl-S parses it and writes the collection; text that is not a JSON object or array is refused with the record untouched; F12 hands the collection to `ced`; a missing record opens as a new `{}`; compile, SED, Save as and the include do not apply; a text is not saved into a collection file under a new name |
| `ide` dictionary items and VOC records | Added | `ide dict file item` and `ide voc record` edit them; the tree shows a file's dictionary as a node of its own; a save asks `dict.edit` or `voc.edit` as a program asks `bp.edit`; they show marks as tokens; `creating.seqkey` takes the file's next sequential id; a record that does not exist opens as a new one; an active select list opens its first records |
| `ide` edit as fields | Added | F12 or Go, Edit as fields: the record is shown as fields, values and subvalues in a fields view inside the IDE's own form (the collection editor's engine; the tree, the tab strip and the messages stay on the screen, and the view has the keyboard to itself while it is up) and comes back as text in the tab; the view writes nothing, the IDE's save does |
| `ide` editing commands | Added | Search, List matching lines (SED's VIEW: the lines that hold a text, in the table), Query replace (Yes, No, All, Quit; one undo step), Find options (match case, whole words), Upcase and Downcase the selection, Import a record here, Export the selection; Build, Run a command (its output in the table; a command that aborts is stopped and the IDE stays up); View, Refresh; none writes a record. In a record shown with `:@vm:` marks Replace changes the record's text, never a mark's token; a text to find is at most 256 characters |
| `ide` go to line | Changed | takes line,column, and field,value,subvalue in a record shown with `:@vm:` marks, as well as a line |
| `ide` import of an operating system file | Added | Search, Import a record here takes `path:/full/name`, from the tab that holds the file or from the file itself through the account's gates |
| `ide` key map | Changed | the settled keys: Ctrl-S is the only save key (F2 went); F5 runs, F7 debugs, F8 compiles, F9 builds (compile and catalogue); F6 and Shift-F6 are the next and previous pane (the tree has no key of its own: F6 / Shift-F6, the Go menu entry Files and records or the mouse reach it, because F3 is the text area's find next); Ctrl-PageDown and Ctrl-PageUp, and Alt-PageDown and Alt-PageUp for a terminal that keeps the Ctrl keys for its own tabs (GNOME Terminal), are the next and previous tab; Ctrl-N is New record, Ctrl-O Open record (a record that exists; names with a dollar sign are refused) and Ctrl-W closes the record (it asks when there are changes); Save as, Write a copy and Find in the records are menu entries with no key; the tree no longer lists the `$` entries |
| `ide` language of a record | Changed | chosen as `sed` chooses it - the file name, then the record id, then the first line (`#!/bin/sh`), then the languages a site added - where it was the suffix of the id alone |
| `ide` make operating system files | Added | New, Save as, the first save of an untitled buffer, Write a copy and Export the selection take `path:/full/name` and make a file of the operating system (mode 0666 less the umask), exclusively and before anything else changes: a file with content is never replaced (an empty one is filled), the directory is never made, and text with a NUL, a byte from 248 to 255 or over 2 MB is refused first; New opens the empty file in a tab and Save as turns the record's tab into the file's |
| `ide` marks as tokens | Added | a record that holds value, subvalue or text marks is shown with `:@vm:`, `:@sm:` and `:@tm:` and read back when saved, so nobody types a mark; a field that holds the text of a token is shown as it is |
| `ide` name form | Added | New record (Ctrl-N), the first save of an untitled buffer, Save as and Write a copy (both in the File menu) ask for the file and the record on one form; a refusal by the account's edit gate or a record that exists is said in the form, which stays open |
| `ide` open the include | Added | Go, Open the include opens the record that the `$include` line at the cursor names, in a tab |
| `ide` operating system files | Added | `ide path:/full/name`, or `path:/full/name` in Open's form, opens a file of the operating system in a tab; it is read and written by `!ide_osfile`, which is not an internal program, so the kernel asks the account's OS gate and edit gates for it (an account without `os-on` reaches its own directory only); saved in place (same inode, owner, mode and links), after a second look at the file (the overwrite question if it changed; a file removed or renamed over is refused) and read back after the write; CR LF, a missing last newline and tabs are kept; a NUL, bytes 248 to 255, a file over 2 MB, a directory, device or pipe are refused, bytes 128 to 247 or a file you may not write open read-only; locked while open; no recovery copy; compile, SED, fields, Save as and the include do not apply to it (Write a copy does: it keeps the text in a record or in a new file of the operating system) |
| `ide` operating system tree | Added | an *Operating system files* node after the account's files, only for an account with operating system access (the administrator or `os-on`): Return lists a directory (directories first, 1000 entries at most, names the IDE cannot show counted) and opens a file in a tab |
| `ide` record locks and read-only records | Added | a record open in a tab is locked until the tab is closed; one that another session holds, or that holds characters outside ASCII (bytes 128 to 247), opens read-only and cannot be saved; an `ide` left open blocks other sessions on its records, as `sed` does |
| `ide` recovery copy | Added | with `recovery-on` for the account, the text of a changed record is copied (owner-only, in the person's Linux home, `~/.local/state/sd/recovery/<account>/`, outside every account and so outside `backup.account`) after a second without typing and at the end of the session; offered back when the record is opened again; a copy the first version left in an account's `$recovery` is still offered; no copies when a directory above the home can be written by group or other; off as delivered |
| `ide` redraw | Changed | no flash; a click on the menu bar opens the menu; the active pane is marked `[*]` |
| `ide` replace | Changed | Ctrl-R is one undo step (one Ctrl-Z gives the text back; it forgot the undo steps), and follows the find options |
| `ide` save | Changed | takes the record's lock and writes on error: a refusing trigger or a full disk is reported and the text kept, where it ended the IDE and lost every tab; Save as moves the editor to the new record; an edit-gate refusal is shown whole in a box; Catalogue says so only when `catalog` did |
| `ide` tab indent | Added | Tab and Shift-Tab indent and outdent the line or the selected lines by 3, one undo step each, never a tab character (the `ide` editor only; `screen memo` keeps its Tab) |
| `ide` untitled buffer | Added | a bare `ide` opens an editable "Untitled 1" with the cursor in it; New record writes nothing until it is saved; the arrows stay in the editor at its first and last line |
| `ide` window lock and foot | Changed | needs 140 by 43 (was 140 by 42) and has the toolkit's foot: the status line, a border and a row of function keys on the last three rows; a window made smaller while it runs holds the keyboard behind a warning that gives both sizes and says unsaved text is lost unless the recovery copy is on, whatever the cursor is doing (the warning is worded shorter in a very small window); `sed` and `ced` keep the cursor-based lock |
| immediate messages | Changed | `message ... immediate` is shown in a box on any terminal |
| `sed` | Changed | the full-screen editor is back with a menu bar, the keys most editors have (`emacs` in `&sed.options&` keeps the old ones), undo and redo, syntax colour and the mouse; its keys are decoded from the terminal's terminfo entry <!--s 365--> |
| `sed` `path:` form | Changed | opens no file now: the `path:` form of a file name went with `FILERULE`, so `sed` asks the account's OS gate and cannot open the file; it no longer retries the name in upper case after that check (`ide path:/full/name` opens an operating system file) |
| `sed`, `ide`, `ed` input ended | Changed | fixed: they used all of a processor for ever when their input had ended |
| `tool.dict`, `tool.voc` edit | Changed | E hands the item or the entry to the `ide` (`ide dict file item`, `ide voc name`), with the page's own gates and boxes, where it used `sed` |
| toolkit pages: menu bar | Added | every `tool.*` page (the administrator pages, the development pages and `my.menu`) has a menu bar on its top row: Esc (when the page has nothing of its own to close first), F10, Alt and a letter, or a click on a title opens it; an entry does what its key does, through the page's own checks and boxes, so the bar adds no access; Esc opens the first menu that does not begin with Quit, so Esc then Enter cannot leave the page; on the home screen's top page Esc opens the bar too |
| toolkit pages: question forms | Added | creating an account, defining a remote server, the custom AI connection, the audit filters, the replace operation of a bulk update and a `my.menu` program ask all their answers on one form (Tab between them, the first refused answer named under them); `tool.dict` T picks the record from a list; none of them changes what is checked or run |
| `tool.sessions` output pane | Added | Ctrl-O (or View > Output) shows the commands the page ran and what they answered, newest first, in a pane of six rows; Ctrl-PgUp and Ctrl-PgDn scroll it, Esc puts it away; it is kept in memory only |
| toolkit pages: the whole window | Changed | the administrator pages, the development pages and the home screen use a window bigger than 140 by 43 whole: more rows, wider boxes, wrapped explanations, tiles spread over the window; they follow a resize, also while a dialog is open; at 140 by 43 they look as they did |
| toolkit pages: window limit and record-box titles | Changed | a window above 500 by 300 is refused before the screen is taken (it cost minutes); the boxes of a record write or delete are titled Write this record? / Delete this record? / Update these records? / Put these records back?; "Press Enter to return" names no screen |

## NO CHANGE

Items on the openQM list that were looked at for this release and needed no change to SD: the defect is not in SD, the
feature was already there, or it does not apply. They are here so that nobody looks for them above.

| Name | Change | What |
|---|---|---|
| 64-bit versions | None | no change in this release <!--s 196--> |
| `between` in a `when` clause | None | no change recorded <!--s 248--> |
| `*` comment line in a paragraph | None | already works <!--s g2--> |
| configuration file location | None | `sd.conf` is already in the SDSYS directory <!--s 14--> |
| `$echo` | None | already there in L1.1-3 <!--s g1--> |
| `errlog` permissions | None | the daemon asks for 0777 and the installer sets 775 (group `sdusers`): every SD user can write it, world write is deliberately not given <!--s 276--> |
| `formlist` bad data | None | no change recorded <!--s 265--> |
| hangup at the break key prompt | None | already ends the process by itself <!--s 266--> |
| inherited public variable | None | beside a function of the same name: already found <!--s 342--> |
| `insert` appending a field | None | `insert`, `ins` and `<-1>`: no change recorded <!--s 475--> |
| `itype()` | None | no change recorded <!--s 328--> |
| `list.users` | None | removed in an earlier release with the other user verbs; the administrator uses `listu` and `tool.sessions` <!--s g53--> |
| `locate` insertion position | None | also a very long numeric item: no change recorded <!--s 527 556--> |
| `loop` ... `repeat` | None | already there in L1.1-3 <!--s g59--> |
| `matbuild` trailing elements | None | unassigned elements at the end: no change recorded <!--s 557--> |
| `matchfield()` `n-mx` pattern | None | at the start of the template: no change recorded <!--s 562--> |
| memory alignment in `redim` | None | no change recorded <!--s 382--> |
| negative default argument | None | for an optional argument: the defect cannot occur, because the feature it belongs to was not in SD <!--s 324--> |
| Pick wildcards in `ne` | None | nothing to fix: the Pick wildcards (`option pick.wildcard`) were removed on 27 October 2026 <!--s 322--> |
| `qmbasic.warnings` | None | `sdbasic.warnings` was removed on 27 October 2026 with the three warning options <!--s g251--> |
| `$qmcall` | None | already there as the `$sdcall` flag, which lets a restricted client session call a subroutine <!--s g212--> |
| `readv` fatal error | None | no change recorded <!--s 559--> |
| record cache and case | None | no change recorded <!--s 330--> |
| `set.date` | None | SD still has the command; nothing was withdrawn <!--s 78--> |
| the inetd network server | None | SD opens no listening port of its own; sshd does <!--s 100--> |
| the `u` format in a report | None | already wraps a long value as `t` and `l` do <!--s 531--> |
| the user limit reached | None | login prints message 1000 and exits cleanly <!--s 275--> |
| `umask` | None | the verb and the `sd.conf` parameter were already there in L1.1-3 <!--s 5 143 g311--> |
| `update.account` | None | already there in L1.1-3 <!--s g102--> |

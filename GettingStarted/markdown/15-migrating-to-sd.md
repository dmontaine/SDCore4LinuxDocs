Title: Migrating to SD
Subtitle: Programs and queries from another MultiValue database: the words that bring a familiar behaviour back, and the words SD does not have.

Programs written for another MultiValue database often lean on one small behaviour
that SD does differently by default: a query that ignores case, a `read` that leaves
the variable alone when the record is missing, a divide by zero that warns instead
of stopping. SD keeps each of these behind a word you turn on yourself. This page
says where the words are set and which rules they follow; the two pages after it
list every word SD has, one line each.

| | | |
|---|---|---|
| **15a** | [Option words](15a-migrating-option-words.html) | the twenty-seven words of the `option` command |
| **15b** | [Mode words](15b-migrating-mode-words.html) | the names `$mode` accepts, and the lines of a `$basic.options` record |

## The rules the words follow

**Everything is off until you turn it on.** A new session has every option off and a
new program has every mode off. SD's own behaviour is the default, and a word only
moves a program or a session away from it, on purpose.

**One word changes one thing.** Each option and mode is a single, small difference:
`query.sort.no.case` makes sorts ignore case, `pick.read` leaves a read
variable alone, and so on. **There is no switch that makes SD behave like D3, mvBase,
UniData, jBASE or any other product as a whole.** `option d3`, `option mvbase`,
`$mode d3` and `$mode mvbase` are refused, and so is `option pick`, which switched
nine words on together and was removed on 27 October 2026. SD has one shortcut that
sets several single-purpose words together, and nothing larger:

| shortcut | sets |
|---|---|
| `option sdbasic.warnings` | `div.zero.warning`, `non.numeric.warning`, `unass.warning` |

It only switches words on and cannot be given `on`, `off` or `display`; turn
the words off one at a time, or with `option all off`.

**A word SD does not have is refused, not skipped.** `option` says *Option name not
recognised* and `$mode` stops the compile with *Unrecognised mode name*. A `login`
paragraph or a program that names a word from another product has to be edited. The
words of other products that SD does not accept are in the last section of this page.

**A word changes how your session or your program behaves, nothing more.** It does
not give an account the shell, `os.execute`, ssh, the API or the right to save to a
VOC, a program file or a dictionary. Those are the administrator's switches, one account
at a time (see [Accounts](05-account-types.html)), and no option or mode sets them.

## Where a word is set

**For one session: the `option` command.**

```
option                        lists every option and whether it is on
option name {on|off|display}  on is the default
option all off                turns every option off
option lptr {n}               prints the list on print unit n (unit 0 if left out)
```

Names are not case sensitive. A setting belongs to the session that made it, and a
phantom does not receive it unless the `inherit` option is on in the process that
started it. To have an option on whenever one account is entered, put the command in
that account's `login` paragraph; the administrator can put it in `master.login` to
have it run for every account.

**For one program: the `$mode` directive.**

```
$mode name {, name ...}
$mode -name
$mode default
```

`-name` turns a mode off again and `$mode default` turns every mode off. A mode is
built into the object code when the program is compiled, so changing it means
compiling again. The form is described in *SD Basic - Program Structure*.

**For every program in a file: the `$basic.options` record.** A record of that name
in the file that holds the source (or, failing that, in the VOC), whose first line is
`x`, gives each program compiled from that file a set of defaults: modes, a catalogue
action, tokens, an automatic `$include`. Its lines are listed in
[15b](15b-migrating-mode-words.html).

## Where to start

| if your programs or queries... | try |
|---|---|
| sort on text without regard to case | `option query.sort.no.case`; for one selection test, the `no.case` keyword after its operator |
| must go on running through a divide by zero, a non-numeric value or an unassigned variable while you find them | `option sdbasic.warnings` |
| expect a `read` that fails to leave its variable as it was | `$mode pick.read` |
| use `locate` as UniVerse does | `$mode uv.locate` |
| use `for` loops whose variable must be stored before the end test | `$mode for.store.before.test` |
| use matrices with no zero element | `$mode pick.matrix` |
| need every program of a file compiled the same way | a `$basic.options` record |

## Words other products have that SD does not accept

SD refuses each of these.

| from another product | in SD |
|---|---|
| `option d3`, `option mvbase` | not provided; see the rules above |
| `option qmbasic.warnings` | the shortcut is `option sdbasic.warnings` |
| `option x` *hex.string* | not provided; set the options one by one |
| `option no.echo.data` | a compiler mode: `$mode no.echo.data` |
| `option create.file.no.case`, `option create.dict.no.case` | not provided; give `no.case` on the `create.file` that makes the file (see [Lower case](11-lower-case.html)) |
| `option keep.filename.case` | not provided: a new file is always named in lower case (see [Lower case](11-lower-case.html)) |
| `option pick`, `assoc.unassoc.mv`, `pick.breakpoint`, `pick.breakpoint.u`, `pick.explode`, `pick.grand.total`, `pick.implied.eq`, `pick.null`, `pick.wildcard`, `qualified.display`, `with.implies.or`, `query.no.case`, `query.priority.and` | removed on 27 October 2026, with the Pick style of query they switched on: write `with city = "Reno"`, put the text after a `break.on` field the way SD does, and use the `like` operator for wildcards, `or` and brackets for the order of tests, and `no.case` after an operator or `option query.sort.no.case` for case |
| `option ampm.upcase`, `crdb.upcase`, `no.date.wrapping`, `space.mct`, `lock.beep`, `ed.no.query.fd`, `create.file.upcase`, `select.keep.case`, `debug.rebind.keys`, `proc.a` | removed on 27 October 2026: the output is as the default always was (`am`, `cr`, `db`), a date such as 31 February rolls into the next month, a lock wait is silent, and `fd` in `ed` asks before it deletes |
| `option local.cat.relative`, `option no.sel.when.filter`, `option silent.tandem` | not provided |
| `option pick.proc`, `option proc.if.no.case` | not provided: PROC is gone (see [Not in SD Core](14-not-in-sd-core.html)) |
| `$mode d3`, `$mode mvbase` | not provided |
| `$mode nocase.strings` | a directive of its own: `$nocase.strings`, or a `nocase.strings` line in `$basic.options` |
| `$mode numeric.boolean`, `scandup`, `sselectv`, `symtab0` | not provided |
| `$mode pick.errmsg` | not provided |

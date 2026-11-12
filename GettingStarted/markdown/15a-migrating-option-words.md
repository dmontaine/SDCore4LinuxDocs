Title: Migrating to SD: option words
Subtitle: Every word of the option command, what it changes, and where else it is described.

This page continues [Migrating to SD](15-migrating-to-sd.html). The words are the
eight that `option` lists. (Seven more were removed on 28 October 2026, each with the
behavior it named off now the only one, or on where that was the useful one:
`numeric.exponent` (`123.45E-2` is not numeric), `suppress.abort.msg` (`abort` always
says where it ran), `dir.sel.omit.hidden` (a select of a directory file includes the
names that begin with a dot), `no.phantom.notify` (a phantom always tells its parent),
`force.reload`, `stacked.account` (an `execute` of `logto` stays in the account it
went to) and `command.level.locks` (a file variable that goes closes its file and its
locks). Six more (`unass.warning`, `div.zero.warning`, `non.numeric.warning`, `inherit`, `query.sort.no.case` and `clear.select`, with the shortcut `sdbasic.warnings` and the `keep.select` statement), then three more (`chain.keep.common`, `backslash.not.quote` and `correlative.reuse`), then four more (`no.sel.list.query`, `catalogue.local`, `inherit.mfile.path`
and `correlative.nocase`) and eleven before them, whose off behavior is now the only one, were removed
on 27 October 2026: `run.no.page`, `paginate.on.heading`, `pick.ml.conv.mask`, `chained.select`,
`default.mv`, `query.string.comp`, `query.str.comp.all`, `assoc.all`, `query.footer.pause`,
`query.merge.print` and `keep.old.object`. Twenty-two words that existed only to imitate other
products were removed on 27 October 2026; see the last section of
[Migrating to SD](15-migrating-to-sd.html).) **All are off in a new session.** `option` *name* turns one
on, `option` *name* `off` turns it off, `option` *name* `display` shows it. The last column
names the page of the User set that also describes the word; **here** means this
page is where it is described.

## Queries: list, sort, select and the rest of the query processor

| word | what it does | also described in |
|---|---|---|
| `$query.debug` | lets a query take the `debugging` keyword; a development aid, shown by `option` only while it is on. Do not use it in an application | here |

## Errors and diagnostics

| word | what it does | also described in |
|---|---|---|
| `dump.on.error` | a fatal run-time error writes a process dump file (`sddump.`*n*) in the dump directory | here |
| `show.stack.on.error` | a fatal run-time error also prints the call stack: program, line and object address | here |
| `no.user.aborts` | the A (abort) answer is removed from the prompts that offer it: pause, the end-of-page prompt, the break key menu and the query processor's page prompt | here |
| `spool.command` | shows the operating system command that prints a job, just before it runs; a diagnostic aid | *SD Basic - Program Structure* |

## Files

| word | what it does | also described in |
|---|---|---|
| `dir.dtm` | writing a record to a directory file moves the directory's date and time modified, even when the record already existed | *SD Basic - Program Structure* |
| `git` | a directory file keeps `.gitignore` and `.gitattributes` under their own names on disk; without it the leading dot becomes `%D` | *SD Basic - Program Structure* |
| `inherit.ownership` | `create.file` gives a new file the owner and group of the account directory. Turn it on for an account only as an administrator's decision | *SD Basic - Program Structure* |

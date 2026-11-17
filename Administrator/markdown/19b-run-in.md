Title: run.in
Subtitle: The administrator's account-scoped run: one command from a fixed list, inside a registered account, and always back in SDSYS.

This page continues [The Master Files: Global
Changes](19a-the-master-files-global-change.html).

## Running one command inside an account: `run.in`

A program is compiled, cataloged and debugged in its own account: its VOC, its private catalog,
the files its I-types translate through. An account that is locked out of its own programs
(`bp-off`) cannot do any of that, so the administrator does it for the account.

```
run.in acme basic bp prog
run.in acme basic bp prog debugging no.query
run.in acme catalog bp prog local no.query
run.in acme decatalog prog
run.in acme delete.catalog prog local
run.in acme debug bp prog
run.in acme compile.dict cust total
```

The verb is in the SDSYS VOC only and refuses anyone else ("Command requires administrator
privileges"). It runs **one** command from the list above, in a **registered** account (never
SDSYS itself, never a path), and **it is back in SDSYS when the command ends**. That includes a
command that aborts, a break and a run-time error in a program being debugged: the session is put
back before anything else happens and says so ("run.in: the command did not finish; the session is
back in account acme"). Without this an administrator would be left in the account, with the
command's reach, until typing `LOGTO sdsys` (the administrator's way back by hand; it is refused to
every other session).

What it checks before it changes anything: the account and every name are one plain word (a-z,
0-9, dot, dash and underscore, a letter or digit first, at most 64 characters, and not a word SD
reads as an option); each option is on that command's own list and is given once; the first name of
`basic`, `catalog`, `debug` and `compile.dict` is a file in **that account's** VOC. **The command
SD runs is built from those words and is never the text you typed.** **`basic` is always given
`no.catalog`**, so a `$catalog` directive in the account's source (or in a file it includes, or in
its `$BASIC.OPTIONS`) is not acted on: without it, compiling the source as the administrator would
catalog it as the administrator, in the global catalog if the directive says `global`. To
catalog a program of an account, say so: `run.in acme catalog bp prog`. `run.in` does not start the
account's `login` paragraph (it would run with the administrator's rights), and it does not nest.

**The command does not run as the administrator.** The account's files,
VOC and programs are written by the account's user, so nothing in them is trusted:

- **The words must be SD's own.** The command word and every option word must be, in that account's
  VOC, exactly the entry SD ships. An account that has changed or removed one (its own `basic`, say)
  is refused before anything happens: *run.in: basic is not SD's own entry in the VOC of account
  acme (it is missing or was changed there); nothing was run*. Put SD's own entry back in that
  account's VOC (the record of the same name in `newvoc`; `update.accounts` puts the shipped entry
  back, whether it is missing or was changed: it asks first only when the type differs, and it
  keeps an entry marked `[LOCKED]` unless it is a verb) and try again.
- **For the command itself the session is not the administrator.** Only the one gate the command
  needs is on (`bp-edit` for `basic`, `catalog`, `decatalog` and `delete.catalog`, `dict-edit` for
  `compile.dict`, none for `debug`), and `sh` and `os.execute` are off whatever the account's own
  switches say. A program being debugged therefore has the account's reach, not yours: it cannot
  open another account's files, run a shell command, `logto` another account (*logto is refused
  while run.in is running a command in account acme*) or follow a Q-pointer out of the account.
  Everything is put back when the command ends, as above.
- **Compiling reads the account and nothing else.** A `$execute` in the source is a compile error
  (*$execute is refused in a compile started by run.in*), and an include or a dictionary that lies
  outside the account is refused; SD's own `syscom` headers are still found.

It adds no authority: the administrator can already `logto` into any registered account. What it
adds is the way back and a shorter list. Every use writes `run.in begin account=… command=…` and
`run.in end account=…` (or `run.in revert account=… reason=abort`) to the audit trail, and a
refusal writes `run.in refused …` with the reason.

## Continued in

[The Master Files: The Group and the
Modes](19c-the-master-files-group-and-modes.html) — the sdsys group and the
modes of what SD makes.

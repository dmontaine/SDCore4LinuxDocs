Title: SD VOC - Using and Managing the VOC
Subtitle: How the command processor reads the VOC, the verbs that manage it, and what account creation puts there.

This page continues [SD VOC - Structure and
Usage](32-sd-voc-structure-and-usage.html).

## How the command processor uses the VOC

The command processor is a BASIC program, `$CPROC`, and it runs a loop:
show any waiting messages, print the prompt, read a line, dispatch it,
repeat. The first word of the line is looked up in the account's `voc`
file.

### Name resolution

A name is tried **as typed, then lower case, then upper case** (and then
with each hyphen changed to a dot, in upper case and in lower case). This is
the change that lets a lower-case `voc`, `bp` and `newvoc` on disk
coexist with code and habits that still type names in upper case.

**Account names are the deliberate exception.** They are still folded
upward, which is what makes signing in case-insensitive.

### If the VOC has nothing, the private vocabulary is tried

If the account's VOC has a record `$private.voc` (type `X`, the name of a
file in field 2), a name that is in no VOC record is looked for in that file
next, as typed, then in lower case, then in upper case. The VOC always wins,
so the private vocabulary can add a command and never replace one the VOC
holds. See [SD VOC - A Private Vocabulary and Your Own Record
Types](32b-sd-voc-private-vocabulary-and-parser.html), which also describes
`$voc.parser`, the record that hands a VOC record of a type SD does not know
to a program of your own.

### If neither has it, the catalogue is tried

A name that is not in the VOC or the private vocabulary is looked for in the **private catalogue**
of the account and then in the **global catalogue**, `gcat`. A hit is
treated exactly as though the VOC had held `V` / `CA` / *name*. This is
why a program you have catalogued can be run by typing its name with no
VOC record of its own.

If neither has it, the command is refused by name.

## Verbs that manage the VOC

### set.file — write a Q-pointer

```
set.file account file.name pointer.name
```

Writes a Q-pointer into the VOC — field 1 `Q`, field 2 the account name,
field 3 the file name. After it, *pointer.name* is usable wherever a file
name is, and the data stays where it is.

**The account must be in the accounts register.** The name is folded to
upper case before the register is read. If it is not there you get
*Account name '...' is not in register* and nothing is written.

**The pointer is followed only into an account you could `logto`** (a member of
its group, and not suspended), whether or not your account holds `os-on`;
otherwise opening it is refused with status 3035. A file pointer you write
yourself (`ed voc ...`, or `create.file ... pathname`) must lead inside your own
account unless your account holds `os-on`.

### update.accounts — refresh from NEWVOC

```
update.accounts
```

Re-runs `LOGIN`'s `update.voc` paragraph, which copies any changed
records from the system `NEWVOC` into the account's VOC. **Since 17 Aug
2026 this is incremental** — it re-copies only the records whose stamp has
changed, not the whole file. Every ordinary account gets the same `NEWVOC`
now, so `update.accounts` is only ever bringing an existing account's copy
up to date after a release changes something — there is no tier list left
for it to consult.

### copy — copy records into the VOC

```
copy from voc messages,myname
copy from src.file to dict tgt.file record.id
```

`copy` can write into the VOC the way it writes into any file. The
`from voc` form copies a VOC record under a new name, which is how an
alias is made without `alias`.

### delete — remove a VOC record

```
delete voc name
```

Removes the record. **`.d` *name* at the command prompt asks first**;
`delete voc name` does not.

### .s and .r — save and recall

```
.s name s e
.r name
```

`.s` writes stack lines *s* to *e* into the VOC as *name* — a sentence
when the range is one line, a paragraph when it is more. `.r` loads a
sentence or paragraph from the VOC into the stack. **The record type
follows from what you saved** rather than from anything you say.

### Listing the VOC by type

SD has no ready-made `list` sentences. (Until 1.2-0 it shipped ten, `listf`,
`listfl`, `listfr`, `listk`, `listpa`, `listph`, `listq`, `listr`, `lists` and
`listv`, as R-records into a file called `SD.VOCLIB`; both are gone.) The query
processor does the same job with the `type` item of the VOC's dictionary:

| To list | Type it |
|---|---|
| all files (F-records) | `list voc with type = "F"` |
| local files only | `list voc with type = "F" and is.remote = ""` |
| remote files only | `list voc with type = "F" and is.remote` |
| all keywords (K-records) | `list voc with type = "K"` |
| all paragraphs (PA-records) | `list voc with type = "PA"` |
| all phrases (PH-records) | `list voc with type = "PH"` |
| all Q-pointers | `list voc with type = "Q"` |
| all remote references (R-records) | `list voc with type = "R"` |
| all sentences (S-records) | `list voc with type = "S"` |
| all verbs (V-records) | `list voc with type = "V"` |

To see the **file type**, the description and the data and dictionary
pathnames of the files, name those items:
`list voc ftype desc data.name dict.name with type = "F"`. The type is `DH` for a
dynamic hashed file (followed by `I` for alternate key indices, `S` for
statistics and `T` for a trigger function), `Dir` for a directory file, `Err`
and the error number for a file that will not open.

The dictionary of the VOC also has the items **`trigger`**, **`encryption`**
and **`replication`**, so `list voc with type = "F" and with trigger` lists the
files that have a trigger function. SD has neither encryption nor replication,
so `with encryption` and `with replication` select nothing and `with no` selects
every file.

### count — count the records

```
count voc
count voc with v = "V"
```

`count` over the VOC gives the total record count. With a selection
clause it counts by type or by any other field.

### ct — display a record

```
ct voc name
```

Displays the record field by field. This is the way to see what a VOC
entry actually contains without an editor.

## The VOC and account creation

`create.account` copies the VOC from `NEWVOC` in the system directory —
**399 records**, counted directly, and identical for every ordinary
account. SDSYS's own VOC is copied from `voc_template` instead — **424
records** — which carries the administration verbs `NEWVOC` does not:
`create.account`, `delete.account`, `modify.account`, `config`, `set.date`,
`update.accounts`, `clean.account`, `list.readu`, `list.locks`, `lock`,
`unlock`, `listu`, `remote.ssh`, `remote.api`, and the rest of the set the
*Administrator* documentation covers. **Unlike SD Core for Windows, there is
no separate `grant`/`revoke`/`list.grants` set** — `modify.account
add`/`delete` folds the grant into one place; see *Accounts and Security* in
the Administrator set.

**What SDSYS alone can do is in the VOC, not in the verb.** An ordinary
account does not have `create.account` because the VOC record for it is
not there, not because a security subroutine refuses it. The name is
simply not recognised. This is the design: what only SDSYS may do is
withheld by giving or withholding the record, the same mechanism the old
account tiers used before they were removed.

## Case on disk

Since 18 Aug 2026 the VOC ids are stored in lower case — `list`,
`create.account` and so on. This changes nothing about what you type —
SD tries a name as typed, then lower, then upper. What it changes is what
SD prints back: `CT VOC LIST` answers `VOC list`.

The file-pointer entries — `bp`, `bp.out`, `gpl.bp`, `gpl.bp.out` — moved
to lower case on 19 Aug 2026. **The migration is complete, not partial**: an
account's own `voc`, and the system directory's `newvoc`, `accounts`,
`messages` and `syscom`, are all lower case on disk too, confirmed directly
— there is nothing left in upper case to migrate. `qfile` was never a path
of its own; it is a VOC pointer to `@SDSYS/$ipc`, the session IPC area, and
has no on-disk name to fold.

## What is not here

**There is no verb that edits the VOC directly.** `ED` edits any file,
and `ED VOC`*name* is how you edit a VOC record by hand. But there is no
verb whose purpose is to create or modify VOC entries — `set.file` writes
one kind, `.s` writes two, and everything else is done with `ED` or with
`copy from voc`.

**`PROC` is removed.** A `PQ`-type record is refused by name. Nothing
that ships is type `PQ`, so this can only be met in a VOC record somebody
wrote.

**The `M` (menu) record type is removed.** A VOC record of that type is no
longer dispatched; the home screen (`home`, or `menu`) is the menu system.

**`EDIT` runs.** It was once exactly the kind of VOC entry described
above — present but undispatchable, its type field reading
`Verb - Full screen editor` rather than `V`. That was reversed 26 Aug
2026: it is a real `V` record now, a working full-screen editor. See [SD
VOC - Structure and Usage](32-sd-voc-structure-and-usage.html#what-sdsyss-own-voc-holds).

## See also

[SD TCL - The Command Processor](19-sd-tcl-command-processor.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html) ·
[SD Basic - File Handling](07-sd-basic-file-handling.html) ·
[SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html).

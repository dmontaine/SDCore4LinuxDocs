Title: SD BASIC - File Handling: Locking and Asking About a File
Subtitle: Locks, transactions, asking about a file, and creating and configuring.

This page continues [SD Basic - File
Handling](07-sd-basic-file-handling.html).

## Locking

SD locks a **record**, not a row or a page, and the lock belongs to the session.

```
readu variable from file.variable, record.id {locked ...} then ... else ...
readvu variable from file.variable, record.id, field ...
matreadu matrix from file.variable, record.id ...
recordlocku file.variable, record.id
recordlockl file.variable, record.id
release {file.variable {, record.id}}
```

| | |
|---|---|
| `readu` | read **and take an update lock** |
| `readl` | read and take a shared read lock |
| `recordlocku` | take an update lock without reading |
| `release` | give locks back |

`write` releases the lock it finds. `release` with no arguments releases
everything the session holds.

```
recordlocked(file.variable, record.id)
```

reports the state. After `readu`, `recordlocked(f, 'R1')` is **2**;
an unlocked record reads **0**; after `release f, 'R1'` it is **0** again.

**The `locked` clause is the only way not to wait.** Without it, a `readu`
against a record another session holds **blocks until that session lets go**.
With it, control goes to the `locked` branch immediately:

```
readu rec from f, id locked
   print 'Someone else is editing that record.'
   return
end then
   ...
end else
   ...
end
```

A program without a `locked` clause is a program that can hang a user
indefinitely with no message. **Any interactive read-for-update should have
one.**

`filelock` and `fileunlock` lock a whole file, and `lock` / `unlock` take one
of 64 numbered general-purpose semaphores — used to serialize something that is
not a record at all, such as a report run.

**The rest of this is its own page.** What the other session sees, what every
`recordlocked()` code means, how to find out **who** holds a lock, and how long
a wait actually is, are all in [SD Basic - Locks and Transactions](14-sd-basic-locks-and-transactions.html), which
covers what two sessions running at once see of each other.

## Transactions

```
begin transaction
   ...
   commit
   ...
   rollback
end transaction
```

Everything written between `begin transaction` and `commit` either all lands or
none of it does. `rollback` discards the lot.

**Locks taken inside a transaction are held until it ends**, whichever way it
ends. That is what makes the transaction safe and also what makes a long one
expensive — keep the span short, and never wait for user input inside one.

**And inside a transaction you must already hold the lock on every record you
write.** The same `write` that works outside one fails inside it with
*"Error 3023 (o/s 0) writing record (Possible full disk?)"*, which is a lock
error wearing a disk error's message. [SD Basic - Locks and Transactions](14-sd-basic-locks-and-transactions.html) has
the detail, along with what `commit`, `rollback` and simply reaching
`end transaction` each do.

## Asking about a file

```
fileinfo(file.variable, key)
```

On a newly created dynamic file:

| Key | Meaning | Result |
|---|---|---|
| `0` | is this variable an open file? | `1` |
| `1` | the VOC name it was opened by | `ZZWORK` |
| `2` | the path on disk | `/home/sd/user_accounts/don/zzwork` |
| `3` | file type | `3` |
| `5` | modulus | |
| `6` | minimum modulus | `1` |
| `7` | group size | |
| `11` | current load percentage | |
| `13` | does the file have alternate key indexes? | |
| `1001` | read-only? | |
| `1003` | size in bytes, excluding indexes | |
| `1021` (`FL$WHO`) | the user numbers of the other sessions that have the file open, a field mark between them | `14` or `14` : `@fm` : `22`, null when there are none |
| `1100` (`FL$HOLDERS`) | the same sessions as text, for messages | `14 (ann), 22 (don)` |

**Key `1021` is the openQM `FL$WHO`, and the caller is left out** unless it has the file
open through more than one file variable. Code
that wants text for a message asks `1100`, as SD's own "cannot gain exclusive access"
messages do. Compile with `$include keys.h`, so that the names carry whatever number they have.

File types: `1` SH, **`3` DH — an ordinary dynamic file**, `4` directory, `5`
sequential.

> **Unlike SD Core for Windows, there is no path-translation caveat
> here.** This port runs natively, so the path `fileinfo()` returns is
> already the one Linux program will use it directly — nothing to
> convert.

> **There is no record-count key.** Key `6` is the *minimum modulus* and reads
> `1` on a small file whatever it contains — `1` with two records
> present and `1` again after `clearfile`. To count records, `select` the file
> and read `selectinfo(list, 3)`, or count in a `readnext` loop.

`dir(pathname)` lists an operating-system directory as a dynamic array - one field
per entry, with the name, `F` or `D` and the size in bytes as its values. **An entry
is `F` only when it is a plain file and `D` only when it is a directory** (a link is
judged by what it leads to): a socket, a device or a pipe is
left out.

## Reaching another file's data

```
trans({dict} file.name, record.id, field, action)
rtrans({dict} file.name, record.id, field, action)
```

Both fetch one field of one record from a file, opening it if needed. `trans`
takes a file name; `rtrans` takes an already-open file variable instead.
(`xlate` was a second name for `trans` and was removed in 2.0-0.)

The *action* says what to do when the record is missing — **or when the file
cannot be opened at all**, which takes the same action:

| | |
|---|---|
| **x** | return the null string, and say nothing (the default) |
| **v** | return the null string and print an error (`Cannot open 'name'` for a file) |
| **c** | return the record id itself |
| **n** | return the record id itself |

(A file that would not open prints the message only with **v**.)

A *field* of `0` returns the record id.

**These open a file on every call unless it is already open.** In a loop over
many records that is a real cost — `open` the file once and use `rtrans`, or
read it directly.

## Creating and configuring

```
create.file path {directory | dynamic}
create file.variable then ... else ...
configure.file file.variable, key, value
```

Most applications create files with the `create.file` **command** rather than
the statement — from BASIC, `execute 'create.file ...'` is the usual route, and
it is what the examples on this page use.

`set.trigger` attaches a program that runs on every write or delete to a file.
A trigger runs inside the caller's transaction, so anything it does is part of
the same all-or-nothing unit. A directory file can have one too: it is
called by `read`, `write`, `delete` and `clearfile`, and not by `writeseq`, `writeblk`,
`oswrite` or `osdelete`; see *Triggers* in
[SD TCL - Files and Records: Comparing, Triggers and Importing](20-sd-tcl-files-and-records-2-comparing-triggers-and-import.html).

## What is not here

Nothing in the file-handling group has been removed from this port, but two
things about it changed:

| | |
|---|---|
| **VFS** | the virtual file system layer has been **removed from the C entirely**. `fileinfo()` never reports a VFS type, and the type code is gone |
| **The data tree** | `/usr/local/sdsys` and the account directories are protected by ordinary Linux file permissions — see *Security* in the **Getting Started** set for exactly what that does and does not guarantee here |

## See also

[SD Basic - Select Lists](08-sd-basic-select-lists.html) · [SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html) ·
[SD Basic - Sequential Files](10-sd-basic-sequential-files.html) · [SD Basic - Alternate Key Indexes](09-sd-basic-alternate-key-indexes.html).

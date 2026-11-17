Title: Sessions and Locks: Lock Tracing, Task Locks and the Sessions Screen
Subtitle: lock.tracer, list.locks, lock, clear.locks, unlock and tool.sessions.

This page continues [Sessions and Locks](02-sessions-and-locks.html).

## Who took which lock, and where: `lock.tracer`

`list.readu` shows what is locked *now*. When the question is who took a lock, in which
program and on which line, or what locked what in the second before a hold-up, switch
the tracer on, let the system run for a short while, and read the log. **Administrator only.**

```
lock.tracer on
lock.tracer off
lock.tracer {user n} {lptr {n}} {no.page}
```

While it is on, every lock any session takes or lets go is added, as one line, to the file
**`locktrace` in the system directory**. `on` empties that file first, so a log is one
switching-on's worth. The file is made with mode 0620: the administrator reads it, and the users
of SD append to it, which is how a session that is not an administrator is logged at all.
A link left in the file's place is refused, and the tracer will not start on it.

The report lists the lines, oldest first, with the **date and time**, the **user number**, the
**action**, the **program** that was running and the **line number** in it, the **file** (cut
from the left when it is long) and the **record id**. `user n` shows one session's lines. `lptr`
prints them, `no.page` stops the pause at the end of a page.

| action | means |
|---|---|
| `Get RU` | a record update lock taken |
| `Get RL` | a shareable read lock taken |
| `RL->RU` | a read lock raised to an update lock |
| `RU->RL` | an update lock lowered to a read lock |
| `Get FX` | a file lock taken |
| `Rel RX` | a record lock let go |
| `Rel FX` | a file lock let go |

**It logs everything, SD's own locks included**: a login takes `$ipc`, the command processor
takes `$command.stack`, and reading the log reads a file. Ask `lock.tracer user n` for one session,
or look for the file you care about. The volume is large and every lock costs a file write, so switch
it on for a short time and off again.

> **Only a lock that is granted is logged**: one that is refused, or has to wait, is not, until the
> moment it is granted. **A session that is killed or lost** has its locks cleared by the cleanup, and
> that is not logged either, so a `Get RU` with no `Rel RX` after it may be a lock the cleanup gave back.
> A program that ends normally lets its locks go through the log, on the line of its `end`. The log is
> lines of value-mark-delimited fields (epoch time, user, pathname, record id, action number, the
> program's object, offset in it in hexadecimal, line), for a program of your own to analyze. openQM's
> report needs a terminal 132 wide; this one is 120.

## Task locks: `list.locks`, `lock`, `clear.locks`

Task locks are **64 numbered flags with no connection to any data**. They mean
whatever the programs using them agree they mean — usually *only one session
runs this job at a time*, where the thing being protected is not a single file.

```
list.locks
lock n {no.wait}
clear.locks {n}
```

```
:list.locks
No task locks reserved by any user
```

and with lock 5 held by user 16, `*` marking your own session:

```
:list.locks
 0:       1:       2:       3:       4:       5: 16*   6:       7:
 8:       9:      10:      11:      12:      13:      14:      15:
16:      17:      18:      19:      20:      21:      22:      23:
```

*(64 numbers over eight rows; the rest are blank and are cut here.)*

### `lock` waits unless you tell it not to

```
:lock 5 no.wait
Set task lock 5
:lock 5 no.wait
Task lock already owned by this process
```

**Without `no.wait` it waits for ever.** It prints *Waiting for task lock to
become available* once, then retries every two seconds until it gets it — right
for a job that must run, wrong for anything unattended. **`no.wait` turns the
wait into a refusal** (*Task lock is already in use*), which a script can act on.

### `clear.locks` gives back your own, and only your own

```
:clear.locks 5
Released task lock 5
:clear.locks
All task locks released
```

**With no number it releases all 64 this session holds**, and says *all* whether
it held any or not.

| | |
|---|---|
| *Released task lock n* | it was yours and it is now free |
| *Task lock n is held by another process* | **`clear.locks` will not take it** |
| *Task lock n is not held by any process* | it was already free |
| *Task lock number must be in range 0 to 63* | from `clear.locks 99` |

## Forcing a lock open: `unlock`

```
unlock file n {user n} record.id {record.id …}
unlock file n {user n} all
unlock file n {user n} filelock
unlock tasklock n {n …}
```

**This is the only verb that takes somebody else's lock, and it needs an
SDSYS session** — having the verb is not enough:

```
:unlock
Command requires administrator privileges
```

**It names a file by number, not by name** — the `File` column of `list.readu`.
That is deliberate: the lock is on a file the machine has open, which may not be
in your VOC at all and may be reached under different names in different
accounts.

| | |
|---|---|
| **`file`** *n* | the file, by the number `list.readu` printed |
| **`user`** *n* | restrict to one session's locks |
| **`all`** | every record lock matching, rather than named ids |
| **`filelock`** | the file lock, which cannot be combined with record ids |
| **`tasklock`** *n* | force a task lock, including one held by another process |

**A file number or a user number is compulsory** — *Either a file number or a
user number must be specified* — so there is no `unlock` that means *everything
on the machine*.

> **Unlocking is not free and SD cannot make it so.** A lock is a promise its
> holder is relying on. Forcing one open while its owner is alive lets two
> sessions write the same record and tells neither. **Establish that the holder
> is dead first** — `pstat` on the user number, `listu` for *(logout pending)* —
> and prefer clearing the session to clearing the lock.

### `unlock tasklock` is the only way back from a killed holder

**Task locks are released when a session ends normally.** They are not part of
any file, so nothing has to be written back.

> **`sd -cleanup` does not give them back, and that is a defect.** It releases
> a dead session's record locks and file locks and leaves its task locks held,
> by a user number nothing is behind, until SD itself is restarted.
> `list.locks` shows the number with an owner and `clear.locks` refuses it
> because it is not yours. **`unlock tasklock` *n*, run as SDSYS, is the way
> out** — that is what the forced form is for. It is recorded in the
> project's fix lists.

## Sessions and locks on one screen: `tool.sessions`

```
tool.sessions
```

**A full-screen page for the administrator** (SDSYS's VOC only; an ordinary account does
not have the verb, and the page is refused before it reads anything to anyone who is not
the administrator). It needs a window of 140 columns by 43 lines. The top list is every
session — user number, Linux process, when it signed on, its kind (user, phantom, API or
SDNet), the login user, the account it is in, where it came from, and whether it is yours
(a star) or a logout is pending. **When SDSYS is signed on in more than one place on a
terminal, each of those rows also says `sdsys x<n>`, the counts line says `SDSYS in <n>
places`, and the audit trail has a line `sdsys second session others=<n>` for each one that
signed on while another was there** (see *Being SDSYS* in *Accounts and Security*). **Ctrl-O
opens an output pane** (six rows, between the row box and the foot) that keeps the commands the
page ran, with what each answered, newest first; Ctrl-PgUp and Ctrl-PgDn scroll it and Esc puts
it away. It is kept in memory for this run of the page only. The lower list is every lock — the user, the file number
and path, the type (`FX` and `SX` lock a whole file, `RU` is read and update, `RL` is read,
`WAIT` is a session waiting for a lock), the record id, since when, and whether a session
with that user number is still signed on. Under the sessions the page says whether logins
are inhibited and by whom, and under the locks it gives the lock limit, the number held
now and the most there have been. **Both lists are read again every three seconds, with no
key pressed, and on F5, and a refresh keeps the cursor on the same user or the same lock,
not on the same row number.** A box under the lists explains the row under the cursor in
plain sentences and shows the exact command its key would run.

| Key | What it does |
|---|---|
| arrows, Page Up, Page Down, Home, End, a click | move in the list that has the focus |
| F6, Shift-F6 | change to the other list (and to the AI line, when the AI is on for the account) |
| L (sessions) | `logout` the selected session; the user number is typed again to confirm. For a session whose process is gone the entry is cleared and its locks are released |
| U (locks) | `unlock` the selected lock; the holder is not told |
| I | `inhibit.login on` when logins are allowed, `off` when they are inhibited |
| / | go to the next row of the list that has the focus that holds a text you type (a user number, a name, a record id; any case; round to the top) |
| F5 | read again |
| F1, ?, a click on the [?] | explain the page |
| Ctrl-Q | leave |

**The page changes nothing by itself.** Each of the three keys builds one command from
values the page has read and checked, shows it in a box with what it does, and runs it
only when you answer Run; Cancel is what Enter chooses. Those three commands are the only
ones the page can run. **`logout` and `unlock` write no audit line of their own, so the
page writes one for every command it ran** (`tool run app=tool.sessions command=...
status=...`), as well as the line that says it was started (`tool start
app=tool.sessions`); `inhibit.login` writes its own as well.

What each key refuses, in words, before any box opens: `L` on the session the page runs
in (leave it with Ctrl-Q); `U` on a `WAIT` row, which is a session waiting for a lock and
not a lock; `U` on a record id with a character the page will not put in a command (only
lower-case letters, digits, dot, dash and underscore go through) or an id that is one of
the words `unlock` reads as a keyword (`all`, `file`, `user`, `filelock`, `tasklock`) —
release those at the prompt with `unlock`. The lock table keeps record ids in upper case
and shows them so; the page sends the id in lower case, which the verb folds.

**Not on the page:** a message to a user, `logout all`, and any change to a session of an
ordinary account's own work. An ordinary account has no such page: its own sessions are
`!listu` from a program.

## Who has these verbs

**All of them are SDSYS's**, so an ordinary account does not have the names
at all — being SDSYS is the whole of the gate, for every verb on this page,
including `unlock`, `logout` and `inhibit.login` against another Linux account's
session. (`inhibit.login` refuses anyone else by name as well, in case a VOC
entry has been given to an account.)

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Operating System Access](03-operating-system-access.html).

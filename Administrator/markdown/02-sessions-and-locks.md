Title: Sessions and Locks
Subtitle: Seeing who is logged in, ending a session that will not end itself, and inspecting or forcing the locks a session holds.

These are the verbs for looking at the machine as a whole and intervening in it:
**whose sessions are running, what they are holding, and how to take either
away.** Every one of them is SDSYS's.

> **This document is separate so that it can be withheld.** It links to
> nothing outside the administrator set. Where a user-set page is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part.

> **Every listing on this page was produced by running it**, on SD Core for
> Linux. The lock listings come from a program that took the locks
> first and then ran the verb against itself, because a lock nobody holds is not
> something a listing can show.

## Two things are not on this page, on purpose

**A programmer needs to understand locks without being able to force one**, so
the *user* documentation keeps the part of the subject that is theirs: what a
task lock is against a database lock, and `release`, which gives back locks your
own session holds and needs no privilege at all. The same goes for `status`,
`phantom`, `pstat`, `pdebug` and `pdump` — a programmer's view of their own
processes.

**This page is the other half**: the verbs that see and act across the machine.

## Who is logged in: `listu`

```
listu {no.page} {lptr {n}}
```

```
:listu
  User  Pid          Puid  Login time    Origin : Username
    12  1789               27 Aug 13:14  : don
    19  1808               27 Aug 13:53  : don
*   27  1828               27 Aug 13:59  : don
```

| | |
|---|---|
| **`*`** | the session you are typing in |
| **`User`** | SD's user number — what `logout`, `pstat` and `pdump` all take |
| **`Pid`** | the Linux process id |
| **`Puid`** | the user number of the **parent**, filled in for a phantom and blank otherwise |
| **`Origin`** | where the session came from |
| **`Username`** | the **Linux** account the session runs as, not the SD account it is in |

**`Username` is the column that matters for permission.** Almost every control
on this page is keyed to the Linux identity, not to the SD account — so two
sessions showing different accounts but the same username are, as far as
`logout` is concerned, the same person's.

**Each line ends with the account the user is in** (`: jack, sales`). A user
moves into another account with `logto` and the table follows; a phantom starts
in its parent's account. The account is shown to the administrator and, for
anybody else, only for the sessions of the login user who is asking; **another
user's account is left blank.** `listu` itself is still the administrator's
verb: an ordinary account has `!listu`, from a program, whose ninth value is the
account.

```
listu detail {no.page} {lptr {n}}
```

`detail` adds a line above the report: the interactive users, the API sessions,
the phantoms that count as licensed, the other phantoms, and the most users
there have been at once since SD started. `system(1056)` gives the same five
numbers. **SD has no licence count**, so the third number is whatever the system
marks as chargeable.

**`Origin` is blank for a local session and that is not a fault.** It reports
an address or a device name, and a console or piped session has neither. It
reads `Phantom` for a phantom and an IP address for a network client.

`SDNet` is also among the values it can print, and you will not normally see
it. The mark behind it is set in only one place, the API server's request 29,
"open an SDNet file", which is refused unless `NETFILES` has bit 2 set (see
*Configuration*). The SDNet described in this set, where a program opens a file
on another SD server, does not use request 29, so a session that comes from it
shows an address like any other API session. This was read from the source and
not run.

**`(logout pending)`** after the name means somebody has asked that session to
end and it has not gone. See below.

## Ending a session: `logout`

```
logout                  end this session
logout n {n …}          end another session, by user number
logout all              end every session but this one
```

**`logout` with no argument ends your own session.** It is `quit` under
another name, which is worth knowing before typing it intending to list
something.

```
:logout 999
Only administrators can logout processes running with other usernames
```

**A session may end only sessions running under the same Linux account**
unless it is SDSYS's. The refusal above came from an ordinary session, and
user 999 does not exist — **the privilege test happens before the number is
looked up**, so this message does not tell you whether the user was real.

**`logout all`** is stricter still: it must be run from the `SDSYS`
account, reached the one way described in *Accounts and Security*. It
leaves your own session alone.

### When a session will not end

`logout` **signals** a process. **If the process has already gone** — killed from
outside SD, or lost with a terminal — there is nothing to signal, and `logout`
finds that out first: it **clears the entry and releases every file, record,
group and task lock the session still held**, and says so (then the text of
message 10167, *User n was not running, so there was nothing to log out*):

```
LOGOUT reaped user 43 (pid 1799435, don) - process was gone.
```

*Run on 24 October 2026 in a sandbox, against a session killed from outside
with `kill -9` while it held a record lock: `logout 43` printed the line above,
and afterwards `listu` did not list the user and `list.readu` did not show the
lock.* The entry matters because **it holds a slot and an exclusive-access
claim**: `NUMUSERS` counts it, and any verb that wants a file to itself —
`build.index` is the usual one — is refused while it is there. So **the way to
clear a dead session is `logout` *n*.**

A session that is **alive and does not answer the signal** is the other case,
and it keeps its entry with **`(logout pending)`** beside it; asking again
signals it again. *That case was not run for this page.* `sd -cleanup`, run as
SDSYS (and a restart of `sd.service` if that does not take it), is the
remaining way to clear entries of sessions that are not going to end.

**Confirm the session is actually dead before clearing it.** `pstat` *n*
answers *(Not responding)* for a session with nothing behind it — it asks the
process and waits about four seconds — and that is the difference between a dead
entry and a busy one. `pstat` is a programmer verb and is documented in the user
set. (`logout` itself only clears an entry whose process is not there; it
signals a live one.)

## Keeping new sessions out while you work: `inhibit.login`

```
inhibit.login on        no new session until it is switched off
inhibit.login off       allow them again
inhibit.login           say which it is, and who set it
```

For maintenance that needs the system quiet. A person who signs in while it is
on is refused with *SD is not accepting new sessions: logins have been
inhibited by* name *(inhibit.login). Try again later.*, and so is an API
connection, before any credential is looked at. **Sessions already running are
not touched** — it does not log anyone out — and neither are the phantoms the
session that set it starts. The refusals are on the audit trail
(`login refused ... reason=logins are inhibited (inhibit.login)`), and so are
the `inhibit.login on` and `off` themselves.

**It is SDSYS's verb, and SDSYS is never locked out by it.** openQM keeps out
every new session, the administrator's included, and the one who set it can be
the only one to switch it off; on a lost terminal that means restarting the
service. Here the administrator can always open a new session, and **any
administrator session may switch it off**. If the session that set it is killed
the inhibit is ignored from then on — the record names a user number *and* a
process id, and a process that is not there holds nothing — and the next `on`
replaces it.

The record is the file `login.inhibit` in the SDSYS directory (user number,
process id, login name, date, time). **It is not the same thing as the hold that
`backup.account` and `restore.account` take**, which keeps *everybody* out,
the administrator's new sessions included, while they run. That hold also lapses
when the session that took it is killed, which it did not until 15 October 2026:
it used to wait for `sd -cleanup` to remove the dead session's entry.

## The paragraph every session runs first: `MASTER.LOGIN`

A VOC record named `MASTER.LOGIN` in the SDSYS account, if it is a paragraph (its first
line is `PA`), is run **once by every new session, before the account's own `LOGIN`
paragraph**: an interactive session, a phantom, and — since 15 October 2026 — an
**API session**, which runs it when it first enters an account. Entering another
account with `logto` runs the new account's `LOGIN` only. There is none unless you write
one, so nothing runs by default; a session shows what it is by `@tty` (`apisrvr` for the
API). It runs in the account just entered, **under that account's own switches**: it can do
no more there than the account's users can.

## What is locked: `list.readu`

```
list.readu {user.no} {detail} {wait} {no.page} {lptr {n}}
```

```
:list.readu
There are no active file, read or update locks held by any user
```

That answer is about the **whole system**, not about you. With locks held:

```
User File Path........................... Type Id..............................
  23    1 /home/sd/user_accounts/don/zzlk31a      RU   R1
  19    4 /home/sd/user_accounts/don/voc          RU   zzlock31
  23    1 /home/sd/user_accounts/don/zzlk31a      RL   R2
```

| | |
|---|---|
| **`User`** | the SD user number holding it — `listu` turns that into a person |
| **`File`** | SD's internal file number, and **this is the number `unlock` wants** |
| **`Path`** | wrapped over as many lines as it needs |
| **`Type`** | `RU` update · `RL` read · `FX` exclusive file lock · `SX` shared file lock · `WAIT` a session waiting for one |
| **`Id`** | the record id; blank for a file lock |

A file lock has no id:

```
User File Path........................... Type Id..............................
  23    1 /home/sd/user_accounts/don/zzlk31a      FX
```

### The keywords

**`detail`** prints the record-lock budget above the listing:

```
:list.readu detail
Record lock limit (NUMLOCKS) = 100, Current = 0, Peak = 2
There are no active file, read or update locks held by any user
```

**`Peak` is the one to watch.** `Current` describes this instant, which is
rarely the instant that mattered. A peak near the limit is how you find out
`NUMLOCKS` needs raising **before** a program fails with the lock table full.
`config` reports the configured limit.

**A user number** restricts the listing to one session. **`wait`** adds the
sessions *waiting* for a lock, as `WAIT` rows — left out by default, so the
plain listing shows the cause of a hold-up and not its victims. **Ask for
`wait` when something is stuck.**

### A lock outliving its session

The `19 … RU zzlock31` row above is real, and it is a lock on a record in an
account's `voc` file left behind by a session that was killed while holding it.
**A dead session's locks are not released by its dying**, any more than its
user-table entry is removed, and everything wanting that record waits for a
process that is not there. **They are released when the entry is cleared**,
which is `logout` *n* for a session whose process is gone (see *When a session
will not end*), or the `tool.sessions` page's L key.

**Take the user number to `pstat`.** *(Not responding)* means clear the session
rather than wait for it.

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
> program's object, offset in it in hexadecimal, line), for a program of your own to analyse. openQM's
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
signed on while another was there** (see *Being SDSYS* in *Accounts and Security*). The lower list is every lock — the user, the file number
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
| Tab | change to the other list |
| L (sessions) | `logout` the selected session; the user number is typed again to confirm. For a session whose process is gone the entry is cleared and its locks are released |
| U (locks) | `unlock` the selected lock; the holder is not told |
| I | `inhibit.login on` when logins are allowed, `off` when they are inhibited |
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

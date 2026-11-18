Title: Sessions and Locks
Subtitle: Seeing who is signed in, ending a session that will not end itself, and inspecting or forcing the locks a session holds.

These are the verbs for looking at the machine as a whole and intervening in it:
**whose sessions are running, what they are holding, and how to take either
away.** Every one of them is SDSYS's.

> **This document is separate so that it can be withheld.** It links to
> nothing outside the administrator set. Where a user-set page is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part.

## Two things are not on this page, on purpose

**A programmer needs to understand locks without being able to force one**, so
the *user* documentation keeps the part of the subject that is theirs: what a
task lock is against a database lock, and `release`, which gives back locks your
own session holds and needs no privilege at all. The same goes for `status`,
`phantom`, `pstat`, `pdebug` and `pdump` — a programmer's view of their own
processes.

**This page is the other half**: the verbs that see and act across the machine.

## Who is signed in: `listu`

```
listu {detail} {no.page} {lptr {n}}
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
numbers. **SD has no license count**, so the third number is whatever the system
marks as chargeable.

**`Origin` is blank for a local session and that is not a fault.** It reports
an address or a device name, and a console or piped session has neither. It
reads `Phantom` for a phantom and an IP address for a network client.

`SDNet` is also among the values it can print, and you will not normally see
it. The mark behind it is set in only one place, the API server's request 29,
"open an SDNet file", which is refused unless `NETFILES` has bit 2 set (see
*Configuration*). The SDNet described in this set, where a program opens a file
on another SD server, does not use request 29, so a session that comes from it
shows an address like any other API session.
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

For a session killed from outside with `kill -9` while it held a record lock,
`logout 43` prints the line above, and afterwards `listu` does not list the user
and `list.readu` does not show the lock. The entry matters because **it holds a slot and an exclusive-access
claim**: `NUMUSERS` counts it, and any verb that wants a file to itself —
`build.index` is the usual one — is refused while it is there. So **the way to
clear a dead session is `logout` *n*.**

A session that is **alive and does not answer the signal** is the other case,
and it keeps its entry with **`(logout pending)`** beside it; asking again
signals it again. `sd -cleanup`, run as
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
when the session that took it is killed, without waiting for `sd -cleanup` to remove the dead session's entry.

## The paragraph every session runs first: `MASTER.LOGIN`

A VOC record named `MASTER.LOGIN` in the SDSYS account, if it is a paragraph (its first
line is `PA`), is run **once by every new session, before the account's own `LOGIN`
paragraph**: an interactive session, a phantom and an
**API session**, which runs it when it first enters an account. Entering another
account with `logto` runs the new account's `LOGIN` only, **except when you are the administrator: a `logto` made in an administrator session runs no `LOGIN` paragraph and does not open the home screen, so you land at the prompt and none of the account's own start-up code runs in your session**; `logto sdsys` then brings the same session back to SDSYS, with no need to sign out (a session that did not sign in as `sdsys` is refused it). There is none unless you write
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

**An id is another user's text, and it is shown safely.** Any user may lock a record
whose id holds an escape sequence, and the listing, the deadlock report and `tool.sessions` would have sent that
sequence to **your** terminal, the administrator's. Now a control character, `del`, a byte from 128 to 159 and a
mark character in an id, a path or a user name are each shown as `?`. The same holds for `getlocks()` and
`system(1083)` in a program. The locks themselves are not changed (`unlock` and `release` act on the real id),
and `fileinfo(f, 1039)` still gives a program its own ids exactly.

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
`config` reports the configured limit, see [Configuration](07-sd-admin-configuration.html).

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

## Continued in

[Sessions and Locks: Lock Tracing, Task Locks and the Sessions
Screen](02a-locks-and-the-sessions-screen.html) — lock.tracer, task locks,
unlock and tool.sessions.

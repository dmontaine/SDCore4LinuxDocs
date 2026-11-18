Title: The Master Files: The Group and the Modes
Subtitle: Who is in the group, and what the files must say.

This page continues [run.in](19b-run-in.html).

## Who is in the group, and what the files must say

A write into an account (an edit, a delete or a compile from `tool.entries`, a save in the editor it opens) needs the `sdsys` user in the account's group **and** the account's files writable by that
group. **As delivered both are arranged for a user account** (see below). The state
*is* the Linux group membership, as it is for `ssh` and the API (`sdssh`, `sdapi`); nothing is written
to the register, and there is no row for it in the gate matrix (`tool.gates`).

**`modify.account` *name* `sdsys-on` and `sdsys-off`** (a user account only; a group account has no
group of its own for the `sdsys` user and is refused: it owns the files of a group account, so it needs
nothing):

```
modify.account acme sdsys-on
modify.account acme sdsys-off
```

* **`sdsys-on`** puts the `sdsys` user in the account's group (`sd-elevate sdsys-join`) and then makes
  the account's VOC and dictionaries group-writable (`sd-elevate group-write`). It says `Account acme:
  sdsys-on done. The sdsys user is in the group of the account, so SDSYS can write everything that
  group may write. Sign on again as SDSYS; a session already running does not have it`. **It can be
  said again**: for an account that is already on it runs `group-write` again, which repairs a mode (a
  VOC or dictionary that arrived by `restore.account` or a copy at the operating system level) and
  changes nothing else. The state it prints is read back from `/etc/group`: a read back that does not show the
  wanted state is reported as a failure, never as a success (`Account acme: ... failed, status 2`).
* **`sdsys-off`** takes the user out (`sd-elevate sdsys-leave`) and says `Account acme: sdsys-off
  done`. For an account that is already off it says `acme already had that access; nothing changed`.
  **It does not end a session of SDSYS that is already running** (a process keeps the groups it started
  with), so that session keeps its write access until it ends.
* **A session of SDSYS that began before a join does not have the group either.** `tool.entries` shows
  such an account as **`relog`** in its SDSYS column (not `yes`), and refuses **E**, **N**, **D**, **C** and
  **B** on it at once: `SDSYS cannot write inside acme from this session: the sdsys user joined its group
  sdu_acme after the session began. Sign on again as SDSYS`.
* If the group the register names cannot be used, `sdsys-on` and `sdsys-off` say so and change nothing:
  `Account acme: the members of the group sdu_acme could not be read (status 2); nothing was changed`, or,
  for a group name that is not valid, `Account acme: the account register does not name a valid group for
  it; nothing was changed`.
* The two words conflict only with each other (`modify.account acme sdsys-on sdsys-off` is refused,
  nothing changed) and may be given in a command with other words. Both are audited, in lower case:
  `modify.account sdsys-on account=acme`, and `sd-elevate` writes a line of its own to the system log
  (`journalctl -t sd-elevate`).
* **`create.account` and the installer switch it on** for a new account: the
  installing user's account is delivered on like every other. `sdsys-off` takes it away from one.

**What is expected to stop working when an account is off.** An edit, delete or compile from `tool.entries` into it. So
is **SDSYS writing inside the account in any other way**: `logto` the account and make a file, edit a
program, catalog; an interactive `update.accounts` for it (`update.accounts
all` skips such an account and says so, see [Account maintenance](01a-account-maintenance.html)); `sd -a`*account* from the operating
system. (The installer's own `update.accounts all` runs as root and is not affected.) `create.account`,
`delete.account`, `backup.account`, `restore.account`, and reading the
account (`logto` and a listing, `tool.entries`' lists) are done by the root helper or only read the files, and are expected to
work. Before 2.0-0 that general write was there for every account, because the membership was; switch
the account on for the time SDSYS needs to work inside it.

**A new user account** gets its group `sdu_`*name* from `create.account` with `root` and the user as
members, and `create.account` then puts the `sdsys` user in it (`sd-elevate sdsys-join`; if that fails the
account is still made, and the message says so and names the repair, `modify.account `*name*` sdsys-on`). A **group
account** is made with `root` and `sdsys` in its group `sdg_`*name* and is owned by `sdsys`, so it needs
nothing. **`delete.account` needs nothing**: the group goes with the account.

**The install and every upgrade** make one decision, **once**: they put the `sdsys` user in the group of
every **registered** user account that does not list it - an `sdu_`*name* group whose account the
register holds, with that same group on its record - and make that account's VOC and dictionaries
group-writable at the account's **registered** place (`sd-elevate sdsys-join`, then `group-write`).
**There is no question.** An `sdu_` group that no registered account owns is left alone and named in one
line (`Left alone, no registered SD account owns them: ...`). Each account joined is printed (`the sdsys
user is now in the group sdu_acme`), and then the installer writes the marker `/home/sd/$sdsys.access`,
so that the administrator's later `sdsys-off` or `sdsys-on` stands: with the marker present the installer
does not touch a group. **If a join or a repair the helper was asked to make failed, the install warns
(with the command that repairs it, `modify.account <account> sdsys-on`), goes on, and does not write the
marker**: running the installer again tries again. An account registered **outside**
`/home/sd/user_accounts` and `/home/sd/group_accounts`, with **no path**, or at a path that **does not
exist** is joined but its modes are not repaired (the helper repairs only those two places); it is named,
with the reason, in a warning of its own, and does **not** hold back the marker - set its modes by hand
(`chmod g+rw`, setgid on the directories). The marker is in `/home/sd`, not in the
sdsys directory, because `deletesdcore.sh` removes the sdsys directory in every cycle and would lose it;
`/home/sd` is kept with the accounts and removed with them. (Only groups
named `sdu_`*name* are looked at; `sdusers` and a group account's group never are.)

**Three `sd-elevate` verbs do the work, each confined**, and none is more than `modify.account` and the
install need. Each leaves a line in the system log (`logger -t sd-elevate`) after it has changed
something:

| `sd-elevate` | does | refuses |
|---|---|---|
| `sdsys-join sdu_`*name* | puts the user `sdsys`, **and no other user**, in that group (`usermod -aG`: it adds, it never replaces) | any group that is not `sdu_`*user* of an SD user who exists (not `sdusers`, not a route group, not `sdg_`, not `sdu_root`, not `sdu_sdsys`), a group that does not exist |
| `sdsys-leave sdu_`*name* | takes the user `sdsys`, **and no other user**, out of that group (`gpasswd -d sdsys`: it removes that one membership and no other); a group that does not list `sdsys` is answered `sdsys is not in sdu_`*name* with exit 0 and left as it is | the same groups as `sdsys-join`, and the same user part; the user is written in the helper, never an argument and never taken from the environment |
| `group-write` *account directory* | gives the account's own group write on its VOC and its dictionaries (g+rwx and setgid on the directories, g+rw on the files in them) | an account directory that is not a direct child of `user_accounts` or `group_accounts`, or whose group is not `sdu_`*name* (`sdg_`*name* for a group account): never `sdusers`, which every account is in |

`sdsys-join` and `sdsys-leave` change one membership of one user and nothing else. `group-write` changes modes only, never owners or groups. It works on file descriptors opened
without following links, so a link a user plants in the tree cannot make root change another file;
it changes only what has the account directory's owner (or `sdsys`) and the account's own group,
leaves the other bits as they are, and does not leave the account directory's filesystem. It says
what it did, and a second run changes nothing.

### The modes of what SD makes

Every session in an ordinary account starts with a `umask` of 002 (022 in the SDSYS account), so a VOC or a dictionary made in the ordinary way is
already group-writable (664 files, 775 directories). A user who changes the umask (the `umask`
verb) would make them closed, so **SD gives a VOC or a dictionary that it has just made its group's
write bit, whatever the umask**: the directory g+rwx and setgid, `%0` and `%1` g+rw. It does so
**only where the account's own directory lets that group write** (if the directory is 755, nothing
is added: a group that cannot write the account directory is not given the VOC), **and only where
the `sdsys` user is in that group** (from 2.0-0: where the account is off, group
write on a new VOC or dictionary would serve nobody, and nothing is forced), only to what the
session itself has just made, and it adds group bits and takes nothing away. The data file next to
a dictionary is not touched. A VOC or dictionary that arrives some other way (`restore.account`, a
copy at the operating system level) keeps the modes it came with: `modify.account` *name* `sdsys-on` (`sd-elevate
group-write`) puts them right, the ones made while the account was off included.

## Accounts being made, restored and deleted

* **`create.account`** makes the group of a user account with `root` and the user in it and then puts
  the `sdsys` user in it (above), so the administrator's edits reach the new account at once.
* **`restore.account`** replaces an account's files at the operating system level and does not change
  their modes: a VOC or dictionary that the archive did not keep group-writable is put right by
  `modify.account` *name* `sdsys-on` (`sd-elevate group-write`).
* **`delete.account`** needs nothing: the group goes with the account.
* **`update.accounts`**, like every other writer, needs nothing more.

## What it does not do

* **It is not a wall against a stolen `sdsys` login.** See "Read this first" above.
* **It does not change what a pointer points at from another account.** A pointer record is the
  account's own record and is edited like any other; its target is edited in the account it lives
  in, SDSYS's included.
* **It does not remove a catalog entry when it deletes a program.** The entry is the account's;
  `run.in` *account* `delete.catalog` or `decatalog` removes it.
* **It does not see a change made outside SD** any differently from SD itself: the page reads the
  accounts' files when it is asked to, so a shell command's change is simply there at the next read.
* **On a machine with one operating-system user there is nothing for the membership to separate.**
  The rule rests on ownership and groups: the group membership and its two verbs, the modes, root
  changing only the account's own files, and the refusal of a write into an account that is off.

## What went with the copies

SD keeps **no copies** in the SDSYS account, because `tool.entries` edits the real records. A
system that had them (a development build) loses:

* the files `voc_master`, `dict_master`, `master_state` (each with its dictionary) and the journal
  `$master.journal` in the SDSYS directory. **The installer removes any of them it still finds**,
  by their exact names (a link among them is removed as a link, and what it points at is left), and
  says how many it removed. An upgrade (`deletesdcore.sh`, then the installer) starts from an empty
  SDSYS directory, so there is normally nothing to remove.
* the verbs **`sync.masters`**, **`check.masters`** and **`list.master.pending`** and the page
  **`tool.masters`**. They are on the VOC deletion list, so the next update of the SDSYS account
  (`update.accounts`, or the sign-on update) takes them out of an old VOC, keeping a copy:
  `list.voc.removed` shows them and `restore.voc` can put one back (it would find no program to run).
  **Use `tool.entries` instead.** The Master files tile of the administrator's home screen opens it.
* the kernel's hook, which noted every write of a VOC or dictionary record for the copies (it cost a
  test on every write), kernel key 150 (`K$MASTERS`) and the status 8910 of a refused save. The key
  and the status are not given to anything else.
* the scheduled-job ids `check-masters` and `sync-masters` of `sd-elevate job-set`, which ran the two
  verbs; `backup-all` and `update-accounts` are left. A job defined with one of the old ids is listed
  as damaged by `sd-elevate job-list`; `sd-elevate job-delete` removes it.

What did **not** go: the `sdsys` user's membership of the account groups and its two verbs, the group
write of a new VOC or dictionary, `run.in`, and the edit gates.

Title: Accounts and Security: The Shared Account and the Files-only Route
Subtitle: shared-read and shared-write, files-on and files-off.

This page continues [Accounts and Security: The Edit Switches and the NET
Switch](01-accounts-and-security-3-edit-switches.html).

### The shared account: `shared-read-on`, `shared-read-off`, `shared-write-on` and `shared-write-off`

The installer makes one group account, named `shared`, and **the files in it can be
opened by every account by file name** — `open "inventory"` in any account finds
the file `shared` holds under that name, with no `logto` and no pointer in the
account's own VOC. Two per-account switches, in fields 13 and 14 of the register
record, decide who may. The full description, with the order of the checks and the
cautions, is its own page: [The shared account](13-the-shared-account.html).

| switch | delivered | words | what it allows |
|---|---|---|---|
| `shared.read` | **on, for every account** | `shared-read-off` / `shared-read-on` | opening the files of `shared` by name, and reading them |
| `shared.write` | off | `shared-write-on` / `shared-write-off` | saving, deleting and clearing records in them (a dictionary needs `dict-on` as well) |

**`shared.read` is the one switch in SD whose blank means ON.** It is only off when
the field says `no`: `shared-read-off` writes `no`, and `shared-read-on` writes
`yes`. A blank field — a new group or other account, and every account that
existed before the switch did — reads as on, so **nothing is withdrawn from an
existing account, and nothing needs to be run at an upgrade.** `shared.write` is
the other way: only `yes` is on. **Anything you place in `shared` can be read by
every account you have not taken the right from**, so put nothing there that is not
meant for everyone, and take the right from the accounts that should not have it
before you fill the account.

```
:modify.account fred shared-read-off
Account fred has shared.read no, shared.write no
:modify.account fred shared-write-on
Account fred has shared.read no, shared.write yes
```

`modify.account` *name* `shared-read-on` / `shared-read-off` / `shared-write-on` /
`shared-write-off` change one switch each and say where the account now stands,
both switches in one line. `create.account user` takes `shared-read-off` and
`shared-write-on` (the other two would only restate the delivered state), and so
do `group` and `other`. Asking for what is already so changes nothing and says so.
Each change is written to the audit trail (`modify.account shared-read-off
account=fred`). A switch may be set on a group or other account, as `net-on` may;
**SDSYS is never a target**.

**It belongs to the account the person is in, like `net-on`:** it is read at
sign-on, again at `logto` into another account, and given back when `logto`
returns, and the API server reads it at every entry. `shared.read` is read when a
file is *opened*, so a file already open stays usable after you withdraw it,
until the person's next entry; `shared.write` is tested at every write.

**How SDSYS puts files in `shared`.** Sign on as SDSYS, `logto shared`, and make
files as in any account: `create.file`, `copy`, programs that write. The account's
directory, `/home/sd/group_accounts/shared`, belongs to `sdsys` with the group
`sdusers` (mode 2775, files 664), so every SD user's own process can read the
files through the kernel, and write them when it has `shared.write`. **Only SDSYS
enters `shared`**: its Linux group is `sdg_shared`, whose members are `root` and
`sdsys`, not `sdusers`, so `logto shared`, a Q-pointer to it and `sd -Ashared` are
refused to everybody else. That is what makes taking `shared.read` away a real
wall for an account that has neither `sh` nor `os`.

**A maintainer who is not SDSYS** is made of two things: membership of the group,
`modify.account shared add` *name* (the Linux user can then `logto shared` and
sign on to it directly), and `shared-write-on` **on the account named `shared`**,
which lets those members write records there. Neither lets a maintainer change the
*structure* of a file — see the page for that. The switches on the account `shared`
decide what its members can do inside it; a blank means write off.

**What it does not do.** The verbs, sentences and programs of `shared` are not
shared; only data files and their dictionaries are. The administrator's own `open`
does not follow `shared` (reach it with `logto shared`). `shared` is not copied to
other servers. The name is reserved: `create.account` refuses it, and
`delete.account shared` is refused.

**Upgrading.** The installer makes `shared` when it is run, and keeps it when the
accounts are kept. **It stops before it changes anything if an account named
`shared` already exists that is not its own**, and names the register record: rename
that account by hand and run the installer again. Removing SD together with its
accounts removes the Linux group `sdg_shared` too; keeping the accounts keeps it.

### The files-only route: `files-on` and `files-off`

There are **two API routes, and the second is narrower.** `api` (the Linux
group `sdapi`) lets a person do everything the API offers: execute commands, call
cataloged subroutines, enter other accounts with `logto`, read and write
sequential files, and work with files. **`files-on` (the Linux group `sdfiles`)
lets a person log in over the API and do files and nothing else.** It exists so
that a login kept for SDNet (see [SDNet](12-sdnet.html)) never needs `sdapi`: the
other server's administrator gives that login `sdfiles`, and whoever steals the
stored login can open and read files on that server and cannot run a command
there. **Changing files there is a further permission, `files-write-on` (the Linux
group `sdfileswrite`)**, given separately and off for a new account (below, *Changing files: `files-write-on`*), and **administering them there - configure, index, create and delete a file, the file's counter - is a third, `files-admin-on` (the Linux group `sdfilesadmin`)**, off for every account (below, *Administering files: `files-admin-on`*).

**Off for a new account, like every other door.** `create.account user` takes
`files-on`, `files-write-on` and `files-admin-on` (each needs the one before it: `files-write-on`
needs `files-on`, and `files-admin-on` needs both); `modify.account` *name* `files-on` / `files-off`,
`files-write-on` / `files-write-off` and `files-admin-on` / `files-admin-off` turn them on and off.
Membership of the group *is* the route, as membership of `sdapi` is for `api`, so
there is no field for it in the register. After a change SD says where the account
stands, **read back from the operating system's group file** rather than taken from
the request, in a line of its own:

```
:modify.account fred files-on
Account fred has files yes
:modify.account fred files-off
Account fred has files no
```

(SD writes a keyword it prints in lower case.)

Asking for what is already so changes nothing and says so ("fred already had that
access; nothing changed"). The change is made by the same privileged helper as the
`api` word (`sudo /usr/local/sbin/sd-elevate addgroup` or `delgroup`, with the
group `sdfiles`), and written to the audit trail (`modify.account files-on
account=fred`). If the group file does not show the state asked for afterwards, SD
reports the failure ("Unable to change remote access for fred, status: 2") and not
a success.

**The rules, in the order the login applies them.** The API server decides at the
end of the login, after the password has been proved:

1. The person must be in `sdusers`, as for every route.
2. A member of **`sdapi` has the whole API, whether or not they are also in
   `sdfiles`: `sdapi` wins.**
3. Otherwise a member of **`sdfiles`** is let in **files only**. The session is
   marked once, at login, and the mark is never cleared for the life of the
   connection.
4. A person in **neither** group is refused exactly as before: "*name* is not
   permitted to use the API", with the reason `not a member of sdapi or sdfiles` in the
   audit trail (the decision is made on both groups). If the group file cannot be read the login is refused,
   not guessed, with a reason of its own.
5. `sdsys` is exempt from both groups by name and keeps the doors it has always
   had; it is never made files-only.

**What a files-only session may ask for.** One function, `!apifilesok`, decides, and
it is an *allow list*: a request number that is not in it is refused, including a
number this release has never heard of.

| allowed | request |
|---|---|
| 1, 2 | quit; get the text of the last error |
| **3, once** | set the account. The first one, which is the entry to an account after login, is allowed; a later one would be a `logto` and is refused |
| 4, 5 | open a file; close it |
| 6 | read |
| 7 to 10 | the locking reads (`readl`, `readlw`, `readu`, `readuw`): **only with `files-write-on`** |
| 11 to 15 | select; read the next id; clear a select list; read a saved list; release a lock |
| 16 to 19 | write; write and keep the lock; delete; delete and keep the lock: **only with `files-write-on`** |
| 26 | select on an index. Allowed because it is a select, with 37 to 39 |
| 30 to 34 | lock a record; clear a file; lock and unlock a file; ask whether a record is locked (34: the answer names the holder by his user number on this server): **only with `files-write-on`** |
| 35, 36 | list the indices |
| 37 to 39 | select a list; select by an index value; select by an index key |
| 40, 41 | file information; read one field (a `readv` that takes a lock is a change and needs `files-write-on`) |
| 42 to 45 | set the left or right end of an index range (`setleft`, `setright`), and select within it (`selectleft`, `selectright`) |
| 46 | the mark mapping |
| 49 | the server's revision |
| 68, 69 | `write` and `writeu ... creating.seqkey` (the file's own counter gives the id): **only with `files-write-on` and `files-admin-on`** |
| 70 | a verb run on this server for the login (`analyze.file`, `configure.file`, `create.index`, `build.index`, `delete.index`, `disable.index`, `create.file`, `delete.file`): **only with `files-write-on` and `files-admin-on`** |
| 71 | `fcontrol`: **only with `files-write-on` and `files-admin-on`** |

| refused | request |
|---|---|
| 20 | call a cataloged subroutine |
| 21, 22, 23 | execute a command; respond to its prompt; end it |
| 24, 25 | the other logins |
| 27, 28 | enter and exit a licensed package (not supported by any route) |
| 29 | open a file on another SDNet server |
| 47, 48 | the SCRAM login itself, which is only possible before the session is logged in |
| 50, 51 | read a variable; `system()` |
| 52, 53 | `trans()` |
| 54 | transactions |
| 55 to 60 | evaluate and the conversions |
| 61 to 67 | sequential files |
| 0, 72 and above, anything else | no such request here |

A refused request is answered with "This login is for files only: request *n* is not
allowed" (a change or lock without the write group: "This login cannot change or lock
files here: ask the administrator for files-write-on (request *n*)"), **the request is not
carried out**, and a line goes to the audit trail (`api refused request=16 route=sdfiles
write=off admin=off user=fred`; a login by this route is `api login route=sdfiles write=on
admin=off user=fred`, with `admin=on` for a person in `sdfilesadmin`). The connection stays
open, so a client that asks for something it should not can carry on with files.

**What is not changed.** Everything else about the session applies as it does to any
other: the account must be entered, the account's own switches (the OS-access
gate, the three edit switches, the NET switch) are loaded and enforced, `SDCLIENT` in
`sd.conf` still decides whether a client may open the files it names, and the
API listener must be on (`remote.api`). **`sdfiles` alone is a read-only route**: the
numbers marked above are refused unless the person is also in `sdfileswrite`.

## Continued in

[Accounts and Security: File Writing, the AI and VOC
Pointers](01-accounts-and-security-5-files-write-ai-pointers.html) — the files
write and admin switches, the AI switch, VOC pointers and the cost of os-on.

Title: The Shared Account
Subtitle: Files that every account can open by name, without logto or a pointer: how they are found, who may change them, and what it does not protect.

The installer makes one group account named **`shared`**. **The data files in it can be opened by
every account by file name**: `open "inventory"` in any account finds the file `shared` holds
under that name, when the account has no entry of its own for it. There is no `logto` and no
pointer to make in the account's VOC, and `list`, `sort`, `select`, `count` and a BASIC program's
`open` all find it the same way.

> **Anything in `shared` can be read by every account that has `shared.read`, and `shared.read`
> is ON for every account until you turn it off.** It is the one switch in SD whose blank means
> on. Put nothing in `shared` that is not meant for everyone, and take the right away
> (`modify.account` *name* `shared-read-off`) from an account that should not have it **before**
> you fill the account. Writing is the other way: it is off until you turn it on.

The switches, the words and the upgrade rule are in
[Accounts and Security](01-accounts-and-security.html#the-shared-account-shared-read-on-shared-read-off-shared-write-on-and-shared-write-off).
This page is the full description.

## What it is, on disk

| | |
|---|---|
| the account | a group account named `shared`; its register record is `accounts/shared` in the SDSYS directory |
| its directory | `/home/sd/group_accounts/shared`, owner `sdsys`, group `sdusers`, mode 2775, files 664 |
| its Linux group | **`sdg_shared`**, whose members are `root` and `sdsys` and nobody else |
| the register's group field | `sdg_shared` |

**Why the group is not `sdusers`.** Signing on to an account, `logto`, a Q-pointer and
`sd -A`*name* all admit exactly the members of the register's group. If that were `sdusers`,
every SD user could `logto shared` and write there whatever `shared.write` said, and
taking `shared.read` away would stop nothing. With `sdg_shared` only SDSYS enters `shared`;
everybody else reaches its files only through the lookup below, which is what the two switches
control. The files themselves belong to `sdusers` so that every SD user's own process can read
them through the kernel and, with `shared.write`, write them.

SDSYS puts files in `shared` the way it works in any account: `logto shared`, then
`create.file`, `copy`, a program that writes, and so on. Making and changing the *structure* of a
file is SDSYS's alone (below).

**The name is reserved.** `create.account` refuses it, with or without a type
("The account name shared is reserved for the shared account, which the installer makes"), and
`delete.account shared` is refused ("The shared account cannot be deleted"). The installer
makes the account with a one-time marker that it removes whatever happens. If an account named
`shared` already exists when the installer is run and is not SD's own (its register record does
not say `/home/sd/group_accounts/shared` on line 1 and `sdg_shared` on line 3), **the install stops
before it changes anything** and names the record; rename that account by hand and run the
installer again.

## How a name is found

An `open` of a name looks, in this order, at:

1. **The account's own VOC.** Its entry, however the case is typed, always wins. So do the
   `PATH:` and *account*`:`*file* forms. Nothing about `shared` is looked at when the account has
   its own entry.
2. **Whether the lookup applies at all.** Only an `open` follows `shared` — a file `open`
   (data, or `open dict`). `openseq`, `deleteseq` and `call "file prog"` never do. The
   session must not be the local administrator and must have `shared.read` on.
3. **The shape of the name.** 1 to 63 characters; the first a letter or a digit, the rest letters,
   digits or one of `. _ - $`. **A name that begins with `$ & ! * _` or `%` is never looked
   up**, which keeps `$savedlists`, `$hold` and every `&...&` file each account's own.
4. **The standard VOC.** A name that is in the standard VOC (`syscom`, `$acc` and the like) is never
   looked up.
5. **The register record of `shared`.** It must exist, must not be suspended, and must hold an
   absolute path. A suspended or missing `shared` shares nothing.
6. **`shared`'s own VOC.** It must hold the name as an **F** entry (a file pointer); a value in
   its field 4 is ignored. Q, N, V, K, X and every other kind of entry are never followed.
7. **The pathname field** of that entry (the dictionary's field for `open dict`): no `@` token,
   and a relative name is taken from `shared`'s directory.
8. **The kernel's test of the path.** The file must exist and lie strictly *inside* `shared`'s
   directory, and no part of the path below the directory may be a VOC, a program file
   (`bp`, `bp.out`, `*.bp`, `*.bp.out`), a dictionary (except the one asked for) or
   `shared`'s private catalogue. A pointer in `shared`'s VOC to a file anywhere else is refused.
9. **The audit line**, once for each name in a session, after the name has been accepted.

A refusal at any step is not a message: the name is simply not there, and the `open` takes its
`else` branch as it would for any missing file. Files are locked exactly as in any account, so two
accounts opening the same shared file see each other's record locks.

### What is not shared

The **VOC, verbs, sentences, paragraphs, catalogue and programs of `shared` are never reached from
another account.** Only data files, and their dictionaries, are shared. A program kept in `shared`
is not run from another account by name, and `shared`'s `voc` and `bp` cannot be opened as data by
any name. The administrator's own `open` does not follow `shared` either: SDSYS reaches the files with
`logto shared`.

## Who may do what

| the session | read by name | save, delete or clear records | write a dictionary | change the structure |
|---|---|---|---|---|
| an account with `shared.read` on (the default) | yes | no — refused | no | no |
| `shared.read` and `shared.write` on | yes | yes | only if `dict-on` too | no |
| `shared.read` off | not found | — | — | no |
| the local SDSYS session (`logto shared`) | — | yes | yes | **yes** |
| SDSYS over the API | yes | yes | yes | no |
| a member of `sdg_shared`, in `logto shared` | — | only if the account `shared` has `shared-write-on` | likewise | no |

* **A record write** — `write`, `writev`, `matwrite`, `delete`, `clearfile`, and the verbs that save
  into a file the user names (`copy ... to`, `ed`, `save.list` and the rest) — needs
  `shared.write`. Without it SD says "A file in the shared account can only be changed by an account
  that has shared.write (SDSYS can give it: modify.account *account* shared-write-on)".
* **A shared dictionary** needs `shared.write` **and** the sign-on account's `dict-on`. A write
  with `dict-on` and without `shared.write` is refused for `shared.write`; with `shared.write` and
  without `dict-on`, for the dictionary.
* **Structure** means making a file by pathname inside `shared`, `clear.file`,
  `configure.file`, `create.index`, `build.index`, `delete.index`, `set.trigger`, the setters of
  `fcontrol`, resizing, renaming and deleting a file or directory. It is refused to everyone who is not the
  local SDSYS session, **for a program marked internal as well, whatever switches the account has**:
  "The structure of a file in the shared account (making, clearing, configuring, indexing,
  triggers, renaming or deleting it) can only be changed by SDSYS, signed on at a terminal".
  Writing a record to an indexed shared file by someone who has `shared.write` still keeps the index.
* **A maintainer who is not SDSYS** is a member of `sdg_shared` (`modify.account shared add`
  *name*) on an account where `shared-write-on` has been given to the account **`shared`** itself.
  Inside `logto shared` the switches are the account `shared`'s own record; a blank means write
  off. A maintainer changes records, never structure.
* **The local administrator** is never refused a record write or a structure change, and is not
  given the by-name lookup (it uses `logto shared`).
* **`basic`** writes an object file by name, so compiling a source that lies in `shared` needs the
  rights to write there; without `shared.write` the compile is refused and nothing is written.

## The audit trail

The first time a session opens each shared name, one line is written, in lower case:

```
shared open file=inventory
```

A second open of the same name in the session writes nothing, and a refused name writes nothing.
The administrator's words are the usual `modify.account shared-read-off account=fred` and its
siblings. Refusals are not audited.

## `list.shared`

```
list.shared
```

`list.shared` lists, one to a line, the names of the files of `shared` that an account with
`shared.read` can open by name, then a count: "Files of the shared account that can be opened by
name: 3". A name is listed only if the lookup above would accept it. It changes nothing and writes no
audit line. It is in SDSYS's set, not in an ordinary account's VOC; if it is put in one, an account
with `shared.read` off is told "Account *name* has shared.read off, so it cannot open the files of
the shared account by name" and sees nothing. When there is no `shared` account in service, or it
is suspended, it says "There is no shared account in service". Run by SDSYS it shows what accounts
with the right can reach (SDSYS's own `open` does not follow `shared`).

## Cautions

1. **Every account with `shared.read` can read everything the lookup reaches.** A file is open to
   all as soon as it has an **F** entry in `shared`'s VOC. A file in the directory with no entry
   in the VOC is not found by name.
2. **An SD program marked internal that opens a file by name could be handed a shared file in
   the place of the account's own** (SD's own internal programs open system files such as
   `$savedlists` and `$hold` by name, on behalf of the account that ran them). That is the confused-deputy case, and it is why a name
   that begins with a symbol, and every name in the standard VOC, is never looked up: a file
   in `shared` called `$hold` would not be found. A name that begins with a letter or a digit
   is a name any account may open, so choose the names in `shared`'s VOC knowing that.
3. **A plain `list` still writes the compiled form of a new I-type into the dictionary it reads.**
   That is an SD program writing on the account's behalf, and it is let through on a shared dictionary
   for an account without `shared.write`. The data is not touched.
4. **An account with `sh-on` or `os-on` reaches the files at the operating-system level.** The files
   belong to `sdusers`, so a shell can read them, and with `shared.read` off that account still can; the
   switch is a wall for an account that has neither of the two, not for one that does.
5. **Withdrawal takes effect at the person's next entry.** `shared.read` is tested when a file
   is opened: a file already open stays usable until the person signs off or enters another
   account. `shared.write` is tested at every write.
6. **SDSYS over the API can write records in `shared` but cannot change its structure.** An API
   session of `sdsys` has no administrator flag, so it follows `shared` (both switches are on for
   it) and cannot make a structure change. Structure changes are made at a local `sdsys` terminal.

## What is not done

* `shared` is not replicated to other servers.
* The programs of `shared` are not shared: there is no catalogue of shared programs.
* Every `open` that misses the account's own VOC for an ordinary lower-case name now reads the
  register and `shared`'s VOC to see; nothing caches a miss yet. Names that begin with a symbol and
  the standard names never reach the disk.
* SD Core Solo has one account, and does not have this.

## See also

[Accounts and Security](01-accounts-and-security.html) for the switches, the words and the report
lines beside the other per-account switches, and for the audit trail. [SDNet](12-sdnet.html) for files on
other SD servers, which use a pointer of their own.

Title: The Installed Scripts
Subtitle: The three helper scripts installed beside SD, the sudoers scope that lets SD run them, and what their exit codes mean.

**Unlike SD Core for Windows, which ships thirty-seven separate PowerShell
scripts, this port does its privileged work through three: one general
helper with many subcommands, and two standalone ones.** Where Windows
needed a script per task because each ran as its own elevated PowerShell
process, this port dispatches by argument through a single `sudo`-scoped
entry point — the same shape of problem, a smaller surface because the
mechanism is free to differ.

They are in `/usr/local/sbin`, and they are there for the same two reasons
Windows's are: so that a step which failed during the installation can be
run again without reinstalling, and so that a choice made at install time
can be changed afterward.

**They are shell scripts, not SD verbs.** Nothing here is typed at an `sd`
prompt. Most need `sudo` to do anything; SD itself reaches them through a
scoped `sudoers` entry that lets `sdusers` run exactly the subcommands
each operation needs, nothing more.

*Italics* mark something you supply, **bold** a word typed as it stands, and
braces an optional part.

## What is here and what is not

**Three scripts ship.** Nothing else from the source tree's `gplbld`
directory is installed. If you find a script named in the source and cannot
find it on an installed machine, that is why.

## Exit codes

| | |
|---|---|
| **0** | done. That includes *"it was already done"* — most subcommands are written to be run twice |
| **2** | **refused.** The line above names why — `die()`'s own convention, printed as `sd-elevate: REFUSED - <reason>` |
| **3** | (`remote-ssh` only) **nothing was there to change.** The firewall would not have gated anything anyway (no `ufw` or firewalld, inactive, or already permissive), so reporting success would be the reassuring falsehood this project's own instrument rule refuses to print |

**There is no exit 1.** A refusal and a failure are the same event here —
`die()` is the one way this script stops short of doing what it was asked,
and it always means 2.

## `sd-elevate`

```sh
sudo /usr/local/sbin/sd-elevate [--dry-run] <subcommand> ...
```

**`--dry-run` reports what it would do and changes nothing** — the
argument, and it comes first.

| Subcommand | Does |
|---|---|
| `useradd`, `userdel`, `userdel-home` | create or remove the Linux user behind an account — `useradd` gives every user it makes the comment `SD account`, and **`userdel` and `userdel-home` act only on a user that carries it** (from 1.2-0; `userdel` used to take any user above the system range). `userdel-home` also removes its home directory. A login that was there before SD, the machine's own administrator included, is out of reach |
| `passwd`, `setpw` | the Linux login password — `setpw` takes it on stdin, one line, never as an argument. **Only for a user that carries the `SD account` comment** (from 1.2-0): the password of anyone else is theirs and the machine administrator's. `setpw` is what `create.account` calls for the user it has just made, and **it sets a first password only**: a user whose `/etc/shadow` entry already holds a password (anything but empty, `*`, `!`, `!!` or `!*`) is refused with `already has a Linux password`, so it can never reset one. Nothing calls `passwd` |
| `pw-check` | judges a password against SD's own complexity rule, on stdin — used before the write, not only at it |
| `groupadd`, `groupdel`, `addgroup`, `delgroup` | the account's own `sdu_`/`sdg_` group, and membership in it — this is what `modify.account add`/`delete` calls underneath. From 1.2-0 `groupadd sdu_`*user* makes the group only for an SD user that exists and puts only `root` and that user in it (the `sdsys` user joins an account's group through `sdsys-join` and nothing else). **`addgroup` is not narrowed:** `modify.account` *name* `add` *person* puts a person in the group of someone else's account, which is the grant, so the verb takes any SD user and any SD group |
| `setgid`, `chown-account` | ownership and the setgid bit on an account directory, at creation. `chown-account sdsys` (the shape for a **group** account's files) takes only paths inside `group_accounts/`*name* and only that account's own group, `sdg_`*name* (`sdusers` for `shared`); from 1.2-0 it refuses a user account's directory, `voc` and `%0`. The shape for a person's own account (`chown-account` *user* `sdu_`*user*) is as it was. The shape for an **other** account (`chown-account root sdusers`, which `create.account other` uses for the path you name, anywhere) takes, from 1.2-0, only a directory or a plain file that **the `sdsys` user owns** — what `create.account` has just made — and a real run chowns through the file it has opened without following a link and found to be `sdsys`'s; `/etc/shadow`, `/etc/passwd`, `/etc/sudoers.d/*` and `/etc/ssh/*` belong to root and are refused (`belongs to uid 0, not to the user sdsys`), where it used to take any path that existed |
| `restore-place` *owner* *group* *staged* *account* | puts a restored tree in the place of an account, as root, and gives it to its owner. The staged tree must be exactly `.sdrestore.`*n*`/accounts/`*name* and the target exactly `user_accounts/`*name* or `group_accounts/`*name*; a user account goes back to its own user and `sdu_`*user*, a group account to `sdsys` and `sdg_`*name* (from 1.2-0 only its own name's group). **It still moves a tree that `sdsys` staged itself** (`sd-accarchive extract` runs without root), so a restore is the administrator's act on an archive the administrator vouches for; that is not narrowed |
| `akpath-set` *data path* *index path* | sets the relocated index directory of a restored hashed file (what `restore.account` calls). It runs `sdidx` as root, so from 1.2-0 the data path must be a hashed file's directory — one that holds a plain `%0` with no second link — and the index path an existing directory, both in one account |
| `rmtree-account` | removes an account's directory tree, for `delete.account remove.home` |
| `sdsys-join sdu_`*user* | puts the `sdsys` user, and no other, in an SD user's account group, so that SDSYS can save a master record into the account's files — see [The master files](19-the-master-files.html). What `modify.account` *name* `sdsys-on` calls; nothing runs it on its own. Refuses every other group (`sdusers`, the route groups, `sdg_`, `sdu_root`, `sdu_sdsys`) and a group that does not exist |
| `sdsys-leave sdu_`*user* | takes the `sdsys` user, and no other, out of an SD user's account group (`gpasswd -d sdsys`): what `modify.account` *name* `sdsys-off` and the installer's one-time ruling call. A group that does not list `sdsys` is left alone (`sdsys is not in sdu_`*user*, exit 0). Refuses the same groups as `sdsys-join` |
| `group-write` *account directory* | gives the account's own group write on the VOC and dictionaries of that one account — only where the account directory's group is its own (`sdu_`*name*, or `sdg_`*name* for a group account), never `sdusers`; modes only, links not followed. Called by `modify.account` *name* `sdsys-on` (the installer no longer calls it). `sdsys-join`, `sdsys-leave` and `group-write` write a line to the system log (`logger -t sd-elevate`) when they have changed something |
| `remote-api on \| local \| off \| show` | the `sdclient.socket` binding and the firewall rule (`ufw` or firewalld) — what `remote.api` calls |
| `remote-ssh on \| off \| show` | the firewall rule for port 22 (`ufw` or firewalld) — what `remote.ssh` calls |
| `cred-own query \| verify \| set` | an ordinary account's own write to `$cred`, which it cannot reach directly — what self-service `modify.password` calls |

**Each subcommand re-derives whether the request is legal itself** — whose
account directory it actually is, whether a user was one SD created —
rather than trusting what the calling SD session claims. That is the whole
of the protection: a session that could talk `sd-elevate` into an
operation on somebody else's account would defeat every gate SD has above
it.

**What the 1.2-0 narrowing is, and is not.** The `sdsys` user may run this
script with any arguments, so each verb is a wall only as far as its own checks
go. In 1.2-0 the verbs above that reached further than their callers send
(`chown-account` for a group account's files and for an other account's path,
`userdel`, `passwd`, `setpw`, `groupadd` of an `sdu_` group, `restore-place`'s
group, `akpath-set`'s paths) were narrowed to what the callers send. The
helper also now sets its own `PATH` (`/usr/sbin:/usr/bin:/sbin:/bin`), runs the
python it uses in isolated mode (so a file of that name left in the caller's
current directory is not imported), and reads the test settings `SD_ACCT_ROOT`,
`SD_ACCARCHIVE` and `SD_SOCKET_UNIT` from the environment only on a `--dry-run`
or in a process that is not root, so a root run through `sudo` takes none of
those settings from the caller (sudo's own `secure_path` and `env_reset` already
did most of that on Debian, Ubuntu and Fedora). Two limits of what was built:
`chown-account root sdusers` still lets the `sdsys` user turn any file or
directory it owns into one owned by `root` and the group `sdusers` (the mode is
unchanged and the kernel clears the setuid bit; a handle it opened for writing
beforehand stays writable), which is much narrower than any path on the machine
but is not nothing; and the group-account verbs look for the directory named
`group_accounts` literally, so a `GRPDIR` set to another name under `/home/sd`
is refused by them. This narrows route R-C
of [The master files](19-the-master-files.html) — what the grant of `sd-elevate`
to `sdsys` can reach — and leaves the global catalogue (route R-B) and whatever
else `sdsys` can do with the helper's other verbs and sudo's other rules as they
were, so it is a narrower grant and not a wall against a stolen `sdsys` login.

## `ssh-forcecommand`

```sh
sudo /usr/local/sbin/ssh-forcecommand --install
sudo /usr/local/sbin/ssh-forcecommand --remove
sudo /usr/local/sbin/ssh-forcecommand --check
```

Writes or removes the fenced `ForceCommand`/`DenyUsers` block in
`/etc/ssh/sshd_config` — see [Remote access and the
machine](05-remote-access-and-the-machine.html). `--install` validates the
candidate with `sshd -t` **before** touching the live file, backs up to
`sshd_config.before-sd`, and refuses rather than overwrite a
`sshd_config` that already has its own `AllowGroups`/`AllowUsers`/
`DenyGroups`/`DenyUsers` line — that is somebody else's decision. The
installer runs `--install` non-fatally; a refusal here leaves SD
installed and working, with the boundary not yet applied, and prints
the command to apply it once the conflict is resolved.

**The `sdai` user (added 21 October 2026).** The installer also makes a system user,
`sdai`, with its own group, no login shell, no home directory and no SD group, for the
model call that SD will make itself in a later release; nothing runs as it yet and it
holds no key. A full delete removes it with the route groups and keeps it when the
accounts are kept. There is **no MCP door at the server**: an AI agent uses the command
line over ssh, and people use the full screen programs. (A group `sdagent` and an ssh
arm for such a door were built and pushed earlier on 21 October and taken out again the
same day; no release carried them.)

## `sd-reconcile-accounts`

```sh
sudo /usr/local/sbin/sd-reconcile-accounts          report, change nothing
sudo /usr/local/sbin/sd-reconcile-accounts --sweep  remove them
```

**Finds `accounts` records whose Linux user is gone** — removed from
outside SD entirely (`userdel`, a decommission script), so SD was never
consulted and the record outlived the user. `list sd.accounts` then
answers wrongly, and `create.account` refuses to recreate the name: true
of the record, false of the machine. Reports by default; `--sweep`
removes the stale records and their directories, and needs root. Exit
**0** the register is clean, **1** something stale is still there
(reported, refused, or would not go), **2** the question could not be
answered. Not run by the installer — a recovery tool for drift that
happened outside SD's own verbs.

## Continued in

[The Scripts SD Runs For Itself](09a-scripts-sd-runs-itself.html) — what
the daemon, the verbs and the installer invoke while running, rather than
what an administrator runs by hand.

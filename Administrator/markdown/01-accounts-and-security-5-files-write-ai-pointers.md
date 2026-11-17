Title: Accounts and Security: File Writing, the AI and VOC Pointers
Subtitle: files-write-on, files-admin-on, ai-on, where a file pointer may lead, and what os-on costs.

This page continues [Accounts and Security: The Shared Account and the
Files-only Route](01-accounts-and-security-4-shared-and-files-only.html).

### Changing files: `files-write-on` and `files-write-off`

A files-only login may write, delete, lock and clear **only if the person is also in
the Linux group `sdfileswrite`**, which the administrator of that server gives with
`modify.account` *name* `files-write-on` (or `files-write-on` after `files-on` in
`create.account user`) and takes away with `files-write-off`. It is off for a new
account. The line SD prints after a change is read back from the group file, as for
`files-on`:

```
:modify.account fred files-write-on
Account fred has files-write yes
```

`files-write-on` for a person who is not in `sdfiles` is refused ("Account fred does
not have files access, so it cannot be given files-write: use files-on first"), because
the group on its own gives nothing; `files-off` takes the person out of both groups.
**`files-off` takes the write group away first, then `sdfiles`, and reads each back**, and it
does the work for a person who is in only one of them. A person who is in `sdfileswrite`
and not in `sdfiles` (a removal that stopped half way, or a change made by hand) used to be
told "fred already had that access; nothing changed" and kept the membership, which the next
`files-on` turned into write access nobody had given; that case is now cleaned up, with the
line `Account fred has files-write no` before `Account fred has files no`. If a removal fails
SD says so and stops: a failure of the write group's removal leaves the person as they were, and
a failure of the second removal leaves them in `sdfiles` alone, read access and never write
without read. `files-on` takes a leftover write membership away before it adds `sdfiles`, and
stops with the same message if it cannot. A
refused change is answered "This login cannot change or lock files here: ask the
administrator for files-write-on (request *n*)", is not carried out, and goes to the audit
trail as `api refused request=16 route=sdfiles write=off admin=off user=fred`; the login line says
`write=on` or `write=off` (and `admin=on` or `admin=off`). `sdapi` members are not affected. Like `sdfiles`, the group is
read at login, so a change reaches the person at their next login. The account's manifest
(`backup.account`) records it as `route.files.write`, and `restore.account` gives it back
only to an account that is in `sdfiles`.

### Administering files: `files-admin-on` and `files-admin-off`

A files-only login may configure a file, build and delete its indices, create and delete a file,
set or take the file's counter (`WRITE ... CREATING.SEQKEY`, `FCONTROL`) **only if the person is
in both `sdfileswrite` and the Linux group `sdfilesadmin`**: `modify.account` *name*
`files-admin-on` (needs `files-on` and `files-write-on` first, else "Account fred does not have
files-write, so it cannot be given files-admin: use files-write-on first"), `files-admin-off`, and
`files-admin-on` after `files-on` and `files-write-on` in `create.account user`. **It is off for
every new account, and the installer does not turn it on.** The line printed is `Account fred has files-admin yes`, read back from the group file.
The three groups are a chain, `sdfiles` < `sdfileswrite` < `sdfilesadmin`: `files-write-off` and
`files-off` take the higher groups away first (administration, write, files), each removal read
back, and a failure half way reports the removals that did happen; `files-on` and `files-write-on`
take a stray higher membership away before they add. What the permission allows, what the server
checks and how it is audited is in [SDNet](12d-sdnet-administration-group-and-read-only-files.html), *The administration group*. A
refused request is answered "This login cannot administer files here: ask the administrator for
files-admin-on (request *n*)" and nothing is carried out. The account's manifest records it as
`route.files.admin`, and `restore.account` gives it back only to an account that is in
`sdfiles` and `sdfileswrite`.

### The AI: `ai-on` and `ai-off`

An account may send text to the AI provider you have chosen (the `ai` verb) **only if the person is in
the Linux group `sdaiusers`**: `modify.account` *name* `ai-on`, `ai-off`, and `ai-on` in
`create.account user`. **It is off for every new account, and the installer
does not turn it on**, because each request is paid for by whoever holds the provider's key.
The line printed is `Account fred has ai yes`, read back from the group file. It stands alone (no
other gate is needed), is for accounts that belong to a person (a group account is refused), and takes
effect at the person's next request. The account's manifest records it as `route.ai`, and
`restore.account` gives it back. Which provider, model and key, what leaves the machine, and the page
that does all of this, `tool.ai`, are in [The AI Helper](20-the-ai-helper.html).

**The route words are not one state.** `ssh`, `api`, `both` and `none` are
absolute about the two routes they name, and **leave `files-on` alone**:
`modify.account fred none` takes away ssh and the API and not the files-only
login. Withdraw it with `files-off`. `sdapi` is never touched by `files-on` or
`files-off`.

**User accounts only.** A group account, which has no Linux user, is refused
`files-on` and `files-off` ("is a group account and has no remote access"), an
`other` account too ("Unable to change remote access ... status: 2"), and
`create.account group` and `create.account other` refuse the word the same way.
`files-on` also refuses a person who is not in `sdusers`, because the login would
refuse them first. If the Linux group `sdfiles` does not exist, `files-on` says
"sdfiles is not a valid Linux Group" and changes nothing, and
`create.account user ... files-on` looks for the group **before** it makes the Linux
user, so nothing is left behind. **An installation made before this release has no
`sdfiles` group, and its helper does not accept it, until the installer is run
again**; the installer makes the group (empty) beside `sdssh` and `sdapi`, and the
helper's list of groups it will touch includes it. Like `sdssh` and `sdapi`, the
group cannot be deleted with the helper's `groupdel`; a full DELETE of SD (not one
that keeps the accounts) removes it with the others.

**A change takes effect at the person's next login.** The group is read when the
login finishes, so a connection already open keeps the route it started with.
To take the route away from somebody who is connected now, `files-off` and end the
connection.

**Audit trail.** A files-only login writes `api login route=sdfiles write=off admin=off user=fred`
(`write=on` for a person in `sdfileswrite`, `admin=on` for one in `sdfilesadmin`). Each refusal writes
`api refused request=26 route=sdfiles write=off admin=off user=fred` (the number is the
request; `write` and `admin` are the state of the login, so a refusal with both `on` is a request
no files-only login may make). A user in neither group, as before, has the refused login in the usual
`api refused` form.

**The archive.** For a user account the manifest carries `route.files: 1` or `0`
beside `route.ssh` and `route.api` (not `files:`, which is already the count of files
in the archive), and `restore.account` puts an account it has to create back in
`sdfiles` if the manifest says so. An archive from before this release has no such
line and restores the account out of the group. A manifest that says `1`, restored on
a machine with no `sdfiles` group, fails for that account with the group message
and creates nothing.

### VOC pointers: where a file pointer may lead, and which Q-pointers are followed

**A VOC pointer is a way to name a file, so it is held to the same rule.** An
account can write a pointer into its own VOC with `ed`, or make one with
`create.file ... pathname`, and a Q-pointer is what `set.file` makes into
another account. For everybody but SDSYS:

| | |
|---|---|
| **a file pointer (F-type)** | must lead **inside the account's own directory**, or inside the directory of an account a Q-pointer was followed into (below), or be **the pointer SD itself put in the VOC** — the same id, with the same path, as in `newvoc` (`syscom`, `$map`, `dict.dict`, `voc`, `newvoc`, `$acc`). An account that holds `os-on` may go anywhere its Linux user can. Anything else is refused with status 3035 |
| **a Q-pointer** into a **registered account** | is followed only if the user **could `logto` that account**: a member of its Linux group, and the account not suspended — `logto`'s own test — **whether or not the account holds `os-on`**. SD's own Q-pointer, `sd.accounts` (which leads into SDSYS, an account nobody can `logto`), is exempt because it is exactly what SD put there |
| **a Q-pointer** that **names a path** | is an operating-system path, and the `os-on` question |

So `set.file` into somebody else's account works only for a user who may enter
that account, and a hand-made pointer at `/etc` or another account's
directory is refused unless the account holds `os-on`. A refused open takes
the `ELSE` branch with status 3035, like any other refusal here. **SDSYS is
never refused.**

**The API's request 29, "open an SDNet file", asks the same question.** It asks it of the
account **named in the request**, from that account's own register record, and not of
the account the API session happens to be in: a file pointer in the named account's VOC
must lead inside that account's own directory (`..` and links resolved, a directory
that merely begins with the account's name is not inside), unless the account holds
`os-on`. SDSYS entering its own account is never refused. It is stricter than the local
rule in one way: the pointers SD itself put in every VOC (`syscom`, `$map`,
`dict.dict`, `newvoc`) lead out of the account and are refused here too,
because a remote caller has no use for them. A refusal is error `ELSE` with status 3035
and a line on the audit trail, `api refused request=29 reason=os gate off user=...
account=... path=...`. The register is read at each request, so `os-off` applies to a
session that is already signed on.

**What this changes on an existing machine.** A Q-pointer that leads into an
account its owner can no longer enter stops opening, and so does a hand-made
file pointer to a directory outside the account in an account that does not
hold `os-on`. The accounts that existed at an upgrade hold `os-on`, so their
own pointers keep working; the Q-pointer rule applies to them too.

The `account:file` form of a file name is always available, with no `sd.conf`
setting: a name in no VOC record with one colon is read as a Q-pointer to that
account and file, and the **Q-pointer rule above applies to it unchanged**, so it
opens only what a Q-pointer the account wrote could open. There is no `path:name` form. Any other file outside the account
is reached only through a VOC pointer, which is held to the `os-on` rule and the
Q-pointer rule above.

### What `os-on` actually costs

Granting `os-on`, or `sh-on`, to an account that also has a remote route is
a larger decision than it looks: **it puts an operating-system shell behind
that account's credential, reachable from wherever the route is reachable
from** — the ssh port, or the API port. What the shell can do is exactly
what that Linux user can do on this machine, and nothing more, because SD
runs it as that user and never as root; so the cost is the cost of giving
that person a login on the machine. For an account that needs only SD,
leave both off.

```
umask {mask}
```

With no argument `umask` reports the session's current value; with one, it
sets it — the standard Unix meaning, applied to files SD itself creates as
well as anything a shelled-out command creates. **This is a real,
per-session mechanism here** — it has no Windows equivalent because Windows
reaches the same guarantee a different way, one inheritable ACL entry set
once by the installer, applied by NTFS below the runtime rather than by a
value a process can forget to set.

## Continued in

[Accounts and Security: Changing One
Account](01-accounts-and-security-6-modify-account.html) — modify.account and
the two account screens.

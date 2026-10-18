Title: Moving an Account
Subtitle: Taking an account to another SD machine with backup.account and restore.account: what you need, the steps, and what comes across.

Moving an account is a backup on one machine, a copy of one file, and a restore on the other.
There is no verb that does it in one go. The two verbs are described on
[Account Maintenance](01a-account-maintenance.html); this page is the procedure for using them
between two machines, and [the next page](17a-moving-an-account-cases.html) is what does not
come across, what happens to the Linux user and groups, and the cases where the machines differ.

> **Three things to know before you start.**
> **No password comes with the account.** An account the new machine does not have asks for a
> new one while it is restored, and `no.query` does not remove that question.
> **The backup is an ordinary, unencrypted zip** of every file in the account. Keep it where
> only SDSYS can read it, and delete it when the move is done.
> **A new account gets its switches from the zip's manifest, a plain text file.** Whoever can
> edit the zip decides what access a restored account is created with.

## What you need

* **Both machines run SD Core for Linux**, the full product. A backup from SD Core Solo is
  refused ("A full product's backup restores only to a full product, and a Solo backup only to
  Solo"). The manifest records the SD release but the restore does not compare it, so put the
  same release, or a newer one, on the new machine. Restoring onto an older one was not tried.
* **You are SDSYS on both**, and **no other session is logged in on either** while the verb runs.
  SD lists any it finds: *1 other session(s) are logged in. Every other session must log out
  first:*, then a line for each. While a backup or restore runs nobody can sign in, at the
  terminal, over ssh or through the API.
* **Disk for a second copy on the new machine.** A restore unpacks the zip into
  `.sdrestore.`*n*, in the folder that holds `user_accounts` and `group_accounts`, before it
  changes anything, and removes it when it ends. If a crashed restore left one, the next refuses:
  *… already exists, left by an earlier restore that did not finish. Remove it, then run
  restore.account again.*

## The steps

**On the old machine, as SDSYS.**

1. *(Optional.)* Record the account's switches to compare after the move:
   `settings.report /home/sd/backups`. It writes `SD-`*host*`-settings-`*yyyymmdd-hhmmss*`.txt`,
   with the same switch keys as the manifest below.
2. Say where backups go, once: `set.backup.directory /home/sd/backups`. It makes the directory if
   it is not there, readable by SDSYS only. Or give a directory each time with `to`.
3. Back the account up. Several names, or `all`, make one zip.

   ```
   backup.account jack
   Backed up 1 account(s) to /home/sd/backups/SD-oldbox-jack-20261018-114948.zip
     jack: 10 files, 45332 bytes, 6 directories
   ```

   SD counts the files, bytes and directories before it packs, compares them with what it wrote,
   and **deletes the zip if they differ**. The restore checks the same numbers. A name already
   taken is never overwritten (*A backup never overwrites a file*). Whatever it did not pack is
   named: *Not in the backup: jack/link.txt (symlink)*.
4. **Copy the zip to the new machine** with whatever you use for files (`scp`, a USB drive). SD
   has no verb for this, and the backup itself is not on the audit trail.

**On the new machine, as SDSYS.**

5. Put the zip where SDSYS can read it. The unpacking runs as SDSYS, not root, so a file that only
   root can read is not found. Keep other users out of its directory.
6. Restore it, naming the zip by its **full path**:

   ```
   restore.account /home/sd/backups/SD-oldbox-jack-20261018-114948.zip jack
   ```

   A bare file name is looked for in the directory `set.backup.directory` saved (and asked for if
   none is). A relative path starts from SD's current directory, not yours, and gives *… does not
   exist.* **`latest` will not find this zip** (see the next page).
7. SD checks the whole zip against its manifest **before it changes anything**, says what will
   happen and asks once (Enter is no):

   ```
     jack will be CREATED.
   Restore these accounts (y/<n>)? y
   ```

   An account the machine already has says *jack will be REPLACED. It now holds 11 files, 45332
   bytes.* **Replaced means its directory is swapped for the zip's and the old one is removed.**
   Whatever was made in it since is gone, and nothing is kept to undo it. If that matters, run
   `backup.account jack` on the new machine first.
8. Check it. For a user account that SD created, the lines it printed say what the account was
   given (*SD routes for jack: …*, *Account jack has SH no, OS.EXECUTE no*, and the lines for the
   edit, NET, FILES and shared switches). `settings.report` gives the same keys to compare with
   step 1. Sign in as the person and open a file.

An account that fails (a name clash, a refused password) is reported as *jack was not restored.*
and the others in the same zip go on. The restore ends with the count of those it restored, and a
non-zero return code if any failed.

## What comes across

Everything under the account's directory **except symbolic links**: files, programs and their
object code, the VOC and dictionaries. A hashed file is copied as the files it is on disk. The zip
also holds a manifest, `manifest.txt`, that any zip tool will show you. It is plain ASCII text:
a header, then one section per account.

```
format: 1
product: linux-full
sd.version: L1.1-3
created: 2026-10-18T11:49:48
host: oldbox
source.root: /home/sd
accounts: 1

[account jack]
type: USER
os.user: jack
os.group: sdu_jack
route.ssh: 0
route.api: 0
route.files: 0
os.sh: 1
os.execute: 0
edit.voc: 1
edit.bp: 1
edit.dict: 1
net: 1
shared.read: 1
shared.write: 1
description: Jack's test account
suspended: 0
source.path: /home/sd/user_accounts/jack
files: 10
bytes: 45332
dirs: 6
gcat: hello = bp.out hello
```

A group account's section has `members:` in place of the `route`, `os`, `edit`, `net` and `shared`
lines.

| In the manifest | On an account **SD has to create** | On an account that **already exists** |
|---|---|---|
| the files | fill the new directory | replace the directory |
| `description`, `suspended` | set from the zip | **set from the zip**, so a suspended account comes back suspended |
| `route.ssh`, `route.api`, `route.files` | the Linux user joins `sdssh`, `sdapi`, `sdfiles` as the zip says | unchanged |
| `os.sh`, `os.execute`, `edit.*`, `net`, `shared.read`, `shared.write` | set as the zip says | **unchanged** |
| `type`, `members` | the kind of account made, and a group account's members | unchanged |
| `gcat:` lines | the program is put in the global catalogue again | same |

A key the zip does not have (an older backup) gives the delivered default: every gate off,
`shared.read` on, `shared.write` off. **An existing account keeps its own switches whatever the zip
says.** In the test a zip with `os.sh: 1` restored over an account with `sh` off left it off; to
change one, use `modify.account`.

**Global programs.** The backup notes each global program whose object file is in the account, and
the restore catalogues it again from the restored file, printing *… re-catalogued globally*. A
program recompiled after it was catalogued no longer matches, so it is not carried;
`settings.report` lists the global catalogue. **Check any name the new machine already uses.** The
source says a different program under the name is left alone and reported (message 13017); in the
test the program from the zip **replaced** it, and its name was printed in capitals.

**Permissions.** Each file and directory keeps its permission bits, except that other-write is
removed and the owner always has read and write (and search on a directory). In the test `0640`,
`0750` and `0755` came back as they were, `0666` as `0664` and `0444` as `0644`. Ownership is not
in the zip: the restore gives the tree to the account's own Linux user and group, with the setgid
bit on every directory. That step needs root and was not run in the test.

## Continued in

[Moving an Account: the Linux User and the Cases](17a-moving-an-account-cases.html).

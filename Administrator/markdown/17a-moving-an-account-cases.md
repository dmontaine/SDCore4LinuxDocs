Title: Moving an Account: the Linux User and the Cases
Subtitle: What does not come across, what a restore does to the Linux user and groups, and the cases where the two machines differ.

This page continues [Moving an Account](17-moving-an-account.html).

## What does not come across

* **Passwords**, the SD one and the Linux one.
* **The `sd-on` switch.** It is not in the manifest, so a restored account has it off, an
  existing one keeps what it had. (`settings.report` does not show it either.)
* **The Linux user's home directory**, its ssh keys and its other group memberships.
* **The system**: SDSYS and its VOC, `sd.conf`, the TLS certificate, the ssh and API setup, the
  audit trail, and every global program that is not tied to an account's object file.
* **Anything the account only points at.** A VOC pointer to a file outside the account is named
  (*outer in jack points outside the account (/etc) and was left unchanged.*) and not followed.
  Indices kept outside the account are not in the zip; the restore says *Rebuild them with
  build.index* (from the source, not run).
* **Accounts outside the accounts folders.** An account whose directory is not directly inside
  `user_accounts` or `group_accounts` is refused by the privileged helper, and **with `all` that
  stops the whole backup**, leaving no zip. Name the other accounts one by one.

`backup.account all` takes every registered account but SDSYS, so **the shared account is in it**.
Restoring `shared` is not covered by anything said here: the restore gives a group account's files
to its register group, `sdg_shared`, while the installer gives that directory to `sdusers`
(see [The Shared Account](13-the-shared-account.html)), so check the group of its files after a
restore. This is from the source and was not run. When you move only some accounts, name them.

## The Linux user and groups

**An account that already exists** keeps its Linux user, its password and its groups. Only its
files, its description and its suspension change.

**A user account SD has to create** is made the way `create.account` makes one:

* The Linux user is named after the **account**. `os.user` and `os.group` in the manifest are
  not read. The user is made with its own home directory and the group `sdu_jack`, joins
  `sdusers`, and joins `sdssh`, `sdapi` and `sdfiles` where the manifest says 1. Its user number is
  whatever the machine gives it, and ownership is set by name, so a different number on the old
  machine does not matter.
* **SD asks for the password at the terminal**, prints the rule (*A password needs at least 8
  characters, with a lower-case letter, an upper-case letter, a digit and a symbol.*) and allows
  three tries. If it is refused or you decline to retry, SD removes the Linux user again, says *An
  account must have a password. Nothing was created.* and the account is *not restored*.
  **`no.query` removes the "Restore these accounts" question and not this one.** In the test the
  commands typed after a `no.query` restore were taken as passwords.
* A route the machine cannot yet serve is said and not refused: *… is set up to sign in over ssh,
  but this machine has no ssh server yet.* The account is still made.

A **group account** is made with its Linux group `sdg_`*name*, owned by `sdsys`. Its `members:` are
Linux user names, and each must be a user of the new machine. One that is not is named and the
rest go on: *nosuchuser could not be added to group sdg_work (status 2). Add it with
modify.account once it is an SD user.*

## When the machines differ

* **Different host names.** `restore.account latest` takes only a backup whose file name carries
  *this* machine's name, the part of the host name before the first dot, in lower case. A zip
  from another machine gives *No backup of jack made on this computer was found in …*. Name the
  file. A renamed file is also never picked by `latest`.
* **A different accounts folder.** Values in the account's VOC that begin with the old account's
  path are rewritten to the new one. In the test a pointer to `/home/sd/user_accounts/jack/inv`
  became the account's path on the test machine. Only the VOC is rewritten: a path written in a
  record or a program is left as it is.
* **The Linux user name is already taken.** SD reuses the user only if SD itself made it (its
  comment is exactly `SD account`) and keeps its password: *jack is a Linux user that SD itself
  created earlier, so the restored account uses it. Its Linux password is unchanged.* That case was
  not run, as no such user was available. Any other user is refused, nothing is created, and the
  account is not restored:

  ```
  Linux user jack already exists.  SD accounts create their own Linux user
  jack was not restored.
  ```

  Rename or remove that Linux user with the operating system's tools, then run the restore again.
  **There is no way to restore under another account name.** A word such as `as` is read as an
  account name: *as is not in this backup.*
* **A Windows backup.** The archive format is shared with SD Core for Windows and the restore has
  code for it. It was not tried.

## When it refuses

| It says | Why |
|---|---|
| The archive does not match its manifest: jack (manifest 99/45332/6, unpacked 10/45332/6). Nothing was restored. | the zip was changed or damaged |
| … has manifest format 2, and this version reads format 1. | a newer zip format |
| This backup is from linux-solo and this system is linux-full. … | the wrong product |
| nosuch is not in this backup. | the name is not in the manifest |
| Making the archive … failed (status 2): sd-elevate: REFUSED … | an account outside the accounts folders |
| 1 other session(s) are logged in. | log them out and run it again |
| … already exists, left by an earlier restore that did not finish. | remove that `.sdrestore.`*n* folder |

None of these changed an account, and the restore leaves no `.sdrestore.`*n* folder behind (except
in the last row, where it is the folder that is the cause). The source also refuses a zip with
an entry outside `manifest.txt` and `accounts/`, a `..` or absolute path, a backslash, or a symbolic
link; that was not run.

## What was seen to work

The steps on this and the previous page were run on a private test copy of SD built from the
source. In it the privileged helper is a stand-in that checks every argument exactly as the real
one does and then acts without root. In it were run: backup of one account, two accounts and `all`,
the manifest, the counts, the refusals above, restore over an existing account (the files,
permissions, VOC rewrite, switches kept, description and suspension from the zip), the restore of
a missing group account with the switches from its manifest, the password dialogue, the
Linux-user clash, and `latest` with another host's zip.

**Not run, because each needs root or a second machine:** the real `backup-pack` and the counting
as root; ownership and setgid after a restore; the making of Linux users and groups, the
password being set, and the removal of a user whose password was refused; the members of a group account being added; the reuse of an SD-made user; the
lines a created user account prints for its routes and switches; indices outside the account; the
audit line, `restore.account account=jack archive=`*file name*, written once for each account
restored; the login hold seen from another session; and a restore from a real second machine.

## See also

[Account Maintenance](01a-account-maintenance.html) for the verbs and `set.backup.directory`;
[Accounts and Security](01-accounts-and-security.html) for the switches;
[Data at Rest](04a-data-at-rest.html) for backups and encryption.

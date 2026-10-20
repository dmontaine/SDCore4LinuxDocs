Title: Upgrading and uninstalling
Subtitle: Replacing an existing installation, and taking SD off the machine.

This page continues [Installing SD Core](01-installation.html). SD must be
uninstalled before `installsdcore.sh` will run again — it refuses outright if
`/usr/local/sdsys/bin/sd` already exists — so "upgrading" here means
uninstalling with accounts kept, then installing again.

## Upgrading

**Uninstalling with your database kept, then installing again, updates
your database in place.**

| Replaced | Kept, and not touched |
|---|---|
| the catalogue and compiled programs | your accounts and their passwords |
| the BASIC source | the private catalogue |
| the messages and include records | anything you added to an account's VOC (the installer adds the release's new commands; see below) |
| the VOC templates and library routines | your print queue and held reports |
| the SDSYS `BP` programs | everything under your own accounts, and `sd.conf` |
| terminfo, the licence, the contributor list | |

Anything SD created while it was running is left as it is, except that each
account's VOC is brought up to the release, as the next paragraphs say.

**The dictionaries are brought up to date for you.** The install step that
writes them (`write_install_dicts`) adds and updates the entries SD ships
and leaves alone any you added. If that step cannot run, the installer says
so rather than finishing quietly.

**Existing accounts pick up a release's new commands automatically**, as in
SD Core for Windows. When you kept your accounts, the installer ends by
running, as the administrator:

```
:update.accounts all
```

It says "Bringing every registered account's VOC up to this release." and
walks every registered account, updating its VOC from `newvoc` — a command
this release adds can then be typed in accounts that already existed. If
`newvoc` changes the type of a record an account already has, it asks about
that record, account by account, so stay at the keyboard until it finishes.

You can run it again yourself at any time, logged in as `sdsys` — after
registering an account from an older system, say. To refresh one account
instead, `update.accounts` (no `all`) run **in that account** updates just
it and offers to do the rest.

**Every install, kept accounts or not, puts the `sdsys` user back in the group of
every account and makes each account's VOC and dictionaries writable by that group**
(it says what it did, and warns without stopping if it could not). The old `sdsys`
user is removed with an uninstall and takes its memberships with it, and SDSYS
needs them to change an account by saving its master record. This gives the
`sdsys` user write access to those files in every account: see
[The master files](19-the-master-files.html) in the administrator set. Running the
installer again repeats it - so taking `sdsys` out of an account's group by hand
(`gpasswd -d`) lasts only until the next install or upgrade, which puts it back.

Two limits are worth knowing before you rely on it.

> **SD only ever adds records to a VOC, never removes them.** An account
> that already has a verb keeps it even after a release withdraws it.
> `update.accounts` cannot be relied on to take something away.

> **A record you have customised can be held back on purpose.** Put
> `[locked]` in field 1 after the type code and the update leaves that
> record alone, naming it in a message so you know what was withheld —
> and therefore which corrections this release made that you have not
> taken. Verbs are the exception: a locked verb is updated anyway, and you
> are told which. The administrator documentation covers it under
> *Accounts and security*.

**An upgrade keeps what accounts could already do with the shell and the
operating system.** A new account now starts with `sh` and `OS.EXECUTE` off
(the `sh-on` and `os-on` switches), but accounts made before those switches
existed have always had both. So when you kept your accounts the installer
switches `sh-on` and `os-on` on, **once**, for every user account that
exists then; ssh and the API are left as they were. Turn either off for an
account whenever you like with `modify.account` *name* `sh-off` / `os-off` —
**a later install does not turn them back on.**

**The same is true of the right to save a change to a VOC, a program file or
a dictionary** (`voc-on`, `bp-on`, `dict-on`), which is also off for a new
account. When the installer is run by the user whose own account already
exists, it switches all three on, once, for every user account in the
register; group and other accounts are left off on purpose, and a different
OS user installing over existing accounts does not run this step. Turn them
off with `voc-off`, `bp-off` and `dict-off`. Accounts you make after the
upgrade start with everything off.

**The installer makes the `shared` account** (a group account whose data files
every account can open by file name; see [Accounts](05-account-types.html#the-shared-account)),
just after the account for the installing user and before the accounts you kept are
brought up to the release. If you kept your accounts, the one you had is kept. Every
account, new or existing, can read the `shared` account's files and none can write them,
until SDSYS says otherwise with `shared-read-off` and `shared-write-on`; nothing is
written to your existing accounts for that.

**The installer stops, before it changes anything, if an account named `shared`
already exists that is not SD's own.** The name is reserved. It names the account's
register record, and you rename that account by hand and run the installer again.

## Uninstalling

`deletesdcore.sh` is in the release package beside `installsdcore.sh` (from
L1.1-1 on), and in the source repository. Run it as yourself, not with `sudo`:

```sh
./deletesdcore.sh
```

Two separate questions, each defaulting to keeping what you have:

```
Keep your existing accounts? (Y/n)
Keep your existing configuration? (Y/n)
```

**Answering "no" to accounts does not delete them on its own** — you must
then type `DELETE` at a second prompt to confirm. **A silent or partial
answer never deletes the database**; only an explicit `DELETE` does.
Deleting is permanent: every SD account, every password (including
SDSYS's), and all data stored in them.

**The uninstaller removes the ssh boundary it installed** — the
`ForceCommand` block in `/etc/ssh/sshd_config` and the helper script that
manages it — and leaves the rest of `sshd_config` as it was. **It does not
remove the `openssh-server` package itself.** It may predate SD, or be in
use by something else; taking a package off the machine is not SD's
decision to make.

The `sdusers` Linux group and the `sdsys` user are removed only on a full
`DELETE` of accounts — kept accounts need `sdusers` to remain readable, and
removing the group would orphan the permissions on your database. **The Linux
group `sdg_shared` (the `shared` account's group) goes the same way:** removed on
a full `DELETE`, kept when the accounts are kept, so that the members an earlier
install gave it cannot be admitted to a new `shared` account by mistake.

## Continued in

[Your first thirty minutes](02-first-run.html) — install to a second user
signing in, in eight steps.

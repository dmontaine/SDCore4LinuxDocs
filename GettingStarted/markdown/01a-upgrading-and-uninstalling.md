Title: Upgrading and uninstalling
Subtitle: Replacing an existing installation, and taking SD off the machine.

This page continues [Installing SD Core](01-installation.html).

## Upgrading

**Run the new release's `installsdcore.sh` over the installed one; no uninstall
is needed.** When `/usr/local/sdsys/bin/sd` is already there, the installer
says *SD Core is already installed: upgrading it in place, keeping your accounts
and your configuration*, runs the new release's `deletesdcore.sh` itself with the
answers that keep both, and then installs. The result is the same as
uninstalling with accounts and configuration kept and installing again, which
still works. If that step cannot run, the installer stops before it installs
anything and says so.

**Uninstalling with your database kept, then installing again, updates
your database in place.**

| Replaced | Kept, and not touched |
|---|---|
| the catalog and compiled programs | your accounts and their passwords |
| the BASIC source | the private catalog |
| the messages and include records | anything you added to an account's VOC (the installer adds the release's new commands; see below) |
| the VOC templates and library routines | your print queue and held reports |
| the SDSYS `BP` programs | everything under your own accounts, and `sd.conf` |
| terminfo, the license, the contributor list | |

Anything SD created while it was running is left as it is, except that each
account's VOC is brought up to the release, as the next paragraphs say.

**The dictionaries are brought up to date for you.** The install step that
writes them (`write_install_dicts`) adds and updates the entries SD ships
and leaves alone any you added. If that step cannot run, the installer says
so rather than finishing quietly.

**The parameters SD no longer has are taken out of a kept `sd.conf` for
you.** SD refuses to start on a name it does not recognize, so when the
installer puts back a `sd.conf` you kept, it removes each line that names a
parameter this release dropped (`APILOGIN`, `CODEPAGE`, `CREATUSR`, `EXCLREM`,
`FILERULE`, `FIXUSERS`, `GDI`, `INVCASE`, `JNLDIR`, `JNLMODE`, `PORTMAP`,
`RINGWAIT` and `TXCHAR`) and says which. A configuration file you copy in by
hand from an older installation needs the same done to it; see
*Configuration* in the Administrator set.

**Existing accounts pick up a release's new commands automatically.** When you kept your accounts, the installer ends by
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

**The `sdsys` user is in the group of every user account as delivered**, so that
SDSYS can change that account's files. An install that keeps accounts puts the user
in the group of each user account it is not in yet, makes the account's record files
writable by that group, and says how many accounts it changed; it asks nothing. It
does this once, and records that in `/home/sd/$sdsys.access` (a group it could not
change is a warning and no record, so the next install tries again). From then on the
installer does not touch these groups, so what the administrator does with
`modify.account` *name* `sdsys-off` and `sdsys-on` stands. See *The Master Files* in
the Administrator documentation for what the membership gives the `sdsys` user (write
access to everything the account's group may write).

**Your files are converted to case-insensitive record ids for you.** Every file
`create.file` makes treats ids as one whatever the case (see
[Lower case](11-lower-case.html)), and an upgrade keeps your existing files, which
were built case sensitive. After the accounts' VOCs are brought up to the release,
the installer walks every registered account, **naming each one as it goes**, reads
each file the account's VOC names first, and converts it only if no two of its ids
differ only by case, so a conversion cannot lose a record. It also makes each
account's private catalog names lower case. The whole walk is kept in
`/var/tmp/sdcore-install-nocase.log`. A file is **left exactly as it was** and named
when:

- it holds two ids that differ only by case (rename or delete one of each pair, then
  run `configure.file` *name* `no.case` on it);
- it has alternate key indexes (convert it by hand with `configure.file`);
- it lies outside its account's directory, or under SDSYS (each is converted by its
  owner with `configure.file` *name* `no.case`);
- it could not be read or rebuilt.

SDSYS's own files are not walked at all. A walk that did not finish prints a warning
and the install goes on; what was not converted keeps working, and ids are still
found typed in any case.

Two limits are worth knowing before you rely on it.

> **The VOC update removes only what is on SD's deletion list.** A record
> that a release withdraws is taken out of an account only if it is on the
> list and is still the record SD shipped, and a copy is saved first
> (`restore.voc` puts it back). Anything else the update leaves alone, and a
> record you marked `[locked]` is kept — a locked verb excepted.

> **A record you have customized can be held back on purpose.** Put
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
exists then and whose switch is still blank; ssh and the API are left as they were. Turn either off for an
account whenever you like with `modify.account` *name* `sh-off` / `os-off` —
**a later install does not turn them back on.**

**The same is true of the right to save a change to a VOC, a program file or
a dictionary** (`voc-on`, `bp-on`, `dict-on`), which is also off for a new
account. When the installer is run by the user whose own account already
exists, it switches all three on, once, for every user account in the
register whose field is blank; group and other accounts are left off on purpose, and a different
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

`deletesdcore.sh` is in the release package beside `installsdcore.sh`, and in the
source repository. Run it as yourself, not with `sudo`:

```sh
./deletesdcore.sh
```

Two separate questions, each defaulting to keeping what you have:

```
Keep your existing accounts? (Y/n)
Keep your existing configuration? (Y/n)
```

**The administrator's scheduled jobs are kept with the configuration.** Their
timers are always stopped and removed, since a timer left behind would start a
program that is gone; when you keep the configuration their definitions are saved
in `/home/sd/jobs.saved`, and the next install schedules each one again and says
how many (*Scheduled jobs: n scheduled again, m NOT*). When the configuration is
deleted, the jobs go with it.

**When something cannot be put back, the install says so in a red box.** If an
install over an installed SD, or a reinstall that keeps your accounts and
configuration, could not put something back as it was (a scheduled job the helper
refuses, the API door or the `sdsys` ssh door that was open and could not be
opened again, or the firewall rule for the API), the closing summary starts, right
under *The SD server is installed.*, with *WARNING: SOME SETTINGS NEED TO BE FIXED.*
in bold red. Each numbered item says how to correct it and gives the lines to type at
the colon prompt. **Sign in to Linux as `sdsys` itself, then start SD:** the commands
are the administrator's, and are refused to any other user and after `su sdsys`.

A scheduled job is made again with `set.job add`, or with `set.job change` when its
definition is already there. When the saved definition is damaged the line shows
`<job> <schedule>`: put in the job and the schedule you had
(`set.job add nightly backup-all daily 02:30`). The box does not give reasons; the
reason a job was refused is in the install's output above it. If the same step fails
when you type it, correct what it reports and type it again. An API or ssh note that
the install did not trust (it must be a plain file owned by root) is listed too: if
that door was not open before, leave it as it is.

When the firewall rule for the API could not be added, a red warning of its own says
so: `remote.api on` adds the rule, and `remote.api local` keeps the API to this
computer. The uninstaller shows the same kind of box at its end for what it could not
save for the next install; do those steps after that install. Nothing is printed when
everything was put back.

**Your screen theme comes back as you had it.** An install, an upgrade or a reload
leaves the `SCREENTHEME` line of a kept `sd.conf` exactly as it was; a kept file with
no such line stays on `mono`. Only a new install starts in `paper`, from the
shipped `sd.conf`.

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
install gave it cannot be admitted to a new `shared` account by mistake. **So does
the Linux group of every other account**, `sdu_<name>` for a user account and
`sdg_<name>` for a group account: on a full `DELETE` the uninstaller reads each
account's group from the register and removes it. A group with an SD-like name
that no account of the register names is left alone, and so are the Linux users
of the user accounts: they hold people's own files.

**What changed since the previous release**, and what an upgrade might break,
is in the *Changes* document that comes with the release: every addition,
change and removal, listed by section.

## Continued in

[Your first thirty minutes](02-first-run.html) — install to a second user
signing in, in eight steps.

Title: Upgrading and uninstalling
Subtitle: Replacing an existing installation, and taking SD off the machine.

This page continues [Installing SD Core](01-installation.html). SD must be
uninstalled before `installsdai.sh` will run again — it refuses outright if
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

## Uninstalling

`deletesdai.sh` is in the release package beside `installsdai.sh` (from
L1.1-1 on), and in the source repository. Run it as yourself, not with `sudo`:

```sh
./deletesdai.sh
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
removing the group would orphan the permissions on your database.

## Continued in

[Your first thirty minutes](02-first-run.html) — install to a second user
signing in, in eight steps.

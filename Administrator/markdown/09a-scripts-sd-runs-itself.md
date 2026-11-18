Title: The Scripts SD Runs For Itself
Subtitle: What calls `sd-elevate`'s subcommands, what the installer does inline, and what runs when SD starts.

This page continues [The Installed Scripts](09-the-installed-scripts.html).

**There is no separate category of scripts "the installer runs" versus
"a verb calls" versus "SD runs for itself".** It is the same `sd-elevate`
and the same subcommands (listed on the previous page) either way, invoked
from `installsdcore.sh` directly, from an administrator verb, or from
`deletesdcore.sh`. This page is about the few steps that have no script of
their own, and the one thing that runs at every start.

## What has no separate script

| Step | How it is done |
|---|---|
| Keeping an ordinary account off the console | not done: an ordinary account's console login is not denied at all (being at the console is being on the machine as that Linux user, which SD's `sh-on`/`os-on` switches do not govern). See *Security and the operating system* in the Getting Started set |
| The service | a `systemd` unit file (`sd.service`, `sdclient.socket`), installed with `install` |
| The editors | `apt-get install micro`, inline in `installsdcore.sh` |
| Bringing every account's VOC up to the release | `update.accounts all`, run inline by `installsdcore.sh` as the administrator when the accounts were kept |
| The route groups and the `sd` command | nothing to run by hand: the installer makes the `sdssh`, `sdapi` and `sdfiles` route groups once, and `modify.account` moves an account in and out of them; `sd` is symlinked into `/usr/local/bin` at install time, and there is no PATH toggle |
| Locking down SD's own files | inline `chown`/`chmod` calls in `installsdcore.sh`, at the specific paths that need them (`$cred` 700, `batch.jobs` 750, and so on — see *Security* in the Getting Started set) |
| `micro`'s syntax file | `micro`'s own program (`gpl.bp/edit`) copies it into the caller's `~/.config/micro/syntax` itself, on first use, with no privilege needed. It reaches an account made after the install without anything to re-run |

## What runs at every start

**`sd-reconcile-accounts --sweep` runs before `sd -start`** as `ExecStartPre`
of `sd.service`, with its exit status ignored, so a stale record can never
stop SD from starting. It removes register records whose Linux user has gone,
and their directories (see the previous page). Run by hand without `--sweep`
it only reports.

## Restarting after a remote-access change

**No SD session is ever ended by a remote-access change.** `remote.api`'s
`on`/`local` restart only the `sdclient.socket` unit; `remote.ssh` only moves
a firewall rule. See [Remote access and the
machine](05-remote-access-and-the-machine.html).

## See also

[Installation and the daemon](08-sd-installation.html) covers what the
installer puts on the machine and what an upgrade replaces.
[Remote access and the machine](05-remote-access-and-the-machine.html)
covers the two verbs that call `sd-elevate`'s remote-access subcommands,
and is the supported way to change either setting.

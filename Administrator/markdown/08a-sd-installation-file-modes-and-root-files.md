Title: Installation: File Modes and the Files Root Runs
Subtitle: The daemon's restart and the files root runs.

This page continues [Installation and the daemon](08-sd-installation.html).

### The daemon is restarted if it dies

`sdlnxd` is run by its own `systemd` unit, `sd-lnxd.service`, and `systemd` starts it again two seconds after it **fails** (`Restart=on-failure`): `kill -9`, a crash or the out-of-memory killer. While it is down the
audit records of ordinary users are in the journal only (see above) and lost sessions are not cleared down (the daemon scans for them every `CLEANUP` seconds, 300 by default); the new daemon takes up both at once.
`sd.service` starts SD with `sd -start -nodaemon`, which does not fork a daemon of its own, and wants `sd-lnxd.service`; stopping `sd.service` stops the daemon with it (`BindsTo=`).
Things to know:

- **A stop is not a failure.** `sd -stop` ends the daemon with SIGTERM and it exits with status 0, so it is **not** started again. After an `sd -stop` by hand `systemctl restart sd.service` brings SD and the daemon back (or `systemctl start sd-lnxd` for the daemon alone while SD is running).
- **A daemon that keeps failing is given up on.** Five starts in a minute and the unit is `failed`; `journalctl -u sd-lnxd` says why, and `sudo systemctl reset-failed sd-lnxd; sudo systemctl start sd-lnxd` starts it again once that is mended.
- **One daemon at a time.** A second `sdlnxd` (started by hand, or by a plain `sd -start`) finds the first named in the shared segment and ends at once with status 0, saying so in the error log.
- **`sd -restart` and a plain `sd -start`** still fork a daemon of their own, outside systemd, so nothing watches it. Use `systemctl restart sd.service`.
- An upgrade over an older installation has the units after SD is deleted (keeping the accounts and the configuration) and installed again. If an old `sd.service` was left behind by a delete, the installer replaces it, and adds `sd-lnxd.service`, when it does not mention that unit.

The error log (`errlog`) is mode 664,
owner `sdsys`, group `sdusers`: every session appends to it, and nothing runs it.

SD's shared memory segment and its semaphores are made mode 0660 and belong to the group `sdusers`, so only SD users can attach them. `ipcs -m` shows the mode of the segment.

**A member of `sdusers` who has an operating-system shell can still write the segment**, because every SD user is in that group. So nothing a session *decides on* is read
from it. A session takes these from places only SDSYS or root can write:

| What | Where a session gets it |
|---|---|
| the system directory (global catalog, register, messages, audit trail, errlog) | `SDSYS=` in `sd.conf` |
| the p-code every session runs | `bin/pcode`, read by the session itself; a copy that others or `sdusers` can write is refused |
| the per-session settings (`SH`, `SPOOLER`, `USRDIR`, `GRPDIR`, `DUMPDIR`, `TEMPDIR` ...) | `sd.conf`, read by the session when it starts |
| the session's own administrator, `sh`, `os.execute` and `sd.accounts` bits and its gates | memory only that process can change |

Two things follow. **`sd.conf` is read by every new session**, so an edit to one of the per-session settings reaches the sessions started after it, without a restart;
the parameters that size or configure the segment still need one. And **a bad line in `sd.conf` stops a new session starting**, with the message `sd -start`
gives, until the line is repaired. It does not stop SD or the sessions already running. If the segment's copy of the system directory differs from the
file's, the file is used and one line goes to the system log.

**What this does not close.** The lock table, the file table and the user table are still in the shared segment and still writable by an SD user with a
shell: such a person can release other people's locks, log other sessions out or fill the user table. That is damage and denial of service, not a way to a
privilege. The gates are walls for an SD *session*; a person with a shell is trusted with the segment. Giving SD users no login shell, or only the
forced-command ssh route, is how an installation that cannot accept that closes it.
The installer leaves a new user's login shell as the operating system's default, because any tighter default would also stop the forced-command ssh route and a
console login that starts `sd`; `sudo usermod -s shell user` changes it for one user. (sshd runs a forced command through the user's login shell, so a shell
that refuses commands closes that route too: choose per user, and see *Remote access and the machine*.)

**The file `$ipc`.** `$ipc`, in the system directory, is the one SD file every user's process has to write (it is `sdsys:sdusers`, directories 2770 and files 0660; an operating-system user
who is not in `sdusers` can no longer read the commands, `DATA` lines and messages it holds), so a member of `sdusers`
with a shell can write it as well. It holds working records and nothing a session is configured from: the lock that orders a phantom's start-up, the start-up
records of a phantom (its command, its `DATA` queue and its log file name), the messages waiting for a user, the phantom register
that `status` shows, and the tables that `profiler`, `hsm` and `pstat` ask another session for. A phantom no longer takes its command, options, `DATA` lines or
log file from it on trust. `phantom` seals the records with a secret that it makes for each phantom and gives only to the new process, in its environment, where
only the same operating-system user (and root) can read it, and which the new process copies and overwrites at once. The phantom runs, stacks and sets nothing unless the seal on
what it read checks; if it does not, the phantom ends at once, says so in its `como` log and to its parent, and writes `phantom refused` to the audit trail.
SD does not run, stack or set anything from the other records (messages, the register and the profiler, `hsm` and `pstat` tables); they are only shown, and a
message is shown as it was written. The conversation of the phantom debugger (`pdebug`) is not carried in `$ipc` at all: its messages are records of a directory file in the
private store of the person who runs `pdebug`, `.local/state/sd/pdebug` below that user's Linux home. SD finds the home in the password database (never from `$HOME`), makes the
directories on the way when they are missing, and uses the store only when every directory from the home down is a real directory that nobody else can write and the store
itself is readable by its owner alone. A `pdebug` and the phantom it debugs therefore reach each other only when both run as the same operating-system user, which is how
they are started in practice; the form in which `pdebug` waits and a phantom is started afterwards by the same person works as before. `pdebug` says it cannot start (message
11948) when the store cannot be set up, and a phantom that finds no store, or a `pdebug` that has gone, behaves as if no `pdebug` were waiting. The store survives a restart of
SD, which `$ipc` did not, so `pdebug` removes the records of its own user number when it starts, and a phantom ignores a start record whose `pdebug` has gone.
The secret is kept in no file and not in the segment. That another operating-system user cannot read the environment of this user's processes is the
operating system's rule.

### The files root runs

`sd.service` runs `bin/sd` as root (`sd -start` and `sd -stop`), `sd-lnxd.service` runs `bin/sdlnxd` as root, `sdclient@.service` (the first stage of every API connection)
runs `bin/sd -n -q` as root, `sd-elevate akpath-set` runs `bin/sdidx` as root, and every session - that first stage included - reads `bin/pcode`. **A file that root runs
must not be one that the `sdsys` login can replace,** or whoever held that login could
change one and have root run it at the next start. **Near its end the installer makes `/usr/local/sdsys/bin` and every file in it `root:root`, with no group or other
write, and makes the directory itself immutable** (`chattr +i`).

| | owner, mode |
|---|---|
| `bin/sd`, `bin/sdlnxd`, `bin/sdidx` | `root:root` 755 |
| `bin/pcode`, `bin/pcode.old` | `root:root`, readable by everyone, writable by root only |
| `bin/sdfix`, `bin/sdconv`, `bin/sdtic`, `bin/sdclilib.so`, `bin/libsdcli.so` | `root:root` 755 (no unit runs them; they are in the same directory, and an administrator may run `sdfix` with `sudo`) |
| `bin` itself | `root:root` 755, immutable |
| `.sdcore-install`, `/usr/local/sbin/sd-elevate`, `sd-accarchive`, `sd-reconcile-accounts` | root's, as before |
| everything else in `/usr/local/sdsys` | `sdsys:sdusers`, as before (the register, the global catalog, `voc`, `bp`, the SDSYS account's files) |

**Why the attribute.** The `sdsys` user owns `/usr/local/sdsys`, and the owner of a directory may rename any entry in it, whoever owns the entry. With the files root's
and nothing more, `sdsys` could move `bin` out of the way and make a `bin` of its own, which `systemd` would run at the next start. The attribute stops that rename, and any new
or removed entry in `bin`; only root can lift it. `lsattr -d /usr/local/sdsys/bin` shows an `i` when it holds. **If the file system does not keep the attribute** (the installer
prints `WARNING: the root-run files were NOT all sealed`, says the directory `could not be made immutable`, and repeats a warning in its closing summary), the files are still root's, but `sdsys` can rename `bin` and put its own in its place, and nothing else closes that.

What this changes for you:

- **To put a new file into `bin`** (a hand-built `sd`, say): `sudo chattr -i /usr/local/sdsys/bin`, copy it in as root, then `sudo chattr +i /usr/local/sdsys/bin`.
  Writing into a file that is already there with `cp` needs root and no change of the attribute; replacing it with `install` or `mv`, which make a new entry in the
  directory, needs the attribute lifted. So do SD's own writes of `bin/pcode` when `SAFEDIR` is set in `sd.conf` (it is off as delivered), because they write a new file and
  rename it.
- **The two things that write `bin/pcode`** - `catalog ... pcode` and compiling a `recursive` program under `sd -internal` - are tools for building SD itself. They are root's
  from now on, and the second makes `bin/pcode.old` when it is not there yet, which needs the attribute lifted; the `sdsys` login does neither. The installer's own passes
  run as root and finish before this step. With the attribute set, `bin` and its files are `root:root` (the `i` shows in `lsattr -d`), the `sdsys` login cannot write, make or
  rename an entry in `bin` or rename `bin` itself, SD and the audit daemon start from it (and `systemd` starts the daemon again after a `kill -9`), and the `SDSYS` account can
  still compile, catalog locally and globally, run a program and run `update.accounts all`.
- **`deletesdcore.sh`** lifts the attribute before it removes the directory, so a delete (with or without keeping the accounts) works as before.

**What this does not close.** The global catalog and the sudo helper `sd-elevate` are still routes from a stolen `sdsys` login to root-run or every-account code (see
[The master files](19-the-master-files.html)); data that root reads but does not run (`terminfo`, `messages`) is still `sdsys`'s; and during the minutes of an install,
before this step, `bin` is still `sdsys`'s - install while nobody holds that login (a first install has no such login yet). The helper does refuse a session that is `sdsys` only through `su sdsys`, `sudo -u sdsys` or a service: it asks that the login behind the call is `sdsys`'s own, and says so when it is not. A real login as `sdsys` (the machine's console, or any other login that really is `sdsys`) is the case it cannot tell from the administrator.

## Continued in

[Installation: The Daemon, Upgrading and
Uninstalling](08b-sd-installation-daemon-upgrading-uninstalling.html) — the
daemon, upgrading and uninstalling.

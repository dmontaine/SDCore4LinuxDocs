Title: Running SD
Subtitle: The daemon, starting and stopping, and what to do after an unclean shutdown.

**SD is a `systemd` service and it is already running.** Nobody types
`sd -start` after every reboot.

| | |
|---|---|
| Unit | `sd.service` (starts the daemon), `sdclient.socket` (the API listener) |
| Start type | enabled — `systemd` starts both at every boot |
| Created by | the installer, which also starts and enables them |
| Removed by | the uninstaller |

## Starting and stopping

**Stopping SD ends every session on the machine**, which is exactly what
`sd -stop` has always done. Either is fine:

```
sudo systemctl stop sd.service sdclient.socket
sudo systemctl start sd.service
sudo systemctl start sdclient.socket
```

```
sd -stop
sd -start
```

**Start it the way you stopped it.** `sd.service` is a one-shot unit: it
stays "active" after it has started SD, and `sd -stop` does not tell it that
SD has gone. So after `sd -stop` the unit still reads active,
`sudo systemctl start sd.service` does nothing, and `sd` keeps answering
"SD has not been started". After `sd -stop`, start SD with `sd -start`, or
with `sudo systemctl restart sd.service`, which stops and starts it through the
unit and leaves the unit and the daemon agreeing again. (`systemctl stop
sd.service` is a stop the unit does know about, so `systemctl start` is the
right partner for that one.)

## `sd -start` and `sd -stop` check the real process, not just the segment

SD's shared state lives in a System V shared-memory segment
(`shmget`/`SD_SHM_KEY`), which — unlike a file — can outlive the daemon
process that created it if SD is killed rather than stopped cleanly.
`sd -start` and `sd -stop` validate the daemon's actual process id rather
than trusting the segment's mere existence:

**"SD is already started" is only said when the daemon really is
running**, and it names the process id — the one `ps` and `kill` use.

**If the segment is there but the daemon is not** — what a killed or
crashed SD leaves behind — `sd -start` says so rather than silently
reporting success against a segment nothing is actually serving. Clearing
it is `sd -stop`'s job.

> Check the daemon by hand at any time:
>
> ```
> ps -C sdlnxd
> ```

**A session still attached ten seconds after the stop is ended.** `sd -stop`
and `sd -restart` send every session the termination signal, wait up to ten
seconds for them to leave, and end any process still attached to SD's shared
memory with `SIGKILL`; they say how many they ended, for example `1
process(es) still attached after ten seconds were ended with SIGKILL`. Only a
process that is attached to SD's own segment is touched, and a session ended
this way does not run its own logout.

**The clean-up daemon is started again if it dies.** `sdlnxd` is the process
that notices a session whose process has gone and clears it down, and writes
the audit trail. It runs as its own unit, `sd-lnxd.service`, and `systemd`
starts it again two seconds after a failure (`kill -9`, a crash, the process
being killed for memory). A stop with `sd -stop` is not a failure and is not
restarted. `systemd` allows five starts of the unit in a minute and refuses the
sixth; **every start counts, a restart after a crash and your own
`systemctl restart sd.service` alike**, so five restarts of your own followed by
a crash leave the daemon down. `sudo systemctl reset-failed sd-lnxd` and
`sudo systemctl start sd-lnxd` take it from there. **A plain `sd -start` still
forks a daemon of its own, which nothing watches**; use
`sudo systemctl restart sd.service` when you want the unit to run it. Only one
daemon runs at a time: a second `sdlnxd` finds the first and ends. See
*Installation and the daemon* in the Administrator set.

**A script may capture what `sd -start` prints.** `x=$(sd -start)` or
`sd -start | tee start.log` returns as soon as SD has started. The daemon it
leaves running does not keep the script's pipe: it writes to `/dev/null`
instead, so anything it prints after the start is not seen there. Sent to a
file or a terminal, its output goes there as before.

**A `shmget` System V segment does not survive a reboot** — the kernel
clears its IPC state on every restart, unlike a file on disk. So unlike a
port where a stale segment can persist across a restart, a reboot here
always leaves a clean slate; the "segment present, daemon dead" case above
is specifically about a crash the machine itself did **not** restart from
(SD killed, or `sd.service` restarted, while the box stays up).

## `sh` runs at the account's own Linux permissions, for an account that has `sh-on`

It needs the account's `sh-on` switch, which SDSYS turns on and a new account
does not have; with it, there is no elevation involved — the command runs as
that account's own Linux user. See [Security and the operating
system](12a-security-and-the-operating-system.html).

**Starting `sd` from inside `sh`** is refused. The shell that `sh` and
`os.execute` start is marked as SD's own, and `sd` typed there answers "SD is
already running in this session - type exit to return to it." in every form of
the command. It keeps a second session from being nested inside the first; it
is not a wall, because the mark is an environment variable of that shell.

## The command line

```
sd                  enter the SD account named after your Linux login
sd -a               prompt for an account
sd -a<name>         enter account <name>  -- refused unless it is your own
sd <command>        run one command       -- needs SDSYS, or batch.jobs
sd -quiet           suppress the displays on entry
sd -u               list current users    -- root or sdsys
sd -k <n> | -k all  log out user n, or everybody
sd -start           start the system
sd -stop            stop the system
sd -suspend         suspend updates   -- root only
sd -resume          resume updates    -- root only
sd -d               diagnostic dump   -- root only
sd -m               dump shared memory -- root only
sd --version        report the version
sd --help           this summary
```

**Three of these behave differently from what you may expect.**

**`sd -a<name>` is refused unless `<name>` is your own account.** An
administrator no longer opens somebody else's account without ever being in
their own — they arrive in their own (`sdsys`) and reach the rest with
**`logto`**, which is where SD checks whether they are allowed in.

**`sd <command>` needs SDSYS**, or an entry for that account in
`batch.jobs`. **Any account can be given one** — every account has the same
VOC now, so there is nothing about the account to consider here; SDSYS's own
`batch.jobs` list is what decides what may run. That is what makes scheduled
jobs possible without giving them SDSYS's own rights — see
[Scheduled jobs](04-scheduled-jobs.html).

**`sd -suspend`, `sd -resume`, `sd -d` and `sd -m` need root**, as `-start`, `-stop`,
`-restart` and `-k` do, and otherwise answer "Command requires administrator
privileges". `-suspend` stops every update on the system and the two dumps show every
session and the configuration, so they are not for ordinary users.

**`sd -cleanup` and `sd -u` are for root or the `sdsys` user**, and answer anybody
else the same way: `-u` lists every session on the machine with its user and
process, and `-cleanup` removes other people's entries from the user table. Inside
SD, `listu` shows an ordinary user their own sessions. `sd -status` is for anyone.

**`sd <command>` runs and exits, and is never asked to set a password.** Nor
is any session with no terminal — a scheduled task, or a piped script. **Only
an interactive `sd` with no command after it still asks**, and then only of
an account that has no password yet.

## Where things are

| | |
|---|---|
| Binaries | `/usr/local/bin` |
| Configuration | `/etc/sd.conf` |
| The database | `/usr/local/sdsys` |
| Accounts | `/home/sd/user_accounts`, `/home/sd/group_accounts` |
| Audit trail | `/usr/local/sdsys/audit` |
| Error log | `/usr/local/sdsys/errlog` |
| Elevation helper log | alongside the installer, `sd-elevate.log` |

## Checking the service

```
systemctl status sd.service sdclient.socket
journalctl -u sd.service
```

`systemctl` reports whether `systemd` thinks the units are running;
`sd -u`, run as `sdsys` or root, reports who is actually connected.

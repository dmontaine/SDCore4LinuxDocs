Title: Scheduled Jobs
Subtitle: The administrator's own jobs on root's timers, the commands an account may run unattended, and how SD tells a scheduled run from anything else.

SD runs work unattended in **two ways, and nothing of either kind is allowed or scheduled as
delivered.** Each is a deliberate act of SDSYS, written to the audit trail, and undone the same way.

| | An account's job | An administrator's job |
|---|---|---|
| Runs as | the account's own Linux user, with the account's rights | the `sdsys` user, with the administrator's rights |
| Scheduled by | that user's crontab or `systemd` timer | a `systemd` timer that only root can set |
| May run | a paragraph or sentence of the account, if it is on the account's list | one of two fixed commands |
| Set up with | `set.batch`, or the account view of `tool.jobs` | `set.job`, or the Jobs view of `tool.jobs` |

An account's job can reach only what its account can. **Work that has to reach every account** (a
backup of all of them, an update of every VOC) is an administrator's job.

> **This document is separate so that it can be withheld.** It links to nothing outside the
> administrator set. The walk-through of an account's job, from the paragraph to the crontab line, is
> *Scheduled jobs* in the **Getting Started** set.

## The administrator's jobs

### What a job can run

A job runs **one command from a list the root helper owns**, chosen by an id. No command text comes from
the page, from `set.job` or from the person typing:

| Job | Runs |
|---|---|
| `backup-all` | `backup.account all`: one archive of every account, in the saved backup directory |
| `update-accounts` | `update.accounts all`: every account's VOC refreshed from the shipped records |

Each runs exactly as it does when typed at the prompt; [Account maintenance](01a-account-maintenance.html)
has both. **A backup starts only when every other session has logged out**, so schedule `backup-all`
for a time when nobody is signed on: a run that finds someone still logged in does not back up.

A command that takes an account name or a path is not on the list. The list changes only with a
release of SD.

### Schedules

A schedule is one of five shapes. The root helper turns it into `systemd`'s own calendar form, so no
calendar text is taken from anyone:

| Schedule | Runs |
|---|---|
| `every 5 minutes` (or `10`, `15`, `20`, `30`) | at minutes divisible by that number, every hour |
| `hourly` | at the start of every hour |
| `daily 02:30` | every day at that time |
| `weekly sun 03:00` | that day (`mon` to `sun`) at that time |
| `monthly 1 04:00` | that day of the month, `1` to `28` (every month has it), at that time |

Times are 00:00 to 23:59 in **the machine's time zone**. **A run missed while the machine was off is not
made up**: the next one is at the next time the schedule names.

### `set.job`

`set.job` is in SDSYS's VOC only and is refused to anyone else ("Command requires administrator
privileges").

```
set.job
set.job add name job schedule
set.job change name job schedule
set.job delete name
set.job run name
```

| Form | Does |
|---|---|
| `set.job` | lists the jobs, each with its schedule, its command, when it runs next and how its last run ended |
| `add` | makes a job; refused when one of that name exists (`set.job change` changes it) |
| `change` | gives an existing job a new job id or schedule; refused when there is no job of that name |
| `delete` | stops the timer, then removes the job |
| `run` | starts the job now, exactly as its timer would, and does not wait for it |

**The name** is 1 to 32 characters: a lower-case letter first, then lower-case letters, digits and dashes,
not ending in a dash. **There can be at most 32 jobs.** A time may also be written *hh.mm*.

```
:set.job add nightly backup-all daily 02:30
sd-elevate: job nightly created
sd-elevate: job nightly is scheduled: daily 02:30
:set.job
job nightly: daily 02:30: backup.account all (backup-all)
   next run: Tue 2026-11-03 02:30:00 UTC; last run: never
```

What you see is what the root helper did; the lines it prints about what it is about to do are left
out. `systemd` may add a line of its own when a timer is first switched on (`Created symlink ...`). A
last run shows its end time and what `systemd` recorded of it (`success`, `exit-code` and so on);
`running now` while it runs.

**`set.job` writes no file.** Every change is `sudo /usr/local/sbin/sd-elevate job-set`, `job-delete`,
`job-run` (and `job-list` for the list), which checks the name, the job and the schedule again; the
change is judged on the helper's own success line, not on its exit status alone. When the helper
refuses, what it said is shown, then `The root helper did not do it (status n)`. Each change is written
to the audit trail with its result:

```
set.job add name=nightly job=backup-all result=done schedule=daily 02:30
```

**That a job exists, or does not, is checked against the list just before the change.** The helper
itself makes or replaces the definition, so two administrator sessions acting on the same name at the
same moment are not kept apart: the last one to reach the helper wins.

### The Jobs view of `tool.jobs`

`tool.jobs` is the Scheduled jobs page, in SDSYS's VOC only, in a window of at least 140 columns by 43
lines. **J** shows the Jobs view and **A** goes back to the account commands. The view lists every job
with its schedule, its command, when it runs next and how its last run ended.

| Key | Does |
|---|---|
| **N** | makes a job: a form asks for the name, the job and the schedule |
| **C** or Enter | changes the selected job's job or schedule (its name stays) |
| **D** | deletes the selected job: you type its name in the box |
| **R** | starts the selected job now; the page does not wait for it |
| **/** | goes to the next row of the box you are in whose name holds a text you type (any case; it goes round to the top), since 9 November 2026 |
| **F5** | reads the list again (a run shows there when it has finished) |
| **Ctrl-O** | shows what each command answered, newest first |

The form refuses a name, a job or a schedule the helper would refuse, before anything is sent. Every
change is then shown as its `set.job` command, with the job's command and the schedule in words, and
runs only when you answer Run; **Cancel is what Enter chooses**. The page writes nothing itself.

### A damaged job

The list shows a definition as **damaged** when it is not what the helper would have written: a file in
the definitions directory whose name is not a job name, a link or anything but a plain file, a file
with a line missing, doubled or unknown, or one naming a job id or a schedule the helper no longer
has. The line says why, in one of four ways:

| The line ends | What causes it |
|---|---|
| `not a job name` | a file whose name is not a job name (it was not written by the helper) |
| `not a plain file` | a link, a directory or anything but a plain file under a job's name |
| `damaged` | a line missing, doubled or unknown, or a file over 4096 bytes |
| `the definition does not agree with the helper` | a job id or a schedule the helper no longer has |

```
damaged nightly: the definition does not agree with the helper
```

**A damaged job is not started by hand**: `set.job run` and **R** refuse it (`Job nightly is damaged;
nothing was started`), and so does the root helper. For a damaged **plain file**, `set.job change`
writes it again and `set.job delete` removes it. **Its timer goes on firing until then**, and each run is
admitted only if the definition still names the exact command the unit starts (below); otherwise the run
is refused and does nothing but write the refusal to the audit trail.

A file whose name is not a job name, and a link or anything but a plain file under a job's name, cannot
be changed or removed by the page or `set.job` (the helper refuses both); remove it as root
(`rm /etc/sdcore/jobs.d/`*file*).

## How a run is recognized

A job's run has no login behind it: `systemd` starts it, and nobody signed in. SD therefore does not ask
who logged in, as it does for every other `sdsys` session; it asks two things that only root controls.

1. **The process is in the job's unit.** `systemd` puts the run in the control group of
   `sdcore-job-`*name*`.service`. The `sdsys` user cannot start a system unit or move a process into one.
2. **The definition names this very command.** `/etc/sdcore/jobs.d/`*name* is a plain file owned by root
   with one link and not writable by group or others, in a directory (and `/etc/sdcore` above it) that is
   root's and closed the same way, and its `name=` and `command=` lines are the unit's name and **exactly
   the command the session was started with**.

Only then is the session made the administrator. The audit trail says so, and **every line the run
writes ends `job=`*name***, the journal's copy included:

```
2026-11-03 02:30:01 user=sdsys uid=1001 pid=5120 elevation granted reason=scheduled job job=nightly
```

The root helper admits the run's own calls to it the same way. A process the job starts inherits its
control group but not its command, so it cannot use the grant to run anything else.

**Any other `sdsys` session that is not a login of `sdsys`'s own** (`su sdsys` or `sudo -u sdsys` from
another user's session, a process a service started) is refused as before:
`elevation refused reason=sdsys session without a sdsys login`.

### The `sdsys` user may not use cron or at

A cron or at job of `sdsys`'s is an ordinary password-only `sdsys` login. **The installer puts `sdsys` in
`/etc/cron.deny`** and, where `at` is installed, `/etc/at.deny`; a crontab `sdsys` already had is moved to
`/var/backups/sdcore-sdsys-crontab.`*date* (root only), and its queued at jobs are removed. Scheduled
administrator work is a job on this page. To let `sdsys` use cron again, take it out of
`/etc/cron.deny`; the details are in [Remote administration over ssh](22-remote-administration-over-ssh.html).

## Where a job is kept

| | |
|---|---|
| Definition | `/etc/sdcore/jobs.d/`*name*, root 0644; the directory root 0755 |
| Service | `/etc/systemd/system/sdcore-job-`*name*`.service`, root 0644 |
| Timer | `/etc/systemd/system/sdcore-job-`*name*`.timer`, root 0644, enabled |

```
# an SD scheduled job, written by sd-elevate job-set; changed only by sd-elevate job-set and job-delete
name=nightly
job=backup-all
command=backup.account all
schedule=daily 02:30
oncalendar=*-*-* 02:30:00
```

The service runs `/usr/local/sdsys/bin/sd "backup.account all"` once, as `sdsys` and the group
`sdusers`, from `/usr/local/sdsys`, after `sd.service`. **Change a job only through `set.job`**: a
definition edited by hand is shown as damaged, and a unit edited by hand is written again by the next
`set.job change`.

The ordinary `systemd` commands show the rest, as root: `systemctl list-timers 'sdcore-job-*'` for the
timers, and `journalctl -u sdcore-job-`*name*`.service` for what a run printed.

**Removing SD** (`deletesdcore.sh`) switches every `sdcore-job-*` timer off, removes the timers and
services, then `/etc/sdcore/jobs.d`.

## An account's commands

An account's job is `sd` started with a command, by a crontab line or a timer of the account's own Linux
user. **The login lets it run only a command on the account's list** in the SD system file
`batch.jobs` (`/usr/local/sdsys/batch.jobs`, `sdsys:sdusers 750`, one record per account), and only if
it is a single name with nothing after it and a paragraph (`PA`) or sentence (`S`) of that account's
VOC. SDSYS's own sessions are not held to a list, and SDSYS has none.

### `set.batch`

```
set.batch
set.batch add account command
set.batch remove account command
```

`set.batch` alone lists every account's commands. `add` checks that the command is a paragraph or a
sentence in that account's VOC (the test the login makes) before it adds it; `remove` takes it off, and
an account whose list is then empty has no record left. Each change is written to the audit trail
(`set.batch add account=fred command=my.report`) and takes effect at the next such session:

```
:set.batch add fred my.report
my.report may now be run from the command line in account fred
:set.batch
Account fred may run from the command line: my.report
```

It refuses `sdsys` (the administrator's account has no list), an account that is not registered, and a
name that is not a paragraph or a sentence there.

**Whoever can change the paragraph changes what the job does.** An allowed command runs with the
account's own rights; keep its VOC record where the account's people may change it only if they may also
decide what runs unattended.

### The account view of `tool.jobs`

The page opens on it. **Accounts** lists every registered account but SDSYS with how many commands it
may run that way; Enter or F6 goes to **Commands**, the paragraphs and sentences of that account's VOC,
each allowed or not. Enter or the space bar on one shows the `set.batch` command and what it does, and
runs it only when you answer Run. A name still on the list whose VOC record is gone, or is no longer a
paragraph or a sentence, is shown as such, and Enter takes it off. A name holding a character other
than a lower-case letter, a digit, a dot, a dash or an underscore cannot be sent from the page: it shows
the `set.batch` command to type at the prompt.

**The page does not write the account's schedule**; that is the crontab or timer of the account's
Linux user.

### When the login refuses

A refused run writes `login refused account=`*account*` reason=`*why* to the audit trail; an admitted one
writes `login account=`*account*` command=`*command*:

| Reason | Means |
|---|---|
| `command line carried arguments` | something followed the name |
| `batch.jobs could not be opened` | the list is missing or unreadable |
| `command is not on the account list` | not allowed for that account |
| `no VOC record for the command` | the account has no such VOC entry |
| `VOC type is not PA or S` | it is there, but not a paragraph or a sentence |

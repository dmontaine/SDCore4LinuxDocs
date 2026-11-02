Title: Scheduled jobs
Subtitle: Running an SD command on a timer, and the permit list that decides which ones.

**A cron job or a systemd timer can run an SD command, and only the
commands an administrator has named for it.**

Typing a command after `sd` — `sd my.report` — used to run unconditionally,
with no gate at all: the group-membership test at entry proved *who* was
running it, never *what* it might run unattended. A scheduled job has
nobody at the keyboard to use judgement, so it needed a pre-vetted list
instead, whoever's Linux identity is actually running it.

There are two ways past the gate now:

| | |
|---|---|
| a session logged in as SDSYS | runs anything, exactly as before |
| anything else | runs what is listed for its account in the SD system file `batch.jobs` |

**Nothing changes for a session you type at.** Commands entered at the `:`
prompt are unaffected, and so is plain `sd` with no command after it.

**There is no password anywhere in this.** The job signs in as its own
Linux account and SD puts it in the matching SD account, exactly as it
would for a person at a keyboard. Nothing has to store a credential for the
job to use, and the job grants nobody anything — no other account is in its
group.

## The permit list

`batch.jobs` is a directory file in `/usr/local/sdsys`, so **one record
per account, named after the account**, holding one command name per line.

**Only an administrator can change it.** It is read-only to `sdusers`
(`sdsys:sdusers 750`) — a user who could add a line to their own record
would be granting themselves the command line.

**It is keyed by the account you end up in**, not by the Linux account
name, and the two are usually the same. `sd -a<name>` cannot be used to
reach somebody else's list: that form is refused unless the account is
your own.

**Any account can be given a list.** Every account has the same VOC now, so
there is nothing about the account type to consider here; SDSYS's own
`batch.jobs` record is what decides who may run one.

Both shapes of record are read — one name per line, and a multivalued field 1 —
so a record written with **`ed`** and a record written by a program agree. A name
still has to match exactly.

## What may be listed

Two rules, and both are tested when the command runs rather than when it is
listed:

**1. A single name with nothing after it.** `my.report` may be listed;
`my.report yesterday` may not, and neither will run:

```
A command run from the command line must be a single name with nothing
after it.  Put anything the job needs to vary inside the paragraph or
sentence being run.
```

That is the rule doing the security work. *"It must be in the VOC"* would be
worth nothing on its own — every verb is a VOC entry — so it is the absence of
arguments that stops a listed name being turned into something else.

**2. A paragraph or a sentence in that account.** A VOC entry of type `PA` or
`S`. Anything else — a verb, a file pointer — is refused by name:

```
MY.REPORT has to be a paragraph or a sentence in this account to be run
from the command line, and it is neither.
```

## Setting one up

Four steps, and the first and third need an administrator for a new account.

**1. Write the work as a paragraph** in the account that will run it. A `PA`
record in that account's VOC, with the commands on the lines after the type:

```
:ed voc my.report
```

Saving a record of the VOC needs the account to hold `voc-on`, which a new
account does not have. SDSYS gives it with `modify.account` *name* `voc-on`
(see [Managing accounts](05a-managing-accounts.html)); accounts that existed
at an upgrade have it already.

**2. Check it runs when you type it**, in that account, before putting it on a
timer.

**3. Allow the name in that account**, logged in to the machine as SDSYS:

```
:set.batch add fred my.report
my.report may now be run from the command line in account fred
```

`set.batch` checks that the name is a paragraph or a sentence in that
account before it adds it, writes the account's record in `batch.jobs`,
and records the change in the audit trail. `set.batch remove fred my.report`
takes it off, and `set.batch` alone lists every account's commands. The
administrator's own account has no list.

**Or use the Scheduled jobs page**, `tool.jobs`. It lists every account
with the number of commands it may run this way. Tab or Enter moves to
the account's paragraphs and sentences, each marked as allowed or not.
Enter on one shows the `set.batch` command and what it does, and runs it
only when you answer Run. A name still on the list whose VOC record has
gone, or is no longer a paragraph or a sentence, is shown as such, and
Enter takes it off. A name holding a character other than a lower-case
letter, a digit, a dot, a dash or an underscore cannot be sent from the
page: it shows the `set.batch` command to type at the prompt.

The page does not write an account's schedule: step 4 is done in the
crontab or the timer of the account's Linux user. (The page's **Jobs**
view, below, schedules the administrator's own jobs.)

`batch.jobs` can still be edited directly (`ed batch.jobs fred`, one
command name per line), but `set.batch` makes the same checks the login
makes, so a mistake shows up when you make it, not at the job's first
run.

**4. Create the scheduled job.** Either cron or a `systemd` timer runs it —
what matters is which Linux account the job runs as:

```
# crontab -u fred -e
0 6 * * *  /usr/local/bin/sd my.report
```

The job runs as a Linux account, and that account needs a matching SD
account — that is the whole of the sign-in. There is no password to
configure anywhere in SD for it.

**Do not run it as `sdsys` or via `sudo`.** It is not needed, and the whole
point of `batch.jobs` is a job that runs without administrator rights. A
job that runs as `sdsys` passes the gate on identity alone and never
consults the list, so it would also be a job nobody had approved a command
for — and per [Security](12-security.html), `sdsys` cannot be reached that
way regardless: SD checks the kernel's own audit loginuid (`K$LOGIN.UID`),
set once by a real login and unforgeable by a cron job or a `sudo`'d
shell, and refuses anything that isn't a genuine local login as `sdsys`.

**Use a Linux account you already had** — that is the case the design was
built around.

## When it refuses

**It fails closed.** Every path that does not reach the end of the check leaves
the command refused, and each one writes a reason to the
[audit trail](12a-security-and-the-operating-system.html#the-audit-trail):

| What is wrong | Recorded as |
|---|---|
| the command line carried an argument | `command line carried arguments` |
| `batch.jobs` is missing or unreadable | `batch.jobs could not be opened` |
| the name is not in this account's record | `command is not on the account list` |
| the name has no VOC entry at all | `no VOC record for the command` |
| it has one, but it is not `PA` or `S` | `VOC type is not PA or S` |

The message on the screen for the third of those names both the command and
the account, and says where an administrator grants it:

```
MY.REPORT is not a command that account FRED may run from the command line.

An administrator grants it by adding the name to the account's record in
the SD system file batch.jobs, which only an administrator can change.
```

**A refusal is not a hang.** `sd <command>` is never asked to set a
password it cannot answer — see [Running SD](03-running-sd.html#the-command-line).

## The administrator's own jobs

**Work that has to reach every account runs as the administrator, and
only as one of two fixed jobs.** An account's own job runs with that
account's rights; the administrator's jobs are for what no single account
may do:

| Job | Runs |
|---|---|
| `backup-all` | `backup.account all` |
| `update-accounts` | `update.accounts all` |

**Nothing is scheduled as delivered.** Each job is a `systemd` timer that
only root can set, kept by the root helper in `/etc/sdcore/jobs.d`; the
`sdsys` user's own crontab is refused (see *Remote administration over
ssh* in the administrator's documentation). At each
run `systemd` starts `sd` with the job's command as the `sdsys` user, and SD
makes it the administrator only when the run is that unit's and the
root-owned definition names exactly that command. Every line the run
writes to the audit trail ends `job=`*name*. A run missed while the machine
was off is not made up; times are the machine's.

**A schedule is one of five shapes:** `every 5`, `10`, `15`, `20` or
`30 minutes`; `hourly`; `daily` *hh:mm*; `weekly` `mon`..`sun` *hh:mm*;
`monthly` *1..28* *hh:mm*.

### From the Scheduled jobs page

In `tool.jobs`, **J** shows the **Jobs** view (**A** goes back to the
account commands). It lists every job with its schedule, its command,
when it runs next and how its last run ended. A definition that does not
agree with the root helper is shown as damaged.

| Key | Does |
|---|---|
| **N** | makes a job: a form asks for the name, the job and the schedule |
| **C** or Enter | changes the selected job's job or schedule (its name stays) |
| **D** | deletes the selected job: you type its name in the box |
| **R** | starts the selected job now, exactly as its timer would; the page does not wait for it |
| **F5** | reads the list again (the last run shows there when it has finished) |

The form refuses a name, a job or a schedule the helper would refuse,
before anything is sent. Every change is then shown as its `set.job`
command, with the job's command and the schedule in words, and runs only
when you answer Run. **The page writes nothing itself:** `set.job` asks
the root helper. A damaged job can be changed or deleted, not run; one
whose file name is not a job name can only be deleted, at the prompt
(`set.job delete` *name*), and the page says so.

### From the prompt

`set.job` does the same at the `:` prompt, logged in as SDSYS:

```
:set.job add nightly backup-all daily 02:30
sd-elevate: job nightly created
sd-elevate: job nightly is scheduled: daily 02:30
:set.job
job nightly: daily 02:30: backup.account all (backup-all)
   next run: Tue 2026-11-03 02:30:00 UTC; last run: never
```

What you see is what the root helper did; the lines it prints about what
it is about to do are left out. `systemd` may add a line of its own when
a timer is first switched on (`Created symlink ...`).

`set.job change` *name job schedule* changes a job (`add` refuses a name
that exists and `change` one that does not), `set.job delete` *name*
removes it, its timer first, and `set.job run` *name* starts it now; a
damaged job is not started (`Job nightly is damaged; nothing was
started`), by `set.job` or by the root helper. A time may also be
written *hh.mm*.

**That a job exists, or does not, is checked against the list just
before the change.** The root helper itself makes or replaces the
definition, so two administrator sessions acting on the same name at the
same moment are not kept apart: the last one to reach the helper wins. The name is 1 to 32 characters: a
lower-case letter first, then lower-case letters, digits and dashes, not
ending in a dash. Each change is written to the audit trail with its
result (`set.job add name=nightly job=backup-all result=done
schedule=daily 02:30`).

`set.job` is the same as running
`sudo /usr/local/sbin/sd-elevate job-set`, `job-delete`, `job-run` or
`job-list` at a shell as `sdsys`; it judges each change on the helper's
own result line, and shows what the helper said when it refuses.

Title: SD TCL - The Terminal and the Session: Timers, Dates and Logging
Subtitle: The bell, the inactivity timer, echo, dates, currency, and command logging.

This page continues [SD TCL - The Terminal and the
Session](29-sd-tcl-the-terminal-and-the-session.html).

## The bell

```
bell on
bell off
```

Sets or clears the character SD sends to sound the terminal bell. **Neither form
prints anything**, and `bell` with no keyword is an error rather than a toggle:
*Mode keyword missing or invalid*.

## Clearing type-ahead and stored prompts

```
clear.input
clear.prompts
```

**`clear.input`** discards anything typed ahead but not yet read.
**`clear.prompts`** discards the inline prompt and response text a previous
command left behind. Neither prints anything.

(The run-together spellings `clearinput` and `clearprompts` were second names
for the same verbs and were removed in 2.0-0.)

> **Neither can be demonstrated down a pipe, and `clear.input` should not be
> sent down one at all.** In a piped session the input stream *is* the script,
> so discarding unread input discards the commands that have not run yet —
> including the `off` that would have ended the session. **A run that did this
> hung, was killed, and left a session in the user table that only `sd
> -cleanup`, run as SDSYS, could clear.** Both verbs are for a person at a
> terminal.

## The inactivity timer

```
autologout
autologout n
```

```
:autologout
Autologout is disabled
```

which is the shipped state. Setting a timer ends a session that has been idle
too long — useful on a machine where people walk away from a prompt, and worth
thinking about before enabling on a machine where a long-running interactive job
is normal.

*n* is minutes and 0 turns it off. **It applies to an API session too**: a client that
executes `autologout 10` (`SDExecute("AUTOLOGOUT 10")`) has its server session ended after
ten minutes in which it sent nothing, and its next request fails at once
(see [SD Client API](37-sd-client-api.html)). The setting belongs to the one session that gave it.

**It works in the full-screen programs too.** The screen library, `ide`, the
home screen and every tool page wait for a key one second at a time, and SD adds up the time
spent waiting across such short waits: only a key actually typed (or the break key) starts the period
again, and the logout is the same as at the prompt. A page left open without typing, `tool.sessions`
included, is therefore logged out like any other session. A program that waits for a key with no time
limit behaves as before, and a timed wait exactly as long as the `autologout` period still ends with a
plain timeout. **A program that polls the keyboard with very short timed `keyin`s and does work between
them counts as waiting**, because the polls add up with nothing typed: `autologout` can end it, and
only a key resets the count.

## The command echo: `echo`

```
echo on
echo off
echo
```

**`echo off` stops SD echoing what you type**; with no keyword it toggles.
Neither form prints anything, and `echo off` suppresses its own confirmation
along with everything else.

```
:echo off
:28 DON
:who
28 DON
```

That is one `who` under `echo off` and one after `echo on`. **The first has no
`:who` line above it** — its output ran straight on after the prompt — and
`echo on` produced no line of its own either, because the echo it restores does
not apply to the command that restores it.

**It is not `hush`, and confusing the two wastes time.** `echo` decides
whether your **input** is shown back; `hush` decides whether SD's **output** is
shown at all. A session that has gone completely silent has `hush on` set; one
where the commands vanish but the answers still appear has `echo off`.

## Dates and times

```
date                    today, spelled out
date internal           today as SD's internal day number
date n                  day number n, spelled out
date some-date          that date's day number
time                    the time and the date
time internal           seconds since midnight
```

```
:time
14:10:34 27 AUG 2026
:date
Thursday, 27 August 2026  02:10pm
```

**`date` prints the time and `time` prints the date.** Both print both, in
different formats and a different order, and neither name says so. `date` is
the long spelled-out form and `time` is the short one.

**`internal`** on either gives the raw number a program would see:

```
:date internal
21424
:time internal
51088
```

the day number and seconds since midnight. **`date` with an argument is a
converter, and which way it converts depends on what you give it** — a bare
number is read as a day number and comes back as a date, anything else is read
as a date and comes back as a day number:

```
:date 20000
Monday, 03 October 2022
:date 4 jul 2026
21370
:date zznotadate
Invalid date format
```

`time` takes no argument other than `internal`.

### Which way round a date is read: `date.format`

```
date.format on | off | display
```

```
:date.format display
European date format is off
```

**`on`** selects European (day-first) date format for the session, **`off`**
returns to the default, and **`display`** reports which is in force. If a default
conversion code other than `D` is set, `display` names that too.

**`date.format` with no keyword prints nothing** — like `pterm`, it wants one.

**Changing the date SD reports is a different thing entirely** — `set.date`
is an administrator verb, it sets the date for your session only and not the
computer's clock, and it is in the **administrator documentation** under
*Account Maintenance*.

## Currency and separators: `nls`

```
nls
nls currency | thousands | decimal
nls currency | thousands | decimal value
nls default
```

Three values control how a number is written: the currency symbol, the thousands
separator and the decimal separator. **`nls` with nothing after it shows all
three**, one to a line:

```
Currency symbol     : '$'
Thousands separator : ','
Decimal separator   : '.'
```

Naming one of the three shows just that one. Naming one and a value sets it, and
**`nls default`** puts all three back to `$`, `,` and `.`. A setting lasts for the
session: the next session starts from the defaults. Anything other than the three
names is refused, *"x is not a recognized NLS key"*.

These are the same three values that **`getnls`** and **`setnls`** read and set
from SD BASIC (see [Data Conversion](06-sd-basic-data-conversion.html)). SD Core for Linux
is English only; `nls` has nothing to do with the language of messages, month
names or day names.

Large letters on the terminal, `block.term`, are described with `block.print` in
[SD TCL - Printing and Spooling](28-sd-tcl-printing-and-spooling.html).

## Waiting

```
sleep n
sleep hh:mm{:ss}
```

A number is seconds; a time is *until* that time, rolling over midnight if it
has already passed. **`sleep` with no argument returns immediately** rather than
sleeping for ever — the argument parses as zero.

## A log of the commands a session runs: `command.logging`

```
command.logging {on | off}
```

`on` starts a log of every command this session runs and where it came from;
`off` stops it; with neither word it says whether it is on and where the file
is. The log is a file named `clog.`*user number*`.log` **in the account
directory**, mode 0600 (nobody but its owner can read it), added to and never
emptied. A line is tab separated: the time as an epoch value, the user number,
the login name, the origin and the command.

| origin | |
|---|---|
| `User` | typed at the prompt |
| `Cmd` | the command line `sd` was started with |
| `PA` | a line of a paragraph |
| `Exec` | any other command a program or a menu runs, such as `execute` |

The `command.logging on` itself is not in the log, because the log starts after
it; `command.logging off` is. **openQM writes the file in `TEMPDIR` and has a
`CMDLOG` parameter that logs every session into one directory; SD has neither.**
`TEMPDIR` is `/tmp` unless `sd.conf` says otherwise, a directory anyone can
write to, where another user could create the file first and be handed the log.
A symbolic link left where the file would be made is refused (*The command log
could not be started*). Logging belongs to the session and is off in the next.

## Writing to the error log

```
logmsg text
```

Everything after the verb is the message. It prints nothing, and what it writes
is a stamped, attributed entry in the system error log:

```
27 Aug 26 13:13:31 User 11 (pid 1786, don):
   nightly run finished
```

**The user number, the process id and the account name are added for you**, so
a message does not need to say who wrote it. The log is
`/usr/local/sdsys/errlog`, shared by every session, which makes `logmsg`
the right way for a phantom or a scheduled job to report something a person will
read later — there is no terminal to print to and no transcript kept.

## Reading the documentation

The documentation PDFs the administrator has installed are files in the `pdf`
directory of the shared account (`/home/sd/group_accounts/shared/pdf`), which every
account may read. To read one, copy it to your own computer (for example with `scp`)
and open it there; at the machine itself, open it with any PDF reader. SD does not
start a reader for you. When a help box (F1, `?` or a `[?]` button) has more in the
documentation, its last line names the PDF.

## See also

[SD TCL - The Command Processor](19-sd-tcl-command-processor.html) ·
[SD TCL - Printing and Spooling](28-sd-tcl-printing-and-spooling.html) ·
[SD Basic - Terminal Input and Output](12-sd-basic-terminal-input-and-output.html).

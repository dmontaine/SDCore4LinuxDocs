Title: The Audit Trail
Subtitle: What SD writes to its audit trail, who writes it, where it is kept, how it is rotated, and the full-screen page that reads it.

SD writes **one line to the audit trail for every act that changes who may do what, or that crosses a
boundary**: a sign-on, a refused request, an account created or changed, a gate turned on, a backup, a
command run from a toolkit page. The trail is a text file of the SDSYS system directory. This page
says what a line looks like, who is able to write one, how the file is kept, and how to read it.

> **This document is separate so that it can be withheld.** It links to nothing outside the
> administrator set. Where a user-set page is worth naming, it is named in words.

## A line

```
2026-10-25 14:03:11 user=fred uid=1001 pid=48213 modify.account net-on account=fred
2026-10-25 14:03:40 user=sdsys sudo=don uid=1002 pid=48990 tool start app=tool.audit
```

A line is the time, then `user=` (the operating-system user that made the entry), `sudo=` when that user
got there through `sudo`, `uid=` and `pid=`, then the **event words**, then any number of `key=value`
pairs. The event words come first and are all lower case (`login`, `modify.account`, `api refused`,
`tool start`); a pair's key is lower case too; a value is whatever a person typed or the system knows
(an account name, a reason) and keeps its case. A value may hold spaces: a word that holds no `=` after
a pair belongs to that pair's value.

## Who writes it

**The user, uid and pid on a line are not the session's word.** Every session sends its record to the
audit daemon (`sdlnxd`, started at boot by `sd-lnxd.service` and again if it dies), which runs as root,
listens on `/run/sd/audit.sock`, and writes `user=` and `pid=` from the credentials the kernel reports for
the sending process. A line cannot name someone else. If the daemon is not running a session appends
the line itself and the user number comes from the session; the same record also goes to the system
journal (`journalctl -t sd_Log`, facility authpriv), where journald stamps the sender's real user and
process.

The daemon takes at most **600 records from one operating-system user in any 60 seconds** and drops the
rest; when that user's window is over it writes one line saying how many were dropped. The limit is
compiled in and is not a setting.

## Where it is kept

| | |
|---|---|
| File | `audit` in the system directory (`/usr/local/sdsys/audit`) |
| Owner and mode | `sdsys:sdusers`, mode 600 (620 on an install made before 24 October 2026; the installer puts it right) |
| Append only | the installer sets the append-only attribute (`chattr +a`) where the file system has it; if it cannot, it says so, and the file is then protected by its mode alone |
| Rotation | at one megabyte the daemon (and `sd -start`) renames it to `audit.yyyymmdd-hhmmss` and starts a new file with the same owner, mode and attribute. A rotated file is not pruned by SD: that is the site's decision, and it starts with `chattr -a` |

Only `sdsys` and root can read it. **SDSYS reads it with its own sign-on**; no other account can.

## Reading it: `tool.audit`

`tool.audit` is a page in SDSYS's VOC only. It needs a window of at least 140 columns by 43 lines, like
the other toolkit pages, and it asks the kernel for the administrator before it reads anything.

The top box names the file shown, its size, the lines loaded, whether older lines remain, the filters in
force and whether the page is following the file. The list under it is the trail, the oldest loaded line
at the top and the newest at the bottom, one row to a line: time, user, event words, then the pairs. The
box at the foot shows the whole line under the cursor, wrapped, and the same line cut into its parts.

**The page reads from the end of the file, in blocks, and never reads a large trail whole.** It opens
on the newest 200 lines that pass the filter; when the cursor goes above the first line it loads 200
more. It keeps at most 3000 lines; beyond that it drops the newest while you go back and the oldest
while you follow. A last line that has no line end yet (the daemon is writing it) is left until it is
whole.

| Key | What it does |
|---|---|
| Up, Down, PgUp, PgDn | move; above the first loaded line, older lines are loaded when the file has them |
| Home, End | the first loaded line; the newest line (End reads the file again) |
| F | asks, one after another: from, to, event words, account, user, text. `from` and `to` are the start of a time stamp (`2026-10-25`, or `2026-10-25 14:30`; `to` with only a date includes the whole day). Event, account, user and text are matched without regard to case; `account` is the line's `account=` value, `user` its `user=` or `sudo=`. Esc leaves every filter as it was |
| C | clears the filters |
| D | goes to the first line at or after a time; no filter changes |
| O | shows the next audit file: the current one, then the rotated ones, newest first |
| L | follows the file: new lines are read every three seconds, and the cursor stays on the newest line if it was there |
| X | saves the lines loaded to a record of the `$HOLD` file of your account, named `audit.yyyymmdd.hhmmss`, and writes the audit line `tool export app=tool.audit lines=n record=id`. `ED $HOLD id` reads it |
| F5 | reads again |
| F1, ? | explain the page |
| Ctrl-Q | leave |

**The page changes nothing.** It runs no command and writes no account or system record. Opening it
writes `tool start app=tool.audit`, and X writes the one export line; both are on the trail.

## What the page does not do

It does not show an account holder's own lines: the trail names every account, user and address on the
machine, and a view limited to one account would need the kernel to filter, which has not been built. It
does not edit, delete or prune a line, and it cannot read a file that only root can read.

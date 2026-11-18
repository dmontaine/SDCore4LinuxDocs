Title: Accounts and Security: The Other Keywords
Subtitle: The recovery copy, file transfer, where a session starts, and the other modify.account words.

This page continues [Accounts and Security: Changing One
Account](01-accounts-and-security-6-modify-account.html).

### The other keywords

| | |
|---|---|
| **`ssh`** \| **`api`** \| **`both`** \| **`none`** | what the account's remote access **is**. Absolute: `api` takes ssh away |
| **`ssh-key-on`** \| **`ssh-key-off`** | ssh sign-in with a key, for a user account whose Linux user SD made (see [Signing in over ssh with a key](01-accounts-and-security-8-home-screen-ssh-keys-passwords.html#signing-in-over-ssh-with-a-key-ssh-key-on-and-ssh-key-off)). **Off as delivered**; independent of `ssh`: the account still needs its ssh route |
| **`sh-on`** \| **`sh-off`** | the `sh` verb |
| **`os-on`** \| **`os-off`** | `OS.EXECUTE`, the screen editors, the embedded Python, and operating-system paths outside the account's own directory (see above) |
| **`sd-on`** \| **`sd-off`** | the directories of other SD accounts the user could `logto` (see above) |
| **`voc-on`** \| **`voc-off`** | saving a change to a VOC (see *The edit switches*) |
| **`bp-on`** \| **`bp-off`** | saving a change to a program file, and compiling and cataloging |
| **`dict-on`** \| **`dict-off`** | saving a change to a dictionary |
| **`recovery-on`** \| **`recovery-off`** | whether the `ide` keeps a recovery copy of text that was not saved (see *The recovery copy*). Not a gate; **off as delivered**; user accounts only |
| **`xfer-on`** \| **`xfer-off`** | moving plain-text files in and out with an sftp client over the ssh login (see *File transfer*). **Off as delivered**; user accounts only; needs `XFER=1` in `sd.conf` as well |
| **`net-on`** \| **`net-off`** | the right to use a server defined for SDNet (see *The NET switch*) |
| **`shared-read-on`** \| **`shared-read-off`** | opening the files of the `shared` account by name. **On unless the field says no** (see *The shared account*) |
| **`shared-write-on`** \| **`shared-write-off`** | writing to the files of the `shared` account. Off unless the field says yes |
| **`files-on`** \| **`files-off`** | the files-only API login: membership of the Linux group `sdfiles` (see *The files-only route*). Independent of `ssh`/`api`/`both`/`none`: those words leave it alone |
| **`files-write-on`** \| **`files-write-off`** | the right to CHANGE files over the files-only login: membership of the Linux group `sdfileswrite`, which needs `files-on` first (`files-off` takes every files group away) |
| **`files-admin-on`** \| **`files-admin-off`** | the right to ADMINISTER files over the files-only login: membership of the Linux group `sdfilesadmin`, which needs `files-on` and `files-write-on` first (see *Administering files*) |
| **`ai-on`** \| **`ai-off`** | the right to use the AI the administrator has chosen: membership of the Linux group `sdaiusers` (see [The AI](01-accounts-and-security-5-files-write-ai-pointers.html#the-ai-ai-on-and-ai-off)) |
| **`start-menu`** \| **`start-terminal`** \| **`start-default`** | where a session on a terminal starts (see *Where a session starts*) |
| **`pins-on`** \| **`pins-off`** | whether the person may add their own programs to the home screen |
| **`sdsys-on`** \| **`sdsys-off`** | whether the `sdsys` user is in the account's Linux group, so that SDSYS can write the account's files; user accounts only (see [The Master Files: The Group and the Modes](19c-the-master-files-group-and-modes.html)) |
| **`suspended`** \| **`unsuspended`** | whether the account can be entered at all |
| **`add`** \| **`delete`** *user* | put a Linux user in, or out of, the account's group |

**The first group is absolute and the second is not.** `ssh`/`api`/`both`/
`none` are four names for one state, so whatever is not named is withdrawn
(of ssh and the API: `files-on` is its own setting and is not withdrawn by them).
`sh-on` and `os-on` are two independent switches over two separate settings,
so **`sh-off` says nothing about `OS.EXECUTE`** and leaves it alone; the
other switches are each their own as well.

After either pair SD says where the account **now** stands, both fields at
once, so that a command that did only what it named is plain to see:

```
:modify.account fred sh-on
Account fred has SH yes, OS.EXECUTE no
:modify.account fred os-on
Account fred has SH yes, OS.EXECUTE yes
:modify.account fred sh-off
Account fred has SH no, OS.EXECUTE yes
```

Asking for what is already so changes nothing and says so ("fred already had
that access; nothing changed"). A route word reports the route in the same
way ("SD routes for fred: ssh and the API." — "fred has no remote access:
not ssh, not the API").

**A change takes effect the next time the account is entered.** The setting
is read when a session signs in, and for `sh`, `os`, `sd`, `net` and the two
`shared` switches again when it `logto`s into the account (the three edit switches
are read at sign-on only),
so a session already open keeps what it started with. To take a grant away from somebody
who is signed in now, change the setting and then end their session.

**Every one of these words is written to the audit trail** (`modify.account
sh-on account=fred` and its siblings), and **SDSYS is never a target**: the
account is refused before the word is read, whatever you asked for, with
*"Account name is invalid"*. A group account
is refused too for the `sh-on`/`sh-off`/`os-on`/`os-off` forms: it has no
Linux user to hold the switch.

**Upgrading keeps what accounts have.** The installer switches `sh` and
`OS.EXECUTE` on, once, for every user account that exists when you upgrade
and whose switch is still blank (an account told `no` stays `no`; ssh and the API are left exactly as they were), so that nobody loses a
command they were using, and in the same way `voc-on`, `bp-on` and
`dict-on`, once, for the same user accounts. This happens when the installer
is run by the user whose own account already exists; a different OS user
installing over existing accounts does not run it. Group and other accounts
are left off on purpose. **`net-on` is not part of it**: nothing used SDNet
before, so every existing account has it off. **The `shared` switches are not part
of it either**: a blank field already reads as `shared.read` on and `shared.write`
off, which is how they are delivered, so every existing account can read the
`shared` account's files and none can write them (take the read right away with
`shared-read-off` before you put anything private there). **Neither is `files-on`**: the
`sdfiles` group is made empty, and nobody is in it until you say so. You can then turn them off one account at a time,
and a later install does not turn them back on. Only accounts made after the
upgrade start with everything off.

### The recovery copy: `recovery-on` and `recovery-off`

```
modify.account account recovery-on | recovery-off
create.account user <name> recovery-on
:modify.account fred recovery-on
Account fred keeps a recovery copy of unsaved editor text: yes
```

With `recovery-on` the `ide` of that account copies the text of every record it has changed and not
saved: after a second without typing, before it hands the screen to a program, and when the session
ends. A hung-up terminal, a lost connection or an abort then does not lose the text. **The copy sits in the person's own Linux home**, in `~/.local/state/sd/recovery/<account>/` (the home the
password database gives their Linux user, never the `HOME` variable), one file per record, readable only by
the person, **outside every account**; it is deleted when the person saves, closes or quits normally, and the
next time the record is opened the `ide` asks whether to use the copy, delete it, or leave the record
unopened (which keeps it). The record itself is never changed until the person saves. `sed` keeps
no copies.

* **Off as delivered.** `create.account` and an existing account have it off until you say so. `recovery-off`
  is the word for `modify.account` only (as `pins-off` is); `create.account` takes `recovery-on` alone, and
  the audit line of a `create.account` that used it ends `gates=` with `recovery-on` among the words.
* **User accounts only, as the verbs have it.** `recovery-on` for a group or other account is refused
  ("... is not a user account, and a recovery copy is kept only in a user account, for its own person; nothing
  was changed"). The administrator is not given a copy either, by the same rule.
* **Where, and when there are none.** The copies are made only when the person's home and every directory
  below it (`.local`, `state`, `sd`, `recovery`, the account's own) are real directories of that Linux user
  that nobody else can write, and every directory **above** the home belongs to root or to that user and
  cannot be written by group or other (a sticky one such as `/tmp` excepted). A home under a group-writable
  directory therefore gets no copies, and the `ide` says the copy could not be written; the text is still in
  the editor. A person who runs SD as root has no home that is trusted and gets none.
* **You cannot read the copies, by design.** `modify.account` runs as `sdsys`; the directories and the files are
  mode 700 and 600 for the person. `recovery-off` stops new copies; copies already made stay and are still
  offered to the person.
* **When it reaches a session.** `recovery-off` stops new copies at once. A running `ide` learned at its start
  whether to keep copies, so `recovery-on` reaches it the next time the person starts the `ide`.
* **The copies are not part of the account.** `backup.account` archives do not contain them (they are in the
  person's home, not in the account), so a text that was not saved never ends up in a backup that
  the administrator can read; the person's own backup of their home does contain them. `restore.account`
  puts the account back with the switch it had.

### File transfer: `xfer-on` and `xfer-off`

```
modify.account account xfer-on | xfer-off
create.account user <name> xfer-on
:modify.account fred xfer-on
Account fred may move files over its ssh login (receive / send): yes
```

With `xfer-on`, and with `XFER=1` in `/etc/sd.conf`, the account's person can move plain-text files into and
out of their own account with an sftp client (OpenSSH `sftp`, WinSCP, FileZilla) signed in with the same
login as for ssh. They open each transfer themselves, from their SD session, with `receive` or `send`
(*User: Moving Files In and Out*); nothing can be moved before that command is typed or after it ends.

**What turning it on opens, plainly.** That person can then bring text of their choosing into the account
from another machine, and take copies of the account's records out to another machine. That is all it
opens, and it is held to this:

* **Off twice as delivered.** `XFER` is 0 and every account has the switch off; both must be on. Neither is
  changed by an upgrade.
* **One directory.** Files come in to `xfer.in` and go out from `xfer.out`, two directory files in the
  account's own directory, and the client can reach nothing else: no other directory, no path, no link is
  followed, and nothing is made, renamed or removed except a file the same connection has just sent. The
  server is SD itself; there is no shell and no system sftp server behind it.
* **Plain text only.** A file with a NUL byte or one of the bytes 248 to 255 is refused, in either
  direction, and so is a name that is not a plain file name. `XFERKIND` narrows it to the extensions you
  list. `XFERFILE` and `XFERSLOT` bound the size of a file and of a whole transfer; `XFERWAIT`, `XFERIDLE`
  and `XFERMAX` bound the time (*Configuration: File transfer over ssh*).
* **Nothing is replaced** unless the person typed `receive overwrite`.
* **User accounts only, and the person's own.** A group or `other` account is refused the switch ("... is
  not a user account, and file transfer is only for a user account, for its own person; nothing was
  changed"), the transfer is opened from the account named after the Linux user and not from one reached
  with `logto`, and the administrator (`sdsys`) has no transfer at all.
* **It needs the ssh route.** The client signs in over ssh, so an account with no `ssh` route cannot
  connect. A file that arrives is only a record in `xfer.in`: bringing a program in does not compile or run
  it, and what the person may then do with it is what the account's other switches allow.
* **Everything is in the audit trail** ([The Audit Trail](21-the-audit-trail.html)): each opening and closing, each connection with
  the address it came from, each file with its size and SHA-256, and each refusal with its reason.

A change takes effect at the next connection: the register is read each time a client connects. To end a
transfer that is under way, `logout` the person's session or the connection (it shows in `listu` as `sftp`).

### Where a session starts: `start-menu`, `start-terminal`, `start-default` and `set.start.default`

A session on a terminal starts either in the **home screen** (a screen of tiles: the
account's tools, a terminal, switch account and sign out; the User's guide has the
page `29a`) or at the **command prompt**. **You decide, account by account**, and you
decide what an account with no setting of its own does:

```
modify.account fred start-terminal       fred starts at the prompt, whatever the default is
modify.account fred start-menu           fred starts in the home screen, whatever the default is
modify.account fred start-default        fred follows the default (the register field is made empty)
set.start.default terminal               accounts that follow the default start at the prompt
set.start.default menu                   ... or in the home screen
set.start.default                        says which it is now
```

* **The default is `menu` as delivered.** `set.start.default` writes the word to the
  file `start.default` in the sdsys directory; the file is absent until you use the verb,
  and absent means menu.
* **EVERY EXISTING ACCOUNT HAS NO SETTING OF ITS OWN**, so after an upgrade each follows
  the default and starts in the home screen. To keep the old start for everyone, run
  `set.start.default terminal` (as SDSYS); to keep it for some,
  `modify.account name start-terminal`.
* The setting is **field 16** of the account's register record. `modify.account` writes it;
  nothing else needs to change, and it applies at the person's next sign-on, and when they type
  `logto` at the prompt to enter the account. It may be set on any kind of account.
* **It is not a wall.** Starting in the home screen confines nobody: its *Terminal* tile gives
  the ordinary command prompt (and `exit` comes back). To keep a person from a prompt you would
  need a setting that removes the prompt itself, which SD does not have.
* The screen is never given to a session that cannot use it: a window under 140 by 43, a pipe,
  a phantom, an API server, or a `logto` that a program ran with `execute`. Scripts and
  scheduled jobs are unchanged.
* `modify.account` says `Account fred starts at: menu` (or `terminal`, or `system default`) and
  `fred already starts that way; nothing changed` when the word is the one already set. It is
  audited as `modify.account start-menu account=fred`, and `set.start.default menu` is audited
  as `set.start.default menu`.
* `create.account` takes `start-menu` and `start-terminal` too, so an account can be made
  with its start in one command (see *Making an account*); `start-default` is not a word of
  `create.account` (an account made without a start word follows the default already).

## Continued in

[Accounts and Security: The Home Screen, ssh Keys and
Passwords](01-accounts-and-security-8-home-screen-ssh-keys-passwords.html) —
the home screen's tiles, ssh keys, suspension, the grant and passwords.

Title: Accounts and Security: Changing One Account
Subtitle: modify.account, tool.accounts and tool.gates.

This page continues [Accounts and Security: File Writing, the AI and VOC
Pointers](01-accounts-and-security-5-files-write-ai-pointers.html).

## Changing one: `modify.account`

```
modify.account account add | delete  <user.name>
modify.account account ssh | api | both | none
modify.account account ssh-key-on | ssh-key-off
modify.account account sh-on | sh-off
modify.account account os-on | os-off
modify.account account sd-on | sd-off
modify.account account voc-on | voc-off
modify.account account bp-on | bp-off
modify.account account dict-on | dict-off
modify.account account recovery-on | recovery-off
modify.account account xfer-on | xfer-off
modify.account account net-on | net-off
modify.account account shared-read-on | shared-read-off
modify.account account shared-write-on | shared-write-off
modify.account account files-on | files-off
modify.account account files-write-on | files-write-off
modify.account account sdsys-on | sdsys-off
modify.account account start-menu | start-terminal | start-default
modify.account account pins-on | pins-off
modify.account account suspended | unsuspended
```

**More than one action in a command.** Any number of the
words above except `add` and `delete` may follow the account, in one command:
`modify.account fred sh-on os-on voc-on bp-on`. SD reads every word first and
then carries out all of them, or none of them:

* **An unknown word, two words that set one access to different states, or
  `add` / `delete` among other words refuses the whole command before anything
  is changed**, and the refusal names the word: `sh-on` with `sh-off`, `ssh`
  with `api` (say `both`), `files-off` with `files-write-on`, and
  `files-admin-on` with `files-off` or `files-write-off` are the conflicts.
* **The words are carried out in one fixed order whatever order they were
  typed:** the route words, then `sh`, `os`, `sd`, the three edit switches,
  `recovery`, `xfer` and `net`, then the shared-account words, then the files
  words (`files-on` before `files-write-on`, which needs it, and that before
  `files-admin-on`), then `ai-on` / `ai-off`, `ssh-key-on` / `ssh-key-off` and
  `sdsys-on` / `sdsys-off`, the start and pins words, and the suspension last.
  Each is reported and audited exactly as if it had been given alone.
* **A command of more than one action ends with a line** saying which were
  carried out, and if one could not be (a refusal such as `sh-on` on a group
  account, or a Linux group change that failed) the others are still carried out
  and the line names the one that was not.

```
:modify.account fred os-on sh-on
Account fred has SH yes, OS.EXECUTE no
Account fred has SH yes, OS.EXECUTE yes
Account fred: 2 actions carried out: sh-on, os-on
:modify.account fred sh-on sh-off
sh-on and sh-off set the same access to different states, and nothing was changed: give one of them
:modify.account fred voc-on bogus
bogus is not a modify.account action, and nothing was changed: give modify.account with an account and no action to see them
:modify.account hr voc-on sh-on
Account hr has VOC.EDIT yes, BP.EDIT no, DICT.EDIT no
hr is a group account and has no Linux user, so it has no shell to permit
Account hr: NOT every action was carried out. Done: voc-on. Not done: sh-on
```

`add` and `delete` take one user name and stand alone: among other words, or
with a word after the user name, they are refused with the message
*add and delete take a user name and stand alone, and nothing was changed: ...*.
The same word twice is one action.

### The accounts on one screen: `tool.accounts`

```
tool.accounts
```

A full-screen page in SDSYS's VOC only (a window of 140 columns by 43 lines or more; in a bigger window this page, like every
administrator page, uses the whole window, with more rows and wider boxes, and follows a resize). The list is every
registered account but SDSYS: its name, its kind (user, group or other), whether it is suspended, **the
gates that are on for it** (read the way `tool.gates` reads them: the register and the Linux groups) and
how many sessions are signed on in it. The box at the foot shows the account under the cursor as the
register and `/etc/group` give it: its path, its Linux user and group, its routes, a group account's
members, the gates that are on and who is signed on in it. **The gate switches are `tool.gates`'s, not
this page's**: a new account has every gate off, as the verb makes it.

| Key | Runs |
|---|---|
| `S` | `modify.account name suspended`, or `unsuspended` when the account is suspended already |
| `A` | `modify.account group add user`, on a group account, for the Linux user you type |
| `R` | `modify.account group delete user`, taking one away |
| `C` | `create.account group name no.query`, `create.account other name path no.query`, or `create.account user name {none\|ssh\|api\|both}` |
| `X` | `delete.account name {remove.home} no.query`, from one dialog where you type the account's name and press Run |

Each shows its command and what it does in a box answered Run or Cancel, **and Cancel is what Enter
chooses**. The verbs ask for the administrator again and write their own audit lines; the page runs
nothing else. **`/`** goes to the next account whose name holds a text you type (any case; it goes
round to the top): the letters are this page's commands, so `/` is how you find an account by typing. **One of them is not run through the page**: creating a user account hands
the terminal to the verb, because `create.account user` asks for the new person's password at a prompt of
its own that shows nothing; nothing typed there passes through the page, and when the verb ends the page
takes the screen again and shows what is registered now. **`X` is one dialog, not a box**: you type the
account's name, choose for a user account whether its home directory is kept (the default) or removed, and
press Run; the page then runs `delete.account name {remove.home} no.query`, since the dialog has asked.
In the create dialog the kind and the doors are chosen from a row of words (Left, Right or the space bar),
not typed. A suspended
account is refused by LOGIN, ssh and the API; sessions already signed on in it keep running until they
end; nothing changes in Linux, so lifting the suspension costs nothing. `F5` reads everything again, `F1`
explains the page and `Ctrl-Q` leaves. Opening the page writes the audit line `tool start app=tool.accounts`.

### Every account against every gate: `tool.gates`

```
tool.gates
```

**The gate matrix** is a full-screen page for the administrator (SDSYS's VOC only; it
is refused, before anything is read, to anyone else: in every other account the same verb
is the account holder's read-only "what my account may do" page, described in the User
set under *What this account may do*). One row for each registered
account but SDSYS, one column for each gate the system has, in the order
`modify.account` carries them out: `ssh api sh os sd voc bp dict xfer net sh-rd sh-wr files
f-wr f-adm ai key home sock`. **`key`** is ssh key sign-in (the words `ssh-key-on` and
`ssh-key-off`, *Signing in over ssh with a key*, below): for a user account whose Linux user SD
made, off as delivered, and turning it ON asks you to type the account's name; a dash for
any other account. With this column an account's name is cut to ten characters in the
matrix and shown in full in the box below it. **`xfer`** is file transfer over the ssh login (the words `xfer-on`
and `xfer-off`, *File transfer*, below): for a user account only, like `sh` and `os`; it is
off as delivered, it works only while `XFER` is 1 in `sd.conf` and the account has the
`ssh` gate, and because it opens a door from the network into the account's transfer
folders, turning it ON asks you to type the account's name. **`home`** is where a session of the account starts: ON is
the home screen, off the command prompt (the words `start-menu` and `start-terminal`).
An account that has never been given either follows the system's default, which is the
installer's answer to *Start new sessions at the home screen or at the command prompt?*
(and `set.start.default` changes it); `modify.account NAME start-default` puts an account
back on the default. It applies to every kind of account, and A and N leave it alone. A cell says **ON**, **off**, a **dash** (the gate does not apply
to this kind of account: ssh, api, files and ai are routes for a person, and a group or
other account has no Linux user of its own) or **plan** (not built yet; sockets). A star
after a cell is a change you have queued; the cell shows the state it would have.
Under the matrix a box says, for the cell under the cursor, what the gate is: its two
words, what ON allows, what OFF still allows, when a change reaches the person, whether
it reaches beyond SD and what it is as delivered. A second box lists the accounts that
have a gate on which reaches beyond SD, and a third the live sessions of the account
under the cursor.

| Key | What it does |
|---|---|
| arrows, a click | move over the cells |
| Enter or the space bar | queue the opposite state for the cell; again takes it back |
| R | run the queued changes of the account on the cursor's row |
| U | drop them |
| T | queue OFF for every gate of that account that is off as delivered and on now |
| A | all gates on: queue ON for every gate of that account that can change (also in the Gates menu) |
| N | all gates off: queue OFF for every gate of that account that can change (also in the Gates menu) |
| F | change which accounts are shown: all, accounts of persons, accounts with a gate on that reaches beyond SD |
| / | go to the next account on show whose name holds a text you type (any case; round to the top) |
| F5 | read the machine again (a queued change is kept) |
| F1, `?`, a click on the `[?]` | explain the matrix |
| Ctrl-Q | leave; when anything is queued, a box asks first: Run the changes, Leave without them, or Cancel (the default) |

**The page writes nothing itself.** The queued changes of one account become ONE
command, `modify.account name word word ...`, shown with its effect in a box that is
answered Run or Cancel (Enter alone is Cancel). The verb reads every word before it
changes anything, so a conflict is refused whole. After the command the page reads the
machine again and shows the verb's own words, so a cell changes because the system
changed, never because the page said so. Every change is audited by the verb as if you
had typed it.

* **Leaving does not drop a queue silently.** Ctrl-Q, or File > Quit, with changes
  queued and not run shows the commands they would be and asks: Run the changes, Leave
  without them, or Cancel. Run the changes shows R's own box for each account in turn,
  with the account's name to type where a gate reaches beyond SD. The page closes only
  when every command ran without a refusal or an error and nothing is left queued;
  otherwise it stays open and shows the message of the account whose command did not
  succeed. Enter and Esc are Cancel. With nothing queued the page leaves at once.
* **A and N only queue.** A quick way to set an account up is **A**, then **Enter** on
  each gate it should not have, then **R**: nothing changes until the box is answered
  Run, and the box still asks for the account's name when a gate that reaches beyond SD
  is turned on. A and N skip a gate that is planned, one that does not apply to the
  kind of account, and `sh` and `os` for an account that is not a person. **T** is the
  narrower "all off": it queues OFF only for what is on and off as delivered
  (`shared-read`, which is on as delivered, is left alone).
* **Turning ON a gate that is off as delivered says so**, and says that leaving it off is
  the tighter choice. **Turning ON a gate that reaches beyond SD** (ssh, api, sh, os,
  sd, net, files, files-write, files-admin, ai, ssh-key) **asks for the account's name to be
  typed**; turning anything OFF does not.
* **ssh and api are one setting** in the verb: the words `ssh`, `api`, `both` and `none`
  SET the pair. The page therefore sends the one word that gives the pair of states you
  queued, and its box says which.
* **files-write needs files, and files-admin needs files-write.** A queue that breaks
  that is refused by the page before the box opens, and the verb refuses it again.
* **A group or other account cannot have `sh` or `os`:** the verb refuses them in both
  directions (a shell granted to a group would be a shell granted to whoever its Linux
  group admits). The page says so instead of queueing them.
* **A change does not reach a session that is already running.** The box says when it
  reaches the person: the next sign-on (voc, bp, dict), the next account entry (sh, os,
  sd, net, shared), the next login (ssh, api, files) or the next request (ai).
* **Home-screen settings are not gates and are not on this page:** `pins-on` / `pins-off`
  and the three start words are managed on the menu management page (`tool.menus`,
  below).

## Continued in

[Accounts and Security: The Other
Keywords](01-accounts-and-security-7-other-keywords.html) — the other
keywords, recovery, file transfer and where a session starts.

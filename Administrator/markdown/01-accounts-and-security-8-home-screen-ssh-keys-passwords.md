Title: Accounts and Security: The Home Screen, ssh Keys and Passwords
Subtitle: set.tile, pins-on, ssh-key-on, suspended, add and delete, and modify.password.

This page continues [Accounts and Security: The Other
Keywords](01-accounts-and-security-7-other-keywords.html).

### What the home screen shows: `set.tile`, `pins-on` and the menu management page

```
tool.menus
```

**Menu management** is a full-screen page for the administrator (SDSYS's VOC only; it
is also a tile on the administrator's own home screen). It lists every account but
SDSYS with where it starts, whether it may add its own programs, and the tiles turned
off for it; for the account you select it shows the standard tiles (the six of the
account, the seven development tiles and the Recent group: 14 rows after the two settings
above them) with `[x]` on and `[ ]` off, and a box that says in plain words what the
settings mean. **It writes
nothing itself:** every change is the command it will run, shown with its effect in a
box you answer *Run* or *Cancel* (Cancel is the button Enter chooses), run by the same
verbs you can type, and the line under the page is the verb's own answer.
**Every setting has a `[?]` at the end of its row** (and one on the accounts list and on
the system default): F1 or `?` on the selected row, or a click on the `[?]`, opens a box
that says what the setting means, ending with the name of the administrator's guide
PDF that says more (in the shared account's `pdf` directory), and a *Close* button. The text is the record of that setting in
the file `context.help` of the shared account.

```
set.tile                          says which tiles are off, one line for each account that has any
set.tile account tile off         turn a tile off for that account
set.tile account tile on          turn it on again
modify.account account pins-on    the person may add their own programs to their home screen
modify.account account pins-off   they may not (the delivered state)
```

* **Tiles are on as delivered and are turned off one account at a time**; there is no
  setting for every account. The standard tile ids are `editor`, `ide`,
  `terminal`, `keys`, `switch` and `signout`, the seven development tiles (`files`, `voc`,
  `dict`, `query`, `bulk`, `catalog` and `test`) and `recent`, which is not a tile but the
  Recent group (below): 14 ids, the ones the page draws and the rows of the *Menu* box of the
  menu management page. **Sign out cannot be turned off**, and neither can the **Back** tile of a sub-menu page: a person must always be able to
  leave. Any other id is accepted and said not to be standard (it would apply to a tile of
  that name in a page of the account's own).
* **`recent`: the Recent group.** A group at the top of the home screen with the tiles the
  person started last, newest first, six at most. **It is off as delivered, and it is the
  person's to turn on** (the *Recent group* entry of the View menu of their home screen); it
  keeps its list in the person's own file `&menus&`, as the record `recent`, and writes
  nothing while it is off. **`set.tile account recent off` is the administrator's wall:** the
  group is then not on that account's page, nothing is read or written for it, and the View
  entry cannot be chosen; the list the person kept stays in their file, and `set.tile
  account recent on` gives the choice back (it does not turn the group on). The list holds
  tile ids and never a command: each recent tile is built from the page as it is, so a tile
  that is off for the account is not offered, and a record edited by hand cannot make the
  page start anything it does not already offer.
* **Sub-menus.** The home screen can open a second page of tiles from a tile, with a Back
  tile, Esc and the path on the status line (the User's guide, page 29a). The delivered page
  declares none, so there is nothing for you to set; a tile of a page of your own that opens
  one is declared in the page table of the `home` program, not in a file.
* The setting is **field 17** of the account's register record (tile ids separated by
  spaces). A tile that is off is not on the page, its menu entry cannot be chosen, and a
  group with no tile left has no heading. It takes effect when the home screen is next
  built (sign-on, F5, Switch account).
* **The Terminal tile off is a wall for an account that starts in the home screen**: the
  screen never leaves the person at the command prompt, whatever ends it, and signs them
  out instead (a window too small to take the screen ends the session after the message).
  An account that starts at the prompt (`start-terminal`) keeps it. **It is a wall only for
  the prompt the screen gives**: the programs behind the other tiles are the account's own,
  so an account that is to be kept to the screen should have the editor, IDE and record
  editor tiles off as well, and a command that gives a shell needs `sh-on`, which is off as
  delivered.
* **`pins-on` is off as delivered.** An account that has it gets a group *My programs* on
  its home screen and the verb `my.menu`, with which the person adds **their own**
  programs (a label and a command they could type at their prompt): they manage only
  their own list, never the standard tiles, and a program of theirs adds no access. It is
  **field 18** of the register record, and the administrator always may. `pins-off` hides
  the group and `my.menu` refuses; the list stays in the person's file.
* `set.tile` says `Tile ide is now off for fred` (and `... was already off ...; nothing
  changed`) and is audited as `set.tile off tile=ide account=fred`; `modify.account` says
  `Account fred may add its own programs to the home screen: yes`.

### Signing in over ssh with a key: `ssh-key-on` and `ssh-key-off`

```
modify.account fred ssh-key-on
modify.account fred ssh-key-off
create.account user fred ssh ssh-key-on
```

**A Linux user that `create.account` makes cannot sign in over ssh with a key, as delivered.**
It signs in with its password, and only if the account's ssh route is on. `ssh-key-on` lets
that one account sign in with a key as well as with its password; `ssh-key-off` takes it
back; `create.account user` *name* `ssh-key-on` makes the account with it on. `ssh-key-on`
does not give the ssh route: the account still needs `ssh` or `both`. The gate matrix
(`tool.gates`) has a column for it, turning it ON there asks you to type the account's
name, and each account's own gate page shows its state, as `own` for a user SD did not make. After the word SD says
`Account fred may sign in over ssh with a key: yes` (or `no`). Only SDSYS may use the
words. The word is audited as `modify.account ssh-key-on account=fred`, and the audit
line of a `create.account` that used it ends `gates=` with `ssh-key-on` among the words.

**What opening it means for security.** A key is a second way in that the account's password
does not control. Whoever holds the private key signs in without the password, SD cannot see
who holds a copy, and changing or removing the password does not close it: the key stays valid until it
is taken out of the person's `authorized_keys` file. Turn it on only for an account whose
keys you trust, and leave it off for everything else; leaving it off is the tighter choice.

**How it is done.** The installer adds a setting to the ssh server's SD block that offers no
key sign-in to the members of the Linux group `sdsshnokey`, and `create.account` puts each
Linux user it makes in that group. `ssh-key-on` takes the user out of the group and
`ssh-key-off` puts it back. The account's password sign-in is not touched either way.

**Who it never affects.** Only a Linux user that SD itself made. The user who ran the
installer, a Linux user attached to an account, root, the `sdsys` user and every user outside
SD keep exactly the ssh settings they had, and `modify.account` refuses `ssh-key-on` and
`ssh-key-off` for them, saying that their keys are their own (a group account or an
`other` account has no Linux user and refuses them too). **The gate pages show a dash** for them.

**What it does not do:**

* **An upgrade changes no existing account.** Every account that existed before keeps the
  key sign-in it had; only accounts made after the upgrade start with keys off. To shut keys
  for an older account, `ssh-key-off` puts it in the group.
* **It does not help on a machine whose own ssh server allows no password sign-in.** There an
  account SD makes cannot use ssh at all until `ssh-key-on`.
* **It does not override a rule you wrote.** A `Match` block or setting of your own in the ssh
  server's configuration that is read before SD's block and sets `PubkeyAuthentication yes` for
  the user wins: the first value the server finds is the one it uses.
* **A backup that holds no such setting restores with it off**: `restore.account` puts the
  user in the group; `ssh-key-on` afterwards if it should have it.
* **The group must exist.** It fails open: if `sdsshnokey` is missing or cannot be read, the
  ssh server offers keys according to the machine's own settings, and `create.account`
  refuses to make a user until the group is there (nothing is created; an account made with
  `ssh-key-on`, or an attached user, is not put in the group and is not asked about it). SD will not delete the
  group; an installation without it needs the installer run again.

### `suspended`/`unsuspended` is a state, not a tier

**Nothing about the account moves except the one field.** No group
membership changes, no VOC changes — every account's VOC is the whole of
`newvoc` regardless of the field. Three doors refuse a suspended account:
signing in, `logto`, and the API.

**`logto` refuses it to the administrator too.** `logto` into a suspended account is
refused for every session, SDSYS's included: `Account fred is suspended`, the session stays
where it was, and the audit trail says `logto refused account=fred reason=suspended`. The
administrator's maintenance of a suspended account does not need `logto`: `run.in fred ...`
(`basic`, `catalog`, `decatalog`, `delete.catalog`, `debug`, `compile.dict`) still works in
one, and `modify.account fred unsuspended` lifts the suspension.

### `add`/`delete` is the grant

```
:modify.account fred add pete
:modify.account fred delete pete
```

**`add` and `delete` are the grant.** There is no separate `grant`, `revoke`
or `list.grants` verb: `modify.account` replaces them. **The grant is Linux
group membership, and nothing is written to the account record.** Every SD
account has a Linux group — `sdu_`*name* for a user account, `sdg_`*name* for a
group account — and entry to the account **is** membership of that group (the
test `logto` makes). `add` puts a Linux user into that group and `delete` takes
one out, through the privileged helper (`sd-elevate addgroup` and `delgroup`).
`usermod -aG` reaches the identical group directly, outside SD, at any time, by
an administrator with a shell, so `modify.account`'s value is the audit line, not
a gate nothing else could reach.

SD says *added to group*, *removed from group*, *is already a member of group*
or *is not a member of* (nothing changed), *is not a member of sdusers, not
allowed* (the person is not a Linux user SD knows; `add` only), or *Unable to add
user ... status: n* when the system refused the change.

**To see who is in an account,** read the Linux group: `tool.accounts` shows a
group account's members, and any account's group can be listed with
`getent group sdu_`*name* (`sdg_`*name* for a group account). The account's own
user is a member like any other.

**A successful `add` or `delete` writes an audit record** to SD's audit trail
(`modify.account add account=`*name*` to=`*user* and `modify.account delete
account=`*name*` from=`*user*), stamped with the user and process that did it. The
identity is stamped by SD and is not passed in, so a caller cannot get it wrong
or forge it.

**`delete` is deliberately unguarded**: taking access away is always allowed. To
take it from somebody who is signed in now, `delete` and then end their session.

## Passwords: `modify.password`

```
modify.password {account}
```

With no account name it changes **your own**, and asks for the current
password first. With one, from SDSYS, it changes that account's — any
account, including SDSYS's own — and does not ask for the old password: an
administrator resetting a forgotten password does not know it.

**The password is never an argument, and a trailing token is refused rather
than ignored:**

```
:modify.password fred hunter2
A password is never given on the command line; modify.password prompts for it
```

**That refusal is the point of the verb's design.** A verb that threw the extra
word away without a word would look as if it had worked, while the password had
already reached SD's command stack, and a shell's history and process list if
the verb was reached from one. Refusing does not put it back, but it says so.

The prompts are hidden, and the account must already exist in the register.
**The rule is checked before the repeat is asked for**, and there are up to
three tries:

The rule is said first (*A password needs at least 8 characters, with a lower-case
letter, an upper-case letter, a digit and a symbol.*). A password that does not meet the rule is refused at once and is not asked for
again; one that does is asked for a second time, and a difference between the
two says *Passwords do not match.* Each failure says which attempt it was; the
third ends the command with *Password not changed.* and nothing is changed. An
empty line at *New password* leaves the password as it was. `create.account user`
asks the same way, with the same three tries, saying the rule first and asking
*Retype new password*. **`modify.password` cannot be scripted**, by design.

**An ordinary account's own change goes through a privileged helper it cannot
bypass** (`sd-elevate cred-own`), because the credential file (`$cred`) belongs
to `sdsys` alone; an administrator — a real `sdsys` login — writes it directly.
At the terminal both look the same.

**SDSYS's own *Linux* login password is a separate thing** — set once,
during installation (`sudo passwd sdsys`), and changed afterward the
ordinary Linux way, not with this verb.

## Continued in

[Account Maintenance](01a-account-maintenance.html) — clean.account,
update.accounts, [locked], config, set.date and delete.account.

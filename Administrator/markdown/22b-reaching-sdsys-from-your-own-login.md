Title: Reaching SDSYS from Your Own Login
Subtitle: How the administrator can let chosen Linux users become SDSYS from this computer, by ssh or through the API, without logging in as sdsys; how to list them and take them off; the risk; and what it refuses.

**The administrator can let chosen Linux users reach SDSYS from this computer without logging out
and in again as `sdsys`.** There are two lists, one for an ssh login and one for a program that signs
in through the API. **Both are empty as delivered**, and with both empty SDSYS is reached exactly as
it was before: at the machine as `sdsys`, or through the doors `remote.sdsys` opens. The installer
does not ask about it. An upgrade that keeps the configuration keeps the lists as they were; a full
uninstall removes them.

* A user on the **ssh list** types `ssh -t fred@localhost sd-sdsys` on this computer, is asked for
  the SD password of `sdsys` once, and is then the administrator in an `sdsys` session.
* A user on the **api list** may have a program of theirs on this computer sign in as `sdsys` over
  SD's Unix socket, with the SD password of `sdsys`.

Either way the SD password of `sdsys` is still needed every time. It is SD's own password for
`sdsys`, the one `modify.password` sets and an API sign-in checks, not the Linux password.

> **Listing a name is a decision about that user, not about one login.** A listed user, from any
> session of theirs on this computer, **a session they reached over the network included**, can
> become the administrator if they also know the SD password of `sdsys`. The administrator can
> change every account on the system. A password typed once into the wrong place, or kept in a file
> that user can read, is then the whole of the protection. List only your own Linux login, the one
> you use as the administrator, and not ordinary users. Keep the lists short, use a long SD password
> for `sdsys` that is used nowhere else, and take a name off (`local.sdsys` *list* `remove`) when it
> is no longer needed.

## The two lists and who may be listed

| List | What a listed user may do |
|---|---|
| `ssh` | become `sdsys` from an ssh login on this computer, with `sd-sdsys` |
| `api` | have a program on this computer sign in as `sdsys` over the API's Unix socket |

Each list holds at most 32 names. A list is a plain text file of root's, one Linux user name to a
line, in `/etc/sdcore`; the administrator changes it only through `local.sdsys` (or the two fields
on the sdsys view of `tool.remote`, with keys to add a name, remove a name and clear a list), never
by editing the file. A list that does not exist is an empty list.

**A name can be listed only if** it is the name of an existing Linux user, of the form SD takes (a
lower-case letter or `_`, then up to 31 lower-case letters, digits, `_` or `-`), with a user id of
1000 or more, and a member of the group `sdusers`. `root` and `sdsys` are never listed, and neither is
a system account. Anything else is refused by name and nothing is changed.

**A list that is not safe is treated as empty.** SD uses a list only when the file is a plain file
(not a link, with no other name), owned by root, not writable by anyone else, under 8 KB, in a
directory that root owns and that is closed to others, with only valid names and no more than 32 of
them. Anything else, and the list refuses everybody; `local.sdsys` says so (see "The verb"), and
`clear` removes the file so the list can be made again.

## The verb: `local.sdsys`

```
local.sdsys
local.sdsys {ssh | api}
local.sdsys {ssh | api} add user {no.query}
local.sdsys {ssh | api} remove user
local.sdsys {ssh | api} clear
```

Only the administrator can use it; anyone else is told "Command requires administrator
privileges". The words, and the user name, are read as lower case whatever was typed.

| | |
|---|---|
| *(no keyword)* | reports both lists and changes nothing |
| `ssh`, `api` | reports that list and changes nothing |
| `add` *user* | puts the name on the list, after a plain warning and a question (below) |
| `remove` *user* | takes the name off; this works for a name whose Linux user has gone |
| `clear` | empties the list (the file is removed); the one way to leave an unsafe list |

`add` says once what listing the name means and asks, unless `no.query` is given. Anything but `y` is
no, and so is an input that ends:

```
:local.sdsys ssh add fred
Listing fred lets that user, from any session of theirs on this computer - one
they reached over the network included - become the administrator with the
SD password of sdsys (ssh -t fred@localhost sd-sdsys).
List fred for sdsys over ssh? (y/<n>) y
sd-elevate: sdsys local ssh: added fred; listed now: fred
```

For the `api` list the warning says that the programs of that user sign in as `sdsys` over the Unix
socket of the API instead. An answer other than `y` prints "fred was not listed; nothing was
changed." and writes nothing.

The report is one line a list:

```
:local.sdsys
sdsys local ssh: listed fred
sdsys local api: none listed
```

A list that is not safe is reported as `sdsys local ssh: unsafe, treated as none listed`, with the
file's name. Listing a name that is listed already, or taking off one that is not, says so and
changes nothing; a 33rd name is refused ("the ssh list holds 32 names already, the most it takes").
A refusal by the system is shown as it was said, and `local.sdsys` adds that the command did not
succeed.

## Reaching SDSYS over ssh

A listed user, on this computer, types:

```
$ ssh -t fred@localhost sd-sdsys
SD password of sdsys:
```

The user's ordinary ssh login to this computer comes first, as for any ssh login; the command
`sd-sdsys` then asks the operating system, and SD again, whether this is a listed user's ssh login
from this computer. **What counts as "an ssh login from this computer" is this: the login came
through the ssh server, and the ssh server recorded its source as a loopback address** (`127.x.x.x`
or `::1`). A login that came in from another computer does not count, nor one that came in at this
computer's own network address; neither does the console, a desktop terminal, `su` or `sudo`.

* **The password** is asked for once, with nothing shown as it is typed. The answer is the SD
  password of `sdsys`.
* **A right password** makes the session the administrator, and the session says so:

  ```
  SD administration granted: this session is the sdsys OS user, reached from
  the ssh login of fred on this computer with the SD password of sdsys
  ```

  The session is `sd` running as the `sdsys` user.
* **A wrong password** ends the session with "The SD password of sdsys was not right, so this session
  is not the administrator and ends here." There is **one try**. After a wrong password SD waits for
  the number of seconds `PWDELAY` gives (3 as delivered, 0 for none) before the session ends.
* **No password to check** (`sdsys` has none set): the session ends with a message that says to
  set one with `modify.password` from a `sdsys` login. Nothing is granted.

A second try is a new ssh login, and the wait applies again.

**The `-t` is needed.** It gives the session a terminal, and this way in is for a person at a terminal:
without one (`ssh` with no `-t`, or with its input taken from a file or another program) no password is
asked and the session is refused as a session without a `sdsys` login, its audit line ending
`why=no-terminal`.

## Reaching SDSYS over the API

A program of a listed user on this computer connects to SD's Unix socket and signs in as `sdsys`, with
the SD password of `sdsys`, as any API program signs in as any account. **It has to do nothing
different: the sign-in is the ordinary one, as `sdsys`.** A session so admitted has every right the
administrator has.

* **Only the Unix socket.** A connection over TCP, the loopback address `127.0.0.1` included, is
  refused for `sdsys`, listed or not.
* **The program must run as the listed user, and the login behind it must be that user's.** A
  program that reached the user through `sudo -u fred` or `su fred` from somebody else's login is
  refused.
* **The password is checked as for every API sign-in**: a wrong one is refused in the same words
  and after the same wait.

## What is refused

Everything that is not a listed user's ssh login from this computer, or a listed user's API program,
meets the refusal it met before the list existed.

**Over ssh**, `sd-sdsys` is refused by the root helper before SD is started. Nothing is started and
the refusal is one line, with a reason word, also written to the system log (SD's audit trail does
not see it, because SD never ran):

```
sd-elevate: REFUSED - sdsys-session: not-listed - this login is not a listed user's ssh login from this computer (local.sdsys ssh): nothing was started
```

| Reason word | when |
|---|---|
| `list-empty` | nobody is on the ssh list (as delivered) |
| `list-unsafe` | the ssh list is not a plain file of root's (see above) |
| `not-listed` | this user is not on the list |
| `not-sd-user` | this user could not be listed now: not in `sdusers`, or a system account |
| `no-user` | the login's user no longer exists |
| `not-ssh` | the login did not come through the ssh server: the console, a desktop terminal |
| `not-local` | the ssh login came from another computer, or from this computer's own network address |
| `no-login`, `other-user`, `other-session`, `no-session`, `session-unsafe` | the login behind the session is not the listed user's own, or the system's record of it is missing or not safe: `su` or `sudo` from another login |

**If the helper let the session in but SD's own check disagrees**, or a session of the `sdsys`
Linux user is started in some other way (`sudo -u sdsys sd`, `su sdsys`) from a login that is not a
listed user's ssh login from this computer, the old refusal stands: "This
session runs as sdsys but the machine was not logged in as sdsys, so it is not the administrator ...",
and the session ends. While the ssh list has names on it, the audit line for that refusal carries the
reason word as well.

**Over the API**, a refusal is the refusal `sdsys` met before: "SDSYS may use the API only from a
process running as the sdsys user on this machine." and the audit line `api refused` with the reason;
while the api list has names on it, the reason carries a `why=` word (`not-listed`, `list-unsafe`,
`not-sd-user`), and for a listed user whose login was somebody else's it says which login it was.

**A list file that is not safe** refuses everybody on that list, in the same words as an empty list
and with `list-unsafe` as the reason.

## What is written down

Every line is in the audit trail ([The Audit Trail](21-the-audit-trail.html)):

* Each change of a list, by the administrator:
  `local.sdsys ssh add user=fred status=ok`, `local.sdsys api remove user=fred status=ok`,
  `local.sdsys ssh clear status=ok`. A change that was refused ends `status=refused`. An `add` that
  was answered no writes nothing.
* A grant over ssh: `elevation granted reason=sdsys local ssh user=fred`.
* A refusal over ssh after the password was asked:
  `elevation refused reason=sdsys local ssh wrong password user=fred`, or
  `elevation refused reason=sdsys local ssh no credential user=fred`.
* The old refusal, while the ssh list has names:
  `elevation refused reason=sdsys session without a sdsys login why=not-listed`. With an empty list
  the line has no `why=`, as before.
* A grant through the API:
  `elevation granted reason=sdsys api from=this machine user=fred`.
* A refusal through the API: `api refused user=sdsys reason=...`, naming the user the program ran as.

The helper's own lines, for a change of a list and for a refused `sd-sdsys`, are in the system log.

## Taking a name off, and closing it again

```
local.sdsys ssh remove fred
local.sdsys api clear
```

`remove` takes a name off one list. `clear` empties a list, and taking off the last name does the
same: the file is removed, which is what "off" is. **With both lists empty nobody has this way
in**, and nothing else was changed to give it. The next try by that user is refused.

## What it does not do

* **It is not for another computer.** Over the network SDSYS is reached only through the doors
  `remote.sdsys` opens ([Remote Administration over ssh](22-remote-administration-over-ssh.html) and
  [Remote Administration through the API](22a-remote-administration-through-the-api.html)), each shut
  as delivered; neither is changed by this page's lists, and a login from another computer is not
  admitted by them.
* **It does not replace the SD password.** The password of `sdsys` is asked every time, once, and a
  listed user who does not know it is refused.
* **It does not let a user in who is not listed**, and does not list anybody for you: both lists are
  empty as delivered.
* **It does not protect against a listed user.** That user, and anyone who has that user's login on
  this computer, can ask for the administrator; only the password stands in the way.
* **It is not in SD Core Solo**, which has no `sdsys`.
* **A background process cannot be started from such a session.** A phantom begins a session of its
  own, which has no terminal to be asked the password at, and is refused as a session without a
  `sdsys` login (the audit line ends `why=no-terminal`). Start background work from a login as `sdsys`.

## See also

[Remote Administration over ssh](22-remote-administration-over-ssh.html) and [Remote
Administration through the API](22a-remote-administration-through-the-api.html) for the doors that
reach `sdsys` from other computers. [Accounts and Security](01-accounts-and-security.html) for what
being SDSYS means. [The Audit Trail](21-the-audit-trail.html) for the lines this writes.

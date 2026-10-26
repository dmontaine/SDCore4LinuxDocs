Title: Remote access and the machine
Subtitle: The two verbs that change the machine rather than SD, and the one thing they both require.

Most administrator verbs change something inside SD. These two change the
machine SD is running on: who may reach it over ssh, and whether SD opens
its API socket at all.

| | |
|---|---|
| `remote.ssh` | decides who may reach the machine's ssh server |
| `remote.api` | decides whether SD opens its API socket, and who may reach it |

**Neither of these installs or removes anything.** `sshd` is the
distribution's own service — installed, started and kept current the way
every other Linux service is, outside SD's remit entirely. These two verbs
only move the firewall rule and the API socket that sit in front of it;
they were built after the SD Core for Windows model of the same name,
under the owner's ruling that a behaviour prevented on one port must be
prevented on both, with the mechanism free to differ where the operating
system does.

> **Neither gives SDSYS remote access, and no setting does.** Opening ssh
> or the API to other computers opens it for ordinary accounts only — and
> of those, only the accounts SDSYS has given the route (`ssh`, `api` or
> `both`, in `create.account` and `modify.account`, or `files-on`, the
> narrower files-only API route), since a new account has none of them.
> **SDSYS has no remote route at all, under any setting these two verbs
> control** — refused at the door, not merely ungranted. Administration
> needs a real login as `sdsys` at the machine's own keyboard, or a
> desktop-sharing view of it. See [Accounts and
> Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it).

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case.

## Both need SDSYS, including to report

Each of them begins by testing the administrator flag — a real `sdsys`
login, not merely elevation — and stops if it is not set:

```
:remote.ssh
Command requires administrator privileges
```

That was run from an ordinary account. **The test runs before the keyword
is read, so the reporting forms are refused too** — there is nothing softer
about asking one of these verbs to just report the current setting, because
reading the answer means reading the firewall and the socket state, which
costs the same standing as changing them.

## Both report when given no keyword

```
remote.ssh
remote.api
```

With no keyword each reports the current state and changes nothing. This
is the supported way to answer "how is this machine set up?"

## remote.ssh

```
remote.ssh {on | off}
```

| | |
|---|---|
| `on` | other computers on the network may connect over ssh |
| `off` | only this computer may connect |

**It moves the firewall rule and never the ssh server itself.** `sshd` is
the distribution's own service, and an administrator's own shell may be
reaching this machine through it right now — there is nothing here
resembling SD Core for Windows's `ssh.server install`/`remove`, because
installing or removing packages is the distribution's job, not SD's. The
rule this verb moves is the one the installer itself wrote (`ufw allow
22/tcp`, or firewalld's port 22/tcp on Fedora). On Fedora the
distribution's own `ssh` service also lets ssh in; `remote.ssh off`
removes only SD's rule and says that the `ssh` service still allows it,
rather than remove a rule SD did not make.

**Where the firewall gates nothing, this refuses rather than lie about
it.** With no firewall (`ufw` or firewalld), an inactive one, or one already allowing incoming
connections by default, a rule change for port 22 changes nothing about
who can actually connect — and reporting "remote ssh access is now OFF"
in that state would be exactly the reassuring falsehood a verifier must
never print. The verb exits with a distinct status (3) having changed
nothing, prints what the firewall actually says, and names why.

**Administrator only, and every change is audited**, the same as
`remote.api`.

## remote.api

```
remote.api {on | local | off}
```

| | |
|---|---|
| `on` | SD listens on port 4247 on every address, and the firewall allows it: other computers may connect |
| `local` | SD listens on `127.0.0.1:4247` only: only this computer may |
| `off` | SD opens no API socket at all, TCP or local |

**There are two axes here and the verb sets both, the same shape as SD
Core for Windows's verb of the same name — the mechanism is entirely
different underneath.** Whether SD listens at all is `systemd`'s
`sdclient.socket` unit; who may reach it is the firewall — `ufw`, or
firewalld on Fedora. The verb drives both and
reads them back, so what it reports after a change is the machine's own
answer, not the verb's intention. The firewall rule is the installer's own
(`ufw allow 4247/tcp`, or firewalld's port 4247/tcp, kept in its saved
settings), so this verb and the install describe one state.

**The local Unix socket is for SD users only.** `/tmp/sdsys/sdclient.socket` is mode 0660, group `sdusers`: the operating system refuses a connection from
anyone else (root excepted) before SD sees it. Until 1.2-0 the unit named the group but not the mode, and systemd then makes a Unix socket 0666, so the
group restricted nothing and anybody on the machine could reach the first stage of an API connection, which runs as root. `remote.api on`, `local` and `off`
do not change the mode. A person who has just been added to `sdusers` must log out and in before the socket lets them through, as for the rest of the data
tree. The installer adds `SocketMode=0660` to an existing `sdclient.socket` that has no `SocketMode=` line, and never touches one that has; to widen it on purpose,
`systemctl edit sdclient.socket` and write `SocketMode=` in the drop-in. `ls -l /tmp/sdsys/sdclient.socket` shows the mode.

**No SD session is ever ended by this verb**, which is where it differs
most from the Windows original. SD Core for Windows's own listener opens
only when SD itself starts, so changing it there restarts the whole
program and ends every session, the caller's included — and asks first.
Here the listener belongs to the socket unit, not to any running `sd`
process: `on` and `local` restart the *socket*, and `off` stops it. A
connection already accepted is its own separate service instance, so
nothing already talking to the API is disturbed by a later change.

**Administrator only** — the same gate `modify.account` uses, because this
changes what the machine offers the network rather than anything about one
account — **and every change is audited**, a Linux addition matching how
the port's own account-tier changes used to be audited before tiers were
removed.

**What a connection costs while nobody has logged in.** Each API connection is one `sd -n -q` process, running as root until the client has logged in, and it is there before any login is checked. Since 20 Oct 2026 it ends when the connection does, and refuses a request that declares a length over 65,536 bytes (after the login the limit is the largest SD string; the client page, *How big a request may be*, has the rules), leaving a line in the system log. Before that date a client that closed at the wrong moment, or sent four bytes that read as a huge length, left its process running at 100% of a processor with nothing to end it but `kill`; a count of `sd -n -q` processes that does not fall back to the number of clients is the sign. **A client that connects, completes the handshake and then says nothing is still left waiting**: SD sets no time limit on a connection that has not logged in, and `remote.api local` or the firewall are what keep it to the people you intend.

## Everything that reaches SD from outside, on one screen: `tool.remote`

```
tool.remote
```

A full-screen page in SDSYS's VOC only (a window of 140 columns by 43 lines or more) of five views,
chosen with the keys `1` to `5`:

| View | What it shows and does |
|---|---|
| `1` doors | what `remote.api` and `remote.ssh` say with no keyword: **the machine's own answer**, read back from the socket unit and the firewall, not what the page meant. `A` changes the API (`on`, `local` or `off`), `S` changes ssh (`on` or `off`); turning either **on** lets other computers reach this one, so its box wants the word `OPEN` typed |
| `2` routes | every user account with the doors it has (`ssh`, `api`, `files`, `files-write`, `files-admin`) and the NET gate, and in words how it can be reached. It only shows: the switches are `tool.gates`'s |
| `3` servers | the SDNet servers of the `netservers` file (read with `!netdefs`): name, address, remote account and mode, the pin shortened, the local accounts that may use it. `X` deletes the one under the cursor (`delete.server`, which does not ask itself, so the box is the question). `N` asks every field, checks them the way `set.server` does and gives **the terminal to the verb**, whose `connect` step shows the key the server presents and its hash and asks whether to trust it |
| `4` connected | every session now by the door it came through: the user number, the kind (user, api, sdnet, phantom), the login user, the account and where it came from |
| `5` TLS | this machine's TLS identity as `settings.report` gives it: the certificate fields and the public-key hash another SD server pins. Never the private key |

The page runs three commands through the routine all the toolkit pages use, each only after a box that
shows the command and what it does was answered Run (**Cancel is what Enter chooses**): `remote.api`,
`remote.ssh` and `delete.server`, besides the two reports. `set.server` is run by the verb itself on the
terminal. The verbs ask for the administrator again and write their own audit lines; the page writes
nothing. A door that the firewall cannot gate is refused by `remote.ssh`, and the page shows the
verb's words. `F5` reads everything again, `F1` explains the page and `Ctrl-Q` leaves. Opening the page
writes the audit line `tool start app=tool.remote`.

## When a change fails

Both report a failure rather than falling silent, and name what did not
happen. `remote.ssh` exits 3, unchanged, when the firewall would not have
gated anything anyway (see above) — a refusal, not a silent success.

Title: SDNet
Subtitle: The NET switch and the server definitions: what is in place for files on another SD server, and what is not there yet.

SDNet is the name for opening a file that lives on **another SD server** and using
it with `READ`, `WRITE`, `SELECT` and `LIST` as if it were local. **This release
has the permission (the NET switch), the list of servers, a person's own login on a
server (`set.netlogin`, kept as values derived from the password and never as the
password), and a VOC pointer of type `N` that opens a file on a defined server: for
reading, selecting and querying, and, only for a server defined `write` whose
administrator has also put the remote user in the Linux group `sdfileswrite`, for
writing and locking.** On the server side there is a second, narrower API route,
`sdfiles`, which lets a login work with files and do nothing else. The pieces that are
not there are listed under "What does not exist yet". Behavior that depends on your own
network is listed in *Known Limits*.

SD has no `server;file` VOC entry over
port 4245 with each server's password in `sd.conf`, which any local user could
read. **This is not that.** Nothing of that kind exists: there is no `;` in a path, no
port 4245 and no password in any file.

## What SDNet is

- **Files on another SD server, read only unless two people say otherwise.** A server is
  `read` unless SDSYS defines it `write` on the client, and the administrator of the
  *target* must also allow writing for that remote user (`sdfileswrite`).
- **The same channel as the API.** The connection is the target server's own API port,
  TLS 1.3 with the SCRAM login bound to the TLS session, and no new listener. A full
  SD Core listens for the API on 4247; a Solo on 4249.
- **Delivered off, and loosened by SDSYS.** The switch is off for every account,
  the list of accounts allowed to use a server is empty, and a server is
  `read` unless SDSYS says otherwise. SDSYS turns each on, one account and one
  server at a time.

## What is in SDNet

| | |
|---|---|
| the **NET switch** | `modify.account` *name* `net-on` / `net-off`, and `net-on` in `create.account user`. See [Accounts and Security](01-accounts-and-security-3-edit-switches.html#the-net-switch-net-on-and-net-off) |
| the **server definitions** | one file, `netservers`, in the SDSYS directory |
| **`set.server`** | adds a definition, or replaces one |
| **`delete.server`** | removes one |
| **`list.servers`** | shows them |
| **`set.netlogin`** | a person makes their own login on a defined server: SD runs the SCRAM exchange once and keeps the derived values (see "Your login on a server") |
| **`delete.netlogin`** | removes it |
| **`sd-elevate netcred-dir`** | the privileged helper step that makes the directory the logins are kept in |
| the **files-only route** | the Linux group `sdfiles`, on the server being reached: `modify.account` *name* `files-on` / `files-off`, and `files-on` in `create.account user`. See "The files-only route on a server" below |

**The first three verbs are SDSYS's.** They are in SDSYS's VOC and in no other account's,
and each one also stops with "Command requires administrator privileges" for
anyone who is not the administrator. **`set.netlogin` and `delete.netlogin` are in
every account's VOC**, because they are for the person whose login it is; the
gates they ask are described below. Commands are shown here in lower case.

### What does not exist yet

- **A connection that is not one of three.** The only things in SD that open a socket
  to a server are `set.server` with the word `connect`, once, for the handshake
  alone, `set.netlogin`, once, for the login exchange, and opening a remote file
  through an `N` pointer (all below). No other verb, statement or program dials a
  server *defined* here. A definition is a record on disk and nothing reads it but
  these.
- **A check that a typed pin is right.** When you type the 64 digits, nothing
  connects and nothing checks them; use `connect` to have the server's own hash
  shown to you. `set.netlogin` and every remote open compare the key the server
  presents with the definition's pin before they send anything.
- **Using the login, apart from a remote file.** The only thing that reads a stored
  login to log in is opening a remote file through an `N` pointer (below).
  `set.netlogin` proves the login works once, at the moment it is made, and keeps
  the result.
- **A way to make the client use only the files-only route.** The server has the route
  (below), the client that opens remote files asks only for requests the route allows,
  and the person who runs the other server can give the remote user `files-on` instead
  of `api`. But `set.netlogin` does not require it, and **the only client use of a stored
  login is opening a remote file**. A
  remote user who is in `sdapi` still has the whole API, and so does a stored login
  made for that user: whoever holds the file can do on that server what that remote
  user can do over the API. Give the remote user `files-on` and not `api`, or choose
  the remote user with that in mind. **A files-only login is read only on the
  server unless the remote user is also in the Linux group `sdfileswrite`**
  (`modify.account` *name* `files-write-on`, below): without it the server refuses every
  write, delete, record lock, file lock and clear, and the locking forms of a
  read, whatever the client's definition says. The definition's `mode` on the
  *client* is still enforced there, but it is no longer the only thing between a
  stored login and a write: **a target's administrator decides whether a login may
  change anything on that target.**
- **Remote files.** A VOC pointer of type `N` opens a file on another server for
  reading, selecting and querying (see "Remote files, read only" below), and, only
  for a server defined with `write`, for writing and locking (see "Writing and
  locking"). The index queries (`INDICES`, `SELECTINDEX`, `SETLEFT`, `SETRIGHT`, `SELECTLEFT`,
  `SELECTRIGHT`) work on any remote file, read definition or write. Changes to an index and anything
  that makes or deletes a file need the administration group (see "Writing and locking").
- **`NETFILES`** in `sd.conf` is not what this uses. Opening a remote file through an
  `N` pointer does not read it. The one thing that does is the API server's old request
  29, "open an SDNet file": it needs bit 2 of `NETFILES`, the same account rules as `logto`
  and the account's NET switch, and a files-only login can never make it. It also refuses a
  VOC pointer that leads out of the account unless the account holds `os-on` (status 3035,
  audit line `api refused request=29 reason=os gate off ...`) (see
  [SD Admin Configuration](07-sd-admin-configuration.html)
  and the VOC pointers section of [Accounts and Security: File Writing, the AI and VOC Pointers](01-accounts-and-security-5-files-write-ai-pointers.html)).
  What you can set in `sd.conf` for SDNet is the two waits, `NETWAIT` and `NETREPLY`
  (below).

## The security model

**Nothing a user can type chooses a host.** The only machines SD will ever be
asked to call are the ones SDSYS has written down, and only SDSYS can write them:
the file is replaced only by these verbs, and the verbs are SDSYS's. A program
cannot define, change or point at a server. (`set.server ... connect` is the one
connection that takes a host as typed: it dials the host SDSYS typed, for a
handshake, and sends nothing. Every other connection goes to a defined server.)
Two things must then both be true before an account can use one: it has the NET
switch (off by default), and it is named in that server's *accounts* list (empty
by default). Neither is a
judgement that nobody should have the capability; each is a decision about who
decides, and it is yours.

**The file holds no secret, and must never hold one.** A definition is a name, an
address, a port, the name of an account, and the hash of a *public* key. The file
is readable by every user (mode 644) on purpose, and only the `sdsys` user writes
it. A person's login on a server is kept somewhere else, in a file only that
person can read (see "Your login on a server").

## The file: `netservers`

It is a plain text file in the SDSYS directory (`/usr/local/sdsys/netservers` on a
standard install), one definition to a line, at most **ten**:

```
name|host|port|account|pin|mode|accounts|created
```

It is always written **whole**: the new text goes to `netservers.new` beside it
and is renamed over the old file, so it is never half written. A session that
changes it holds a lock for the length of the change (a second administrator
session that tries meanwhile is told to try again). The mode of the new file is
644 whoever asked, and the file is owned by whoever ran the session, which is
`sdsys`.

| field | rule |
|---|---|
| **name** | a lower case letter, then up to 15 lower case letters or digits. Capitals typed are converted |
| **host** | 1 to 253 letters, digits, dots, hyphens or colons: a DNS name, an IPv4 address or an IPv6 literal. It does not start with a hyphen or a dot. Capitals are converted |
| **port** | a whole number from 1 to 65535: the port **of the server you are defining**, chosen when you define it (4247 for a full SD Core, 4249 for a Solo). SD does not insist on either number. `04249` is stored as 4249 |
| **account** | the account to enter on the remote server: 1 to 32 letters, digits, dots, underscores or hyphens. Kept as typed, because the other server's names are its own |
| **pin** | the SHA-256 hash of the server's public key: exactly 64 hexadecimal digits, stored in lower case. A new certificate with the same key keeps the same pin |
| **mode** | `read` or `write`. `read` unless `write` is given. What a program may do with the server's files, once it can open them |
| **accounts** | the **local** accounts that may use the server: registered account names separated by commas, no spaces, no empty name, at most 2000 characters, each listed once. **Empty means nobody**, and empty is what you get unless you list some |
| **created** | the date the definition was made, `yyyy-mm-dd`. Set by SD |

No field may hold a vertical bar, a control character or a character above the
ASCII range, so a line cannot be made into something else.

## Continued in

[SDNet: Servers](12a-sdnet-servers.html) — set.server, delete.server and
list.servers.

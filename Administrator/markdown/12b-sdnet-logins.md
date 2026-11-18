Title: SDNet: Your Login on a Server
Subtitle: What is kept of a login, where, and set.netlogin and delete.netlogin.

This page continues [SDNet: Servers](12a-sdnet-servers.html).

## Your login on a server: `set.netlogin` and `delete.netlogin`

A defined server is a name, an address and a key. To use it, a person also needs a
**login** on it: a user name and password that the other server knows. `set.netlogin`
is how a person gives SD that login, once, and `delete.netlogin` is how they take
it away. **They are the person's own verbs, in every account's VOC, and SDSYS does
not set a login for anyone else.**

```
set.netlogin name
delete.netlogin name
```

### What is kept: not the password

**SD never stores the password.** It is typed hidden, used once to work out some
values, and cleared from memory. What is kept is what the SCRAM-SHA-256 login
(RFC 5802 and 7677, the same login the API uses) derives from the password:

- the **salt** and **iteration count** the other server chose for that user,
- the **ClientKey** and the **ServerKey**, which are keyed hashes of a
  PBKDF2-HMAC-SHA-256 stretch of the password and the salt.

A later login needs those and not the password. That is the whole reason for
keeping them: the file can be used without anyone typing anything, and it is not
the password.

**What a person who reads the file can and cannot do.** Be exact about this,
because "not the password" can sound safer than it is.

- **They can log in as that remote user to that one server.** The ClientKey is
  the secret that proves the user, so having it is as good as having the password
  *for that server*. They cannot log in to a different server, because the salt
  and so the keys are different there, even if the password was the same.
- **They cannot read the password from it.** The keys are one-way. **They can
  guess it offline.** Anyone holding the salt, the count and a key can try
  passwords at their own speed and check each against the key, with no server
  involved. The iteration count (the server chose it; this release accepts nothing
  outside the API's own limits) slows that, but a weak password still falls to it,
  and a password that was reused elsewhere is then known elsewhere. This is why
  the file is kept private (below), and why the remote password should be a
  strong one that is not used for anything else.
- **The ServerKey does not let them pretend to be the server to you.** It would
  let a program produce a signature that looks right, but SD compares the key the
  server presents with the pin in the definition before it sends anything, and an
  impostor does not have the real server's private key.

### Where it is kept, and why there

```
/var/lib/sd-net/<linux user>/<server name>
```

- `/var/lib/sd-net` is owned by root, mode 755, and holds one directory for each
  person that has one.
- `/var/lib/sd-net/<linux user>` is owned by that person, mode **700**.
- The file is owned by that person, mode **600**, one line, written whole through a
  temporary file `<server name>.new` and renamed, so a failure leaves any older login
  as it was:

```
v1|remote user|salt (base64)|iterations|ClientKey (base64)|ServerKey (base64)|pin|created
```

`pin` is the pin of the definition *when the login was made* (64 hex digits) and
`created` is `yyyy-mm-dd`.

**Uninstalling.** `deletesdcore.sh` removes `/var/lib/sd-net`, and with it every
person's stored login, **if the accounts are deleted or the configuration is
deleted** (either answer to its two questions), and keeps it only when both are
kept; it says which it did. A stored login is as good as that server's password,
and a reinstall that kept nothing has no server definitions for it to belong to.
After a reinstall that deleted either, each person runs `set.netlogin` again.

**It is outside the account directory on purpose.** An account's programs reach
the operating system's files only through the account's own directory unless the
account holds the `sh` or `os.execute` switch. Anything kept inside an account
directory, or under the home directory, could be read by an account program with
`OPENSEQ`; a file in `/var/lib/sd-net/<user>` cannot be reached that way by an
account without those switches. That makes the file safe from the ordinary
account program. It does not make it safe from a person.

**The honest limit.** An account that holds the **`sh`** or the **`os.execute`**
switch can read anything its Linux user can read, and this file is something that
Linux user can read, **exactly as such an account can read `~/.ssh`**. The file's
privacy is the operating system's privacy of that one user, no more. If an account
runs untrusted code with one of those switches on, a login kept by the same Linux
user is exposed to it. Two accounts of the same Linux user share the one file for a
server, because the file belongs to the Linux user and not to the SD account.

**How a program reads it.** Only through an internal subroutine, `$netcred`, that
no ordinary program can call (its name starts with a dollar sign). Before every
use of the file or its directory, `$netcred` asks the C check `SD_FILE_PRIVATE`
(one of the SDEXT functions, key 111, again callable only from an internal
program): the path is a **regular file and not a link**, owned by the user who is
running, with **no group or world permission bits**, and its directory is owned by
that user, is not a link, and has no group or world bits (mode 700). That is the test
ssh makes of a private key. A file or directory that fails it is **never opened**:
the stored login is reported as not trusted and nothing in it is used. `$netcred`
also refuses a login made for a different pin than the definition has now, so a
login does not carry over to a server whose key has changed (or to a server
redefined under the same name).

### `set.netlogin`

```
:set.netlogin hq
Setting up your login on server hq (hq.example.com:4247).  Your password is used once here and is not stored
Remote user: reports
Remote password:
Your login on server hq as reports is stored.  The password is not stored
```

(`Remote password:` is typed hidden.) *Remote user* is the user name that the other
server has for you; it is not the *account* field of the definition (which is the
account entered on the other server later, once something uses the login).

**The checks, in order.** Every local check comes first and asks you for
nothing; the prompts come after them; the network comes after the prompts.

1. The command has exactly one word after it, and that word is a valid server name.
2. **The account has the NET switch**, or the session is the administrator.
3. **The server is defined**, and its pin is a well formed one.
4. **The account is in the server's *accounts* list**, unless the session is the
   administrator's.
5. The session is a Linux user that can keep a login: not `sdsys` and not `root`.
6. **The directory is ready:** SD runs `sudo -n /usr/local/sbin/sd-elevate netcred-dir`
   (below) and then asks `SD_FILE_PRIVATE` whether the directory it was given is
   private and the person's own. `-n` is there so a person without the sudo
   permission is refused and not asked for a Linux password in the middle of an SD
   session.
7. The two prompts. A user name that is empty or not valid (letters, digits,
   dots, underscores and hyphens, up to 32) ends the command before the password is
   asked. An empty password, or input that ends, ends it too.
8. **One TLS connection** to the host and port of the definition, waiting at most
   `NETWAIT` seconds (5 unless changed).
9. **The key the server presents is compared with the pin, before anything is
   sent.** A different key ends the command with nothing sent and the password
   still unspent.
10. The server's one-byte acknowledgement, then the SCRAM exchange exactly as the
    API client makes it: two packets from SD, two replies from the server, bound to
    the TLS session. SD checks that the server's nonce extends its own, that the
    iteration count is a whole number within the API's limits, that the salt is
    well formed, and **that the server's signature is right**, so the server has
    to know the password too. Each read or write waits at most 15 seconds.
11. Only then is the login written, through `$netcred`.

**Nothing else is sent.** No account is entered on the other server and no quit
is sent; the connection is closed when the exchange ends. On any failure nothing
is stored, and **an existing login is left exactly as it was**. When the exchange
succeeds, an existing login for the same server is **replaced without a question**,
because the person has just proved the new one.

**When it does not work:**

| you see | meaning |
|---|---|
| `Usage: set.netlogin server` | the wrong number of words |
| `Server name x is not valid` | not a lower case letter followed by up to 15 lower case letters or digits |
| `This account does not have the NET gate, so it cannot log in to a server.  Ask the administrator (modify.account x net-on)` | no NET switch |
| `No server is defined with the name x` | there is no such definition |
| `Account x is not listed for server y.  Ask the administrator to list it (set.server ... accounts)` | the account is not in the definition's list |
| `The administrator has no Linux login of its own to keep a server login in.  Use an ordinary user's account` | the session is `sdsys` (or `root`) |
| `The directory for your server logins is not ready or is not private (...).  Nothing was done` | `netcred-dir` failed (for example the sudo permission is missing, or this installation has not been brought up to date) or the directory failed the private check; the text in the brackets is the helper's last line, cleaned |
| `The remote user name is not valid (...)` / `A password is required.  Nothing was changed` | the prompts |
| `Cannot connect to host:port (status n, os error m).  Nothing was sent or stored` | nothing is listening, the address is wrong, or `NETWAIT` seconds passed |
| `The TLS handshake with host:port did not complete.  Nothing was sent or stored` | something answered but not with TLS |
| `The server at host:port gave no public key hash.  Nothing was sent or stored` | a session was made but no hash could be read |
| `The key presented by host:port is not the key in the definition of server x.  Nothing was sent to it and nothing was stored.  It is not the server that was defined, or its key was renewed` | the pin check. If the other server really did get a new key, define the server again (with `connect`) and then run `set.netlogin` again |
| `The connection to host:port failed or timed out at ...` | a read or write of the exchange failed or waited 15 seconds |
| `The server's first message was not valid (...)` | the server's reply was not what the exchange allows |
| `The server refused the login (...)` | wrong user name or password, or the server will not allow it; the server's text, if any, is cleaned to printable characters and cut |
| `The server's signature did not verify, so it does not know the password or is not the real server` | the final check |
| `The keys could not be derived (...)` | SD could not work out the values; the final message was not sent |
| `The login for server x could not be stored or removed (...)` | the last step failed; any older login is as it was |

### `delete.netlogin`

```
:delete.netlogin hq
Your login on server hq was deleted
```

It removes **your** login on that server and nothing else. It asks for no switch,
since removing a login adds nothing to what an account may do, and it connects to
nothing; the definition is not touched. If there is no login:
`There is no login stored for server hq.  set.netlogin hq makes one`. **A file
that is not the plain private file `set.netlogin` makes is refused and left where
it is** (the message says the stored login is not trusted); a person with such a
file in the way removes it from the shell.

`delete.server` leaves people's login files behind. They are inert: a login made
for a pin the definition no longer has is refused, so it cannot be used. But a
server defined again under the same name *with the same pin* finds them valid, so
people who do not want that run `delete.netlogin` first.

### Where it works

`set.netlogin` and `delete.netlogin` need a **local session of an ordinary Linux
user**: the file is that user's and the ownership check is made against the user
the session runs as. In an API session the process runs as `sdsys`, and the
check fails closed (the stored login is "not trusted"). The administrator,
who is `sdsys`, has no login of its own to keep.

### The helper: `sd-elevate netcred-dir`

The directory `/var/lib/sd-net/<user>` cannot be made by the user (its parent is
root's), so `set.netlogin` asks a helper:

```
sudo -n /usr/local/sbin/sd-elevate netcred-dir
```

It takes **no argument**; whose directory it makes is read from sudo's own record
of who asked (`SUDO_USER` and `SUDO_UID`, which must agree with the user database),
never from anything typed. It refuses root, `sdsys`, a user below the
minimum ordinary uid and an unknown user. It makes `/var/lib/sd-net` (root,
mode 755) if there is none, then the caller's own directory (the caller, their
primary group, mode 700). **It is safe to run again**: if the directory is there it
changes nothing but a wrong mode, which it sets back to 700. It refuses, and says
so, if either path is a link or a file, if the user's directory belongs to
someone else, or if `/var/lib/sd-net` is writable by its group or by everyone. It
prints `netcred-dir: <path>` on a line of its own **only after reading the
directory back and finding it right**. `--dry-run` shows the commands and makes
nothing, and does not print that line. Root never writes a file inside the user's
directory.

`/etc/sudoers.d/sdcore` gives members of the `sdusers` group this one command,
`sd-elevate netcred-dir` with no argument, **beside** the three `cred-own` commands. **The sudoers file is installed by
the installer.** Without that permission `set.netlogin` stops at
the directory step (check 6) with a message that includes sudo's own refusal.

## Continued in

[SDNet: The Files-only Route](12c-sdnet-files-only-route.html) — the
files-only route and the sdfileswrite group.

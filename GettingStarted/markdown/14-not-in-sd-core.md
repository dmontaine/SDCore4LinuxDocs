Title: Not in SD Core
Subtitle: What has been removed, why, and what to use instead.

This page exists so you do not spend time hunting for something that is not
there. **It names what is gone and what to use in its place; it does not
document the removed features themselves.**

Everything here was in OpenQM, in ScarletDME, or in upstream `sdb64`, and is
not in SD Core for Linux. **Most of these removals were made independently
on SD Core for Windows too, for the same reasons** — see that port's own
version of this page — which is worth knowing if you come across a decision
recorded on one side and wonder whether it binds the other.

> **If you had a use for any of these, say so.** Several were removed on the
> reasoning that nothing needed them. That reasoning is worth testing against
> real use.

## Editors

| Gone | Use instead |
|---|---|
| `update.record` — the full-screen record editor | **`sed`** or **`micro`** |
| `modify` — the full-screen record editor from OpenQM | **`sed`** or **`micro`** |

**`sed` was removed and has come back**, with drop-down menus that show the key
for each action, so it is no longer in this table.

**SD Core's own full-screen editing is `sed` and `micro`**, which open the
record in each program by name — see
[Programmer commands](07-programmer-commands.html#editors), which also says
what they are good for and what they cannot do. **Unlike SD Core for
Windows, `edit` is not one of them here — it aliases `ed`, the line editor,
because there is no Linux program to alias it to the way Microsoft Edit
serves that role there.** The two removed programs above are gone as
*programs*; the capability is not.

`modify` is not in SD Core at all, for any account.

**`modify.account` and `modify.password` are not affected.** They are
different verbs with different programs behind them. `modify.account` is
SDSYS's alone; `modify.password` is every account's, for its own password —
only naming a different account needs SDSYS.

> **`ed`** was never affected by any full-screen keyboard fault — it reads
> whole lines and goes through the command-line editor.

## The PROC language

`PROC` is gone. **A VOC item of type `PQ` now reports that PROC is not
supported instead of running.** Your `PQ` records are left alone — it is the
interpreter that has gone, not the records.

**Do not confuse PROC with the query processor.** `list`, `count`, `select`
and `sort` are unaffected. They are a different thing despite the similar name.

## SDNet — remote file access

SD could open a file held on another SD server by putting `server;file` in a
VOC entry, with each server's password in `sd.conf`. **That form is gone, and
it stays gone. A VOC entry containing a semicolon is simply a file name that
does not resolve.**

**A different SDNet has replaced it.** A VOC entry of type `N` names a server
that SDSYS has defined with `set.server` and a file on it; the verbs
`set.server`, `delete.server` and `list.servers` are SDSYS's, and
`set.netlogin` and `delete.netlogin` let a person store their own login (never
the password) for a server. Nothing is open by default: an account needs the
`net-on` switch, has to be named in the server's list, and a server is read
only unless SDSYS defines it as `write` **and** the administrator of the other
server has also let that remote login change files there (`files-write-on` on
that server); configuring, indexing, creating and deleting a remote file, and
the file's counter, need a third permission there (`files-admin-on`). It uses the other server's API port
over TLS and does not put a password in any file. The *Administrator* set's
*SDNet* page describes it.

**The API is not affected.** `!sdclient` and the remote API are a separate
mechanism and are unchanged. See [API access](09-api-access.html).

**`NETFILES` is still accepted in `sd.conf`**, so an existing configuration
file will not stop SD starting, and the new SDNet does not use it. The only
thing that reads it is the API server's old request to open an SDNet file,
which is refused unless bit 2 of `NETFILES` is set (and, since October 2026,
unless the caller could `logto` that account and the account has `net-on`, and, since
20 October 2026, a file pointer that leads out of the account is followed only if the
account has `os-on`); the
value is 0 unless `sd.conf` sets it. The two settings the new SDNet does read
are `NETWAIT` and `NETREPLY`, the seconds to wait for a connection and for each
reply.
The *Administrator* set's *Configuration* page has the detail.

## Virtual file systems

**SD has never been able to open a virtual file system.** Nothing in the
file-opening code ever recognised a `VFS:` pathname. What the language carried
was the *outline* of one, and none of it could be reached: a VOC F-pointer
written as `VFS:something` was reported as a virtual file system, passed the
name resolver, and then failed to open with an unrelated error.

All of it has been removed, so the language no longer offers a feature it
cannot perform.

**These names are no longer defined, and a program mentioning one will no
longer compile:**

```
FL$TYPE.VFS      SYSCOM KEYS.H
ER$VFS.NAME      SYSCOM ERR.H
ER$VFS.CLASS     SYSCOM ERR.H
ER$VFS.NGLBL     SYSCOM ERR.H
```

`ftype` no longer returns `VFS` for a `VFS:` pathname.

**IF ONE OF YOUR PROGRAMS REFERS TO ANY OF THESE, it was testing for a state
SD could not reach, and the test can be deleted.**

## Tape and restore

The `TAPE`/`RESTORE` subsystem is gone, along with the assumption of a
tape-backed sequential medium it was built around. Back up and restore SD
data the ordinary Linux way — at the file level, with the daemon stopped,
or through your own export/import BASIC.

## Language and locale

**SD Core is English only.** `set.language` and `load.language` do not exist.
`nls` is still there: it shows and sets the currency symbol and the thousands
and decimal separators, which is all it ever did.

## Embedded Python — kept, and this port's own decision to keep it

**Unlike SD Core for Windows, which dropped it and only later brought back a
narrower, process-isolated form, this port never removed embedded Python.**
It links directly against the interpreter, and there is no separate helper
process to talk to over a pipe.

**BASIC-callable programs** (`call !py_createdict`, and so on) are the
interface — there is no TCL verb, so this is a programming capability, not
a command you type at the prompt. **Starting it and running code in it
need the account's `os-on` switch**, the same one as `OS.EXECUTE`, because
the interpreter runs arbitrary code in the session's own process — see
[Security and the operating
system](12a-security-and-the-operating-system.html).

## Field-level encryption

**`encrypt.field` is gone, and with it field-level encryption from TCL.**

**Encryption in SD BASIC is unaffected and is the supported route.**
`sdencrypt()` and `sddecrypt()` ship — see *SD Basic - System and Environment*.
What has gone is the TCL verb that encrypted a field in place, and
**nothing replaces that**.

## Account and configuration items

| Gone | Notes |
|---|---|
| `CREATUSR` | `config` no longer lists it; `config('CREATUSR')` returns nothing. The parameter itself was removed on 27 October 2026, and a `CREATUSR` line in `sd.conf` now stops SD from starting (the installer takes it out of a kept file) — `create.account` always creates the Linux user, there is nothing to opt in to |
| `grant`/`revoke`/`list.grants` | folded into `modify.account add`/`delete` — see [Accounts](05-account-types.html) |
| the `os.users` permit list | the file is gone; `sh-on`/`sh-off`/`os-on`/`os-off` are kept, and they set two fields of the account's own register record instead — see [Security and the operating system](12a-security-and-the-operating-system.html) |

**`umask` is kept, deliberately, and is not on this list** — a real
difference from SD Core for Windows, where it was removed as inert. It is
a live mechanism here; see [Accounts](05-account-types.html).

## Eighteen SDSYS test and legacy programs

`bigstr_test`, `msgtest`, `pcl`, `pcl.grid`, `pcode_list`, `sdtest_v8`,
`sd_encrypt`/`_b64`/`_ext`, `sd_ext`, `test.then.else`, `testsz`, `u0032`,
`u50bb`, `vfs.cls`, `pref_t`, `sdTests` and `tilde_test` are no longer
installed into the SDSYS `bp` file — developer-era test and demonstration
programs with no product function, not something an application ever
called. **`py_json`, `py_term`, `py_test` and `py_test2` were kept
deliberately**, as the documented examples for embedded Python, above.

**`pcl` is unaffected as a printer feature** — the `pcl` keyword and the
catalogued `pcl` routine in `gpl.bp` are both still there. What has gone is
a second, older copy of the source sitting in `bp`.

**SD ships nothing into the SDSYS `bp` file at all now.** It is created
empty and is yours — and because of that, **`bp` and its compiled objects
are preserved when you upgrade**, alongside your accounts and the rest of
your own data.

## Things that were never features, and are not coming

These are not removals. They are stated here because a reader coming from
another MultiValue system will otherwise assume they exist.

**SD cannot be installed unattended.** `installsdcore.sh` asks for
confirmation and, at the end, three passwords — there is no flag to skip
either. Unattended deployment from this installer is not supported; a
site that needs one builds its own automation around the same underlying
verbs and Linux tools the installer itself uses.

**scp and sftp do not work inbound over ssh, for anybody**, once SD's ssh
boundary is in place — which it is, regardless of whether remote ssh
access is turned on. This is the accepted cost of putting every ssh
session straight into SD. See
[ssh access](08-ssh-access.html#the-cost-scp-and-sftp-stop-working-inbound-over-ssh).

**The cleartext API login is gone**, and a client that still sends a password
in clear is refused outright. See [API access](09-api-access.html).

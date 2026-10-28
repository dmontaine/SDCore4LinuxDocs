Title: SD Basic - Status, Encryption and the Machine
Subtitle: Status codes, checksums, encryption, the file mask, the @variables, os.execute and the error log.

This page continues [SD Basic - System and
Environment](16-sd-basic-system-and-environment.html).

## STATUS() and OS.ERROR()

`status()` carries the result of the last operation that sets one. It is
overwritten constantly, so **read it into a variable on the line after the call
you care about**, not three lines later. Every `status()` value quoted in this
document set was captured that way.

`os.error()` carries the operating system's own error number from the last call
that made one, and is `0` when nothing has failed.

Codes worth knowing:

| | |
|---|---|
| `1004` | item not found |
| `1006` | bad action key |
| `1008` | action failed — `os.error()` has the detail |
| `1011` | timeout |
| `3001` | subfile not found |
| `3006` | record not found |
| `3007` | **no VOC record** — from a failed `open` of a name that is not in the VOC |
| `3021` | cannot gain exclusive access to a file |
| `3023` | write or delete with no lock held |
| `7005` / `7012` / `7013` | socket: cannot connect / cannot bind / closed |

## CHECKSUM()

```
checksum(string)
```

| | |
|---|---|
| `checksum('ABC')` | `451` |
| `checksum('abc')` | `291` |
| `checksum('ACB')` | `448` |
| `checksum('')` | `0` |
| `checksum('A' : @fm : 'B')` | **`-325`** |

It is case sensitive and order sensitive, and **it can be negative**, so a
program that stores it needs a signed field. It is a change detector, not a
digest: it is short, and it is not a security primitive.

## SDENCRYPT() and SDDECRYPT()

```
sdencrypt(data, key, encoding)
sddecrypt(data, key, encoding)
```

Three arguments. The encoding is `201` for hex or `202` for base64.

**A passphrase is not a key, but an ordinary program can make one.**
`sdencrypt('The quick brown fox', 'secretkey', 202)` returns **nothing** and
sets `status()` to **10204**, a key length error. The key has to
be an encoded 256-bit key. Make it with `sdkey(passphrase, salt)`, where the salt
comes from `sdsalt()` and is kept with the data, or take a random one from
`sdrandkey()`; both are in every account, and
[SD Basic - Encryption](06a-sd-basic-encryption.html) has the worked example.
Until 18 October 2026 this page said the opposite, and that there was no way in:
that stopped being true when `sdsalt()`, `sdkey()` and `sdrandkey()` were added.

## UMASK()

```
umask(n)
```

Sets the file creation mask and returns the **previous** value. A negative
argument asks without setting:

| call | returned | mask afterwards |
|---|---|---|
| `umask(-1)` | `2` | `2` — unchanged |
| `umask(18)` | `2` — the old value | `18` |
| `umask(-1)` | `18` | `18` |
| `umask(2)` | `18` | `2` — restored |

So the way to change it temporarily is to keep what the setting call returned
and pass it back.

## @SENTENCE and the other @variables

`@sentence` holds the command line that started the program: `RUN BP ZZMATH`.

| | Value |
|---|---|
| `@who` | `DON` — **upper case** |
| `@logname` | `don` — **lower case** |
| `@path` | `/home/sd/user_accounts/don` |
| `@sdsys` | `/usr/local/sdsys` |
| `@userno` | `67`, the same as `system(18)` |
| `@tty` | **empty in a piped session** |
| `@system.return.code` | `1` |
| `@user.return.code` | `0` |
| `@crtwide` / `@crthigh` | `200` / `9999` — whatever `TERM` last set |

**`@who` and `@logname` differ in case for the same account.** Compare them
with `upcase()` on both sides or the test fails on a machine where it worked.

`set.exit.status` sets what SD returns to the operating system when the session
ends.

## OS.EXECUTE

```
os.execute command {capturing variable}
```

**It needs the account's `os-on` switch**, which SDSYS turns on and a new
account does not have. Without it the statement stops the program with
"*name* is not permitted to use OS.EXECUTE" before the command is touched.
With it, `OS.EXECUTE` executes at the account's own Linux permissions, the
same wall that already governs what that account's user could do at a shell
prompt outside SD. A subroutine your program calls is held to the same rule.
See the *Administrator* set's *Accounts and Security* chapter, "The
operating-system switches: `sh-on` and `os-on`".

## LOGMSG

```
logmsg text
```

Writes a line to SD's error log. It has no return value, and **what `status()`
says afterwards is whatever the previous statement left there** — worth knowing
because it looks like a result.

## What is not here

**A whole family of functions is internal-only, and the compiler's complaint
names something else entirely.** This program, in an ordinary account:

```
      v1 = kernel(28, 0)
      v5 = option('X')
      v6 = pterm(1, '')
```

compiles to, at the **last line of the program** (line 4 of this four-line
file, counting its `end`):

```
4: Matrix KERNEL is not referenced in a DIM statement
WARNING: KERNEL is not assigned a value
WARNING: OPTION is not assigned a value
WARNING: PTERM is not assigned a value
1 error(s)
```

A name the compiler does not know as a function is read as a **matrix
reference**, so the complaint is about a `dim` statement you never wrote, at a line
number nowhere near the call. **If a function you are sure exists produces
that, it exists and this account may not call it.** A call with three arguments
gives a different but equally misleading answer — `sdext(101, 'pw', 'salt')`
is *"Right bracket not found where expected"*, because a matrix takes at most
two subscripts.

Internal-only: `kernel()`, `option()`, `pterm()`, `sdext()`, `testlock()` and
`getlocks()`.
The compiler's list is longer than that; those six are the ones this page
put in front of it. They are reachable only from a program compiled
with `$internal`, which additionally requires an administrator in the `SDSYS`
account.

**`ospath()` is not on that list any more.** Any program may call it, with the
openQM keys, and the account's OS access gate decides what it may look at:

```
ospath(path, key {, qualifier})
```

| key | name | answer |
|---|---|---|
| 0 · 1 | | is *path* a valid path name · a valid single file name (text only, no gate) |
| 2 | | it exists, as a file or a directory |
| 3 | | a file name `D` and seven digits that is not in the directory *path* (the name, not the path) |
| 4 · 9 | `os$fullpathx` | the full path name; SD keeps the case, so the two are one |
| 5 | | delete a file or an **empty** directory — never a tree. True if it was removed |
| 6 | | is it open in SD, by any user |
| 7 | | when it was modified, as an epoch value; 0 if it is not there |
| 8 | | flush this process's cache of dynamic files; true |
| 10 | `os$parent` | the parent directory |
| 11 · 12 | `os$uid` · `os$gid` | the owner's and group's numbers; 0 if the path is not there |
| 13 · 14 | | make a directory · make it and the levels above it; true if done |
| 15 | `os$modes` | the permission bits as a decimal number (`0755` is 493); 0 if it is not there |
| 16 · 17 | `os$is.file` · `os$is.dir` | a file · a directory |
| 18 | | the Windows owner: a null string on Linux |

The names are in the `keys.h` header; 6 and 18 have none, so give those as numbers. Every key that
looks at or changes the file system (all but 0, 1, 4, 8, 9, 10 and 18) asks the account's gate
first: an account with neither `os-on` nor `sd-on` is held to its own directory, and a refusal
answers false with `status()` set to a permission error. An unknown key answers false with
`status()` 1. The qualifier is read and ignored. An internal program's own `ospath()`, with its
different numbers, is unchanged.

**And some statements are restricted the same way.** These 34 are
*"Unrecognised statement"* to a program that is not compiled `$internal` by an
administrator (each was compiled once in a plain program to check):
`add`, `akclear`, `akdelete`, `akenable`, `akread`, `akrelease`, `akwrite`,
`callv`, `configure.file`, `create.ak`, `delete.ak`, `delete.common`,
`keyboard.input`, `modify`, `quit`, `release.lock`, `remove.token`,
`reset.modes`, `rewind`, `run`, `set.modes`, `set.status`, `set.trigger`,
`set.unassigned`, `sortinit`, `unload.object`, `varset`, `writepkt`, `como`,
and the whole debugging family — `debug.on`, `debug.off`, `debug.set`,
`breakpoint` and `watch`. An earlier version of this list gave 13 of them and
left out `set.status`; it is the compiler's own `restricted.statements` list
that counts, and the *Administrator* set's *SD Basic - Restricted Commands*
page carries the same names.

**`errmsg` is not a statement at all.** It compiles to *"Unrecognised
statement"* for everybody, as any word the compiler does not know does. It was
removed from the compiler's statement table in July 2024. An earlier version of
this page said the name was left behind in the table; only a comment beside the
table still holds it.

**`sendmail`, `chgphant()` and `ccall()` compile for an ordinary account**, and
each needs something outside SD before it can do anything: `sendmail` a mail
relay, `chgphant` a phantom to change, and `ccall` a C function registered into
the executable. Nothing on this page depends on them.

**`procread` and `procwrite`** belong to the PROC language rather than to BASIC
and are only meaningful inside one.

## See also

[SD Basic - Program Control](02-sd-basic-program-control.html) ·
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html) ·
[SD Basic - Debugging](17-sd-basic-debugging.html) ·
[SD Basic - Locks and Transactions](14-sd-basic-locks-and-transactions.html).

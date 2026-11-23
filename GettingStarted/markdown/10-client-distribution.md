Title: Client distribution
Subtitle: The shared library an application needs, why there are two names, and how to build one.

An application reaches SD Core for Linux through a shared library. **You do not have to
find it inside an installed SD system** — the source builds standalone as
well, because the person writing an application and the person running the
server are not always the same person.

## Two names, one source

```
sdclilib.so
libsdcli.so
```

Both are built from the same object files in the same step — `sdclilib.so`
is the name an application historically asks for; `libsdcli.so` follows the
ordinary Unix `lib*.so` convention (`-lsdcli` at link time). **They are not
two copies to keep in sync by hand** — one build target produces both, so
there is nothing to drift.

**There is no 32-bit client**, for Linux or for Windows: a 32-bit application
must be built again as a 64-bit one. A program written for QM does not work
with SD out of the box, because of the changes SD has made.

## Where it lands

Built to `bin/` under the source tree by `make sd`; a server install places
it alongside the `sd` binary itself, under `/usr/local/sdsys/bin`. There is
no separate client-only package yet — building from source, or copying the
`.so` from an existing install, is how an application gets it today.

## The library must speak SCRAM

**There is no cleartext API login.** A client that sends a password in
clear is refused with *"Cleartext login is no longer supported; this server
requires SCRAM authentication"*. Use the client library that comes with SD.

An account that has no password set is refused, **and the refusal reads as a
wrong password**, because from the server's point of view there is no
credential to check; `modify.password` sets one.

## Connecting

Your application code does not change. `SDConnect()` and `SDConnectLocal()`
take the same arguments and return the same things they always did.

| | |
|---|---|
| `SDConnect()` | over the network, to port **4247** |
| `SDConnectLocal()` | on the same machine. **Sends no password and never did**, so SCRAM does not apply |

BASIC programs reaching another SD server use the `!sdclient` class, which
speaks the same SCRAM login, so a program that uses it needs no change.

Everything about what a connected session may open, the three gates it must
clear, and the identity it runs as is on [API access](09-api-access.html).

## Building from source

The source lives in the server's own repository at
`sdb_ai/sd64/gplsrc/sdclilib`, and `make sd` produces it together with the
server — <https://github.com/dmontaine/SDCore4Linux>. **No built `.so` is
committed**, so a clone builds — the same no-binaries rule the whole
repository follows.

A standalone copy of the same source, kept in sync for building the client
without the whole server tree, is at
<https://github.com/dmontaine/linuxsdclilib>.

**The C headers are shipped with the source tree**, and **a header for each of seven more languages
is installed with the server**, in `/usr/local/sdsys/syscom`: `sdclient.bas` (Basic), `sdclient.pb`
(PureBasic), `sdclient.module` (Gambas 3), `sdclilibbind.pas` (Free Pascal and Lazarus), `sdclient.py`
(Python 3), `sdclient.cs` (C# and .NET) and `sdclient.php` (PHP, with FFI), beside `sdclilib.h`. All
eight declare every function of the library; see *SD Client API* and *SD Client API: Language Bindings*
in the **User** set.

**They are for clients on any machine.** The server carries them so that whoever writes a client has them,
including a Windows client of this Linux server: it uses the same files with the Windows kit's C client
library, `sdclilib.dll`, in place of `sdclilib.so` (the same functions, the same protocol and login).
SD Core for Windows does the same the other way round and carries the Linux client's files.

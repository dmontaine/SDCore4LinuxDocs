Title: SD Client API: Language Bindings
Subtitle: The headers for eight languages, and what the API cannot do.

This page continues [SD Client API](37-sd-client-api.html).

## Language bindings

A header for each of eight languages is in the `syscom` directory of the
installation (`/usr/local/sdsys/syscom`). Each declares **every function in the
reference above**, with the parameters the library takes; the function
signatures are identical in meaning and the syntax differs. They are copies to
take into your own project, not something SD loads.

**They are for client programs on any machine, not only on the server's.** The
server's installation carries them so that whoever writes a client has them,
and a client on Windows uses the same files with the C client library of SD
Core for Windows, `sdclilib.dll`; a client on Linux uses `sdclilib.so`. The two
libraries have the same functions and speak the same protocol and login, so a
client built on either can connect to a server of either kind. (A Windows
program against a Linux server has not been run in this release; the protocol
is shared, the programs have not met.) The Visual Basic header, `sdclient.bas`,
is the exception that proves it: it is for the Windows VB DLL, `sdclient.dll`.

| Language | File | Notes |
|---|---|---|
| C, C++ | `sdclilib.h` | |
| Basic (Visual Basic) | `sdclient.bas` | for the VB client DLL: no `SDCallx`, `SDGetArg`, `SDDebug` or `SDFree` |
| PureBasic | `sdclient.pb` | procedures that call the library: `SDCall0` to `SDCall20`, `SDCallx0` to `SDCallx20`; strings the library returns are freed for you |
| Gambas 3 | `sdclient.module` | `Extern` declarations; change the `Library` path to where `sdclilib.so` is |
| Free Pascal, Lazarus | `sdclilibbind.pas` | unit `SdCliLibBind`: the types, the function pointers, and `LoadSdCliLib` / `UnloadSdCliLib` |
| Python 3 | `sdclient.py` | `ctypes` bindings with `argtypes` and `restype` for each function; `import ctypes` and the library path are at the top |
| C#, .NET | `sdclient.cs` | the static class `SDClient`: a P/Invoke declaration for each function, `Z()` / `Str()` / `StrN()` to turn a string into the bytes a parameter wants and a result back into a string, and `SDCall0` to `SDCall20` / `SDCallx0` to `SDCallx20`. Works with `sdclilib.so` on Linux and `sdclilib.dll` on Windows |
| PHP 7.4 and later | `sdclient.php` | the class `SDClient`: the library's C declarations for the FFI extension, `SDClient::load()`, and `str()` / `strn()` / `intRef()` helpers. FFI must be enabled (`ffi.enable=true` for a web server's PHP) |

None of them declares `SDEnterPackage` or `SDExitPackage` (licensed packages
are not supported) or `SDConnectUDS` (removed; the Python header would not
load with it). Where the library returns a string it has allocated, the memory
is yours to give back with `SDFree`. In Python, `restype = ctypes.c_char_p` copies
the string and leaves the original allocated, which leaks in a program that makes
many calls; declare `c_void_p`, read it with `ctypes.string_at()` and pass it to
`SDFree` if that matters to you. `SDCallx` returns nothing, and `SDReadList` and
`SDReadNext` take only the list number: the extra `ErrNo` argument in the Gambas
header is ignored by the library.

### Gambas 3

```
Library "./sdclilib"
Extern SDConnect(Host As String, Port As Integer, UserName As String,
  Password As String, Account As String) As Boolean
Extern SDRead(FileNo As Integer, Id As String,
  ByRef Errno As Integer) As String
```

### PureBasic

```
IncludeFile "/usr/local/sdsys/syscom/sdclient.pb"
If SDConnectLocal("myaccount")
   fno.l = SDOpen("CUSTOMERS")
   Debug SDRead(fno, "1001", @errno.l)
   SDDisconnect()
EndIf
```

### Free Pascal / Lazarus

```pascal
uses SdCliLibBind;
...
if LoadSdCliLib('/usr/local/sdsys/bin') and (SDConnectLocal('myaccount') <> 0) then
begin
  Fno := SDOpen('CUSTOMERS');
  ...
  SDDisconnect;
end;
UnloadSdCliLib;
```

`LoadSdCliLib` loads `sdclilib.so`, resolves every function pointer and
returns False, with all of them nil, if the library or any one function is
missing; `UnloadSdCliLib` releases it.

### Python 3 (ctypes)

```python
import ctypes
_lib = ctypes.CDLL('./sdclilib.so')

SDEvalConv = _lib.SDEvalConv
SDEvalConv.argtypes = [ctypes.c_int, ctypes.c_char_p,
    ctypes.c_char_p, ctypes.c_char_p]
SDEvalConv.restype = ctypes.c_char_p
```

The file also defines `CFUNCTYPE` types for the per-arity `SDCall` and
`SDCallx` wrappers (`SDCall0_type` to `SDCall20_type`, `SDCallx0_type` to
`SDCallx20_type`).

### C# and .NET (P/Invoke)

```csharp
using static SDClient;

if (SDConnect(Z("server"), 4247, Z("user"), Z("password"), Z("account")) != 0)
{
    int fno = SDOpen(Z("CUSTOMERS"));
    string rec = Str(SDRead(fno, Z("1001"), out int err));
    SDDisconnect();
}
```

**Strings are bytes.** SD strings carry the marks `0xFB` to `0xFF`, and a
UTF-8 conversion by .NET would damage them, so every string parameter is a
`byte[]` and every string result an `IntPtr`; `Z(s)` makes the NUL-terminated
bytes of a string (one byte for each character, characters above 255 are not
allowed) and `Str(p)` / `StrN(p, n)` read a result the same way and give the
library's memory back with `SDFree`. `FM`, `VM` and `SVM` are the marks as
characters. An `int *` parameter is an `out int`. Variadic C functions cannot
be declared in C#, so `SDCall` and `SDCallx` are `SDCall0` to `SDCall20` and
`SDCallx0` to `SDCallx20`, all the same entry point; **`SDCall` writes the
subroutine's results back into the buffers you give it with no check of their
size, so use `SDCallx` and read the arguments with `SDGetArg`.**

The library is loaded by the name `sdclilib`: `sdclilib.dll` on Windows,
`sdclilib.so` or `libsdclilib.so` on Linux, from where .NET looks (the
program's directory, `PATH` or `LD_LIBRARY_PATH`, or a resolver you set with
`NativeLibrary.SetDllImportResolver`). The calling convention is cdecl on both.
A 64-bit program needs the 64-bit library.

### PHP (FFI)

```php
require 'sdclient.php';
$sd = SDClient::load('/usr/local/sdsys/bin/sdclilib.so');
if ($sd->SDConnect('server', 4247, 'user', 'password', 'account')) {
    $fno = $sd->SDOpen('CUSTOMERS');
    $err = SDClient::intRef();
    $rec = SDClient::str($sd->SDRead($fno, '1001', FFI::addr($err)));
    $sd->SDDisconnect();
}
```

A PHP string is already a string of bytes, so the marks pass through unchanged.
`SDClient::str($p)` copies a result into a PHP string and frees the library's
copy; `strn($p, $n)` does the same for `$n` bytes that may hold zeros
(`SDReadBlk`). Use `SDCallx` and `SDGetArg` rather than `SDCall`, which writes
into the buffers it is given and must not be given a PHP string.

**Neither of these two files has been run.** No .NET or PHP runtime was
available when they were written; they are held to the library's header by a
check (every function, every parameter and result type, the calling convention,
the status constants, and the PHP declarations read by a C compiler beside the
header itself), which is not the same as a program having called the library.
If one does not load for you, the report is welcome.

## What the API cannot do

| | |
|---|---|
| `sh` and `OS.EXECUTE` | **only if the account holds `sh-on` / `os-on`**: the API server reads the account's switches when it enters the account, as sign-in does, and a new account has neither (SDSYS has none, so it has no shell over the API). `SDCLIENT` in `sd.conf` is the further control, if a site wants one; see the *Administrator* set's *Configuration* chapter |
| Open files outside the account | refused (status 3035 — *not permitted*) |
| Reach the credential file | never, and cannot be added |
| Enumerate accounts | refused; all three failure cases give the same message |

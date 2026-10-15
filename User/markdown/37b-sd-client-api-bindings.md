Title: SD Client API: Language Bindings
Subtitle: The headers for six languages, and what the API cannot do.

This page continues [SD Client API](37-sd-client-api.html).

## Language bindings

A header for each of six languages is in the `syscom` directory of the
installation (`/usr/local/sdsys/syscom`). Each declares **every function in the
reference above**, with the parameters the library takes; the function
signatures are identical in meaning and the syntax differs. They are copies to
take into your own project, not something SD loads.

| Language | File | Notes |
|---|---|---|
| C, C++ | `sdclilib.h` | |
| Basic (Visual Basic) | `sdclient.bas` | for the VB client DLL: no `SDCallx`, `SDGetArg`, `SDDebug` or `SDFree` |
| PureBasic | `sdclient.pb` | procedures that call the library: `SDCall0` to `SDCall20`, `SDCallx0` to `SDCallx20`; strings the library returns are freed for you |
| Gambas 3 | `sdclient.module` | `Extern` declarations; change the `Library` path to where `sdclilib.so` is |
| Free Pascal, Lazarus | `sdclilibbind.pas` | unit `SdCliLibBind`: the types, the function pointers, and `LoadSdCliLib` / `UnloadSdCliLib` |
| Python 3 | `sdclient.py` | `ctypes` bindings with `argtypes` and `restype` for each function; `import ctypes` and the library path are at the top |

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

## What the API cannot do

| | |
|---|---|
| `sh` and `OS.EXECUTE` | **only if the account holds `sh-on` / `os-on`**: the API server reads the account's switches when it enters the account, as sign-in does, and a new account has neither (SDSYS has none, so it has no shell over the API). `SDCLIENT` in `sd.conf` is the further control, if a site wants one; see the *Administrator* set's *Configuration* chapter |
| Open files outside the account | refused (status 3035 — *not permitted*) |
| Reach the credential file | never, and cannot be added |
| Enumerate accounts | refused; all three failure cases give the same message |

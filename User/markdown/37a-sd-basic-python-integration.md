Title: Embedded Python
Subtitle: The CPython interpreter built into SD, the dictionary, list and string objects it exposes, and the twenty-one cataloged functions that reach it from BASIC.

SD Core for Linux embeds CPython so a BASIC program can run Python code and
exchange data with it. Twenty-one cataloged routines carry this - counted
alongside the rest of SD's global catalog in the User set's *SD Standard
Subroutines* page, which does not repeat them; this page is where they are
documented.

## The short version

A BASIC program declares each function it uses, then calls it like any other:

```
deffun PY_CREATEDICT(dictname) calling '!PY_CREATEDICT'
status = PY_CREATEDICT('mydict')
```

All twenty-one are `$internal`-compiled and ship already cataloged, so no
account needs to compile or catalog anything to use them - only the
declarations and a call. `$include sdpyfunc.h` declares all of them at once.
Failure is always `status()`, not the returned value: several of
these functions return an empty string on both "genuinely empty" and
"failed," so `status()` is what tells them apart. **Every function that takes an object,
dictionary, list or string name refuses an empty one before making the
underlying call**, setting `status()` to 1: a function that returns a value
returns an empty string (`PY_OBJLEN` returns 0), and one that returns a status
returns 1 - never one of the `-120xx` codes below, which all describe
something Python said.

**Starting the interpreter and running code in it need the account's `os-on`
switch** - the same one as `OS.EXECUTE`, because Python runs arbitrary code in
your own process. SDSYS turns it on with `modify.account` *name* `os-on`; a new
account does not have it. The question is put to the **account**, not to the
routine: `$internal` controls who may *compile* a new internal-mode program, and
a cataloged routine like `PY_CREATEDICT` is internal, but the interpreter
itself refuses to start for an account without `os-on`. `PY_INITIALIZE` then
returns null with `status()` 3035 and prints nothing, so a program that needs
Python should test for it.

**The installer brings what this needs.** Python is built into SD when it is
installed, so nothing is left for an administrator to install separately
afterwards.

## Interpreter lifecycle

| Function | Returns |
|---|---|
| `PY_INITIALIZE()` | 0 if the interpreter is already running or starts cleanly; otherwise an error code below. A second call is a no-op that also returns `0`. Python's own `print()` writes to your terminal, with line endings that suit a terminal session |
| `PY_IS_INITIALIZED()` | 1 if the interpreter is running, 0 if not. Never fails and never needs the permission check, so it is the one `PY_` call safe to make from any session as a probe |
| `PY_FINALIZE()` | Shuts the interpreter down. Rarely needed - a session ending does this for you |
| `PY_RUNSTRING(script)` | Runs `script` as Python source in the interpreter's global namespace. An empty `script` is refused before it reaches Python (`status()` 1) |
| `PY_RUNFILE(path)` | Runs the Python file at `path`. `path` is checked for shape before it is run: a path that is empty, is longer than 255 characters, or holds anything but letters, digits and `. _ - / :` is refused (`status()` 1) without reaching Python |

```
st = PY_INITIALIZE()
if st # 0 then
   * st is one of the error codes below
end
```

## Dictionaries

A "dictionary" here is a Python `dict`, held by name in the interpreter's own
namespace - `dictname` is a handle, not a value. It has string keys and string
values.

| Function | Returns |
|---|---|
| `PY_CREATEDICT(dictname)` | Creates an empty dictionary |
| `PY_CLEARDICT(dictname)` | Empties it. The name stays in the namespace |
| `PY_DICTVALSETS(dictname,key,value)` | Sets (or creates) `key` to the string `value` |
| `PY_DICTVALGETS(dictname,key)` | Returns the string value of `key`, or an empty string if it is not there (`status()` -12007) |
| `PY_DICTIDEL(dictname,key)` | Deletes `key` |
| `PY_DICTGETKEYS(dictname)` | Returns every key, field-mark (`@fm`) separated |
| `PY_DICTGETVALUES(dictname)` | Returns every value, field-mark (`@fm`) separated |

## Lists

A Python `list`, likewise held by name.

| Function | Returns |
|---|---|
| `PY_LISTCREATE(listname)` | Creates an empty list. `PY_LISTCRTE` is the same function under an older name; both work |
| `PY_LISTCLR(listname)` | Empties it |
| `PY_LISTAPPD(listname,objname)` | Appends the named Python object - a string, a dictionary, another list made with these functions, or anything a script left in the namespace - to the list |
| `PY_LISTGETS(listname)` | Returns every item, field-mark (`@fm`) separated |

A list has to be made with `PY_LISTCREATE` before anything is appended to it.
It is shaped like `PY_CREATEDICT`, and a name that is already taken is refused
with its own "list already exists" code (`-12038`).

## Strings

A Python `str`, held by name - distinct from an ordinary BASIC string
variable.

| Function | Returns |
|---|---|
| `PY_STRSET(strname,value)` | Sets (or creates) the named Python string to `value` |
| `PY_STRGET(strname)` | Returns its value |

## Reading an object generically

These take the name of any Python object already created above - a
dictionary, a list, a string, or anything a run script left in the
namespace - rather than a type-specific handle.

| Function | Returns |
|---|---|
| `PY_OBJLEN(objname)` | Its length, as Python's own `len()` would report. Returns `SD_INT_OVERFLW` (**-10302**) if the true length does not fit a 32-bit int |
| `PY_OBJTYPE(objname)` | A numeric type code, **not a type name** - see the table below |
| `PY_GETATTR(objname)` | Its value as a string |

`PY_OBJTYPE` returns one of six codes - a number, not the word "list" or
"dictionary" (a list made with `PY_LISTCREATE` answers `2`):

| Code | Python type |
|---|---|
| 0 | unknown - none of the five below |
| 1 | string (`str`) |
| 2 | list |
| 3 | dictionary (`dict`) |
| 4 | integer (`int`) |
| 5 | float |

## Error codes

Every function that returns a status uses one of these, defined in `err.h`
of the `syscom` file:

| Code | Meaning |
|---|---|
| -12001 | interpreter not initialized |
| -12002 | `PyDict_New()` failed |
| -12003 | failed to set `__builtins__` |
| -12004 | an exception was raised running the script |
| -12005 | error reported by `PY_FINALIZE` |
| -12006 | could not open the script file |
| -12007 | key not found in the dictionary |
| -12008 | failed to convert a Python object to a string |
| -12009 | error encoding a Python string from Unicode to Latin-1 |
| -12010 | cannot import `__main__` |
| -12011 | could not get the `__main__` dictionary |
| -12012 | dictionary already exists |
| -12013 | failed to add to the namespace |
| -12014 | the named object does not exist |
| -12015 | failed to set a dictionary key/value |
| -12016 | failed to delete a dictionary key/value |
| -12017 | object is not a dictionary |
| -12018 | error encoding a string from Latin-1 to Unicode |
| -12019 | object is not a string |
| -12020 | failed to remove the object from the namespace |
| -12030 | object contains no items |
| -12031 | failed to create a Python string object |
| -12032 | failed to concatenate Python string objects |
| -12033 | failed to access a list item |
| -12034 | object is not a list |

The gap between -12020 and -12030 is not a reservation for anything
documented here - it is simply where the two error blocks were written, ten
codes apart.

**The list functions have four codes of their own, -12035 to -12038.** A wrong
type reports -12034 and a missing append target -12014; the append or clear
call itself failing is -12035 or -12036:

| Code | Meaning |
|---|---|
| -12035 | list append failed |
| -12036 | list clear failed |
| -12037 | `PyList_New()` failed |
| -12038 | list already exists |

The permission is the account's `os-on` switch, above: a program whose account
has not got it is refused by SD before Python is touched, and the `PY_`
function gives back a non-zero `status()` (3035), not one of the codes in these
tables.

## Example programs

Four example programs are installed in the SDSYS account's `bp` file:

| Program | What it shows |
|---|---|
| `PY_TEST` | starting Python, running a short script, and reading its results back: the dictionary and list the script made, a dictionary and a string made with the functions above, the keys, values and items as field-mark lists, the size and type of each object, and a string appended to a list |
| `PY_TEST2` | the same with data read from a file: a record is stored as a Python string, read back, and compared with the original (`Match` or `Do Not Match!`). Set the file's path near the start (`xxxx` is an account name) before you run it |
| `PY_JSON` | Python's `json` module on a file you name: the file is loaded, then walked object by object with `PY_OBJTYPE`, `PY_OBJLEN` and `PY_DICTGETKEYS`, and every key and value is printed, indented by nesting |
| `PY_TERM` | a minimal prompt that runs the Python you type: lines are collected and `!` runs them, `??` shows them, `?` gives help and `quit` ends; the up and down arrows recall earlier lines |

Copy one into your own account's `bp` to compile and run it. Like any use of
Python, it needs the account's `os-on` switch. A short sequence of the same
kind of calls:

```
$include sdpyfunc.h
st = PY_INITIALIZE()
if st # 0 then stop
st = PY_RUNSTRING('countdown = {"3": "Three", "2": "Two", "1": "One"}')
st = PY_CREATEDICT('my_dict')
st = PY_DICTVALSETS('my_dict', 'k1', 'first value')
crt PY_DICTVALGETS('my_dict', 'k1')    ;* first value
crt PY_OBJLEN('countdown')             ;* 3
keys = PY_DICTGETKEYS('countdown')     ;* the keys, separated by @fm
```


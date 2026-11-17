Title: SD Client API: Select Lists to Error Handling
Subtitle: The rest of the function reference: select lists, the server, dictionary items, sequential files, packages and errors.

This page continues [SD Client API](37-sd-client-api.html).

### Select lists

| Function | Returns | Description |
|---|---|---|
| `SDSelect(fileNo, listNo)` | none | select all records in a file |
| `SDSelectIndex(fileNo, indexName, indexValue, listNo)` | none | select by index value |
| `SDSelectLeft(fileNo, indexName, listNo)` | String | select left of an index cursor |
| `SDSelectRight(fileNo, indexName, listNo)` | String | select right of an index cursor |
| `SDSetLeft(fileNo, indexName)` | none | position cursor left |
| `SDSetRight(fileNo, indexName)` | none | position cursor right |
| `SDReadNext(listNo, err)` | String | read next select list id |
| `SDReadList(listNo, err)` | String | read the whole list as a dynamic array |
| `SDClearSelect(listNo)` | none | clear a select list |
| `SDIndices(fileNo, indexName)` | String | `indices()` on the server: with a null name the names of the file's alternate key indexes, with a name that index's details; the null string for an index the file has not |

### The server: revision, variables, SYSTEM() and transactions

| Function | Returns | Description |
|---|---|---|
| `SDRevision()` | String | the client's revision on its own before a connection; once connected, the client's and the server's, as two values separated by a value mark. Works without a connection |
| `SDGetVar(name)` | String | the value of an `@` variable on the server, with or without the `@`, in either case. The names it knows are `@SELECTED`, `@LOGNAME` (also `@USER`), `@WHO`, `@PATH`, `@USERNO`, `@TTY`, `@DS`, `@SENTENCE`, `@COMMAND`, `@SYSTEM.RETURN.CODE`, `@USER.RETURN.CODE`, `@DATE`, `@TIME`, `@ID`, `@ANS` and `@USER0` to `@USER4`; any other name gives the null string, not an error |
| `SDSystem(key)` | String | `system(key)` on the server |
| `SDTxn(mode)` | none | **1** start a transaction, **2** commit, **3** abort, **4** commit *non-durably*: a transaction nested in another is merged into its parent, which alone writes to the files (see *Locks and transactions*). Modes 2 to 4 need a transaction to be running; a mode out of range or a commit with nothing to commit is refused with a message and the session goes on |

### Dictionary items and conversions

| Function | Returns | Description |
|---|---|---|
| `SDEvaluate(dictFileNo, names, data, id)` | String | evaluate dictionary items on the server against a record. `dictFileNo` is the number `SDOpen("DICT name")` gave, `names` one name or several separated by value marks, `data` the record (it becomes `@RECORD`) and `id` its id (`@ID`; pass the null string when the item does not use it). The answers come back joined by **item marks** (character 255). D and I items work (SD has no A or S items since 2.0-0); an I-type that is not compiled is compiled for the call and the dictionary is **not written to**. A name that is not in the dictionary gives the null string; a phrase or other item that defines no data, and an expression that will not compile, give the null string with `SDError()` saying which. Conversion codes in the item are *not* applied |
| `SDEvalConv(dictFileNo, names, data, id)` | String | the same, and the item's output conversion is applied to each value of its answer |
| `SDIConv(data, code)` | String | `iconv()` on the server, which has every conversion code |
| `SDOConv(data, code)` | String | `oconv()` on the server |
| `SDIConvs(data, code)` | String | `iconvs()`: the conversion is applied to each element of a dynamic array in turn |
| `SDOConvs(data, code)` | String | `oconvs()` |

After a conversion `SDStatus()` is **the conversion's own status** — 0 after a successful one, otherwise as `iconv()` and `oconv()` describe it — and it is for that call alone: the next successful conversion leaves it 0. These need a connection. **A session that the administrator has restricted with `SDCLIENT` cannot reach a file or call a program, so it is refused a conversion code that does either** — a `T` code with a file in it, or a `U` code; the ordinary codes (dates, masked decimals, case) are not affected.

### Sequential files

| Function | Returns | Description |
|---|---|---|
| `SDOpenSeq(file, id, modes)` | Integer | open a sequential file, as `openseq` does. With an `id`, `file` is the name of a **directory file** and `id` the item in it; with a **null `id`**, `file` is a **pathname**. Returns a file number, or **0** with `SDStatus()` and `SDError()` saying why. A file that is not there yet gets a number and is made by the first write. `modes` is added up from: **2** give up with a locked answer if another process has the file (without it the call waits), **16** read only, **256** append, **512** overwrite (empty the file on opening), **1024** flush after every write, **4096** shared (append, for several writers) |
| `SDReadSeq(fileNo, err)` | String | the next line, without its terminator. `err` is the server's answer: **2** at the end of the file, where the string is empty |
| `SDReadBlk(fileNo, bytes, actual)` | String | up to *bytes* bytes (1 to 100,000,000). `actual` is how many came back: fewer at the end of the file, **0** with nothing left. The data may hold any byte, zero included, so read it by `actual` and not by its terminator |
| `SDWriteSeq(fileNo, rec)` | none | write a line and a terminator |
| `SDWriteBlk(fileNo, rec, bytes)` | none | write exactly *bytes* bytes, no terminator added |
| `SDSeek(fileNo, offset, relTo)` | none | position: *relTo* **0** from the start, **1** from here, **2** from the end (a negative offset counts back) |
| `SDWeofSeq(fileNo)` | none | cut the file off at the current position |
| `SDClose(fileNo)` | none | close it (the same function as for any file) |
| `SDWriteSeqKey(fileNo, rec)` | String | **not a sequential file function**: write *rec* to the **hashed** file `SDOpen` gave, under the id the file's own counter gives it (`write … creating.seqkey`), and return that id. The update lock the write takes is released before the call returns. A directory file is refused, with the null string and `SDError()` saying a hashed file is needed |
| `SDWriteuSeqKey(fileNo, rec)` | String | the same, and the update lock is **kept** (`writeu`) |

Their numbers begin at 10001 and are not those of `SDOpen`, so a number of one kind given to a function of the other is refused. The counter starts at 1 and is set with `configure.file … next` ([SD Basic - File Handling](07-sd-basic-file-handling.html)).

**The gates are the ones `openseq` has for any program.** A session whose server is restricted with `SDCLIENT` cannot open any file. An item of a directory file is an SD file and is opened through the VOC, as `openseq` opens it; a file flagged trusted is refused. **A bare pathname is an operating system file, and an account without the `os-on` switch reaches only its own directory by it**: `/etc/hostname`, a sibling account's file, a path that climbs out with `..` and a new file in `/tmp` are all refused with *… is not a file this account may open*, and nothing is made. (The API server asks the account's own switch itself: it is an internal program, which the kernel does not otherwise hold to the gate.)

### Packages

| Function | Returns | Description |
|---|---|---|
| `SDEnterPackage(name)`, `SDExitPackage(name)` | Boolean | **not supported**: licensed packages are not part of SD and the server refuses both. The library still exports them, and the language headers do not declare them |

### Error handling

| Function | Returns | Description |
|---|---|---|
| `SDError()` | String | get the last error message |
| `SDDebug(mode)` | none | enable/disable debug mode |
| `SDStatus()` | Long | get the last server status code |
| `SDFree(ptr)` | none | free a returned pointer |

## Continued in

[SD Client API: Language Bindings](37b-sd-client-api-bindings.html) — the eight
language headers and what the API cannot do

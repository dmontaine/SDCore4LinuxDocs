Title: sdfix: What It Checks and Repairs
Subtitle: Every error a check reports, what -F or -Q does about it, the dump and rebuild of mis-hashed groups, interactive mode, and the faults in the tool that were found by running it and fixed.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

This is the second half of [sdfix, the File Check Tool](14-sdfix.html), which
has the options and the rules for running it.

## What a check reports, and what `-F` does

A check never changes the file, except for `-Z`. Under `-F` every row with a
repair is done without asking; under `-Q` each is offered with `Fix?`.

| The check says | Meaning | The repair |
|---|---|---|
| `Invalid group size (n bytes)` | the header's group size is not a multiple of 1,024 or is out of range | none; the check stops |
| `Large record size is invalid (n)` | the size above which a record goes to its own blocks is outside the group | resets it to the group size less the block header |
| `Invalid split and/or merge loads (a, b)` | split load is not above merge load | writes the defaults SD gives a new file, split 80 and merge 50, and says `Corrected by resetting to defaults (80, 50)` |
| `AKn subfile found but not expected` | an index file the header does not list | deletes the file (an index in the file's own directory or in a relocated index directory), and says `Corrected by deleting affected AK index subfile` only if it went; otherwise `The AK index subfile could not be deleted` |
| `AKn subfile not found` | the header lists an index whose file is gone | removes the index from the header. **The file then has no index of that name.** Create and build it again |
| `Cannot read AKn subfile header`, `AKn subfile has incorrect magic number` | a damaged index file (the magic number) | deletes the file and removes the index from the header (if the file could not be deleted it says so and still removes the index from the header). An index file that cannot be read at all (an empty one, say) is reported once, as `Cannot read AKn subfile header`, and repaired once. Create and build it again |
| `Active group n found after released group(s)!` | a used group follows groups marked as released | writes empty groups over the released ones |
| `Group n has incorrect block type (t)` | | sets the type to data |
| `Record 'id' mis-hashed into group n. Should be in group m` | the record's id does not hash to the group it is in | queues the group for dump and rebuild (below). Only `-F` queues; `-Q` reports only. At most 50 are reported |
| `Error in large record. Group g, ... Record cannot be recovered.` | the chain of a large record is broken | **deletes the record**; its header is cut out of the group |
| `Apparent modulus a differs from recorded modulus b` | the groups actually in use do not match the header | sets the header's modulus to the number of groups in use |
| `Incorrect mod_value (a), expected b` | | sets it |
| `Minimum modulus is invalid (n)` | | sets it to 1 |
| `Load error: Actual a, file header b` | the bytes in use differ from the header's count | updates the header |
| `Record count error: Actual a, file header (adjusted) b`, `Header record count has not been set` | | updates the header |
| `Overflow block x has non-zero used byte count` | a block on the free chain holds data | clears it |
| `Faulty next block pointer`, `Read error at ...` | the free chain is broken | none; the walk of the free chain stops |
| `Overflow block n (xaddr) unreferenced` | reachable from no group, large record or free chain | puts it on the free chain |
| `AK n node k unreferenced` | an index node reachable from nothing | puts it on the index's free node chain |
| `Non-existant node`, `Read error on node`, `Type t node ... also referenced from`, `Unexpected node type`, `Invalid forward pointer in free node` and the like | the index tree is damaged | **none**. Index trees are only reported on. Delete the index and build it again |

The header's longest-id value is also reset to the real longest id under `-F`,
without a message, because a value above SD's id limit would stop the file
opening.

**`-F` is not a repair of last resort.** Several rows rewrite the header from
what the scan found. If the scan is wrong because a group is damaged, the
header is then wrong in step with it, and the next run is quiet about it. Look
at what a check reports before you let `-F` act on it.

## Dump and rebuild of mis-hashed groups

When `-F` has queued groups, the check ends with a question that **is asked
even under `-F`**:

```
Dump and rebuild groups with mis-hashed records? Y
Creating temporary file
Data copied to temporary file
Original groups cleared
Data rewritten
Temporary file deleted
```

In this example the header's mod value was 1, so half the records hashed
to the wrong group. The check reports 20 records, the `-F` run sets the mod value
back to 2 and rebuilds the group, and a second check is clean. All 40 records
were still there.

* The temporary file is `~SDFix.n` (n is your numeric user id) **in the
  directory you ran the program from**, not beside the file. It holds a copy of
  every queued group (its size is the group size times the groups queued, plus
  overflow). Run from somewhere with room for it.
* The order is: copy the groups out, clear them in the file, write the records
  back. **If the run stops after "Original groups cleared", the records exist only
  in the temporary file.** Keep it and your backup together.
* It queues at most 50 groups, and only the groups holding the first 50
  mis-hashed records reported. A damaged file may need the run repeated until a
  check is clean.
* If a record that is in the wrong group also exists in its right group, the
  program prints *Record 'id' not moved as a correctly hashed version also
  exists*. **This case was not provoked here**, and the code that follows the
  message does not skip the record. Compare record counts after a run that
  prints it.

## Interactive mode (`-I`)

This is a developer's debugging tool, and it can write anywhere in the file.
**It is off unless the configuration file has `DEBUG` with bit 2 set** (`DEBUG=2`
in the `[sd]` section). Without that, `sdfix -I` prints the usage text and does
nothing.

The prompt shows the selected subfile (`0?`). Commands: `check`, `fix`
(a check with `-F`'s unconditional repairs); `Gn` display group *n*, `ga` all
groups; `h` the header, with the file offset of each field in hex; `Lid` the
hash value, group and address of a record id; `Sn` select a subfile (0 primary,
1 overflow, 2 onward indexes); `n` and `p` next and previous window; a number
shows the window at that decimal address; `rebuild n` dump and rebuild group *n*;
`recover`; `z` the file's statistics counters; `?`; `q`.

* **Addresses it prints with an `x` in front are decimal.** `Header size 2048
  (x0800)` is the hex form; `Group 1 (x000000002048)` is 2,048 in decimal.
  The offsets `h` prints at the start of each line, without an `x`, are hex.
* **`Wa=x` writes into the file.** Do not use it on a
  file you cannot lose. The address *a* is **hex**, the same text `h` prints
  (`W002E=4142`), and the value *x* is 2, 4 or 8 hex digits for 1, 2 or 4 bytes,
  written **in the order you type them**, which is the order a dump of the file
  shows them. It prints `Was` and the bytes that were there. `Wa="text"` writes the
  text. An address past the end of the subfile is `Illegal address`, a value that
  is not 2, 4 or 8 hex digits is `Illegal data length`, and any character that is
  not a hex digit is `Format error in W command`. The address must be hex digits
  followed at once by `=` (spaces before it are allowed): `W1G0=41`, `W10xyz=41`
  and `W10 =41` are format errors and write nothing. The address and the value are
  read as hex digits, as written.
* `h` shows `Next seq id`, the counter used by `write ... creating.seqkey`, and
  warns if it is negative.

## What it will not do

* It checks that SD does not have the file open, and nothing else. When SD is
  not running there is nothing to ask, and a file held by another program,
  `sdidx` or `sdconv` is not seen; the result is whatever the two processes make
  of it.
* It does not take a backup, and no run can be undone.
* It does not repair an index tree. It reports one, and removes an index from the
  header only when the index file is missing or unreadable.
* It does not recover records that are lost. The one repair that removes a record
  is the broken large-record one, and it does so on purpose.
* It works on **hashed files only**: an SD dynamic file, a directory holding `%0`
  and `%1`. A directory file (one OS file per record), a sequential file or a
  non-SD path is skipped, and with only such paths the run says *No SD hashed
  files found matching given name(s)* and exits 1.
* It does not convert byte order. That is `sdconv`, and as built, `sdconv` does
  not convert hashed files at all; see [sdconv](16-sdconv.html).
* It does not move or delete index directories. That is [sdidx](15-sdidx.html).

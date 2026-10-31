Title: Importing a Tape Image
Subtitle: tape.import makes a new user account from a save image written by another system's ACCOUNT.SAVE: what it makes, what it leaves out, the log, and what it will not do.

`tape.import` reads a **save image** and makes a **new user account** from it. The image is a file: the
output of an `ACCOUNT.SAVE` that was written to a tape file. It is the administrator's verb: it is in the
SDSYS account's VOC and in no other, and no one can be given it.

> **This document is separate so that it can be withheld.** It links to nothing outside the
> administrator set.

## The command

```
tape.import image to account {from account} {format as|r83|jbs|fs|mv} {list} {no.query}
```

| Word | Meaning |
|---|---|
| *image* | the absolute path of the save image: a file, never a device. A path with `.` or `..` in it, a doubled slash or a slash at the end is refused. |
| `to` *account* | the name of a **new** user account. An account that exists is refused; nothing is merged into it. |
| `from` *account* | the account the image holds, if you want it checked. An image holds one account in this release. |
| `format` *layout* | the layout of the image: `as` (the default, what the old `ACCOUNT.SAVE` wrote), or `r83`, `jbs`, `fs` or `mv`. See [The layouts](#the-layouts). Any other word is a syntax error; `ultfs` is refused by name. |
| `list` | read the image to the end, say what it holds, make nothing. |
| `no.query` | do not ask whether to go on. A new user account still asks for its password, as `create.account` does: the account is a Linux user. |

`tape.import` reads the whole image **before** it makes anything. An image it cannot understand is
refused with a code and a sentence (*The image was refused: R-NOEOF (no end-of-file block after the
data)*), and nothing has been made. Only then does it ask, make the account, and fill it.

## The layouts

`as` is what the old `ACCOUNT.SAVE` wrote, and it is the only layout that has been checked against an
image a program really wrote. `r83`, `jbs`, `fs` and `mv` are read **as the original reader of the old
tape subsystem read them**, and **no real image of any of them has been seen**: an image of one of them
may be refused although it is good, and a good result does not prove that the system which wrote it wrote
what this reader expects.

| Word | What the reader expects |
|---|---|
| `as` | three labels, with an end-of-file block and a descriptor block between them, then the data |
| `r83` | two labels, with any number of end-of-file blocks between them, then the data |
| `jbs`, `fs` | one label, then the data (the two words read alike) |
| `mv` | one label, then the data, which may contain header tokens; they are left out and logged |

For the layouts other than `as` a label only has to begin with an item mark, `L`, a block size and some
printable text. A block has a pad of NULs or spaces, or none at all (block size `0200`). File numbers are
hexadecimal. Items of the types `F` and `E` are read like ordinary items. The end of the account is marked
`XX`, `XC` or `X`. The account the image holds is the one the first file header of the data names; the
name must be printable and at most 64 characters.

These are refused, each with its own code: `format ultfs` (the original reader's own tests disagree about
where an Ultimate save's data starts); an item of the types `B` and `R`, of the large form `L`, or of the
binary form of another system; and a save made by `T-DUMP`.

## What is made

The new account is a user account with **every gate off**: no ssh, no API, no `sh`, no `os.execute`, no
files access, no edit gates. Turn on what the person needs with `modify.account`, as for any account.

| In the image | In the new account |
|---|---|
| a file's data part | a file of that name, in lower case: dynamic, or a directory file if it was one |
| a file's dictionary | `name.dic`, with its items; an item that SD's own `ACCOUNT.SAVE` had turned from a `D` item into an `A` item is turned back |
| a record | a record of the same id, in lower case, with its fields, values and subvalues as they were. Record content is stored byte for byte and is never interpreted. |
| the old account's VOC | the items that are not pointers, in the file `md.import`; an `F` or `Q` pointer is left out |
| a VOC file or a file whose name the account already has | the file is called `tape.<name>` |

## What is left out, and logged

* A **file name** that is not English letters, digits and `. _ $ -`, that begins with a dot, or that is
  a path. A **record id** with a control character, a byte above 127, a slash, no characters, or more than
  64 characters; and, in a directory file, a quote. Two names that differ only in case keep the first.
* A **binary item**: the old `ACCOUNT.SAVE` stored a record that holds an item mark, a compiled program
  among them, in a form of its own. It is counted and left out. Nothing from an image is ever compiled,
  catalogued or run.
* A **header token** of the layouts other than `as`: it holds no record.
* An **index definition**. The files are made; build the indices with `build.index`.
* A second part of a file with the same name, and a file number that has two headers.

## The log

Every run that reaches the filling step writes a **new record** in the file `tape.log` of the SDSYS
account, whether the account was made or not. Its id is `<account>.<yyyymmdd>.<hhmmss>.<user number>`. Its
first lines are the image's path, the time, the account, the result and the counts; then one line for
everything that was left out, in the form `kind|file|id|reason`. At most 10,000 lines are kept; a last
line says how many more there were. The screen shows only the totals.

## Limits

An item over 16 MB, an image of more than 1 GB, more than 10,000 files, or a disk that would be left with
less than a tenth free are refused. `tape.import` has no way to read a **tape drive**, a named pipe or a
second reel: the image is one file.

## If it fails

A failure while the files are written removes the account again: its directory, its Linux user and home,
and its groups, and says so (*The new account NAME was removed again because filling it failed*). If the
removal itself fails, the message says which step did not complete, and what to check by hand.

## What it does not do

* It reads the layout the old `ACCOUNT.SAVE` wrote, and the others only as [described above](#the-layouts).
  Images from other systems' own save programs are not tested; they may be refused, and an image that is
  read is no proof that another system wrote it the way this reader understands it.
* It does not restore into an existing account, and it does not merge.
* It does not build indices, compile programs, or make a user's password: the person is given a password
  as for any new user account.

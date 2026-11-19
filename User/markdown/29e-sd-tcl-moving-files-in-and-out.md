Title: SD TCL - Moving Files In and Out
Subtitle: Bringing a text file into your account, and taking one out, with an sftp program over your usual login.

```
receive {overwrite}
send file id {id ...}
```

`receive` and `send` move plain-text files between your SD account and another computer: a CSV or JSON
file to load, the source of a program, a report to take away. You type the command in SD, it waits, and you
move the files with an **sftp program** on your own computer, signed in with **the same name and password
(or key) you use to reach SD over ssh**. Nothing can be moved before you type the command or after it ends.

**It is off until the administrator turns it on**, for the system and for your account. If it is not, the
command says which is missing:

```
:receive
File transfer is not turned on for this system (XFER is 0 in sd.conf)
:receive
Account fred may not move files over its ssh login (the administrator allows it with modify.account fred xfer-on)
```

Type it **in your own account**, the one named after your login, not in one you reached with `logto`.

## Bringing files in: `receive`

```
:receive
Ready to receive into xfer.in.  Connect an sftp client to 192.0.2.10 port 22 as fred and put the files.  Press Enter here when done.
```

Leave that session waiting and, on your own computer, connect and put the files. With OpenSSH's `sftp`:

```
$ sftp fred@192.0.2.10
sftp> put orders.csv
sftp> put prices.json
sftp> quit
```

Then press Enter in SD:

```
Transfer closed (closed here): 2 file(s), 18422 bytes
   orders.csv   sha256 3cba0fa370b447d084ff3a17bb9d5ccf25c945332f82af439e63a6ce03446b44
   prices.json   sha256 9f2c41d0a7e3b85c6f1d24e09b7a3c58d6e1f0a2b4c6d8e0f1a3b5c7d9e1f3a5
```

The SHA-256 of each file is printed so that you can compare it with the same sum taken on your own
computer (`sha256sum orders.csv`, or `Get-FileHash orders.csv` in PowerShell): equal sums mean the file
arrived exactly as it left. PowerShell prints the sum in capitals and SD in small letters; the case of the
letters does not matter.

**The files are records of the file `xfer.in`** in your account, which SD makes the first time you use
`receive`. Each file is one record, its name the record id, each line a field:

```
:list xfer.in
:ct xfer.in orders.csv
:copy from xfer.in to bp myprog.bas,myprog
```

A program reads one like any record (`OPEN 'xfer.in' TO f`, `READ rec FROM f, 'orders.csv'`). When you no
longer need a file there, delete it (`delete xfer.in orders.csv`).

**A file that is already there is not replaced.** The sftp program is told the transfer failed and the file
in `xfer.in` is left as it was. To replace files, open the transfer with:

```
:receive overwrite
```

**From the home screen.** Where a transfer can be opened, your home screen has a **Receive files** tile
among your own tools; it runs `receive` and, when the transfer ends, waits for Enter so that the list of
files and their SHA-256 can be read before the home screen comes back. It never replaces a file (type
`receive overwrite` for that). `send` is typed: it needs the file and the records.

## Taking files out: `send`

```
:send bp myprog.bas report.txt
Ready to send from xfer.out.  Connect an sftp client to 192.0.2.10 port 22 as fred and get the files.  Press Enter here when done.
```

`send` copies the records you name from the file you name into the file `xfer.out` of your account, each as
a text file with the record id as its name and a line for each field, and waits. On your own computer:

```
$ sftp fred@192.0.2.10
sftp> get myprog.bas
sftp> get report.txt
sftp> quit
```

Press Enter in SD when you have them. `send` says so for each record it could not copy and carries on with
the rest; if none could be copied it opens nothing. Records stay in `xfer.out` until you delete them, and
whatever is there can be fetched while a `send` is waiting, so clear out what you no longer want to offer
(`clear.file xfer.out`).

## What can be moved

* **Plain text only.** A file that holds a NUL byte, or one of the bytes 248 to 255, is refused: a picture,
  a spreadsheet in its own format, a compressed file. Accented letters and the other bytes from 128 to 247
  are moved as they are; SD does not change or interpret them. For `send`, a record that holds a value mark
  or subvalue mark is not plain text either: only the field mark, which becomes a new line.
* **A plain name.** One name with no directory, not starting with `.` or `~`, and with none of
  `* , = > < % / + : ; ? " \`. There are no sub-directories, and the sftp program sees nothing of your
  account except `xfer.in` (during `receive`) or `xfer.out` (during `send`).
* **Whole files.** A file is sent from its start to its end; a broken transfer cannot be resumed, and a
  file that did not arrive whole is not kept. Send it again.
* **Within the limits the administrator has set**: the size of one file (10 megabytes as delivered), the
  size of everything in one transfer (100 megabytes), and perhaps only certain kinds of file (by the
  ending of the name, such as `.csv`).
* **In one direction.** While `receive` waits nothing can be fetched, and while `send` waits nothing can be
  put. The sftp program cannot make a directory, and can rename or delete only a file it has just sent.

## When it ends

The transfer ends when you press Enter, and also by itself:

| It says | Because |
|---|---|
| `closed here` | you pressed Enter |
| `no connection came in time` | no sftp program connected (ten minutes, as delivered) |
| `nothing more came` | an sftp program connected and then nothing happened (two minutes, as delivered) |
| `the time limit for a transfer was reached` | the longest a transfer may stay open (sixty minutes, as delivered) |
| `this session's input ended` | the session was ended while it waited |

A file that was part way through at that moment is not kept. Type the command again to carry on.

**Each transfer is a connection of its own.** When it ends, the sftp program is disconnected; to `send`
after a `receive` (or to `receive` again), type the command and connect the sftp program again.

## With other sftp programs

**WinSCP.** Choose the SFTP protocol, the host, port 22 (or the one your administrator gave you), your name
and password. **Turn off transfer resume** (Preferences, Transfer, Endurance: *Enable transfer
resume/transfer to temporary filename for*: Disable): with it on, WinSCP sends a large file under a
temporary name ending `.filepart`, which is refused where only certain kinds of file are taken. SD sets a
file's permissions itself; what the sftp program asks for them is not applied.

**FileZilla.** In the Site Manager choose *SFTP - SSH File Transfer Protocol*, the host, the port, *Logon
Type: Normal* (or *Key file*), your name and password. The remote side shows one directory, `/`.

**Any of them** will show an error in words when SD refuses something, or only "Permission denied" or
"Failure"; the reason is always one of those on this page. If it says no transfer is open, type `receive`
or `send` in SD first, or again: the earlier one has ended.

## What the session shows meanwhile

The sftp connection is a process of its own; `listu` shows it with the address it came from and `sftp`
where a terminal would be. Ending your SD session ends the transfer and the connection with it.

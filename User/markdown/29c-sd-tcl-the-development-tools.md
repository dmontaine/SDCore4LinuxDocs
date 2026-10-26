Title: SD TCL - The Development Tools
Subtitle: Full-screen pages for the work in your own account: its files, and the verbs that make and change them.

```
tool.files
tool.voc
```

These pages are for **the account you are signed in to**. They work in every account (they are in
everybody's vocabulary), they need a real terminal of at least **140 columns by 43 lines**, and they add no
access: every change they make is a command you could have typed, run for you after a box that shows the
exact command. A gate that is off for your account is met as the command's own refusal; the page shows
the gates you hold, and never tries an operation to find out.

The home screen has a tile for each of them, in the group *Develop*.

## tool.files - the files of the account

```
tool.files
```

**`tool.files`** lists every file the account's VOC points at, one row each, in name order:

| column | what it says |
|---|---|
| Name | the file's name in the VOC |
| Kind | `dynamic` (records in groups, the usual data file), `directory` (each record is a file in a directory of the operating system), `sequential`, `server` (a file on another SD server) |
| Records | the file's own approximate count of records |
| Modulus | how many groups a dynamic file has now |
| Bytes | the size on disk of a dynamic file without its indices |
| Idx | how many alternate-key indices it has |
| Trigger | the name of its trigger, if it has one |
| Case | `any` when record ids ignore case (**as delivered**: jack and JACK are one record), `exact` when they do not |
| Dict | whether it has a dictionary |
| Open | `yes` when another session has the file open |

The box under the list describes **the file under the cursor**: where it is on disk, how many records it
holds, its modulus and group size and how full the groups are, the size of the primary and overflow parts,
whether ids ignore case, whether it can be written, its indices and its trigger, and who else has it
open. The line between the boxes shows the **gates your session holds** (`voc-edit`, `dict-edit`,
`bp-edit`), asked of the system.

### What the keys do

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **N** | make a file: asks for a name, then *dynamic* or *directory*, then shows `create.file name` in a box |
| **C** | clear the file under the cursor (`clear.file name`) |
| **D** | delete it (`delete.file name no.query`) |
| **A** | run `analyse.file` on it: the terminal is handed to the verb, which prints its report; Enter brings the page back |
| **I** | run `list.index` on it (its indices, in full), the same way |
| **T** | run `list.triggers` on it, the same way |
| **/** or F11 | show only the names that hold some text (empty shows them all) |
| Esc | clear the filter |
| F5 | read the files again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**Every change goes through a box.** The box shows the exact command, says what it does, and has two
buttons, *Run* and *Cancel*; **Cancel is the one Enter chooses**, so a stray Enter runs nothing. *Clear* and
*Delete* then ask for **the file's name, typed**; a wrong name does nothing. The command is the ordinary
verb, so its own checks are the checks: a file open in another session cannot be cleared or deleted, and
what the verb says is what the status line shows.

**A name the page does not give to a command.** The page hands a command only names of letters a-z,
digits, dot, dash and underscore. A file whose name has anything else (a capital, an `&`, a `$`) is listed and
described, and the page says which verb to type at the prompt for it instead.

**Gates.** Making a new file, and clearing or deleting an ordinary data file, are not held back by the
edit gates: the new VOC pointer is a side effect of an ordinary command. The gates matter for the
protected kinds: clearing or deleting a **program file** (such as `bp`) needs `bp-edit`, and a
**dictionary** on its own needs `dict-edit`. The page shows which of the three gates your session holds
(`voc-edit`, `dict-edit`, `bp-edit`); if one is off, the verb's own refusal is what you get, shown on the
status line, and the file is left as it was. The administrator turns a gate on for an account with
`modify.account` (see *Accounts and Security*). Files of the **shared account** are not in your VOC as
files and are never changed from here.

## tool.voc - the vocabulary of the account

```
tool.voc
```

**`tool.voc`** lists every entry of the account's VOC, the file that tells SD what each word on a command line
means, one row each, in name order:

| column | what it says |
|---|---|
| Name | the entry's id |
| Type | `V` verb, `K` keyword, `F` file, `Q` pointer to a file in another account, `R` pointer to a record, `PA` paragraph, `S` stored sentence, `X` text |
| Points at | what it leads to, in a few words: the program a verb runs, the path of a file, the account and file of a Q-pointer |
| Works | for a file or a Q-pointer, whether the file it names can be opened (`yes`, `NO`); the page opens it to see |
| Against the shipped VOC | `same` as NEWVOC, the vocabulary every account was copied from; `changed` from it; or `added` in this account |

The box under the list shows **the entry under the cursor**, field by field. The line between the boxes shows
the **gates your session holds**, as `tool.files` does.

| key | does |
|---|---|
| Up, Down, PgUp, PgDn, Home, End | move the cursor |
| **E** | edit the entry in SED (`sed voc name`): the terminal is handed to SED, and Enter brings the page back at the same entry |
| **D** | delete the entry (`delete voc name`) after a box that shows the command, with the id typed |
| **T** | choose the type shown: all, verbs, files, pointers, paragraphs and sentences, other |
| **S** | choose the state shown: all, only the entries that differ from the shipped VOC, only broken pointers |
| **/** or F11 | show only the ids that hold some text |
| Esc | clear the filter |
| F5 | read the VOC again |
| F1, **?**, a click on **[?]** | help |
| Ctrl-Q | leave |

**The page writes nothing itself.** A record is changed by SED, which the page starts, or by `delete`, which
it runs; both are ordinary commands with their ordinary checks. Writing the VOC by hand needs the
**`voc-edit`** gate: without it SED's save and the delete are refused by the kernel and the entry is left as
it was. A VOC pointer made by an ordinary command such as `create.file` is not held back by the gate.

**An id the page does not give to a command.** As in `tool.files`, only ids of letters a-z, digits, dot,
dash and underscore are put into a command. A VOC id may have much else (a capital, `$`, `%`, `&`); such an
entry is listed and shown, and the page says which command to type for it instead.

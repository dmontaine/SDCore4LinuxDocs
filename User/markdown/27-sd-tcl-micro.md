Title: SD TCL - The micro Screen Editor
Subtitle: The capable one — SD BASIC highlighting, a command bar, split windows and a help screen.

```
micro {dict} file record
```

`micro` opens a record in **micro**, a full-screen editor, and is the one
external editor SD hands records to. (`edit` is a second name for the line editor
[ed](25-sd-tcl-ed.html); the NANO verb was added and removed again in 1.2-0.)
Two things make it the one to use for programming:

| | |
|---|---|
| **it highlights SD BASIC** | statements, reserved words, intrinsics, strings and comments, from rules SD generates out of the compiler's own tables and ships |
| **it has a command bar and a help screen** | so everything it can do is reachable and readable without leaving the editor |

It also has multiple files open at once, split windows, a plugin system and
rebindable keys. **If you only want to change one line in a record**, `ed`
works anywhere, with no screen to learn.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part.

> **The keys below are micro's own**, read from the default bindings and the
> help text inside the version SD installs — **micro 2.0.15**. SD installs
> micro and calls it; it does not implement it, so where a binding differs
> the editor is right.

## micro is installed with SD

**You do not install anything.** `micro` is installed by SD's installer as
an ordinary package.

If that could not happen — an offline machine, or one whose policy blocks
the package manager — the verb says so, rather than opening nothing and
reporting the record unchanged.

## The keys

`Ctrl-S` saves, `Ctrl-Q` quits, and **`Ctrl-G` opens the help screen**, which is
the answer to everything not on this page.

| | |
|---|---|
| **`Ctrl-S`** | save |
| **`Ctrl-Q`** | close the file — and quit, if it is the last one open |
| **`Ctrl-G`** | open and close **help** |
| **`Ctrl-E`** | the **command bar** — see below |
| **`Alt-G`** | show and hide the key hints |
| **`Ctrl-Z`** · **`Ctrl-Y`** | undo · redo |
| **`Ctrl-X`** · **`Ctrl-C`** · **`Ctrl-V`** | cut · copy · paste |
| **`Ctrl-K`** · **`Ctrl-D`** | cut the current line · duplicate it |
| **`Ctrl-A`** | select all |
| **`Ctrl-F`** | find |
| **`Ctrl-N`** · **`Ctrl-P`** | find next · find previous |
| **`Ctrl-O`** | open a file |
| **`Ctrl-T`** | open a new tab |
| **`Alt-A`** · **`Alt-E`** | start · end of line |
| **`Alt-B`** · **`Alt-F`** | previous · next word |

Function keys work too, for anyone who prefers them: **`F1`** help, **`F2`**
save, **`F3`** or **`F7`** find, **`F4`** or **`F10`** quit.

> **`Ctrl-Q` closes the file rather than the editor.** With one record open —
> which is how SD starts it — that is the same thing. With a second file opened
> by hand it is not, and micro stays up until the last one is closed.

## The command bar

**`Ctrl-E`** opens a `>` prompt at the foot of the screen. It takes micro's own
commands, and the two worth knowing on the first day are:

| | |
|---|---|
| `> help` | the same screen as `Ctrl-G` |
| `> help keybindings` | every key, including the ones not listed above |
| `> set` *option* *value* | change a setting for this session |

## Where micro keeps its configuration, and why saving works here

**Unlike SD Core for Windows, this port has no release blocker around
saving.** micro looks for its configuration in the calling user's own
`~/.config/micro` — a directory that account already owns, since it is
simply their own home. There is nothing under a shared, root-owned
install path for an ordinary account to fail to write to. The syntax
rules SD ships are copied into that directory on first use (`gpl.bp/edit`
does the copy itself, with no privilege needed), and stay there for every
later edit.

## Highlighting SD BASIC

**SD SHIPS THE RULES AND POINTS micro AT THEM.** They are generated from the
BASIC compiler's own tables rather than typed by hand, so the list of
statements, reserved words and intrinsics is the one the compiler actually
accepts.

**It works on a record from a `bp` file and not on other records**, and the
reason is worth knowing: micro decides which language a file is by matching its
*name*, and a record called `MY.REPORT` tells it nothing. So SD names the
working copy `*record*.editing.sdbasic`, and that suffix is what micro
recognises. A record edited out of any other file is plain text.

## What SD does around the editor

| | |
|---|---|
| **the working copy** | the record is copied into `$hold` as *record*`.editing`, and micro is run on that. It is removed on every exit, including the ones that fail |
| **saving** | *"Save? &lt;Y&gt;es, &lt;N&gt;o"*, then for a `bp` record *"Compile?"* and *"Catalog?"* |
| **a `dict` record** | is always saved and re-compiled with `compile.dict` |
| **finishing** | *"&lt;E&gt;xit or &lt;R&gt;e-edit"*, so a compile error can be fixed without starting again |

**A compiled dictionary record is truncated to its first 15 fields while you
edit it**, which is what you want: the fields after them are the compiled form,
and `compile.dict` rebuilds them when you save.

`micro` needs a real terminal and refuses a session driven down a pipe:

```
:micro bp zzed
micro needs a terminal to draw on, and this session has none.
ed, the line editor, works anywhere.
```

Both usage errors name the verb you typed:

```
:micro
No file name specified.  Usage: micro {dict} <file> <record>
:micro bp
No record name specified.  Usage: micro {dict} <file> <record>
```

## Marks, and how to type one

A **field** mark is a line break, so micro handles fields on its own. The other
three have a token you type instead. **Every token is `~` and one more
character, and `~` is the only escape character.**

| | |
|---|---|
| `~~` | a value mark |
| `` ~` `` | a subvalue mark |
| `~!` | a text mark |
| `~-` | a literal `~`, where one would otherwise be misread |
| `~,` | a literal `,`, where one would otherwise read as a separator |

**Marks in a row are separated by a comma** — a text mark, a text mark and a
value mark is `~!,~!,~~`. Written token against token a run of marks cannot be
read, so SD puts a comma between them. **Type the comma yourself when you enter
marks in a row.** It is a separator and not data — which is why a literal comma
standing in exactly that position, between two marks, is written `~,`.

**The conversion is lossless: no record is refused and none is mangled**,
whatever it contains. A tilde is written `~-` **only where the character after
it would make the pair look like a token** — another `~`, a backtick, a `!`, a
`-`, a `,`, or a mark. Everywhere else a tilde is left exactly as you wrote it,
so `a~b` is still `a~b` and ordinary source reads normally.

## The gate — `os-on`, off for a new account

**`micro` needs the account's `os-on` switch**, the same one as `OS.EXECUTE`
(and not `sh-on`: an account can be refused the shell and still run the editor,
or the reverse). SDSYS turns it on with `modify.account` *name* `os-on`; a new
account does not have it, and an account without it is told so when it types
the verb. With it the editor runs at once, and what it can read or write outside
SD is exactly what the account's Linux user may touch, because they are the
same permissions. See the *Administrator* set's *Accounts and Security* chapter,
"The operating-system switches: `sh-on` and `os-on`".

## Who has these verbs

**Every account has `micro`, `edit` and `ed` in its VOC, and `ed` and `edit`
always run.** `micro` needs the account's `os-on` switch, as above.

## See also

[SD TCL - The ed Line Editor](25-sd-tcl-ed.html) ·
[SD TCL - Programs and the Catalogue](24-sd-tcl-programs-and-the-catalogue.html).

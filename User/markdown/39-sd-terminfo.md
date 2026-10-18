Title: SD Terminal Information (Terminfo)
Subtitle: The terminfo database, the definitions that ship, and the compiler that ships with them.

SD uses a terminfo database to know what byte sequences a terminal sends for
each key, and what sequences to emit for screen control — cursor movement,
clear, colour, bold, underline.

Most installations never touch it. The shipped definitions cover the
terminals in ordinary use, and `linux` works with any standard Linux
console or terminal emulator.

## The default terminal

```
term
```

```
Page width: 120
Page depth: 36
Device    : linux
```

The default terminal type is `linux`.

> Existing accounts keep their old setting until their VOC is updated.
> Until then, `term linux` sets it for the session.

## What ships

**About 50 terminfo definitions ship with SD**, compiling to **82 terminal
names** — the extra names are variants. For example, `vt100-w` is an alias
that maps to the same definition as its base name.

Common names that work out of the box: `linux`, `vt100`, `vt220`,
`wyse60`, `ansi`, `xterm`.

The `-at` terminal types (`vt100-at`, `vt220-at`, `wy60-at` and the rest)
were AccuTerm's, and `sdterm` was SDTerm's. They are gone: SD no longer
supports either terminal program. A session that was set to one of them
should use `xterm`, `vt100` or `vt220`.

A name that is not installed is refused and your current type is kept:

```
:term vt320
Unrecognised terminal name
```

There is no `vt320` definition; `vt220` or `xterm` does the same job.

## Setting the terminal

```
term                    * report current type and page size
term linux              * set for this session
term 140,42             * set page size
term default            * restore 140 x 42 (prints nothing; check with bare term)
```

The page size is worked out at login in this order:

1. the `LINES` and `COLUMNS` environment variables if they are numeric
2. the terminfo entry's `lines` and `cols`
3. otherwise 42 and 140

A console or ssh session normally gets its real window size. 140 × 42
is the fallback when nothing answers — a phantom or a piped script.
The terminfo entries that name a width and a depth say 140 and 42; the
132-column entries keep their own depth.

## The page is 140 × 42

SD's default is **140 columns by 42 lines**, not 80 × 24 — and no longer
the 120 × 36 of the releases before 18 October 2026. A console window
narrower than that makes wide reports look wrapped or truncated — which
reads as a formatting bug and is not one. `term 120,36` gives the old
size back for a session that wants it.

The default is only a default. `term w,h` takes any width from 20 to
32767 and any depth from 10 to 32767, larger or smaller than 140 × 42,
and nothing else clamps it. A real terminal still decides its own size,
and `term default` puts the page back to 140 × 42 whatever the window.

## The terminfo source

`terminfo.src` ships with SD. It is a text file containing all the
definitions in source form. You can read it to see what a terminal
definition looks like, and you can use it as a template for a custom
definition.

## Ending one attribute: `eblink`, `edim`, `erev`, `ebold` and `eprot`

SD turned blink, half intensity, reverse video and bold off with `sgr0`, which ends **every**
attribute and the colours as well. A terminal entry can now give each its own capability:

| capability | ends | sent by |
|---|---|---|
| `eblink` | flashing text | `@(-6)` |
| `edim` | half intensity | `@(-12)` |
| `erev` | reverse video | `@(-14)` |
| `ebold` | bold | `@(-59)` |
| `eprot` | protected mode | nothing yet: no `@()` function uses it |

When the entry defines the capability, the function sends it; **when it does not, the function
sends `sgr0` as before.** No entry that ships with SD defines any of the five, so nothing changes
until you add them. SD's own programs that use `@(-14)` to put the colours back (the query
processor's styles, SED, the pick lists) therefore behave as they did on every stock terminal.
Think before you give an entry an `erev` of its own: it ends reverse video and nothing else, where
`sgr0` ended the colours too.

Put the additions in `terminfo.mods` in the SDSYS account directory, which the installer compiles
after `terminfo.src` so that an upgrade does not lose them, and compile with `sdtic` as described
below. The start functions `@(-5)` and `@(-13)` were not changed. Tested with a copy of the `ansi`
entry that has all five, a copy that has none and a copy with only `erev`.

## Compiling a definition

**`sdtic` is built alongside the server during installation** — it is
what compiles `terminfo.src` at install time — **but, unlike SD Core for
Windows, is not currently left on the machine afterward.** The installer
deletes its whole temporary build tree once installation finishes, and
`sdtic` was only ever in that tree. To compile a custom definition after
the fact, build it yourself from a clone of the source
(`make sd` in `sdb_ai/sd64` produces `bin/sdtic`) rather than expect a
copy already on the machine.

```
sdtic {options} src...
```

| | |
|---|---|
| `-d` | decompile a named terminal entry instead of compiling |
| `-i` | display an index of terminal names |
| `-p`*path* | use the terminfo library at *path* |
| `-t`*name* | compile only *name*; may be repeated |
| `-v` | verbose |
| `-x` | do not overwrite entries that already exist |

Without `-d` it compiles the source files you name. With `-d`, the argument is a
terminal name to decompile rather than a file.

Two things follow from `-d` that are worth knowing. It is how you read a shipped
definition without hunting through `terminfo.src`, and it is how you produce a
starting point for a variant of one:

```
sdtic -d vt220 > myterm.src
```

Edit that, then compile it back in. `-x` is the safe form while you are
experimenting, because it refuses to overwrite a definition that already
exists.

The compiled definitions live under `/usr/local/sdsys/terminfo`, in
single-letter directories by first letter. Writing there needs SDSYS's own
permissions, so run `sdtic` as `sdsys` when you are adding a definition
for the machine.

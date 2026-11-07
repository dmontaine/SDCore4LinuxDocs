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

SD takes the type from your terminal's `TERM` when you sign on. `xterm`,
`xterm-256color`, the VTE and Konsole terminals, `tmux`, `screen`, `alacritty`,
`kitty`, `foot`, `rxvt` and `st` are signed on as `xterm`; the Linux console is
`linux`; a name SD has no entry for falls back to `linux`. You can still type
`term xterm` or `term linux`: the keys work either way.

> Before this release every account's `login` paragraph said `term linux`, so a
> graphical terminal was signed on as `linux` and its F1 to F5 and Home keys did
> not work. Existing accounts lose that line the next time their VOC is updated;
> until then `term xterm` sets it for the session.

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
term 140,43             * set page size
term default            * restore 140 x 43 (prints nothing; check with bare term)
```

The page size is worked out at login in this order:

1. the `LINES` and `COLUMNS` environment variables if they are numeric
2. the terminfo entry's `lines` and `cols`
3. otherwise 43 and 140

A console or ssh session normally gets its real window size. 140 × 43
is the fallback when nothing answers — a phantom or a piped script.
The terminfo entries that name a width and a depth say 140 and 43; the
132-column entries keep their own depth.

## The page is 140 × 43

SD's default is **140 columns by 43 lines**, not 80 × 24 — and no longer
the 120 × 36 of the releases before 18 October 2026 (it was 140 × 42 until
2 November 2026). A console window
narrower than that makes wide reports look wrapped or truncated — which
reads as a formatting bug and is not one. `term 120,36` gives the old
size back for a session that wants it.

The default is only a default. `term w,h` takes any width from 20 to
32767 and any depth from 10 to 32767, larger or smaller than 140 × 43,
and nothing else clamps it. A real terminal still decides its own size,
and `term default` puts the page back to 140 × 43 whatever the window.

## The Linux text console, with no desktop

The full-screen tools - the home screen, the IDE, the administrator and
development pages, the debugger - work on the text console of a server that
has no desktop (the screen at tty1 to tty6), over ssh from any terminal, and in
a terminal emulator alike. On the console SD signs on with the type `linux`.
What the console needs, and what it cannot do, is below. It was tried on a
real Debian 13 console.

**It needs a window of 140 columns by 43 rows.** A text console is as big as
the screen's resolution divided by the size of one character of its font, so a
small screen is a small console:

| the console | its size | |
|---|---|---|
| 1280 × 800, an 8 × 16 font | 160 × 50 | works |
| 1920 × 1080, an 8 × 16 font | 240 × 67 | works |
| 1024 × 768, an 8 × 16 font | 128 × 48 | too narrow |
| a text screen without a framebuffer | 80 × 25 | too small |

On a console that is too small SD says so and does not start the page: *home
needs a window of at least 140 columns by 43 lines; this one is 80 by 25*. An
account that starts in the home screen is then signed out.
`stty size` shows the size. A narrower font gives the room back: `sudo setfont
Lat15-Terminus12x6` (a font 6 pixels wide and 12 high) makes a 1280 × 800
console 213 × 66 and a 1024 × 768 one 170 × 64, and SD's pages use the
whole of it. `setfont` changes the console it is run on, until the next boot.
To keep it, on Debian and Ubuntu run `sudo dpkg-reconfigure console-setup` and
choose the Terminus font in 6x12. A higher video mode (the kernel's `video=` parameter, or
the boot loader's graphics mode) does the same from the other side.

**The keys.** Everything a console can send works, and SD names it as it does
anywhere else: the letters, Ctrl with a letter, Alt with a letter (the console
sends Esc and the letter), the arrow keys, Home, End, Insert, Delete, Page Up,
Page Down and F1 to F12, **Shift-F1 to Shift-F8** (which the console sends as
F13 to F20) and **Shift-Tab** (which it sends as Esc and Tab). What the Linux
console does not send at all:

- Ctrl, Shift or Alt together with an arrow, Home, End, Insert, Delete, Page Up
  or Page Down arrive as the plain key; there is no Ctrl-Left, Ctrl-Home or
  Ctrl-Page Down on a console. Shift-F9 to Shift-F12 and Ctrl-F1 to Ctrl-F12
  send nothing.
- Alt-F1 to Alt-F12 and Alt-Left and Alt-Right switch to another console, and
  Shift-Page Up and Shift-Page Down scroll the console's own history; the
  kernel keeps them.

So on a console the IDE's *Next tab*, *Previous tab* and *Previous pane* are
chosen from the *Go* menu (F10), and F6 goes through the panes, and the
editor's word and start-of-text moves have no key: use the arrows, Home and End,
and *Go to line* (Ctrl-L). Every other key of the pages and the IDE is a key the
console sends. `tool.keys` shows what SD was given for each key you press.

**The mouse.** A console does not report the mouse the way a terminal emulator
does, but the *gpm* daemon reads it there. The installer installs the package
`gpm` with SD's other packages (since 3 November 2026), and the Debian and
Ubuntu package enables and starts the daemon itself, which takes the mouse from
`/dev/input/mice`; the installer does not start or enable it, so an
administrator who turned the service off finds it off after an upgrade. While
gpm is running, a full-screen program that asks for the mouse is
connected to it and is given the same press, release, drag and wheel reports
as an emulator would give, so every page that takes the mouse takes it on the
console, and gpm draws the pointer. Nothing is needed in SD, and with the
daemon stopped there is simply no mouse. If `gpm` cannot be installed (in a
container, for example), the installer prints a warning and goes on; install it
later with `sudo apt-get install gpm`. Removing SD leaves the `gpm` package
installed. SD asks gpm only when the terminal type is
`linux` and its input is a text console, so a session over ssh, in `tmux` or
`screen`, or in an emulator is not affected, and a program that opens its
screen with `nomouse` is not connected. SED reads its own mouse reports
and has no mouse on the console.

**Colour and borders.** The console has eight colours and bold, and the
themes (`blue`, `classic`, `mono`) work on it. On a console set to UTF-8, which
is what Debian gives, the pages draw their borders with line-drawing characters.

**The debugger.** The console has no alternate screen, so the full-screen debugger
takes the one screen: it clears it when it comes up and clears it again when it lets
the program go. A program that owns the screen library's screen has it drawn again from
what the library knows; text the program printed with `PRINT` or `CRT`, and what was on the
screen before the debugger started, is gone. `LINE.MODE` in the VOC record `$debug.options`
keeps the line-by-line debugger, which clears nothing. See *SD BASIC debugging*.

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

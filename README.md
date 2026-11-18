# SD Core for Linux - documentation

The documentation of **SD Core for Linux**, written in Markdown. The server
source is in the separate `SDCore4Linux` repository; nothing here is needed to
build SD, and nothing there is needed to build these pages.

## What is here

Five sets of documents, each in a `markdown/` folder (the source); the `html/`
and `pdf/` folders beside it are generated.

| Set | For | Contents |
|---|---|---|
| `GettingStarted/` | everyone | installing SD Core on Linux, running it, accounts and security, what differs from OpenQM and from SD Core for Windows, and moving programs over from other MultiValue databases |
| `User/` | programmers and users | SD BASIC by subject, SD TCL by subject, the VOC and dictionaries, files, standard subroutines, the client API, the terminal screen library, a tutorial with worked programs, the glossary and the generated syntax cards (`94` SD BASIC, `95` SD TCL) |
| `Administrator/` | the administrator | accounts and access gates, sessions and locks, operating system access, encryption, remote access, system limits, configuration, installation and the service, the installed scripts, restricted commands, known limits, SDNet, the shared account, the master files, the `sdfix`, `sdidx` and `sdconv` tools, moving an account to another machine, giving an AI agent an account of its own, the AI helper, the audit trail, remote administration over ssh, and scheduled jobs. Everything in it is administrator-only or unavailable to an application, so an administrator can withhold the whole set |
| `TUIGuide/` | programmers, from the administrator's documents | *SD Text User Interface - Programmer's Guide*: building a full-screen page of your own in SD BASIC with the public `!tk` routines and `tkpub.h` - the shape of a program, the window and its floor, the key table and menus, the finder, the confirm box, the form, the pick lists, the output pane, and how a page uses the `screen` statement with the routines - with five worked example programs and a reference of every routine. A document of its own, with its own page numbers and its own book |
| `Changes/` | everyone upgrading | what was added, changed and removed in this version, by area |

The sets do not link to each other, because each is handed out on its own. Where
a page in another set is worth naming, it is named in words.

### Page numbers

A number with a letter after it is the second half of a long page (`04` and
`04a`); pages are kept to about 14,000 characters so a reader moves between
pages rather than scrolling through one. `00a` is the copyright and license
page, which comes first in every set; `00b` is the introduction. The syntax
cards sit at the end (`94` and `95`) so they can grow without renumbering
anything.

The copyright and license block appears in full once per set, on `00a`; every
other page carries a one-line footer with the product, version, copyright and
license name.

## Reading the pages

`start-docs.sh` serves the pages on `http://localhost:8123/` and opens
`index.html` in a browser:

```sh
sh start-docs.sh
```

## Building the HTML

```sh
pip install markdown
python3 tools/mkdoc.py --in GettingStarted/markdown --out GettingStarted/html
```

Every step is a plain Python script; the only dependency is **python-markdown**
(`python3-markdown` in a distribution's packages). Run `mkdoc.py` once for each
set, with that set's `markdown` and `html` folders.

`tools/mkdoc.py` renders each Markdown page to one self-contained HTML file (the
style is embedded, so a page can be copied anywhere). `tools/add_nav.py` adds the
previous/next links and checks that each set has its license page first, and
`tools/mkbook.py` joins a set into one book (`tools/mkbookpdf.py` and
`tools/mkpdf.sh` make a PDF). The generated pages are not tracked; the Markdown
is the source.

The syntax cards are generated from SD itself and are not edited by hand:

```sh
SD64=/path/to/SDCore4Linux/sdb_ai/sd64
python3 tools/mksyntax.py $SD64/sdsys/gpl.bp/bcomp User/markdown/94-sd-basic-syntax.md Administrator/markdown/10-sd-basic-restricted-commands.md
python3 tools/mktclsyntax.py $SD64/sdsys User/markdown/95-sd-tcl-syntax.md
python3 tools/linkup.py User/markdown
```

`mksyntax.py` and `mktclsyntax.py` refuse to write a card if a name the compiler
accepts, or a verb the VOC holds, has no line in `tools/syntax-shapes.txt` or
`tools/tcl-syntax-shapes.txt`, one `NAME = syntax` per line. `linkup.py` turns
the page names the two cards write in italics into links.

`tools/checklinks.py`, `tools/docmap.py`, `tools/tclmap.py`, `tools/confmap.py`
and `tools/verbcounts.py` check the links and that every SD BASIC name, TCL verb
and `sd.conf` parameter is documented.

The PowerShell programs in `tools/` (`mkpdf.ps1`, `mkbookpdf.ps1`, `release.ps1`,
`sdtcl.ps1`, `sdprobe.ps1`, `sdprobe2.ps1`, `sdcompile.ps1`, `sddebug.ps1`) and
`tools/scriptmap.py`, which checks the installed PowerShell scripts against their
page, are the Windows documentation's tools. They are kept here so that the
`tools` folder is the same in every SD documentation repository; nothing on Linux
runs them.

## License

See `GettingStarted/markdown/00a-copyright-and-licence.md`.

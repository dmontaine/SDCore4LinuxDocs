# SD Core for Linux - documentation

The documentation of **SD Core for Linux**, written in Markdown. The server
source is in the separate `SDCore4Linux` repository; nothing here is needed to
build SD, and nothing there is needed to build these pages.

## What is here

Four sets of documents, each in a `markdown/` folder (the source); the `html/`
and `pdf/` folders beside it are generated.

| Set | For | Contents |
|---|---|---|
| `GettingStarted/` | everyone | installing SD Core on Linux, running it, accounts and security, what differs from OpenQM, and moving programs over from other MultiValue databases |
| `User/` | programmers and users | SD BASIC by subject, SD TCL by subject, the VOC and dictionaries, files, standard subroutines, the client API, the terminal screen library, a tutorial with worked programs, the glossary and the generated syntax cards (`94` SD BASIC, `95` SD TCL) |
| `Administrator/` | the administrator | accounts and access gates, sessions and locks, operating system access, encryption, remote access, system limits, configuration, installation and the service, the installed scripts, restricted commands, known limits, SDNet, the shared account, the master files, the `sdfix`, `sdidx` and `sdconv` tools, moving an account to another machine, and giving an AI agent an account of its own. Everything in it is administrator-only or unavailable to an application, so an administrator can withhold the whole set |
| `Changes/` | everyone upgrading | what was added, changed and removed in this version, by area |

The sets do not link to each other, because each is handed out on its own. Where
a page in another set is worth naming, it is named in words.

### Page numbers

A number with a letter after it is the second half of a long page (`04` and
`04a`); pages are kept to about 14,000 characters so a reader moves between
pages rather than scrolling through one. `00a` is the copyright and licence
page, which comes first in every set; `00b` is the introduction. The syntax
cards sit at the end (`94` and `95`) so they can grow without renumbering
anything.

The copyright and licence block appears in full once per set, on `00a`; every
other page carries a one-line footer with the product, version, copyright and
licence name.

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

`tools/mkdoc.py` renders each Markdown page to one self-contained HTML file (the
style is embedded, so a page can be copied anywhere). `tools/add_nav.py` adds the
previous/next links and checks that each set has its licence page first, and
`tools/mkbook.py` joins a set into one book. The generated pages are not
tracked; the Markdown is the source.

The syntax cards are generated from SD itself and are not edited by hand:

```sh
python3 tools/mksyntax.py <sdsys>/gpl.bp/bcomp User/markdown/94-sd-basic-syntax.md Administrator/markdown/10-sd-basic-restricted-commands.md
python3 tools/mktclsyntax.py <sdsys> User/markdown/95-sd-tcl-syntax.md
```

`tools/checklinks.py`, `tools/docmap.py` and `tools/tclmap.py` check the links
and that every SD BASIC name and TCL verb is documented.

## Licence

See `GettingStarted/markdown/00a-copyright-and-licence.md`.

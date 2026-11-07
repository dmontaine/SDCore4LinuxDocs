Title: The AI Helper
Subtitle: One provider and one model for every account, a key that SD never sees, and a gate for each account.

SD can ask an AI model a question for an account holder (the `ai` verb, see [SD TCL - Asking the AI](29b-sd-tcl-asking-the-ai.html)). This page is for the administrator: it says what is set up, what leaves the machine, how to choose the provider and give it a model and a key, and how to allow or stop an account.

> **Nothing is on as delivered.** There is no provider, no key, and no account has the gate (each named provider comes with a default model, so the model is the one thing you need not supply). Until you have done the other three, the `ai` verb says so in words and nothing is sent anywhere. Turning one of them on is your act, and each is one command (or one key on the AI choice page) that can be undone.

## What leaves the machine

When a person types `ai some text`, SD shows them the text, the provider and the model, and asks whether to send it. Only if they answer `y` or `yes` does anything go out. What goes out is your standing text (below), that text, one fixed sentence that asks for a short plain answer, and a limit on the length of the answer. It is sent over **https**, with the certificate checked, to the address of the provider you chose, and to nowhere else. The key goes only to that address.

SD adds nothing of the account, the session or the data. A person can of course type or paste whatever they like into the question, which is why the preview is not optional and why the gate is yours to give.

**The standing text.** Every request, from the `ai` verb and from every AI line, begins with a few lines of yours: what SD is, how its commands are written, which gates there are, and where SD's help is. SD ships a default; you can replace it (see [The standing text](#the-standing-text) below). It is yours and is invisible to the person asking: it is not in their preview and it does not change their question. The preview's size counts it.

**Passages of the documentation.** The AI line (the home screen, the pages of the toolkit, the IDE, SED, the collection editor and the debugger; not the `ai` verb) also adds up to four sections of SD's own documentation that match the request, at most 2,400 bytes each and 6,000 in all, and the preview lists them (page, section, size, first lines) before anything is sent. The installer puts the markdown of the User and Administrator documents in `docs/user` and `docs/admin` under the system directory, from the documentation repository at the branch it installs. `docs/user` is readable by every session (755, files 644). **`docs/admin` is yours alone: mode 700 and files 600, owner `sdsys`, which is the only operating-system user an administrator session runs as, and the routine asks SD for the administrator before it looks there.** An account holder's request is never answered from those pages. The directory is replaced whole at each install and is not a place to put your own text. If the installer could not reach the documentation it prints a note, installs nothing and the AI line works without passages. This is documentation, not source: the rule below that the AI is never given SD's own code is unchanged.

## What the AI is never given, and what is not taken to it

**The AI in SD helps a person use SD and write their own programs, dictionaries and files. It is never given SD's own code or any other system information, whichever provider you chose, and not even the administrator can take a question about changing SD to it from inside SD.** The source is open, so someone who wants help changing SD can ask an AI outside SD; inside SD that help is not offered. Two things enforce this, and they are not equally strong.

1. **Where the text comes from (enforced).** Every program that puts the text of a record or file into a request (the IDE, SED, the collection editor and the debugger) tells the AI routine where the text comes from. Before anything is shown or sent, the routine refuses text that is part of SD itself, and text whose origin it cannot tell. SD's own files are everything in the system directory (the programs, headers, messages, help text, dictionaries and files of the system account, the account register, the audit trail and the error log), the AI helper's directories, `/run/sd`, `/etc/sd.conf`, and any directory called `gplsrc`, `gplbld` or `gplobj`. It is decided by where a file is, with links and `..` followed, never by what the text says. The headers in `syscom` live in the system directory, so they are not sent either; a person's own programs are, `$include` lines and all. If you want the AI to see one of those headers for a person's program, copy it into that person's account: a copy there is the account's own file, and nothing is opened up.
2. **What is typed (a screen).** A request that names the system's code or build is refused in words before it is shown, and nothing is sent: `gpl.bp`, `gplsrc`, `gplbld`, `$internal`, a kernel file such as `op_sort.c`, a kernel key such as `k$audit`, the compiler's own programs, the makefile, SD's source or kernel code. **This is a screen, not a wall.** A question that names none of those is not caught, and a question that does reach an AI may be answered from whatever that AI learned of the open source. SD's gate is here, in SD.

Nothing the AI returns is run, and the output of a command is never given back to it. A refusal writes one line to the audit trail (`ai refused why=request ...` or `ai refused why=origin ...`) and never the text. What a person types or pastes themselves is theirs, and is in the preview.

## The pieces

| Piece | What it is |
|---|---|
| `sd-ai` (in `/usr/local/lib/sd-ai/`) | The helper. A small Python program, started by systemd for each request, as the operating system user `sdai`. It is the only part of SD that connects outward and the only part that can read a key. Root owns it; no SD account can replace it. |
| `/run/sd-ai/sock` | The socket the helper listens on (`sd-ai.socket`; group `sdusers`, mode 0660). Whoever connects is identified by the operating system, not by anything they write. |
| `/var/lib/sd-ai/` | The helper's own directory: the settings (`ai.conf`), one key file per provider (mode 0600, readable by `sdai` only) and the counters of the limits. |
| `/usr/local/lib/sd-ai/ai-providers` | The connection details that come with SD for Anthropic, OpenAI, Google and DeepSeek, and each one's default model. Root owns it. |
| `/usr/local/lib/sd-ai/ai-context` | The standing text that comes with SD. Root owns it; an install replaces it. Your own text, when you have saved one, is `/var/lib/sd-ai/context` and is kept by an upgrade. |
| `sd-ai-ctl` | The administrator's client for the helper. It is what asks for a key at the terminal, without echo. |
| `sdaiusers` | The Linux group that is the **gate**. Membership of it is what lets an account use the AI. |

The helper asks the operating system who is calling (the user id of the connection), so the gate does not depend on SD's own programs being honest: a program that talks to the socket directly gets the same answer.

## The things that turn it on

1. **A provider.** One for the whole machine: Anthropic, OpenAI, Google, DeepSeek or Custom.
2. **A model** for that provider. Each of the four named providers comes with a default model, shown on the page and used until you name another (`set.ai model PROVIDER NAME`; a dash goes back to the default). The defaults are the balanced model of each provider as its own documentation named it on 1 November 2026, and none has been tried against a real key: **model names change, so check the one you will pay for.** Custom has no default; its model is yours.
3. **A key** for that provider, from the provider's own account. It is typed at a prompt that shows nothing, and kept for the helper only.
4. **The gate for each account that may use it**: `modify.account NAME ai-on`.

The same provider and the same model serve every account; there is no choice per account and no key per account. Of the four, only the provider, the key and the gates have to be supplied: the AI stays off until all three are.

## The AI choice page: `tool.ai`

```
tool.ai
```

An administrator-only full-screen page (140 columns by 43 lines at least; it is in SDSYS's VOC only). It has two boxes.

**Provider** lists Anthropic, OpenAI, Google and DeepSeek, then Custom, one to a row. A check box marks the provider in use; none marked means the AI is off. The four named providers come with their address and a default model filled in (the Model column says `(default)` beside one you have not changed); you supply the key, and M names another model if you want one. **Custom** is the fifth choice, where you fill in everything yourself, the model included: a name, an `https://` address, the request layout (`anthropic` or `openai`), the authentication (`bearer` or `x-api-key`), a version header (or none) and the name of the field that limits the length of an answer. Below the list, the row under the cursor is shown in full, with the file of certificate authorities and the limits.

**Accounts** lists the accounts that belong to a person, with the state of each one's `ai` gate.

| Key | In the Provider box | In the Accounts box |
|---|---|---|
| Enter or space | check the provider under the cursor (you type its name to confirm), or uncheck the one in use | turn the account's gate on (you type the account's name) or off |
| M | name the model (a dash goes back to the provider's default; Custom has none, so there it clears it) | |
| K | set the key: the terminal is handed to the helper's own prompt | |
| X | remove the key | |
| C | fill in Custom | |
| D | remove the Custom connection (the helper refuses while it is in use) | |
| A | the file of certificate authorities (you type `ca` to confirm) | |
| L | change a limit | |
| T | the standing text, in a box with an editor | the same |
| Tab | change box | change box |
| F1, `?` or a click on `[?]` | explain the box | explain the box |
| F5 | read the machine again | read the machine again |
| Ctrl-Q | leave | leave |

**The page writes nothing itself and knows no key.** Every change is a `set.ai` or `modify.account` sentence, shown with its effect in a box that you answer Run or Cancel (Enter chooses Cancel). The page then runs exactly that sentence. The key is not typed on the page: the page gives the terminal to `set.ai key`, whose prompt belongs to the helper, and takes the screen back when you press Enter.

Opening the page changes nothing and writes one audit line, `tool start app=tool.ai`.

## The verb: `set.ai`

```
set.ai
set.ai provider anthropic | openai | google | deepseek | custom | none
set.ai model PROVIDER NAME | -
set.ai key PROVIDER
set.ai key PROVIDER clear
set.ai custom NAME URL FORMAT AUTH VERSION MAXPARAM
set.ai custom clear
set.ai ca PATH | -
set.ai limit NAME NUMBER
set.ai context HEX | -
```

For the administrator only (SDSYS's VOC). Alone it says what is set: the provider in use, each provider's address, model and whether its key is set, the certificate file and the limits. It never shows a key. `provider none` turns the AI off for everyone. `key` hands the terminal to the helper's prompt; nothing typed there reaches SD. A word may hold letters, digits and `. _ : / @ + , -` and nothing else. The helper checks every result whole before it writes it: one provider selected means its details are complete, a Custom address is `https://` with no query string, a limit is a whole number in range.

The limits, and what they are as delivered:

| Limit | Delivered | Meaning |
|---|---|---|
| `requests-hour` | 20 | requests one operating system user may make in an hour |
| `tokens-day` | 100000 | tokens (in plus out) one user may use in a day |
| `timeout` | 30 | seconds to wait for the provider (at most 300) |
| `bytes-request` | 65536 | the most that may be sent in one request |
| `bytes-reply` | 65536 | the most that may come back |
| `max-tokens` | 1024 | the longest answer asked for |

## The standing text

Press **T** on `tool.ai` (or choose Provider, Standing text). A box shows the text that is sent first with every AI request from every account, and says whether it is SD's default or yours. Edit it there: Enter starts a new line and Tab moves to the buttons. **Save** shows the command and its effect in a Run / Cancel box (Enter chooses Cancel), and Run keeps your text. **Shipped default** removes yours, so SD's default is sent again. **Cancel** or Esc changes nothing.

The default tells the AI that this is SD Core for Linux, that it should answer for SD and not for another multivalue product, that command words are lower case, which dictionary types there are, that access to the operating system, the shell and the API is a gate you turn on for each account, and where SD's help is: F1 and the `[?]` buttons, the `pdf` command, the SD BASIC guide and the knowledge pack under `/usr/local/sdsys/agent-pack` (for an AI agent that can read files on this machine), and the documentation on the web. Put your own site's facts in it, such as which accounts and files matter and how your programs are named.

What is kept:

- plain English: printable ASCII characters and new lines, at most 4,000 characters;
- nothing that names SD's own code or build (`gpl.bp`, `gplsrc` and the other names of the screen above). Such a text is refused when you save it, with the line `set.ai context refused name=...` in the audit trail. A text that names them all the same (written into the helper's file by hand) stops every request, with `ai refused why=context`, until it is put right.

The text is sent to the provider with every request, before SD's own instruction, and counts towards `bytes-request`. It is invisible to the person asking: it is not in their preview (the size shown there counts it) and their question is sent as they typed it. It is kept by the helper in `/var/lib/sd-ai/context` (owner `sdai`, mode 0640), and only you can change it. An upgrade keeps it; removing SD with its configuration removes it.

At the prompt the verb takes the text as one word of hexadecimal (`set.ai context 48656c6c6f`), which is how the page passes a text of several lines; `set.ai context -` goes back to the default. `sd-ai-ctl show` says whose text is in use and how long it is.

## The gate for each account

```
modify.account NAME ai-on
modify.account NAME ai-off
create.account user NAME ai-on
```

The gate is membership of the Linux group `sdaiusers`, as `sdapi` and `sdfiles` are for the API and the files route. It is **off for every account** as delivered and for every new account; the installer's question about opening the gates leaves it out on purpose, because every request is paid for by whoever holds the provider's key. It is for accounts that belong to a person (not a group account), and `ai-on` needs the person to be a member of `sdusers`, as the other gates do. The line printed is `Account fred has ai yes`, read back from the group file. It takes effect at the person's next request: the helper looks at the group each time. `modify.account NAME ai-on ai-off` in one command is refused.

SDSYS has no gate: the administrator, who chooses the provider and holds the key, may always use the AI, from the prompt (`ai`) and from the AI line of every page, once a provider, a model and a key are set. `modify.account sdsys ai-on` is not needed and is refused, as every `modify.account` of SDSYS is.

The backup of an account records the gate (`route.ai`) and a restore puts it back.

## The key

The key is typed at the helper's own prompt (`set.ai key anthropic`, or K on the page). It goes from your terminal to the helper over the socket and is written to `/var/lib/sd-ai/keys/anthropic`, mode 0600, owned by `sdai`. SD does not read it, keep it, print it or put it in the audit trail; the page and the verb read back only whether it is **set**. `set.ai key anthropic clear` removes it. A key is never an argument of a command, so it is in no process list and no history.

If a key is lost or shown to someone, clear it and ask the provider for a new one: SD cannot tell you who has seen it.

## Custom: say it plainly

Custom lets you point the helper at any `https://` address. The text people send, and the key, then go to that host. That is your deliberate act and it is the widest thing on this page. What stays fixed: https only (a local model server on `http://` is not allowed), the certificate and the host name are always checked (there is no switch to turn that off), the helper never follows a redirect to another host, and the key is sent only to the address you gave. A private certificate authority is the file you name with `set.ai ca`; **it replaces the system store for the helper**, so whoever holds one of its keys can read what accounts send and the key. Use a file you trust, and `set.ai ca -` to go back to the system store.

If you want only the three named providers, leave Custom unfilled.

## The audit trail

All in lower case, none with a key or the text:

```
ai request account=fred program=ai bytes.out=154
set.ai provider=anthropic
set.ai model provider=anthropic model=claude-...
set.ai key set provider=anthropic
set.ai key cleared provider=anthropic
set.ai custom name=MyLLM host=api.example.com
set.ai limit name=tokens-day value=50000
set.ai context bytes=1640
set.ai context=default
set.ai context refused name=gpl.bp
ai refused why=context app=home name=gpl.bp
modify.account ai-on account=fred
tool start app=tool.ai
```

The `ai request` line is written by the SD kernel **before** the connection is made, with the account and the program that called, so a crash or a refusal still leaves the record. The Custom line names the host and never the whole address.

## Troubleshooting

| What you see | What it means |
|---|---|
| `The AI helper could not be reached: it is not running, or it is not installed` | the socket is not there: `systemctl status sd-ai.socket`; an install from before this release has not set it up |
| `The AI is off: the administrator has not chosen a provider` | nothing is checked on the page (`set.ai provider ...`) |
| `The AI is not set up for anthropic: the administrator has not set its model` (or `key`) | the provider is chosen but its key is missing; a model is missing only for Custom, which has no default (the named providers have one) |
| `This account may not use the AI: ... modify.account NAME ai-on` | the account is not in `sdaiusers` |
| `The AI did not answer: limit (...)` | one of the limits above is used up; wait, or raise it |
| `The AI did not answer: net (...)` or `timeout` | the provider could not be reached; check the address, the certificate and the clock |

## What has not been shown

The helper, the verb and the page are tested against a stand-in provider on this machine, in a private copy of SD. They have **not been run against a real provider**: the request layouts follow each provider's published documentation, and the one for OpenAI (`max_completion_tokens`) has not been checked against a real key. A real install, the real systemd socket and the helper running as `sdai` are a separate check.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Giving an AI Agent an Account](18-the-agent-account.html) ·
[Operating system access](03-operating-system-access.html).

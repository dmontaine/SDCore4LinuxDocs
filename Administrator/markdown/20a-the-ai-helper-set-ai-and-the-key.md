Title: The AI Helper: set.ai, the Key and Troubleshooting
Subtitle: The set.ai verb, the standing text, the gate for each account, the key, Custom, the audit trail and troubleshooting.

This page continues [The AI Helper](20-the-ai-helper.html).

## The verb: `set.ai`

```
set.ai
set.ai provider anthropic | openai | google | deepseek | custom | none
set.ai model PROVIDER NAME | -
set.ai models PROVIDER
set.ai key PROVIDER
set.ai key PROVIDER handover
set.ai key PROVIDER clear
set.ai custom NAME URL FORMAT AUTH VERSION MAXPARAM
set.ai custom clear
set.ai ca PATH | -
set.ai limit NAME NUMBER
set.ai context HEX | -
```

For the administrator only (SDSYS's VOC). Alone it says what is set: the provider in use, each provider's address, model and whether its key is set, the certificate file and the limits. It never shows a key. `provider none` turns the AI off for everyone. `models` asks the provider, with its key, for the names of its models and prints them, one to a line. `model` keeps the name you give, and says so when the provider does not list it (`deepseek does not list a model named Deepseek-V4-Pro, so requests may be refused`, then `It lists deepseek-v4-pro`). `key` hands the terminal to the helper's prompt; nothing typed there reaches SD. `key PROVIDER handover` is what the page runs: it reads the page's hand-over file and removes it. When a provider refuses a request, its own explanation is shown after the HTTP status (`the provider refused the request (HTTP 400): Model Not Exist`), cut to one line, with any copy of the key taken out; a refused key (401 or 403) shows only that the key was not accepted. A word may hold letters, digits and `. _ : / @ + , -` and nothing else. The helper checks every result whole before it writes it: one provider selected means its details are complete, a Custom address is `https://` with no query string, a limit is a whole number in range.

The limits, and what they are as delivered:

| Limit | Delivered | Meaning |
|---|---|---|
| `requests-hour` | 20 | requests one operating system user may make in an hour |
| `tokens-day` | 100000 | tokens (in plus out) one user may use in a day |
| `timeout` | 30 | seconds to wait for the provider (at most 300) |
| `bytes-request` | 65536 | the most that may be sent in one request |
| `bytes-reply` | 65536 | the most that may come back |
| `max-tokens` | 1024 | the longest answer, at the prompt and on every page: raise it for longer answers (the helper never asks a provider for more) |

## The standing text

Press **T** on `tool.ai` (or choose Provider, Standing text). A box shows the text that is sent first with every AI request from every account, and says whether it is SD's default or yours. Edit it there: Enter starts a new line and Tab moves to the buttons. **Save** shows the command and its effect in a Run / Cancel box (Enter chooses Cancel), and Run keeps your text. **Shipped default** removes yours, so SD's default is sent again. **Cancel** or Esc changes nothing.

The default tells the AI that this is SD Core for Linux, that it should answer for SD and not for another multivalue product, that command words are lower case, which dictionary types there are, that access to the operating system, the shell and the API is a gate you turn on for each account, and where SD's help is: F1 and the `[?]` buttons, the documentation PDFs in the shared account, the SD BASIC guide and the knowledge pack under `/usr/local/sdsys/agent-pack` (for an AI agent that can read files on this machine), and the documentation on the web. Put your own site's facts in it, such as which accounts and files matter and how your programs are named.

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

The gate is membership of the Linux group `sdaiusers`, as `sdapi` and `sdfiles` are for the API and the files route. It is **off for every account** as delivered and for every new account; the installer's question *Open every access gate for your SD account?*, answered `y`, opens it for the installing user's own account with every other gate, and for no other. Every request is paid for by whoever holds the provider's key, so answer `n` if that account should not have it. It is for accounts that belong to a person (not a group account), and `ai-on` needs the person to be a member of `sdusers`, as the other gates do. The line printed is `Account fred has ai yes`, read back from the group file. It takes effect at the person's next request: the helper looks at the group each time. `modify.account NAME ai-on ai-off` in one command is refused.

SDSYS has no gate: the administrator, who chooses the provider and holds the key, may always use the AI, from the prompt (`ai`) and from the AI line of every page, once a provider, a model and a key are set. `modify.account sdsys ai-on` is not needed and is refused, as every `modify.account` of SDSYS is.

The backup of an account records the gate (`route.ai`) and a restore puts it back.

## The key

The key is typed at the helper's own prompt (`set.ai key anthropic`) or in the setup dialog on the page. At the prompt it goes from your terminal straight to the helper and SD never sees it; the prompt shows one `*` for each character you type or paste (Backspace takes one back), so a long key shows that it arrived, and the key itself is never shown (the number of stars is its length, which anyone looking at the screen can count). From the dialog it passes through SD's memory and a hand-over file only `sdsys` can reach, which is removed at once (see above). Either way it is written to `/var/lib/sd-ai/keys/anthropic`, mode 0600, owned by `sdai`; SD does not keep it, print it or put it in the audit trail, and the page and the verb read back only whether it is **set**. `set.ai key anthropic clear` removes it. A key is never an argument of a command, so it is in no process list and no history.

If a key is lost or shown to someone, clear it and ask the provider for a new one: SD cannot tell you who has seen it.

## Custom: say it plainly

Custom lets you point the helper at any `https://` address. The text people send, and the key, then go to that host. That is your deliberate act and it is the widest thing on this page. What stays fixed: https only (a local model server on `http://` is not allowed), TLS 1.2 or later, the certificate and the host name are always checked (there is no switch to turn that off), the helper never follows a redirect to another host, and the key is sent only to the address you gave. A private certificate authority is the file you name with `set.ai ca`; **it replaces the system store for the helper**, so whoever holds one of its keys can read what accounts send and the key. Use a file you trust, and `set.ai ca -` to go back to the system store.

If you want only the four named providers, leave Custom unfilled.

## The audit trail

All in lower case, none with a key or the text:

```
ai request account=fred program=ai bytes.out=154
set.ai provider=anthropic
set.ai model provider=anthropic model=claude-...
set.ai key set provider=anthropic
set.ai key set provider=anthropic from=page
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
| `The AI did not answer: net (...)` or `timeout` | the provider could not be reached; check the address, the certificate, the clock, and whether the machine needs a proxy to reach the internet (the helper uses none) |
| `The AI did not answer: refused (the provider refused the request (HTTP 400): ...)` | the provider's own words follow the status: often a model it does not have; choose one from its list with S |

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Giving an AI Agent an Account](18-the-agent-account.html) ·
[Operating system access](03-operating-system-access.html) ·
[The Audit Trail](21-the-audit-trail.html).

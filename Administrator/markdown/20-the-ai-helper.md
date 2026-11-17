Title: The AI Helper
Subtitle: One provider and one model for every account, a key that SD never sees, and a gate for each account.

SD can ask an AI model a question for an account holder (the `ai` verb, see *SD TCL - Asking the AI* in the User documentation). This page is for the administrator: it says what is set up, what leaves the machine, how to choose the provider and give it a model and a key, and how to allow or stop an account.

> **Nothing is on as delivered.** There is no provider, no key, and no account has the gate (each named provider comes with a default model, so the model is the one thing you need not supply). Until you have done the other three, the `ai` verb says so in words and nothing is sent anywhere. Turning one of them on is your act, and each is one command (or one key on the AI choice page) that can be undone. The one exception is the installer's question *Open every access gate for your SD account?*: answered `y`, it gives the installing user's own account the `ai` gate along with the others. It still sends nothing until you have chosen a provider and set its key.

## What leaves the machine

When a person types `ai some text`, SD shows them the text, the provider and the model, and asks whether to send it. Only if they answer `y` or `yes` does anything go out. What goes out is your standing text (below), that text, one fixed sentence that asks for a short plain answer, and a limit on the length of the answer. It is sent over **https**, with the certificate checked, to the address of the provider you chose, and to nowhere else. The key goes only to that address. No proxy is used: a machine that reaches the internet only through an HTTP proxy cannot use the AI.

SD adds nothing of the account, the session or the data. A person can of course type or paste whatever they like into the question, which is why the preview is not optional and why the gate is yours to give.

**The standing text.** Every request, from the `ai` verb and from every AI line, begins with a few lines of yours: what SD is, how its commands are written, which gates there are, and where SD's help is. SD ships a default; you can replace it (see [The standing text](20a-the-ai-helper-set-ai-and-the-key.html#the-standing-text) below). It is yours and is invisible to the person asking: it is not in their preview and it does not change their question. The preview's size counts it.

**Passages of the documentation.** The AI line (the home screen, the pages of the toolkit, the IDE, SED, the collection editor and the debugger; not the `ai` verb) also adds up to four sections of SD's own documentation that match the request, at most 2,400 bytes each and 6,000 in all. Like the standing text and SD's fixed instruction they are not shown in the preview; its size counts them. The installer puts the markdown of the User and Administrator documents in `docs/user` and `docs/admin` under the system directory, from the documentation repository at the branch it installs. `docs/user` is readable by every session (755, files 644). **`docs/admin` is yours alone: mode 700 and files 600, owner `sdsys`, which is the only operating-system user an administrator session runs as, and the routine asks SD for the administrator before it looks there.** An account holder's request is never answered from those pages. The directory is replaced whole at each install and is not a place to put your own text. If the installer could not reach the documentation it prints a note, installs nothing and the AI line works without passages. This is documentation, not source: the rule below that the AI is never given SD's own code is unchanged.

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
2. **A model** for that provider. Each of the four named providers comes with a default model, shown on the page and used until you name another (`set.ai model PROVIDER NAME`; a dash goes back to the default). The defaults are the balanced model of each provider as its own documentation named it (DeepSeek's is `deepseek-v4-flash` since DeepSeek retired `deepseek-chat`): **model names change, so check the one you will pay for.** On the page the model is chosen from the provider's own list in the setup dialog (S), and `set.ai models PROVIDER` prints that list at the prompt. Model names are case-sensitive: `deepseek-v4-pro` works, `Deepseek-V4-Pro` does not. Custom has no default; its model is yours.
3. **A key** for that provider, from the provider's own account. It is typed or pasted in the setup dialog (shown as `*`) or at the helper's own prompt, and kept for the helper only.
4. **The gate for each account that may use it**: `modify.account NAME ai-on`.

The same provider and the same model serve every account; there is no choice per account and no key per account. Of the four, only the provider, the key and the gates have to be supplied: the AI stays off until all three are.

## The AI choice page: `tool.ai`

```
tool.ai
```

An administrator-only full-screen page (140 columns by 43 lines at least; it is in SDSYS's VOC only). It has two boxes.

**Provider** lists Anthropic, OpenAI, Google and DeepSeek, then Custom, one to a row. A check box marks the provider in use; none marked means the AI is off. The four named providers come with their address and a default model filled in (the Model column says `(default)` beside one you have not changed); you supply the key, and S (setup) sets the key and the model together. **Custom** is the fifth choice, where you fill in everything yourself, the model included: a name, an `https://` address, the request layout (`anthropic` or `openai`), the authentication (`bearer` or `x-api-key`), a version header (or none) and the name of the field that limits the length of an answer. Below the list, the row under the cursor is shown in full, with the file of certificate authorities and the limits.

**Accounts** lists the accounts that belong to a person, with the state of each one's `ai` gate.

| Key | In the Provider box | In the Accounts box |
|---|---|---|
| Enter or space | check the provider under the cursor (you type its name to confirm), or uncheck the one in use | turn the account's gate on (you type the account's name) or off |
| S | the setup dialog for the provider under the cursor: the key and the model, the model chosen from the provider's own list (below) | |
| X | remove the key | |
| C | fill in Custom | |
| D | remove the Custom connection (the helper refuses while it is in use) | |
| A | the file of certificate authorities (you type `ca` to confirm) | |
| L | change a limit | |
| T | the standing text, in a box with an editor | the same |
| F6, Shift-F6, Left, Right | change box (F6 goes on to the AI line when the AI is on for this account) | change box |
| F1, `?` or a click on `[?]` | explain the box | explain the box |
| F5 | read the machine again | read the machine again |
| Ctrl-Q | leave | leave |

**The page keeps nothing itself and never shows a key.** Every change is a `set.ai` or `modify.account` sentence, shown with its effect in a box that you answer Run or Cancel (Enter chooses Cancel). The page then runs exactly that sentence. The exception is the setup dialog, whose Save is the confirmation.

**The setup dialog (S).** It looks the same every time, whatever is already set:

- **Key**, a password field. What you type or paste is shown as `*`. When a key is already set the field shows a row of twelve stars, which keeps it; replace them to give a new key.
- **Model**, a list of the provider's own model names, with the one in use chosen. With no key yet the list says the key comes first: enter the key and press Tab, and the list is filled from the provider with that key. A model in use that the list does not hold is pointed out, and when it differs from a listed one only in capitals (`Deepseek-V4-Pro` for `deepseek-v4-pro`) the listed one is chosen for you.
- **Other name**, only for a model the list does not hold, such as on a Custom server that gives no list. A name typed here is still checked against the list when there is one.
- **Save** sets what you chose; **Cancel** or Esc changes nothing more (a key already handed over by Tab stays set, and the page says so).

**What the dialog does with the key.** When you leave the Key field with a new key (Tab, or Enter, which then shows the list rather than saving), the page writes it to a file in a directory only `sdsys` can enter (`$aikey` in the SD system directory, mode 0700), runs `set.ai key PROVIDER handover`, which gives that file to the helper's client as its input, and removes the file whether or not that worked. The key is never on a command line and never in the audit trail. It does pass through SD's memory while the dialog is open, and through that file for a moment. If you would rather it never touched SD, use `set.ai key PROVIDER` at the prompt, which hands the terminal to the helper's own prompt.

Opening the page changes nothing and writes one audit line, `tool start app=tool.ai`.

## Continued in

[The AI Helper: set.ai, the Key and
Troubleshooting](20a-the-ai-helper-set-ai-and-the-key.html) — set.ai, the
standing text, the key and troubleshooting.

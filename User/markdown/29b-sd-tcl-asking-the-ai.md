Title: SD TCL - Asking the AI
Subtitle: One question to the AI your administrator has chosen, after you have seen what will be sent.

```
ai text
ai "text that ends with a question mark?"
```

**`ai`** sends your text to an AI model and prints the answer. It is off until your administrator has chosen a provider, given it a model and a key, **and allowed your account**; until then it says which of those is missing and sends nothing.

## What you see

```
:ai what does the SELECT verb do
This will be sent to anthropic (model claude-...), 190 bytes; the provider sees all of it:
You are answering a question typed at the terminal of SD Core for Linux, a multivalue database. Answer briefly, in plain text without markup.
what does the SELECT verb do
Send it? (y/N)
```

You see the provider, the model and the size, then **everything that will leave the machine**: one fixed sentence that asks for a short plain answer, and your text. Nothing is sent unless you answer `y` or `yes`. Anything else - Enter alone, `n`, a typing error, an input that has ended - sends nothing, so a program cannot make `ai` send by feeding it an answer.

The answer is printed as plain text, wrapped to your window, followed by the tokens used:

```
Waiting for the answer ...

The SELECT verb builds a list of record ids ...

Tokens used: 31 in, 52 out (anthropic)
```

If the answer was cut at the length limit, or characters had to be replaced with `?` (only plain text is shown: no colours, no cursor movements, no letters outside the English alphabet), it says so.

## Questions that end with a question mark

The command line is read by TCL first, and **a TCL command that ends with `?` is added to the command stack without being run**. So `ai what is a select list?` does nothing. Put the text in quotes:

```
ai "what is a select list?"
```

The quotes are taken off before anything is shown or sent.

## What is sent, and what is not

Only your text and the fixed sentence. `ai` does not add your account, your files, your session or your data. If you paste a record into the question, the provider sees it. The administrator's audit trail records that you asked (your account, the program, the number of bytes), never what you asked or what came back.

`ai` only prints the answer. It never runs anything the answer says.

## If it says no

| It says | Why |
|---|---|
| `The AI is off: the administrator has not chosen a provider` | nothing has been set up |
| `The AI is not set up for anthropic: the administrator has not set its model` (or `key`) | the provider is chosen but not finished |
| `This account may not use the AI: the administrator can allow it with modify.account NAME ai-on` | your account has not been allowed |
| `The AI did not answer: limit (...)` | you, or everyone on your Linux user, have used the hourly or the daily limit |
| `The AI did not answer: net (...)` or `timeout` | the provider could not be reached or did not answer in time |
| `The AI helper could not be reached` | the helper that talks to the provider is not running |

It needs no terminal features and works over ssh. In a session with no one to answer (a script, a phantom) it asks, gets no answer, and sends nothing.

## See also

[The AI helper](20-the-ai-helper.html) (for the administrator) ·
[SD TCL - The Terminal and the Session](29-sd-tcl-the-terminal-and-the-session.html).

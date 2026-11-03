Title: SD TCL - Asking the AI
Subtitle: One question to the AI your administrator has chosen, after you have seen what will be sent.

```
ai text
ai "text that ends with a question mark?"
```

**`ai`** sends your text to an AI model and prints the answer. It is off until your administrator has chosen a provider, given it a key (and a model, for a Custom provider), **and allowed your account**; until then it says which of those is missing and sends nothing.

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

SD does not take questions about its own code or build (`gpl.bp`, `gplsrc`, the kernel) to the AI: it says so and sends nothing; the source is open, so ask an AI outside SD for that. In the editors, a record of SD's own files, such as a header in `syscom`, is never sent either.

### Passages of the documentation (the AI line, not the `ai` verb)

When you ask in the AI line (the home screen, a page of the toolkit, the IDE, SED, the collection editor or the debugger), SD looks through its own User documentation for the sections that match your words and adds up to four of them to the request, so that the model answers from SD's pages and not from what it remembers of other multivalue systems. The preview shows how many passages there are and how many bytes, each one's page and section in brackets (for example `[user/01-sd-basic-program-structure.md#the-program-header]`) and its first four lines, and says how many lines more it sends. A preview taller than the screen scrolls with PgUp and PgDn (Home and End go to its first and last lines; the bottom border says which lines are shown), and Send and Cancel stay on the screen. Nothing leaves until you choose Send, and Cancel is the default. A passage is at most 2,400 bytes and all of them 6,000. A request of common words, or of words no page holds, gets none. The model is asked to name the page it used, so you can find it in the documents. If you are the administrator, the pages written for the administrator are searched too; they are never searched for anyone else.

If the documentation could not be fetched when SD was installed, there are no passages and the line works as it did. The `ai` verb adds no passages.

## The AI line on a page of the toolkit

The full-screen pages of the toolkit have the same line as [the home screen](29a-sd-tcl-the-home-screen.html), when the AI is on for your account. **Every page has it - the development pages (`tool.voc`, `tool.files`, `tool.catalog`, `tool.dict`, `tool.query`, `tool.bulk`, `tool.test`, the holder's `tool.gates`), `my.menu`, and the administrator's pages - except `tool.keys`, which shows every key you press, F6 included.** On `my.menu` the line only answers questions: every key there changes your list, so it is offered none. The line is the row just above the status line, and the list above it is one row shorter to make room. **Without the AI there is no line, no F6 on the key row and no AI title in the menu bar, and the page is exactly what it was.**

Press **F6**, or choose **AI > Ask the AI** in the menu bar, or click the line. Type what you want in your own words and press Enter. As on the home screen, Enter sends nothing: it shows **everything that will leave the machine** (the provider and model, one fixed instruction, what the page is and the list of what it offers, your request), **Cancel is the default**, and you choose **Send** (press `s`) to send. While the line has the focus it takes your keys; Esc gives the focus back to the page and keeps what you typed.

What it can do is only what **keys of the page that change what is shown** can do, and the page decides which. On `tool.voc` these are T (the type shown), S (the state shown), `/` (the name filter) and F5 (read again); on `tool.files` and `tool.catalog`, `/` and F5; on `tool.dict` the Items and Indices views, back to the file, `/` and F5; on `tool.query` the file filter and reading the files again; on `tool.bulk` the list switch and F5; on `tool.test` the filter, F5 and the output pane of the runs; on `tool.gates`, F5. On the administrator's pages it is the same kind of key - the views, filters, the output pane and refresh - and **nothing that changes an account, a gate, a session, a door, a setting, a backup or the master files is offered**: no create, delete, suspend, queue, logout, unlock, sync, restore, edit or key.

**A few keys that make or compile something are offered too:** N (a new item) and C (compile the I item under the cursor) on `tool.dict`, N (a new file) on `tool.files`, and B (compile the program under the cursor) on `tool.catalog`. For these, **Reject is the default**: Enter alone turns the proposal down, and you press `a` to accept it. **Delete, edit, clear, run, apply, save, quit and the rest are never offered.** If the AI names one of them anyway, or anything else the page does not offer, the proposal is ignored, with a note, and nothing happens.

An action you accept is carried out by **the page's own key**, exactly as if you had pressed it, so what the page does for that key, and anything it asks first, is unchanged. **A name the AI gives with the action** (the new file's name, the new item's id, the text of a filter) is only put in the page's own question as its answer to start from: you can change it, the page checks it as if you had typed it, and the page's own box (Run or Cancel) still comes after. Enter alone accepts a proposal that only changes what is shown. No command is run from a page. The page sends no record and no value of any file, only what it is and what it offers; the audit trail records that you asked, never what.

## The AI line in the dictionary form

The [dictionary form](24-sd-tcl-programs-and-the-catalogue.html) of the IDE (an item of a file's dictionary shown as rows: Type, Field #, Conversion Cd, Column Heading, Len & Just and the rest) has an **AI>** line at its foot when the AI is on for your account. Press **F6**, Tab to it or click it, say what the item should be in your own words - *a date in field 3 headed Joined*, *a total of the amounts, two decimals* - and press Enter. Enter in this line asks the AI; it does not accept the form.

The preview shows everything that will be sent, and **Cancel is the default**: the instruction, which says the page is a form and how values for it are given, **the list of the form's fields** (the key and what each holds), what the form is, **the item's values as they are on the screen**, and your request. Because the item's values are sent, **an item of the dictionary of one of SD's own files is never sent**: SD asks where the item is first and refuses, before any preview, as it does in the editors.

The answer shows **every value the AI proposes, in full**, with **Accept** and **Reject**, and **Reject is the default**: Enter alone fills nothing. **Accept** puts each value into its row **only if it passes the form's own check** (the same check as a value you type: a field number from 0 to 9999, a format such as `30 L`, a conversion SD knows, one line where the row is one line); a Type the AI gives is checked first and makes the rows of that type, as typing it would. The line near the foot says how many rows were filled and **names each value that was not, and why**; a name the AI gave that is not a field of the form is left out and said in the answer. **Nothing is written**: you look at the rows, change what you like, and **Accept** the form, and the IDE's own save writes the item, with your dictionary-edit gate and its overwrite question, as for any other item. The form offers no command and runs none.

## Follow up: a question about the answer

Every answer's box has a **Follow up** button, after the others, and it is never the default. It applies nothing - a proposed change, action, command or set of values is not taken - and **your next request from the same place carries that question and the AI's answer** with it, so you can ask *and the next line?* or *make it two decimals instead* without saying everything again. On the home screen and the pages the line says **AI follow-up>** while one is waiting; in the IDE, SED, the collection editor, the debugger and the dictionary form the status line says so.

The next request's preview **shows the earlier question and answer in full**, before your request, and counts their size; Cancel is still the default. They go to the provider as the earlier turns of a conversation. Choosing Follow up again on that answer carries both exchanges, and so on up to **the last three**.

A follow-up is **used once**: the next request takes it whether you send it or cancel the preview. It is also dropped **after ten minutes**, when you leave the page (or the home screen is made again), in another account, and by any other program's AI line - each place carries only its own. The earlier questions are screened again as if you had just typed them. The audit trail says that a request was a follow-up and how many exchanges it carried, never what they said.

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

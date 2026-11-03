Title: SD Text User Interface - A Form and a Confirm Box
Subtitle: The third example: a form checked by the program, a confirm box whose default is Cancel, a record the program writes itself, the output pane and the Esc rule.

`notes` lists the records of a file of the account and writes a new one. The form
asks for the record; the program checks what was typed; a confirm box shows what
will be written; and only the program writes it. The file is an ordinary data file
of the account:

```
create.file notes
```

## The program

```
* notes - a form, a confirm box, a record the program writes, and the output pane
$include tkpub.h
$include err.h

   prompt ''
   open 'notes' to notes.f else
      crt 'notes: the file notes cannot be opened'
      stop
   end
   call !tkopen('notes', ctx, err, '', '')
   if err # '' then
      crt err
      stop
   end

   keys = ''
   call !tkkeys('add', keys, 'ctrl-q', 'quit', 'quit', '', 1)
   call !tkkeys('add', keys, 'ctrl-n', 'new', 'new', '', 1)
   call !tkkeys('add', keys, 'ctrl-o', 'output', 'output', '', 1)
   call !tkkeys('add', keys, 'esc', 'menu', 'menu', '', 1)
   call !tkkeys('menu', keys, 'quit', '&File', '&Quit', '', '')
   call !tkkeys('menu', keys, 'new', '&File', '&New note', '', '')
   call !tkkeys('menu', keys, 'output', '&View', '&Output', '', '')

   outopen = 0
   gosub declare.layout
   gen = 0
   msg = 'Ctrl-N writes a new note'
   gosub draw.all
   loop
      call !tkmenubar('draw', ctx, keys, 'Notes', '', '', mr)
      call !tkframe(ctx, keys, 'Notes', msg)
      nm = ''
      screen key returning nm
      if nm = '' then
         if status() = ER$EOF then exit
         continue
      end
      mr = ''
      call !tkmenubar('key', ctx, keys, 'Notes', nm, outopen, mr)
      if mr<1> # '' then nm = mr<4>
      begin case
         case nm = ''
            null
         case nm = 'guardquit' or nm = 'ctrl-q'
            exit
         case nm = 'resize'
            call !tklayout('refresh', ctx, '', chg)
            gosub redraw
         case nm = 'ctrl-n'
            gosub new.note
         case nm = 'ctrl-o'
            gosub toggle.out
         case nm = 'esc'
            if outopen then gosub toggle.out
         case outopen and (nm = 'up' or nm = 'down' or nm = 'pgup' or nm = 'pgdn')
            oc = ''
            call !tkout('key', ctx, nm, '', oc)
            call !tkout('draw', ctx, 'output', '', oc)
      end case
   repeat
   call !tkclose(ctx)
   stop

new.note:
   spec = 'New note' : @fm : '&Write' : @fm : ''
   spec<4> = 'id' : @vm : 'Record id' : @vm : 20
   spec<5> = 'text' : @vm : 'Text' : @vm : 60 : @vm : 500
   fa = '' ; fb = '' ; fc = ''
   call !tkform('open', ctx, spec, '', fc)
   loop
      call !tkform('run', ctx, fa, fb, fc)
      if fa # 'ok' then exit
      id = trim(fb<1>)
      bad = ''
      if id = '' then bad = 'A note needs a record id.'
      if index(id, ' ', 1) then bad = 'A record id here has no spaces.'
      if bad = '' then exit
      call !tkform('say', ctx, bad, 'id', '')
   repeat
   call !tkform('close', ctx, '', '', '')
   if fa # 'ok' then
      msg = 'Nothing was written'
      return
   end

   sent = 'write ' : id : ' in notes'
   lines = 'The text: ' : fb<2>
   read old from notes.f, id then
      lines<-1> = 'A note ' : id : ' exists; Write replaces it.'
   end
   res = '' ; cm = ''
   call !tkconfirm(sent, lines, '', res, cm, 'Write this record?', '&Write,&Cancel')
   if res # 'run' then
      msg = 'Nothing was written'
      call !tkout('add', ctx, 'info', sent : ': ' : cm, '')
      return
   end
   write fb<2> to notes.f, id
   call !tkout('add', ctx, 'ok', 'wrote ' : id : ' in notes', '')
   msg = 'Wrote ' : id
   gosub draw.list
   if outopen then call !tkout('draw', ctx, 'output', '', oc)
   return

toggle.out:
   oc = ''
   call !tkout('toggle', ctx, '', '', oc)
   outopen = oc
   gosub declare.layout
   gosub redraw
   return

declare.layout:
   d = ''
   if outopen then
      d<1> = 'list' : @vm : 1 : @vm : 1 : @vm : 29 : @vm : 138 : @vm : '' : @vm : 'stretch' : @vm : 1 : @vm : 'stretch' : @vm : 1
      d<2> = 'output' : @vm : 2 : @vm : 1 : @vm : 10 : @vm : 138 : @vm : '' : @vm : '' : @vm : '' : @vm : 'stretch' : @vm : 1
   end else
      d<1> = 'list' : @vm : 1 : @vm : 1 : @vm : 39 : @vm : 138 : @vm : '' : @vm : 'stretch' : @vm : 1 : @vm : 'stretch' : @vm : 1
   end
   perr = ''
   call !tklayout('declare', ctx, d, perr)
   return

redraw:
   gen += 1
   ctx<TK.C.GEN> = gen
   gosub draw.all
   return

draw.all:
   screen clear at 0,ctx<TK.C.YBODY> size ctx<TK.C.W>,ctx<TK.C.BODYH>
   gosub draw.list
   oc = ''
   if outopen then call !tkout('draw', ctx, 'output', '', oc)
   return

draw.list:
   r = ''
   call !tklayout('pane', ctx, 'list', r)
   screen box at r<1,1>,r<1,2> size r<1,3>,r<1,4> title 'Notes'
   ids = ''
   select notes.f to 1
   loop
      readnext id from 1 else exit
      locate id in ids<1> by 'AL' setting p else null
      ins id before ids<p>
   repeat
   for i = 1 to r<1,4> - 2
      s = ''
      if ids<i> # '' then
         read t from notes.f, ids<i> else t = ''
         s = fmt(ids<i>, '20L') : t
      end
      screen text s at r<1,1> + 2,r<1,2> + i width r<1,3> - 4
   next i
   return
end
```

## The form

`spec<1>` is the title, `spec<2>` the label of the button that does the work, with
its `&` letter, and `spec<3>` the hint line (null gives the library's own). Each
field from `spec<4>` on is one entry: its id, its label, its width, its longest
text, and 1 for an entry shown as `*`. The fourth argument of `open` holds the
starting texts, one to a field.

`run` lets the person fill the form in and returns `ok` (Return in an entry presses
the default button) or `cancel`, the texts as typed, one to a field, and the id of
the entry that has the focus. **The form checks nothing.** The program does, and
when it refuses, `say` writes the refusal under the entries, puts the focus on the
entry named, and the program calls `run` again. Return with the id empty:

```
15   |                                   +- New note -----------------------------------------------------+                                   |
16   |                                   |                                                                |                                   |
17   |                                   | Record id                                                      |                                   |
18   |                                   | Text                                                           |                                   |
19   |                                   |                                                                |                                   |
20   |                                   | A note needs a record id.                                      |                                   |
21   |                                   |                                                                |                                   |
22   |                                   |                                                                |                                   |
23   |                                   | [ Write ]   [ Cancel ]                                         |                                   |
24   |                                   | Return does it, Esc leaves                                     |                                   |
25   |                                   |                                                                |                                   |
26   |                                   +----------------------------------------------------------------+                                   |
```

Tab moved to the next entry. In a small form of two entries, starting texts `ann` and null
showed `ann` in the first entry; a masked entry showed `1234` as `****`; and Esc
returned `cancel` with the texts typed so far still in `b` (`ann` and `1234`), so a
program that keeps only what `ok` returns must test `a` first, as this one does.

`close` puts back the screen that was under the form; call it on every way out of
the form, as `!tkclose` on every way out of the page.

## The confirm box

`!tkconfirm` shows a sentence and its explanation and asks. Its seven arguments:
the sentence, shown wrapped at spaces and never altered; the explanation, one line
to a field; a name the person must type as a second step (null here); `res` and
`msg`, returned; the title of the box; and the buttons. Null title is
`Run this command?` and null buttons are `&Run,&Cancel`; this program, which writes
a record rather than run a command, gives `Write this record?` and `&Write,&Cancel`:

```
17   |                                        +- Write this record? --------------------------------+                                         |
18   |                                        | this will run:                                      |                                         |
19   |                                        |   write phone in notes                              |                                         |
20   |                                        |                                                     |                                         |
21   |                                        | The text: Call the plumber about the kitchen tap.   |                                         |
22   |                                        |                                                     |                                         |
23   |                                        |                [ Write ]  [ Cancel ]                |                                         |
24   |                                        |                                                     |                                         |
25   |                                        +-----------------------------------------------------+                                         |
```

**The last button is Cancel and Enter chooses it.** Enter alone gave `res` = `cancel`
and `msg` = `nothing was run`; the record was not written (`ct notes phone` then said
`Record 'phone' not found`). **w** - the first button's letter - gave `res` = `run`.
**The box runs nothing and writes nothing**: the program's own `write` statement,
after `res` is `run`, wrote the record, and `ct notes phone` then showed it.

**A name to type.** For something that cannot be undone, give the name the person
must type as the third argument. In a box with the sentence
`delete notes phone` and the name `phone`, **r** opened a second box,
`type phone to run it`. `phon` returned `res` = `wrong` and `msg` =
`nothing was run: what was typed is not phone`; `phone` returned `run`; Esc in the
first box returned `cancel`.

## The output pane

`!tkout('add', ctx, kind, text, '')` keeps a line in the page's history, in memory,
for this run of the program; `kind` is `ok`, `refuse`, `out` or `info`. The pane is
closed until the program opens it. **Ctrl-O** here calls `toggle`, declares the
layout again - the list 10 rows shorter and a pane called `output` under it - and
draws everything; `!tkout('draw', ctx, 'output', '', oc)` draws the history in that
pane, the newest first:

```
29   +----------------------------------------------------------------------------------------------------------------------------------------+
30    Output
31   ok wrote phone in notes
32      write phone in notes: nothing was run
33  
    (rows 34 to 39 are the same as row 33)
40  [Notes]  Wrote phone
```

The pane never closes itself. The program closes it - here with **Ctrl-O** again or
with **Esc**.

## The Esc rule

**Esc closes what the page has open first; only when nothing is open does it open the
menu bar.** The sixth argument of `!tkmenubar('key', ...)` tells the bar which: this
program passes `outopen`, 1 while the output pane is open. With the pane open, Esc
was not the bar's; it came to the program's `case nm = 'esc'`, which closed the
pane. Pressed again, with nothing open, Esc opened the menu bar. File's only other
entry is Quit, which the library puts last, so File begins with **New note** and
Esc opened File:

```
 0   File  View
 1   New note    ^N --------------------------------------------------------------------------------------------------------------------------+
 2   Quit        ^Q        Tomatoes, beans and the old roses by the fence.                                                                    |
```

## A text longer than its place

`screen text ... width n` cuts a text at `n` cells; it does not wrap. The list shows
it: the record `reading` ends at the right border, at `the correlat`. To show a long
text whole, cut it into lines with `!tkwrap` first
([Panes and Pickers](05-panes-and-pickers.html)).

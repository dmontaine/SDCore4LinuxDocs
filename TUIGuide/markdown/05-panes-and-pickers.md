Title: SD Text User Interface - Panes and Pickers
Subtitle: The fourth example: two panes side by side and the focus, text wrapped to a pane, a pick list the program makes, and the record picker.

`browse` shows the records of the file `notes` from the third example: their ids in
one pane and the chosen record's text, wrapped, in the other. **Tab** moves the focus
between them. Three pickers find a record: a list the program makes, the records of
`notes`, and any file of the account and then a record in it.

## The program

```
* browse - two panes and the focus, wrapped text, a pick list and the record picker
$include tkpub.h
$include err.h

   prompt ''
   open 'notes' to notes.f else
      crt 'browse: the file notes cannot be opened'
      stop
   end
   call !tkopen('browse', ctx, err, '', '')
   if err # '' then
      crt err
      stop
   end

   keys = ''
   call !tkkeys('add', keys, 'ctrl-q', 'quit', 'quit', '', 1)
   call !tkkeys('add', keys, 'tab', 'next box', 'next', '', 1)
   call !tkkeys('add', keys, 'ctrl-p', 'jump', 'jump', '', 1)
   call !tkkeys('add', keys, 'ctrl-r', 'record', 'record', '', 1)
   call !tkkeys('add', keys, 'ctrl-f', 'any file', 'anyfile', '', 1)
   call !tkkeys('add', keys, 'esc', 'menu', 'menu', '', 1)
   call !tkkeys('menu', keys, 'quit', '&File', '&Quit', '', '')
   call !tkkeys('menu', keys, 'jump', '&Go', '&Jump to a note', '', '')
   call !tkkeys('menu', keys, 'record', '&Go', 'Pick a &record', '', '')
   call !tkkeys('menu', keys, 'anyfile', '&Go', 'Pick a &file and a record', '', '')

   d = ''
   d<1> = 'list' : @vm : 1 : @vm : 1 : @vm : 39 : @vm : 40 : @vm : '' : @vm : 'stretch' : @vm : 1
   d<2> = 'text' : @vm : 1 : @vm : 2 : @vm : 39 : @vm : 97 : @vm : 1 : @vm : 'stretch' : @vm : 1 : @vm : 'stretch' : @vm : 1
   ctx<TK.C.FOCI> = 'list' : @sm : 'Notes' : @vm : 'text' : @sm : 'Text'
   perr = ''
   call !tklayout('declare', ctx, d, perr)

   gosub read.ids
   ci = 1
   pane = 'Notes'
   gen = 0
   msg = n : ' note(s)'
   gosub draw.all
   loop
      call !tkmenubar('draw', ctx, keys, pane, '', '', mr)
      call !tkframe(ctx, keys, pane, msg)
      nm = ''
      screen key returning nm
      if nm = '' then
         if status() = ER$EOF then exit
         continue
      end
      mr = ''
      call !tkmenubar('key', ctx, keys, pane, nm, 0, mr)
      if mr<1> # '' then nm = mr<4>
      begin case
         case nm = ''
            null
         case nm = 'guardquit' or nm = 'ctrl-q'
            exit
         case nm = 'resize'
            call !tklayout('refresh', ctx, '', chg)
            gen += 1
            ctx<TK.C.GEN> = gen
            gosub draw.all
         case nm = 'tab'
            if pane = 'Notes' then pane = 'Text' else pane = 'Notes'
         case nm = 'up' and pane = 'Notes'
            if ci > 1 then ci -= 1
            gosub draw.panes
         case nm = 'down' and pane = 'Notes'
            if ci < n then ci += 1
            gosub draw.panes
         case nm = 'ctrl-p'
            gosub jump
         case nm = 'ctrl-r'
            gosub pick.record
         case nm = 'ctrl-f'
            gosub pick.any
      end case
   repeat
   call !tkclose(ctx)
   stop

read.ids:
   ids = ''
   select notes.f to 1
   loop
      readnext id from 1 else exit
      locate id in ids<1> by 'AL' setting p else null
      ins id before ids<p>
   repeat
   n = dcount(ids, @fm)
   return

* a pick from a list the program makes: nothing is opened or read by the picker
jump:
   items = ''
   for k = 1 to n
      read t from notes.f, ids<k> else t = ''
      items<k> = ids<k> : @vm : t[1, 60]
   next k
   mode = 'list'
   mode<2> = 'Note' : @vm : 'Begins'
   mode<3> = 16 : @vm : 60
   pid = 'Jump to a note'
   pres = ''
   pstart = ci
   call !tkpickrec(ctx, mode, items, pid, pres, pstart)
   if pres = 'ok' then
      ci = pid
      msg = 'Jumped to ' : ids<ci>
      gosub draw.panes
   end else
      msg = 'Nothing chosen'
   end
   return

* the record picker on the file notes
pick.record:
   pfile = 'notes'
   pid = '' ; pres = '' ; pnew = ''
   call !tkpickrec(ctx, 'record', pfile, pid, pres, pnew)
   begin case
      case pres = 'ok'
         locate pid in ids<1> setting p then
            ci = p
            gosub draw.panes
         end
         msg = 'Picked ' : pid
      case pres = 'new'
         msg = 'Ctrl-N in the picker: a new record would be ' : pnew
      case 1
         msg = 'Nothing picked'
   end case
   return

* a file of the account and then a record in it; the program opens it itself
pick.any:
   pfile = '' ; pid = '' ; pres = '' ; pnew = ''
   call !tkpickrec(ctx, '', pfile, pid, pres, pnew)
   if pres # 'ok' then
      msg = 'Nothing picked (' : pres : ')'
      return
   end
   open pfile to f then
      read t from f, pid then
         msg = pfile : ' ' : pid : ': ' : len(t) : ' characters'
      end else
         msg = pfile : ' ' : pid : ': not read'
      end
   end else
      msg = pfile : ': this account cannot open it'
   end
   return

draw.all:
   screen clear at 0,ctx<TK.C.YBODY> size ctx<TK.C.W>,ctx<TK.C.BODYH>
   gosub draw.panes
   return

draw.panes:
   r = ''
   call !tklayout('pane', ctx, 'list', r)
   screen box at r<1,1>,r<1,2> size r<1,3>,r<1,4> title 'Notes'
   for i = 1 to r<1,4> - 2
      screen text ids<i> at r<1,1> + 2,r<1,2> + i attr (if i = ci then 'highlight' else 'normal') width r<1,3> - 4
   next i
   call !tklayout('pane', ctx, 'text', r)
   screen box at r<1,1>,r<1,2> size r<1,3>,r<1,4> title 'Text'
   t = ''
   if ci <= n then
      read t from notes.f, ids<ci> else t = ''
   end
   lines = ''
   call !tkwrap(t, r<1,3> - 4, lines)
   for i = 1 to r<1,4> - 2
      screen text lines<i> at r<1,1> + 2,r<1,2> + i width r<1,3> - 4
   next i
   return
end
```

## Two panes and the focus

Both panes are in band 1: `list` in column 1, 40 wide, and `text` in column 2, 97
wide, after a gap of 1 column - 138 in all, the width of the body. `ctx<TK.C.FOCI>`
names the panes that take the focus, each with the name the program gives
`!tkframe`. The frame then marks the box of the pane named in the status line `[*]`
and the other `[-]`. The program moves the focus itself: **Tab** only changes
`pane`. With the record `reading` chosen (**Down** twice):

```
 0   File  Go                                                                                                                  browse  don@zzhd
 1   +- Notes ---------------------------[*]+ +- Text -------------------------------------------------------------------------------------[-]+
 2   | garden                               | | Read the chapter on dictionaries again, then try the examples on a copy of the file: the      |
 3   | phone                                | | conversions, the correlatives and the I-types that call a subroutine, and write down what     |
 4   | reading                              | | each one returns for an empty field, a field with several values, and a value that is not a   |
 5   |                                      | | number.                                                                                       |
 6   |                                      | |                                                                                               |
    (rows 7 to 38 are the same as row 6)
39   +--------------------------------------+ +-----------------------------------------------------------------------------------------------+
40  [Notes]  3 note(s)
41  --------------------------------------------------------------------------------------------------------------------------------------------
42  ^Q quit  Tab next box  ^P jump  ^R record  ^F any file  Esc menu
```

After **Tab** the marks and the status line follow the focus:

```
 1   +- Notes ---------------------------[-]+ +- Text -------------------------------------------------------------------------------------[*]+
40  [Text]  3 note(s)
```

The chosen row of the list is drawn with the style `highlight`, in reverse video,
which a copy as text cannot show.

## Text that fits its pane

`!tkwrap(t, r<1,3> - 4, lines)` cut the record into the lines above, each ending at
the last space that keeps it within the 93 columns inside the box. Without it,
`screen text ... width` would cut the text at the box's edge, as the list of the third
example does.

## A bigger window

The program asks `!tklayout` for each pane's place every time it draws, so it needs
nothing more to use a bigger window. At 180 by 55 the body was 178 by 51. Both panes
stretch down, so both took the 12 extra rows; only `text` stretches across, so it
took the 40 extra columns and `list` stayed 40 wide:

```
 0   File  Go                                                                                                                                                          browse  don@zzhd
 1   +- Notes ---------------------------[*]+ +- Text -----------------------------------------------------------------------------------------------------------------------------[-]+
 2   | garden                               | | Tomatoes, beans and the old roses by the fence.                                                                                       |
 3   | phone                                | |                                                                                                                                       |
 4   | reading                              | |                                                                                                                                       |
 5   |                                      | |                                                                                                                                       |
    (rows 6 to 50 are the same as row 5)
51   +--------------------------------------+ +---------------------------------------------------------------------------------------------------------------------------------------+
52  [Notes]  3 note(s)
53  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
54  ^Q quit  Tab next box  ^P jump  ^R record  ^F any file  Esc menu
```

## The pickers

**Ctrl-P**, **Ctrl-R** and **Ctrl-F** open the three pickers; [The Pickers](05a-the-pickers.html)
shows each one.

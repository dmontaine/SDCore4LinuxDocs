Title: SD VOC - A Private Vocabulary and Your Own Record Types
Subtitle: The two optional VOC records $private.voc and $voc.parser: where SD looks for a command that the VOC does not hold, and what it does with a VOC record whose type it does not know.

This page continues [SD VOC - Using and Managing the
VOC](32a-sd-voc-in-use.html). Both records described here are ordinary VOC
records of type `X`, and neither is in a stock VOC: an account has them only
if somebody wrote them. SD reads `$private.voc` each time it looks up a
command, and `$voc.parser` once, when the session signs on.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case. In the tables, *italics* mark something you supply.

> **Every example on this page was run** on a private SD built from the
> Dev tip of 18 October 2026, in ordinary sessions (an account is not the
> administrator's). The names `zzpv`, `zzhello` and the like are the ones the
> runs used.

## Where a command is looked for

The first word of a line is the command. The command processor looks for it
in this order, and stops at the first place that has it:

1. **The account's VOC.** The word as typed, then in lower case, then in
   upper case. **There is no hyphen form** (it was removed in 1.2-0):
   `zz-vdot` does not find a VOC record called `zz.vdot`.
2. **The private vocabulary**, if the VOC has `$private.voc`. The word as
   typed, then in lower case, then in upper case; `zz-dot` does not find a
   private record called `zz.dot` either.
3. **The private catalogue and then the global one**, as page 32a describes.
4. Otherwise `xx is not in your VOC`.

So the private vocabulary is searched only for a word that is in **no** VOC
record, and it is searched **before** the catalogue.

## `$private.voc`: a second vocabulary in a file of your own

```
001  X
002  filename
```

Field 1 is `X` (a capital or a small `x`; anything after the first letter is a
comment). Field 2 is the name of a file, and the file is laid out as the VOC
is: each record's id is a command word and its contents are a VOC record of
any type. A verb, a sentence and a paragraph all work.

```
:create.file zzpv
```

A program that makes the file, puts three records in it and points the VOC at
it (the writes to the VOC need the switch described under *Who can make
them*, below):

```
open 'zzpv' to f else stop
write 'PA':@fm:'display paragraph from the private vocabulary' on f, 'zzhello'
write 'S':@fm:'display sentence from the private vocabulary' on f, 'zzsent'
write 'PA':@fm:'display private vocabulary copy' on f, 'zzdup'
open 'voc' to v else stop
write 'PA':@fm:'display the VOC copy of zzdup' on v, 'zzdup'
write 'X':@fm:'zzpv' on v, '$private.voc'
```

Before the `$private.voc` record is written:

```
:zzhello
zzhello is not in your VOC
```

After it:

```
:zzhello
paragraph from the private vocabulary
:ZZHELLO
paragraph from the private vocabulary
:zzsent
sentence from the private vocabulary
:zzdup
the VOC copy of zzdup
```

`zzdup` is in both, and the VOC's record is the one that ran. **A private
vocabulary can add a command. It can never replace one that the VOC holds.**
It can replace one that exists only in a catalogue: with a program `zzcatprog`
catalogued in the private catalogue and a private record of the same name,

```
:zzcatprog
private vocabulary beats the catalogue
```

ran the private record, not the program.

### What else to know

* **The record is read every time.** SD reads `$private.voc` and opens the
  file for each command that the VOC does not hold, then closes it. Writing,
  changing or deleting the record takes effect on the next command, in the
  same session.
* **A record that does not work is ignored without a message.** The command is
  then reported as not in the VOC. That is what happens when field 1 is not
  `X` (a record of type `F` was tried), when field 2 is empty, when the name
  is in no VOC record, and when the name leads to a place the account may not
  open (an `F` record naming `/etc`, in an account that does not hold `os-on`;
  the administrator's own session does open it).
* **The file is opened as any file name is,** under the same rules: a name
  in the account's VOC (here `zzpv`, which `create.file` put there), and
  failing that a file of the shared account (see below).
* **A record found there is run as a VOC record is.** A `V` record in mode
  `ca` that names a catalogued program runs it. A `V` record in mode `os` is
  refused for an account without the shell switch (`xx is not permitted to use
  the operating system shell`), exactly as the same record in the VOC would
  be. A `K` record with no command in it is answered `'zzkey' is not valid for
  this usage`.

## `$voc.parser`: handling a record type SD does not know

```
001  X
002  type code {value mark type code ...}
003  handler {value mark handler ...}
```

Field 2 is a list of record type codes and field 3 a list of the names of
catalogued subroutines, paired by position. Field 1 must be a capital `X`: a
small `x` in this record is ignored.

When a command word has a record (in the VOC, in the private vocabulary, or
made from a catalogued program, which SD treats as a `V` record), SD first
runs down this list, and only then applies its own rules for `V`, `PA`, `S`,
`K` and the rest. For each entry in order:

* The record's field 1 and the type code are both put in upper case, and the
  record matches if its field 1 **begins** with the type code. The match is a
  prefix: `zz` matches `zz lower case type`, and `p` would match every record
  of type `PA`, `PQ` or `PH`.
* If the handler is catalogued, SD calls it as
  `call @handler(verb, record)` and the command is finished. `verb` is the
  command word and `record` is the whole VOC record. The whole command line is
  in `@sentence`.
* If the handler is **not** catalogued, SD says nothing and goes on to the
  next entry, and finally to its own rules.

The first matching entry whose handler is catalogued wins.

A handler is a catalogued subroutine that takes two arguments:

```
subroutine zzhandler(verb, rec)
   crt 'handler verb=':verb:' type=':rec<1>:' f2=':rec<2>:' f3=':rec<3>:' sentence=':@sentence
return
end
```

It was compiled and catalogued (`basic bp zzhandler`, then `catalog bp
zzhandler`). The VOC then held `$voc.parser` with field 1 `X`, field 2 `ZZ`
and field 3 `zzhandler`, and a record `zzcust` whose field 1 is `ZZ custom
record type` and whose fields 2 and 3 are `alpha` and `beta`. A new session
gave:

```
:zzcust a b
handler verb=zzcust type=ZZ custom record type f2=alpha f3=beta sentence=zzcust a b
```

Without the `$voc.parser` record the same line was `'zzcust' is not valid
for this usage`. A handler with the wrong number of arguments ends the
command with `Argument count mismatch calling zzhandler (Call=2, subr=1)`
and the number of a line in the command processor (the session carries on).

### When the list is read

* **At sign-on, once.** A record written during a session changes nothing in
  that session: `zzcust` was still `not valid for this usage` after the
  record had been written, and was handled in the next session.
* **`logto` does not read the new account's record.** A session that signed
  on to an account with a `$voc.parser` record kept that list after `logto` to
  an account without one, and was handled by it there. A session that signed
  on to an account without the record did not use the record of the account
  it went to.

### Things this can do to a whole session

Because it runs before SD's own rules, an entry can take over commands that
already work:

* A type code of `v` hands **every verb** to the handler, including `date` and
  `off`, and SD's own code for it does not run. `date` printed only the
  handler's line.
* A type code of `p` hands every paragraph; one of `k`, every keyword record
  (`display` was handed over, `date` still ran).
* **A blank type code matches every record.** A list whose second value is
  empty (`ZZ`, a value mark, nothing) sends `term`, `run` and `off` to the
  handler as well, the administrator's session included.

A handler that only prints something leaves the commands it was given
undone. Because `run` and `off` are commands too, **the record cannot then be
corrected from inside the account.** It was removed from outside, by the
administrator signed on to the `sdsys` account running an ordinary program
that opened the account's `voc` by its path and deleted `$voc.parser`; after
that the account worked again. Test a new entry on an account you can reach
from outside before you put it on one you cannot.

## Who can make them

Both records are changes to a VOC, so writing, changing or deleting either
needs the **`voc.edit`** switch, which SDSYS gives with `modify.account`
*name* `voc-on`, or SDSYS itself. Without it a program's `write` is refused
with status 3035, and a program with no `on error` stops with `The VOC can
only be changed by an account that has voc.edit`. Reading is never stopped.

What the switch covers is the **VOC**, and only that:

* **The private vocabulary's file is not covered.** The switch looks at the
  name of the file being written, and a file called `zzpv` is an ordinary data
  file. Once the VOC points at it, any session that can write the file, in an
  account with no edit switch at all, can add commands to it and replace
  commands in it. This was run: an account with all three switches off wrote
  a new record and replaced `zzhello`, and both ran. It still cannot touch the
  VOC's own records, so it cannot replace a VOC command.
* **A file in the shared account.** `$private.voc` may name a file of the
  shared account, found by name by an account that holds `shared.read` (on
  unless SDSYS turns it off). Such an account ran `zzshcmd` from it; an
  account with `shared.read` off did not find the file. The first account's
  write to that file was refused with status 3035, because `shared.write` is
  off unless SDSYS turns it on. So a private vocabulary kept there can be changed only by SDSYS and by
  accounts SDSYS has given `shared.write`. The shared account's own VOC is not searched for
  commands; only this pointer reaches its files.
* **A handler is a catalogued program,** and cataloguing needs `bp.edit`
  (`Programs can only be compiled or catalogued by an account that has
  bp.edit`). `voc.edit` alone is enough to switch on a handler that is
  already catalogued: an account with `voc-on` and no `bp-on` wrote the record
  and the handler ran.
* **Neither record is in a stock VOC.** Nothing SD ships writes them.

## See also

[SD VOC - Structure and Usage](32-sd-voc-structure-and-usage.html) ·
[SD VOC - Using and Managing the VOC](32a-sd-voc-in-use.html) ·
[SD TCL - Programs and the Catalogue](24-sd-tcl-programs-and-the-catalogue.html).

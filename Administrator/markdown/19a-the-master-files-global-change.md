Title: The Master Files: Global Changes
Subtitle: G, the change of every row shown, and U to put it back.

This page continues [The Master Files](19-the-master-files.html).

### A global change of every row shown: `G`, and `U` to put it back

**`G` makes one change to every row the page shows, in every account the rows come from.** The rows
are exactly those on the screen: the hits of a find (`F`, every account) or the entries a filter
(`/`) keeps in the account under the cursor. A filter or a find must be on, and a list cut short at
the page's limit is refused (narrow it until every row is shown). `G` asks what to change **on one form, titled *Global
change*, with the button *Preview***; Tab moves between the fields, and a refusal is said on the
form, which stays open until every answer passes or you cancel:

- **VOC entries and dictionary items**: four fields. *Field* is its number (1 to 500) or, for a
  dictionary item, the word `heading` (field 4 of a D, I, E or L item; an item of another type is
  refused for having no heading). *Change* is a choice, `replace` or `set`. With `replace`,
  *Text to replace* is taken out of the field and *With, or the value* goes in its place (empty
  takes the text out); with `set`, the field becomes *With, or the value* (empty empties it) and
  *Text to replace* is not used. A text to replace may not be empty.
- **Field 1 is the type of the record** (a VOC entry's V, F, Q, PA ...; a dictionary item's D, I,
  PH ...), and changing it turns a verb or a pointer into something else. `G` therefore changes it
  on **one record only**: when more than one record is shown the form refuses it, before the preview
  (`field 1 is the type of the record: G changes it on one record only, and 3 are shown ...`), and
  on a single record the box carries a **WARNING** line with the old and the new type (`"X" ->
  "PA"`). Cancel is still the default, and `U` puts field 1 back like any other field (field 1 is excluded from batch actions and allowed on a single item with a confirm warning).
- **Programs**: two fields only, *Text to replace* and *Replace it with*, for the source of every
  program shown (an empty second text takes the first out). Each program changed is then
  compiled again **in its own account** through `run.in` (as `C` does), and is counted as failed
  when the compiler does not say it compiled.

The texts are printable characters only, up to 120 of them. **One box** (titled *Update these
records?*) then shows the change, and each account with how many records would change, the first
ids, how many are as they are already and how many would be refused, with the first reasons. **Run
or Cancel is all it asks** (Cancel is the default): no name or count is typed. This is looser than
`D`, which asks for the id; that is how the page is delivered.

Run writes **account by account**. Each account is judged again (it must still be in the register,
and an SDSYS session in the `relog` state is refused for it, as for `E`), and each file by **the
pointer rule** before it is opened for writing: the path, what the kernel opened, and the two parts
of a hashed file must lie inside the account (a program's own file too). A row whose file lies
outside the account it is listed under - the dictionary of `@SDSYS/voc.dic`, another account's file
reached through a pointer, a path written with `..`, a link - is **refused**, in the box and again
at the write; its target is never written. Each record is read with its update lock (a record
another session holds is refused) and must still be what the box read (one changed since is
refused). **A refusal or a failure is counted and the run goes on**, in that account and in the
next. A box then shows, for each account, how many records were changed, refused and failed, with
the first reasons; the audit trail gets one line per account:
`master global account=ze1 kind=dict changed=2 refused=3 failed=0` (`kind=voc`, `dict` or `bp`).

**`U` puts the last global change back.** Before each record is written, the record as it was is
kept in `&entries.undo&`, a file of SDSYS's own account; the first time, a box shows the command
that makes it (`create.file &entries.undo&`) and nothing is changed unless it is made. It holds the
last run only: a new run replaces it. `U` (offered while there is a run that has not been put back)
shows a box titled *Put these records back?* (Run or Cancel) and then puts back each record **only
if it is still exactly what the run wrote**; a record edited since is left as it is and counted,
never overwritten, and so is one that has gone or that another session holds. The pointer rule is
asked again, and a program put back is compiled again in its account. The audit trail gets
`entries undo account=ze1 records=2` for each account. When nothing was held, refused or failed the
run is marked put back and `U` is no longer offered.

The AI line of the page is not offered `G` or `U`.

## Continued in

[run.in](19b-run-in.html) — run.in.

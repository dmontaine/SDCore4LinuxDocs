Title: SDNet: The Files-only Route
Subtitle: The files-only route on a server and its write group.

This page continues [SDNet: Your Login on a Server](12b-sdnet-logins.html).

## The files-only route on a server

This section is about the server being **reached**, the one whose administrator is
giving somebody a login. (The same machine is that server for others and the client
for its own people, so both halves can be yours.)

The way to log in to a server's API is membership of the Linux
group `sdapi`, which gives everything the API offers: execute commands, call
subroutines, enter other accounts with `logto`, work with sequential files and files.
A stored SDNet login on that route, taken from a machine, would give whoever took it
all of that. **So there is a second route, the Linux group `sdfiles`: a login that is
in `sdusers` and `sdfiles` and not in `sdapi` is let in "files only".** The rest of
the rules, the table of what is allowed and refused and why, the words and the
messages are in [Accounts and Security](01-accounts-and-security-4-shared-and-files-only.html#the-files-only-route-files-on-and-files-off); in short:

- **`sdapi` wins.** A remote user who is in both groups has the whole API.
- **A user in neither group is refused**, as before. Both groups are empty for a new
  account until the administrator of that server adds the person
  (`modify.account` *name* `files-on`, or `files-on` when the account is made).
- A files-only session may open and close files; read records; select, read the next
  id and read and save lists; ask about locks and release them; use indices; ask for
  file information; and set its account **once**, which is the entry after login.
  **With the write group as well** (next section) it may also write and delete
  records, take record and file locks (and read with a lock), and clear a file.
  **It may not** call a
  subroutine, execute a command or answer its prompts, enter another account,
  use sequential files, read variables, run `system()`, `trans()` or an evaluation or
  conversion, run a transaction, or open an SDNet file on a third server. Any other
  request, and any request number SD does not know, is refused: the table
  is an allow list.
- A refused request is not carried out. It is answered with "This login is for files
  only: request *n* is not allowed" and written to the audit trail; the connection
  stays up.
- Everything else about the session is as for any other API login: the account has to
  be entered, its switches (OS access, the edit switches, NET) apply, `SDCLIENT` still
  applies, and `sdsys` is never made files-only.
- **It is a read-only route unless the remote user is also in `sdfileswrite`** (next
  section). The table above is what `sdfiles` alone allows: the writes, deletes, locks
  and clear are in it only for a login that also has the write group.

### The write group: `sdfileswrite`

**A login on the target server may change something only if the target's administrator
allows it.** That is the rule, and it is why
a *write* server definition on a client is no longer enough by itself: the definition
says what the client is willing to do, the write group says what the target is willing
to let that login do.

- The Linux group **`sdfileswrite`** is made, empty, by the installer beside `sdfiles`.
  SDSYS gives it to one person at a time on the server being reached:
  `modify.account` *name* `files-write-on`, taken away with `files-write-off`, and
  `files-write-on` after `files-on` in `create.account user`. **It is off for a new
  account.**
- **`files-write-on` needs `files-on` first.** The group alone gives nothing (the login
  route is `sdfiles`), so for a person who is not in `sdfiles` it is refused: "Account
  *name* does not have files access, so it cannot be given files-write: use files-on
  first" (message 11523). `create.account user` *name* `files-write-on` without `files-on` is refused
  the same way before anything is made. A group or other account is refused as for
  `files-on`.
- **`files-off` takes the person out of `sdfileswrite` too, and first**, so a later
  `files-on` does not hand the write back without you saying so. It removes the write
  group, reads it back, then removes `sdfiles` and reads that back, and it does the work
  for a person who is in only one of the two: a person who is in `sdfileswrite` and
  not in `sdfiles` (a removal that stopped half way, or a change made by hand) is
  taken out of it, so a membership left in place cannot become write access at the
  next `files-on`. If a
  removal fails the command says so ("Unable to change remote access for *name*,
  status: *n*") and stops: a failure of the write group's removal leaves the person
  exactly as they were, and a failure of the second removal leaves them in `sdfiles`
  alone, with read access and never write access without read. **In that second case the
  command says what did happen before it says it failed**: it prints
  `Account fred has files-write no` and writes the audit line
  `modify.account files-write-off account=fred` for the removal that worked (the audit line
  for `files-off` itself is written only when both removals worked), so the screen and the
  trail agree with `/etc/group`. When the write group
  went and the command went on to succeed, the same line `Account fred has files-write no`
  comes before `Account fred has files no`.
  `files-on` removes a leftover `sdfileswrite` membership **before** it adds `sdfiles`,
  and stops with the same failure message if it cannot; if the leftover went and the add
  of `sdfiles` then fails, the person is left in neither group, and the command says so in
  the same way (`files-write no` line, `files-write-off` audit line, then the failure).
- **What it changes.** Without it a files-only login is refused: write (16), writeu (17),
  delete (18), deleteu (19), lock record (30), clearfile (31), file lock (32) and file
  unlock (33), a test of a lock (34, which is what `RECORDLOCKED()` sends), the four locking reads (7 to 10), and a `READV` with a lock flag. They are
  answered "This login cannot change or lock files here: ask the administrator for
  files-write-on (request *n*)" (message 11521) and **nothing is carried out**. Reads, selects, `READV` without
  a lock, file information, the indices and `RELEASE` still work. (A test of a lock names the
  holder by his user number on this server, which a login that cannot lock has no business
  with.)
- **`sdapi` is not touched.** A remote user in `sdapi` has the whole API as before, with
  or without the write group, and `sdsys` is never made files-only.
- **The refusal is in the audit trail of the target**, in lower case:
  `api refused request=16 route=sdfiles write=off admin=off user=name`, and a login by this route is
  written `api login route=sdfiles write=on admin=off user=name` (`write=off` for a login without the
  group; the `admin=` word is the administration group, next section). **The person at the
  client is told why**: a program that does not trap the error with `ON ERROR` stops with
  message 11500, "Server *name* answered *write* with an error: This login cannot change or lock files
  here: ask the administrator for files-write-on (request 16)". (The client shows the
  text of any `ON ERROR` reply that has one, cut at 100 characters; a reply with no text
  still shows "status *n*".) A
  program that traps the error with `ON ERROR` sees `STATUS()` 7000, as before. The audit
  trail on the target also has the request number.
- **The group is read at login**, from `/etc/group`, so a change takes effect at the
  person's **next** login on that server, and a refusal to read the group file refuses
  the login with its own reason.
- **A machine without the groups has neither** until the installer is run again; until then
  `files-on` and `files-write-on` say that the group does not exist and change nothing, and
  `create.account` refuses to make a user it was asked to give the route.
- **A server defined `write` on a client** writes only when the remote user has been
  given the group on the target (one `modify.account` word there). Reads are unaffected.

## Continued in

[SDNet: The Administration Group and Remote Files, Read
Only](12d-sdnet-administration-group-and-read-only-files.html) — the
sdfilesadmin group and remote files, read only.

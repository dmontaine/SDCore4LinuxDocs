Title: Encrypting the data SD keeps on disk
Subtitle: Putting SD's four data trees on an encrypted volume, what that protects, what it does not, and how the machine must be unlocked at boot.

This page is about the bottom layer in the table on the encryption page: the
disk. SD itself is unchanged by it. The encryption is done by the operating
system, to the volume the SD directories live on. The encryption page explains
the other two layers, which are the application's.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case.

> **The recipe below was run, not only written.** It was witnessed on a Debian
> 13 virtual machine with SD Core for Linux built from the `Dev` branch. The
> first section says exactly what was and was not witnessed.

## The short version

**Encrypt the volume, then move the four data trees onto it.** A stolen or
discarded disk, or a backup copied off the machine, then holds ciphertext.
**It protects nothing once the volume is open.** While SD is running on an
open volume, anyone who can log in as root, as the `sdsys` administrator or as
an SD user reads the data as plaintext, and so does anyone who mounts it.

Two things must be set up for this to hold, and neither is done by the
installer:

1. SD must not start on the bare directories when the volume is absent. An
   ordering drop-in does this (see below).
2. Swap must be encrypted or switched off, because SD's shared memory can be
   paged out to it.

## Where SD keeps its data

| Path | What is there |
|---|---|
| `/usr/local/sdsys` | the register (`accounts/`), `$cred/`, the audit file, the error log, `dumps/` and the binaries |
| `/home/sd` | `user_accounts` and `group_accounts`, the account files |
| `/var/lib/sd-net` | per-user, per-server SDNet credentials, mode 600 |
| `/etc/sd-tls` | `api.pem`, the TLS private key, root-owned |

**`/etc/sd.conf` stays plaintext.** It holds paths only, and it is read before
any of the volume is mounted. Keep it on the root filesystem.

The shared memory segment (`0x53434c01` in the witnessed install) is in RAM and
is not a file. It is recreated each time SD starts.

**The sort work area is not under SDSYS.** SD's default places are
`TEMPDIR`, which is `$TMP` or `/tmp`, and `SORTWORK`, which follows `TEMPDIR`.
The sort files are named `~SDS<user>.<n>`. A sort of 150,000 keys under
default settings put the work files in `/tmp`, and one of them held the
plaintext keys. So the sort area must be moved onto the volume as well:

```
# in /etc/sd.conf
SORTWORK=/home/sd/sortwork
```

Create the directory on the volume first, with the sticky bit set:

```bash
sudo install -d -m 1777 /home/sd/sortwork
```

If that directory does not exist when SD starts, SD falls back silently to
`TEMPDIR`, which is `/tmp`. The ordering drop-in below stops SD starting
before the volume is open, and so keeps this from happening on a normal boot.
`TEMPDIR` itself, for SD's other temporary files, was not tested and is not
covered by this page.

**Backups.** `BACKUPDIR` is not set by default. `BACKUP.ACCOUNT` writes plain
zip files wherever `BACKUPDIR` points. A copy taken off the machine is not
encrypted by this recipe unless the backup directory is on the encrypted
volume, and even then only until the file leaves it.

## Method one: LUKS2 on a volume, the four trees bound over it

This is the method that was witnessed for the whole data set, end to end.

### Install the tools

```bash
sudo apt-get install -y cryptsetup systemd-cryptsetup
```

`cryptsetup` is in `/usr/sbin`, which is not on an ordinary user's path, so
run it as `sudo /usr/sbin/cryptsetup`. On Debian 13 the boot-time generator
`systemd-cryptsetup@.service` comes from the separate `systemd-cryptsetup`
package. With only `cryptsetup` installed, the boot unit does not exist and the
start fails.

### Create the container

```bash
sudo modprobe loop dm_crypt
truncate -s 300M /var/tmp/l1-luks.img
printf '%s' "PASSPHRASE" | sudo /usr/sbin/cryptsetup luksFormat --type luks2 -q --key-file=- /var/tmp/l1-luks.img
printf '%s' "PASSPHRASE" | sudo /usr/sbin/cryptsetup open --key-file=- /var/tmp/l1-luks.img l1crypt
sudo mkfs.ext4 -q -L sdl1luks /dev/mapper/l1crypt
sudo mkdir -p /mnt/l1-luks
sudo mount /dev/mapper/l1crypt /mnt/l1-luks
```

The witnessed container used aes-xts-plain64 with a 512-bit key, an argon2id
keyslot and 4096-byte sectors. In a real installation the image would be sized
to the data, and it would live on a disk the administrator chooses, not in
`/var/tmp`. The 300 MB size is the test's.

Replace `PASSPHRASE` with the passphrase. Do not write it into a script or a
history file.

### Move the data, in order

Stop SD first. Do not copy the trees while SD is running.

```bash
sudo systemctl stop sd.service
for d in usr/local/sdsys home/sd var/lib/sd-net etc/sd-tls; do
  sudo mkdir -p /mnt/l1-luks/$d
  sudo rsync -aHAX --numeric-ids /$d/ /mnt/l1-luks/$d/
done
for d in usr/local/sdsys home/sd var/lib/sd-net etc/sd-tls; do
  sudo mount --bind /mnt/l1-luks/$d /$d
done
sudo systemctl start sd.service
```

`rsync -aHAX --numeric-ids` keeps ownership, permissions, hard links, ACLs and
extended attributes. The witness checked that `sdsys:sdusers` and the root-only
`/etc/sd-tls` came across unchanged.

**The old plaintext is still there.** The bind mounts hide the original
directories but do not remove them. They remain on the root disk under the
mount points. Deleting files does not guarantee that their blocks are erased
on ext4 or on an SSD. The cleanest order is to encrypt before any data enters
the system, which means a fresh install. Otherwise treat the old blocks of the
disk as exposed.

### Tear down, in order

Teardown is the reverse of the start, and stopping the service releases the
shared memory.

```bash
sudo systemctl stop sd.service
for d in etc/sd-tls var/lib/sd-net home/sd usr/local/sdsys; do
  sudo umount /$d
done
sudo umount /mnt/l1-luks
sudo /usr/sbin/cryptsetup close l1crypt
sync
```

### What the raw container showed

After a record was written through SD and the volume closed, the raw image was
searched for the text of the record, the record id, the account path and the
SDSYS path. Every search returned 0. The same flow on an unencrypted ext4 image
returned matches for each.

```bash
sudo grep -a -c PLAINTEXT-MARKER-ZEBRA-4417 /var/tmp/l1-luks.img
sudo strings -a /var/tmp/l1-luks.img | grep -c PLAINTEXT-MARKER-ZEBRA-4417
```

`file` describes the image as "LUKS encrypted file, ver 2". The text search is
evidence about the bytes that were searched, not a proof about every byte.

## Unlock at boot

The volume must be opened and mounted before `sd.service` starts, and SD must
not start if it cannot be. Two parts do this. Both were witnessed, and neither
is shipped by the installer.

### The ordering drop-in

```ini
# /etc/systemd/system/sd.service.d/encrypted-data.conf
[Unit]
RequiresMountsFor=/usr/local/sdsys /home/sd /var/lib/sd-net /etc/sd-tls
```

With the four bind mounts in `/etc/fstab`, each marked to wait for the volume:

```
/dev/mapper/l1crypt /mnt/l1-luks ext4 noauto,nofail,x-systemd.requires=systemd-cryptsetup@l1crypt.service 0 0
/mnt/l1-luks/usr/local/sdsys /usr/local/sdsys none bind,noauto,nofail,x-systemd.requires-mounts-for=/mnt/l1-luks 0 0
/mnt/l1-luks/home/sd /home/sd none bind,noauto,nofail,x-systemd.requires-mounts-for=/mnt/l1-luks 0 0
/mnt/l1-luks/var/lib/sd-net /var/lib/sd-net none bind,noauto,nofail,x-systemd.requires-mounts-for=/mnt/l1-luks 0 0
/mnt/l1-luks/etc/sd-tls /etc/sd-tls none bind,noauto,nofail,x-systemd.requires-mounts-for=/mnt/l1-luks 0 0
```

Then:

```bash
sudo systemctl daemon-reload
systemctl list-dependencies sd.service
systemctl show -p RequiresMountsFor sd.service
```

The first command lists the four `.mount` units. The second echoes the four
paths.

**Without the drop-in, SD starts on the wrong disk.** Witnessed: with the
volume not mounted and no ordering, `systemctl start sd.service` reported
`active`, and SD ran on the unencrypted directories underneath the mount
points. `COUNT l1test` printed "File not found", and anything written then
would have landed in plaintext. With the drop-in and the fstab entries the
same start failed with "A dependency job for sd.service failed", return code
1, and SD stayed down.

### Unlock by keyfile

```
# /etc/crypttab
l1crypt /var/tmp/l1-luks.img /var/tmp/l1-keyfile luks,nofail
```

With a keyfile, `systemctl start sd.service` from a fully locked state opened
the container, mounted it, bound the four paths and started SD. The record was
readable at once.

**The trade-off, stated plainly.** A keyfile on the same machine as the
container gives no protection against anyone who can read that machine's root
disk. It protects only a container that is taken away on its own, without the
machine. For the keyfile to mean anything it must live on a second device, or
be released by a TPM, and nothing of that kind was built or tested. The
witnessed keyfile was in `/var/tmp`, and that is a test arrangement, not a
recommendation.

### Unlock by passphrase

```
# /etc/crypttab
l1crypt /var/tmp/l1-luks.img none luks,nofail,timeout=90s,tries=1
```

With the key field `none`, the boot waits for a passphrase. The
witness answered the question through systemd's password-agent protocol:

```bash
sudo systemctl start sd.service --no-block
# the question is in /run/systemd/ask-password/ask.*; its Socket= line gives the reply path
printf '%s' "PASSPHRASE" | sudo /usr/lib/systemd/systemd-reply-password 1 SOCKET
```

SD came up and read the record. **A console or Plymouth prompt was not
exercised,** and no reboot was performed. The ordering in this section was
shown by starting the service from a locked state and by the dependency list,
not by a real boot. With nobody answering and `timeout=5s`, the start failed
closed, as above.

**The trade-off.** A passphrase is typed at every boot, so a machine that
restarts unattended stays down until someone unlocks it, and a
`WantedBy=default.target` service with a failed dependency leaves SD down
after boot until someone runs `systemctl start sd.service`. That is the
intended behaviour for stolen-disk protection. It is not a convenience.

## Method two: fscrypt on a dedicated ext4 volume

**fscrypt was witnessed only on a separate ext4 image, not on the root
filesystem of the test machine.** The root filesystem did not have the
`encrypt` feature. It can be made with `tune2fs -O encrypt`, but that cannot be
undone with `tune2fs`, so the witness did not change the root filesystem. To
use fscrypt for the data, the volume must be made with `mkfs.ext4 -O encrypt`
from the start.

```bash
truncate -s 300M /var/tmp/l1-fsc.img
sudo losetup -f --show /var/tmp/l1-fsc.img
sudo mkfs.ext4 -q -O encrypt -L sdl1fsc /dev/loopN
sudo mount /dev/loopN /mnt/l1-fsc
sudo fscrypt setup --quiet --force
sudo fscrypt setup /mnt/l1-fsc --quiet
sudo mkdir /mnt/l1-fsc/sdenc
printf '%s\n' "PASSPHRASE" | sudo fscrypt encrypt /mnt/l1-fsc/sdenc --source=custom_passphrase --name=sdenc-prot --quiet
```

`/dev/loopN` is the loop device `losetup` reported. Replace `PASSPHRASE` as
before.

**Do not install `libpam-fscrypt`.** It enables itself in `/etc/pam.d/common-auth`,
`common-password` and `common-session` by default. The witness removed it and
checked that no fscrypt line remained in PAM. Install only the `fscrypt`
package.

`fscrypt setup` writes `/etc/fscrypt.conf` and a `/.fscrypt` directory on the
root filesystem. Those are part of the set-up and are not on the volume.

The witnessed status after encryption was policy version 2, contents
`AES_256_XTS`, filenames `AES_256_CTS`, and `Unlocked: Yes`.

The four trees were copied into `sdenc/` under the same relative paths, bound
over their usual places, and SD was started as in method one. Then, with SD
stopped and the binds removed:

```bash
sudo fscrypt lock /mnt/l1-fsc/sdenc
```

While locked, `ls` showed encrypted names, and the raw image held no record
text, no `l1test`, no `user_accounts` and no `sdsys`. Unlock with:

```bash
printf '%s\n' "PASSPHRASE" | sudo fscrypt unlock /mnt/l1-fsc/sdenc --quiet
```

fscrypt hides contents and file names only. File sizes, owners, modes, the
directory structure, timestamps and the top-level unencrypted name (here
`sdenc`) remain visible in the raw image. The boot ordering and unlock
arrangements in the section above were not witnessed for fscrypt. Method one
is the one whose boot path was tested.

## Method and what is not covered

| Point | Status |
|---|---|
| LUKS2 container, four trees, record readable after reopen | witnessed |
| Raw image has no record text or SD paths | witnessed (text search) |
| Wrong passphrase refused | witnessed |
| Keyfile added as a second slot and used to open | witnessed |
| Ordering drop-in: start fails when the volume is absent | witnessed |
| Keyfile unlock at start | witnessed |
| Passphrase unlock through the password-agent protocol | witnessed, but not through a console or Plymouth prompt |
| Real reboot | not performed |
| fscrypt on a dedicated ext4 image | witnessed |
| fscrypt on the root filesystem | not witnessed, and not possible without re-making the filesystem |
| Sort work area moved to `SORTWORK` on the volume | witnessed |
| `TEMPDIR` moved onto the volume | not tested |
| SDNet and the API client on the volume | not exercised |
| Swap encrypted or disabled | not witnessed. The test machine's swap was unencrypted and unused |
| Backup directory on the volume | not witnessed |

The 1 GiB argon2id memory for the keyslot is the cryptsetup default, so
unlocking a passphrase keyslot needs about 1 GiB of free memory.

## What to do, in order

1. Decide where the volume lives, and keep its passphrase or keyfile where a
   stolen machine does not give it away.
2. Set `SORTWORK` in `/etc/sd.conf` to a directory on the volume, created with
   mode 1777.
3. With SD stopped, create the container and move the four trees as above.
4. Write the ordering drop-in and the fstab and crypttab entries. Check them
   with `systemctl list-dependencies sd.service` and
   `systemctl show -p RequiresMountsFor sd.service`.
5. Encrypt or switch off swap, and decide the backup directory's location.
6. Test a start from a locked state before trusting it. The start must fail.

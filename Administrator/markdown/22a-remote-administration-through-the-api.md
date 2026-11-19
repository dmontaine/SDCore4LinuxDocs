Title: Remote Administration through the API
Subtitle: How SDSYS, the administrator, can sign in through the API from another computer, for chosen addresses; how to open and shut it; what it gives; the risk; and what it refuses.

**SDSYS can sign in through the API from another computer, but only after you have opened that
door, and only from the addresses you name.** As delivered the door is shut. The installer does
not ask about it. An upgrade that keeps the configuration leaves it as it was; a full uninstall
removes it. It is meant for an administration program on another computer, such as an API
administration client, that signs in as SDSYS.

**Open it with care: with the door open, nothing but `sdsys`'s SD password stands between those
addresses and the administrator.** It is the password the installer called "sdsys's SD password",
not the Linux one. Use a long password that is used nowhere else, name the narrowest addresses that
work, and shut the door again when it is not needed.

**What a session gets.** An API session signed in as SDSYS has every right the administrator has,
the same as SDSYS at the computer's own keyboard. An API session into any other account has exactly
that account's rights and nothing more: the API never gives an ordinary account more than it has
elsewhere.

> This document is separate so that it can be withheld. It links to nothing outside the
> administrator set. Where a page in another set is worth naming, it is named in words.

## Opening and shutting the door

Signed in as `sdsys` at the computer, or over ssh if that door is open:

```
remote.sdsys api on address ...
remote.sdsys api on any
remote.sdsys api off
remote.sdsys api
```

| | |
|---|---|
| `api on` *address ...* | opens the door for those addresses, and only those. Up to 32. The list replaces the one before |
| `api on any` | opens it for every address. Only on its own, never in a list |
| `api off` | shuts it again, as delivered |
| `api` | says whether it is open and for which addresses, and changes nothing |
| *(no keyword)* | says how both doors stand, ssh and the API, and changes nothing |

An address is written in one of these forms:

| | |
|---|---|
| `192.168.1.20` | one IPv4 address |
| `2001:db8::20` | one IPv6 address |
| `192.168.1.0/24` | a range: every address whose first 24 bits are those of `192.168.1.0` |
| `fd00:1:2:3::/64` | an IPv6 range |

A range of length 0 (`0.0.0.0/0`, `::/0`) is refused: it would be every address, and the word
`any` is the only way to ask for that. Anything that is not an address or a range is refused before
anything is changed, and so is `any` together with other addresses. SD's API listens on IPv4 only,
so an IPv6 address or range is accepted and kept but no client reaches SD from one.

The same can be done without SD, with root:

```
sudo /usr/local/sbin/sd-elevate sdsys-api on 192.168.1.20
sudo /usr/local/sbin/sd-elevate sdsys-api off
sudo /usr/local/sbin/sd-elevate sdsys-api status
```

**The API must also be open to other computers** for a client to reach it at all: the installer's
question "Allow API access from other computers?", or `remote.api on` later. That opens TCP port
4247 for every account; this door decides whether SDSYS may use it.

## Choosing the addresses

* **An address that never changes** is the tightest choice: the administration computer's own
  address. If it gets its address from DHCP, ask the network's router for a reservation, so that it
  always gets the same one.
* **A range** suits a computer whose address changes inside one network: `192.168.1.0/24` admits
  any address of that network. Every computer in the range can then reach the sign-in, though each
  still needs the password.
* **Travelling** is safest through a VPN into your own network, so that the client arrives from a
  listed range. `any` is there for when a VPN is not possible: with it, anyone who can reach this
  computer's API port, from anywhere on the internet, can try the password.

A client that comes in through a gateway that translates addresses (a home router, a cloud load
balancer) arrives from the gateway's address, not its own; name that one. A refusal says which
address SD saw.

## From this computer

SDSYS may always use the API from this computer, over SD's Unix socket, whatever the door says, and
such a session also has every right of the administrator. It is admitted only when the program at
the other end runs as `sdsys` **and** the computer was logged in as `sdsys`: a program that reached
`sdsys` through `su sdsys` or `sudo -u sdsys` from somebody else's login is refused, exactly as it is
at the terminal. A loopback TCP connection (`127.0.0.1`) is not this way in; it is refused for
SDSYS, because a tunnel ends there and its owner cannot be seen. The administrator can also list
Linux users whose programs on this computer may sign in as SDSYS over the same socket; the list is
empty as delivered (see [Reaching SDSYS from Your Own Login](22b-reaching-sdsys-from-your-own-login.html)).

## A tunnelled connection does not show where it began

An ssh tunnel (port forwarding to the API port) ends on this computer, so what SD sees is an address
of this computer and not the address of the computer the person is sitting at. SD therefore treats
a connection from **any of this computer's own addresses** as coming from this computer: loopback
(`127.0.0.1`, `::1`), and also the computer's own network addresses, read from its interfaces at each
sign-in. Such a connection meets the local door, which SDSYS may use only over the Unix socket, so
it is refused for SDSYS over TCP whatever the list holds. A tunnel aimed at this computer's network
address cannot reach SDSYS's sign-in even if that address, or a range containing it, is in the
list. Listing it does nothing, so name only the addresses of the administration computers.

## What refuses

| SD says | when |
|---|---|
| SDSYS may be reached through the API from another computer only when the administrator has opened it | the door is shut |
| ... only from an address the administrator listed with remote.sdsys api on, and *address* is not one of them | the door is open, but not for that address |
| This session runs as sdsys but the machine was not logged in as sdsys ... | from this computer, through `su` or `sudo -u` |
| SDSYS may use the API only from a process running as the sdsys user on this machine ... | from this computer, by a program that is not `sdsys` |

A wrong password is refused in the same words as for any account, after the same delay.

## What is written down

* Each change of the door: an audit line `remote.sdsys api on from=192.168.1.0/24 status=0` and the
  like, with the addresses you gave and the helper's exit status; the system log has the helper's own
  line.
* Each SDSYS sign-in through the API: `elevation granted reason=sdsys api from=192.168.1.20`, or
  `from=this machine` for the local connection, or `from=this machine user=fred` for a listed
  user's program at the Unix socket ([Reaching SDSYS from Your Own Login](22b-reaching-sdsys-from-your-own-login.html)).
* Each refusal: the reason and the address, in the audit trail.

## What SD changes on the computer

* **`/etc/sdcore/sdsys-api`**: root's, readable by root only. The first line is `on`, and each line
  after it is one address or range, written in its standard form (`192.168.1.99/24` becomes
  `192.168.1.0/24`, an address alone gets `/32` or `/128`). `off` removes the file.
* Nothing else: no firewall rule, no listener and no account is changed by this door.

## What it does not do

* It does not open the API port; `remote.api` does.
* It does not give any account but SDSYS more than its own rights.
* It does not accept a key, a certificate or a second factor: the SD password is the whole of it.
* It does not protect against someone who has the password and an address you listed.

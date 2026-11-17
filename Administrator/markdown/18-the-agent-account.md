Title: Giving an AI Agent an Account
Subtitle: A recipe with no code: a user and an SD account of the agent's own, so that the operating system is the wall.

An AI agent that works on an SD project needs a place to work and a limit on what it can reach. Prompts, tool scopes and promises inside the agent's own software protect against mistakes and against instructions hidden in the data it reads. **They do not stop an agent that holds a person's ssh key**: with that key it can open an interactive `sd` as that person and do whatever the person can. The wall that holds is the operating system's, and this recipe is how to build it from what SD already has.

> **The agent is never you.** Do not give it your ssh key, your password, a shared password or a terminal that is already signed in.

The full recipe is `agent-pack/recipe/agent-account.md` in the SD Core for Linux source repository, with a template for the project's `CLAUDE.md` and a Claude Code skill that carries the SD knowledge (see *SD and AI Agents* in the User documentation). The installer puts the guide and the knowledge pack of the installed version under `/usr/local/sdsys/agent-pack/` (text, owned by `sdsys`, writable by no SD user). The agent's own account cannot read that path, since a path outside an account needs `os-on` and this recipe does not give it, so copy the folder to the machine where the agent runs instead of opening a gate for it. In outline, at the local `sdsys` login:

1. **Make the account**, with the fewest gates that let it do its job: `create.account user proj-agent ssh bp-on`. `ssh` gives the remote route, and `bp-on` lets the account compile and catalog (without it even `basic` is refused). The verb asks for a password for the new Linux user and `no.query` does not suppress that, so it cannot be scripted. Leave `sh-on`, `os-on`, `sd-on`, `voc-on`, `dict-on`, `net-on`, `files-on` and `shared-write-on` off. Every word you add widens what an instruction hidden in a record could make the agent do.
2. **Decide how it signs in.** As delivered the account SD makes signs in over ssh **with its password** and cannot use a key, because a key is a second way in that the password does not control. If you want the agent to use a key, so that no password is kept where the agent runs, say so account by account: `modify.account proj-agent ssh-key-on` (or `ssh-key-on` in the `create.account` command), then install its public key for that user as for any Linux user. **Opening it means that whoever holds that private key is the agent's account**, and a changed password does not close it; remove the key from the user's `authorized_keys` file, or `modify.account proj-agent ssh-key-off`, to take it back. Either way every ssh session of an SD account is forced into `sd` for that account, so the sign-in gives a session in SD and no shell. A machine whose ssh server allows no password sign-in leaves the agent no way in until `ssh-key-on`; a rule of your own in the ssh server's configuration, read before SD's, wins over SD's.
3. **Give it a workspace of its own**, populated with copies. Keep the production data in accounts the agent is not a member of. If it must see real data, put that data in a group account of its own and add the agent to it with `modify.account`.
4. **Prove the wall** before you trust it. As the agent, try the things the guide says are refused: the `sh` verb, `os.execute`, a path outside the account, a write to the VOC, a restricted statement. Each must be refused in the words the guide quotes. If one succeeds, a gate is open that you did not mean to open.
5. **Keep the hand-over human.** The agent proposes; a person reads the program and copies it into the production account.
6. **Take it back** with `modify.account proj-agent none` (the ssh route), `modify.account proj-agent suspended`, `modify.account proj-agent ssh-key-off` (the key alone), or by removing the key.

## What this does not give you

There are no scopes inside the account: the agent can read, change and delete everything in its own account and in any group account it belongs to, which is why the production data is elsewhere. The audit trail names what the agent did, not what it saw. There is no MCP door: the agent works through its own terminal and the account's own rights, and nothing else is offered to it. And no setting protects you from a prompt that persuades the agent to ask *you* for more: the answer to a request to switch a gate on is yours, and the safe default is no.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Remote access and the machine](05-remote-access-and-the-machine.html).

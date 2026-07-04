# Lab 004: Users, Groups, and Ownership

## Objective

Practice identifying the current user, group membership, numeric user and group IDs, and how file ownership affects access.

This lab is intentionally local and safe. It only creates and modifies files inside this lab directory.

## Commands Practiced

- whoami
- id
- groups
- getent passwd
- getent group
- ls -l
- ls -ln
- stat
- sudo
- chown

## Concepts Practiced

- Username
- User ID, also called UID
- Primary group
- Group ID, also called GID
- Supplementary groups
- File owner
- File group
- Numeric ownership
- Root-owned files
- Why ownership and permissions work together

## What I Learned

- `whoami` shows the current effective username.
- `id` gives a fuller identity view, including UID, primary GID, and supplementary groups.
- `groups` shows which groups the current user belongs to.
- `getent passwd username` shows user account information from the system identity database.
- `getent group groupname` shows group information from the system identity database.
- `ls -l` shows file owner and group names.
- `ls -ln` shows numeric UID and GID instead of names.
- `stat` shows detailed ownership, permission, and timestamp metadata.
- A file can be readable but not writable depending on its owner, group, and permission bits.
- Root-owned files may not be writable by a normal user even if they can be read.
- `sudo` temporarily runs a command with elevated privileges when the user is allowed to do so.
- `chown` changes file ownership and usually requires elevated privileges.
- Ownership and permissions are separate but related: ownership defines who the permission bits apply to.

## Follow-up Questions

- Why do Linux systems use numeric UID and GID values internally?
- What happens if two systems have the same username but different UID values?
- Why can ownership become important with NFS mounts?
- Why are root-owned files common under `/etc`, `/var`, and system directories?
- Why is it risky to recursively run `chown` or `chmod` without understanding the target path?

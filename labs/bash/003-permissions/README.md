# Lab 003: Permissions and Executable Files

## Objective

Practice basic Linux file permissions, executable bits, symbolic permissions, octal permissions, and file metadata.

This lab is intentionally local and safe. It only modifies files inside this lab directory.

## Commands Practiced

- ls -l
- chmod
- stat
- umask
- touch
- mkdir
- file

## Concepts Practiced

- Read permission
- Write permission
- Execute permission
- Owner, group, and other permissions
- Symbolic permissions like `u+x`
- Octal permissions like `644`, `600`, and `755`
- Why scripts need execute permission to run as `./script.sh`

## What I Learned

- Linux permissions control who can read, write, and execute files.
- `ls -l` shows permissions in a human-readable format.
- The first character in `ls -l` output shows the file type, such as `-` for a regular file or `d` for a directory.
- The next nine characters show permissions for user, group, and others.
- `chmod` changes permissions on files and directories.
- Symbolic permission changes, like `chmod u+x file`, are readable and specific.
- Octal permissions, like `chmod 644 file`, are compact and common in documentation and automation.
- `600` is useful for private files because only the owner can read and write.
- `644` is common for normal readable files.
- `755` is common for executable scripts and directories.
- A shell script can be run with `bash script.sh` even if it is not executable.
- A shell script needs the executable bit set before it can be run as `./script.sh`.
- `stat` gives more detailed permission and metadata information than `ls -l`.
- The main habit from this lab is to check permissions before assuming a file can be read, modified, or executed.

## Follow-up Questions

- Why should SSH private keys usually use restrictive permissions like `600`?
- Why do directories need execute permission?
- When is symbolic `chmod` clearer than octal `chmod`?
- When is octal `chmod` better for scripts and automation?

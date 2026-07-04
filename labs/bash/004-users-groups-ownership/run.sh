#!/usr/bin/env bash

set -u

OUTPUT_DIR="results"
OUTPUT_FILE="${OUTPUT_DIR}/users-groups-ownership-$(date +%Y%m%d-%H%M%S).txt"
PLAYGROUND_DIR="playground"

mkdir -p "$OUTPUT_DIR"
rm -rf "$PLAYGROUND_DIR"
mkdir -p "$PLAYGROUND_DIR"

{
  echo "Lab 004: Users, Groups, and Ownership"
  echo "Run date: $(date)"
  echo "====================================="
  echo

  echo "### whoami"
  whoami
  echo

  echo "### id"
  id
  echo

  echo "### id -u, id -g, id -un, id -gn"
  echo "UID: $(id -u)"
  echo "GID: $(id -g)"
  echo "Username: $(id -un)"
  echo "Primary group name: $(id -gn)"
  echo

  echo "### groups"
  groups
  echo

  echo "### getent passwd current user"
  getent passwd "$(whoami)" || true
  echo

  echo "### getent group primary group"
  getent group "$(id -gn)" || true
  echo

  echo "### Create user-owned files"
  echo "This file is owned by the current user." > "$PLAYGROUND_DIR/user-owned.txt"
  touch "$PLAYGROUND_DIR/empty-user-file.txt"
  echo

  echo "### ls -la playground"
  ls -la "$PLAYGROUND_DIR"
  echo

  echo "### ls -lan playground"
  ls -lan "$PLAYGROUND_DIR"
  echo

  echo "### stat user-owned file"
  stat "$PLAYGROUND_DIR/user-owned.txt"
  echo

  echo "### Create root-owned file using sudo if available"
  if command -v sudo >/dev/null 2>&1; then
    sudo touch "$PLAYGROUND_DIR/root-owned.txt"
    sudo chown root:root "$PLAYGROUND_DIR/root-owned.txt"
    sudo chmod 644 "$PLAYGROUND_DIR/root-owned.txt"
    echo "Created root-owned file."
  else
    echo "sudo is not available in this environment."
  fi
  echo

  echo "### Ownership after creating root-owned file"
  ls -la "$PLAYGROUND_DIR"
  echo
  ls -lan "$PLAYGROUND_DIR"
  echo

  if [ -f "$PLAYGROUND_DIR/root-owned.txt" ]; then
    echo "### stat root-owned file"
    stat "$PLAYGROUND_DIR/root-owned.txt"
    echo

    echo "### Try to append to root-owned file as current user"
    if bash -c "echo 'Attempted write by normal user' >> '$PLAYGROUND_DIR/root-owned.txt'"; then
      echo "Append succeeded."
    else
      echo "Append failed as expected because the current user does not own the file and does not have write permission."
    fi
    echo

    echo "### Use sudo to append to root-owned file"
    sudo bash -c "echo 'Write using sudo' >> '$PLAYGROUND_DIR/root-owned.txt'"
    echo "sudo write succeeded."
    echo

    echo "### Show root-owned file contents"
    cat "$PLAYGROUND_DIR/root-owned.txt"
    echo
  fi

} 2>&1 | tee "$OUTPUT_FILE"

echo
echo "Output saved to: $OUTPUT_FILE"

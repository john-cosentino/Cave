#!/usr/bin/env bash

set -u

OUTPUT_DIR="results"
OUTPUT_FILE="${OUTPUT_DIR}/permissions-$(date +%Y%m%d-%H%M%S).txt"
PLAYGROUND_DIR="playground"

mkdir -p "$OUTPUT_DIR"
rm -rf "$PLAYGROUND_DIR"
mkdir -p "$PLAYGROUND_DIR"

{
  echo "Lab 003: Permissions and Executable Files"
  echo "Run date: $(date)"
  echo "========================================="
  echo

  echo "### Current umask"
  umask
  echo

  echo "### Create test files"
  touch "$PLAYGROUND_DIR/notes.txt"
  touch "$PLAYGROUND_DIR/private.txt"

  cat > "$PLAYGROUND_DIR/script.sh" <<'SCRIPT'
#!/usr/bin/env bash
echo "This script ran successfully."
SCRIPT

  echo "Files created under $PLAYGROUND_DIR"
  echo

  echo "### Initial permissions"
  ls -la "$PLAYGROUND_DIR"
  echo

  echo "### File type checks"
  file "$PLAYGROUND_DIR/notes.txt"
  file "$PLAYGROUND_DIR/script.sh"
  echo

  echo "### stat before chmod"
  stat "$PLAYGROUND_DIR/notes.txt"
  echo
  stat "$PLAYGROUND_DIR/script.sh"
  echo

  echo "### Run script with bash before executable bit"
  bash "$PLAYGROUND_DIR/script.sh"
  echo

  echo "### Try to run script directly before executable bit"
  "$PLAYGROUND_DIR/script.sh"
  echo "Exit code from direct execution attempt: $?"
  echo

  echo "### Apply chmod examples"
  chmod 644 "$PLAYGROUND_DIR/notes.txt"
  chmod 600 "$PLAYGROUND_DIR/private.txt"
  chmod u+x "$PLAYGROUND_DIR/script.sh"
  echo

  echo "### Permissions after chmod"
  ls -la "$PLAYGROUND_DIR"
  echo

  echo "### Run script directly after executable bit"
  "$PLAYGROUND_DIR/script.sh"
  echo

  echo "### stat after chmod"
  stat "$PLAYGROUND_DIR/private.txt"
  echo
  stat "$PLAYGROUND_DIR/script.sh"
  echo

  echo "### Apply octal 755 to script"
  chmod 755 "$PLAYGROUND_DIR/script.sh"
  ls -l "$PLAYGROUND_DIR/script.sh"
  echo

} 2>&1 | tee "$OUTPUT_FILE"

echo
echo "Output saved to: $OUTPUT_FILE"

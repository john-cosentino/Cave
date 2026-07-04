#!/usr/bin/env bash

set -u

OUTPUT_DIR="results"
OUTPUT_FILE="${OUTPUT_DIR}/filesystem-navigation-$(date +%Y%m%d-%H%M%S).txt"

mkdir -p "$OUTPUT_DIR"

{
  echo "Lab 002: Filesystem Navigation and Inspection"
  echo "Run date: $(date)"
  echo "============================================="
  echo

  echo "### pwd"
  pwd
  echo

  echo "### ls -la"
  ls -la
  echo

  echo "### tree -a -L 3 ."
  tree -a -L 3 .
  echo

  echo "### find . -maxdepth 3 -type f"
  find . -maxdepth 3 -type f | sort
  echo

  echo "### du -h --max-depth=2 ."
  du -h --max-depth=2 . | sort -h
  echo

  echo "### stat README.md"
  stat README.md
  echo

  echo "### stat run.sh"
  stat run.sh
  echo

  echo "### file README.md"
  file README.md
  echo

  echo "### file run.sh"
  file run.sh
  echo

  echo "### head -20 README.md"
  head -20 README.md
  echo

  echo "### tail -20 README.md"
  tail -20 README.md
  echo

} | tee "$OUTPUT_FILE"

echo
echo "Output saved to: $OUTPUT_FILE"

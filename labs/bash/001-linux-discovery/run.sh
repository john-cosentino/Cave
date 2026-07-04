#!/usr/bin/env bash

set -u

OUTPUT_DIR="results"
OUTPUT_FILE="${OUTPUT_DIR}/linux-discovery-$(date +%Y%m%d-%H%M%S).txt"

mkdir -p "$OUTPUT_DIR"

{
  echo "Lab 001: Linux Discovery Commands"
  echo "Run date: $(date)"
  echo "======================================"
  echo

  echo "### whoami"
  whoami
  echo

  echo "### hostname"
  hostname
  echo

  echo "### pwd"
  pwd
  echo

  echo "### ls -la"
  ls -la
  echo

  echo "### uname -a"
  uname -a
  echo

  echo "### /etc/os-release"
  cat /etc/os-release
  echo

  echo "### df -h"
  df -h
  echo

  echo "### free -h"
  free -h
  echo

  echo "### ip addr"
  ip addr
  echo

  echo "### ip route"
  ip route
  echo

  echo "### ps aux | head -20"
  ps aux | head -20
  echo

} | tee "$OUTPUT_FILE"

echo
echo "Output saved to: $OUTPUT_FILE"

#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
SCRIPT_NAME="$SCRIPT_DIR/app/clock.py"

# Re-exec with sudo if not root (GPIO/DMA requires root)
if [ "$(id -u)" -ne 0 ]; then
    exec sudo bash "$0" "$@"
fi

cd "$SCRIPT_DIR"

if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo "Warning: Virtual environment not found. Using system Python."
fi

exec python3 "$SCRIPT_NAME" "$@"

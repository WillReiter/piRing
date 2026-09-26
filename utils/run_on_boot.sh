#!/bin/bash

# Installs a cron job that launches auto_start.sh on every boot.
# Safe to run more than once: any existing entry is replaced.

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
START_SCRIPT="$PROJECT_DIR/utils/auto_start.sh"
LOG_FILE="$PROJECT_DIR/auto_start.log"
CRON_ENTRY="@reboot sleep 10 && $START_SCRIPT >> $LOG_FILE 2>&1"

chmod +x "$START_SCRIPT"

# auto_start.sh re-execs itself with sudo, which must not prompt from cron
if ! sudo -n true 2>/dev/null; then
    echo "Warning: passwordless sudo is not available for $(whoami); auto_start.sh will fail at boot."
fi

(crontab -l 2>/dev/null | grep -vF "$START_SCRIPT" || true; echo "$CRON_ENTRY") | crontab -

echo "Installed boot job:"
echo "  $CRON_ENTRY"

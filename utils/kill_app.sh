#!/bin/bash

SCRIPT_TO_KILL="${1:-clock.py}"

sudo pkill -2 -f "$SCRIPT_TO_KILL"

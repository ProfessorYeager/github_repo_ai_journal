#!/bin/bash

# Configuration
INTERVAL=900 # 15 minutes in seconds

echo "Starting AI Journal Watcher..."
echo "Monitoring for changes every 15 minutes."
echo "Press [CTRL+C] to stop."

while true; do
    echo "[$(date)] Running check..."
    python3 scripts/auto_journal.py
    
    echo "Sleeping for 15 minutes..."
    sleep $INTERVAL
done

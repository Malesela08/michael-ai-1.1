#!/bin/bash
# Michael AI - Autonomous Git Auto-Commit & Push Loop (15-Minute Interval)

INTERVAL=900 # 15 minutes in seconds

echo "[AUTO-COMMIT WORKER] Started. Checking for changes every 15 minutes..."

while true; do
    if [[ -n $(git status --porcelain) ]]; then
        TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S SAST")
        echo "[AUTO-COMMIT WORKER] Changes detected at $TIMESTAMP. Committing..."
        git add .
        git commit -m "auto: periodic sync - $TIMESTAMP"
        git push origin main
        echo "[AUTO-COMMIT WORKER] Changes successfully pushed to origin/main."
    else
        echo "[AUTO-COMMIT WORKER] $(date "+%H:%M:%S") - Working tree clean. No changes to commit."
    fi
    sleep $INTERVAL
done

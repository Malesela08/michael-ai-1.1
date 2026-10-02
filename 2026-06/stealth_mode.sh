#!/bin/bash
if [ "$1" == "lockoff" ]; then
    echo "--- Initiating Complete Stealth Mode ---"
    pkill -f guardian-angel
    history -c && history -w
    rm -rf /tmp/guardian_logs/*
    echo "--- System is now Dark/Invisible ---"
elif [ "$1" == "online" ]; then
    echo "--- Initiating Online Stealth Mode ---"
    # Proxy settings removed - direct connection restored
    nohup ./start_guardian_ai.py > /dev/null 2>&1 &
    echo "--- System Online and Hardened ---"
fi

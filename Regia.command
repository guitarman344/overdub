#!/bin/zsh
# Doppio clic: avvia Regia (se non è già accesa) e la apre in Chrome.
cd "$(dirname "$0")"
if ! curl -s -o /dev/null http://localhost:8765/api/videos; then
  nohup /usr/bin/python3 server.py "$HOME/Documents/Video Youtube - Tiktok" > regia.log 2>&1 &
  for i in {1..20}; do curl -s -o /dev/null http://localhost:8765/api/videos && break; sleep 0.25; done
fi
open -a "Google Chrome" http://localhost:8765
osascript -e 'tell application "Terminal" to close (every window whose name contains "Regia.command")' > /dev/null 2>&1 &
exit 0

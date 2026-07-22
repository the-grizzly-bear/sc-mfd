#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
fuser -k 80/tcp 8080/tcp 2>/dev/null   # by port; pkill -f would kill this shell
sleep 1
setsid python3 -u -m scmfd serve > server.log 2>&1 < /dev/null &
disown 2>/dev/null
for _ in $(seq 1 15); do
  ss -tlnp 2>/dev/null | grep -qE ':80 |:8080 ' && { echo "SC-MFD up ($(grep -o 'serving on :[0-9]*' server.log | tail -1))"; exit 0; }
  sleep 1
done
echo "FAILED:"; cat server.log

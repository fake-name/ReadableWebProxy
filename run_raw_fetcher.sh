#!/usr/bin/env bash

# source venv/bin/activate

until pypy3 runScrape.py raw; do
    echo "Server 'pypy3 runScrape.py raw' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
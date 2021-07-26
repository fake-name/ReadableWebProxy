#!/usr/bin/env bash

# source venv/bin/activate

until pypy3 run.py; do
    echo "Server 'pypy3 run.py' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
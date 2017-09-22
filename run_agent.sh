#!/usr/bin/env bash

# source venv/bin/activate

until python3 runFetchAgent.py; do
    echo "Server 'python3 runFetchAgent.py' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
#!/bin/bash

# Bash script to validate goal files
# This simply calls the Python script

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[ERROR] Python is required to run the goal validator" >&2
        exit 1
    fi
fi

# Call the Python validation script with the provided files
python3 "$(dirname "$0")/validate_goals.py" "$@"

# Pass through the exit code from the Python script
exit $?
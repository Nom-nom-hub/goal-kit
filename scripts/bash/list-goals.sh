#!/bin/bash

# list-goals.sh - List all goals in the goal-dev-spec project
# Usage: ./list-goals.sh

set -e

# Check if we're in a goal-dev-spec project
if [ ! -f "./.goal/goal.yaml" ] && [ ! -f "./goal.yaml" ]; then
    echo "Error: Not in a goal-dev-spec project directory"
    echo "Run 'goal init' first or navigate to a goal-dev-spec project directory"
    exit 1
fi

# Use the goal CLI to list goals
if command -v goal &> /dev/null; then
    goal list
else
    echo "Error: goal CLI not found"
    echo "Please install goal-dev-spec CLI to use this script"
    exit 1
fi
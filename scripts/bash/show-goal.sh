#!/bin/bash

# show-goal.sh - Show details of a specific goal in the goal-dev-spec project
# Usage: ./show-goal.sh <goal-id>

set -e

# Check if we're in a goal-dev-spec project
if [ ! -f "./.goal/goal.yaml" ] && [ ! -f "./goal.yaml" ]; then
    echo "Error: Not in a goal-dev-spec project directory"
    echo "Run 'goal init' first or navigate to a goal-dev-spec project directory"
    exit 1
fi

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <goal-id>"
    echo "Use 'list-goals.sh' to find goal IDs"
    exit 1
fi

GOAL_ID="$1"

# Use the goal CLI to show the goal
if command -v goal &> /dev/null; then
    goal show "$GOAL_ID"
else
    echo "Error: goal CLI not found"
    echo "Please install goal-dev-spec CLI to use this script"
    exit 1
fi
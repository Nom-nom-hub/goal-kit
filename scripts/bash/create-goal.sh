#!/bin/bash

# create-goal.sh - Create a new goal in the goal-dev-spec project
# Usage: ./create-goal.sh "Goal Title" "Goal Description"

set -e

# Check if we're in a goal-dev-spec project
if [ ! -f "./.goal/goal.yaml" ] && [ ! -f "./goal.yaml" ]; then
    echo "Error: Not in a goal-dev-spec project directory"
    echo "Run 'goal init' first or navigate to a goal-dev-spec project directory"
    exit 1
fi

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 \"Goal Title\" \"Goal Description\""
    exit 1
fi

GOAL_TITLE="$1"
GOAL_DESCRIPTION="$2"

# Use the goal CLI to create the goal
if command -v goal &> /dev/null; then
    goal create "$GOAL_TITLE" "$GOAL_DESCRIPTION"
else
    echo "Error: goal CLI not found"
    echo "Please install goal-dev-spec CLI to use this script"
    exit 1
fi
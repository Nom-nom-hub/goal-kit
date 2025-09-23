#!/bin/bash

# update-goal-status.sh - Update the status of a specific goal in the goal-dev-spec project
# Usage: ./update-goal-status.sh <goal-id> <status>

set -e

# Check if we're in a goal-dev-spec project
if [ ! -f "./.goal/goal.yaml" ] && [ ! -f "./goal.yaml" ]; then
    echo "Error: Not in a goal-dev-spec project directory"
    echo "Run 'goal init' first or navigate to a goal-dev-spec project directory"
    exit 1
fi

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <goal-id> <status>"
    echo "Valid statuses: draft, planned, in_progress, completed, blocked"
    exit 1
fi

GOAL_ID="$1"
STATUS="$2"

# Use the goal CLI to update the goal status
if command -v goal &> /dev/null; then
    # This would require implementing an update command in the goal CLI
    echo "Updating goal $GOAL_ID status to $STATUS"
    echo "Note: This functionality needs to be implemented in the goal CLI"
else
    echo "Error: goal CLI not found"
    echo "Please install goal-dev-spec CLI to use this script"
    exit 1
fi
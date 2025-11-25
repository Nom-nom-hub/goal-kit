#!/bin/bash
# Fix error handling in bash scripts by replacing set -e with common.sh pattern

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASH_SCRIPTS_DIR="$SCRIPT_DIR/bash"

# Files to update
SCRIPTS=(
    "create-report.sh"
    "create-review.sh"
    "create-tasks.sh"
    "setup-execution.sh"
    "setup-milestones.sh"
    "setup-strategy.sh"
    "update-agent-context.sh"
)

for script in "${SCRIPTS[@]}"; do
    filepath="$BASH_SCRIPTS_DIR/$script"
    if [ ! -f "$filepath" ]; then
        echo "File not found: $filepath"
        continue
    fi
    
    echo "Processing: $script"
    
    # Check if already has common.sh sourced
    if grep -q 'source.*common\.sh' "$filepath"; then
        echo "  Already has common.sh sourced"
        continue
    fi
    
    # Replace set -e with common.sh sourcing and handle_error usage
    # This would be easier in sed/awk
    echo "  Would need manual updates"
done

echo "Done"

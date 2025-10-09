#!/bin/bash

# Common utilities for Goal Kit scripts

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if we're in a git repository
is_git_repo() {
    git rev-parse --git-dir >/dev/null 2>&1
}

# Get the root directory of the current git repository
get_git_root() {
    git rev-parse --show-toplevel
}

# Check if required tools are installed
check_prerequisites() {
    local missing_tools=()

    if ! command_exists git; then
        missing_tools+=("git")
    fi

    if ! command_exists uv; then
        missing_tools+=("uv")
    fi

    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_info "Please install the missing tools and try again."
        exit 1
    fi

    log_success "All prerequisites are installed"
}

# Create a new branch for the current goal
create_goal_branch() {
    local goal_name="$1"
    local branch_name

    # Convert goal name to branch format (e.g., "001-user-authentication")
    if [[ "$goal_name" =~ ^[0-9]+- ]]; then
        branch_name="$goal_name"
    else
        # Find the next available number
        local max_num=0
        while IFS= read -r branch; do
            if [[ "$branch" =~ ^[0-9]+- ]]; then
                local num="${branch%%-*}"
                if (( num > max_num )); then
                    max_num=$num
                fi
            fi
        done < <(git branch -a | grep -E '^[[:space:]]*[0-9]+-' | sed 's/^[[:space:]]*//' | sed 's/remotes\/origin\///')

        branch_name="$(printf "%03d" $((max_num + 1)))-$goal_name"
    fi

    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        log_info "Branch $branch_name already exists, switching to it"
        git checkout "$branch_name"
    else
        log_info "Creating new branch: $branch_name"
        git checkout -b "$branch_name"
    fi

    echo "$branch_name"
}

# Update the CLAUDE.md or similar file with current context
update_agent_context() {
    local project_root
    project_root=$(get_git_root)

    # Look for agent-specific context files
    local context_files=(
        "CLAUDE.md"
        ".claude/context.md"
        "GEMINI.md"
        ".gemini/context.md"
        "CURSOR.md"
        ".cursor/context.md"
    )

    for context_file in "${context_files[@]}"; do
        if [[ -f "$project_root/$context_file" ]]; then
            log_info "Updating context in $context_file"
            # Add current goal context to the file
            cat >> "$project_root/$context_file" << EOF

## Current Goal Context

**Active Goal**: $(basename "$(pwd)")"
**Goal Directory**: $(pwd)
**Branch**: $(git branch --show-current)

This project uses Goal-Driven Development. Focus on:
- Measurable outcomes over feature specifications
- Multiple strategy exploration before implementation
- Learning and adaptation during execution
- Success metrics validation

Available commands:
- /goalkit.vision - Establish project vision and principles
- /goalkit.goal - Define goals and success criteria
- /goalkit.strategies - Explore implementation strategies
- /goalkit.milestones - Create measurable milestones
- /goalkit.execute - Execute with learning and adaptation

EOF
            return 0
        fi
    done

    log_warning "No agent context file found to update"
}

# Validate that we're in a goal directory
validate_goal_context() {
    local current_dir
    current_dir=$(basename "$(pwd)")

    # Check if we're in a goals subdirectory
    if [[ "$(pwd)" != *"goals/"* ]]; then
        log_error "Not in a goal directory"
        log_info "Please navigate to a goal directory (e.g., goals/001-user-authentication/)"
        exit 1
    fi

    # Check for required goal files
    local required_files=("goal.md")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Missing required file: $file"
            exit 1
        fi
    done

    log_success "Goal context validated"
}

# Get the goal name from current directory
get_current_goal_name() {
    basename "$(pwd)"
}

# Print a summary of the current goal
print_goal_summary() {
    local goal_dir="$1"

    if [[ -f "$goal_dir/goal.md" ]]; then
        log_info "Current Goal Summary:"
        echo

        # Extract and display key information from goal.md
        grep -A 5 -B 2 "Goal Statement" "$goal_dir/goal.md" 2>/dev/null || echo "  No goal statement found"
        echo
        grep -A 10 "Success Metrics" "$goal_dir/goal.md" 2>/dev/null || echo "  No success metrics defined"
        echo
    fi
}

# Check if a command is available in the current agent
check_agent_command() {
    local command="$1"

    # This would need to be implemented based on the specific agent
    # For now, we'll assume the command is available if we're in a goal-kit project
    return 0
}

# Setup environment variables for goal development
setup_goal_environment() {
    local goal_dir="$1"

    export GOAL_KIT_PROJECT_ROOT="$(get_git_root)"
    export GOAL_KIT_GOAL_DIR="$goal_dir"
    export GOAL_KIT_GOAL_NAME="$(basename "$goal_dir")"

    log_info "Goal environment configured"
    log_info "  Project Root: $GOAL_KIT_PROJECT_ROOT"
    log_info "  Goal Directory: $GOAL_KIT_GOAL_DIR"
    log_info "  Goal Name: $GOAL_KIT_GOAL_NAME"
}

# Cleanup function for error handling
cleanup_on_error() {
    local exit_code=$?
    if (( exit_code != 0 )); then
        log_error "Script failed with exit code $exit_code"
        # Add any cleanup logic here
    fi
    exit $exit_code
}

# Set up error handling
trap cleanup_on_error ERR

# Main execution guard
main() {
    # Check if script is being sourced or executed
    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        log_error "This script should be sourced, not executed directly"
        log_info "Usage: source ${BASH_SOURCE[0]}"
        exit 1
    fi
}

# Only run main if script is executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
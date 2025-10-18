#!/bin/bash

# Setup milestone planning in a Goal Kit project

set -euo pipefail

#!/bin/bash

# Setup milestone planning in a Goal Kit project

set -euo pipefail

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Function to display usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS] GOAL_DIRECTORY

Setup milestone planning in the current Goal Kit project.

OPTIONS:
    -h, --help              Show this help message
    -d, --dry-run          Show what would be created without creating it
    -v, --verbose          Enable verbose output
    -j, --json             Output JSON with milestone details only
    --force                Overwrite existing milestone file without prompting

ARGUMENTS:
    GOAL_DIRECTORY         Path to the goal directory to create milestones for

EXAMPLES:
    $0 goals/001-user-authentication
    $0 --dry-run goals/001-user-authentication
    $0 --json goals/001-user-authentication
    $0 -v goals/001-user-authentication
    $0 --force goals/001-user-authentication

EOF
}

# Function to display usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS] GOAL_DIRECTORY

Setup milestone planning in the current Goal Kit project.

OPTIONS:
    -h, --help              Show this help message
    -d, --dry-run          Show what would be created without creating it
    -v, --verbose          Enable verbose output
    -j, --json             Output JSON with milestone details only
    --force                Overwrite existing milestone file without prompting

ARGUMENTS:
    GOAL_DIRECTORY         Path to the goal directory to create milestones for

EXAMPLES:
    $0 goals/001-user-authentication
    $0 --dry-run goals/001-user-authentication
    $0 --json goals/001-user-authentication
    $0 -v goals/001-user-authentication
    $0 --force goals/001-user-authentication

EOF
}

# Parse command line arguments
DRY_RUN=false
VERBOSE=false
JSON_MODE=false
FORCE_OVERWRITE=false
GOAL_DIR=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -j|--json)
            JSON_MODE=true
            shift
            ;;
        --force)
            FORCE_OVERWRITE=true
            shift
            ;;
        -*)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            if [[ -n "$GOAL_DIR" ]]; then
                log_error "Multiple goal directories specified: $GOAL_DIR and $1"
                usage
                exit 1
            fi
            GOAL_DIR="$1"
            shift
            ;;
    esac
done

# Validate arguments
if [[ -z "$GOAL_DIR" ]]; then
    log_error "Goal directory is required"
    usage
    exit 1
fi

# Check if we're in a git repository
if ! is_git_repo; then
    log_error "Not in a git repository"
    log_info "Please run this from the root of a Goal Kit project"
    exit 1
fi

# Get project root
PROJECT_ROOT=$(get_git_root)
cd "$PROJECT_ROOT"

# If JSON mode, output JSON and exit early
if [[ "$JSON_MODE" == "true" ]]; then
    # Check if goal directory exists
    if [[ ! -d "$GOAL_DIR" ]]; then
        log_error "Goal directory does not exist: $GOAL_DIR"
        exit 1
    fi
    
    # Get goal directory name without path
    GOAL_DIR_NAME=$(basename "$GOAL_DIR")
    MILESTONE_FILE="$GOAL_DIR/milestones.md"
    BRANCH_NAME="$GOAL_DIR_NAME"
    
    # Output JSON with required variables using common function
    JSON_DATA="{\"GOAL_DIR\":\"$GOAL_DIR\",\"MILESTONE_FILE\":\"$MILESTONE_FILE\",\"BRANCH_NAME\":\"$BRANCH_NAME\"}"
    output_json_mode "$JSON_DATA"
fi

# Verify goal directory exists
if [[ ! -d "$GOAL_DIR" ]]; then
    log_error "Goal directory does not exist: $GOAL_DIR"
    exit 1
fi

# Check if milestones.md already exists
MILESTONE_FILE="$GOAL_DIR/milestones.md"
if [[ -f "$MILESTONE_FILE" ]]; then
    log_warning "Milestone file already exists: $MILESTONE_FILE"
    if [[ "$DRY_RUN" == "false" ]]; then
        if [[ "$FORCE_OVERWRITE" == "true" ]]; then
            log_info "--force specified, overwriting milestone file without prompt"
        elif [[ -t 0 ]]; then
            read -p "Overwrite existing milestone file? (y/N): " response
            if [[ ! "$response" =~ ^[Yy]$ ]]; then
                log_info "Operation cancelled"
                exit 0
            fi
        else
            log_error "Non-interactive mode detected and --force not set. Operation cancelled."
            exit 1
        fi
    fi
fi

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "[DRY RUN] Would create milestone file: $MILESTONE_FILE"
    exit 0
fi

# Create milestone file with basic template
cat > "$MILESTONE_FILE" << EOF
# Milestone Plan for $(basename "$GOAL_DIR")

## Overview
Milestone plan for goal: $(basename "$GOAL_DIR")

## Milestone Definition Framework
- **Measurable Outcomes**: Clear indicators of milestone achievement
- **Learning Objectives**: What to discover at each milestone
- **Value Delivery**: User/business value at each step
- **Implementation Approaches**: Different ways to achieve the milestone

## Progress Tracking Framework
- **Overall Progress Metrics**: How to measure goal advancement
- **Milestone Health Indicators**: Signs of milestone success or trouble
- **Adaptation Triggers**: When to adjust approach or sequence

## Review Process
- **Milestone Review Cadence**: Regular assessment schedule
- **Review Framework**: What to evaluate at each review
- **Decision Framework**: How to adapt based on results

## Success Validation
- **Milestone Success Criteria**: When milestone is considered complete
- **Goal Progress Indicators**: How milestone advances the goal
- **Learning Quality Assessment**: How to evaluate insights gained
EOF

log_success "Created milestone file: $MILESTONE_FILE"

# Print summary
log_success "Milestone planning setup completed!"
echo
log_info "Milestone Details:"
echo "  Goal Directory: $GOAL_DIR"
echo "  Milestone File: $MILESTONE_FILE"
echo
log_info "Next Steps:"
echo "  1. Review and enhance the milestone plan"
echo "  2. Use /goalkit.execute to implement with learning and adaptation"

# Setup goal environment for immediate development
if ! setup_goal_environment "$GOAL_DIR"; then
    log_error "Failed to setup goal environment for $GOAL_DIR"
    exit 1
fi
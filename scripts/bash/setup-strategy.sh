#!/bin/bash

# Setup strategy analysis in a Goal Kit project

set -euo pipefail

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Function to display usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS] GOAL_DIRECTORY

Setup strategy analysis in the current Goal Kit project.

OPTIONS:
    -h, --help              Show this help message
    -d, --dry-run          Show what would be created without creating it
    -v, --verbose          Enable verbose output
    -j, --json             Output JSON with strategy details only

ARGUMENTS:
    GOAL_DIRECTORY         Path to the goal directory to analyze

EXAMPLES:
    $0 goals/001-user-authentication
    $0 --dry-run goals/001-user-authentication
    $0 --json goals/001-user-authentication
    $0 -v goals/001-user-authentication

EOF
}

# Parse command line arguments
DRY_RUN=false
VERBOSE=false
JSON_MODE=false
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
        -*)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            if [[ -z "$GOAL_DIR" ]]; then
                GOAL_DIR="$1"
            else
                GOAL_DIR="$GOAL_DIR $1"
            fi
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
    STRATEGY_FILE="$GOAL_DIR/strategies.md"
    BRANCH_NAME="$GOAL_DIR_NAME"
    
    # Output JSON with required variables
    cat << EOF
{
  "GOAL_DIR": "$GOAL_DIR",
  "STRATEGY_FILE": "$STRATEGY_FILE",
  "BRANCH_NAME": "$BRANCH_NAME"
}
EOF
    exit 0
fi

# Verify goal directory exists
if [[ ! -d "$GOAL_DIR" ]]; then
    log_error "Goal directory does not exist: $GOAL_DIR"
    exit 1
fi

# Check if strategies.md already exists
STRATEGY_FILE="$GOAL_DIR/strategies.md"
if [[ -f "$STRATEGY_FILE" ]]; then
    log_warning "Strategy file already exists: $STRATEGY_FILE"
    if [[ "$DRY_RUN" == "false" ]]; then
        response=$(echo "n")
        read -p "Overwrite existing strategy file? (y/N): " response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            log_info "Operation cancelled"
            exit 0
        fi
    fi
fi

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "[DRY RUN] Would create strategy file: $STRATEGY_FILE"
    exit 0
fi

# Create strategy file with basic template
cat > "$STRATEGY_FILE" << EOF
# Strategy Analysis for $(basename "$GOAL_DIR")

## Overview
Strategy analysis for goal: $(basename "$GOAL_DIR")

## Strategy Exploration Framework
- **Technical Strategy Options**: Different technologies and architectures
- **User Experience Strategies**: Various approaches to user interaction
- **Implementation Strategies**: Different development and rollout approaches

## Strategy Comparison Matrix
- **Technical Feasibility**: How practical each strategy is to implement
- **User Experience Quality**: How well each strategy serves users
- **Development Effort**: Resources required for each strategy
- **Risk Level**: Potential issues and their likelihood
- **Learning Potential**: What each strategy can teach

## Recommended Starting Strategy
- **Primary Recommendation**: Which strategy to try first
- **Rationale**: Evidence-based reasoning for the choice
- **Success Criteria**: How to validate if the strategy works
- **Fallback Options**: Alternative strategies if primary fails

## Validation Experiments
- **Critical Assumption Tests**: Experiments to validate strategy assumptions
- **Measurement Plan**: How to evaluate strategy effectiveness
- **Success Thresholds**: When strategy is considered successful
EOF

log_success "Created strategy file: $STRATEGY_FILE"

# Print summary
log_success "Strategy analysis setup completed!"
echo
log_info "Strategy Details:"
echo "  Goal Directory: $GOAL_DIR"
echo "  Strategy File: $STRATEGY_FILE"
echo
log_info "Next Steps:"
echo "  1. Review and enhance the strategy analysis"
echo "  2. Use /goalkit.milestones to create measurable milestones"
echo "  3. Use /goalkit.execute to implement with learning and adaptation"

# Setup goal environment for immediate development
setup_goal_environment "$GOAL_DIR"
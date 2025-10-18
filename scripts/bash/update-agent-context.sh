#!/bin/bash

# Update AI agent context for Goal Kit development

set -euo pipefail

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}") && pwd)"
source "$SCRIPT_DIR/common.sh"

# Function to display usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Update AI agent context files with current Goal Kit project information.

OPTIONS:
    -h, --help              Show this help message
    -v, --verbose          Enable verbose output
    -f, --force           Force update even if no changes detected

EXAMPLES:
    $0
    $0 --verbose
    $0 --force

EOF
}

# Parse command line arguments
VERBOSE=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -*)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            log_error "Unexpected argument: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate we're in a git repository
if ! is_git_repo; then
    log_error "Not in a git repository"
    log_info "Please run this from the root of a Goal Kit project"
    exit 1
fi

# Get project information
PROJECT_ROOT=$(get_git_root)
cd "$PROJECT_ROOT"

# Check if this is a Goal Kit project
if [[ ! -f ".goalkit/vision.md" ]]; then
    log_error "Not a Goal Kit project"
    log_info "Please run 'goalkeeper init' first to set up the project"
    exit 1
fi

if [[ "$VERBOSE" == "true" ]]; then
    log_info "Updating agent context in $PROJECT_ROOT"
fi

# Agent context files to update (in order of preference)
CONTEXT_FILES=(
    "CLAUDE.md"
    ".claude/context.md"
    "GEMINI.md"
    ".gemini/context.md"
    "CURSOR.md"
    ".cursor/context.md"
    "WINDSURF.md"
    ".windsurf/context.md"
    "KILOCODE.md"
    ".kilocode/context.md"
)

UPDATED_FILES=()
PROJECT_NAME=$(basename "$PROJECT_ROOT")
CURRENT_BRANCH=$(git branch --show-current)
ACTIVE_GOALS_COUNT=$(find goals -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)

# Generate context content
CONTEXT_CONTENT=$(cat << EOF
# Goal Kit Project Context

**Project**: $PROJECT_NAME
**Branch**: $CURRENT_BRANCH
**Active Goals**: $ACTIVE_GOALS_COUNT
**Updated**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## 🎯 Goal-Driven Development Status

This project uses Goal-Driven Development methodology. Focus on:
- Measurable outcomes over feature specifications
- Multiple strategy exploration before implementation
- Learning and adaptation during execution
- Success metrics validation

## 📋 Available Commands

### Core Commands
- **/goalkit.vision** - Establish project vision and principles
- **/goalkit.goal** - Define goals and success criteria
- **/goalkit.strategies** - Explore implementation strategies
- **/goalkit.milestones** - Create measurable milestones
- **/goalkit.execute** - Execute with learning and adaptation



## 🚀 Project Vision

$(head -20 .goalkit/vision.md 2>/dev/null | grep -v "^#" | head -10 || echo "Vision document not yet created")

## 🎯 Active Goals

$(if [[ -d "goals" ]] && [[ $ACTIVE_GOALS_COUNT -gt 0 ]]; then
    echo "Recent goals:"
    for goal_dir in goals/*/; do
        if [[ -d "$goal_dir" ]]; then
            goal_name=$(basename "$goal_dir")
            goal_statement=$(grep -m 1 "Goal Statement" "$goal_dir/goal.md" 2>/dev/null | sed 's/.*Goal Statement: //' | head -1 || echo "Goal definition in progress")
            echo "- **$goal_name**: $goal_statement"
        fi
    done | head -5
else
    echo "No active goals yet. Use /goalkit.goal to create your first goal."
fi)

## 📊 Development Principles

Remember these core principles:
1. **Outcome-First**: Prioritize user and business outcomes
2. **Strategy Flexibility**: Multiple valid approaches exist for any goal
3. **Measurement-Driven**: Progress must be measured and validated
4. **Learning Integration**: Treat implementation as hypothesis testing
5. **Adaptive Planning**: Change course based on evidence

## 🔧 Next Recommended Actions

$(if [[ $ACTIVE_GOALS_COUNT -eq 0 ]]; then
    echo "1. Use /goalkit.vision to establish project vision"
    echo "2. Use /goalkit.goal to define first goal"
else
    echo "1. Review active goals in goals/ directory"
    echo "2. Use /goalkit.strategies to explore implementation approaches"
    echo "3. Use /goalkit.milestones to plan measurable progress steps"
fi)

---

*This context is automatically updated by update-agent-context.sh. Last updated: $(date)*
EOF
)

# Update context files
for context_file in "${CONTEXT_FILES[@]}"; do
    if [[ -f "$PROJECT_ROOT/$context_file" ]] || [[ "$FORCE" == "true" ]]; then
        if echo "$CONTEXT_CONTENT" > "$PROJECT_ROOT/$context_file"; then
            UPDATED_FILES+=("$context_file")
            if [[ "$VERBOSE" == "true" ]]; then
                log_success "Updated $context_file"
            fi
        else
            log_error "Failed to update $context_file"
        fi
    fi
done

# Summary
if [[ ${#UPDATED_FILES[@]} -gt 0 ]]; then
    log_success "Updated agent context in ${#UPDATED_FILES[@]} file(s):"
    for file in "${UPDATED_FILES[@]}"; do
        echo "  - $file"
    done
else
    log_warning "No agent context files found to update"
    log_info "Supported files:"
    for file in "${CONTEXT_FILES[@]}"; do
        echo "  - $file"
    done
fi

echo
log_info "Agent context update completed!"
log_info "Project: $PROJECT_NAME"
log_info "Branch: $CURRENT_BRANCH"
log_info "Active Goals: $ACTIVE_GOALS_COUNT"

if [[ $ACTIVE_GOALS_COUNT -gt 0 ]]; then
    log_info "Recent goals:"
    for goal_dir in goals/*/; do
        if [[ -d "$goal_dir" ]]; then
            goal_name=$(basename "$goal_dir")
            echo "  - $goal_name"
        fi
    done | head -3
fi
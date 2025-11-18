#!/bin/bash

# Generate implementation tasks for a goal

set -e

GOAL_DIR="${1:-}"
FORCE=false
JSON=false
VERBOSE=false

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --force)
            FORCE=true
            shift
            ;;
        --json)
            JSON=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            GOAL_DIR="$1"
            shift
            ;;
    esac
done

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    write_error "Not in a git repository"
    write_info "Please run this from the root of a Goal Kit project"
    exit 1
fi

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

# Check if this is a Goal Kit project
if [ ! -f ".goalkit/vision.md" ]; then
    write_error "Not a Goal Kit project"
    write_info "Please run 'goalkeeper init' first to set up the project"
    exit 1
fi

# Determine goal directory
if [ -z "$GOAL_DIR" ]; then
    # Check if we're in a goal directory
    CURRENT_DIR="$(pwd)"
    if [[ "$CURRENT_DIR" == *".goalkit/goals"* ]]; then
        GOAL_DIR=$(basename "$CURRENT_DIR")
    else
        write_error "Goal directory not specified and not in a goal directory"
        write_info "Usage: create-tasks.sh [goal-dir-name] or run from a goal directory"
        exit 1
    fi
fi

# Find the goal directory
TARGET_GOAL_DIR=".goalkit/goals/$GOAL_DIR"

if [ ! -d "$TARGET_GOAL_DIR" ]; then
    write_error "Goal directory not found: $GOAL_DIR"
    exit 1
fi

# Check for goal.md
GOAL_FILE="$TARGET_GOAL_DIR/goal.md"
if [ ! -f "$GOAL_FILE" ]; then
    write_error "goal.md not found in goal directory"
    exit 1
fi

# Define tasks file path
TASKS_FILE="$TARGET_GOAL_DIR/tasks.md"

# If JSON mode, output JSON
if [ "$JSON" = true ]; then
    echo "{\"GOAL_DIR\":\"$GOAL_DIR\",\"TASKS_FILE\":\"$TASKS_FILE\",\"GOAL_FILE\":\"$GOAL_FILE\"}"
    exit 0
fi

# Check if tasks file already exists
if [ -f "$TASKS_FILE" ] && [ "$FORCE" = false ]; then
    write_warning "Tasks file already exists: $TASKS_FILE"
    write_info "Use --force to overwrite"
    exit 0
fi

# Get timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Check if template exists
TEMPLATE_PATH=".goalkit/templates/tasks-template.md"
if [ -f "$TEMPLATE_PATH" ]; then
    TASKS_CONTENT=$(cat "$TEMPLATE_PATH")
    TASKS_CONTENT="${TASKS_CONTENT//\[GOAL\]/$GOAL_DIR}"
    TASKS_CONTENT="${TASKS_CONTENT//\[DATE\]/$TIMESTAMP}"
else
    # Fallback to default content
    TASKS_CONTENT="# Implementation Tasks: $GOAL_DIR

**Created**: $TIMESTAMP
**Last Updated**: $TIMESTAMP
**Goal Directory**: $GOAL_DIR

## Overview

This document contains the detailed implementation tasks needed to achieve the goal defined in goal.md.
Tasks should be broken down into:
- Clear, actionable items
- Specific acceptance criteria
- Dependencies and sequencing
- Estimated effort

## Phase 1: Foundation & Setup

### Task 1.1: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Specific criterion 3]

**Dependencies**: [List any dependencies]
**Effort**: [Estimated effort: Small/Medium/Large]

---

### Task 1.2: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

**Dependencies**: Task 1.1
**Effort**: [Estimated effort]

---

## Phase 2: Core Implementation

### Task 2.1: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Specific criterion 3]

**Dependencies**: Task 1.1, Task 1.2
**Effort**: [Estimated effort]

---

### Task 2.2: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

**Dependencies**: Task 2.1
**Effort**: [Estimated effort]

---

## Phase 3: Testing & Validation

### Task 3.1: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

**Dependencies**: [List dependencies]
**Effort**: [Estimated effort]

---

## Phase 4: Deployment & Documentation

### Task 4.1: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

**Dependencies**: [List dependencies]
**Effort**: [Estimated effort]

---

## Notes

- Update task status as you progress through implementation
- Use checkboxes to track acceptance criteria completion
- Reference this file in pull requests and commits
"
fi

# Write tasks file
echo "$TASKS_CONTENT" > "$TASKS_FILE"
write_success "Created tasks.md: $TASKS_FILE"

# Git operations
git add "$TASKS_FILE" 2>/dev/null || true
git commit -m "Add implementation tasks for goal: $GOAL_DIR" 2>/dev/null || true

write_success "Tasks committed to repository"

# Print summary
echo ""
write_info "Tasks file created successfully!"
echo "  Goal Directory: $GOAL_DIR"
echo "  Tasks File: $TASKS_FILE"
echo ""
write_info "Next Steps:"
echo "  1. Fill in detailed tasks for each phase"
echo "  2. Break down complex tasks into subtasks"
echo "  3. Define clear acceptance criteria"
echo "  4. Use /goalkit.taskstoissues to convert tasks to GitHub issues"
echo ""

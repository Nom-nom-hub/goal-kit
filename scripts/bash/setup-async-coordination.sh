#!/bin/bash
# Setup async coordination for a goal in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_async_coordination_file() {
    local goal_directory="$1"
    local dry_run=false
    local force=false
    local json_mode=false
    # shellcheck disable=SC2034
    local verbose=false

    shift 1
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run) dry_run=true; shift ;;
            --force) force=true; shift ;;
            --json) json_mode=true; shift ;;
            # shellcheck disable=SC2034
            --verbose) verbose=true; shift ;;
            *) handle_error "Unknown option: $1" ;;
        esac
    done

    if ! test_git_repo; then
        handle_error "Not in a git repository. Please run this from the root of a Goal Kit project"
    fi

    local project_root
    project_root=$(get_git_root) || handle_error "Could not determine git root"
    if [ -z "$project_root" ]; then
        handle_error "Could not determine git root. Not in a git repository."
    fi

    cd "$project_root" || handle_error "Failed to change to project root: $project_root"

    if [ "$json_mode" = true ]; then
        if [ ! -d "$goal_directory" ]; then
            handle_error "Goal directory does not exist: $goal_directory"
        fi

        local goal_dir_name
        goal_dir_name=$(basename "$goal_directory")
        local coordination_file="$goal_directory/async-coordination.md"

        cat <<EOF
{"GOAL_DIR":"$goal_directory","COORDINATION_FILE":"$coordination_file","BRANCH_NAME":"$goal_dir_name"}
EOF
        return
    fi

    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi

    local coordination_file="$goal_directory/async-coordination.md"
    if [ -f "$coordination_file" ] && [ "$dry_run" = false ]; then
        write_warning "Async coordination file already exists: $coordination_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing async coordination file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi

    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create async coordination file: $coordination_file"
        return
    fi

    local goal_dir_name
    goal_dir_name=$(basename "$goal_directory")
    local timestamp
    timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')

    cat > "$coordination_file" <<EOF || handle_error "Failed to write async coordination file: $coordination_file"
# Async Coordination Plan for $goal_dir_name

**Created**: $timestamp
**Status**: Draft

## Overview
Async-first collaboration plan for goal: $goal_dir_name

## Communication Rituals
- **Daily Async Standup**: [Format, channel, cadence]
- **Weekly Async Updates**: [Summary format, recipients]
- **Decision Process**: [How async decisions are made]

## Milestone Handoffs
- **Handoff Points**: [Key transitions between phases]
- **Ownership Transfer**: [Who hands off to whom]
- **Acceptance Criteria**: [How handoffs are validated]

## Escalation Path
- **Decision Authority**: [Who decides what]
- **Escalation Triggers**: [When decisions escalate]
- **Resolution Timeline**: [Expected resolution time]

## Learning Capture
- **Ritual**: [How learnings are captured]
- **Frequency**: [When insights are shared]
- **Format**: [Template for documenting learnings]

## Sync Exceptions
- **Required Sync Points**: [When real-time discussion is needed]
- **Duration**: [How long sync sessions run]
- **Attendees**: [Who participates]
EOF

    write_success "Created async coordination file: $coordination_file"

    if ! set_goal_environment "$goal_directory"; then
        handle_error "Failed to setup goal environment for $goal_directory"
    fi
}

main() {
    if [ $# -lt 1 ]; then
        handle_error "Goal directory is required. Usage: $0 <goal_directory> [--dry-run] [--force] [--json] [--verbose]"
    fi
    create_async_coordination_file "$@"
}

main "$@"

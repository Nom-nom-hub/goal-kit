#!/bin/bash
# Setup cross-goal coordination in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_cross_goal_coordination_file() {
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
        local coordination_file="$goal_directory/cross-goal-coordination.md"

        cat <<EOF
{"GOAL_DIR":"$goal_directory","COORDINATION_FILE":"$coordination_file","BRANCH_NAME":"$goal_dir_name"}
EOF
        return
    fi

    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi

    local coordination_file="$goal_directory/cross-goal-coordination.md"
    if [ -f "$coordination_file" ] && [ "$dry_run" = false ]; then
        write_warning "Cross-goal coordination file already exists: $coordination_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing cross-goal coordination file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi

    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create cross-goal coordination file: $coordination_file"
        return
    fi

    local goal_dir_name
    goal_dir_name=$(basename "$goal_directory")
    local timestamp
    timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')

    cat > "$coordination_file" <<EOF || handle_error "Failed to write cross-goal coordination file: $coordination_file"
# Cross-Goal Coordination Plan for $goal_dir_name

**Created**: $timestamp
**Status**: Draft

## Overview
Coordination plan between goal $goal_dir_name and other active goals.

## Blocking Goals
- **Dependencies**: [What goals must complete before this one]
- **Blocking Deliverables**: [Specific outputs needed]
- **Contingency**: [Fallback if dependencies slip]

## Unblocking Goals
- **Goals Unblocked**: [What goals depend on this one]
- **Deliverables**: [What outputs unblock others]
- **Timeline Impact**: [When dependent goals can start]

## Critical Path
- **If This Goal Slips**: [Impact on dependent goals 1, 2, and 4 weeks]
- **Bottlenecks**: [Where delays are most likely]

## Handoff Protocol
- **Transfer Points**: [When ownership changes between goals]
- **Acceptance Criteria**: [How handoffs are validated]
- **Communication**: [How handoff stakeholders are notified]

## Synchronization Plan
- **Cross-Goal Sync Cadence**: [When teams sync up]
- **Shared Milestones**: [Joint progress checks]
- **Risk Monitoring**: [How cascade risks are tracked]

## Contingency Plan
- **Fallback Strategies**: [What if blocking goals slip]
- **Parallel Work**: [What can proceed independently]
EOF

    write_success "Created cross-goal coordination file: $coordination_file"

    if ! set_goal_environment "$goal_directory"; then
        handle_error "Failed to setup goal environment for $goal_directory"
    fi
}

main() {
    if [ $# -lt 1 ]; then
        handle_error "Goal directory is required. Usage: $0 <goal_directory> [--dry-run] [--force] [--json] [--verbose]"
    fi
    create_cross_goal_coordination_file "$@"
}

main "$@"

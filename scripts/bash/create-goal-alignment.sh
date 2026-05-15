#!/bin/bash
# Create goal alignment document in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_goal_alignment_file() {
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
        local alignment_file="$goal_directory/goal-alignment.md"

        cat <<EOF
{"GOAL_DIR":"$goal_directory","ALIGNMENT_FILE":"$alignment_file","BRANCH_NAME":"$goal_dir_name"}
EOF
        return
    fi

    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi

    local alignment_file="$goal_directory/goal-alignment.md"
    if [ -f "$alignment_file" ] && [ "$dry_run" = false ]; then
        write_warning "Goal alignment file already exists: $alignment_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing goal alignment file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi

    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create goal alignment file: $alignment_file"
        return
    fi

    local goal_dir_name
    goal_dir_name=$(basename "$goal_directory")
    local timestamp
    timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')

    cat > "$alignment_file" <<EOF || handle_error "Failed to write goal alignment file: $alignment_file"
# Goal Alignment: $goal_dir_name

**Created**: $timestamp
**Status**: Draft

## Strategic Pillar
- **Primary Pillar**: [Which strategic pillar this goal advances]
- **Connection**: [Explicit link between goal and pillar]

## 3-Year Objectives Supported
- **Objective 1**: [How this goal advances the objective]
- **Objective 2**: [How this goal advances the objective]

## Values Alignment
- **Value 1**: [How goal approach demonstrates this value]
- **Value 2**: [How goal approach demonstrates this value]
- **Value 3**: [How goal approach demonstrates this value]

## Business Impact
- **Revenue**: [Expected revenue impact]
- **Cost**: [Expected cost impact]
- **Risk**: [Risk reduction or mitigation]
- **Capability**: [New capabilities built]
- **Stakeholder**: [Stakeholder impact]

## Dependencies
- **Internal Dependencies**: [What else needs to succeed]
- **External Dependencies**: [Outside factors required]

## Metrics Alignment
- **Goal Metrics**: [Success criteria from goal.md]
- **Org Metrics**: [How they feed organizational metrics]
- **Linkage**: [Explicit connection between goal and org metrics]

## Stakeholder Alignment
- **Stakeholders**: [Who has been consulted]
- **Status**: [Aligned / Pending / Concerns]
EOF

    write_success "Created goal alignment file: $alignment_file"

    if ! set_goal_environment "$goal_directory"; then
        handle_error "Failed to setup goal environment for $goal_directory"
    fi
}

main() {
    if [ $# -lt 1 ]; then
        handle_error "Goal directory is required. Usage: $0 <goal_directory> [--dry-run] [--force] [--json] [--verbose]"
    fi
    create_goal_alignment_file "$@"
}

main "$@"

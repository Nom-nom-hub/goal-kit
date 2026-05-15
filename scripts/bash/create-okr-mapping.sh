#!/bin/bash
# Create OKR mapping document for a goal in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_okr_mapping_file() {
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
        local mapping_file="$goal_directory/okr-mapping.md"

        cat <<EOF
{"GOAL_DIR":"$goal_directory","MAPPING_FILE":"$mapping_file","BRANCH_NAME":"$goal_dir_name"}
EOF
        return
    fi

    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi

    local mapping_file="$goal_directory/okr-mapping.md"
    if [ -f "$mapping_file" ] && [ "$dry_run" = false ]; then
        write_warning "OKR mapping file already exists: $mapping_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing OKR mapping file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi

    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create OKR mapping file: $mapping_file"
        return
    fi

    local goal_dir_name
    goal_dir_name=$(basename "$goal_directory")
    local timestamp
    timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')

    cat > "$mapping_file" <<EOF || handle_error "Failed to write OKR mapping file: $mapping_file"
# OKR Mapping: $goal_dir_name

**Created**: $timestamp
**Status**: Draft

## Mapping Summary
- **Goal**: $goal_dir_name
- **Supporting KRs**: [Which OKR key results this goal supports]
- **Contribution %**: [Estimated contribution to each KR]

## Goal-KR Connections
### KR 1: [KR Title]
- **Success Criteria Link**: [How goal metrics prove KR achievement]
- **Contribution**: [Estimated percentage]

### KR 2: [KR Title]
- **Success Criteria Link**: [How goal metrics prove KR achievement]
- **Contribution**: [Estimated percentage]

## Timeline Alignment
- **Goal Completion Date**: [When goal finishes]
- **OKR Measurement Date**: [When OKR progress is measured]
- **Risk**: [If goal finishes after OKR measurement]

## Confidence & Risk
- **Confidence Level**: [1-5 assessment]
- **Key Risks**: [What could prevent goal from driving KRs]
- **Mitigations**: [How risks are addressed]

## OKR Check-In Integration
- **Mid-Quarter Review**: [How goal progress feeds OKR review]
- **End-of-Quarter**: [How goal impact on KRs is measured]
EOF

    write_success "Created OKR mapping file: $mapping_file"

    if ! set_goal_environment "$goal_directory"; then
        handle_error "Failed to setup goal environment for $goal_directory"
    fi
}

main() {
    if [ $# -lt 1 ]; then
        handle_error "Goal directory is required. Usage: $0 <goal_directory> [--dry-run] [--force] [--json] [--verbose]"
    fi
    create_okr_mapping_file "$@"
}

main "$@"

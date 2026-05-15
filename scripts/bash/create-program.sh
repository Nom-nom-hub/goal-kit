#!/bin/bash
# Create a program structure in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_program_file() {
    local program_name="$1"
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

    # Clean program name for directory use
    local clean_name
    clean_name=$(echo "$program_name" | sed 's/[^a-zA-Z0-9 -]//g' | sed 's/  */-/g' | sed 's/-$//' | tr '[:upper:]' '[:lower:]')
    local program_dir=".goalkit/programs/$clean_name"
    local program_file="$program_dir/program.md"

    if [ "$json_mode" = true ]; then
        cat <<EOF
{"PROGRAM_DIR":"$program_dir","PROGRAM_FILE":"$program_file","PROGRAM_NAME":"$program_name"}
EOF
        return
    fi

    if [ -f "$program_file" ] && [ "$dry_run" = false ]; then
        write_warning "Program file already exists: $program_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing program file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi

    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create program file: $program_file"
        return
    fi

    mkdir -p "$program_dir" || handle_error "Failed to create program directory: $program_dir"

    local timestamp
    timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')

    cat > "$program_file" <<EOF || handle_error "Failed to write program file: $program_file"
# Program: $program_name

**Created**: $timestamp
**Status**: Draft

## Vision
[2-3 sentence vision statement for this program]

## Strategic Context
- **Strategic Pillar**: [Which pillar this program serves]
- **Business Impact**: [Expected business outcomes]
- **Timeline**: [6+ week timeline]

## Goals in Program

### Goal 1: [Goal Name]
- **Owner**: [Goal owner]
- **Timeline**: [Start - End]
- **Success Criteria**: [Measurable outcomes]
- **Dependencies**: [What blocks this goal]

### Goal 2: [Goal Name]
- **Owner**: [Goal owner]
- **Timeline**: [Start - End]
- **Success Criteria**: [Measurable outcomes]
- **Dependencies**: [What blocks this goal]

[Add additional goals as needed]

## Timeline
\`\`\`
[ASCII timeline showing goal sequence and dependencies]
\`\`\`

## Governance
- **Exec Sponsor**: [Executive sponsor name]
- **Program Manager**: [Program manager name]
- **Review Cadence**: [How often the program is reviewed]
- **Decision Authority**: [Who decides scope/timeline/resources]

## Resource Allocation
- **Teams**: [Teams involved]
- **Allocation**: [Percentage per team]
- **Budget**: [Estimated budget if applicable]

## Success Criteria
- **Functional**: [What gets built]
- **Business**: [Revenue/cost/market impact]
- **Quality**: [Uptime/reliability targets]
- **Team**: [Skills/morale/retention goals]
EOF

    write_success "Created program file: $program_file"
    echo
    write_info "Program Details:"
    echo "  Name: $program_name"
    echo "  Directory: $program_dir"
    echo "  File: $program_file"
    echo
    write_info "Next Steps:"
    echo "  1. Define the program vision and goals"
    echo "  2. Map dependencies between goals"
    echo "  3. Use /goalkit.goal-alignment to create goals in this program"
    echo "  4. Use /goalkit.execute to begin execution"
    echo
}

main() {
    if [ $# -lt 1 ]; then
        handle_error "Program name is required. Usage: $0 <program_name> [--dry-run] [--force] [--json] [--verbose]"
    fi
    create_program_file "$@"
}

main "$@"

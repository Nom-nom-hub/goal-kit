#!/bin/bash
# Setup team roles for a goal in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_team_roles_file() {
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
        local roles_file="$goal_directory/team-roles.md"

        cat <<EOF
{"GOAL_DIR":"$goal_directory","ROLES_FILE":"$roles_file","BRANCH_NAME":"$goal_dir_name"}
EOF
        return
    fi

    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi

    local roles_file="$goal_directory/team-roles.md"
    if [ -f "$roles_file" ] && [ "$dry_run" = false ]; then
        write_warning "Team roles file already exists: $roles_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing team roles file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi

    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create team roles file: $roles_file"
        return
    fi

    local goal_dir_name
    goal_dir_name=$(basename "$goal_directory")
    local timestamp
    timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')

    cat > "$roles_file" <<EOF || handle_error "Failed to write team roles file: $roles_file"
# Team Roles: $goal_dir_name

**Created**: $timestamp
**Status**: Draft

## Role Definitions

### Goal Owner
- **Name**: [Goal owner name]
- **Responsibility**: Overall goal success and decision making
- **Authority**: Scope, timeline, and resource decisions
- **Accountability**: Goal completion and success criteria

### Technical Lead
- **Name**: [Technical lead name]
- **Responsibility**: Technical direction and architecture
- **Authority**: Technical decisions and implementation approach
- **Accountability**: Technical quality and delivery

### Product Owner
- **Name**: [Product owner name]
- **Responsibility**: Requirements and stakeholder management
- **Authority**: Priority and scope decisions
- **Accountability**: Value delivery and user satisfaction

### QA Owner
- **Name**: [QA owner name]
- **Responsibility**: Quality standards and testing
- **Authority**: Quality gates and release sign-off
- **Accountability**: Product quality

## RACI Matrix

| Milestone | Goal Owner | Tech Lead | Product | QA | DevOps |
|-----------|-----------|-----------|---------|-----|--------|
| Planning | A/R | C | C | I | I |
| Implementation | A/I | R | C | I | C |
| Testing | A/I | C | C | R | I |
| Deployment | A/I | I | I | C | R |

## Role Interactions
- **Goal Owner ↔ Tech Lead**: Weekly tech review
- **Product ↔ Goal Owner**: Priority alignment as needed
- **QA ↔ Tech Lead**: Test plan review before testing phase

## Escalation Path
- **Technical Disagreements**: Tech Lead decides, escalate to Goal Owner
- **Scope Changes**: Product Owner decides, escalate to Goal Owner
- **Resource Conflicts**: Goal Owner decides, escalate to Program Manager
EOF

    write_success "Created team roles file: $roles_file"

    if ! set_goal_environment "$goal_directory"; then
        handle_error "Failed to setup goal environment for $goal_directory"
    fi
}

main() {
    if [ $# -lt 1 ]; then
        handle_error "Goal directory is required. Usage: $0 <goal_directory> [--dry-run] [--force] [--json] [--verbose]"
    fi
    create_team_roles_file "$@"
}

main "$@"

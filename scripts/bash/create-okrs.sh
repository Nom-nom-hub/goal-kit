#!/bin/bash
# Create quarterly OKRs document in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_okrs_file() {
    local quarter="$1"
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
        local okrs_file=".goalkit/okrs.md"

        cat <<EOF
{"OKRS_FILE":"$okrs_file","OKRS_DIR":".goalkit","QUARTER":"$quarter"}
EOF
        return
    fi

    local okrs_file=".goalkit/okrs.md"
    if [ -f "$okrs_file" ] && [ "$dry_run" = false ]; then
        write_warning "OKRs file already exists: $okrs_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing OKRs file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi

    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create OKRs file: $okrs_file"
        return
    fi

    local quarter_clean="${quarter:-Current Quarter}"
    local timestamp
    timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')

    cat > "$okrs_file" <<EOF || handle_error "Failed to write OKRs file: $okrs_file"
# OKRs: $quarter_clean

**Created**: $timestamp
**Status**: Draft

## Summary
Quarterly OKRs for $quarter_clean aligned with organizational vision.

## Objectives

### Objective 1: [Objective Title]

**Confidence**: [1-5]

**Key Results**:
- KR 1.1: [Measurable target]
- KR 1.2: [Measurable target]
- KR 1.3: [Measurable target]

**Strategic Pillar**: [Pillar this objective serves]

**Anticipated Goals**: [Goals planned to achieve this objective]

---

### Objective 2: [Objective Title]

**Confidence**: [1-5]

**Key Results**:
- KR 2.1: [Measurable target]
- KR 2.2: [Measurable target]
- KR 2.3: [Measurable target]

**Strategic Pillar**: [Pillar this objective serves]

**Anticipated Goals**: [Goals planned to achieve this objective]

---

### Objective 3: [Objective Title]

**Confidence**: [1-5]

**Key Results**:
- KR 3.1: [Measurable target]
- KR 3.2: [Measurable target]
- KR 3.3: [Measurable target]

**Strategic Pillar**: [Pillar this objective serves]

**Anticipated Goals**: [Goals planned to achieve this objective]

## Dependencies & Risks
- **Key Dependencies**: [What needs to happen for OKR success]
- **Risks**: [Potential blockers]
- **Mitigations**: [How risks are addressed]

## Review Schedule
- **Mid-Quarter Check-In**: [Date]
- **End-of-Quarter Review**: [Date]
EOF

    write_success "Created OKRs file: $okrs_file"

    write_success "OKRs setup completed!"
    echo
    write_info "Next Steps:"
    echo "  1. Fill in objectives and key results"
    echo "  2. Review and set confidence levels"
    echo "  3. Use /goalkit.goal-alignment to create aligned goals"
    echo "  4. Use /goalkit.goal to define specific goals supporting these OKRs"
    echo
}

main() {
    create_okrs_file "$@"
}

main "$@"

#!/bin/bash
# Setup compliance checklist in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_compliance_checklist_file() {
    local goal_directory="$1"
    local dry_run=false
    local force=false
    local json_mode=false
    local verbose=false
    
    # Parse remaining arguments
    shift 1
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run=true
                shift
                ;;
            --force)
                force=true
                shift
                ;;
            --json)
                json_mode=true
                shift
                ;;
            --verbose)
                verbose=true
                shift
                ;;
            *)
                handle_error "Unknown option: $1"
                ;;
        esac
    done
    
    # Check if we're in a git repository
    if ! test_git_repo; then
        handle_error "Not in a git repository. Please run this from the root of a Goal Kit project"
    fi
    
    # Get project root
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
        
        local compliance_file="$goal_directory/compliance-checklist.md"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_directory","COMPLIANCE_FILE":"$compliance_file"}
EOF
        return
    fi
    
    # Verify goal directory exists
    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi
    
    # Check if compliance-checklist.md already exists
    local compliance_file="$goal_directory/compliance-checklist.md"
    if [ -f "$compliance_file" ] && [ "$dry_run" = false ]; then
        write_warning "Compliance checklist file already exists: $compliance_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing compliance checklist? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create compliance checklist file: $compliance_file"
        return
    fi
    
    # Check if template exists, otherwise create default
    if [ -f "$project_root/templates/compliance-checklist-template.md" ]; then
        # Create compliance-checklist.md file using template
        if ! cat "$project_root/templates/compliance-checklist-template.md" > "$compliance_file" 2>/dev/null; then
            write_warning "Failed to copy compliance checklist template, using default content"
        else
            # Replace placeholders in the template
            local goal_dir_name=$(basename "$goal_directory")
            local timestamp=$(date -u +'%Y-%m-%d')
            sed -i.bak "s/\[Goal Name or Service Name\]/$goal_dir_name/g" "$compliance_file" || handle_error "Failed to replace placeholders"
            sed -i.bak "s/\[Date\]/$timestamp/g" "$compliance_file" || handle_error "Failed to replace date"
            sed -i.bak "s/\[Name\]/[Compliance Officer]/g" "$compliance_file" || true
            rm -f "$compliance_file.bak" 2>/dev/null || true
        fi
    fi
    
    write_success "Created compliance checklist file: $compliance_file"
    
    # Print summary
    write_success "Compliance checklist setup completed!"
    echo
    write_info "Compliance Checklist Details:"
    echo "  Goal Directory: $goal_directory"
    echo "  Compliance File: $compliance_file"
    echo
    
    write_info "Next Steps:"
    echo "  1. Identify all applicable compliance frameworks (GDPR, HIPAA, SOC2, PCI-DSS, WCAG, internal policies)"
    echo "  2. List specific requirements for each framework"
    echo "  3. Assess current state: Met, Partially Met, At Risk, Not Met"
    echo "  4. Document gaps with root causes"
    echo "  5. Create remediation plans for Critical/High gaps with owners and timelines"
    echo "  6. Collect evidence (policies, logs, documentation, certifications)"
    echo "  7. Set up monitoring and review cadence"
    echo "  8. Prepare for audits (internal and external)"
    
    # Setup goal environment
    if ! set_goal_environment "$goal_directory"; then
        handle_error "Failed to setup goal environment for $goal_directory"
    fi
}

# Main entry point
main() {
    if [ $# -lt 1 ]; then
        handle_error "Goal directory is required. Usage: $0 <goal_directory> [--dry-run] [--force] [--json] [--verbose]"
    fi
    
    create_compliance_checklist_file "$@"
}

main "$@"

#!/bin/bash
# Setup security review in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_security_review_file() {
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
        
        local security_review_file="$goal_directory/security-review.md"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_directory","SECURITY_REVIEW_FILE":"$security_review_file"}
EOF
        return
    fi
    
    # Verify goal directory exists
    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi
    
    # Check if security-review.md already exists
    local security_review_file="$goal_directory/security-review.md"
    if [ -f "$security_review_file" ] && [ "$dry_run" = false ]; then
        write_warning "Security review file already exists: $security_review_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing security review? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create security review file: $security_review_file"
        return
    fi
    
    # Check if template exists, otherwise create default
    if [ -f "$project_root/templates/security-review-template.md" ]; then
        # Create security-review.md file using template
        if ! cat "$project_root/templates/security-review-template.md" > "$security_review_file" 2>/dev/null; then
            write_warning "Failed to copy security review template, using default content"
        else
            # Replace placeholders in the template
            local goal_dir_name=$(basename "$goal_directory")
            local timestamp=$(date -u +'%Y-%m-%d')
            sed -i.bak "s/\[Goal Name or Service Name\]/$goal_dir_name/g" "$security_review_file" || handle_error "Failed to replace placeholders"
            sed -i.bak "s/\[Date\]/$timestamp/g" "$security_review_file" || handle_error "Failed to replace date"
            sed -i.bak "s/\[Name\/Team\]/[Security Team]/g" "$security_review_file" || true
            rm -f "$security_review_file.bak" 2>/dev/null || true
        fi
    fi
    
    write_success "Created security review file: $security_review_file"
    
    # Print summary
    write_success "Security review setup completed!"
    echo
    write_info "Security Review Details:"
    echo "  Goal Directory: $goal_directory"
    echo "  Security Review File: $security_review_file"
    echo
    
    write_info "Next Steps:"
    echo "  1. Identify threat vectors (external attacks, insider threats, data breaches, DoS, supply chain)"
    echo "  2. Document data flows and external dependencies"
    echo "  3. Scan for OWASP Top 10 vulnerabilities"
    echo "  4. Check dependencies for known CVEs"
    echo "  5. Assess compliance requirements (GDPR, HIPAA, SOC2, etc.)"
    echo "  6. Triage findings: Critical/High/Medium/Low with remediation plans"
    echo "  7. Escalate Critical/High findings immediately"
    
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
    
    create_security_review_file "$@"
}

main "$@"

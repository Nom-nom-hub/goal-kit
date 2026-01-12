#!/bin/bash
# Setup risk register in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_risk_register_file() {
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
        
        local risk_register_file="$goal_directory/risk-register.md"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_directory","RISK_REGISTER_FILE":"$risk_register_file"}
EOF
        return
    fi
    
    # Verify goal directory exists
    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi
    
    # Check if risk-register.md already exists
    local risk_register_file="$goal_directory/risk-register.md"
    if [ -f "$risk_register_file" ] && [ "$dry_run" = false ]; then
        write_warning "Risk register file already exists: $risk_register_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing risk register? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create risk register file: $risk_register_file"
        return
    fi
    
    # Check if template exists, otherwise create default
    if [ -f "$project_root/templates/risk-register-template.md" ]; then
        # Create risk-register.md file using template
        if ! cat "$project_root/templates/risk-register-template.md" > "$risk_register_file" 2>/dev/null; then
            write_warning "Failed to copy risk register template, using default content"
        else
            # Replace placeholders in the template
            local goal_dir_name=$(basename "$goal_directory")
            local timestamp=$(date -u +'%Y-%m-%d')
            sed -i.bak "s/\[Goal Name\]/$goal_dir_name/g" "$risk_register_file" || handle_error "Failed to replace placeholders"
            sed -i.bak "s/\[Date\]/$timestamp/g" "$risk_register_file" || handle_error "Failed to replace date"
            sed -i.bak "s/\[Name\]/[Team Member]/g" "$risk_register_file" || true
            rm -f "$risk_register_file.bak" 2>/dev/null || true
        fi
    fi
    
    write_success "Created risk register file: $risk_register_file"
    
    # Print summary
    write_success "Risk register setup completed!"
    echo
    write_info "Risk Register Details:"
    echo "  Goal Directory: $goal_directory"
    echo "  Risk Register File: $risk_register_file"
    echo
    
    write_info "Next Steps:"
    echo "  1. Identify 8-12 risks across technical, organizational, market, and external categories"
    echo "  2. Assess each risk: Probability (Low/Medium/High) × Impact (Low/Medium/High)"
    echo "  3. Define mitigation strategies for Top 5 risks"
    echo "  4. Assign owners and timelines to each mitigation"
    echo "  5. Set up weekly risk triage cadence"
    
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
    
    create_risk_register_file "$@"
}

main "$@"

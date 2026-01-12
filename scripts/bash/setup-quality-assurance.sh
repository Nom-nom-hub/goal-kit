#!/bin/bash
# Setup quality assurance plan in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_quality_assurance_file() {
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
        
        local qa_file="$goal_directory/quality-assurance.md"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_directory","QA_FILE":"$qa_file"}
EOF
        return
    fi
    
    # Verify goal directory exists
    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi
    
    # Check if quality-assurance.md already exists
    local qa_file="$goal_directory/quality-assurance.md"
    if [ -f "$qa_file" ] && [ "$dry_run" = false ]; then
        write_warning "Quality assurance file already exists: $qa_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing quality assurance plan? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create quality assurance file: $qa_file"
        return
    fi
    
    # Check if template exists, otherwise create default
    if [ -f "$project_root/templates/quality-assurance-template.md" ]; then
        # Create quality-assurance.md file using template
        if ! cat "$project_root/templates/quality-assurance-template.md" > "$qa_file" 2>/dev/null; then
            write_warning "Failed to copy quality assurance template, using default content"
        else
            # Replace placeholders in the template
            local goal_dir_name=$(basename "$goal_directory")
            local timestamp=$(date -u +'%Y-%m-%d')
            sed -i.bak "s/\[Goal Name\]/$goal_dir_name/g" "$qa_file" || handle_error "Failed to replace placeholders"
            sed -i.bak "s/\[Date\]/$timestamp/g" "$qa_file" || handle_error "Failed to replace date"
            sed -i.bak "s/\[QA Lead \/ Engineering Lead\]/[QA Lead]/g" "$qa_file" || true
            rm -f "$qa_file.bak" 2>/dev/null || true
        fi
    fi
    
    write_success "Created quality assurance file: $qa_file"
    
    # Print summary
    write_success "Quality assurance setup completed!"
    echo
    write_info "Quality Assurance Details:"
    echo "  Goal Directory: $goal_directory"
    echo "  QA File: $qa_file"
    echo
    
    write_info "Next Steps:"
    echo "  1. Define critical quality dimensions (3-4 max: functionality, performance, reliability, etc.)"
    echo "  2. Set quality goals for each dimension"
    echo "  3. Define testing strategy (80% unit, 40% integration, 10% E2E)"
    echo "  4. Document acceptance criteria for all features"
    echo "  5. Define release gates (code quality, functional, performance, accessibility, security)"
    echo "  6. Set up quality metrics dashboard (coverage, pass rate, bug trends)"
    echo "  7. Establish quality review cadence"
    
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
    
    create_quality_assurance_file "$@"
}

main "$@"

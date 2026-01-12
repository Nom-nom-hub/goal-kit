#!/bin/bash
# Setup detailed retrospective in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_detailed_retrospective_file() {
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
        
        local retrospective_file="$goal_directory/detailed-retrospective.md"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_directory","RETROSPECTIVE_FILE":"$retrospective_file"}
EOF
        return
    fi
    
    # Verify goal directory exists
    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi
    
    # Check if detailed-retrospective.md already exists
    local retrospective_file="$goal_directory/detailed-retrospective.md"
    if [ -f "$retrospective_file" ] && [ "$dry_run" = false ]; then
        write_warning "Detailed retrospective file already exists: $retrospective_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing detailed retrospective? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create detailed retrospective file: $retrospective_file"
        return
    fi
    
    # Check if template exists, otherwise create default
    if [ -f "$project_root/templates/detailed-retrospective-template.md" ]; then
        # Create detailed-retrospective.md file using template
        if ! cat "$project_root/templates/detailed-retrospective-template.md" > "$retrospective_file" 2>/dev/null; then
            write_warning "Failed to copy detailed retrospective template, using default content"
        else
            # Replace placeholders in the template
            local goal_dir_name=$(basename "$goal_directory")
            local timestamp=$(date -u +'%Y-%m-%d')
            sed -i.bak "s/\[Goal or Program Name\]/$goal_dir_name/g" "$retrospective_file" || handle_error "Failed to replace placeholders"
            sed -i.bak "s/\[Date\]/$timestamp/g" "$retrospective_file" || handle_error "Failed to replace date"
            sed -i.bak "s/\[Name\]/[Facilitator]/g" "$retrospective_file" || true
            rm -f "$retrospective_file.bak" 2>/dev/null || true
        fi
    fi
    
    write_success "Created detailed retrospective file: $retrospective_file"
    
    # Print summary
    write_success "Detailed retrospective setup completed!"
    echo
    write_info "Detailed Retrospective Details:"
    echo "  Goal Directory: $goal_directory"
    echo "  Retrospective File: $retrospective_file"
    echo
    
    write_info "Next Steps:"
    echo "  1. Gather execution metrics: timeline, velocity, scope, resources"
    echo "  2. Review quality & reliability: code coverage, bugs, uptime, incidents"
    echo "  3. Analyze risk outcomes: which risks materialized, which were avoided"
    echo "  4. Collect team feedback: collaboration, communication, satisfaction"
    echo "  5. Quantify outcomes with baselines and trends"
    echo "  6. Identify what worked well and celebrate successes"
    echo "  7. Identify improvement areas and specific action items"
    echo "  8. Prepare leadership summary with key findings"
    echo "  9. Archive lessons learned for future teams"
    
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
    
    create_detailed_retrospective_file "$@"
}

main "$@"

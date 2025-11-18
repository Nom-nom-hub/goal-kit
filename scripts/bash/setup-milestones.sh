#!/bin/bash
# Setup milestone planning in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_milestone_file() {
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
                write_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Check if we're in a git repository
    if ! test_git_repo; then
        write_error "Not in a git repository"
        write_info "Please run this from the root of a Goal Kit project"
        exit 1
    fi
    
    # Get project root
    local project_root
    project_root=$(get_git_root)
    if [ -z "$project_root" ]; then
        write_error "Could not determine git root. Not in a git repository."
        exit 1
    fi
    
    cd "$project_root" || exit 1
    
    if [ "$json_mode" = true ]; then
        if [ ! -d "$goal_directory" ]; then
            write_error "Goal directory does not exist: $goal_directory"
            exit 1
        fi
        
        local goal_dir_name=$(basename "$goal_directory")
        local milestone_file="$goal_directory/milestones.md"
        local branch_name="$goal_dir_name"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_directory","MILESTONE_FILE":"$milestone_file","BRANCH_NAME":"$branch_name"}
EOF
        return
    fi
    
    # Verify goal directory exists
    if [ ! -d "$goal_directory" ]; then
        write_error "Goal directory does not exist: $goal_directory"
        exit 1
    fi
    
    # Check if milestones.md already exists
    local milestone_file="$goal_directory/milestones.md"
    if [ -f "$milestone_file" ] && [ "$dry_run" = false ]; then
        write_warning "Milestone file already exists: $milestone_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing milestone file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create milestone file: $milestone_file"
        return
    fi
    
    # Create milestone file with basic template
    local goal_dir_name=$(basename "$goal_directory")
    
    cat > "$milestone_file" <<EOF
# Milestone Plan for $goal_dir_name

## Overview
Milestone plan for goal: $goal_dir_name

## Milestone Definition Framework
- **Measurable Outcomes**: Clear indicators of milestone achievement
- **Learning Objectives**: What to discover at each milestone
- **Value Delivery**: User/business value at each step
- **Implementation Approaches**: Different ways to achieve the milestone

## Progress Tracking Framework
- **Overall Progress Metrics**: How to measure goal advancement
- **Milestone Health Indicators**: Signs of milestone success or trouble
- **Adaptation Triggers**: When to adjust approach or sequence

## Review Process
- **Milestone Review Cadence**: Regular assessment schedule
- **Review Framework**: What to evaluate at each review
- **Decision Framework**: How to adapt based on results

## Success Validation
- **Milestone Success Criteria**: When milestone is considered complete
- **Goal Progress Indicators**: How milestone advances the goal
- **Learning Quality Assessment**: How to evaluate insights gained
EOF
    
    write_success "Created milestone file: $milestone_file"
    
    # Print summary
    write_success "Milestone planning setup completed!"
    echo
    write_info "Milestone Details:"
    echo "  Goal Directory: $goal_directory"
    echo "  Milestone File: $milestone_file"
    echo
    
    write_info "Next Steps:"
    echo "  1. Review and enhance the milestone plan"
    echo "  2. Use /goalkit.execute to implement with learning and adaptation"
    
    # Setup goal environment for immediate development
    if ! set_goal_environment "$goal_directory"; then
        write_error "Failed to setup goal environment for $goal_directory"
        exit 1
    fi
}

# Main entry point
main() {
    if [ $# -lt 1 ]; then
        write_error "Goal directory is required"
        echo "Usage: $0 <goal_directory> [--dry-run] [--force] [--json] [--verbose]"
        exit 1
    fi
    
    create_milestone_file "$@"
}

main "$@"

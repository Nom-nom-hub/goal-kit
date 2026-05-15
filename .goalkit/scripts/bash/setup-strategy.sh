#!/bin/bash
# Setup strategy analysis in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_strategy_file() {
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
        
        local goal_dir_name=$(basename "$goal_directory")
        local strategy_file="$goal_directory/strategies.md"
        local branch_name="$goal_dir_name"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_directory","STRATEGY_FILE":"$strategy_file","BRANCH_NAME":"$branch_name"}
EOF
        return
    fi
    
    # Verify goal directory exists
    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi
    
    # Check if strategies.md already exists
    local strategy_file="$goal_directory/strategies.md"
    if [ -f "$strategy_file" ] && [ "$dry_run" = false ]; then
        write_warning "Strategy file already exists: $strategy_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing strategy file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        else
            write_info "Overwriting strategy file due to --force option."
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create strategy file: $strategy_file"
        return
    fi
    
    # Create strategy file with basic template
    local goal_dir_name=$(basename "$goal_directory")
    
    cat > "$strategy_file" <<EOF || handle_error "Failed to write strategy file: $strategy_file"
# Strategy Analysis for $goal_dir_name

## Overview
Strategy analysis for goal: $goal_dir_name

## Strategy Exploration Framework
- **Technical Strategy Options**: Different technologies and architectures
- **User Experience Strategies**: Various approaches to user interaction
- **Implementation Strategies**: Different development and rollout approaches

## Strategy Comparison Matrix
- **Technical Feasibility**: How practical each strategy is to implement
- **User Experience Quality**: How well each strategy serves users
- **Development Effort**: Resources required for each strategy
- **Risk Level**: Potential issues and their likelihood
- **Learning Potential**: What each strategy can teach

## Recommended Starting Strategy
- **Primary Recommendation**: Which strategy to try first
- **Rationale**: Evidence-based reasoning for the choice
- **Success Criteria**: How to validate if the strategy works
- **Fallback Options**: Alternative strategies if primary fails

## Validation Experiments
- **Critical Assumption Tests**: Experiments to validate strategy assumptions
- **Measurement Plan**: How to evaluate strategy effectiveness
- **Success Thresholds**: When strategy is considered successful
EOF
    
    write_success "Created strategy file: $strategy_file"
    
    # Print summary
    write_success "Strategy analysis setup completed!"
    echo
    write_info "Strategy Details:"
    echo "  Goal Directory: $goal_directory"
    echo "  Strategy File: $strategy_file"
    echo
    
    write_info "Next Steps:"
    echo "  1. Review and enhance the strategy analysis"
    echo "  2. Use /goalkit.milestones to create measurable milestones" 
    echo "  3. Use /goalkit.execute to implement with learning and adaptation"
    
    # Setup goal environment for immediate development
    if ! set_goal_environment "$goal_directory"; then
        handle_error "Failed to setup goal environment for $goal_directory"
    fi
}

# Main entry point
main() {
    if [ $# -lt 1 ]; then
        write_error "Goal directory is required"
        echo "Usage: $0 <goal_directory> [--dry-run] [--force] [--json] [--verbose]"
        exit 1
    fi
    
    create_strategy_file "$@"
}

main "$@"

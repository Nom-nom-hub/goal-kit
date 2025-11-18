#!/bin/bash
# Setup execution plan in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_execution_file() {
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
        local execution_file="$goal_directory/execution.md"
        local branch_name="$goal_dir_name"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_directory","EXECUTION_FILE":"$execution_file","BRANCH_NAME":"$branch_name"}
EOF
        return
    fi
    
    # Verify goal directory exists
    if [ ! -d "$goal_directory" ]; then
        write_error "Goal directory does not exist: $goal_directory"
        exit 1
    fi
    
    # Check if execution.md already exists
    local execution_file="$goal_directory/execution.md"
    if [ -f "$execution_file" ] && [ "$dry_run" = false ]; then
        write_warning "Execution file already exists: $execution_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing execution file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create execution file: $execution_file"
        return
    fi
    
    # Create execution file with basic template
    local goal_dir_name=$(basename "$goal_directory")
    local timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')
    
    cat > "$execution_file" <<EOF
# Execution Plan for $goal_dir_name

**Created**: $timestamp
**Status**: In Planning

## Overview
Execution plan for goal: $goal_dir_name

## Selected Strategy
- **Strategy Name**: [Which strategy are we implementing]
- **Rationale**: [Why this strategy was selected]
- **Success Criteria**: [How to measure strategy success]

## Execution Timeline

### Phase 1: Foundation
- **Duration**: [Timeline for initial setup]
- **Key Activities**: [What needs to be done first]
- **Dependencies**: [What must be in place]
- **Success Indicators**: [How to know Phase 1 is complete]

### Phase 2: Implementation
- **Duration**: [Timeline for main implementation]
- **Key Activities**: [Core implementation work]
- **Learning Objectives**: [What to learn during this phase]
- **Success Indicators**: [How to know Phase 2 is complete]

### Phase 3: Validation
- **Duration**: [Timeline for testing and validation]
- **Validation Approach**: [How to test success]
- **Measurement Plan**: [How to measure success metrics]
- **Success Indicators**: [How to know Phase 3 is complete]

## Daily/Weekly Execution

### Development Cycle
- **Daily Standups**: [What to check in on daily]
- **Weekly Reviews**: [What to assess weekly]
- **Progress Tracking**: [How to track progress against milestones]

### Decision Framework
- **Adaptation Signals**: [When to consider changing approach]
- **Go/No-Go Criteria**: [When to continue vs. pivot]
- **Escalation Path**: [When to involve others in decisions]

## Learning and Adaptation

### Critical Assumptions
- **Assumption 1**: [What assumption is critical to success]
- **How to Validate**: [How to test if the assumption holds]
- **If Wrong**: [What to do if the assumption fails]

### Learning Loops
- **Learn**: [What insights to gather]
- **Measure**: [How to measure learning]
- **Adapt**: [How to apply learning]

## Risk Management

### Key Risks
- **Risk 1**: [Potential risk to execution]
  - **Likelihood**: [High/Medium/Low]
  - **Impact**: [What happens if this occurs]
  - **Mitigation**: [How to prevent this risk]

### Contingency Plans
- **Plan A**: [Primary execution approach]
- **Plan B**: [Alternative if Plan A stalls]
- **Fallback**: [Emergency fallback approach]

## Communication and Coordination

### Stakeholder Updates
- **Frequency**: [How often to update]
- **Format**: [How to communicate progress]
- **Key Metrics**: [What to highlight in updates]

### Blockers and Escalation
- **Blocker Resolution**: [How to handle blockers]
- **Escalation Path**: [When and how to escalate]

## Completion Criteria

### Execution Success
- [ ] All milestones completed on schedule
- [ ] Success metrics achieved at target levels
- [ ] Primary risks mitigated
- [ ] Learning objectives captured

### Goal Completion
- [ ] Execution complete and validated
- [ ] All success metrics confirmed achieved
- [ ] Documentation complete
- [ ] Ready for post-execution review

---

*This execution plan guides day-to-day work. Review and update regularly based on progress and learning.*
EOF
    
    write_success "Created execution file: $execution_file"
    
    # Print summary
    write_success "Execution plan setup completed!"
    echo
    write_info "Execution Details:"
    echo "  Goal Directory: $goal_directory"
    echo "  Execution File: $execution_file"
    echo
    
    write_info "Next Steps:"
    echo "  1. Review and customize the execution plan"
    echo "  2. Define your first day's work items"
    echo "  3. Begin execution with regular progress checks"
    echo "  4. Document learnings as you progress"
    
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
    
    create_execution_file "$@"
}

main "$@"

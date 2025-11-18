#!/bin/bash
# Create a new goal in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Parse arguments
create_goal() {
    local goal_description="$1"
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
    
    # Validate arguments
    if [ -z "$goal_description" ]; then
        write_error "Goal description is required"
        exit 1
    fi
    
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
    
    # Check if this is a Goal Kit project
    if [ ! -f ".goalkit/vision.md" ]; then
        write_error "Not a Goal Kit project"
        write_info "Please run 'goalkeeper init' first to set up the project"
        exit 1
    fi
    
    # If JSON mode, output JSON and exit early
    if [ "$json_mode" = true ]; then
        local goals_dir=".goalkit/goals"
        local next_number=1
        
        if [ -d "$goals_dir" ]; then
            for dir in "$goals_dir"/*-*/; do
                if [ -d "$dir" ]; then
                    local dir_name=$(basename "$dir")
                    if [[ "$dir_name" =~ ^([0-9]+)- ]]; then
                        local num=${BASH_REMATCH[1]}
                        if [ "$num" -ge "$next_number" ]; then
                            next_number=$((num + 1))
                        fi
                    fi
                fi
            done
        fi
        
        # Create goal directory name
        local goal_number=$(printf "%03d" "$next_number")
        local clean_description=$(echo "$goal_description" | sed 's/[^a-zA-Z0-9 -]//g' | sed 's/  */-/g' | sed 's/-$//' | tr '[:upper:]' '[:lower:]')
        local goal_dir_name="${goal_number}-${clean_description}"
        local goal_dir=".goalkit/goals/$goal_dir_name"
        local goal_file="$goal_dir/goal.md"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_dir","GOAL_FILE":"$goal_file","GOAL_DESCRIPTION":"$goal_description","BRANCH_NAME":"$goal_dir_name"}
EOF
        return
    fi
    
    # Check if goals directory exists
    local goals_dir=".goalkit/goals"
    if [ ! -d "$goals_dir" ]; then
        if [ "$dry_run" = true ]; then
            write_info "[DRY RUN] Would create goals directory: $goals_dir"
        else
            mkdir -p "$goals_dir"
            write_success "Created goals directory: $goals_dir"
        fi
    fi
    
    # Find the next goal number
    local next_number=1
    if [ -d "$goals_dir" ]; then
        for dir in "$goals_dir"/*-*/; do
            if [ -d "$dir" ]; then
                local dir_name=$(basename "$dir")
                if [[ "$dir_name" =~ ^([0-9]+)- ]]; then
                    local num=${BASH_REMATCH[1]}
                    if [ "$num" -ge "$next_number" ]; then
                        next_number=$((num + 1))
                    fi
                fi
            fi
        done
    fi
    
    # Create goal directory name
    local goal_number=$(printf "%03d" "$next_number")
    local clean_description=$(echo "$goal_description" | sed 's/[^a-zA-Z0-9 -]//g' | sed 's/  */-/g' | sed 's/-$//' | tr '[:upper:]' '[:lower:]')
    local goal_dir_name="${goal_number}-${clean_description}"
    local goal_dir=".goalkit/goals/$goal_dir_name"
    local full_goal_dir="$project_root/$goal_dir"
    
    # Check if goal directory already exists
    if [ -d "$full_goal_dir" ]; then
        if [ "$force" = false ]; then
            write_error "Goal directory already exists: $goal_dir"
            write_info "Use a different goal description or remove the existing directory"
            exit 1
        else
            if [ "$verbose" = true ]; then
                write_info "Overwriting existing goal directory: $goal_dir"
            fi
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create goal directory: $goal_dir"
        write_info "[DRY RUN] Would create goal.md with description: $goal_description"
        write_info "[DRY RUN] Would create branch: $goal_dir_name"
        return
    fi
    
    # Create goal directory
    mkdir -p "$full_goal_dir"
    write_success "Created goal directory: $goal_dir"
    
    # Get current timestamp
    local timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')
    
    # Create goal.md file with goal structure
    cat > "$full_goal_dir/goal.md" <<EOF
# Goal Statement: $goal_description

**Branch**: \`$goal_dir_name\`
**Created**: $timestamp
**Status**: Draft
**Methodology**: Goal-Driven Development

## 🎯 Goal Definition

**Goal Statement**: $goal_description

**Context**: [Why is this goal important? What problem does it solve?]

**Success Level**: [What "successful goal achievement" looks like]

## 📊 Success Metrics

### Primary Metrics (Must achieve for successful goal completion)

- **Metric 1**: [Measurable outcome 1] - Target: [specific, quantifiable target]
- **Metric 2**: [Measurable outcome 2] - Target: [specific, quantifiable target] 
- **Metric 3**: [Measurable outcome 3] - Target: [specific, quantifiable target]

### Secondary Metrics (Valuable but not required)

- **Metric 1**: [Nice-to-have outcome 1] - Target: [aspirational target]
- **Metric 2**: [Nice-to-have outcome 2] - Target: [aspirational target]

## 🔍 Validation Strategy

### Measurement Approach
- **Data Sources**: [Where to collect metrics from]
- **Measurement Frequency**: [How often to measure progress]
- **Success Thresholds**: [When to consider the goal achieved]

### Learning Objectives
- **What to Learn**: [Key insights to gain from achieving this goal]
- **Adaptation Points**: [When to reconsider the approach]
- **Documentation**: [What information to document for future reference]

## 📝 Goal Breakdown

### Critical Path Activities
- **Activity 1**: [Key activity 1 to achieve the goal]
- **Activity 2**: [Key activity 2 to achieve the goal]
- **Activity 3**: [Key activity 3 to achieve the goal]

### Dependencies
- **Dependency 1**: [What this goal depends on]
- **Dependency 2**: [What this goal depends on]

### Risk Assessment
- **Risk 1**: [Potential risk] - Mitigation: [how to mitigate]
- **Risk 2**: [Potential risk] - Mitigation: [how to mitigate]

## 🔄 Review Process

### Review Schedule
- **Check-ins**: [Regular assessment schedule]
- **Milestone Reviews**: [When to evaluate progress]

### Success Validation
- **[Validation 1]**: [How to confirm goal is achieved]
- **[Validation 2]**: [How to confirm goal is achieved]

## 🏁 Completion Criteria

### Success Indicators
- [ ] Primary metrics achieved at target levels
- [ ] Goal objectives validated through measurement
- [ ] Learning objectives accomplished
- [ ] No major unforeseen issues discovered

### Success Validation
- **[Validation 1]**: [How to confirm goal was successful]
- **[Validation 2]**: [How to confirm goal was successful]

## 🔁 Adaptation Framework

### Regular Review Schedule
- **Weekly**: [Goal effectiveness assessment]
- **When Metrics Diverge**: [How to adjust approach]
- **When Learning Occurs**: [How to incorporate new information]

### Adaptation Triggers
- **Pivot Trigger 1**: [When to change approach]
- **Pause Trigger**: [When to temporarily adjust]
- **Realign Trigger**: [When to reconsider entirely]

---

*This goal definition serves as the foundation for all work related to achieving this objective. All strategies, milestones, and execution should align with these defined success metrics.*
EOF
    
    write_success "Created goal.md with description: $goal_description"
    
    # Create git branch for this goal
    if [ "$verbose" = true ]; then
        write_info "Setting up git branch for this goal..."
    fi
    
    cd "$project_root" || exit 1
    local branch_name
    branch_name=$(new_goal_branch "$goal_dir_name")
    
    # Add and commit the new goal
    git add "$goal_dir" > /dev/null 2>&1
    git commit -m "Add goal: $goal_description

- Created goal definition in $goal_dir/goal.md
- Branch: $branch_name" > /dev/null 2>&1
    
    write_success "Goal committed to branch: $branch_name"
    
    # Update agent context
    update_agent_context > /dev/null 2>&1
    
    # Print summary
    write_success "Goal created successfully!"
    echo
    write_info "Goal Details:"
    echo "  Directory: $goal_dir"
    echo "  Branch: $branch_name"
    echo "  Description: $goal_description"
    echo
    write_info "Next Steps:"
    echo "  1. Navigate to goal directory: cd $goal_dir"
    echo "  2. Complete the goal definition with specific details"
    echo "  3. Use /goalkit.strategies to explore implementation strategies"
    echo "  4. Use /goalkit.milestones to create measurable milestones" 
    echo "  5. Use /goalkit.execute to implement with learning and adaptation"
    echo
    git branch --show-current
}

# Main entry point
main() {
    if [ $# -lt 1 ]; then
        write_error "Goal description is required"
        echo "Usage: $0 <goal_description> [--dry-run] [--force] [--json] [--verbose]"
        exit 1
    fi
    
    create_goal "$@"
}

main "$@"

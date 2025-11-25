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
        handle_error "Not in a git repository. Please run this from the root of a Goal Kit project"
    fi
    
    # Get project root
    local project_root
    project_root=$(get_git_root) || handle_error "Could not determine git root"
    if [ -z "$project_root" ]; then
        handle_error "Could not determine git root. Not in a git repository."
    fi
    
    cd "$project_root" || handle_error "Failed to change to project root: $project_root"
    
    # Check if this is a Goal Kit project
    if [ ! -f ".goalkit/vision.md" ]; then
        handle_error "Not a Goal Kit project. Please run 'goalkeeper init' first to set up the project"
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
            mkdir -p "$goals_dir" || handle_error "Failed to create goals directory: $goals_dir"
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
    mkdir -p "$full_goal_dir" || handle_error "Failed to create goal directory: $full_goal_dir"
    write_success "Created goal directory: $goal_dir"
    
    # Get current timestamp
    local timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')
    
    # Check if template exists, otherwise create default goal.md
    if [ -f "$project_root/.goalkit/templates/goal-template.md" ]; then
        # Create goal.md file using the template
        cat "$project_root/.goalkit/templates/goal-template.md" > "$full_goal_dir/goal.md" || handle_error "Failed to copy goal template"

        # Replace placeholders in the template
        sed -i.bak "s/\[GOAL DESCRIPTION\]/$goal_description/g" "$full_goal_dir/goal.md" || handle_error "Failed to replace placeholders in goal.md"
        sed -i.bak "s/\[###-goal-name\]/$goal_dir_name/g" "$full_goal_dir/goal.md" || handle_error "Failed to replace goal name in goal.md"
        sed -i.bak "s/\[DATE\]/$timestamp/g" "$full_goal_dir/goal.md" || handle_error "Failed to replace date in goal.md"
        rm -f "$full_goal_dir/goal.md.bak" 2>/dev/null || true
    else
        # Fallback to default content if template not found
        cat > "$full_goal_dir/goal.md" <<EOF
# Goal Statement: $goal_description

**Goal Branch**: \`$goal_dir_name\`
**Created**: $timestamp
**Status**: Draft
**Methodology**: Goal-Driven Development

## Beneficiary Scenarios & Validation *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as beneficiary journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY VALIDATABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Validated independently
  - Demonstrated to users independently
-->

### Beneficiary Story 1 - [Brief Title] (Priority: P1)

[Describe this beneficiary journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Validation**: [Describe how this can be validated independently - e.g., "Can be fully validated by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### Beneficiary Story 2 - [Brief Title] (Priority: P2)

[Describe this beneficiary journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Validation**: [Describe how this can be validated independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### Beneficiary Story 3 - [Brief Title] (Priority: P3)

[Describe this beneficiary journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Validation**: [Describe how this can be validated independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more beneficiary stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System/Process MUST [specific capability, e.g., "allow users to achieve goal"]
- **FR-002**: System/Process MUST [specific capability, e.g., "validate success metrics"]
- **FR-003**: Stakeholders MUST be able to [key interaction, e.g., "measure goal progress"]
- **FR-004**: System/Process MUST [data requirement, e.g., "persist goal progress"]
- **FR-005**: System/Process MUST [behavior, e.g., "log all validation events"]

*Example of marking unclear requirements:*

- **FR-006**: System/Process MUST support [NEEDS CLARIFICATION: specific support method not specified - validation approach, measurement method, etc?]
- **FR-007**: System/Process MUST achieve [NEEDS CLARIFICATION: target level not specified - specific metrics not defined]

### Key Entities *(include if goal involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Stakeholders can measure goal progress in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 measurement requests without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of stakeholders successfully validate primary goal on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
EOF
    fi
    
    write_success "Created goal.md with description: $goal_description"
    
    # Create git branch for this goal
    if [ "$verbose" = true ]; then
        write_info "Setting up git branch for this goal..."
    fi
    
    cd "$project_root" || handle_error "Failed to change to project root: $project_root"
    local branch_name
    branch_name=$(new_goal_branch "$goal_dir_name") || handle_error "Failed to create git branch for goal"
    
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

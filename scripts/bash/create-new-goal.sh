#!/bin/bash

# Create a new goal in a Goal Kit project

set -euo pipefail

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Function to display usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS] GOAL_DESCRIPTION

Create a new goal in the current Goal Kit project.

OPTIONS:
    -h, --help              Show this help message
    -d, --dry-run          Show what would be created without creating it
    -v, --verbose          Enable verbose output

ARGUMENTS:
    GOAL_DESCRIPTION       Description of the goal to create

EXAMPLES:
    $0 "Improve user onboarding experience"
    $0 --dry-run "Add user authentication system"
    $0 -v "Build analytics dashboard for user behavior"

EOF
}

# Parse command line arguments
DRY_RUN=false
VERBOSE=false
GOAL_DESCRIPTION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -*)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            if [[ -z "$GOAL_DESCRIPTION" ]]; then
                GOAL_DESCRIPTION="$1"
            else
                GOAL_DESCRIPTION="$GOAL_DESCRIPTION $1"
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [[ -z "$GOAL_DESCRIPTION" ]]; then
    log_error "Goal description is required"
    usage
    exit 1
fi

# Check if we're in a git repository
if ! is_git_repo; then
    log_error "Not in a git repository"
    log_info "Please run this from the root of a Goal Kit project"
    exit 1
fi

# Get project root
PROJECT_ROOT=$(get_git_root)
cd "$PROJECT_ROOT"

# Check if this is a Goal Kit project
if [[ ! -d ".goalkit" ]]; then
    log_error "Not a Goal Kit project"
    log_info "Please run 'goalkeeper init' first to set up the project"
    exit 1
fi

# If JSON mode, output JSON and exit early
if [[ "$JSON_MODE" == "true" ]]; then
    # Find the next goal number
    NEXT_NUMBER=1
    GOALS_DIR="goals"
    if [[ -d "$GOALS_DIR" ]]; then
        # Find the highest numbered goal directory
        for dir in "$GOALS_DIR"/*/; do
            if [[ -d "$dir" ]]; then
                dir_name=$(basename "$dir")
                if [[ "$dir_name" =~ ^[0-9]+- ]]; then
                    num="${dir_name%%-*}"
                    if [[ "$num" -ge "$NEXT_NUMBER" ]]; then
                        NEXT_NUMBER=$((num + 1))
                    fi
                fi
            fi
        done
    fi

    # Create goal directory name
    GOAL_NUMBER=$(printf "%03d" "$NEXT_NUMBER")
    GOAL_DIR_NAME="${GOAL_NUMBER}-$(echo "$GOAL_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')"
    GOAL_DIR="$GOALS_DIR/$GOAL_DIR_NAME"
    GOAL_FILE="$GOAL_DIR/goal.md"
    
    # Output JSON with required variables using common function
    JSON_DATA="{\"GOAL_DIR\":\"$GOAL_DIR\",\"GOAL_FILE\":\"$GOAL_FILE\",\"GOAL_DESCRIPTION\":\"$GOAL_DESCRIPTION\",\"BRANCH_NAME\":\"$GOAL_DIR_NAME\"}"
    output_json_mode "$JSON_DATA"
fi

# Check if goals directory exists
GOALS_DIR="goals"
if [[ ! -d "$GOALS_DIR" ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would create goals directory: $GOALS_DIR"
    else
        mkdir -p "$GOALS_DIR"
        log_success "Created goals directory: $GOALS_DIR"
    fi
fi

# Find the next goal number
NEXT_NUMBER=1
if [[ -d "$GOALS_DIR" ]]; then
    # Find the highest numbered goal directory
    for dir in "$GOALS_DIR"/*/; do
        if [[ -d "$dir" ]]; then
            dir_name=$(basename "$dir")
            if [[ "$dir_name" =~ ^[0-9]+- ]]; then
                num="${dir_name%%-*}"
                if [[ "$num" -ge "$NEXT_NUMBER" ]]; then
                    NEXT_NUMBER=$((num + 1))
                fi
            fi
        fi
    done
fi

# Create goal directory name
GOAL_NUMBER=$(printf "%03d" "$NEXT_NUMBER")
GOAL_DIR_NAME="${GOAL_NUMBER}-$(echo "$GOAL_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')"
GOAL_DIR="$GOALS_DIR/$GOAL_DIR_NAME"

# Check if goal directory already exists
if [[ -d "$GOAL_DIR" ]]; then
    log_error "Goal directory already exists: $GOAL_DIR"
    log_info "Use a different goal description or remove the existing directory"
    exit 1
fi

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "[DRY RUN] Would create goal directory: $GOAL_DIR"
    log_info "[DRY RUN] Would create goal.md with description: $GOAL_DESCRIPTION"
    log_info "[DRY RUN] Would create branch: $GOAL_DIR_NAME"
    exit 0
fi

# Create goal directory
mkdir -p "$GOAL_DIR"
log_success "Created goal directory: $GOAL_DIR"

# Create goal.md file with better structure and guidance
cat > "$GOAL_DIR/goal.md" << EOF
# Goal Definition: ${GOAL_DESCRIPTION}

**Goal Branch**: \`${GOAL_DIR_NAME}\`
**Created**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Status**: Draft
**Vision**: [link to vision document]

## 🎯 Goal Overview

**Goal Statement**: ${GOAL_DESCRIPTION}

**Context**: [Why is this goal important? What problem does it solve?]

**Success Level**: [What "success" looks like for this goal]

## 📊 Success Metrics

### Primary Metrics (Must achieve for success)

- **Metric 1**: [Measurable outcome] - Target: [specific, quantifiable target]
- **Metric 2**: [Measurable outcome] - Target: [specific, quantifiable target]
- **Metric 3**: [Measurable outcome] - Target: [specific, quantifiable target]

### Secondary Metrics (Valuable but not required)

- **Metric 1**: [Nice-to-have outcome] - Target: [aspirational target]
- **Metric 2**: [Nice-to-have outcome] - Target: [aspirational target]

## 👥 Target Users & Stakeholders

### Primary Users
- **[User Type 1]**: [How they benefit from this goal]
- **[User Type 2]**: [How they benefit from this goal]

### Stakeholders
- **[Stakeholder 1]**: [Their interest in this goal]
- **[Stakeholder 2]**: [Their interest in this goal]

## 🎯 Goal Hypotheses

### Key Assumptions
- **Hypothesis 1**: [Testable assumption about user behavior or outcome]
- **Hypothesis 2**: [Testable assumption about technical feasibility]
- **Hypothesis 3**: [Testable assumption about business value]

### Risk Factors
- **Risk 1**: [Potential issue] - Mitigation: [how to address]
- **Risk 2**: [Potential issue] - Mitigation: [how to address]

## 🚀 Goal Milestones

### Milestone 1: [Milestone Title] (Priority: P1)
**Description**: [What this milestone achieves]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]

**Validation Method**: [How to confirm this milestone is achieved]

**Expected Timeline**: [Rough time estimate]

---

### Milestone 2: [Milestone Title] (Priority: P2)
**Description**: [What this milestone achieves]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]

**Validation Method**: [How to confirm this milestone is achieved]

**Expected Timeline**: [Rough time estimate]

---

### Milestone 3: [Milestone Title] (Priority: P3)
**Description**: [What this milestone achieves]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]

**Validation Method**: [How to confirm this milestone is achieved]

**Expected Timeline**: [Rough time estimate]

---

## 🔍 Validation Strategy

### Measurement Approach
- **Data Sources**: [Where to collect metrics from]
- **Measurement Frequency**: [How often to measure]
- **Success Thresholds**: [When to consider the goal achieved]

### Learning Objectives
- **What to Learn**: [Key insights to gain from pursuing this goal]
- **Pivot Points**: [When to reconsider the goal or approach]
- **Documentation**: [What to document for future reference]

## 🎯 Goal Dependencies

### Supports These Goals
- **[Goal 1]**: [How this goal contributes to another goal]
- **[Goal 2]**: [How this goal contributes to another goal]

### Depends on These Goals
- **[Goal 1]**: [What this goal needs from another goal]
- **[Goal 2]**: [What this goal needs from another goal]

## 💡 Strategy Exploration Areas

### Technical Strategies to Explore
- **[Strategy 1]**: [Alternative approach to consider]
- **[Strategy 2]**: [Alternative approach to consider]

### User Experience Strategies to Explore
- **[UX Approach 1]**: [Different way users could achieve this goal]
- **[UX Approach 2]**: [Different way users could achieve this goal]

### Implementation Strategies to Explore
- **[Implementation 1]**: [Different development approach]
- **[Implementation 2]**: [Different development approach]

## 📈 Success Criteria Validation

### Goal Achievement Checklist
- [ ] Primary metrics achieved at target levels
- [ ] User feedback validates the outcome
- [ ] Business impact confirmed through measurement
- [ ] Learning objectives accomplished
- [ ] No significant negative consequences discovered

### Goal Failure Indicators
- [ ] Primary metrics not achievable despite multiple strategies
- [ ] User feedback indicates different needs
- [ ] Business case no longer valid
- [ ] Technical constraints make goal unachievable

## 🔄 Review & Adaptation Points

### Regular Review Schedule
- **After Each Milestone**: [What to review and how]
- **Monthly**: [Strategic review of goal relevance]
- **Quarterly**: [Overall goal effectiveness assessment]

### Adaptation Triggers
- **Pivot Trigger 1**: [When to consider changing approach]
- **Pause Trigger**: [When to temporarily stop pursuing this goal]
- **Abandon Trigger**: [When to stop pursuing this goal entirely]

---

*This goal definition serves as the foundation for strategy exploration and milestone planning. It should be reviewed and updated as learning occurs during implementation.*
EOF

log_success "Created goal.md with description: $GOAL_DESCRIPTION"

# Create git branch for this goal
log_info "Setting up git branch for this goal..."
cd "$PROJECT_ROOT"
BRANCH_NAME=$(create_goal_branch "$GOAL_DIR_NAME")

# Add and commit the new goal
cd "$PROJECT_ROOT"
git add "$GOAL_DIR"
git commit -m "Add goal: $GOAL_DESCRIPTION

- Created goal definition in $GOAL_DIR/goal.md
- Branch: $BRANCH_NAME"

log_success "Goal committed to branch: $BRANCH_NAME"

# Update agent context
update_agent_context

# Print summary
log_success "Goal created successfully!"
echo
log_info "Goal Details:"
echo "  Directory: $GOAL_DIR"
echo "  Branch: $BRANCH_NAME"
echo "  Description: $GOAL_DESCRIPTION"
echo
log_info "Next Steps:"
echo "  1. Navigate to goal directory: cd $GOAL_DIR"
echo "  2. Use /goalkit.strategies to explore implementation approaches"
echo "  3. Use /goalkit.milestones to create measurable milestones"
echo "  4. Use /goalkit.execute to implement with learning and adaptation"
echo
log_info "Current branch is: $(git branch --show-current)"

# Setup goal environment for immediate development
setup_goal_environment "$GOAL_DIR"
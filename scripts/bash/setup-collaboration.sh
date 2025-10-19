#!/bin/bash

# Create a new collaboration plan in a Goal Kit project
# Supports both single-agent coordination and multi-agent coordination

set -euo pipefail

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Function to display usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS] COLLABORATION_DESCRIPTION

Create a new collaboration plan in the current Goal Kit project.

OPTIONS:
    -h, --help              Show this help message
    -d, --dry-run          Show what would be created without creating it
    -v, --verbose          Enable verbose output

ARGUMENTS:
    COLLABORATION_DESCRIPTION       Description of the collaboration to create

EXAMPLES:
    $0 "Coordinate work between frontend and backend agents"
    $0 --dry-run "Maintain consistency across agent interactions"
    $0 -v "Synchronize progress tracking between multiple agents"

EOF
}

# Parse command line arguments
DRY_RUN=false
VERBOSE=false
COLLAB_DESCRIPTION=""

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
            if [[ -z "$COLLAB_DESCRIPTION" ]]; then
                COLLAB_DESCRIPTION="$1"
            else
                COLLAB_DESCRIPTION="$COLLAB_DESCRIPTION $1"
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [[ -z "$COLLAB_DESCRIPTION" ]]; then
    log_error "Collaboration description is required"
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
if [[ ! -f ".goalkit/vision.md" ]]; then
    log_error "Not a Goal Kit project"
    log_info "Please run 'goalkeeper init' first to set up the project"
    exit 1
fi

# If JSON mode, output JSON and exit early
if [[ "$JSON_MODE" == "true" ]]; then
    # Find the next collaboration number (use same numbering as goals)
    NEXT_NUMBER=1
    COLLABS_DIR="collaborations"
    if [[ -d "$COLLABS_DIR" ]]; then
        # Find the highest numbered collaboration directory
        for dir in "$COLLABS_DIR"/*/; do
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

    # Create collaboration directory name
    COLLAB_NUMBER=$(printf "%03d" "$NEXT_NUMBER")
    COLLAB_DIR_NAME="${COLLAB_NUMBER}-$(echo "$COLLAB_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')"
    COLLAB_DIR="$COLLABS_DIR/$COLLAB_DIR_NAME"
    COLLAB_FILE="$COLLAB_DIR/collaboration.md"
    
    # Output JSON with required variables using common function
    JSON_DATA="{\"COLLAB_DIR\":\"$COLLAB_DIR\",\"COLLAB_FILE\":\"$COLLAB_FILE\",\"COLLAB_DESCRIPTION\":\"$COLLAB_DESCRIPTION\",\"BRANCH_NAME\":\"$COLLAB_DIR_NAME\"}"
    output_json_mode "$JSON_DATA"
fi

# Check if collaborations directory exists
COLLABS_DIR="collaborations"
if [[ ! -d "$COLLABS_DIR" ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would create collaborations directory: $COLLABS_DIR"
    else
        mkdir -p "$COLLABS_DIR"
        log_success "Created collaborations directory: $COLLABS_DIR"
    fi
fi

# Find the next collaboration number (use same numbering as goals)
NEXT_NUMBER=1
if [[ -d "$COLLABS_DIR" ]]; then
    # Find the highest numbered collaboration directory
    for dir in "$COLLABS_DIR"/*/; do
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

# Create collaboration directory name
COLLAB_NUMBER=$(printf "%03d" "$NEXT_NUMBER")
COLLAB_DIR_NAME="${COLLAB_NUMBER}-$(echo "$COLLAB_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')"
COLLAB_DIR="$COLLABS_DIR/$COLLAB_DIR_NAME"

# Check if collaboration directory already exists
if [[ -d "$COLLAB_DIR" ]]; then
    log_error "Collaboration directory already exists: $COLLAB_DIR"
    log_info "Use a different collaboration description or remove the existing directory"
    exit 1
fi

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "[DRY RUN] Would create collaboration directory: $COLLAB_DIR"
    log_info "[DRY RUN] Would create collaboration.md with description: $COLLAB_DESCRIPTION"
    log_info "[DRY RUN] Would create branch: $COLLAB_DIR_NAME"
    exit 0
fi

# Create collaboration directory
mkdir -p "$COLLAB_DIR"
log_success "Created collaboration directory: $COLLAB_DIR"

# Create collaboration.md file with coordination structure
cat > "$COLLAB_DIR/collaboration.md" << EOF
# Collaboration Plan: ${COLLAB_DESCRIPTION}

**Branch**: \`${COLLAB_DIR_NAME}\`
**Created**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Mode**: [Single-Agent/Multi-Agent/Self-Coordination]
**Status**: Draft

## 🤝 Collaboration Overview

**Coordination Statement**: ${COLLAB_DESCRIPTION}

**Context**: [Why is this coordination important? What coordination challenge does it solve?]

**Participants**: [List of agents, systems, or processes involved in coordination - use "Self" for single-agent coordination]

**Success Level**: [What \"successful coordination\" looks like for this collaboration]

## 🎯 Coordination Mode

### Selected Mode: [Single-Agent Mode | Multi-Agent Mode | Self-Coordination Mode]

**Mode Justification**: [Why this coordination mode was selected - detected agents, user input, or default behavior]

### Single-Agent Mode Features
- **Self-Consistency**: Maintaining consistency across different interactions with the same agent
- **State Tracking**: Tracking decision state across different sessions
- **Progress Validation**: Validating previous decisions remain valid

### Multi-Agent Mode Features (If Applicable)
- **Agent Awareness**: Agents aware of work done by other agents
- **Conflict Detection**: Identifying potential conflicts between agent work
- **Task Synchronization**: Coordinating work between agents to avoid conflicts
- **Knowledge Sharing**: Agents can access information created by other agents

### Self-Coordination Mode Features
- **State Consistency**: Ensuring the agent maintains consistency with its own previous work
- **Self-Verification**: Checking if previous decisions are still valid
- **Progress Tracking**: Maintaining awareness of own progress over time

## 📊 Coordination Success Metrics

### Primary Metrics (Must achieve for successful coordination)

- **Metric 1**: [Measurable coordination outcome] - Target: [specific, quantifiable target]
- **Metric 2**: [Measurable coordination outcome] - Target: [specific, quantifiable target]
- **Metric 3**: [Measurable coordination outcome] - Target: [specific, quantifiable target]

### Secondary Metrics (Valuable but not required)

- **Metric 1**: [Nice-to-have coordination outcome] - Target: [aspirational target]
- **Metric 2**: [Nice-to-have coordination outcome] - Target: [aspirational target]

## 👥 Coordination Participants & Roles

### Coordination Participants
- **[Participant 1]**: [Role in coordination - what they do]
- **[Participant 2]**: [Role in coordination - what they do]

### Coordination Responsibilities
- **[Responsibility 1]**: [Who handles this coordination task]
- **[Responsibility 2]**: [Who handles this coordination task]

## 🎯 Coordination Activities

### Activity 1: [Activity Title] (Priority: P1)
**Description**: [What this coordination activity achieves]

**Success Indicators**:
- [Measurable coordination outcome 1]
- [Measurable coordination outcome 2]

**Validation Method**: [How to confirm this coordination activity is achieved]

**Expected Timeline**: [Rough time estimate]

**Owner**: [Who is responsible for this activity]

---

### Activity 2: [Activity Title] (Priority: P2)
**Description**: [What this coordination activity achieves]

**Success Indicators**:
- [Measurable coordination outcome 1]
- [Measurable coordination outcome 2]

**Validation Method**: [How to confirm this coordination activity is achieved]

**Expected Timeline**: [Rough time estimate]

**Owner**: [Who is responsible for this activity]

---

### Activity 3: [Activity Title] (Priority: P3)
**Description**: [What this coordination activity achieves]

**Success Indicators**:
- [Measurable coordination outcome 1]
- [Measurable coordination outcome 2]

**Validation Method**: [How to confirm this coordination activity is achieved]

**Expected Timeline**: [Rough time estimate]

**Owner**: [Who is responsible for this activity]

---

## 🔗 Coordination Dependencies

### Coordination Dependencies
- **[Dependency 1]**: [What this coordination depends on]
- **[Dependency 2]**: [What this coordination depends on]

### Coordination Impacts
- **[Impact 1]**: [What this coordination affects]
- **[Impact 2]**: [What this coordination affects]

## 🗣️ Communication Plan

### Communication Channels
- **[Channel 1]**: [How coordination information is shared]
- **[Channel 2]**: [How coordination information is shared]

### Communication Frequency
- **Status Updates**: [How often coordination status is checked/shared]
- **Conflict Resolution**: [How conflicts are communicated and resolved]

### Communication Protocol
- **[Protocol 1]**: [How coordination information is formatted/shared]
- **[Protocol 2]**: [How coordination information is formatted/shared]

## 🔄 Synchronization Points

### Synchronization Events
- **[Event 1]**: [When coordination alignment happens]
- **[Event 2]**: [When coordination alignment happens]

### Synchronization Process
- **[Process 1]**: [How coordination alignment is achieved]
- **[Process 2]**: [How coordination alignment is achieved]

## ⚠️ Conflict Resolution

### Potential Conflicts
- **[Conflict 1]**: [What could go wrong in coordination]
- **[Conflict 2]**: [What could go wrong in coordination]

### Resolution Approaches
- **[Approach 1]**: [How to resolve this type of conflict]
- **[Approach 2]**: [How to resolve this type of conflict]

## 📈 Coordination Validation Strategy

### Measurement Approach
- **Data Sources**: [Where to collect coordination metrics from]
- **Measurement Frequency**: [How often to measure coordination effectiveness]
- **Success Thresholds**: [When to consider the coordination successful]

### Learning Objectives
- **What to Learn**: [Key insights to gain from coordination]
- **Adaptation Points**: [When to reconsider the coordination approach]
- **Documentation**: [What coordination information to document for future reference]

## 📋 Coordination Checkpoints

### Coordination Milestones
- **[Milestone 1]**: [Coordination achievement to reach]
- **[Milestone 2]**: [Coordination achievement to reach]

### Coordination Verification Points
- **[Verification 1]**: [When to verify coordination is working properly]
- **[Verification 2]**: [When to verify coordination is working properly]

## 🚀 Coordination Implementation

### Setup Requirements
- **[Requirement 1]**: [What needs to be set up for coordination]
- **[Requirement 2]**: [What needs to be set up for coordination]

### Implementation Steps
1. **Step 1**: [First step in coordination implementation]
2. **Step 2**: [Second step in coordination implementation]
3. **Step 3**: [Third step in coordination implementation]

## 🏁 Coordination Completion Criteria

### Success Indicators
- [ ] Primary coordination metrics achieved at target levels
- [ ] Coordination objectives validated through measurement
- [ ] All coordination participants aligned and informed
- [ ] No significant coordination conflicts discovered
- [ ] Coordination learning objectives accomplished

### Success Validation
- **[Validation 1]**: [How to confirm coordination was successful]
- **[Validation 2]**: [How to confirm coordination was successful]

## 🔁 Coordination Review & Adaptation

### Regular Review Schedule
- **After Each Activity**: [What to review and how]
- **Weekly**: [Coordination effectiveness assessment]
- **When Conflicts Arise**: [How to reassess coordination approach]

### Adaptation Triggers
- **Pivot Trigger 1**: [When to change coordination approach]
- **Pause Trigger**: [When to temporarily adjust coordination]
- **Realign Trigger**: [When to reconsider coordination strategy entirely]

## 🔄 Coordination State Management

### State Tracking
- **[State Element 1]**: [What coordination state is tracked]
- **[State Element 2]**: [What coordination state is tracked]

### State Validation
- **[Validation 1]**: [How to ensure coordination state is valid]
- **[Validation 2]**: [How to ensure coordination state is valid]

---

*This collaboration plan serves as the foundation for coordinated work between agents or for maintaining consistency in single-agent environments. It should be reviewed and updated as coordination needs evolve during implementation.*
EOF

log_success "Created collaboration.md with description: $COLLAB_DESCRIPTION"

# Get current persona for the collaboration
CURRENT_PERSONA="general"
PERSONA_CONFIG_DIR="$PROJECT_ROOT/.goalkit/personas"
CURRENT_PERSONA_FILE="$PERSONA_CONFIG_DIR/current_persona.txt"
if [[ -f "$CURRENT_PERSONA_FILE" ]]; then
    CURRENT_PERSONA=$(cat "$CURRENT_PERSONA_FILE")
fi

# Create git branch for this collaboration
log_info "Setting up git branch for this collaboration..."
cd "$PROJECT_ROOT"
BRANCH_NAME=$(create_goal_branch "$COLLAB_DIR_NAME")  # Reuse goal branch function

# Add and commit the new collaboration
cd "$PROJECT_ROOT"
git add "$COLLAB_DIR"
git commit -m "Add collaboration: $COLLAB_DESCRIPTION

- Created collaboration definition in $COLLAB_DIR/collaboration.md
- Branch: $BRANCH_NAME
- Active persona: $CURRENT_PERSONA"

log_success "Collaboration committed to branch: $BRANCH_NAME"

# Update agent context
update_agent_context

# Print summary
log_success "Collaboration created successfully!"
echo
log_info "Collaboration Details:"
echo "  Directory: $COLLAB_DIR"
echo "  Branch: $BRANCH_NAME"
echo "  Description: $COLLAB_DESCRIPTION"
echo
log_info "Next Steps:"
echo "  1. Navigate to collaboration directory: cd $COLLAB_DIR"
echo "  2. Complete the collaboration plan with specific details"
echo "  3. Use coordination features as needed during development"
echo
log_info "Current branch is: $(git branch --show-current)"

# Setup collaboration environment for immediate development
setup_goal_environment "$COLLAB_DIR"
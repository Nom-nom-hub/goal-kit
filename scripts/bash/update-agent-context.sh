#!/bin/bash
# Update agent context files with latest project information
# This script updates all agent context files (.claude/context.md, CLAUDE.md, etc.)
# with current project state, active goals, and vision information

# Get the script directory and source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# Parse arguments
JSON_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --json|-j)
            JSON_MODE=true
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
PROJECT_ROOT=$(get_git_root) || handle_error "Could not determine git root"
if [ -z "$PROJECT_ROOT" ]; then
    handle_error "Could not determine git root. Not in a git repository."
fi

cd "$PROJECT_ROOT" || handle_error "Failed to change to project root: $PROJECT_ROOT"

# Check if this is a Goal Kit project
VISION_FILE=".goalkit/vision.md"
if [ ! -f "$VISION_FILE" ]; then
    handle_error "Not a Goal Kit project. Please run 'goalkeeper init' first to set up the project"
fi

# If JSON mode, output JSON and exit early
if [ "$JSON_MODE" = true ]; then
    cat << EOF
{"STATUS":"context-updated","PROJECT_ROOT":"$PROJECT_ROOT"}
EOF
    exit 0
fi

# Define context files to update
CONTEXT_FILES=(
    "CLAUDE.md"
    ".claude/context.md"
    "GEMINI.md"
    ".gemini/context.md"
    "CURSOR.md"
    ".cursor/context.md"
    "QWEN.md"
    ".qwen/context.md"
    "WINDSURF.md"
    ".windsurf/context.md"
    "KILOCODE.md"
    ".kilocode/context.md"
    "ROO.md"
    ".roo/context.md"
    "CODEBUDDY.md"
    ".codebuddy/context.md"
    "Q.md"
    ".amazonq/context.md"
    "OPENCODE.md"
    "AUGMENT.md"
    ".augment/context.md"
)

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

# Count active goals
ACTIVE_GOALS=0
if [ -d "goals" ]; then
    ACTIVE_GOALS=$(find goals -maxdepth 1 -type d ! -name "goals" 2>/dev/null | wc -l)
fi

# Get timestamp
TIMESTAMP=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
TIMESTAMP_LOCAL=$(date +'%Y-%m-%d %H:%M:%S')

FOUND_CONTEXT_FILE=false

for CONTEXT_FILE in "${CONTEXT_FILES[@]}"; do
    if [ -f "$CONTEXT_FILE" ]; then
        FOUND_CONTEXT_FILE=true
        write_info "Updating context in $CONTEXT_FILE"
        
        # Create context content
        CONTEXT_CONTENT="# Goal Kit Project Context

**Project**: $(basename "$PROJECT_ROOT")
**Branch**: $CURRENT_BRANCH
**Active Goals**: $ACTIVE_GOALS
**Updated**: $TIMESTAMP

## 🎯 Goal-Driven Development Status

This project uses Goal-Driven Development methodology. Focus on:
- Measurable outcomes over feature specifications
- Multiple strategy exploration before implementation
- Learning and adaptation during execution
- Success metrics validation

## 📋 Available Commands

### Core Commands
- **/goalkit.vision** - Establish project vision and principles
- **/goalkit.goal** - Define goals and success criteria
- **/goalkit.strategies** - Explore implementation strategies
- **/goalkit.milestones** - Create measurable milestones
- **/goalkit.execute** - Execute with learning and adaptation

## 🚀 Project Vision

"

        # Add vision content if it exists
        if [ -f "$VISION_FILE" ]; then
            VISION_LINES=$(grep -v "^#" "$VISION_FILE" 2>/dev/null | head -10 || true)
            CONTEXT_CONTENT+="$VISION_LINES"
        fi
        
        CONTEXT_CONTENT+="

## 🎯 Active Goals

"
        
        # Add goal information
        if [ -d "goals" ]; then
            GOAL_COUNT=$(find goals -maxdepth 1 -type d ! -name "goals" 2>/dev/null | wc -l)
            if [ "$GOAL_COUNT" -gt 0 ]; then
                CONTEXT_CONTENT+="Recent goals:\n"
                find goals -maxdepth 1 -type d ! -name "goals" 2>/dev/null | sort | head -3 | while read GOAL_DIR; do
                    GOAL_NAME=$(basename "$GOAL_DIR")
                    CONTEXT_CONTENT+="- **$GOAL_NAME**: Goal in progress\n"
                done
            else
                CONTEXT_CONTENT+="No active goals yet. Use /goalkit.goal to create your first goal.\n"
            fi
        else
            CONTEXT_CONTENT+="No active goals yet. Use /goalkit.goal to create your first goal.\n"
        fi
        
        CONTEXT_CONTENT+="## 📊 Development Principles

Remember these core principles:
1. **Outcome-First**: Prioritize user and business outcomes
2. **Strategy Flexibility**: Multiple valid approaches exist for any goal
3. **Measurement-Driven**: Progress must be measured and validated
4. **Learning Integration**: Treat implementation as hypothesis testing
5. **Adaptive Planning**: Change course based on evidence

## 🔧 Next Recommended Actions

"
        
        if [ ! -d "goals" ] || [ $(find goals -maxdepth 1 -type d ! -name "goals" 2>/dev/null | wc -l) -eq 0 ]; then
            CONTEXT_CONTENT+="1. Use /goalkit.vision to establish project vision
2. Use /goalkit.goal to define first goal
"
        else
            CONTEXT_CONTENT+="1. Review active goals in goals/ directory
2. Use /goalkit.strategies to explore implementation approaches
3. Use /goalkit.milestones to plan measurable progress steps
"
        fi
        
        CONTEXT_CONTENT+="

---

*This context is automatically updated by update-agent-context.sh. Last updated: $TIMESTAMP_LOCAL*
"
        
        # Write context file
        echo -e "$CONTEXT_CONTENT" > "$CONTEXT_FILE"
    fi
done

if [ "$FOUND_CONTEXT_FILE" = false ]; then
    write_warning "No agent context file found to update"
    exit 0
fi

write_success "Agent context files updated"
write_host ""
write_info "Context Update Complete:"
write_host "  Project: $(basename "$PROJECT_ROOT")"
write_host "  Location: $PROJECT_ROOT"
write_host "  Updated: $TIMESTAMP_LOCAL"

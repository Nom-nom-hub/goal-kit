#!/bin/bash

# Create or edit the vision document in a Goal Kit project

set -e

VISION_DESCRIPTION="${1:-}"
EDIT=false
FORCE=false
JSON=false
VERBOSE=false

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --edit)
            EDIT=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --json)
            JSON=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            VISION_DESCRIPTION="$1"
            shift
            ;;
    esac
done

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    write_error "Not in a git repository"
    write_info "Please run this from the root of a Goal Kit project"
    exit 1
fi

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

# Check if this is a Goal Kit project
VISION_FILE=".goalkit/vision.md"
if [ ! -f "$VISION_FILE" ]; then
    # If JSON mode, output JSON even for new project
    if [ "$JSON" = true ]; then
        echo '{"VISION_FILE":"'"$VISION_FILE"'","VISION_DIR":".goalkit"}'
        return 0
    fi
fi

# If JSON mode, output JSON with file path
if [ "$JSON" = true ]; then
    echo '{"VISION_FILE":"'"$VISION_FILE"'","VISION_DIR":".goalkit"}'
    exit 0
fi

# Check if vision file already exists
if [ -f "$VISION_FILE" ]; then
    if [ "$EDIT" = true ] || [ "$VERBOSE" = true ]; then
        if [ "$VERBOSE" = true ]; then
            write_info "Opening vision file for editing..."
        fi
        # Open in default editor
        if command -v code &> /dev/null; then
            code "$VISION_FILE"
        elif command -v nano &> /dev/null; then
            nano "$VISION_FILE"
        else
            vi "$VISION_FILE"
        fi
        exit 0
    elif [ "$FORCE" = false ]; then
        write_warning "Vision file already exists: $VISION_FILE"
        write_info "Use --edit to open in editor or --force to overwrite"
        exit 0
    fi
fi

# Create .goalkit directory if it doesn't exist
mkdir -p ".goalkit"

# Get timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Check if template exists
TEMPLATE_PATH=".goalkit/templates/vision-template.md"
if [ -f "$TEMPLATE_PATH" ]; then
    VISION_CONTENT=$(cat "$TEMPLATE_PATH")
    
    # Replace placeholders if description provided
    if [ -n "$VISION_DESCRIPTION" ]; then
        VISION_CONTENT="${VISION_CONTENT//\[PROJECT NAME\]/$VISION_DESCRIPTION}"
    fi
    
    VISION_CONTENT="${VISION_CONTENT//\[DATE\]/$TIMESTAMP}"
else
    # Fallback to default content
    PROJECT_NAME="${VISION_DESCRIPTION:-$(basename "$PROJECT_ROOT")}"
    
    VISION_CONTENT="# Vision: $PROJECT_NAME

**Created**: $TIMESTAMP
**Last Updated**: $TIMESTAMP

## Vision Statement

[Define the overarching vision for this project - what are we trying to achieve and why does it matter?]

## Core Principles

1. **[Principle 1]**: [Explain what this principle means for the project]
2. **[Principle 2]**: [Explain what this principle means for the project]
3. **[Principle 3]**: [Explain what this principle means for the project]

## Success Definition

What will success look like for this vision? Define the key indicators:

- **Market/User Impact**: [Describe the impact on target users or market]
- **Quality Metrics**: [Describe quality standards and expectations]
- **Timeline**: [Rough timeline for vision realization]
- **Team/Resource Impact**: [How this affects the team or organization]

## Strategic Goals

These are the major stepping stones to realize the vision:

1. **[Strategic Goal 1]**: [Description and why it's important]
2. **[Strategic Goal 2]**: [Description and why it's important]
3. **[Strategic Goal 3]**: [Description and why it's important]

## Constraints & Considerations

- **Technical Constraints**: [List any technical limitations or considerations]
- **Resource Constraints**: [List resource limitations]
- **Timeline Constraints**: [Any time-related constraints]
- **Regulatory/Compliance**: [Any compliance or legal considerations]

## Next Steps

1. Refine and validate this vision with stakeholders
2. Define specific goals aligned with this vision
3. Create measurable milestones for progress tracking
4. Communicate the vision clearly to all team members
"
fi

# Write vision file
echo "$VISION_CONTENT" > "$VISION_FILE"
write_success "Created vision.md: $VISION_FILE"

# Git operations
git add "$VISION_FILE" 2>/dev/null || true
git commit -m "Add project vision" 2>/dev/null || true

write_success "Vision committed to repository"

# Print summary
echo ""
write_info "Vision file created successfully!"
echo "  File: $VISION_FILE"
echo ""
write_info "Next Steps:"
echo "  1. Edit the vision file to add your project details"
echo "  2. Define core principles and success criteria"
echo "  3. Use /goalkit.goal to define specific goals"
echo "  4. Use /goalkit.strategies to plan implementation approaches"
echo ""

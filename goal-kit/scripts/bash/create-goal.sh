#!/bin/bash

# Goal-Kit Goal Creation Script
# Creates new goal projects with proper structure and templates

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOAL_KIT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
TEMPLATES_DIR="$GOAL_KIT_DIR/templates"
DEFAULT_GOAL_DIR="$HOME/goals"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Utility functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Help function
show_help() {
    cat << EOF
Goal-Kit Goal Creation Script

USAGE:
    $0 [OPTIONS] GOAL_NAME

OPTIONS:
    -c, --category CATEGORY    Goal category (personal, business, learning, software, research)
    -p, --priority PRIORITY    Priority level (low, medium, high, critical)
    -d, --deadline DEADLINE    Target completion date (YYYY-MM-DD)
    -t, --template TEMPLATE    Template to use (standard, learning-goal, business-goal, etc.)
    -o, --output-dir DIR       Output directory (default: ~/goals)
    -v, --verbose              Verbose output
    -h, --help                 Show this help message

EXAMPLES:
    $0 "Learn Python Data Science" -c learning -p high -d 2024-12-31
    $0 "Launch SaaS Product" -c business -t business-goal -o ./projects
    $0 "Build Mobile App" -c software -p high -v

EOF
}

# Validate dependencies
check_dependencies() {
    local missing_deps=()

    if ! command -v jq &> /dev/null; then
        missing_deps+=("jq")
    fi

    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install the missing dependencies and try again."
        exit 1
    fi
}

# Validate input parameters
validate_input() {
    local goal_name="$1"

    if [ -z "$goal_name" ]; then
        log_error "Goal name is required"
        show_help
        exit 1
    fi

    # Validate goal name format (no special characters except spaces, hyphens, underscores)
    if [[ ! "$goal_name" =~ ^[a-zA-Z0-9[:space:]_-]+$ ]]; then
        log_error "Goal name contains invalid characters. Use only letters, numbers, spaces, hyphens, and underscores."
        exit 1
    fi
}

# Parse command line arguments
parse_arguments() {
    GOAL_NAME=""
    CATEGORY="personal"
    PRIORITY="medium"
    DEADLINE=""
    TEMPLATE="standard"
    OUTPUT_DIR="$DEFAULT_GOAL_DIR"
    VERBOSE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--category)
                CATEGORY="$2"
                shift 2
                ;;
            -p|--priority)
                PRIORITY="$2"
                shift 2
                ;;
            -d|--deadline)
                DEADLINE="$2"
                shift 2
                ;;
            -t|--template)
                TEMPLATE="$2"
                shift 2
                ;;
            -o|--output-dir)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -*)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                if [ -z "$GOAL_NAME" ]; then
                    GOAL_NAME="$1"
                else
                    log_error "Multiple goal names specified. Please provide only one goal name."
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done

    validate_input "$GOAL_NAME"
}

# Validate template exists
validate_template() {
    local template="$1"
    local template_file="$TEMPLATES_DIR/${template}.json"

    if [ ! -f "$template_file" ]; then
        log_error "Template '$template' not found in $TEMPLATES_DIR"
        log_info "Available templates:"
        ls "$TEMPLATES_DIR"/*.json | sed 's|.*/||' | sed 's|\.json||' | sed 's/^/  - /'
        exit 1
    fi

    if [ "$VERBOSE" = true ]; then
        log_info "Using template: $template_file"
    fi
}

# Create goal directory structure
create_goal_structure() {
    local goal_name="$1"
    local output_dir="$2"
    local goal_dir="$output_dir/$goal_name"

    if [ -d "$goal_dir" ]; then
        log_error "Goal directory already exists: $goal_dir"
        log_info "Use a different name or remove the existing directory."
        exit 1
    fi

    log_info "Creating goal directory structure..."

    # Create main directory
    mkdir -p "$goal_dir"

    # Create subdirectories
    mkdir -p "$goal_dir/milestones"
    mkdir -p "$goal_dir/achievements"
    mkdir -p "$goal_dir/progress"
    mkdir -p "$goal_dir/templates"
    mkdir -p "$goal_dir/docs"

    if [ "$VERBOSE" = true ]; then
        log_success "Created directory structure at: $goal_dir"
    fi
}

# Generate goal ID
generate_goal_id() {
    local goal_name="$1"
    local timestamp=$(date +%Y%m%d%H%M%S)
    local short_name=$(echo "$goal_name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | cut -c1-20)
    echo "goal-${timestamp}-${short_name}"
}

# Create goal configuration file
create_goal_file() {
    local goal_name="$1"
    local goal_id="$2"
    local category="$3"
    local priority="$4"
    local deadline="$5"
    local template="$6"
    local goal_dir="$7"
    local goal_file="$goal_dir/goal.json"

    log_info "Creating goal configuration file..."

    # Read template file
    local template_file="$TEMPLATES_DIR/${template}.json"
    local template_content=$(cat "$template_file")

    # Update template with goal-specific information
    local created_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local defined_at="$created_at"

    # Use jq to update the JSON
    local updated_content=$(echo "$template_content" | jq \
        --arg name "$goal_name" \
        --arg category "$category" \
        --arg priority "$priority" \
        --arg deadline "$deadline" \
        --arg created_at "$created_at" \
        --arg defined_at "$defined_at" \
        --arg goal_id "$goal_id" \
        '.name = $name |
         .metadata.template = "'$template'" |
         .created_at = $created_at |
         .defined_at = $defined_at |
         .deadline = $deadline |
         .category = $category |
         .priority = $priority')

    # Write the updated content to the goal file
    echo "$updated_content" > "$goal_file"

    if [ "$VERBOSE" = true ]; then
        log_success "Created goal file: $goal_file"
    fi
}

# Initialize git repository
initialize_git_repo() {
    local goal_dir="$1"
    local goal_name="$2"

    log_info "Initializing Git repository..."

    cd "$goal_dir"

    # Initialize git repo
    git init --quiet

    # Create .gitignore
    cat > .gitignore << 'EOF'
# Goal-Kit specific
*.log
*.tmp
.DS_Store
Thumbs.db

# Progress and temporary files
progress/auto-save-*
temp/
cache/

# Sensitive data
.env
.env.local
secrets.json

# OS generated files
*.swp
*.swo
*~
EOF

    # Initial commit
    git add .
    git commit -m "Initial goal setup: $goal_name" --quiet

    if [ "$VERBOSE" = true ]; then
        log_success "Git repository initialized"
    fi
}

# Create README file
create_readme() {
    local goal_name="$1"
    local goal_dir="$2"
    local readme_file="$goal_dir/README.md"

    log_info "Creating README file..."

    cat > "$readme_file" << EOF
# $goal_name

## Goal Overview

**Goal ID:** [Generated ID]
**Category:** $CATEGORY
**Priority:** $PRIORITY
**Created:** $(date +%Y-%m-%d)
$(if [ -n "$DEADLINE" ]; then echo "**Deadline:** $DEADLINE"; fi)

## Description

[Goal description will be added here]

## Progress Tracking

- **Milestones:** [Number] defined milestones
- **Status:** Active
- **Progress:** 0%

## Getting Started

1. Review the goal definition in \`goal.json\`
2. Check milestones in the \`milestones/\` directory
3. Update progress regularly using progress tracking tools
4. Commit changes to track your journey

## Directory Structure

\`\`\`
$goal_name/
├── goal.json              # Main goal configuration
├── README.md              # This file
├── milestones/            # Milestone definitions
├── achievements/          # Achievement documentation
├── progress/              # Progress reports and metrics
├── templates/             # Goal-specific templates
└── docs/                  # Additional documentation
\`\`\`

## Quick Commands

\`\`\`bash
# Update progress
goal progress update --progress 25

# Add new milestone
goal milestone add "New Milestone" --duration 2

# Generate progress report
goal progress report --format markdown
\`\`\`

## Notes

- Keep this README updated with important information
- Use the milestones directory to track major achievements
- Regular progress updates help maintain momentum
- Celebrate achievements as you reach them!

---

*Created with Goal-Kit on $(date +%Y-%m-%d)*
EOF

    if [ "$VERBOSE" = true ]; then
        log_success "Created README file: $readme_file"
    fi
}

# Main execution
main() {
    log_info "Goal-Kit Goal Creation Script v1.0"
    log_info "=================================="

    # Parse arguments
    parse_arguments "$@"

    # Check dependencies
    check_dependencies

    # Validate template
    validate_template "$TEMPLATE"

    # Create directory structure
    create_goal_structure "$GOAL_NAME" "$OUTPUT_DIR"

    # Generate goal ID
    local goal_id=$(generate_goal_id "$GOAL_NAME")

    # Get full path for goal directory
    local goal_dir="$OUTPUT_DIR/$GOAL_NAME"

    # Create goal configuration
    create_goal_file "$GOAL_NAME" "$goal_id" "$CATEGORY" "$PRIORITY" "$DEADLINE" "$TEMPLATE" "$goal_dir"

    # Initialize git repository
    initialize_git_repo "$goal_dir" "$GOAL_NAME"

    # Create README
    create_readme "$GOAL_NAME" "$goal_dir"

    # Success message
    log_success "Goal project '$GOAL_NAME' created successfully!"
    log_info "Location: $goal_dir"
    log_info "Goal ID: $goal_id"
    log_info ""
    log_info "Next steps:"
    log_info "1. Review and customize your goal in: $goal_dir/goal.json"
    log_info "2. Start working on the first milestone"
    log_info "3. Update progress regularly"
    log_info "4. Use 'goal progress' commands to track your journey"
    log_info ""
    log_info "Happy goal achievement! 🎯"
}

# Run main function with all arguments
main "$@"
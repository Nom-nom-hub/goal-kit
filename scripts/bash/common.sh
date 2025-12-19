#!/bin/bash
# Common utilities for Goal Kit bash scripts

# Strict error handling
set -o pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Global error flag
SCRIPT_ERROR=0
TEMP_FILES=()

# Cleanup function
cleanup() {
    local exit_code=$?
    
    # Remove temporary files
    for temp_file in "${TEMP_FILES[@]}"; do
        if [ -f "$temp_file" ] || [ -d "$temp_file" ]; then
            rm -rf "$temp_file" 2>/dev/null || true
        fi
    done
    
    if [ $exit_code -ne 0 ] && [ $SCRIPT_ERROR -eq 0 ]; then
        write_error "Script failed with exit code $exit_code"
    fi
    
    exit $exit_code
}

# Register cleanup
trap cleanup EXIT

# Error handling function
handle_error() {
    local message="$1"
    local exit_code="${2:-1}"
    local line_number="${3:-$LINENO}"
    
    SCRIPT_ERROR=1
    write_error "$message (line $line_number)"
    exit $exit_code
}

# Output functions with colors
write_colored() {
    local message="$1"
    local color="${2:-${NC}}"
    echo -e "${color}${message}${NC}"
}

write_info() {
    write_colored "[INFO] $1" "${BLUE}"
}

write_success() {
    write_colored "[SUCCESS] $1" "${GREEN}"
}

write_warning() {
    write_colored "[WARNING] $1" "${YELLOW}"
}

write_error() {
    write_colored "[ERROR] $1" "${RED}" >&2
}

write_step() {
    write_colored "[STEP] $1" "${CYAN}"
}

write_goal() {
    write_colored "[GOAL] $1" "${MAGENTA}"
}

# Git utilities
test_git_repo() {
    git rev-parse --git-dir > /dev/null 2>&1
    return $?
}

get_git_root() {
    # First try git command
    if test_git_repo; then
        git rev-parse --show-toplevel 2>/dev/null
        return $?
    fi
    
    # Fallback: look for .goalkit directory
    local current_dir="$(pwd)"
    while [ "$current_dir" != "/" ]; do
        if [ -d "$current_dir/.goalkit" ]; then
            echo "$current_dir"
            return 0
        fi
        current_dir="$(dirname "$current_dir")"
    done
    
    return 1
}

# Command existence check
test_command_exists() {
    command -v "$1" > /dev/null 2>&1
    return $?
}

# Validate command exists or exit
require_command() {
    local command="$1"
    local install_hint="${2:-}"
    
    if ! test_command_exists "$command"; then
        write_error "Required command not found: $command"
        if [ -n "$install_hint" ]; then
            write_info "Install it using: $install_hint"
        fi
        exit 1
    fi
}

# Validate file exists
require_file() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        handle_error "Required file not found: $file"
    fi
}

# Validate directory exists
require_directory() {
    local directory="$1"
    
    if [ ! -d "$directory" ]; then
        handle_error "Required directory not found: $directory"
    fi
}

# Create directory with proper error handling
create_directory_safe() {
    local directory="$1"
    
    if [ -d "$directory" ]; then
        return 0
    fi
    
    # Create parent directories if needed
    local parent_dir
    parent_dir="$(dirname "$directory")"
    if [ ! -d "$parent_dir" ]; then
        create_directory_safe "$parent_dir" || return 1
    fi
    
    if ! mkdir -p "$directory" 2>/dev/null; then
        write_error "Failed to create directory: $directory"
        return 1
    fi
    
    return 0
}

# Validate writable path
validate_writable() {
    local path="$1"
    local parent_dir=$(dirname "$path")
    
    # Create parent directory if it doesn't exist for validation
    if [ ! -d "$parent_dir" ]; then
        write_error "Parent directory does not exist: $parent_dir"
        return 1
    fi
    
    if [ ! -w "$parent_dir" ]; then
        write_error "Directory is not writable: $parent_dir"
        write_info "Check file permissions: ls -ld $parent_dir"
        return 1
    fi
    
    return 0
}

# Register temporary file for cleanup
register_temp_file() {
    TEMP_FILES+=("$1")
}

# Check for required tools
test_prerequisites() {
    local missing_tools=()
    
    if ! test_command_exists "git"; then
        missing_tools+=("git")
    fi
    
    if ! test_command_exists "uv"; then
        missing_tools+=("uv")
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        write_error "Missing required tools: ${missing_tools[*]}"
        write_info "Please install the missing tools and try again."
        exit 1
    fi
    
    write_success "All prerequisites are installed"
}

# Create new goal branch
new_goal_branch() {
    local goal_name="$1"
    local branch_name="$goal_name"
    
    # Check if branch already exists
    if git rev-parse --verify "$branch_name" > /dev/null 2>&1; then
        write_info "Branch $branch_name already exists, switching to it"
        git checkout "$branch_name" || {
            write_error "Failed to switch to branch: $branch_name"
            exit 1
        }
    else
        write_info "Creating new branch: $branch_name"
        git checkout -b "$branch_name" || {
            write_error "Failed to create branch: $branch_name"
            exit 1
        }
    fi
    
    echo "$branch_name"
}

# Update agent context
update_agent_context() {
    local project_root
    project_root=$(get_git_root)
    
    if [ $? -ne 0 ] || [ -z "$project_root" ]; then
        write_error "Could not determine git root. Not in a git repository."
        return 1
    fi
    
    local context_files=(
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
    
    local current_branch
    current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    
    local active_goals=0
    if [ -d "$project_root/goals" ]; then
        active_goals=$(find "$project_root/goals" -maxdepth 1 -type d ! -name "goals" | wc -l)
    fi
    
    local found_context_file=0
    local context_file
    for context_file in "${context_files[@]}"; do
        local full_path="$project_root/$context_file"
        if [ -f "$full_path" ]; then
            write_info "Updating context in $context_file"
            found_context_file=1
            
            local context_content="# Goal Kit Project Context

**Project**: $(basename "$project_root")
**Branch**: $current_branch
**Active Goals**: $active_goals
**Updated**: $(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')

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
            local vision_path="$project_root/.goalkit/vision.md"
            if [ -f "$vision_path" ]; then
                head -n 10 "$vision_path" | grep -v "^#" >> /tmp/context_$$.txt
                context_content+=$(cat /tmp/context_$$.txt)
                rm -f /tmp/context_$$.txt
            fi
            
            context_content+="

## 🎯 Active Goals

"
            
            # Add goal information
            local goals_dir="$project_root/goals"
            if [ -d "$goals_dir" ]; then
                local goal_dirs=($(find "$goals_dir" -maxdepth 1 -type d ! -name "goals" | sort | head -n 3))
                if [ ${#goal_dirs[@]} -gt 0 ]; then
                    context_content+="Recent goals:
"
                    for goal_path in "${goal_dirs[@]}"; do
                        local goal_file="$goal_path/goal.md"
                        if [ -f "$goal_file" ]; then
                            local goal_dir_name=$(basename "$goal_path")
                            context_content+="- **$goal_dir_name**: Goal definition in progress
"
                        fi
                    done
                else
                    context_content+="No active goals yet. Use /goalkit.goal to create your first goal.
"
                fi
            else
                context_content+="No active goals yet. Use /goalkit.goal to create your first goal.
"
            fi
            
            context_content+="## 📊 Development Principles

Remember these core principles:
1. **Outcome-First**: Prioritize user and business outcomes
2. **Strategy Flexibility**: Multiple valid approaches exist for any goal
3. **Measurement-Driven**: Progress must be measured and validated
4. **Learning Integration**: Treat implementation as hypothesis testing
5. **Adaptive Planning**: Change course based on evidence

## 🔧 Next Recommended Actions

"
            
            if [ ! -d "$goals_dir" ] || [ $(find "$goals_dir" -maxdepth 1 -type d ! -name "goals" | wc -l) -eq 0 ]; then
                context_content+="1. Use /goalkit.vision to establish project vision
2. Use /goalkit.goal to define first goal
"
            else
                context_content+="1. Review active goals in goals/ directory
2. Use /goalkit.strategies to explore implementation approaches
3. Use /goalkit.milestones to plan measurable progress steps
"
            fi
            
            context_content+="
---

*This context is automatically updated by update-agent-context.sh. Last updated: $(date +'%Y-%m-%d %H:%M:%S')*

"
            
            echo -n "$context_content" > "$full_path"
            break
        fi
    done
    
    if [ $found_context_file -eq 0 ]; then
        write_warning "No agent context file found to update"
        return 1
    fi
    
    return 0
}

# Validate goal context
test_goal_context() {
    local current_dir
    current_dir=$(pwd)
    
    if [[ "$current_dir" != *"goals"* ]]; then
        write_error "Not in a goal directory"
        write_info "Please navigate to a goal directory (e.g., goals/001-user-authentication/)"
        exit 1
    fi
    
    if [ ! -f "goal.md" ]; then
        write_error "Missing required file: goal.md"
        exit 1
    fi
    
    write_success "Goal context validated"
}

# Setup goal environment
set_goal_environment() {
    local goal_dir="$1"
    local project_root
    project_root=$(get_git_root)
    
    if [ $? -ne 0 ] || [ -z "$project_root" ]; then
        write_error "Could not determine git root. Not in a git repository."
        return 1
    fi
    
    # Resolve goal_dir to absolute path if relative
    if [[ ! "$goal_dir" = /* ]]; then
        goal_dir="$project_root/$goal_dir"
    fi
    goal_dir="$(cd "$goal_dir" 2>/dev/null && pwd)" || {
        write_error "Goal directory does not exist: $goal_dir"
        return 1
    }
    
    local goal_name
    goal_name=$(basename "$goal_dir")
    
    export GOAL_KIT_PROJECT_ROOT="$project_root"
    export GOAL_KIT_GOAL_DIR="$goal_dir"
    export GOAL_KIT_GOAL_NAME="$goal_name"
    
    write_info "Goal environment configured"
    write_info "  Project Root: $project_root"
    write_info "  Goal Directory: $goal_dir"
    write_info "  Goal Name: $goal_name"
}

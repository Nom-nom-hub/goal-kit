#!/bin/bash

# Manage agent personas in Goal Kit projects
# Allows switching between specialized agent roles for different tasks

set -euo pipefail

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Function to display usage information
usage() {
    cat << EOF
Usage: $0 [COMMAND] [OPTIONS]

Manage agent personas for specialized roles in Goal Kit projects.

COMMANDS:
    list                    List all available personas
    current                 Show currently active persona
    switch <persona>        Switch to specified persona
    status                  Show detailed status of current persona
    help                    Show this help message

OPTIONS:
    -h, --help              Show this help message
    -v, --verbose          Enable verbose output

EXAMPLES:
    $0 list
    $0 current
    $0 switch github
    $0 status
    $0 switch milestone --verbose

EOF
}

# Get project root
PROJECT_ROOT=$(get_git_root)
if [[ -z "$PROJECT_ROOT" ]]; then
    log_error "Not in a git repository"
    exit 1
fi

cd "$PROJECT_ROOT"

# Check if this is a Goal Kit project
if [[ ! -d ".goalkit" ]]; then
    log_error "Not a Goal Kit project"
    log_info "Please run 'goalkeeper init' first to set up the project"
    exit 1
fi

# Get persona config dir
PERSONA_CONFIG_DIR="$PROJECT_ROOT/.goalkit/personas"
mkdir -p "$PERSONA_CONFIG_DIR"

# Get current persona file
CURRENT_PERSONA_FILE="$PERSONA_CONFIG_DIR/current_persona.txt"

# Set default persona if file doesn't exist
if [[ ! -f "$CURRENT_PERSONA_FILE" ]]; then
    echo "general" > "$CURRENT_PERSONA_FILE"
fi

# Get default personas configuration
PERSONAS_CONFIG='{
  "default_persona": "general",
  "personas": {
    "general": {
      "name": "General Agent",
      "description": "Handles all aspects of goal-driven development without specialization",
      "capabilities": ["all"],
      "default_context": "General goal-driven development agent",
      "color": "blue"
    },
    "github": {
      "name": "GitHub/Git Specialist",
      "description": "Specializes in version control, repository management, and GitHub workflows",
      "capabilities": ["git", "github", "version_control", "branching", "merging", "pull_requests"],
      "default_context": "GitHub/Git specialist focused on repository management, branching strategies, pull requests, and version control best practices",
      "color": "orange",
      "specializations": [
        "Git workflow optimization",
        "Branching and merging strategies", 
        "Pull request creation and review",
        "Repository maintenance",
        "Tagging and release management"
      ]
    },
    "milestone": {
      "name": "Milestone Planner", 
      "description": "Specializes in breaking down goals into measurable milestones and tracking progress",
      "capabilities": ["milestones", "planning", "measurement", "tracking", "goals"],
      "default_context": "Milestone planning specialist focused on creating measurable, achievable milestones with clear success criteria and tracking mechanisms",
      "color": "green",
      "specializations": [
        "Goal decomposition",
        "Milestone creation",
        "Success metric definition", 
        "Progress tracking setup",
        "Dependency mapping"
      ]
    },
    "strategy": {
      "name": "Strategy Explorer",
      "description": "Specializes in exploring multiple implementation strategies and technical approaches",
      "capabilities": ["strategies", "technical_decision", "research", "analysis", "architectural_design"],
      "default_context": "Strategy exploration specialist focused on evaluating different technical approaches, architectural patterns, and implementation strategies",
      "color": "purple",
      "specializations": [
        "Technical approach evaluation",
        "Architecture decision support",
        "Risk assessment",
        "Technology research", 
        "Solution comparison"
      ]
    },
    "qa": {
      "name": "Quality Assurance",
      "description": "Specializes in testing, validation, quality metrics, and best practices",
      "capabilities": ["testing", "quality", "validation", "review", "best_practices"],
      "default_context": "Quality assurance specialist focused on testing strategies, validation approaches, code quality, and best practices",
      "color": "red",
      "specializations": [
        "Testing strategy development",
        "Code review processes",
        "Quality metric implementation",
        "Validation frameworks", 
        "Best practices enforcement"
      ]
    },
    "documentation": {
      "name": "Documentation Specialist",
      "description": "Specializes in creating and maintaining project documentation",
      "capabilities": ["documentation", "writing", "technical_writing", "knowledge_management"],
      "default_context": "Documentation specialist focused on creating clear, comprehensive documentation for all project aspects",
      "color": "teal",
      "specializations": [
        "Technical documentation",
        "API documentation", 
        "Process documentation",
        "Knowledge base creation",
        "User guides"
      ]
    }
  }
}'

# Function to get persona data
get_persona_data() {
    local persona_name="$1"
    echo "$PERSONAS_CONFIG" | python3 -c "
import sys, json
data = json.load(sys.stdin)
persona = data['personas'].get('$persona_name')
if persona:
    print(json.dumps(persona))
else:
    print('{}')
"
}

# Function to list all personas
list_personas() {
    local personas_json
    personas_json=$(echo "$PERSONAS_CONFIG" | python3 -c "
import sys, json
data = json.load(sys.stdin)
result = []
for name, info in data['personas'].items():
    result.append(f'{name}: {info[\"name\"]} - {info[\"description\"]}')
print('\\n'.join(result))
")
    
    log_info "Available Personas:"
    echo "$personas_json"
}

# Function to show current persona
show_current_persona() {
    local current_persona
    current_persona=$(cat "$CURRENT_PERSONA_FILE")
    
    if [[ "$current_persona" == "general" ]]; then
        log_info "Current Persona: $current_persona (General Agent)"
        log_info "Description: General goal-driven development agent"
    else
        local persona_data
        persona_data=$(get_persona_data "$current_persona")
        local persona_name
        persona_name=$(echo "$persona_data" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('name', 'Unknown'))" 2>/dev/null || echo "Unknown")
        local persona_desc
        persona_desc=$(echo "$persona_data" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('description', 'No description'))" 2>/dev/null || echo "No description")
        
        log_success "Current Persona: $current_persona ($persona_name)"
        log_info "Description: $persona_desc"
    fi
}

# Function to switch persona
switch_persona() {
    local target_persona="$1"
    local valid_personas
    valid_personas=$(echo "$PERSONAS_CONFIG" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(' '.join(data['personas'].keys()))
")
    
    if [[ ! " $valid_personas " =~ " $target_persona " ]]; then
        log_error "Invalid persona: $target_persona"
        log_info "Valid personas: $valid_personas"
        exit 1
    fi
    
    # Get persona details
    local persona_data
    persona_data=$(get_persona_data "$target_persona")
    local persona_name
    persona_name=$(echo "$persona_data" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('name', 'Unknown'))" 2>/dev/null || echo "Unknown")
    
    # Save the new persona
    echo "$target_persona" > "$CURRENT_PERSONA_FILE"
    
    log_success "Switched to persona: $target_persona ($persona_name)"
    
    # Update agent context with new persona info
    update_agent_context
    
    # Show persona details
    log_info "Capabilities: $(echo "$persona_data" | python3 -c "import sys, json; data = json.load(sys.stdin); print(', '.join(data.get('capabilities', ['none'])))" 2>/dev/null || echo "none")"
    log_info "Specializations: $(echo "$persona_data" | python3 -c "import sys, json; data = json.load(sys.stdin); specs = data.get('specializations', []); print(', '.join(specs[:3]) + ('...' if len(specs) > 3 else ''))" 2>/dev/null || echo "N/A")"
}

# Function to show detailed status
show_status() {
    show_current_persona
    local current_persona
    current_persona=$(cat "$CURRENT_PERSONA_FILE")
    local persona_data
    persona_data=$(get_persona_data "$current_persona")
    
    echo
    log_info "Persona Details:"
    echo "  Name: $(echo "$persona_data" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('name', 'Unknown'))" 2>/dev/null || echo "Unknown")"
    echo "  Capabilities: $(echo "$persona_data" | python3 -c "import sys, json; data = json.load(sys.stdin); print(', '.join(data.get('capabilities', ['none'])))" 2>/dev/null || echo "none")"
    echo "  Specializations:"
    echo "$persona_data" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for spec in data.get('specializations', []):
    print(f'    - {spec}')
" 2>/dev/null || echo "    N/A"
}

# Parse command
COMMAND="${1:-help}"

case "$COMMAND" in
    list)
        list_personas
        ;;
    current)
        show_current_persona
        ;;
    switch)
        if [[ -z "${2:-}" ]]; then
            log_error "Please specify a persona to switch to"
            usage
            exit 1
        fi
        switch_persona "$2"
        ;;
    status)
        show_status
        ;;
    help|h|\?)
        usage
        ;;
    *)
        log_error "Unknown command: $COMMAND"
        usage
        exit 1
        ;;
esac
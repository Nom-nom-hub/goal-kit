#!/bin/bash

# Check prerequisites for Goal Kit development

set -euo pipefail

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}") && pwd)"
source "$SCRIPT_DIR/common.sh"

# Function to display usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Check that all required tools are installed for Goal Kit development.

OPTIONS:
    -h, --help              Show this help message
    -v, --verbose          Enable verbose output
    -f, --fix             Attempt to fix missing prerequisites

EXAMPLES:
    $0
    $0 --verbose
    $0 --fix

EOF
}

# Parse command line arguments
VERBOSE=false
FIX=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--fix)
            FIX=true
            shift
            ;;
        -*)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            log_error "Unexpected argument: $1"
            usage
            exit 1
            ;;
    esac
done

# Required tools for Goal Kit development
REQUIRED_TOOLS=(
    "git:Git version control:https://git-scm.com/downloads"
    "uv:Python package manager:https://docs.astral.sh/uv/"
)

# Optional but recommended tools
OPTIONAL_TOOLS=(
    "node:Node.js runtime:https://nodejs.org/"
    "npm:Node package manager"
    "python:Python runtime:https://python.org/"
    "docker:Docker containerization:https://docker.com/"
)

# AI agent tools (at least one should be available)
AGENT_TOOLS=(
    "claude:Claude Code CLI:https://docs.anthropic.com/en/docs/claude-code/setup"
    "code:Visual Studio Code"
    "cursor:Cursor IDE"
    "gemini:Gemini CLI:https://github.com/google-gemini/gemini-cli"
    "qwen:Qwen Code CLI:https://github.com/QwenLM/qwen-code"
    "opencode:opencode CLI:https://opencode.ai"
    "codex:Codex CLI:https://github.com/openai/codex"
    "windsurf:Windsurf IDE:https://windsurf.com/"
    "kilocode:Kilo Code IDE:https://github.com/Kilo-Org/kilocode"
    "auggie:Auggie CLI:https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli"
    "q:Amazon Q Developer CLI:https://aws.amazon.com/developer/learning/q-developer-cli/"
)

log_info "Checking Goal Kit prerequisites..."

# Check required tools
log_info "Checking required tools..."
MISSING_REQUIRED=()
for tool_info in "${REQUIRED_TOOLS[@]}"; do
    IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"

    if [[ "$VERBOSE" == "true" ]]; then
        log_info "  Checking $tool_name..."
    fi

    if command_exists "$tool_name"; then
        if [[ "$VERBOSE" == "true" ]]; then
            local version
            version=$($tool_name --version 2>/dev/null | head -n1 || echo "version check not available")
            log_success "  $tool_name: $version"
        fi
    else
        MISSING_REQUIRED+=("$tool_name:$tool_description:$tool_url")
        log_error "  $tool_name: NOT FOUND"
    fi
done

# Check optional tools
log_info "Checking optional tools..."
MISSING_OPTIONAL=()
for tool_info in "${OPTIONAL_TOOLS[@]}"; do
    IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"

    if [[ "$VERBOSE" == "true" ]]; then
        log_info "  Checking $tool_name..."
    fi

    if command_exists "$tool_name"; then
        if [[ "$VERBOSE" == "true" ]]; then
            local version
            version=$($tool_name --version 2>/dev/null | head -n1 || echo "version check not available")
            log_success "  $tool_name: $version"
        fi
    else
        MISSING_OPTIONAL+=("$tool_name:$tool_description:$tool_url")
        if [[ "$VERBOSE" == "true" ]]; then
            log_warning "  $tool_name: NOT FOUND (optional)"
        fi
    fi
done

# Check AI agent tools
log_info "Checking AI agent tools..."
AGENT_FOUND=false
MISSING_AGENTS=()
for tool_info in "${AGENT_TOOLS[@]}"; do
    IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"

    if [[ "$VERBOSE" == "true" ]]; then
        log_info "  Checking $tool_name..."
    fi

    if command_exists "$tool_name"; then
        AGENT_FOUND=true
        if [[ "$VERBOSE" == "true" ]]; then
            local version
            version=$($tool_name --version 2>/dev/null | head -n1 || echo "version check not available")
            log_success "  $tool_name: $version"
        fi
    else
        MISSING_AGENTS+=("$tool_name:$tool_description:$tool_url")
        if [[ "$VERBOSE" == "true" ]]; then
            log_warning "  $tool_name: NOT FOUND"
        fi
    fi
done

# Summary
echo
if [[ ${#MISSING_REQUIRED[@]} -eq 0 ]]; then
    log_success "All required tools are installed!"
else
    log_error "Missing required tools:"
    for tool_info in "${MISSING_REQUIRED[@]}"; do
        IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"
        echo "  - $tool_name ($tool_description)"
        echo "    Install: $tool_url"
    done

    if [[ "$FIX" == "true" ]]; then
        log_info "Attempting to fix missing prerequisites..."

        # Try to install uv (most common missing tool)
        if command_exists "curl" && command_exists "bash"; then
            log_info "Installing uv package manager..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
        fi
    fi
fi

if [[ ${#MISSING_OPTIONAL[@]} -gt 0 ]]; then
    log_warning "Missing optional tools (development will still work):"
    for tool_info in "${MISSING_OPTIONAL[@]}"; do
        IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"
        echo "  - $tool_name ($tool_description)"
        echo "    Install: $tool_url"
    done
fi

if [[ "$AGENT_FOUND" == "false" ]]; then
    log_warning "No AI agent tools found. For the best experience, install at least one:"
    for tool_info in "${MISSING_AGENTS[@]}"; do
        IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"
        echo "  - $tool_name ($tool_description)"
        echo "    Install: $tool_url"
    done
else
    log_success "At least one AI agent tool is available!"
fi

echo
if [[ ${#MISSING_REQUIRED[@]} -eq 0 ]]; then
    log_success "Goal Kit prerequisites check completed successfully!"
    log_info "You can now use Goal Kit for goal-driven development."
else
    log_error "Please install missing required tools before using Goal Kit."
    exit 1
fi
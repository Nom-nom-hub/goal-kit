#!/bin/bash

# Check prerequisites for Goal Kit development

set -euo pipefail

# Determine script directory safely
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Attempt to source common utilities if present
if [[ -f "$SCRIPT_DIR/common.sh" ]]; then
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/common.sh"
else
    # Define fallback functions if common.sh not found
    log_info()    { echo -e "\033[1;34m[INFO]\033[0m $*"; }
    log_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $*"; }
    log_warning() { echo -e "\033[1;33m[WARN]\033[0m $*"; }
    log_error()   { echo -e "\033[1;31m[ERROR]\033[0m $*"; }
    command_exists() { command -v "$1" >/dev/null 2>&1; }
fi

# Usage function
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Check that all required tools are installed for Goal Kit development.

OPTIONS:
  -h, --help        Show this help message
  -v, --verbose     Enable verbose output
  -f, --fix         Attempt to fix missing prerequisites

EXAMPLES:
  $0
  $0 --verbose
  $0 --fix
EOF
}

# Parse command-line arguments
VERBOSE=false
FIX=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage; exit 0 ;;
        -v|--verbose)
            VERBOSE=true; shift ;;
        -f|--fix)
            FIX=true; shift ;;
        -*)
            log_error "Unknown option: $1"; usage; exit 1 ;;
        *)
            log_error "Unexpected argument: $1"; usage; exit 1 ;;
    esac
done

# Required tools
REQUIRED_TOOLS=(
    "git:Git version control:https://git-scm.com/downloads"
    "uv:Python package manager:https://docs.astral.sh/uv/"
)

# Optional tools
OPTIONAL_TOOLS=(
    "node:Node.js runtime:https://nodejs.org/"
    "npm:Node package manager"
    "python:Python runtime:https://python.org/"
    "docker:Docker containerization:https://docker.com/"
)

# AI agent tools (at least one should exist)
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

# ---- Required Tools ----
log_info "Checking required tools..."
MISSING_REQUIRED=()
for tool_info in "${REQUIRED_TOOLS[@]}"; do
    IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"

    [[ "$VERBOSE" == "true" ]] && log_info "  Checking $tool_name..."

    if command_exists "$tool_name"; then
        if [[ "$VERBOSE" == "true" ]]; then
            version=$($tool_name --version 2>/dev/null | head -n1 || echo "version unavailable")
            log_success "  $tool_name: $version"
        fi
    else
        MISSING_REQUIRED+=("$tool_info")
        log_error "  $tool_name: NOT FOUND"
    fi
done

# ---- Optional Tools ----
log_info "Checking optional tools..."
MISSING_OPTIONAL=()
for tool_info in "${OPTIONAL_TOOLS[@]}"; do
    IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"

    [[ "$VERBOSE" == "true" ]] && log_info "  Checking $tool_name..."

    if command_exists "$tool_name"; then
        [[ "$VERBOSE" == "true" ]] && log_success "  $tool_name installed"
    else
        MISSING_OPTIONAL+=("$tool_info")
        [[ "$VERBOSE" == "true" ]] && log_warning "  $tool_name: NOT FOUND (optional)"
    fi
done

# ---- AI Agent Tools ----
log_info "Checking AI agent tools..."
AGENT_FOUND=false
MISSING_AGENTS=()

for tool_info in "${AGENT_TOOLS[@]}"; do
    IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"
    [[ "$VERBOSE" == "true" ]] && log_info "  Checking $tool_name..."

    if command_exists "$tool_name"; then
        AGENT_FOUND=true
        [[ "$VERBOSE" == "true" ]] && log_success "  $tool_name available"
    else
        MISSING_AGENTS+=("$tool_info")
    fi
done

# ---- Summary ----
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
        if command_exists "curl" && command_exists "bash"; then
            log_info "Installing uv package manager..."
            curl -LsSf https://astral.sh/uv/install.sh | bash || log_error "Failed to install uv"
        else
            log_warning "curl or bash not found; cannot auto-fix"
        fi
    fi
fi

if [[ ${#MISSING_OPTIONAL[@]} -gt 0 ]]; then
    log_warning "Missing optional tools (development will still work):"
    for tool_info in "${MISSING_OPTIONAL[@]}"; do
        IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"
        echo "  - $tool_name ($tool_description)"
        [[ -n "${tool_url:-}" ]] && echo "    Install: $tool_url"
    done
fi

if [[ "$AGENT_FOUND" == "false" ]]; then
    log_warning "No AI agent tools found. For best experience, install at least one:"
    for tool_info in "${MISSING_AGENTS[@]}"; do
        IFS=':' read -r tool_name tool_description tool_url <<< "$tool_info"
        echo "  - $tool_name ($tool_description)"
        [[ -n "${tool_url:-}" ]] && echo "    Install: $tool_url"
    done
else
    log_success "At least one AI agent tool detected."
fi

echo
if [[ ${#MISSING_REQUIRED[@]} -eq 0 ]]; then
    log_success "Goal Kit prerequisites check completed successfully!"
    log_info "You can now use Goal Kit for goal-driven development."
else
    log_error "Please install missing required tools before using Goal Kit."
    exit 1
fi

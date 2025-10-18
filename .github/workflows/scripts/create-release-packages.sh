#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh
# Create zip archives for each AI agent and script type combination
# Usage: create-release-packages.sh <version>

# Check if we're running on Windows/Cygwin and redirect to PowerShell version if needed
case "$(uname -s)" in
    *MINGW*|*MSYS*|*CYGWIN*)
        if command -v pwsh >/dev/null 2>&1; then
            echo "Running on Windows - using PowerShell version" >&2
            pwsh -ExecutionPolicy Bypass -File "$(dirname "$0")/create-release-packages.ps1" "$@"
            exit $?
        elif command -v powershell >/dev/null 2>&1; then
            echo "Running on Windows - using PowerShell version" >&2
            powershell -ExecutionPolicy Bypass -File "$(dirname "$0")/create-release-packages.ps1" "$@"
            exit $?
        fi
        ;;
esac

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

echo "Building release packages for $VERSION"

# List of AI agents to create packages for
AGENTS=(
    "copilot"
    "claude"
    "gemini"
    "cursor"
    "qwen"
    "opencode"
    "codex"
    "windsurf"
    "kilocode"
    "auggie"
    "codebuddy"
    "roo"
    "q"
)

# Script types
SCRIPT_TYPES=("sh" "ps")

# Create a directory for generated releases
mkdir -p .genreleases

# Function to create a temporary directory for packaging
create_temp_package_dir() {
    local agent="$1"
    local script_type="$2"
    local temp_dir

    # Create temp directory (cross-platform compatible)
    if command -v mktemp >/dev/null 2>&1; then
        temp_dir=$(mktemp -d 2>/dev/null || mktemp -d -t tmp)
    else
        # Fallback for Windows/other systems
        temp_dir="/tmp/goalkit_temp_$(date +%s)_$"
        mkdir -p "$temp_dir"
    fi
    echo "Created temp dir for $agent-$script_type at $temp_dir" >&2

    # Create the .goalkit directory structure in temp
    mkdir -p "$temp_dir/.goalkit"
    
    # Copy common files (only if they exist)
    if [ -d "memory/" ]; then
        cp -r memory/ "$temp_dir/"
    fi
    if [ -d "templates/" ]; then
        cp -r templates/ "$temp_dir/"
    fi
    for file in CHANGELOG.md LICENSE README.md SECURITY.md .gitignore; do
        if [ -f "$file" ]; then
            cp "$file" "$temp_dir/"
        fi
    done

    # Copy agent-specific files
    case "$agent" in
        "copilot")
            if [ -d ".github/agent_templates/copilot" ]; then
                mkdir -p "$temp_dir/.github"
                cp -r .github/agent_templates/copilot/* "$temp_dir/.github/"
            fi
            ;;
        "claude")
            if [ -d ".claude" ]; then
                mkdir -p "$temp_dir/.claude"
                cp -r .claude/* "$temp_dir/.claude/"
            fi
            ;;
        "gemini")
            if [ -d ".gemini" ]; then
                mkdir -p "$temp_dir/.gemini"
                cp -r .gemini/* "$temp_dir/.gemini/"
            fi
            ;;
        "cursor")
            if [ -d ".cursor" ]; then
                mkdir -p "$temp_dir/.cursor"
                cp -r .cursor/* "$temp_dir/.cursor/"
            fi
            ;;
        "qwen")
            if [ -d ".qwen" ]; then
                mkdir -p "$temp_dir/.qwen"
                cp -r .qwen/* "$temp_dir/.qwen/"
            fi
            ;;
        "opencode")
            if [ -d ".opencode" ]; then
                mkdir -p "$temp_dir/.opencode"
                cp -r .opencode/* "$temp_dir/.opencode/"
            fi
            ;;
        "codex")
            if [ -d ".codex" ]; then
                mkdir -p "$temp_dir/.codex"
                cp -r .codex/* "$temp_dir/.codex/"
            fi
            ;;
        "windsurf")
            if [ -d ".windsurf" ]; then
                mkdir -p "$temp_dir/.windsurf"
                cp -r .windsurf/* "$temp_dir/.windsurf/"
            fi
            ;;
        "kilocode")
            if [ -d ".kilocode" ]; then
                mkdir -p "$temp_dir/.kilocode"
                cp -r .kilocode/* "$temp_dir/.kilocode/"
            fi
            ;;
        "auggie")
            if [ -d ".augment" ]; then
                mkdir -p "$temp_dir/.augment"
                cp -r .augment/* "$temp_dir/.augment/"
            fi
            ;;
        "roo")
            if [ -d ".roo" ]; then
                mkdir -p "$temp_dir/.roo"
                cp -r .roo/* "$temp_dir/.roo/"
            fi
            ;;
        "q")
            if [ -d ".amazonq" ]; then
                mkdir -p "$temp_dir/.amazonq"
                cp -r .amazonq/* "$temp_dir/.amazonq/"
            fi
            ;;
    esac

    # Copy script files based on type
    if [[ "$script_type" == "sh" ]]; then
        if [ -d "scripts/bash" ]; then
            mkdir -p "$temp_dir/.goalkit/scripts"
            cp -r scripts/bash/* "$temp_dir/.goalkit/scripts/"
        fi
    elif [[ "$script_type" == "ps" ]]; then
        if [ -d "scripts/powershell" ]; then
            mkdir -p "$temp_dir/.goalkit/scripts"
            cp -r scripts/powershell/* "$temp_dir/.goalkit/scripts/"
        fi
    fi

    # Clean up unnecessary files from the package
    rm -rf "$temp_dir/scripts"
    find "$temp_dir" -name ".DS_Store" -delete 2>/dev/null || true

    # Output the temp_dir to stdout (for assignment) and the message to stderr
    echo "$temp_dir"
}

# Main loop to create packages
for agent in "${AGENTS[@]}"; do
    for script_type in "${SCRIPT_TYPES[@]}"; do
        echo "Packaging for $agent with $script_type scripts..."
        TEMP_DIR=$(create_temp_package_dir "$agent" "$script_type")

        # Define archive name
        ARCHIVE_NAME="goal-kit-template-$agent-$script_type-$VERSION.zip"
        
        # Create zip archive
        if command -v zip >/dev/null 2>&1; then
            # Ensure the output directory exists
            mkdir -p .genreleases
            (
                cd "$TEMP_DIR"
                zip -r "../.genreleases/$ARCHIVE_NAME" .
            )
        else
            echo "Error: zip command not found. Please install zip utility to create release packages." >&2
            echo "On Ubuntu/Debian: sudo apt-get install zip" >&2
            echo "On macOS: brew install zip" >&2
            echo "On Windows with Chocolatey: choco install zip" >&2
            echo "Falling back to PowerShell version..." >&2
            if command -v pwsh >/dev/null 2>&1; then
                pwsh -ExecutionPolicy Bypass -File "$(dirname "$0")/create-release-packages.ps1" "$VERSION"
                exit $?
            elif command -v powershell >/dev/null 2>&1; then
                powershell -ExecutionPolicy Bypass -File "$(dirname "$0")/create-release-packages.ps1" "$VERSION"
                exit $?
            fi
            exit 1
        fi

        # Clean up temp directory
        rm -rf "$TEMP_DIR"
        echo "Created .genreleases/$ARCHIVE_NAME"
    done
done

echo "All release packages created successfully."
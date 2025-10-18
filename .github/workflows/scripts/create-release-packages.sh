#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh
# Create zip archives for each AI agent and script type combination
# Usage: create-release-packages.sh <version>

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

    temp_dir=$(mktemp -d)
    echo "Created temp dir for $agent-$script_type at $temp_dir"

    # Copy common files
    cp -r .goalkit/ "$temp_dir/"
    cp -r memory/ "$temp_dir/"
    cp -r templates/ "$temp_dir/"
    cp CHANGELOG.md LICENSE README.md SECURITY.md .gitignore "$temp_dir/"

    # Copy agent-specific files
    case "$agent" in
        "copilot")
            if [ -d ".github/agent_templates/copilot" ]; then
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
        cp -r scripts/bash/* "$temp_dir/.goalkit/scripts/"
    elif [[ "$script_type" == "ps" ]]; then
        cp -r scripts/powershell/* "$temp_dir/.goalkit/scripts/"
    fi

    # Clean up unnecessary files from the package
    rm -rf "$temp_dir/scripts"
    find "$temp_dir" -name ".DS_Store" -delete

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
        (
            cd "$TEMP_DIR"
            zip -r "../../.genreleases/$ARCHIVE_NAME" .
        )

        # Clean up temp directory
        rm -rf "$TEMP_DIR"
        echo "Created .genreleases/$ARCHIVE_NAME"
    done
done

echo "All release packages created successfully."
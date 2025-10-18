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

# Main loop to create packages
for agent in "${AGENTS[@]}"; do
    for script_type in "${SCRIPT_TYPES[@]}"; do
        echo "Packaging for $agent with $script_type scripts..."
        
        # Create temp directory
        TEMP_DIR=$(mktemp -d)
        echo "Created temp dir for $agent-$script_type at $TEMP_DIR" >&2

        # Create the .goalkit directory structure in temp
        mkdir -p "$TEMP_DIR/.goalkit"
        
        # Copy common files (only if they exist)
        if [ -d "memory/" ]; then
            cp -r memory/ "$TEMP_DIR/"
        fi
        if [ -d "templates/" ]; then
            cp -r templates/ "$TEMP_DIR/"
        fi
        for file in CHANGELOG.md LICENSE README.md SECURITY.md .gitignore; do
            if [ -f "$file" ]; then
                cp "$file" "$TEMP_DIR/"
            fi
        done

        # Copy agent-specific files
        case "$agent" in
            "copilot")
                if [ -d ".github/agent_templates/copilot" ]; then
                    mkdir -p "$TEMP_DIR/.github"
                    cp -r .github/agent_templates/copilot/* "$TEMP_DIR/.github/" 2>/dev/null || true
                fi
                ;;
            "claude")
                if [ -d ".claude" ]; then
                    mkdir -p "$TEMP_DIR/.claude"
                    cp -r .claude/* "$TEMP_DIR/.claude/" 2>/dev/null || true
                fi
                ;;
            "gemini")
                if [ -d ".gemini" ]; then
                    mkdir -p "$TEMP_DIR/.gemini"
                    cp -r .gemini/* "$TEMP_DIR/.gemini/" 2>/dev/null || true
                fi
                ;;
            "cursor")
                if [ -d ".cursor" ]; then
                    mkdir -p "$TEMP_DIR/.cursor"
                    cp -r .cursor/* "$TEMP_DIR/.cursor/" 2>/dev/null || true
                fi
                ;;
            "qwen")
                if [ -d ".qwen" ]; then
                    mkdir -p "$TEMP_DIR/.qwen"
                    cp -r .qwen/* "$TEMP_DIR/.qwen/" 2>/dev/null || true
                fi
                ;;
            "opencode")
                if [ -d ".opencode" ]; then
                    mkdir -p "$TEMP_DIR/.opencode"
                    cp -r .opencode/* "$TEMP_DIR/.opencode/" 2>/dev/null || true
                fi
                ;;
            "codex")
                if [ -d ".codex" ]; then
                    mkdir -p "$TEMP_DIR/.codex"
                    cp -r .codex/* "$TEMP_DIR/.codex/" 2>/dev/null || true
                fi
                ;;
            "windsurf")
                if [ -d ".windsurf" ]; then
                    mkdir -p "$TEMP_DIR/.windsurf"
                    cp -r .windsurf/* "$TEMP_DIR/.windsurf/" 2>/dev/null || true
                fi
                ;;
            "kilocode")
                if [ -d ".kilocode" ]; then
                    mkdir -p "$TEMP_DIR/.kilocode"
                    cp -r .kilocode/* "$TEMP_DIR/.kilocode/" 2>/dev/null || true
                fi
                ;;
            "auggie")
                if [ -d ".augment" ]; then
                    mkdir -p "$TEMP_DIR/.augment"
                    cp -r .augment/* "$TEMP_DIR/.augment/" 2>/dev/null || true
                fi
                ;;
            "roo")
                if [ -d ".roo" ]; then
                    mkdir -p "$TEMP_DIR/.roo"
                    cp -r .roo/* "$TEMP_DIR/.roo/" 2>/dev/null || true
                fi
                ;;
            "q")
                if [ -d ".amazonq" ]; then
                    mkdir -p "$TEMP_DIR/.amazonq"
                    cp -r .amazonq/* "$TEMP_DIR/.amazonq/" 2>/dev/null || true
                fi
                ;;
        esac

        # Copy script files based on type
        if [[ "$script_type" == "sh" ]]; then
            if [ -d "scripts/bash" ]; then
                mkdir -p "$TEMP_DIR/.goalkit/scripts"
                cp -r scripts/bash/* "$TEMP_DIR/.goalkit/scripts/" 2>/dev/null || true
            fi
        elif [[ "$script_type" == "ps" ]]; then
            if [ -d "scripts/powershell" ]; then
                mkdir -p "$TEMP_DIR/.goalkit/scripts"
                cp -r scripts/powershell/* "$TEMP_DIR/.goalkit/scripts/" 2>/dev/null || true
            fi
        fi

        # Clean up unnecessary files from the package
        rm -rf "$TEMP_DIR/scripts"
        find "$TEMP_DIR" -name ".DS_Store" -delete 2>/dev/null || true

        # Define archive name
        ARCHIVE_NAME="goal-kit-template-$agent-$script_type-$VERSION.zip"
        
        # Create zip archive
        if command -v zip >/dev/null 2>&1; then
            # Create zip from temp directory to the project root's .genreleases folder
            (cd "$TEMP_DIR" && zip -r "../.genreleases/$ARCHIVE_NAME" .)
        else
            echo "Error: zip command not found. Please install zip utility to create release packages." >&2
            exit 1
        fi

        # Clean up temp directory
        rm -rf "$TEMP_DIR"
        echo "Created .genreleases/$ARCHIVE_NAME"
    done
done

echo "All release packages created successfully."
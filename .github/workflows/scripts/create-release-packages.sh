#!/bin/bash
set -e

VERSION=$1
RELEASE_DIR="release-packages"

echo "Creating release packages for version $VERSION..."

# Create release directory
mkdir -p "$RELEASE_DIR"

# Ensure source .github directory exists before starting
if [ ! -d ".github" ]; then
    echo "Error: .github directory not found in source"
    exit 1
fi

# Function to create template package for an AI agent
create_template_package() {
    local AI=$1
    local SCRIPT_TYPE=$2
    local TEMPLATE_DIR="goal-kit-template-${AI}-${SCRIPT_TYPE}-${VERSION}"

    echo "Creating template package for ${AI} with ${SCRIPT_TYPE} scripts..."

    # Create template directory structure
    mkdir -p "$TEMPLATE_DIR"

    # Copy core files - preserve source structure
    if [ -d ".github" ]; then
        cp -r .github "$TEMPLATE_DIR/"
    fi
    if [ -d "docs" ]; then
        cp -r docs "$TEMPLATE_DIR/"
    fi
    if [ -d "memory" ]; then
        cp -r memory "$TEMPLATE_DIR/"
    fi
    if [ -d "src" ]; then
        cp -r src "$TEMPLATE_DIR/"
    fi
    if [ -d "templates" ]; then
        cp -r templates "$TEMPLATE_DIR/"
    fi
    if [ -f "README.md" ]; then
        cp README.md "$TEMPLATE_DIR/"
    fi
    if [ -f "LICENSE" ]; then
        cp LICENSE "$TEMPLATE_DIR/" 2>/dev/null || true
    fi

    # Remove development files
    rm -rf "$TEMPLATE_DIR/.git"
    rm -rf "$TEMPLATE_DIR/demo-goal-project"
    rm -rf "$TEMPLATE_DIR/spec-kit"
    rm -rf "$TEMPLATE_DIR/.qwen"
    rm -rf "$TEMPLATE_DIR/.goalify"
    rm -rf "$TEMPLATE_DIR/.qodo"
    rm -rf "$TEMPLATE_DIR/release-packages"
    rm -rf "$TEMPLATE_DIR/.github/workflows/scripts"

    # Create zip file
    # Remove 'v' prefix from version if present to avoid double 'v'
    CLEAN_VERSION=${VERSION#v}
    ZIP_NAME="goal-kit-template-${AI}-${SCRIPT_TYPE}-v${CLEAN_VERSION}.zip"

    # Detect OS and use appropriate zip command
    if command -v zip &> /dev/null; then
        # Linux/macOS with zip command
        cd "$(dirname "$TEMPLATE_DIR")"
        zip -r "$ZIP_NAME" "$(basename "$TEMPLATE_DIR")"
        cd ..
        mv "$ZIP_NAME" "$RELEASE_DIR/"
    elif command -v 7z &> /dev/null; then
        # Windows with 7-Zip
        cd "$(dirname "$TEMPLATE_DIR")"
        7z a "$ZIP_NAME" "$(basename "$TEMPLATE_DIR")"
        cd ..
        mv "$ZIP_NAME" "$RELEASE_DIR/"
    elif command -v powershell &> /dev/null; then
        # Windows with PowerShell (fallback)
        cd "$(dirname "$TEMPLATE_DIR")"
        powershell -Command "Compress-Archive -Path '$(basename "$TEMPLATE_DIR")' -DestinationPath '$ZIP_NAME'"
        cd ..
        if [ -f "$ZIP_NAME" ]; then
            mv "$ZIP_NAME" "$RELEASE_DIR/"
        fi
    else
        echo "Error: No zip utility found (zip, 7z, or PowerShell)"
        exit 1
    fi

    echo "Created $ZIP_NAME"
}

# Create packages for all AI agents and script types
AI_AGENTS=("copilot" "claude" "gemini" "cursor" "qwen" "opencode" "codex" "windsurf" "kilocode" "auggie" "roo" "deepseek" "tabnine" "grok" "codewhisperer")
SCRIPT_TYPES=("sh" "ps")

for AI in "${AI_AGENTS[@]}"; do
    for SCRIPT in "${SCRIPT_TYPES[@]}"; do
        create_template_package "$AI" "$SCRIPT"
    done
done

echo "Release packages created in $RELEASE_DIR/"
ls -la "$RELEASE_DIR"/
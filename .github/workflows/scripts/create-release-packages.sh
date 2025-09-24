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
    local TEMPLATE_DIR="goal-dev-spec-template-${AI}-${SCRIPT_TYPE}-${VERSION}"

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
    rm -rf "$TEMPLATE_DIR/.specify"
    rm -rf "$TEMPLATE_DIR/.qodo"

    # Create zip file
    ZIP_NAME="goal-dev-spec-template-${AI}-${SCRIPT_TYPE}-v${VERSION}.zip"
    cd "$(dirname "$TEMPLATE_DIR")"
    zip -r "../$ZIP_NAME" "$(basename "$TEMPLATE_DIR")"
    cd ..

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
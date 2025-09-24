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
    cd "$(dirname "$TEMPLATE_DIR")"
    TEMPLATE_BASENAME="$(basename "$TEMPLATE_DIR")"

    if command -v zip &> /dev/null; then
        # Linux/macOS with zip command
        echo "Using zip command..."
        if zip -r "$ZIP_NAME" "$TEMPLATE_BASENAME"; then
            echo "✓ Created $ZIP_NAME with zip"
        else
            echo "Error: zip command failed"
            exit 1
        fi
    elif command -v 7z &> /dev/null; then
        # Windows with 7-Zip
        echo "Using 7z command..."
        if 7z a "$ZIP_NAME" "$TEMPLATE_BASENAME"; then
            echo "✓ Created $ZIP_NAME with 7z"
        else
            echo "Error: 7z command failed"
            exit 1
        fi
    elif command -v tar &> /dev/null && command -v gzip &> /dev/null; then
        # Fallback: tar + gzip (available on most Linux systems)
        echo "Using tar + gzip..."
        TAR_NAME="${ZIP_NAME%.zip}.tar.gz"
        if tar -czf "$TAR_NAME" "$TEMPLATE_BASENAME"; then
            echo "✓ Created $TAR_NAME with tar+gzip"
            # Rename to .zip for consistency
            mv "$TAR_NAME" "$ZIP_NAME"
            echo "✓ Renamed to $ZIP_NAME"
        else
            echo "Error: tar command failed"
            exit 1
        fi
    elif command -v powershell &> /dev/null; then
        # Windows with PowerShell (fallback)
        echo "Using PowerShell Compress-Archive..."
        if powershell -Command "Compress-Archive -Path '$TEMPLATE_BASENAME' -DestinationPath '$ZIP_NAME'"; then
            echo "✓ Created $ZIP_NAME with PowerShell"
        else
            echo "Error: PowerShell command failed"
            exit 1
        fi
    else
        echo "Error: No zip utility found (zip, 7z, tar+gzip, or PowerShell)"
        echo "Available commands:"
        which zip 7z tar gzip powershell || echo "None found"
        exit 1
    fi

    cd ..
    if [ -f "$ZIP_NAME" ]; then
        mv "$ZIP_NAME" "$RELEASE_DIR/"
        echo "✓ Moved $ZIP_NAME to $RELEASE_DIR/"
    else
        echo "Error: $ZIP_NAME was not created in $(pwd)"
        ls -la
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
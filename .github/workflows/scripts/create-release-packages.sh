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

    # Create zip file
    # Remove 'v' prefix from version if present to avoid double 'v'
    CLEAN_VERSION=${VERSION#v}
    ZIP_NAME="goal-kit-template-${AI}-${SCRIPT_TYPE}-v${CLEAN_VERSION}.zip"

    # Detect OS and use appropriate zip command
    # Get the full path to the template directory
    TEMPLATE_FULL_PATH="$(pwd)/$TEMPLATE_DIR"
    TEMPLATE_BASENAME="$(basename "$TEMPLATE_DIR")"
    SCRIPT_WORK_DIR="$(pwd)"

    echo "Template directory: $TEMPLATE_FULL_PATH"
    echo "Template basename: $TEMPLATE_BASENAME"
    echo "Working directory: $SCRIPT_WORK_DIR"
    echo "Release directory: $RELEASE_DIR"

    # Change to the template's parent directory for compression
    TEMPLATE_PARENT_DIR="$(dirname "$TEMPLATE_FULL_PATH")"
    echo "Template parent directory: $TEMPLATE_PARENT_DIR"

    cd "$TEMPLATE_PARENT_DIR"

    # Try different compression methods
    if command -v zip &> /dev/null; then
        # Linux/macOS with zip command
        echo "Using zip command..."
        ZIP_FULL_PATH="$SCRIPT_WORK_DIR/$ZIP_NAME"
        echo "Zip will be created at: $ZIP_FULL_PATH"
        if zip -r "$ZIP_FULL_PATH" "$TEMPLATE_BASENAME"; then
            echo "✓ Created $ZIP_FULL_PATH with zip"
        else
            echo "Error: zip command failed with exit code $?"
            cd "$SCRIPT_WORK_DIR"
            exit 1
        fi
    elif command -v 7z &> /dev/null; then
        # Windows with 7-Zip
        echo "Using 7z command..."
        ZIP_FULL_PATH="$SCRIPT_WORK_DIR/$ZIP_NAME"
        echo "Zip will be created at: $ZIP_FULL_PATH"
        if 7z a "$ZIP_FULL_PATH" "$TEMPLATE_BASENAME"; then
            echo "✓ Created $ZIP_FULL_PATH with 7z"
        else
            echo "Error: 7z command failed with exit code $?"
            cd "$SCRIPT_WORK_DIR"
            exit 1
        fi
    elif command -v tar &> /dev/null && command -v gzip &> /dev/null; then
        # Fallback: tar + gzip (Linux standard - always available)
        echo "Using tar + gzip..."
        TAR_FULL_PATH="$SCRIPT_WORK_DIR/${ZIP_NAME%.zip}.tar.gz"
        echo "Tar will be created at: $TAR_FULL_PATH"
        if tar -czf "$TAR_FULL_PATH" "$TEMPLATE_BASENAME"; then
            echo "✓ Created $TAR_FULL_PATH with tar+gzip"
            # Rename to .zip for consistency
            ZIP_FULL_PATH="$SCRIPT_WORK_DIR/$ZIP_NAME"
            if mv "$TAR_FULL_PATH" "$ZIP_FULL_PATH"; then
                echo "✓ Renamed to $ZIP_FULL_PATH"
            else
                echo "Error: Failed to rename $TAR_FULL_PATH to $ZIP_FULL_PATH"
                cd "$SCRIPT_WORK_DIR"
                exit 1
            fi
        else
            echo "Error: tar command failed with exit code $?"
            cd "$SCRIPT_WORK_DIR"
            exit 1
        fi
    elif command -v powershell &> /dev/null; then
        # Windows with PowerShell (fallback)
        echo "Using PowerShell Compress-Archive..."
        ZIP_FULL_PATH="$SCRIPT_WORK_DIR/$ZIP_NAME"
        echo "Zip will be created at: $ZIP_FULL_PATH"
        if powershell -Command "Compress-Archive -Path '$TEMPLATE_BASENAME' -DestinationPath '$ZIP_FULL_PATH'"; then
            echo "✓ Created $ZIP_FULL_PATH with PowerShell"
        else
            echo "Error: PowerShell command failed with exit code $?"
            cd "$SCRIPT_WORK_DIR"
            exit 1
        fi
    else
        echo "Error: No zip utility found (zip, 7z, tar+gzip, or PowerShell)"
        echo "Current directory: $(pwd)"
        echo "Template directory: $TEMPLATE_FULL_PATH"
        echo "Available commands:"
        which zip 7z tar gzip powershell || echo "None found"
        echo "Directory listing:"
        ls -la "$(dirname "$TEMPLATE_FULL_PATH")"
        cd "$SCRIPT_WORK_DIR"
        exit 1
    fi

    # Return to script working directory and verify file was created
    cd "$SCRIPT_WORK_DIR"
    ZIP_FULL_PATH="$SCRIPT_WORK_DIR/$ZIP_NAME"
    if [ -f "$ZIP_FULL_PATH" ]; then
        echo "✓ Zip file exists at: $ZIP_FULL_PATH"
        if mv "$ZIP_FULL_PATH" "$RELEASE_DIR/"; then
            echo "✓ Moved $ZIP_NAME to $RELEASE_DIR/"
        else
            echo "Error: Failed to move $ZIP_FULL_PATH to $RELEASE_DIR/"
            ls -la "$RELEASE_DIR/"
            exit 1
        fi
    else
        echo "Error: $ZIP_NAME was not created"
        echo "Expected location: $ZIP_FULL_PATH"
        echo "Current directory: $(pwd)"
        echo "Directory listing:"
        ls -la
        echo "Parent directory listing:"
        ls -la "$(dirname "$TEMPLATE_FULL_PATH")"
        echo "Template directory contents:"
        ls -la "$TEMPLATE_FULL_PATH"
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
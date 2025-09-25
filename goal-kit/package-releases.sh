#!/usr/bin/env bash
set -euo pipefail

VERSION="0.0.1"
RELEASE_DIR="../releases"
GOAL_KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

AI_AGENTS=(
    "cursor" "claude" "qwen" "roo" "copilot"
    "auggie" "gemini" "windsurf" "codex"
    "kilocode" "opencode"
)

PLATFORMS=("sh" "ps")

mkdir -p "$RELEASE_DIR"
mkdir -p "/tmp/goal-kit-release"

for agent in "${AI_AGENTS[@]}"; do
    for platform in "${PLATFORMS[@]}"; do
        PACKAGE_NAME="goal-kit-template-${agent}-${platform}-v${VERSION}"
        PACKAGE_DIR="/tmp/goal-kit-release/$PACKAGE_NAME"
        PACKAGE_FILE="$RELEASE_DIR/$PACKAGE_NAME.zip"

        mkdir -p "$PACKAGE_DIR"

        # Copy templates
        cp -r "$GOAL_KIT_DIR/templates" "$PACKAGE_DIR/" 2>/dev/null || true
        cp -r "$GOAL_KIT_DIR/.goalify" "$PACKAGE_DIR/" 2>/dev/null || true
        cp -r "$GOAL_KIT_DIR/.qwen" "$PACKAGE_DIR/" 2>/dev/null || true

        # Copy scripts
        if [ "$platform" = "sh" ]; then
            mkdir -p "$PACKAGE_DIR/scripts/bash"
            cp "$GOAL_KIT_DIR/scripts/bash/"*.sh "$PACKAGE_DIR/scripts/bash/" 2>/dev/null || true
        else
            mkdir -p "$PACKAGE_DIR/scripts/powershell"
            cp "$GOAL_KIT_DIR/scripts/powershell/"*.ps1 "$PACKAGE_DIR/scripts/powershell/" 2>/dev/null || true
        fi

        cp "$GOAL_KIT_DIR/scripts/"*.sh "$PACKAGE_DIR/" 2>/dev/null || true

        # Create simple README
        echo "# Goal-Kit Template for $agent ($platform)" > "$PACKAGE_DIR/README.md"
        echo "Version: $VERSION" >> "$PACKAGE_DIR/README.md"

        # Zip package
        cd "/tmp/goal-kit-release"
        if command -v zip >/dev/null 2>&1; then
            zip -r "$PACKAGE_FILE" "$PACKAGE_NAME" >/dev/null
        else
            echo "❌ zip command not found" >&2
            exit 1
        fi

        echo "✅ Created $PACKAGE_FILE"
        rm -rf "$PACKAGE_DIR"
    done
done

echo "🎉 All packages created in $RELEASE_DIR"

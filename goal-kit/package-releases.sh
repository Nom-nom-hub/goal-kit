#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with all Goal-Kit template zip files
# Usage: create-github-release.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Remove 'v' prefix from version for release title
VERSION_NO_V=${VERSION#v}

# Directory where release zips are stored
RELEASE_DIR="../releases"

# AI Agents
AI_AGENTS=(
    "cursor"
    "claude"
    "qwen"
    "roo"
    "copilot"
    "auggie"
    "gemini"
    "windsurf"
    "codex"
    "kilocode"
    "opencode"
)

# Platforms
PLATFORMS=("sh" "ps")

# Build the list of files to upload
FILES=()
for agent in "${AI_AGENTS[@]}"; do
    for platform in "${PLATFORMS[@]}"; do
        file="$RELEASE_DIR/goal-kit-template-${agent}-${platform}-v${VERSION}.zip"
        if [[ -f "$file" ]]; then
            FILES+=("$file")
        else
            echo "⚠️  Warning: Release file not found: $file"
        fi
    done
done

if [[ ${#FILES[@]} -eq 0 ]]; then
    echo "❌ No release files found to upload. Exiting."
    exit 1
fi

# Create GitHub release
gh release create "$VERSION" \
  "${FILES[@]}" \
  --title "Goal-Kit Templates - $VERSION_NO_V" \
  --notes-file release_notes.md

echo "✅ GitHub release $VERSION created successfully!"

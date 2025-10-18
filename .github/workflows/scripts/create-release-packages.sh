#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh
# Build zip archives for each AI agent and script type
# Usage: create-release-packages.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"
echo "Building release packages for $VERSION"

# Agents and script types
AGENTS=(copilot claude gemini cursor qwen opencode codex windsurf kilocode auggie roo q)
SCRIPT_TYPES=(sh ps)

# Ensure release folder exists
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"

for agent in "${AGENTS[@]}"; do
  for script_type in "${SCRIPT_TYPES[@]}"; do
    echo "Packaging $agent ($script_type)..."

    # Temp working dir
    TEMP_DIR=$(mktemp -d)
    echo "Using temp dir: $TEMP_DIR"

    # Base goalkit structure
    GOALKIT_DIR="$TEMP_DIR/.goalkit"
    mkdir -p "$GOALKIT_DIR"

    # Copy common folders into .goalkit (avoid double nesting)
    [ -d memory ] && cp -r memory "$GOALKIT_DIR/"
    [ -d templates ] && cp -r templates "$GOALKIT_DIR/"

    # Copy top-level files
    for file in CHANGELOG.md LICENSE README.md SECURITY.md .gitignore; do
      [ -f "$file" ] && cp "$file" "$TEMP_DIR/"
    done

    # Copy agent-specific directories to temp root (not inside .goalkit)
    case "$agent" in
      copilot)   [ -d ".github/agent_templates/copilot" ] && cp -r .github/agent_templates/copilot "$TEMP_DIR/.github" ;;
      claude)    [ -d ".claude" ] && cp -r .claude "$TEMP_DIR/" ;;
      gemini)    [ -d ".gemini" ] && cp -r .gemini "$TEMP_DIR/" ;;
      cursor)    [ -d ".cursor" ] && cp -r .cursor "$TEMP_DIR/" ;;
      qwen)      [ -d ".qwen" ] && cp -r .qwen "$TEMP_DIR/" ;;
      opencode)  [ -d ".opencode" ] && cp -r .opencode "$TEMP_DIR/" ;;
      codex)     [ -d ".codex" ] && cp -r .codex "$TEMP_DIR/" ;;
      windsurf)  [ -d ".windsurf" ] && cp -r .windsurf "$TEMP_DIR/" ;;
      kilocode)  [ -d ".kilocode" ] && cp -r .kilocode "$TEMP_DIR/" ;;
      auggie)    [ -d ".augment" ] && cp -r .augment "$TEMP_DIR/" ;;
      roo)       [ -d ".roo" ] && cp -r .roo "$TEMP_DIR/" ;;
      q)         [ -d ".amazonq" ] && cp -r .amazonq "$TEMP_DIR/" ;;
    esac

    # Copy script files based on type
    mkdir -p "$GOALKIT_DIR/scripts"
    if [[ "$script_type" == "sh" && -d scripts/bash ]]; then
      cp -r scripts/bash/* "$GOALKIT_DIR/scripts/" 2>/dev/null || true
    elif [[ "$script_type" == "ps" && -d scripts/powershell ]]; then
      cp -r scripts/powershell/* "$GOALKIT_DIR/scripts/" 2>/dev/null || true
    fi

    # Remove any unneeded top-level script dirs to prevent duplication
    rm -rf "$TEMP_DIR/scripts" 2>/dev/null || true
    find "$TEMP_DIR" -name ".DS_Store" -delete 2>/dev/null || true

    # Archive
    ARCHIVE_NAME="goal-kit-template-$agent-$script_type-$VERSION.zip"
    (cd "$TEMP_DIR" && zip -r "$PWD/$GENRELEASES_DIR/$ARCHIVE_NAME" .)

    # Cleanup temp
    rm -rf "$TEMP_DIR"
    echo "Created $GENRELEASES_DIR/$ARCHIVE_NAME"
  done
done

echo "All release packages created successfully."

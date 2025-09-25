#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with all template zip files
# Usage: create-github-release.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Remove 'v' prefix from version for release titles
VERSION_NO_V=${VERSION#v}

gh release create "$VERSION" \
  ../releases/goal-kit-template-copilot-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-copilot-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-claude-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-claude-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-gemini-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-gemini-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-cursor-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-cursor-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-opencode-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-opencode-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-qwen-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-qwen-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-windsurf-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-windsurf-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-codex-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-codex-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-kilocode-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-kilocode-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-auggie-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-auggie-ps-v"$VERSION".zip \
  ../releases/goal-kit-template-roo-sh-v"$VERSION".zip \
  ../releases/goal-kit-template-roo-ps-v"$VERSION".zip \
  --title "Goal-Kit Templates - $VERSION_NO_V" \
  --notes-file ../releases/RELEASE_NOTES.md
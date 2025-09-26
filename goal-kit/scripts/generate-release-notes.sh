#!/usr/bin/env bash
set -euo pipefail

# generate-release-notes.sh
# Script to generate release notes for a new version

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <new_version> <previous_version>" >&2
  exit 1
fi

NEW_VERSION="$1"
PREVIOUS_VERSION="$2"

echo "Release notes for version $NEW_VERSION" > release_notes.md
echo "" >> release_notes.md
echo "## Changes" >> release_notes.md
echo "- Updated goal templates" >> release_notes.md
echo "- Improved scripts for bash and PowerShell" >> release_notes.md
echo "- Bug fixes and performance improvements" >> release_notes.md

# Extract commit messages since last tag if there was a previous version
if [ "$PREVIOUS_VERSION" != "v0.0.0" ] && [ -n "$PREVIOUS_VERSION" ]; then
  echo "" >> release_notes.md
  echo "## Commits since $PREVIOUS_VERSION" >> release_notes.md
  git log --oneline "$PREVIOUS_VERSION"..HEAD >> release_notes.md
fi

cat release_notes.md
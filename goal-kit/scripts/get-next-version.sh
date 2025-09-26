#!/usr/bin/env bash
set -euo pipefail

# get-next-version.sh
# Script to get the next version based on the current version in pyproject.toml

if [[ $# -ne 0 ]]; then
  echo "Usage: $0" >&2
  exit 1
fi

# Get current version from pyproject.toml
CURRENT_VERSION=$(grep -E "^version = " goal-kit/pyproject.toml | sed 's/version = "\(.*\)"/\1/')

# Parse version components
VERSION_PARTS=($(echo $CURRENT_VERSION | tr '.' ' '))
MAJOR=${VERSION_PARTS[0]:-0}
MINOR=${VERSION_PARTS[1]:-0}
PATCH=${VERSION_PARTS[2]:-0}

# Increment patch version
PATCH=$((PATCH + 1))
NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
NEW_VERSION_WITH_V="v${MAJOR}.${MINOR}.${PATCH}"

echo "Current version: $CURRENT_VERSION"
echo "New version: $NEW_VERSION_WITH_V"

# Output in a format that can be used by GitHub Actions
echo "new_version=$NEW_VERSION_WITH_V"
echo "current_version=$CURRENT_VERSION"

# For GitHub Actions output (when run in that context)
if [ -n "${GITHUB_OUTPUT:-}" ]; then
  echo "new_version=$NEW_VERSION_WITH_V" >> $GITHUB_OUTPUT
  echo "current_version=$CURRENT_VERSION" >> $GITHUB_OUTPUT
fi
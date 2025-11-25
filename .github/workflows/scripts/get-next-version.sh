#!/usr/bin/env bash
set -euo pipefail

# get-next-version.sh
# Read version from pyproject.toml (source of truth)
# Usage: get-next-version.sh

# Extract version from pyproject.toml
if [ -f "pyproject.toml" ]; then
    # Look for version = "X.Y.Z" in pyproject.toml
    VERSION=$(grep -oP 'version\s*=\s*"\K[^"]+' pyproject.toml || echo "0.0.0")
else
    VERSION="0.0.0"
fi

NEW_VERSION="v$VERSION"

# Get the latest tag, or use v0.0.0 if no tags exist
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# Only proceed if the new version is different from the latest tag
if [ "$NEW_VERSION" = "$LATEST_TAG" ]; then
    echo "Version in pyproject.toml ($NEW_VERSION) matches latest tag. No release needed."
    exit 0
fi

# Set outputs for GitHub Actions
echo "latest_tag=$LATEST_TAG" >> "$GITHUB_OUTPUT"
echo "new_version=$NEW_VERSION" >> "$GITHUB_OUTPUT"
echo "New version will be: $NEW_VERSION (from pyproject.toml)"
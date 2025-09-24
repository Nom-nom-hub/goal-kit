#!/bin/bash
set -e

# Get the latest tag from git
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# Remove 'v' prefix if present
VERSION=${LATEST_TAG#v}

# Split version into components
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

# Increment patch version
PATCH=$((PATCH + 1))

# Create new version
NEW_VERSION="$MAJOR.$MINOR.$PATCH"

echo "Latest tag: $LATEST_TAG"
echo "New version: v$NEW_VERSION"

# Set outputs for GitHub Actions
echo "new_version=v$NEW_VERSION" >> $GITHUB_OUTPUT
echo "latest_tag=$LATEST_TAG" >> $GITHUB_OUTPUT
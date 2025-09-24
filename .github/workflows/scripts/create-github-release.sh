#!/bin/bash
set -e

VERSION=$1
REPO="Nom-nom-hub/goal-dev-spec"

echo "Creating GitHub release $VERSION..."

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI not found. Please install it from https://cli.github.com/"
    exit 1
fi

# Authenticate with GitHub CLI if not already authenticated
if ! gh auth status &> /dev/null; then
    echo "Please authenticate with GitHub CLI first:"
    echo "gh auth login"
    exit 1
fi

# Create the release
if [ -f "release_notes.md" ]; then
    gh release create "$VERSION" \
        --repo "$REPO" \
        --title "Goal-Driven Development Kit v$VERSION" \
        --notes-file "release_notes.md" \
        release-packages/*.zip
else
    gh release create "$VERSION" \
        --repo "$REPO" \
        --title "Goal-Driven Development Kit v$VERSION" \
        --notes "Release $VERSION of Goal-Driven Development Kit" \
        release-packages/*.zip
fi

echo "Release $VERSION created successfully!"
echo "Release URL: https://github.com/$REPO/releases/tag/$VERSION"
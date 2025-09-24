#!/bin/bash
set -e

VERSION=$1
REPO="Nom-nom-hub/goal-dev-spec"

# Check if release already exists
if gh release view "$VERSION" >/dev/null 2>&1; then
    echo "Release $VERSION already exists"
    echo "exists=true" >> $GITHUB_OUTPUT
else
    echo "Release $VERSION does not exist"
    echo "exists=false" >> $GITHUB_OUTPUT
fi
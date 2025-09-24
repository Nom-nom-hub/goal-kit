#!/bin/bash
set -e

VERSION=$1

echo "Updating version to $VERSION..."

# Update version in README.md
sed -i "s/v[0-9]\+\.[0-9]\+\.[0-9]\+/v$VERSION/g" README.md

# If there's a pyproject.toml, update it
if [ -f "pyproject.toml" ]; then
    sed -i "s/version = \"[0-9]\+\.[0-9]\+\.[0-9]\+\"/version = \"$VERSION\"/" pyproject.toml
fi

echo "Version updated to $VERSION in project files"
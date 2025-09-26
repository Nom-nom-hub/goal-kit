#!/usr/bin/env bash
set -euo pipefail

# check-release-exists.sh
# Script to check if a release already exists for a given version

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Check if the release already exists using GitHub CLI
if gh release view "$VERSION" >/dev/null 2>&1; then
  echo "exists=true"
  exit 0
else
  echo "exists=false"
  exit 0
fi
#!/usr/bin/env bash
set -euo pipefail

# generate-release-notes.sh
# Generate release notes from CHANGELOG.md
# Usage: generate-release-notes.sh <new_version> <last_tag>

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <new_version> <last_tag>" >&2
  exit 1
fi

NEW_VERSION="$1"
LAST_TAG="$2"

# Extract the section for the new version from CHANGELOG.md
# Remove 'v' prefix if present in version
CLEAN_VERSION=$(echo "$NEW_VERSION" | sed 's/^v//')

CHANGELOG_SECTION=$(awk -v version="$CLEAN_VERSION" '
BEGIN { in_section = 0; section = ""; }
/^## \\[/{ 
    if (in_section) exit 0;
    # Check if this line starts with the target version (with optional date info after)
    if ($0 ~ ("## \\\[" version ".*")) {
        in_section = 1;
        next;
    } else {
        next;
    }
}
in_section { 
    if ($0 ~ /^## \\[/) { 
        exit 0; 
    }
    section = section $0 "\n";
}
END { 
    gsub(/\r/, "", section);
    print section; 
}
' CHANGELOG.md)

# Create release notes
cat > release_notes.md << EOF
This is the latest set of Goal Kit releases that you can use with your AI agent of choice. We recommend using the Goalkeeper CLI to scaffold your projects, however you can download these independently and manage them yourself.

## Recent Changes

$CHANGELOG_SECTION

EOF

cat >> release_notes.md << EOF

## Supported AI Agents

All packages include templates for:
- Claude Code, GitHub Copilot, Gemini CLI, Cursor, Qwen Code, opencode, Codex CLI, Windsurf, Kilo Code, Auggie CLI, Roo Code, Amazon Q Developer CLI

EOF

echo "Generated release notes:"
cat release_notes.md
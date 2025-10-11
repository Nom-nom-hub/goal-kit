#!/usr/bin/env bash
set -euo pipefail

# generate-release-notes.sh
# Generate release notes from git history
# Usage: generate-release-notes.sh <new_version> <last_tag>

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <new_version> <last_tag>" >&2
  exit 1
fi

NEW_VERSION="$1"
LAST_TAG="$2"

# Get commits since last tag
if [ "$LAST_TAG" = "v0.0.0" ]; then
  # Check how many commits we have and use that as the limit
  COMMIT_COUNT=$(git rev-list --count HEAD)
  if [ "$COMMIT_COUNT" -gt 10 ]; then
    COMMITS=$(git log --oneline --pretty=format:"- %s" HEAD~10..HEAD)
  else
    COMMITS=$(git log --oneline --pretty=format:"- %s" HEAD~$COMMIT_COUNT..HEAD 2>/dev/null || git log --oneline --pretty=format:"- %s")
  fi
else
  COMMITS=$(git log --oneline --pretty=format:"- %s" $LAST_TAG..HEAD)
fi

# Create release notes
cat > release_notes.md << EOF
This is the latest set of Goal Kit releases that you can use with your AI agent of choice. We recommend using the Goalkeeper CLI to scaffold your projects, however you can download these independently and manage them yourself.

## What's New in Goal-Driven Development

Goal Kit introduces a new approach to software development that focuses on outcomes and learning rather than detailed upfront specifications. This release includes:

- **Goal-driven workflow** with vision → goals → strategies → milestones → execution
- **Multiple strategy exploration** for each goal to find optimal approaches
- **Adaptive execution** with continuous learning and evidence-based changes
- **Comprehensive measurement** frameworks for tracking progress
- **Cross-platform support** for both Windows (PowerShell) and Unix (Bash) systems
- **AI-powered memory system** for continuous learning and improvement
- **18 powerful slash commands** for complete workflow coverage
- **Advanced analytics and insights** for data-driven development

## Recent Changes

EOF

# Add the actual commits to the release notes
if [ -n "$COMMITS" ]; then
  echo "" >> release_notes.md
  echo "## Changes in This Release" >> release_notes.md
  echo "" >> release_notes.md
  echo "$COMMITS" >> release_notes.md
else
  echo "" >> release_notes.md
  echo "No new commits in this release." >> release_notes.md
fi

cat >> release_notes.md << EOF

## Supported AI Agents

All packages include templates for:
- Claude Code, GitHub Copilot, Gemini CLI, Cursor, Qwen Code, opencode, Codex CLI, Windsurf, Kilo Code, Auggie CLI, Roo Code, Amazon Q Developer CLI

EOF

echo "Generated release notes:"
cat release_notes.md
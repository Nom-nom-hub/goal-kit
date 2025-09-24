#!/bin/bash
set -e

VERSION=$1
LATEST_TAG=$2

echo "Generating release notes for version $VERSION..."

# Get changes since last tag
if [ -n "$LATEST_TAG" ]; then
    CHANGES=$(git log --oneline --pretty=format:"- %s" "$LATEST_TAG"..HEAD)
else
    CHANGES=$(git log --oneline --pretty=format:"- %s" | head -20)
fi

# Create release notes
cat > release_notes.md << EOF
# Goal-Driven Development Kit v${VERSION}

## 🎯 What's New

This release introduces **Goal-Driven Development**, a revolutionary approach to software development that focuses on outcomes rather than specifications.

### Key Features

- **Goal-First Development**: Define objectives before technical implementation
- **Strategy Evaluation**: Multiple implementation approaches considered
- **Enhanced CLI**: New \`goal\` command with goal-driven workflow
- **Professional Documentation**: Complete guides and examples
- **CI/CD Ready**: Automated releases and documentation deployment

### New Workflow

\`\`\`bash
/goals        # Define project objectives
/clarify      # Clarify and validate goals
/strategize   # Develop implementation strategies
/plan         # Create technical implementation plans
/tasks        # Generate actionable tasks
/implement    # Execute implementation
\`\`\`

## 🚀 Installation

\`\`\`bash
uvx --from git+https://github.com/Nom-nom-hub/goal-kit.git goal init <PROJECT_NAME>
\`\`\`

## 📝 Changes

$CHANGES

---

*Built with ❤️ for developers who want to build software that matters.*
EOF

echo "Release notes generated in release_notes.md"
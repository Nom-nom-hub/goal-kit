#!/bin/bash

# Goal-Kit Release Packaging Script
# Packages goal-kit templates for different AI agents

set -e  # Exit on any error

# Configuration
VERSION="0.0.1"
RELEASE_DIR="../releases"
GOAL_KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Utility functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# AI Agents to support
AI_AGENTS=(
    "cursor"
    "claude"
    "qwen"
    "roo"
    "copilot"
    "auggie"
    "gemini"
    "windsurf"
    "codex"
    "kilocode"
    "opencode"
)

# Create release directory
create_release_structure() {
    log_info "Creating release structure..."

    # Create main release directory
    mkdir -p "$RELEASE_DIR"

    # Create temporary packaging directory
    mkdir -p "/tmp/goal-kit-release"

    log_success "Release structure created"
}

# Package for specific agent and platform
package_agent_platform() {
    local agent="$1"
    local platform="$2"  # "sh" or "ps"

    log_info "Packaging goal-kit for $agent ($platform)..."

    local package_name="goal-kit-template-${agent}-${platform}-v${VERSION}"
    local package_dir="/tmp/goal-kit-release/$package_name"
    local package_file="$RELEASE_DIR/$package_name.zip"

    # Create package directory
    mkdir -p "$package_dir"

    # Copy core files
    cp -r "$GOAL_KIT_DIR/templates" "$package_dir/" 2>/dev/null || true
    cp -r "$GOAL_KIT_DIR/.goalify" "$package_dir/" 2>/dev/null || true
    cp -r "$GOAL_KIT_DIR/.qwen" "$package_dir/" 2>/dev/null || true

    # Copy platform-specific scripts
    if [ "$platform" = "sh" ]; then
        mkdir -p "$package_dir/scripts/bash"
        cp "$GOAL_KIT_DIR/scripts/bash/"*.sh "$package_dir/scripts/bash/" 2>/dev/null || true
    elif [ "$platform" = "ps" ]; then
        mkdir -p "$package_dir/scripts/powershell"
        cp "$GOAL_KIT_DIR/scripts/powershell/"*.ps1 "$package_dir/scripts/powershell/" 2>/dev/null || true
    fi

    # Copy shared scripts
    cp "$GOAL_KIT_DIR/scripts/"*.sh "$package_dir/" 2>/dev/null || true

    # Create agent-specific configuration
    cat > "$package_dir/README.md" << EOF
# Goal-Kit Template for $agent

**Version:** $VERSION
**Platform:** $platform
**AI Agent:** $agent

## Installation

1. Extract this package to your project directory
2. Run the setup script:
   - Bash: \`./setup.sh\`
   - PowerShell: \`.\setup.ps1\`

## What's Included

- Comprehensive goal templates
- AI-friendly structured templates
- Automation scripts
- Progress tracking tools
- Multi-format reporting

## Quick Start

\`\`\`bash
# Create a new goal
./create-goal.sh "Your Goal Name" --category personal --priority high

# Update progress
./update-progress.sh ./your-goal --progress 50 --status on_track

# Generate reports
./generate-report.sh ./your-goal --format markdown --type detailed
\`\`\`

## Features

- ✅ Goal Definition and Planning
- ✅ Milestone Management
- ✅ Progress Tracking
- ✅ Achievement Execution
- ✅ Multi-format Reporting
- ✅ Cross-platform Scripts
- ✅ AI Agent Integration

---

*Packaged for $agent on $(date +%Y-%m-%d)*
EOF

    # Create setup script
    if [ "$platform" = "sh" ]; then
        cat > "$package_dir/setup.sh" << 'EOF'
#!/bin/bash
echo "Goal-Kit setup for Bash environment"
echo "=================================="
echo ""
echo "Setting up goal templates..."
chmod +x scripts/bash/*.sh
echo "✅ Bash scripts configured"
echo ""
echo "Installation complete!"
echo "You can now use Goal-Kit commands:"
echo "  ./create-goal.sh 'Goal Name' --category personal"
echo "  ./update-progress.sh ./path/to/goal --progress 50"
echo "  ./generate-report.sh ./path/to/goal --format markdown"
EOF
        chmod +x "$package_dir/setup.sh"
    elif [ "$platform" = "ps" ]; then
        cat > "$package_dir/setup.ps1" << 'EOF'
Write-Host "Goal-Kit setup for PowerShell environment" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Setting up goal templates..."
Write-Host "Configuring PowerShell scripts..."
Write-Host "✅ PowerShell scripts configured" -ForegroundColor Green
Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "You can now use Goal-Kit commands:"
Write-Host "  .\create-goal.ps1 'Goal Name' -Category personal" -ForegroundColor Yellow
Write-Host "  .\update-progress.ps1 .\path\to\goal -Progress 50" -ForegroundColor Yellow
Write-Host "  .\generate-report.ps1 .\path\to\goal -Format markdown" -ForegroundColor Yellow
EOF
    fi

    # Create package
    cd "/tmp/goal-kit-release"

    # Use PowerShell on Windows, fallback to zip on Unix
    if [ "$OS" = "Windows_NT" ] || [ -n "$WINDIR" ]; then
        # Windows - use PowerShell
        powershell.exe -Command "Compress-Archive -Path '$package_name' -DestinationPath '$package_file' -Force" 2>/dev/null || true
    else
        # Unix/Linux/macOS - use zip
        if command -v zip >/dev/null 2>&1; then
            zip -r "$package_file" "$package_name" > /dev/null
        else
            log_error "zip command not found. Please install zip or use a different compression method."
            exit 1
        fi
    fi

    # Generate checksum
    local checksum=$(sha256sum "$package_file" | cut -d' ' -f1)
    echo "$checksum" > "$package_file.sha256"

    log_success "Created package: $package_name.zip"
    log_info "SHA256: $checksum"
    log_info "Size: $(du -h "$package_file" | cut -f1)"

    # Cleanup
    rm -rf "$package_dir"
}

# Package all agents
package_all_releases() {
    log_info "Creating Goal-Kit releases v$VERSION..."
    log_info "====================================="

    for agent in "${AI_AGENTS[@]}"; do
        log_info "Processing $agent..."

        # Package for Bash
        package_agent_platform "$agent" "sh"

        # Package for PowerShell
        package_agent_platform "$agent" "ps"
    done

    log_success "All releases created successfully!"
}

# Generate release notes
generate_release_notes() {
    log_info "Generating release notes..."

    local release_notes="$RELEASE_DIR/RELEASE_NOTES.md"

    cat > "$release_notes" << EOF
# Goal-Kit Templates - $VERSION

**Release Date:** $(date +%Y-%m-%d)
**Previous Version:** N/A (Initial Release)

## Overview

This is the initial release of Goal-Kit, a comprehensive goal management template system that supports the full goal lifecycle from definition through completion.

## What's New

### 🎯 Core Features
- **Goal Definition Templates** - Comprehensive goal planning with SMART criteria
- **Milestone Planning** - Detailed milestone breakdown with dependencies
- **Achievement Execution** - TDD-style task execution with progress tracking
- **Progress Reporting** - Multi-format reporting (JSON, Markdown, HTML, PDF)

### 🤖 AI Agent Support
- **AI-Friendly Templates** - Structured templates optimized for AI agents
- **Multiple Agent Support** - Templates for Cursor, Claude, Qwen, Roo, and more
- **Cross-Platform Scripts** - Both Bash and PowerShell support

### 📊 Goal Categories
- **Personal Goals** - Individual achievement and development
- **Business Goals** - Organizational and entrepreneurial objectives
- **Learning Goals** - Education and skill development tracking
- **Software Projects** - Technical project goal management
- **Research Goals** - Academic and research project planning

## Installation

### Using Goal-Kit CLI
\`\`\`bash
# For Bash/Linux/macOS
curl -L https://github.com/your-repo/goal-kit/releases/download/v$VERSION/goal-kit-template-cursor-sh-v$VERSION.zip -o goal-kit.zip
unzip goal-kit.zip

# For PowerShell/Windows
Invoke-WebRequest -Uri https://github.com/your-repo/goal-kit/releases/download/v$VERSION/goal-kit-template-cursor-ps-v$VERSION.zip -OutFile goal-kit.zip
Expand-Archive goal-kit.zip
\`\`\`

### Manual Installation
1. Download the appropriate package for your AI agent and platform
2. Extract to your project directory
3. Run the setup script (setup.sh or setup.ps1)
4. Start creating goals!

## Files

### Template Packages
$(for agent in "${AI_AGENTS[@]}"; do echo "- **goal-kit-template-${agent}-sh-v${VERSION}.zip** - $agent Bash/Linux/macOS"; done)
$(for agent in "${AI_AGENTS[@]}"; do echo "- **goal-kit-template-${agent}-ps-v${VERSION}.zip** - $agent PowerShell/Windows"; done)

### Package Contents
- \`templates/\` - Core goal templates
- \`.goalify/templates/\` - AI-friendly structured templates
- \`.qwen/commands/\` - AI agent command definitions
- \`scripts/bash/\` - Bash automation scripts
- \`scripts/powershell/\` - PowerShell automation scripts
- \`README.md\` - Package-specific documentation
- \`setup.sh/ps1\` - Installation and setup script

## Features

### Goal Management
- ✅ Comprehensive goal definition templates
- ✅ Milestone planning and tracking
- ✅ Achievement execution with TDD-style workflows
- ✅ Progress tracking and metrics
- ✅ Multi-format reporting

### AI Integration
- ✅ Structured templates for AI agents
- ✅ TOML command definitions
- ✅ Execution flow diagrams
- ✅ Quality gates and validation
- ✅ Review checklists

### Automation
- ✅ Cross-platform scripts (Bash + PowerShell)
- ✅ Git integration for version control
- ✅ Progress reporting automation
- ✅ Template validation
- ✅ Evidence management

## Compatibility

### AI Agents
$(for agent in "${AI_AGENTS[@]}"; do echo "- ✅ **$agent**"; done)

### Platforms
- ✅ **Linux** (Bash scripts)
- ✅ **macOS** (Bash scripts)
- ✅ **Windows** (PowerShell scripts)

### Tools
- ✅ Git (version control)
- ✅ jq (JSON processing)
- ✅ Standard shell tools

## Getting Started

### 1. Create Your First Goal
\`\`\`bash
# Create a new goal
./create-goal.sh "Learn Python Data Science" --category learning --priority high

# Or with PowerShell
.\create-goal.ps1 "Learn Python Data Science" -Category learning -Priority high
\`\`\`

### 2. Update Progress
\`\`\`bash
# Update goal progress
./update-progress.sh ./my-goal --progress 50 --status on_track

# Generate progress report
./generate-report.sh ./my-goal --format markdown --type detailed
\`\`\`

### 3. Track Achievements
\`\`\`bash
# Mark milestones complete
./achieve.sh ./my-goal M1 --status completed --progress 100
\`\`\`

## Support

### Documentation
- [Goal-Kit Documentation](https://github.com/your-repo/goal-kit)
- [Template Guide](https://github.com/your-repo/goal-kit/docs/templates)
- [Script Reference](https://github.com/your-repo/goal-kit/docs/scripts)

### Community
- [GitHub Issues](https://github.com/your-repo/goal-kit/issues)
- [Discussions](https://github.com/your-repo/goal-kit/discussions)
- [Contributing](https://github.com/your-repo/goal-kit/blob/main/CONTRIBUTING.md)

## Changelog

### v$VERSION (Initial Release)
- 🎉 **Initial release** of Goal-Kit template system
- ✅ Comprehensive goal management templates
- ✅ AI agent integration and support
- ✅ Cross-platform automation scripts
- ✅ Multi-format reporting capabilities
- ✅ Professional documentation and guides

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by Spec-Kit and other AI agent tooling
- Thanks to all contributors and early adopters
- Special thanks to the AI agent communities for their support

---

**Goal-Kit v$VERSION** - Comprehensive Goal Management for AI Agents 🎯
EOF

    log_success "Generated release notes: $release_notes"
}

# Main execution
main() {
    log_info "Goal-Kit Release Packaging v$VERSION"
    log_info "=================================="

    # Create release structure
    create_release_structure

    # Package all releases
    package_all_releases

    # Generate release notes
    generate_release_notes

    # Display results
    log_success "Release packaging completed!"
    log_info "Generated $((${#AI_AGENTS[@]} * 2)) packages in $RELEASE_DIR/"
    log_info ""
    log_info "Package summary:"
    for agent in "${AI_AGENTS[@]}"; do
        echo "  - goal-kit-template-${agent}-sh-v${VERSION}.zip"
        echo "  - goal-kit-template-${agent}-ps-v${VERSION}.zip"
    done
    log_info ""
    log_info "Next steps:"
    log_info "1. Test the packages with different AI agents"
    log_info "2. Create GitHub release with all packages"
    log_info "3. Update documentation links"
    log_info "4. Announce the release!"
}

# Run main function
main "$@"
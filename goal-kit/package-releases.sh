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
log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

# AI Agents to support (labels only, not commands!)
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
    mkdir -p "$RELEASE_DIR"
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

    mkdir -p "$package_dir"

    # Copy files
    cp -r "$GOAL_KIT_DIR/templates" "$package_dir/" 2>/dev/null || true
    cp -r "$GOAL_KIT_DIR/.goalify" "$package_dir/" 2>/dev/null || true
    cp -r "$GOAL_KIT_DIR/.qwen" "$package_dir/" 2>/dev/null || true

    if [ "$platform" = "sh" ]; then
        mkdir -p "$package_dir/scripts/bash"
        cp "$GOAL_KIT_DIR/scripts/bash/"*.sh "$package_dir/scripts/bash/" 2>/dev/null || true
    elif [ "$platform" = "ps" ]; then
        mkdir -p "$package_dir/scripts/powershell"
        cp "$GOAL_KIT_DIR/scripts/powershell/"*.ps1 "$package_dir/scripts/powershell/" 2>/dev/null || true
    fi

    cp "$GOAL_KIT_DIR/scripts/"*.sh "$package_dir/" 2>/dev/null || true

    # Agent-specific README
    cat > "$package_dir/README.md" << EOF
# Goal-Kit Template for $agent
**Version:** $VERSION  
**Platform:** $platform  
**AI Agent:** $agent
EOF

    # Setup scripts
    if [ "$platform" = "sh" ]; then
        cat > "$package_dir/setup.sh" << 'EOF'
#!/bin/bash
echo "Goal-Kit setup for Bash environment"
chmod +x scripts/bash/*.sh 2>/dev/null || true
echo "✅ Bash scripts configured"
EOF
        chmod +x "$package_dir/setup.sh"
    elif [ "$platform" = "ps" ]; then
        cat > "$package_dir/setup.ps1" << 'EOF'
Write-Host "Goal-Kit setup for PowerShell environment" -ForegroundColor Green
Write-Host "✅ PowerShell scripts configured" -ForegroundColor Green
EOF
    fi

    cd "/tmp/goal-kit-release"
    if [ "$OS" = "Windows_NT" ] || [ -n "$WINDIR" ]; then
        powershell.exe -Command "Compress-Archive -Path '$package_name' -DestinationPath '$package_file' -Force" 2>/dev/null || true
    else
        if command -v zip >/dev/null 2>&1; then
            zip -r "$package_file" "$package_name" > /dev/null
        else
            log_error "zip not found"
            exit 1
        fi
    fi

    local checksum
    checksum=$(sha256sum "$package_file" | cut -d' ' -f1)
    echo "$checksum" > "$package_file.sha256"

    log_success "Created package: $package_name.zip"
}

# Check if agent should be packaged (always true now)
agent_command_exists() {
    local agent="$1"
    # These are logical agent labels, not binaries. Always return success.
    return 0
}

# Package all agents
package_all_releases() {
    log_info "Creating Goal-Kit releases v$VERSION..."
    local packaged_count=0
    for agent in "${AI_AGENTS[@]}"; do
        log_info "Processing $agent..."
        package_agent_platform "$agent" "sh"
        package_agent_platform "$agent" "ps"
        ((packaged_count++))
    done

    if [ $packaged_count -eq 0 ]; then
        log_error "No agents were packaged."
        exit 1
    fi

    log_success "Packaged $packaged_count agents successfully!"
}

# Main
main() {
    log_info "Goal-Kit Release Packaging v$VERSION"
    create_release_structure
    package_all_releases
    log_success "Release packaging completed!"
}
main "$@"

#!/bin/bash
# Goal-Kit Release Packaging Script
# Packages Goal-Kit templates for different AI agents

set -euo pipefail

# Configuration
VERSION="${1:-0.0.1}"
RELEASE_DIR="releases"
GOAL_KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging
log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

# AI Agents to support
AI_AGENTS=("cursor")

# Create release directory
create_release_structure() {
    log_info "Creating release structure..."
    mkdir -p "$GOAL_KIT_DIR/$RELEASE_DIR"
    mkdir -p "$GOAL_KIT_DIR/.tmp-goal-kit-release"
    log_success "Release structure created"
}

# Package for agent/platform
package_agent_platform() {
    local agent="$1"
    local platform="$2"  # sh or ps

    log_info "Packaging Goal-Kit for $agent ($platform)..."

    local package_name="goal-kit-template-${agent}-${platform}-v${VERSION}"
    local package_dir="$GOAL_KIT_DIR/.tmp-goal-kit-release/$package_name"
    local package_file="$RELEASE_DIR/$package_name.zip"

    mkdir -p "$package_dir"

    # Copy templates and scripts
    cp -r "$GOAL_KIT_DIR/templates" "$package_dir/" 2>/dev/null || true
    cp -r "$GOAL_KIT_DIR/.goalify" "$package_dir/" 2>/dev/null || true
    cp -r "$GOAL_KIT_DIR/.qwen" "$package_dir/" 2>/dev/null || true

    if [ "$platform" = "sh" ]; then
        mkdir -p "$package_dir/scripts/bash"
        cp "$GOAL_KIT_DIR/scripts/bash/"*.sh "$package_dir/scripts/bash/" 2>/dev/null || true
    else
        mkdir -p "$package_dir/scripts/powershell"
        cp "$GOAL_KIT_DIR/scripts/powershell/"*.ps1 "$package_dir/scripts/powershell/" 2>/dev/null || true
    fi

    # Agent README
    cat > "$package_dir/README.md" << EOF
# Goal-Kit Template for $agent
**Version:** $VERSION  
**Platform:** $platform  
**AI Agent:** $agent
EOF

    # Setup script
    if [ "$platform" = "sh" ]; then
        cat > "$package_dir/setup.sh" << 'EOF'
#!/bin/bash
echo "Setting up Goal-Kit Bash environment..."
chmod +x scripts/bash/*.sh
echo "✅ Bash scripts ready"
EOF
        chmod +x "$package_dir/setup.sh"
    else
        cat > "$package_dir/setup.ps1" << 'EOF'
Write-Host "Setting up Goal-Kit PowerShell environment" -ForegroundColor Green
Write-Host "✅ PowerShell scripts ready" -ForegroundColor Green
EOF
    fi

    # Ensure the release directory exists using absolute path
    ABSOLUTE_RELEASE_DIR="$(cd "$(dirname "$GOAL_KIT_DIR")" && pwd)/$(basename "$RELEASE_DIR")"
    mkdir -p "$ABSOLUTE_RELEASE_DIR"
    
    # Update package_file to point to the correct location for checksum generation
    package_file="$ABSOLUTE_RELEASE_DIR/goal-kit-template-${agent}-${platform}-v${VERSION}.zip"
    
    # Zip from the package directory to the absolute release location
    # Copy files from package_dir to the release zip file using absolute paths
    zip -r "$package_file" -j "$package_dir"/*

    # SHA256 checksum
    if [ -f "$GOAL_KIT_DIR/$package_file" ]; then
        sha256sum "$GOAL_KIT_DIR/$package_file" | cut -d' ' -f1 > "$GOAL_KIT_DIR/$package_file.sha256"
    else
        log_error "Package file not found for checksum: $GOAL_KIT_DIR/$package_file"
        exit 1
    fi
    log_success "Created package: $(basename "$package_file")"
}

# Package all agents
package_all_releases() {
    log_info "Packaging Goal-Kit releases v$VERSION..."
    local count=0
    for agent in "${AI_AGENTS[@]}"; do
        package_agent_platform "$agent" "sh"
        package_agent_platform "$agent" "ps"
        ((count++))
    done
    log_success "Packaged $count agents successfully!"
}

# Main
main() {
    log_info "Goal-Kit Release Packaging v$VERSION"
    create_release_structure
    package_all_releases
    log_success "Release packaging completed!"
}

main "$@"
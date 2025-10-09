param(
    [switch]$Verbose = $false,
    [switch]$Fix = $false
)

# Check prerequisites for Goal Kit development

# Load common utilities
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$scriptDir\common.ps1"

if ($Verbose) {
    Write-Info "Checking Goal Kit prerequisites..."
}

# Required tools for Goal Kit development
$requiredTools = @(
    @{Name = "git"; Description = "Git version control"; Url = "https://git-scm.com/downloads"},
    @{Name = "uv"; Description = "Python package manager"; Url = "https://docs.astral.sh/uv/"}
)

# Optional but recommended tools
$optionalTools = @(
    @{Name = "node"; Description = "Node.js runtime"; Url = "https://nodejs.org/"},
    @{Name = "python"; Description = "Python runtime"; Url = "https://python.org/"},
    @{Name = "docker"; Description = "Docker containerization"; Url = "https://docker.com/"}
)

# AI agent tools (at least one should be available)
$agentTools = @(
    @{Name = "claude"; Description = "Claude Code CLI"; Url = "https://docs.anthropic.com/en/docs/claude-code/setup"},
    @{Name = "code"; Description = "Visual Studio Code"; Url = "https://code.visualstudio.com/"},
    @{Name = "cursor"; Description = "Cursor IDE"; Url = "https://cursor.sh/"},
    @{Name = "gemini"; Description = "Gemini CLI"; Url = "https://github.com/google-gemini/gemini-cli"},
    @{Name = "qwen"; Description = "Qwen Code CLI"; Url = "https://github.com/QwenLM/qwen-code"},
    @{Name = "opencode"; Description = "opencode CLI"; Url = "https://opencode.ai"},
    @{Name = "codex"; Description = "Codex CLI"; Url = "https://github.com/openai/codex"},
    @{Name = "windsurf"; Description = "Windsurf IDE"; Url = "https://windsurf.com/"},
    @{Name = "kilocode"; Description = "Kilo Code IDE"; Url = "https://github.com/Kilo-Org/kilocode"},
    @{Name = "auggie"; Description = "Auggie CLI"; Url = "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli"},
    @{Name = "q"; Description = "Amazon Q Developer CLI"; Url = "https://aws.amazon.com/developer/learning/q-developer-cli/"}
)

Write-Info "Checking required tools..."
$missingRequired = @()
foreach ($tool in $requiredTools) {
    if ($Verbose) {
        Write-Info "  Checking $($tool.Name)..."
    }

    if (Test-CommandExists $tool.Name) {
        if ($Verbose) {
            try {
                $version = & $tool.Name --version 2>$null | Select-Object -First 1
                Write-Success "  $($tool.Name): $version"
            }
            catch {
                Write-Success "  $($tool.Name): version check not available"
            }
        }
    }
    else {
        $missingRequired += $tool
        Write-Error "  $($tool.Name): NOT FOUND"
    }
}

# Check optional tools
Write-Info "Checking optional tools..."
$missingOptional = @()
foreach ($tool in $optionalTools) {
    if ($Verbose) {
        Write-Info "  Checking $($tool.Name)..."
    }

    if (Test-CommandExists $tool.Name) {
        if ($Verbose) {
            try {
                $version = & $tool.Name --version 2>$null | Select-Object -First 1
                Write-Success "  $($tool.Name): $version"
            }
            catch {
                Write-Success "  $($tool.Name): version check not available"
            }
        }
    }
    else {
        $missingOptional += $tool
        if ($Verbose) {
            Write-Warning "  $($tool.Name): NOT FOUND (optional)"
        }
    }
}

# Check AI agent tools
Write-Info "Checking AI agent tools..."
$agentFound = $false
$missingAgents = @()
foreach ($tool in $agentTools) {
    if ($Verbose) {
        Write-Info "  Checking $($tool.Name)..."
    }

    if (Test-CommandExists $tool.Name) {
        $agentFound = $true
        if ($Verbose) {
            try {
                $version = & $tool.Name --version 2>$null | Select-Object -First 1
                Write-Success "  $($tool.Name): $version"
            }
            catch {
                Write-Success "  $($tool.Name): version check not available"
            }
        }
    }
    else {
        $missingAgents += $tool
        if ($Verbose) {
            Write-Warning "  $($tool.Name): NOT FOUND"
        }
    }
}

# Summary
""
if ($missingRequired.Count -eq 0) {
    Write-Success "All required tools are installed!"
}
else {
    Write-Error "Missing required tools:"
    foreach ($tool in $missingRequired) {
        "  - $($tool.Name) ($($tool.Description))"
        "    Install: $($tool.Url)"
    }

    if ($Fix) {
        Write-Info "Attempting to fix missing prerequisites..."

        # Try to install uv (most common missing tool)
        if (Test-CommandExists "curl") {
            Write-Info "Installing uv package manager..."
            try {
                powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
            }
            catch {
                Write-Warning "Failed to install uv automatically. Please install manually."
            }
        }
    }
}

if ($missingOptional.Count -gt 0) {
    Write-Warning "Missing optional tools (development will still work):"
    foreach ($tool in $missingOptional) {
        "  - $($tool.Name) ($($tool.Description))"
        "    Install: $($tool.Url)"
    }
}

if (-not $agentFound) {
    Write-Warning "No AI agent tools found. For the best experience, install at least one:"
    foreach ($tool in $missingAgents) {
        "  - $($tool.Name) ($($tool.Description))"
        "    Install: $($tool.Url)"
    }
}
else {
    Write-Success "At least one AI agent tool is available!"
}

""
if ($missingRequired.Count -eq 0) {
    Write-Success "Goal Kit prerequisites check completed successfully!"
    Write-Info "You can now use Goal Kit for goal-driven development."
}
else {
    Write-Error "Please install missing required tools before using Goal Kit."
    exit 1
}
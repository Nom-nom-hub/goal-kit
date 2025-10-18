param(
    [switch]$Verbose = $false,
    [switch]$Force = $false
)

# Update AI agent context for Goal Kit development

# Load common utilities
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$scriptDir\common.ps1"

# Function to display usage information
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [OPTIONS]" -ForegroundColor Cyan
    ""
    "Update AI agent context files with current Goal Kit project information."
    ""
    "OPTIONS:"
    "    -Verbose          Enable verbose output"
    "    -Force           Force update even if no changes detected"
    "    -h, -?           Show this help message"
    ""
    "EXAMPLES:"
    "    $($MyInvocation.MyCommand.Name)"
    "    $($MyInvocation.MyCommand.Name) -Verbose"
    "    $($MyInvocation.MyCommand.Name) -Force"
    ""
}

# Show help if requested
if ($args -contains "-h" -or $args -contains "-?") {
    Show-Usage
    exit 0
}

# Validate we're in a git repository
if (-not (Test-GitRepo)) {
    Write-Error "Not in a git repository"
    Write-Info "Please run this from the root of a Goal Kit project"
    exit 1
}

# Get project information
$projectRoot = Get-GitRoot
Set-Location $projectRoot

# Check if this is a Goal Kit project
if (-not (Test-Path ".goalkit/vision.md")) {
    Write-Error "Not a Goal Kit project"
    Write-Info "Please run 'goalkeeper init' first to set up the project"
    exit 1
}

if ($Verbose) {
    Write-Info "Updating agent context in $projectRoot"
}

# Agent context files to update (in order of preference)
$contextFiles = @(
    "CLAUDE.md",
    ".claude\context.md",
    "GEMINI.md",
    ".gemini\context.md",
    "CURSOR.md",
    ".cursor\context.md",
    "WINDSURF.md",
    ".windsurf\context.md",
    "KILOCODE.md",
    ".kilocode\context.md"
)

$updatedFiles = @()
$projectName = Split-Path $projectRoot -Leaf
$currentBranch = git branch --show-current
$activeGoalsCount = 0

if (Test-Path "goals") {
    $activeGoalsCount = (Get-ChildItem "goals" -Directory).Count
}

# Generate context content
$contextContent = @"
// Goal Kit Project Context

**Project**: $projectName
**Branch**: $currentBranch
**Active Goals**: $activeGoalsCount
**Updated**: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")

## 🎯 Goal-Driven Development Status

This project uses Goal-Driven Development methodology. Focus on:
- Measurable outcomes over feature specifications
- Multiple strategy exploration before implementation
- Learning and adaptation during execution
- Success metrics validation

## 📋 Available Commands

### Core Commands
- **/goalkit.vision** - Establish project vision and principles
- **/goalkit.goal** - Define goals and success criteria
- **/goalkit.strategies** - Explore implementation strategies
- **/goalkit.milestones** - Create measurable milestones
- **/goalkit.execute** - Execute with learning and adaptation



## 🚀 Project Vision

$(if (Test-Path ".goalkit\vision.md") {
    Get-Content ".goalkit\vision.md" -Head 10 | Where-Object { $_ -notlike "#*" } | Select-Object -First 5
})

## 🎯 Active Goals

$(if (Test-Path "goals" -and $activeGoalsCount -gt 0) {
    "Recent goals:"
    Get-ChildItem "goals" -Directory | ForEach-Object {
        $goalDir = $_.FullName
        $goalStatement = Get-Content "$goalDir\goal.md" -ErrorAction SilentlyContinue |
            Where-Object { $_ -like "*Goal Statement*" } |
            Select-Object -First 1 |
            ForEach-Object { $_ -replace ".*Goal Statement:\s*", "" }
        $statement = if ($goalStatement) { $goalStatement } else { "Goal definition in progress" }
        "- **$($_.Name)**: $statement"
    } | Select-Object -First 3
} else {
    "No active goals yet. Use /goalkit.goal to create your first goal."
})

## 📊 Development Principles

Remember these core principles:
1. **Outcome-First**: Prioritize user and business outcomes
2. **Strategy Flexibility**: Multiple valid approaches exist for any goal
3. **Measurement-Driven**: Progress must be measured and validated
4. **Learning Integration**: Treat implementation as hypothesis testing
5. **Adaptive Planning**: Change course based on evidence

## 🔧 Next Recommended Actions

$(if ($activeGoalsCount -eq 0) {
    "1. Use /goalkit.vision to establish project vision"
    "2. Use /goalkit.goal to define first goal"
} else {
    "1. Review active goals in goals/ directory"
    "2. Use /goalkit.strategies to explore implementation approaches"
    "3. Use /goalkit.milestones to plan measurable progress steps"
})

---

*This context is automatically updated by update-agent-context.ps1. Last updated: $(Get-Date)*

"@

# Update context files
foreach ($contextFile in $contextFiles) {
    $fullPath = Join-Path $projectRoot $contextFile
    if ((Test-Path $fullPath) -or $Force) {
        try {
            $contextContent | Out-File $fullPath -Encoding UTF8
            $updatedFiles += $contextFile
            if ($Verbose) {
                Write-Success "Updated $contextFile"
            }
        }
        catch {
            Write-Error "Failed to update $contextFile"
        }
    }
}

# Summary
if ($updatedFiles.Count -gt 0) {
    Write-Success "Updated agent context in $($updatedFiles.Count) file(s):"
    foreach ($file in $updatedFiles) {
        "  - $file"
    }
}
else {
    Write-Warning "No agent context files found to update"
    Write-Info "Supported files:"
    foreach ($file in $contextFiles) {
        "  - $file"
    }
}

""
Write-Success "Agent context update completed!"
Write-Info "Project: $projectName"
Write-Info "Branch: $currentBranch"
Write-Info "Active Goals: $activeGoalsCount"

if ($activeGoalsCount -gt 0) {
    Write-Info "Recent goals:"
    Get-ChildItem "goals" -Directory | ForEach-Object {
        "  - $($_.Name)"
    } | Select-Object -First 3
}
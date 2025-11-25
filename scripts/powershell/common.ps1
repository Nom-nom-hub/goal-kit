# Common utilities for Goal Kit PowerShell scripts

# Strict error handling
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

# Color codes for output
$Colors = @{
    Red = 'Red'
    Green = 'Green'
    Yellow = 'Yellow'
    Blue = 'Cyan'
    Cyan = 'Cyan'
    Magenta = 'Magenta'
    White = 'White'
}

# Global variables for error handling
$script:ScriptError = $false
$script:TempFiles = @()

# Cleanup function
function Cleanup-TempFiles {
    foreach ($tempFile in $script:TempFiles) {
        try {
            if (Test-Path $tempFile) {
                Remove-Item -Path $tempFile -Force -Recurse -ErrorAction SilentlyContinue
            }
        } catch {
            # Silently ignore cleanup errors
        }
    }
}

# Register cleanup on exit
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup-TempFiles }

# Handle errors
function Handle-Error {
    param(
        [string]$Message,
        [int]$ExitCode = 1
    )
    
    $script:ScriptError = $true
    Write-Error-Custom $Message
    exit $ExitCode
}

# Output functions with colors
function Write-Colored {
    param(
        [string]$Message,
        [string]$Color = 'White'
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Info {
    param([string]$Message)
    Write-Colored "[INFO] $Message" -Color $Colors.Blue
}

function Write-Success {
    param([string]$Message)
    Write-Colored "[SUCCESS] $Message" -Color $Colors.Green
}

function Write-Warning {
    param([string]$Message)
    Write-Colored "[WARNING] $Message" -Color $Colors.Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Colored "[ERROR] $Message" -Color $Colors.Red
}

function Write-Step {
    param([string]$Message)
    Write-Colored "[STEP] $Message" -Color $Colors.Cyan
}

function Write-Goal {
    param([string]$Message)
    Write-Colored "[GOAL] $Message" -Color $Colors.Magenta
}

# Git utilities
function Test-GitRepo {
    try {
        git rev-parse --git-dir 2>$null | Out-Null
        return $?
    } catch {
        return $false
    }
}

function Get-GitRoot {
    try {
        $root = git rev-parse --show-toplevel 2>$null
        if ($?) {
            return $root
        }
        return $null
    } catch {
        return $null
    }
}

# Command existence check
function Test-CommandExists {
    param([string]$Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
}

# Require command or exit
function Require-Command {
    param(
        [string]$Command,
        [string]$InstallHint = ""
    )
    
    if (-not (Test-CommandExists $Command)) {
        Write-Error-Custom "Required command not found: $Command"
        if (-not [string]::IsNullOrEmpty($InstallHint)) {
            Write-Info "Install it using: $InstallHint"
        }
        exit 1
    }
}

# Require file exists
function Require-File {
    param([string]$FilePath)
    
    if (-not (Test-Path $FilePath)) {
        Handle-Error "Required file not found: $FilePath"
    }
}

# Require directory exists
function Require-Directory {
    param([string]$DirectoryPath)
    
    if (-not (Test-Path $DirectoryPath)) {
        Handle-Error "Required directory not found: $DirectoryPath"
    }
}

# Validate path is writable
function Validate-Writable {
    param([string]$Path)
    
    $parentDir = Split-Path -Parent $Path
    
    if (-not (Test-Path $parentDir)) {
        Write-Error-Custom "Parent directory does not exist: $parentDir"
        return $false
    }
    
    try {
        $testFile = [System.IO.Path]::GetTempFileName()
        Move-Item -Path $testFile -Destination $parentDir -Force -ErrorAction SilentlyContinue
        if (Test-Path (Join-Path $parentDir (Split-Path -Leaf $testFile))) {
            Remove-Item (Join-Path $parentDir (Split-Path -Leaf $testFile)) -Force -ErrorAction SilentlyContinue
        }
    } catch {
        Write-Error-Custom "Directory is not writable: $parentDir"
        return $false
    }
    
    return $true
}

# Register temporary file for cleanup
function Register-TempFile {
    param([string]$FilePath)
    $script:TempFiles += $FilePath
}

# Check for required tools
function Test-Prerequisites {
    $missingTools = @()
    
    if (-not (Test-CommandExists "git")) {
        $missingTools += "git"
    }
    
    if (-not (Test-CommandExists "uv")) {
        $missingTools += "uv"
    }
    
    if ($missingTools.Count -gt 0) {
        Write-Error-Custom "Missing required tools: $($missingTools -join ', ')"
        Write-Info "Please install the missing tools and try again."
        exit 1
    }
    
    Write-Success "All prerequisites are installed"
}

# Create new goal branch
function New-GoalBranch {
    param([string]$GoalName)
    
    $branchName = $GoalName
    
    # Check if branch already exists
    try {
        git rev-parse --verify $branchName 2>$null | Out-Null
        if ($?) {
            Write-Info "Branch $branchName already exists, switching to it"
            git checkout $branchName 2>$null
            if (-not $?) {
                Write-Error-Custom "Failed to switch to branch: $branchName"
                exit 1
            }
        } else {
            Write-Info "Creating new branch: $branchName"
            git checkout -b $branchName 2>$null
            if (-not $?) {
                Write-Error-Custom "Failed to create branch: $branchName"
                exit 1
            }
        }
    } catch {
        Write-Error-Custom "Failed to create or switch to branch: $branchName"
        exit 1
    }
    
    return $branchName
}

# Update agent context
function Update-AgentContext {
    $projectRoot = Get-GitRoot
    
    if ([string]::IsNullOrEmpty($projectRoot)) {
        Write-Error-Custom "Could not determine git root. Not in a git repository."
        return $false
    }
    
    $contextFiles = @(
        "CLAUDE.md",
        ".claude/context.md",
        "GEMINI.md",
        ".gemini/context.md",
        "CURSOR.md",
        ".cursor/context.md",
        "QWEN.md",
        ".qwen/context.md",
        "WINDSURF.md",
        ".windsurf/context.md",
        "KILOCODE.md",
        ".kilocode/context.md",
        "ROO.md",
        ".roo/context.md",
        "CODEBUDDY.md",
        ".codebuddy/context.md",
        "Q.md",
        ".amazonq/context.md",
        "OPENCODE.md",
        "AUGMENT.md",
        ".augment/context.md"
    )
    
    $currentBranch = git branch --show-current 2>$null
    if ([string]::IsNullOrEmpty($currentBranch)) {
        $currentBranch = "unknown"
    }
    
    $activeGoals = 0
    $goalsPath = Join-Path -Path $projectRoot -ChildPath "goals"
    if (Test-Path $goalsPath) {
        $activeGoals = @(Get-ChildItem -Path $goalsPath -Directory).Count
    }
    
    $foundContextFile = $false
    
    foreach ($contextFile in $contextFiles) {
        $fullPath = Join-Path -Path $projectRoot -ChildPath $contextFile
        
        if (Test-Path $fullPath) {
            Write-Info "Updating context in $contextFile"
            $foundContextFile = $true
            
            $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
            
            $contextContent = @"
# Goal Kit Project Context

**Project**: $(Split-Path -Leaf $projectRoot)
**Branch**: $currentBranch
**Active Goals**: $activeGoals
**Updated**: $timestamp

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

"@
            
            # Add vision content if it exists
            $visionPath = Join-Path (Join-Path $projectRoot ".goalkit") "vision.md"
            if (Test-Path $visionPath) {
                $visionLines = (Get-Content $visionPath | Where-Object { -not $_.StartsWith("#") }) | Select-Object -First 10
                $contextContent += ($visionLines -join "`n")
            }
            
            $contextContent += @"

## 🎯 Active Goals

"@
            
            # Add goal information
            if (Test-Path $goalsPath) {
                $goalDirs = @(Get-ChildItem -Path $goalsPath -Directory | Select-Object -First 3)
                if ($goalDirs.Count -gt 0) {
                    $contextContent += "Recent goals:`n"
                    foreach ($goalDir in $goalDirs) {
                        $goalFile = Join-Path $goalDir.FullName "goal.md"
                        if (Test-Path $goalFile) {
                            $contextContent += "- **$($goalDir.Name)**: Goal definition in progress`n"
                        }
                    }
                } else {
                    $contextContent += "No active goals yet. Use /goalkit.goal to create your first goal.`n"
                }
            } else {
                $contextContent += "No active goals yet. Use /goalkit.goal to create your first goal.`n"
            }
            
            $contextContent += @"
## 📊 Development Principles

Remember these core principles:
1. **Outcome-First**: Prioritize user and business outcomes
2. **Strategy Flexibility**: Multiple valid approaches exist for any goal
3. **Measurement-Driven**: Progress must be measured and validated
4. **Learning Integration**: Treat implementation as hypothesis testing
5. **Adaptive Planning**: Change course based on evidence

## 🔧 Next Recommended Actions

"@
            
            if (-not (Test-Path $goalsPath) -or @(Get-ChildItem -Path $goalsPath -Directory).Count -eq 0) {
                $contextContent += @"
1. Use /goalkit.vision to establish project vision
2. Use /goalkit.goal to define first goal
"@
            } else {
                $contextContent += @"
1. Review active goals in goals/ directory
2. Use /goalkit.strategies to explore implementation approaches
3. Use /goalkit.milestones to plan measurable progress steps
"@
            }
            
            $timestamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
            $contextContent += @"

---

*This context is automatically updated by update-agent-context.ps1. Last updated: $timestamp*

"@
            
            Set-Content -Path $fullPath -Value $contextContent -Encoding UTF8
            return $true
        }
    }
    
    if (-not $foundContextFile) {
        Write-Warning "No agent context file found to update"
        return $false
    }
    
    return $false
}

# Validate goal context
function Test-GoalContext {
    $currentDir = Get-Location
    
    if ($currentDir -notmatch "goals") {
        Write-Error-Custom "Not in a goal directory"
        Write-Info "Please navigate to a goal directory (e.g., goals\001-user-authentication\)"
        exit 1
    }
    
    if (-not (Test-Path "goal.md")) {
        Write-Error-Custom "Missing required file: goal.md"
        exit 1
    }
    
    Write-Success "Goal context validated"
}

# Setup goal environment
function Set-GoalEnvironment {
    param([string]$GoalDir)
    
    $projectRoot = Get-GitRoot
    
    if ([string]::IsNullOrEmpty($projectRoot)) {
        Write-Error-Custom "Could not determine git root. Not in a git repository."
        return $false
    }
    
    $goalName = Split-Path -Leaf $GoalDir
    
    $env:GOAL_KIT_PROJECT_ROOT = $projectRoot
    $env:GOAL_KIT_GOAL_DIR = $GoalDir
    $env:GOAL_KIT_GOAL_NAME = $goalName
    
    Write-Info "Goal environment configured"
    Write-Info "  Project Root: $projectRoot"
    Write-Info "  Goal Directory: $GoalDir"
    Write-Info "  Goal Name: $goalName"
    
    return $true
}

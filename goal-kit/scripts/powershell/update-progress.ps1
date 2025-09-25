
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalPath,

    [Parameter(Mandatory=$false)]
    [int]$Progress,

    [Parameter(Mandatory=$false)]
    [string]$Status,

    [Parameter(Mandatory=$false)]
    [string[]]$Metrics,

    [Parameter(Mandatory=$false)]
    [string]$Notes,

    [Parameter(Mandatory=$false)]
    [string]$Report,

    [Parameter(Mandatory=$false)]
    [string]$Evidence,

    [Parameter(Mandatory=$false)]
    [switch]$Verbose,

    [Parameter(Mandatory=$false)]
    [switch]$Help
)

# Goal-Kit PowerShell Progress Update Script
# Updates goal progress and generates reports

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$GoalKitDir = Split-Path -Parent $ScriptDir

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$NC = "White"

# Utility functions
function Write-Info {
    param([string]$Message)
    Write-Host "[$Blue]INFO[$NC] $Message" -ForegroundColor $Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[$Green]SUCCESS[$NC] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[$Yellow]WARNING[$NC] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[$Red]ERROR[$NC] $Message" -ForegroundColor $Red
}

function Show-Help {
    Write-Host "Goal-Kit PowerShell Progress Update Script" -ForegroundColor $Green
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor $Yellow
    Write-Host "    .\update-progress.ps1 [OPTIONS] GOAL_PATH" -ForegroundColor $White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor $Yellow
    Write-Host "    -Progress PERCENT     Overall progress percentage (0-100)" -ForegroundColor $White
    Write-Host "    -Status STATUS        Progress status (not_started, in_progress, on_track, behind, ahead, completed)" -ForegroundColor $White
    Write-Host "    -Metrics KEY:VALUE    Progress metrics (can be used multiple times)" -ForegroundColor $White
    Write-Host "    -Notes NOTES          Progress notes" -ForegroundColor $White
    Write-Host "    -Report FORMAT        Generate report in specified format (json, markdown, html)" -ForegroundColor $White
    Write-Host "    -Evidence FILE        Add evidence file" -ForegroundColor $White
    Write-Host "    -Verbose              Verbose output" -ForegroundColor $White
    Write-Host "    -Help                 Show this help message" -ForegroundColor $White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor $Yellow
    Write-Host "    .\update-progress.ps1 ./my-goal -Progress 75 -Status on_track -Metrics 'tasks_completed:45','total_tasks:60'" -ForegroundColor $White
    Write-Host "    .\update-progress.ps1 ./my-goal -Progress 90 -Status ahead -Report markdown" -ForegroundColor $White
    Write-Host "    .\update-progress.ps1 ./my-goal -Metrics 'accuracy:94%' -Notes 'Model performance improved significantly'" -ForegroundColor $White
}

# Validate dependencies
function Test-Dependencies {
    try {
        $jqVersion = & jq --version 2>$null
        if (-not $jqVersion) {
            Write-Error "jq is required but not installed"
            exit 1
        }
    }
    catch {
        Write-Error "jq is required but not installed"
        exit 1
    }

    try {
        $gitVersion = & git --version 2>$null
        if (-not $gitVersion) {
            Write-Warning "git not found - version control features will be limited"
        }
    }
    catch {
        Write-Warning "git not found - version control features will be limited"
    }
}

# Validate input
function Test-Input {
    param(

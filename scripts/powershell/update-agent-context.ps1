# Update agent context files with latest project information
# This script updates all agent context files (.claude/context.md, CLAUDE.md, etc.)
# with current project state, active goals, and vision information

param(
    [switch]$Json = $false
)

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function Update-Context {
    param(
        [bool]$JsonMode
    )
    
    # Check if we're in a git repository
    if (-not (Test-GitRepo)) {
        Write-Error-Custom "Not in a git repository"
        Write-Info "Please run this from the root of a Goal Kit project"
        exit 1
    }
    
    # Get project root
    $projectRoot = Get-GitRoot
    if ([string]::IsNullOrEmpty($projectRoot)) {
        Write-Error-Custom "Could not determine git root. Not in a git repository."
        exit 1
    }
    
    Set-Location $projectRoot | Out-Null
    
    # Check if this is a Goal Kit project
    $visionFile = Join-Path -Path ".goalkit" -ChildPath "vision.md"
    if (-not (Test-Path $visionFile)) {
        Write-Error-Custom "Not a Goal Kit project"
        Write-Info "Please run 'goalkeeper init' first to set up the project"
        exit 1
    }
    
    # If JSON mode, output JSON and exit early
    if ($JsonMode) {
        $jsonOutput = @{
            "STATUS" = "context-updated"
            "PROJECT_ROOT" = $projectRoot
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }
    
    # Update agent context using the common function
    $result = Update-AgentContext
    
    if ($result) {
        Write-Success "Agent context files updated"
    } else {
        Write-Info "Agent context already up to date or no context files found"
    }
    
    Write-Host ""
    Write-Info "Context Update Complete:"
    Write-Host "  Project: $(Split-Path -Leaf $projectRoot)"
    Write-Host "  Location: $projectRoot"
    Write-Host "  Updated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

# Main execution
Update-Context -JsonMode $Json

#!/usr/bin/env pwsh
# Setup detailed retrospective in a Goal Kit project

param(
    [Parameter(Mandatory=$true)]
    [string]$GoalDirectory,
    
    [switch]$DryRun,
    [switch]$Force,
    [switch]$Json,
    [switch]$Verbose
)

# Import common functions
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$ScriptDir/common.ps1"

function Create-DetailedRetrospectiveFile {
    param(
        [string]$GoalDir,
        [bool]$DryRunMode,
        [bool]$ForceMode,
        [bool]$JsonMode,
        [bool]$VerboseMode
    )
    
    # Check if in git repo
    if (-not (Test-GitRepo)) {
        Write-Error "Not in a git repository. Please run this from the root of a Goal Kit project"
        exit 1
    }
    
    $ProjectRoot = Get-GitRoot
    if (-not $ProjectRoot) {
        Write-Error "Could not determine git root"
        exit 1
    }
    
    Set-Location $ProjectRoot
    
    if ($JsonMode) {
        if (-not (Test-Path $GoalDir -PathType Container)) {
            Write-Error "Goal directory does not exist: $GoalDir"
            exit 1
        }
        
        $RetrospectiveFile = Join-Path $GoalDir "detailed-retrospective.md"
        
        $output = @{
            GOAL_DIR = $GoalDir
            RETROSPECTIVE_FILE = $RetrospectiveFile
        } | ConvertTo-Json -Compress
        
        Write-Output $output
        return
    }
    
    # Verify goal directory exists
    if (-not (Test-Path $GoalDir -PathType Container)) {
        Write-Error "Goal directory does not exist: $GoalDir"
        exit 1
    }
    
    $RetrospectiveFile = Join-Path $GoalDir "detailed-retrospective.md"
    
    # Check if file already exists
    if ((Test-Path $RetrospectiveFile) -and -not $DryRunMode) {
        Write-Warning "Detailed retrospective file already exists: $RetrospectiveFile"
        if (-not $ForceMode) {
            $response = Read-Host "Overwrite existing detailed retrospective? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Information "Operation cancelled"
                return
            }
        }
    }
    
    if ($DryRunMode) {
        Write-Information "[DRY RUN] Would create detailed retrospective file: $RetrospectiveFile"
        return
    }
    
    # Check if template exists
    $TemplateFile = Join-Path $ProjectRoot "templates/detailed-retrospective-template.md"
    if (Test-Path $TemplateFile) {
        Copy-Item $TemplateFile $RetrospectiveFile -Force
        
        # Replace placeholders
        $GoalDirName = Split-Path -Leaf $GoalDir
        $Timestamp = Get-Date -Format "yyyy-MM-dd"
        
        $Content = Get-Content $RetrospectiveFile -Raw
        $Content = $Content -replace "\[Goal or Program Name\]", $GoalDirName
        $Content = $Content -replace "\[Date\]", $Timestamp
        $Content = $Content -replace "\[Name\]", "[Facilitator]"
        
        Set-Content $RetrospectiveFile $Content
    }
    
    Write-Success "Created detailed retrospective file: $RetrospectiveFile"
    Write-Information "Detailed retrospective setup completed!"
    Write-Information ""
    Write-Information "Detailed Retrospective Details:"
    Write-Information "  Goal Directory: $GoalDir"
    Write-Information "  Retrospective File: $RetrospectiveFile"
    Write-Information ""
    Write-Information "Next Steps:"
    Write-Information "  1. Gather execution metrics: timeline, velocity, scope, resources"
    Write-Information "  2. Review quality & reliability: code coverage, bugs, uptime, incidents"
    Write-Information "  3. Analyze risk outcomes: which risks materialized, which were avoided"
    Write-Information "  4. Collect team feedback: collaboration, communication, satisfaction"
    Write-Information "  5. Quantify outcomes with baselines and trends"
    Write-Information "  6. Identify what worked well and celebrate successes"
    Write-Information "  7. Identify improvement areas and specific action items"
    Write-Information "  8. Prepare leadership summary with key findings"
    Write-Information "  9. Archive lessons learned for future teams"
}

# Main
Create-DetailedRetrospectiveFile -GoalDir $GoalDirectory -DryRunMode $DryRun -ForceMode $Force -JsonMode $Json -VerboseMode $Verbose

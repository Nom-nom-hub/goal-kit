#!/usr/bin/env pwsh
# Setup quality assurance plan in a Goal Kit project

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

function Create-QualityAssuranceFile {
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
        
        $QAFile = Join-Path $GoalDir "quality-assurance.md"
        
        $output = @{
            GOAL_DIR = $GoalDir
            QA_FILE = $QAFile
        } | ConvertTo-Json -Compress
        
        Write-Output $output
        return
    }
    
    # Verify goal directory exists
    if (-not (Test-Path $GoalDir -PathType Container)) {
        Write-Error "Goal directory does not exist: $GoalDir"
        exit 1
    }
    
    $QAFile = Join-Path $GoalDir "quality-assurance.md"
    
    # Check if file already exists
    if ((Test-Path $QAFile) -and -not $DryRunMode) {
        Write-Warning "Quality assurance file already exists: $QAFile"
        if (-not $ForceMode) {
            $response = Read-Host "Overwrite existing quality assurance plan? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Information "Operation cancelled"
                return
            }
        }
    }
    
    if ($DryRunMode) {
        Write-Information "[DRY RUN] Would create quality assurance file: $QAFile"
        return
    }
    
    # Check if template exists
    $TemplateFile = Join-Path $ProjectRoot "templates/quality-assurance-template.md"
    if (Test-Path $TemplateFile) {
        Copy-Item $TemplateFile $QAFile -Force
        
        # Replace placeholders
        $GoalDirName = Split-Path -Leaf $GoalDir
        $Timestamp = Get-Date -Format "yyyy-MM-dd"
        
        $Content = Get-Content $QAFile -Raw
        $Content = $Content -replace "\[Goal Name\]", $GoalDirName
        $Content = $Content -replace "\[Date\]", $Timestamp
        $Content = $Content -replace "\[QA Lead / Engineering Lead\]", "[QA Lead]"
        
        Set-Content $QAFile $Content
    }
    
    Write-Success "Created quality assurance file: $QAFile"
    Write-Information "Quality assurance setup completed!"
    Write-Information ""
    Write-Information "Quality Assurance Details:"
    Write-Information "  Goal Directory: $GoalDir"
    Write-Information "  QA File: $QAFile"
    Write-Information ""
    Write-Information "Next Steps:"
    Write-Information "  1. Define critical quality dimensions (3-4 max: functionality, performance, reliability, etc.)"
    Write-Information "  2. Set quality goals for each dimension"
    Write-Information "  3. Define testing strategy (80% unit, 40% integration, 10% E2E)"
    Write-Information "  4. Document acceptance criteria for all features"
    Write-Information "  5. Define release gates (code quality, functional, performance, accessibility, security)"
    Write-Information "  6. Set up quality metrics dashboard (coverage, pass rate, bug trends)"
    Write-Information "  7. Establish quality review cadence"
}

# Main
Create-QualityAssuranceFile -GoalDir $GoalDirectory -DryRunMode $DryRun -ForceMode $Force -JsonMode $Json -VerboseMode $Verbose

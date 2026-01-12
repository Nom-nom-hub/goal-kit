#!/usr/bin/env pwsh
# Setup risk register in a Goal Kit project

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

function Create-RiskRegisterFile {
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
        
        $RiskRegisterFile = Join-Path $GoalDir "risk-register.md"
        
        $output = @{
            GOAL_DIR = $GoalDir
            RISK_REGISTER_FILE = $RiskRegisterFile
        } | ConvertTo-Json -Compress
        
        Write-Output $output
        return
    }
    
    # Verify goal directory exists
    if (-not (Test-Path $GoalDir -PathType Container)) {
        Write-Error "Goal directory does not exist: $GoalDir"
        exit 1
    }
    
    $RiskRegisterFile = Join-Path $GoalDir "risk-register.md"
    
    # Check if file already exists
    if ((Test-Path $RiskRegisterFile) -and -not $DryRunMode) {
        Write-Warning "Risk register file already exists: $RiskRegisterFile"
        if (-not $ForceMode) {
            $response = Read-Host "Overwrite existing risk register? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Information "Operation cancelled"
                return
            }
        }
    }
    
    if ($DryRunMode) {
        Write-Information "[DRY RUN] Would create risk register file: $RiskRegisterFile"
        return
    }
    
    # Check if template exists
    $TemplateFile = Join-Path $ProjectRoot "templates/risk-register-template.md"
    if (Test-Path $TemplateFile) {
        Copy-Item $TemplateFile $RiskRegisterFile -Force
        
        # Replace placeholders
        $GoalDirName = Split-Path -Leaf $GoalDir
        $Timestamp = Get-Date -Format "yyyy-MM-dd"
        
        $Content = Get-Content $RiskRegisterFile -Raw
        $Content = $Content -replace "\[Goal Name\]", $GoalDirName
        $Content = $Content -replace "\[Date\]", $Timestamp
        $Content = $Content -replace "\[Name\]", "[Team Member]"
        
        Set-Content $RiskRegisterFile $Content
    }
    
    Write-Success "Created risk register file: $RiskRegisterFile"
    Write-Information "Risk register setup completed!"
    Write-Information ""
    Write-Information "Risk Register Details:"
    Write-Information "  Goal Directory: $GoalDir"
    Write-Information "  Risk Register File: $RiskRegisterFile"
    Write-Information ""
    Write-Information "Next Steps:"
    Write-Information "  1. Identify 8-12 risks across technical, organizational, market, and external categories"
    Write-Information "  2. Assess each risk: Probability (Low/Medium/High) × Impact (Low/Medium/High)"
    Write-Information "  3. Define mitigation strategies for Top 5 risks"
    Write-Information "  4. Assign owners and timelines to each mitigation"
    Write-Information "  5. Set up weekly risk triage cadence"
}

# Main
Create-RiskRegisterFile -GoalDir $GoalDirectory -DryRunMode $DryRun -ForceMode $Force -JsonMode $Json -VerboseMode $Verbose

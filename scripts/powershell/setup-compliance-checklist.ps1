#!/usr/bin/env pwsh
# Setup compliance checklist in a Goal Kit project

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

function Create-ComplianceChecklistFile {
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
        
        $ComplianceFile = Join-Path $GoalDir "compliance-checklist.md"
        
        $output = @{
            GOAL_DIR = $GoalDir
            COMPLIANCE_FILE = $ComplianceFile
        } | ConvertTo-Json -Compress
        
        Write-Output $output
        return
    }
    
    # Verify goal directory exists
    if (-not (Test-Path $GoalDir -PathType Container)) {
        Write-Error "Goal directory does not exist: $GoalDir"
        exit 1
    }
    
    $ComplianceFile = Join-Path $GoalDir "compliance-checklist.md"
    
    # Check if file already exists
    if ((Test-Path $ComplianceFile) -and -not $DryRunMode) {
        Write-Warning "Compliance checklist file already exists: $ComplianceFile"
        if (-not $ForceMode) {
            $response = Read-Host "Overwrite existing compliance checklist? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Information "Operation cancelled"
                return
            }
        }
    }
    
    if ($DryRunMode) {
        Write-Information "[DRY RUN] Would create compliance checklist file: $ComplianceFile"
        return
    }
    
    # Check if template exists
    $TemplateFile = Join-Path $ProjectRoot "templates/compliance-checklist-template.md"
    if (Test-Path $TemplateFile) {
        Copy-Item $TemplateFile $ComplianceFile -Force
        
        # Replace placeholders
        $GoalDirName = Split-Path -Leaf $GoalDir
        $Timestamp = Get-Date -Format "yyyy-MM-dd"
        
        $Content = Get-Content $ComplianceFile -Raw
        $Content = $Content -replace "\[Goal/Deliverable\]", $GoalDirName
        $Content = $Content -replace "\[Date\]", $Timestamp
        $Content = $Content -replace "\[Name\]", "[Compliance Officer]"
        
        Set-Content $ComplianceFile $Content
    }
    
    Write-Success "Created compliance checklist file: $ComplianceFile"
    Write-Information "Compliance checklist setup completed!"
    Write-Information ""
    Write-Information "Compliance Checklist Details:"
    Write-Information "  Goal Directory: $GoalDir"
    Write-Information "  Compliance File: $ComplianceFile"
    Write-Information ""
    Write-Information "Next Steps:"
    Write-Information "  1. Identify all applicable compliance frameworks (GDPR, HIPAA, SOC2, PCI-DSS, WCAG, internal policies)"
    Write-Information "  2. List specific requirements for each framework"
    Write-Information "  3. Assess current state: Met, Partially Met, At Risk, Not Met"
    Write-Information "  4. Document gaps with root causes"
    Write-Information "  5. Create remediation plans for Critical/High gaps with owners and timelines"
    Write-Information "  6. Collect evidence (policies, logs, documentation, certifications)"
    Write-Information "  7. Set up monitoring and review cadence"
    Write-Information "  8. Prepare for audits (internal and external)"
}

# Main
Create-ComplianceChecklistFile -GoalDir $GoalDirectory -DryRunMode $DryRun -ForceMode $Force -JsonMode $Json -VerboseMode $Verbose

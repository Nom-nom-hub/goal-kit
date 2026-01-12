#!/usr/bin/env pwsh
# Setup security review in a Goal Kit project

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

function Create-SecurityReviewFile {
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
        
        $SecurityReviewFile = Join-Path $GoalDir "security-review.md"
        
        $output = @{
            GOAL_DIR = $GoalDir
            SECURITY_REVIEW_FILE = $SecurityReviewFile
        } | ConvertTo-Json -Compress
        
        Write-Output $output
        return
    }
    
    # Verify goal directory exists
    if (-not (Test-Path $GoalDir -PathType Container)) {
        Write-Error "Goal directory does not exist: $GoalDir"
        exit 1
    }
    
    $SecurityReviewFile = Join-Path $GoalDir "security-review.md"
    
    # Check if file already exists
    if ((Test-Path $SecurityReviewFile) -and -not $DryRunMode) {
        Write-Warning "Security review file already exists: $SecurityReviewFile"
        if (-not $ForceMode) {
            $response = Read-Host "Overwrite existing security review? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Information "Operation cancelled"
                return
            }
        }
    }
    
    if ($DryRunMode) {
        Write-Information "[DRY RUN] Would create security review file: $SecurityReviewFile"
        return
    }
    
    # Check if template exists
    $TemplateFile = Join-Path $ProjectRoot "templates/security-review-template.md"
    if (Test-Path $TemplateFile) {
        Copy-Item $TemplateFile $SecurityReviewFile -Force
        
        # Replace placeholders
        $GoalDirName = Split-Path -Leaf $GoalDir
        $Timestamp = Get-Date -Format "yyyy-MM-dd"
        
        $Content = Get-Content $SecurityReviewFile -Raw
        $Content = $Content -replace "\[Goal/Deliverable\]", $GoalDirName
        $Content = $Content -replace "\[Date\]", $Timestamp
        $Content = $Content -replace "\[Name/Team\]", "[Security Team]"
        
        Set-Content $SecurityReviewFile $Content
    }
    
    Write-Success "Created security review file: $SecurityReviewFile"
    Write-Information "Security review setup completed!"
    Write-Information ""
    Write-Information "Security Review Details:"
    Write-Information "  Goal Directory: $GoalDir"
    Write-Information "  Security Review File: $SecurityReviewFile"
    Write-Information ""
    Write-Information "Next Steps:"
    Write-Information "  1. Identify threat vectors (external attacks, insider threats, data breaches, DoS, supply chain)"
    Write-Information "  2. Document data flows and external dependencies"
    Write-Information "  3. Scan for OWASP Top 10 vulnerabilities"
    Write-Information "  4. Check dependencies for known CVEs"
    Write-Information "  5. Assess compliance requirements (GDPR, HIPAA, SOC2, etc.)"
    Write-Information "  6. Triage findings: Critical/High/Medium/Low with remediation plans"
    Write-Information "  7. Escalate Critical/High findings immediately"
}

# Main
Create-SecurityReviewFile -GoalDir $GoalDirectory -DryRunMode $DryRun -ForceMode $Force -JsonMode $Json -VerboseMode $Verbose

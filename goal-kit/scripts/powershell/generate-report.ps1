param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalPath,

    [Parameter(Mandatory=$false)]
    [string]$Format = "markdown",

    [Parameter(Mandatory=$false)]
    [string]$Type = "detailed",

    [Parameter(Mandatory=$false)]
    [string]$Period = "all",

    [Parameter(Mandatory=$false)]
    [string]$OutputFile,

    [Parameter(Mandatory=$false)]
    [switch]$IncludeEvidence,

    [Parameter(Mandatory=$false)]
    [switch]$IncludeMetrics,

    [Parameter(Mandatory=$false)]
    [switch]$Charts,

    [Parameter(Mandatory=$false)]
    [switch]$Verbose,

    [Parameter(Mandatory=$false)]
    [switch]$Help
)

# Goal-Kit PowerShell Report Generation Script
# Generates comprehensive progress reports for goals

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
    Write-Host "Goal-Kit PowerShell Report Generation Script" -ForegroundColor $Green
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor $Yellow
    Write-Host "    .\generate-report.ps1 [OPTIONS] GOAL_PATH" -ForegroundColor $White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor $Yellow
    Write-Host "    -Format FORMAT        Report format (json, markdown, html, pdf)" -ForegroundColor $White
    Write-Host "    -Type TYPE            Report type (summary, detailed, milestone, achievement)" -ForegroundColor $White
    Write-Host "    -Period PERIOD        Reporting period (daily, weekly, monthly, quarterly, all)" -ForegroundColor $White
    Write-Host "    -Output FILE          Output file path (default: auto-generated)" -ForegroundColor $White
    Write-Host "    -IncludeEvidence      Include evidence files in report" -ForegroundColor $White
    Write-Host "    -IncludeMetrics       Include detailed metrics" -ForegroundColor $White
    Write-Host "    -Charts               Generate charts and visualizations" -ForegroundColor $White
    Write-Host "    -Verbose              Verbose output" -ForegroundColor $White
    Write-Host "    -Help                 Show this help message" -ForegroundColor $White
    Write-Host ""
    Write-Host "REPORT TYPES:" -ForegroundColor $Yellow
    Write-Host "    summary       - High-level overview with key metrics" -ForegroundColor $White
    Write-Host "    detailed      - Comprehensive report with full details" -ForegroundColor $White
    Write-Host "    milestone     - Focus on milestone progress" -ForegroundColor $White
    Write-Host "    achievement   - Focus on achievement tracking" -ForegroundColor $White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor $Yellow
    Write-Host "    .\generate-report.ps1 ./my-goal -Format markdown -Type detailed" -ForegroundColor $White
    Write-Host "    .\generate-report.ps1 ./my-goal -Format html -Type summary -IncludeMetrics" -ForegroundColor $White
    Write-Host "    .\generate-report.ps1 ./my-goal -Format json -Period monthly -Output ./reports/monthly-report.json" -ForegroundColor $White
}

# Validate dependencies
function Test-Dependencies {
    $missingDeps = @()

    try {
        $jqVersion = & jq --version 2>$null
        if (-not $jqVersion) {
            $missingDeps += "jq"
        }
    }
    catch {
        $missingDeps += "jq"
    }

    if ($missingDeps.Count -gt 0) {
        Write-Error "Missing required dependencies: $($missingDeps -join ', ')"
        Write-Info "Please install the missing dependencies and try again."
        exit 1
    }
}

# Generate output filename if not provided
function Get-OutputFilename {
    param(
        [string]$GoalPath,
        [string]$Format,
        [string]$Type,
        [string]$Period
    )

    if (-not $OutputFile) {
        $goalName = Split-Path $GoalPath -Leaf
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $OutputFile = Join-Path $GoalPath "reports\$($Type)-report-$timestamp.$Format"
    }

    # Ensure output directory exists
    $outputDir = Split-Path $OutputFile -Parent
    if (-not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }

    if ($Verbose) {
        Write-Info "Output file: $OutputFile"
    }

    return $OutputFile
}

# Read goal data
function Read-GoalData {
    param([string]$GoalFile)

    if (-not (Test-Path $GoalFile)) {
        Write-Error "Goal file not found: $GoalFile"
        exit 1
    }

    $goalContent = Get-Content $GoalFile -Raw | ConvertFrom-Json

    # Extract basic goal information
    $script:GoalName = $goalContent.name
    $script:GoalId = $goalContent.metadata.template
    $script:Progress = $goalContent.progress
    $script:Status = $goalContent.status
    $script:Category = $goalContent.category
    $script:Priority = $goalContent.priority
    $script:CreatedAt = $goalContent.created_at
    $script:UpdatedAt = $goalContent.updated_at

    # Calculate duration
    $createdDate = [DateTime]::Parse($CreatedAt)
    $currentDate = Get-Date
    $script:DurationDays = ($currentDate - $createdDate).Days

    if ($Verbose) {
        Write-Info "Read goal data: $GoalName ($Progress% complete)"
    }
}

# Collect progress data
function Get-ProgressData {
    param(
        [string]$GoalPath,
        [string]$Period
    )

    $progressDir = Join-Path $GoalPath "progress"
    $script:ProgressEntries = @()
    $script:MilestoneCount = 0
    $script:AchievementCount = 0

    if (Test-Path $progressDir) {
        $progressFiles = Get-ChildItem "$progressDir\*.json" -ErrorAction SilentlyContinue

        if ($progressFiles) {
            $script:ProgressEntries = $progressFiles
        }
    }

    # Count milestones and achievements
    $milestoneDir = Join-Path $GoalPath "milestones"
    if (Test-Path $milestoneDir) {
        $script:MilestoneCount = (Get-ChildItem "$milestoneDir\*.json" -ErrorAction SilentlyContinue).Count
    }

    $achievementDir = Join-Path $GoalPath "achievements"
    if (Test-Path $achievementDir) {
        $script:AchievementCount = (Get-ChildItem "$achievementDir\*" -File -ErrorAction SilentlyContinue).Count
    }

    if ($Verbose) {
        Write-Info "Found $($ProgressEntries.Count) progress entries, $MilestoneCount milestones, $AchievementCount achievements"
    }
}

# Generate JSON report
function New-JsonReport {
    param(
        [string]$GoalPath,
        [string]$OutputFile
    )

    Write-Info "Generating JSON report..."

    $reportData = @{
        report_metadata = @{
            type = $Type
            format = "json"
            generated_at = (Get-Date -Format "o")
            period = $Period
            generator = "goal-kit-report-generator"
        }
        goal = @{
            name = $GoalName
            id = $GoalId
            progress = $Progress
            status = $Status
            category = $Category
            priority = $Priority
            created_at = $CreatedAt
            updated_at = $UpdatedAt
            duration_days = $DurationDays
        }
        metrics = @{
            milestones_count = $MilestoneCount
            achievements_count = $AchievementCount
            progress_entries_count = $ProgressEntries.Count
        }
    }

    if ($IncludeMetrics -and $ProgressEntries.Count -gt 0) {
        $reportData["progress_history"] = @()
        foreach ($entry in $ProgressEntries) {
            $entryContent = Get-Content $entry.FullName -Raw | ConvertFrom-Json
            $reportData["progress_history"] += $entryContent
        }
    }

    $reportData | ConvertTo-Json -Depth 10 | Set-Content $OutputFile
    Write-Success "Generated JSON report: $OutputFile"
}

# Generate Markdown report
function New-MarkdownReport {
    param(
        [string]$GoalPath,
        [string]$OutputFile
    )

    Write-Info "Generating Markdown report..."

    $reportContent = @"
# Goal Progress Report: $GoalName

## Executive Summary
- **Goal:** $GoalName
- **Progress:** $Progress%
- **Status:** $Status
- **Category:** $Category
- **Priority:** $Priority
- **Report Generated:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC')
- **Report Period:** $Period
- **Duration:** $DurationDays days

## Progress Overview

### Key Metrics
| Metric | Value |
|--------|-------|
| Progress | $Progress% |
| Milestones | $MilestoneCount |
| Achievements | $AchievementCount |
| Progress Entries | $($ProgressEntries.Count) |

### Status Timeline
- **Created:** $(([DateTime]::Parse($CreatedAt)).ToString('yyyy-MM-dd HH:mm UTC'))
- **Last Updated:** $(([DateTime]::Parse($UpdatedAt)).ToString('HH:mm UTC'))

"@

    if ($IncludeMetrics -and $ProgressEntries.Count -gt 0) {
        $reportContent += @"

## Detailed Progress History

### Recent Progress Entries
"@

        # Add recent progress entries (limit to 10)
        $recentEntries = $ProgressEntries | Select-Object -First 10
        foreach ($entry in $recentEntries) {
            $entryContent = Get-Content $entry.FullName -Raw | ConvertFrom-Json
            $timestamp = $entryContent.timestamp
            $progress = $entryContent.progress
            $status = $entryContent.status
            $notes = $entryContent.notes

            $entryDate = [DateTime]::Parse($timestamp)
            $reportContent += @"

#### $($entryDate.ToString('yyyy-MM-dd HH:mm UTC'))
- **Progress:** $progress%
- **Status:** $status
$(if ($notes) { "- **Notes:** $notes" })
"@
        }

        if ($ProgressEntries.Count -eq 0) {
            $reportContent += @"

*No progress entries found for the selected period.*
"@
        }
    }

    if ($IncludeEvidence) {
        $reportContent += @"

## Achievements and Evidence

### Recent Achievements
"@

        $achievementDir = Join-Path $GoalPath "achievements"
        if (Test-Path $achievementDir) {
            $achievementFiles = Get-ChildItem "$achievementDir\*" -File -ErrorAction SilentlyContinue | Select-Object -First 10
            if ($achievementFiles.Count -gt 0) {
                foreach ($file in $achievementFiles) {
                    $filename = $file.Name
                    $reportContent += @"
- [$filename]($($file.FullName))
"@
                }
            } else {
                $reportContent += @"
*No achievements recorded yet.*
"@
            }
        }
    }

    if ($Type -eq "milestone") {
        $reportContent += @"

## Milestone Progress

### Milestone Status
"@

        $milestoneDir = Join-Path $GoalPath "milestones"
        if (Test-Path $milestoneDir) {
            $milestoneFiles = Get-ChildItem "$milestoneDir\*.json" -ErrorAction SilentlyContinue
            if ($milestoneFiles.Count -gt 0) {
                $reportContent += @"
| Milestone | Status | Progress |
|-----------|--------|----------|
"@

                foreach ($milestoneFile in $milestoneFiles) {
                    $milestoneContent = Get-Content $milestoneFile.FullName -Raw | ConvertFrom-Json
                    $name = $milestoneContent.name
                    $status = $milestoneContent.status
                    $progress = $milestoneContent.progress

                    $reportContent += @"
| $name | $status | $progress% |
"@
                }
            } else {
                $reportContent += @"
*No milestones defined yet.*
"@
            }
        }
    }

    $reportContent += @"

## Recommendations

### Next Steps
- Continue regular progress updates
- Review milestone progress regularly
- Celebrate achievements as they are completed
- Adjust goals as needed based on progress

### Success Factors
- Maintain consistent progress tracking
- Regular milestone reviews
- Stakeholder communication
- Adaptability to changing circumstances

## Report Metadata

- **Report Type:** $Type
- **Generated By:** Goal-Kit Report Generator
- **Version:** 1.0
- **Data Period:** $Period

---
*This report was generated automatically by Goal-Kit. Keep up the great work!*
"@

    $reportContent | Set-Content $OutputFile
    Write-Success "Generated Markdown report: $OutputFile"
}

# Generate HTML report
function New-HtmlReport {
    param(
        [string]$GoalPath,
        [string]$OutputFile
    )

    Write-Info "Generating HTML report..."

    $reportContent = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Goal Progress Report: $GoalName</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .header {
            background: linear-gradient(135deg, #007acc, #0056b3);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .metric-item {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4caf50, #81c784);
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #007acc;
            color: white;
        }
        .status-$Status {
            padding: 4px 8px;
            border-radius: 12px;
            color: white;
            font-size: 0.8em;
            text-transform: uppercase;
        }
        .status-completed { background-color: #4caf50; }
        .status-on_track { background-color: #2196f3; }
        .status-behind { background-color: #ff9800; }
        .status-ahead { background-color: #9c27b0; }
        .status-not_started { background-color: #757575; }
        .status-at_risk { background-color: #f44336; }
        .section {
            margin: 30px 0;
        }
        .section h2 {
            color: #007acc;
            border-bottom: 2px solid #007acc;
            padding-bottom: 10px;
        }
        .evidence-item {
            background: #f5f5f5;
            padding: 10px;
            margin: 5px 0;
            border-left: 4px solid #007acc;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Goal Progress Report</h1>
        <h2>$GoalName</h2>
        <p>Generated on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC')</p>
    </div>

    <div class="metric-grid">
        <div class="metric-item">
            <h3>Progress</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: $Progress%"></div>
            </div>
            <strong>$Progress%</strong>
        </div>
        <div class="metric-item">
            <h3>Status</h3>
            <div class="status-$Status">$Status</div>
        </div>
        <div class="metric-item">
            <h3>Category</h3>
            <strong>$Category</strong>
        </div>
        <div class="metric-item">
            <h3>Priority</h3>
            <strong>$Priority</strong>
        </div>
    </div>

    <div class="section">
        <h2>Goal Information</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Goal Name</td><td>$GoalName</td></tr>
            <tr><td>Progress</td><td>$Progress%</td></tr>
            <tr><td>Status</td><td><span class="status-$Status">$Status</span></td></tr>
            <tr><td>Category</td><td>$Category</td></tr>
            <tr><td>Priority</td><td>$Priority</td></tr>
            <tr><td>Created</td><td>$(([DateTime]::Parse($CreatedAt)).ToString('yyyy-MM-dd HH:mm UTC'))</td></tr>
            <tr><td>Last Updated</td><td>$(([DateTime]::Parse($UpdatedAt)).ToString('HH:mm UTC'))</td></tr>
            <tr><td>Duration</td><td>$DurationDays days</td></tr>
        </table>
    </div>
"@

    # Add progress history section
    if ($IncludeMetrics -and $ProgressEntries.Count -gt 0) {
        $reportContent += @"

    <div class="section">
        <h2>Recent Progress</h2>
        <table>
            <tr><th>Date</th><th>Progress</th><th>Status</th><th>Notes</th></tr>
"@

        $recentEntries = $ProgressEntries | Select-Object -First 10
        foreach ($entry in $recentEntries) {
            $entryContent = Get-Content $entry.FullName -Raw | ConvertFrom-Json
            $timestamp = $entryContent.timestamp
            $progress = $entryContent.progress
            $status = $entryContent.status
            $notes = $entryContent.notes

            $entryDate = [DateTime]::Parse($timestamp)
            $reportContent += @"
            <tr>
                <td>$($entryDate.ToString('yyyy-MM-dd HH:mm'))</td>
                <td>$progress%</td>
                <td><span class="status-$status">$status</span></td>
                <td>$($notes.Substring(0, [Math]::Min(50, $notes.Length)))...</td>
            </tr>
"@
        }

        $reportContent += @"
        </table>
    </div>
"@
    }

    # Add achievements section
    if ($IncludeEvidence) {
        $reportContent += @"

    <div class="section">
        <h2>Achievements & Evidence</h2>
"@

        $achievementDir = Join-Path $GoalPath "achievements"
        if (Test-Path $achievementDir) {
            $achievementFiles = Get-ChildItem "$achievementDir\*" -File -ErrorAction SilentlyContinue | Select-Object -First 10
            if ($achievementFiles.Count -gt 0) {
                foreach ($file in $achievementFiles) {
                    $filename = $file.Name
                    $fileDate = $file.LastWriteTime
                    $reportContent += @"
        <div class="evidence-item">
            <strong>$filename</strong><br>
            <small>$($fileDate.ToString('yyyy-MM-dd HH:mm'))</small>
        </div>
"@
                }
            } else {
                $reportContent += @"
        <p>No achievements recorded yet.</p>
"@
            }
        }

        $reportContent += @"
    </div>
"@
    }

    # Close HTML
    $reportContent += @"

    <div class="section">
        <h2>Report Information</h2>
        <p><strong>Report Type:</strong> $Type</p>
        <p><strong>Period:</strong> $Period</p>
        <p><strong>Generated by:</strong> Goal-Kit v1.0</p>
    </div>

</body>
</html>
"@

    $reportContent | Set-Content $OutputFile
    Write-Success "Generated HTML report: $OutputFile"
}

# Main execution
function Main {
    Write-Info "Goal-Kit PowerShell Report Generation Script v1.0"
    Write-Info "================================================="

    # Show help if requested
    if ($Help) {
        Show-Help
        return
    }

    # Validate dependencies
    Test-Dependencies

    # Generate output filename
    $OutputFile = Get-OutputFilename $GoalPath $Format $Type $Period

    # Read goal data
    $goalFile = Join-Path $GoalPath "goal.json"
    Read-GoalData $goalFile

    # Collect progress data
    Get-ProgressData $GoalPath $Period

    # Generate report based on format
    switch ($Format) {
        "json" {
            New-JsonReport $GoalPath $OutputFile
        }
        "markdown" {
            New-MarkdownReport $GoalPath $OutputFile
        }
        "html" {
            New-HtmlReport $GoalPath $OutputFile
        }
        "pdf" {
            Write-Info "Generating PDF report..."
            New-MarkdownReport $GoalPath "$OutputFile.md"

            # Check if pandoc is available for PDF generation
            try {
                $pandocVersion = & pandoc --version 2>$null
                if ($pandocVersion) {
                    & pandoc "$OutputFile.md" -o $OutputFile --pdf-engine=pdflatex 2>$null
                    Remove-Item "$OutputFile.md" -ErrorAction SilentlyContinue
                    Write-Success "Generated PDF report: $OutputFile"
                } else {
                    Write-Warning "PDF generation tools not available. PDF report not generated."
                    Write-Info "You can convert the Markdown report to PDF manually."
                }
            }
            catch {
                Write-Warning "PDF generation failed. PDF report not generated."
                Write-Info "You can convert the Markdown report to PDF manually."
            }
        }
        default {
            Write-Error "Unsupported format: $Format"
            exit 1
        }
    }

    Write-Success "Report generation completed successfully!"
    Write-Info "Report saved to: $OutputFile"
    Write-Info "Keep up the great work! 📊"
}

# Run main function
Main
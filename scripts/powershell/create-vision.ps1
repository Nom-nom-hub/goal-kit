# Create or edit the vision document in a Goal Kit project

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$VisionDescription,
    
    [switch]$Edit = $false,
    [switch]$Force = $false,
    [switch]$Json = $false,
    [switch]$Verbose = $false
)

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "common.ps1")

function New-Vision {
    param(
        [string]$VisionDescription,
        [bool]$Edit,
        [bool]$Force,
        [bool]$JsonMode,
        [bool]$VerboseMode
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
    
    # Define vision file path
    $visionFile = Join-Path ".goalkit" "vision.md"
    
    # If JSON mode, output JSON with file path
    if ($JsonMode) {
        $jsonOutput = @{
            "VISION_FILE" = $visionFile
            "VISION_DIR" = ".goalkit"
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }
    
    # Check if vision file already exists
    if (Test-Path $visionFile) {
        if ($Edit -or $VerboseMode) {
            if ($VerboseMode) {
                Write-Info "Opening vision file for editing..."
            }
            # Open in default editor (code, notepad, etc.)
            if (Get-Command code -ErrorAction SilentlyContinue) {
                code $visionFile
            } else {
                notepad $visionFile
            }
            return
        } elseif (-not $Force) {
            Write-Warning "Vision file already exists: $visionFile"
            Write-Info "Use --edit to open in editor or --force to overwrite"
            exit 0
        }
    }
    
    # Create .goalkit directory if it doesn't exist
    $goalKitDir = Join-Path ".goalkit"
    if (-not (Test-Path $goalKitDir)) {
        New-Item -ItemType Directory -Path $goalKitDir -Force | Out-Null
    }
    
    # Get timestamp
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    
    # Check if template exists
    $templatePath = Join-Path $projectRoot ".goalkit" "templates" "vision-template.md"
    if (Test-Path $templatePath) {
        $templateContent = Get-Content -Path $templatePath -Raw
        
        # Replace placeholders if description provided
        if (-not [string]::IsNullOrEmpty($VisionDescription)) {
            $visionContent = $templateContent -replace '\[PROJECT NAME\]', $VisionDescription
        } else {
            $visionContent = $templateContent
        }
        
        $visionContent = $visionContent -replace '\[DATE\]', $timestamp
    } else {
        # Fallback to default content
        $projectName = if (-not [string]::IsNullOrEmpty($VisionDescription)) { $VisionDescription } else { Split-Path -Leaf $projectRoot }
        
        $visionContent = @"
# Vision: $projectName

**Created**: $timestamp
**Last Updated**: $timestamp

## Vision Statement

[Define the overarching vision for this project - what are we trying to achieve and why does it matter?]

## Core Principles

1. **[Principle 1]**: [Explain what this principle means for the project]
2. **[Principle 2]**: [Explain what this principle means for the project]
3. **[Principle 3]**: [Explain what this principle means for the project]

## Success Definition

What will success look like for this vision? Define the key indicators:

- **Market/User Impact**: [Describe the impact on target users or market]
- **Quality Metrics**: [Describe quality standards and expectations]
- **Timeline**: [Rough timeline for vision realization]
- **Team/Resource Impact**: [How this affects the team or organization]

## Strategic Goals

These are the major stepping stones to realize the vision:

1. **[Strategic Goal 1]**: [Description and why it's important]
2. **[Strategic Goal 2]**: [Description and why it's important]
3. **[Strategic Goal 3]**: [Description and why it's important]

## Constraints & Considerations

- **Technical Constraints**: [List any technical limitations or considerations]
- **Resource Constraints**: [List resource limitations]
- **Timeline Constraints**: [Any time-related constraints]
- **Regulatory/Compliance**: [Any compliance or legal considerations]

## Next Steps

1. Refine and validate this vision with stakeholders
2. Define specific goals aligned with this vision
3. Create measurable milestones for progress tracking
4. Communicate the vision clearly to all team members
"@
    }
    
    # Write vision file
    Set-Content -Path $visionFile -Value $visionContent -Encoding UTF8
    Write-Success "Created vision.md: $visionFile"
    
    # Git operations
    git add $visionFile 2>$null | Out-Null
    git commit -m "Add project vision" 2>$null | Out-Null
    
    Write-Success "Vision committed to repository"
    
    # Print summary
    Write-Host ""
    Write-Info "Vision file created successfully!"
    Write-Host "  File: $visionFile"
    Write-Host ""
    Write-Info "Next Steps:"
    Write-Host "  1. Edit the vision file to add your project details"
    Write-Host "  2. Define core principles and success criteria"
    Write-Host "  3. Use /goalkit.goal to define specific goals"
    Write-Host "  4. Use /goalkit.strategies to plan implementation approaches"
    Write-Host ""
}

# Main execution
New-Vision -VisionDescription $VisionDescription -Edit $Edit -Force $Force -JsonMode $Json -VerboseMode $Verbose

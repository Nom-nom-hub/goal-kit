param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

$ReleaseDir = "release-packages"
$ErrorActionPreference = "Stop"

Write-Host "Creating release packages for version $Version..."

# Create release directory
if (!(Test-Path $ReleaseDir)) {
    New-Item -ItemType Directory -Path $ReleaseDir | Out-Null
}

# Function to create template package for an AI agent
function Create-TemplatePackage {
    param(
        [string]$AI,
        [string]$ScriptType
    )

    $TemplateDir = "goal-kit-template-${AI}-${ScriptType}-${Version}"
    Write-Host "Creating template package for ${AI} with ${ScriptType} scripts..."

    # Create template directory structure
    if (!(Test-Path $TemplateDir)) {
        New-Item -ItemType Directory -Path $TemplateDir | Out-Null
    }

    # Copy core files - preserve source structure
    $directories = @("docs", "memory", "src", "templates")
    $files = @("README.md", "LICENSE")

    foreach ($dir in $directories) {
        if (Test-Path $dir) {
            Copy-Item -Path $dir -Destination $TemplateDir -Recurse -Force
        }
    }

    # Copy .github but exclude scripts directory to avoid self-compression issues
    if (Test-Path ".github") {
        Copy-Item -Path ".github" -Destination $TemplateDir -Recurse -Force
        # Remove the scripts directory from the template
        $scriptsPath = Join-Path $TemplateDir ".github\workflows\scripts"
        if (Test-Path $scriptsPath) {
            Remove-Item -Path $scriptsPath -Recurse -Force
        }
    }

    foreach ($file in $files) {
        if (Test-Path $file) {
            Copy-Item -Path $file -Destination $TemplateDir -Force
        }
    }

    # Remove development files
    $removePaths = @(
        "$TemplateDir\.git",
        "$TemplateDir\demo-goal-project",
        "$TemplateDir\spec-kit",
        "$TemplateDir\.qwen",
        "$TemplateDir\.goalify",
        "$TemplateDir\.qodo"
    )

    foreach ($path in $removePaths) {
        if (Test-Path $path) {
            Remove-Item -Path $path -Recurse -Force
        }
    }

    # Create zip file
    $CleanVersion = $Version -replace '^v', ''
    $ZipName = "goal-kit-template-${AI}-${ScriptType}-v${CleanVersion}.zip"

    $TemplateParent = Split-Path -Parent $TemplateDir
    Push-Location $TemplateParent
    Compress-Archive -Path (Split-Path -Leaf $TemplateDir) -DestinationPath $ZipName -Force
    Pop-Location

    # Move zip to release directory
    Move-Item -Path $ZipName -Destination $ReleaseDir -Force

    Write-Host "Created $ZipName"
}

# Create packages for all AI agents and script types
$AI_Agents = @("copilot", "claude", "gemini", "cursor", "qwen", "opencode", "codex", "windsurf", "kilocode", "auggie", "roo", "deepseek", "tabnine", "grok", "codewhisperer")
$Script_Types = @("sh", "ps")

foreach ($AI in $AI_Agents) {
    foreach ($Script in $Script_Types) {
        Create-TemplatePackage -AI $AI -ScriptType $Script
    }
}

Write-Host "Release packages created in $ReleaseDir/"
Get-ChildItem -Path $ReleaseDir -Name
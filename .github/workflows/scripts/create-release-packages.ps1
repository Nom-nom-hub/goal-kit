#!/usr/bin/env pwsh

# Check if version argument is provided
if ($args.Length -ne 1) {
    Write-Error "Usage: create-release-packages.ps1 <version>"
    exit 1
}

$VERSION = $args[0]

Write-Host "Building release packages for $VERSION"

# List of AI agents to create packages for
$AGENTS = @(
    "copilot",
    "claude", 
    "gemini",
    "cursor",
    "qwen",
    "opencode",
    "codex",
    "windsurf",
    "kilocode",
    "auggie",
    "codebuddy",
    "roo",
    "q"
)

# Script types
$SCRIPT_TYPES = @("sh", "ps")

# Create a directory for generated releases
if (!(Test-Path ".genreleases")) {
    New-Item -ItemType Directory -Path ".genreleases" | Out-Null
}

# Function to create a temporary directory for packaging
function Create-TempPackageDir {
    param(
        [string]$Agent,
        [string]$ScriptType
    )

    # Create temp directory using .NET method for cross-platform compatibility
    $tempPath = [System.IO.Path]::GetTempPath()
    $tempDir = Join-Path $tempPath "goalkit_temp_$(Get-Date -Format 'yyyyMMddHHmmss')_$((Get-Random))"
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    
    Write-Host "Created temp dir for $Agent-$ScriptType at $tempDir" -ForegroundColor Yellow

    # Create the .goalkit directory structure in temp
    $goalkitDir = Join-Path $tempDir ".goalkit"
    New-Item -ItemType Directory -Path $goalkitDir -Force | Out-Null
    
    # Copy common files (only if they exist)
    if (Test-Path "memory/") {
        Copy-Item -Path "memory/*" -Destination "$tempDir/memory/" -Recurse -Force
    }
    if (Test-Path "templates/") {
        Copy-Item -Path "templates/*" -Destination "$tempDir/templates/" -Recurse -Force
    }
    
    $filesToCopy = @("CHANGELOG.md", "LICENSE", "README.md", "SECURITY.md", ".gitignore")
    foreach ($file in $filesToCopy) {
        if (Test-Path $file) {
            Copy-Item -Path $file -Destination $tempDir -Force
        }
    }

    # Copy agent-specific files
    switch ($Agent) {
        "copilot" {
            if (Test-Path ".github/agent_templates/copilot") {
                $targetDir = Join-Path $tempDir ".github"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".github/agent_templates/copilot/*" -Destination $targetDir -Recurse -Force
            }
        }
        "claude" {
            if (Test-Path ".claude") {
                $targetDir = Join-Path $tempDir ".claude"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".claude/*" -Destination $targetDir -Recurse -Force
            }
        }
        "gemini" {
            if (Test-Path ".gemini") {
                $targetDir = Join-Path $tempDir ".gemini"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".gemini/*" -Destination $targetDir -Recurse -Force
            }
        }
        "cursor" {
            if (Test-Path ".cursor") {
                $targetDir = Join-Path $tempDir ".cursor"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".cursor/*" -Destination $targetDir -Recurse -Force
            }
        }
        "qwen" {
            if (Test-Path ".qwen") {
                $targetDir = Join-Path $tempDir ".qwen"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".qwen/*" -Destination $targetDir -Recurse -Force
            }
        }
        "opencode" {
            if (Test-Path ".opencode") {
                $targetDir = Join-Path $tempDir ".opencode"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".opencode/*" -Destination $targetDir -Recurse -Force
            }
        }
        "codex" {
            if (Test-Path ".codex") {
                $targetDir = Join-Path $tempDir ".codex"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".codex/*" -Destination $targetDir -Recurse -Force
            }
        }
        "windsurf" {
            if (Test-Path ".windsurf") {
                $targetDir = Join-Path $tempDir ".windsurf"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".windsurf/*" -Destination $targetDir -Recurse -Force
            }
        }
        "kilocode" {
            if (Test-Path ".kilocode") {
                $targetDir = Join-Path $tempDir ".kilocode"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".kilocode/*" -Destination $targetDir -Recurse -Force
            }
        }
        "auggie" {
            if (Test-Path ".augment") {
                $targetDir = Join-Path $tempDir ".augment"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".augment/*" -Destination $targetDir -Recurse -Force
            }
        }
        "roo" {
            if (Test-Path ".roo") {
                $targetDir = Join-Path $tempDir ".roo"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".roo/*" -Destination $targetDir -Recurse -Force
            }
        }
        "q" {
            if (Test-Path ".amazonq") {
                $targetDir = Join-Path $tempDir ".amazonq"
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Copy-Item -Path ".amazonq/*" -Destination $targetDir -Recurse -Force
            }
        }
    }

    # Copy script files based on type
    if ($ScriptType -eq "sh") {
        if (Test-Path "scripts/bash") {
            $targetDir = Join-Path $tempDir ".goalkit/scripts"
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            Copy-Item -Path "scripts/bash/*" -Destination $targetDir -Recurse -Force
        }
    }
    elseif ($ScriptType -eq "ps") {
        if (Test-Path "scripts/powershell") {
            $targetDir = Join-Path $tempDir ".goalkit/scripts"
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            Copy-Item -Path "scripts/powershell/*" -Destination $targetDir -Recurse -Force
        }
    }

    # Clean up unnecessary files from the package
    if (Test-Path "$tempDir/scripts") {
        Remove-Item "$tempDir/scripts" -Recurse -Force
    }
    
    # Remove any hidden .DS_Store files if they exist
    Get-ChildItem -Path $tempDir -Filter ".DS_Store" -Recurse -Force | Remove-Item -Force

    return $tempDir
}

# Main loop to create packages
foreach ($agent in $AGENTS) {
    foreach ($scriptType in $SCRIPT_TYPES) {
        Write-Host "Packaging for $agent with $scriptType scripts..." -ForegroundColor Green
        $TEMP_DIR = Create-TempPackageDir -Agent $agent -ScriptType $scriptType

        # Define archive name
        $ARCHIVE_NAME = "goal-kit-template-$agent-$scriptType-$VERSION.zip"
        
        # Create zip archive using PowerShell Compress-Archive
        try {
            Compress-Archive -Path "$TEMP_DIR/*" -DestinationPath ".genreleases/$ARCHIVE_NAME" -Force
            Write-Host "Created .genreleases/$ARCHIVE_NAME" -ForegroundColor Green
        }
        catch {
            Write-Error "Failed to create archive: $_"
            exit 1
        }

        # Clean up temp directory
        Remove-Item $TEMP_DIR -Recurse -Force
    }
}

Write-Host "All release packages created successfully." -ForegroundColor Green
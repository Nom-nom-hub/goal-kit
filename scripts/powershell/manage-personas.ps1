param(
    [Parameter(Position = 0)]
    [ValidateSet("list", "current", "switch", "status", "help")]
    [string]$Command = "help",
    
    [Parameter(Position = 1)]
    [string]$Persona,
    
    [switch]$Verbose,
    [switch]$Help
)

# Manage agent personas in Goal Kit projects
# Allows switching between specialized agent roles for different tasks

# Load common utilities
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
$CommonScript = Join-Path $ScriptDir "common.ps1"
if (Test-Path $CommonScript) {
    . $CommonScript
}

# Function to display usage information
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [COMMAND] [OPTIONS]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Manage agent personas for specialized roles in Goal Kit projects." -ForegroundColor White
    Write-Host ""
    Write-Host "COMMANDS:" -ForegroundColor Yellow
    Write-Host "    list                    List all available personas" -ForegroundColor White
    Write-Host "    current                 Show currently active persona" -ForegroundColor White
    Write-Host "    switch <persona>        Switch to specified persona" -ForegroundColor White
    Write-Host "    status                  Show detailed status of current persona" -ForegroundColor White
    Write-Host "    help                    Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "    -Verbose                Enable verbose output" -ForegroundColor White
    Write-Host "    -Help                   Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Green
    Write-Host "    $($MyInvocation.MyCommand.Name) list" -ForegroundColor White
    Write-Host "    $($MyInvocation.MyCommand.Name) current" -ForegroundColor White
    Write-Host "    $($MyInvocation.MyCommand.Name) switch github" -ForegroundColor White
    Write-Host "    $($MyInvocation.MyCommand.Name) status" -ForegroundColor White
    Write-Host "    $($MyInvocation.MyCommand.Name) switch milestone -Verbose" -ForegroundColor White
    Write-Host ""
}

if ($Help -or $Command -eq "help") {
    Show-Usage
    exit 0
}

# Get project root
$ProjectRoot = Get-GitRoot
if (-not $ProjectRoot) {
    Write-Error "Not in a git repository"
    exit 1
}

Set-Location $ProjectRoot

# Check if this is a Goal Kit project
$VisionFile = Join-Path $ProjectRoot ".goalkit" "vision.md"
if (-not (Test-Path $VisionFile)) {
    Write-Error "Not a Goal Kit project"
    Write-Info "Please run 'goalkeeper init' first to set up the project"
    exit 1
}

# Get persona config dir
$PersonaConfigDir = Join-Path $ProjectRoot ".goalkit" "personas"
if (-not (Test-Path $PersonaConfigDir)) {
    New-Item -ItemType Directory -Path $PersonaConfigDir -Force | Out-Null
}

# Get current persona file
$CurrentPersonaFile = Join-Path $PersonaConfigDir "current_persona.txt"

# Set default persona if file doesn't exist
if (-not (Test-Path $CurrentPersonaFile)) {
    "general" | Out-File $CurrentPersonaFile -Encoding UTF8
}

# Get personas configuration
$PersonasConfig = @{
    default_persona = "general"
    personas = @{
        general = @{
            name = "General Agent"
            description = "Handles all aspects of goal-driven development without specialization"
            capabilities = @("all")
            default_context = "General goal-driven development agent"
            color = "blue"
        }
        github = @{
            name = "GitHub/Git Specialist"
            description = "Specializes in version control, repository management, and GitHub workflows"
            capabilities = @("git", "github", "version_control", "branching", "merging", "pull_requests")
            default_context = "GitHub/Git specialist focused on repository management, branching strategies, pull requests, and version control best practices"
            color = "orange"
            specializations = @(
                "Git workflow optimization",
                "Branching and merging strategies",
                "Pull request creation and review", 
                "Repository maintenance",
                "Tagging and release management"
            )
        }
        milestone = @{
            name = "Milestone Planner"
            description = "Specializes in breaking down goals into measurable milestones and tracking progress"
            capabilities = @("milestones", "planning", "measurement", "tracking", "goals")
            default_context = "Milestone planning specialist focused on creating measurable, achievable milestones with clear success criteria and tracking mechanisms"
            color = "green"
            specializations = @(
                "Goal decomposition",
                "Milestone creation", 
                "Success metric definition",
                "Progress tracking setup",
                "Dependency mapping"
            )
        }
        strategy = @{
            name = "Strategy Explorer"
            description = "Specializes in exploring multiple implementation strategies and technical approaches"
            capabilities = @("strategies", "technical_decision", "research", "analysis", "architectural_design")
            default_context = "Strategy exploration specialist focused on evaluating different technical approaches, architectural patterns, and implementation strategies"
            color = "purple"
            specializations = @(
                "Technical approach evaluation",
                "Architecture decision support", 
                "Risk assessment",
                "Technology research",
                "Solution comparison"
            )
        }
        qa = @{
            name = "Quality Assurance"
            description = "Specializes in testing, validation, quality metrics, and best practices"
            capabilities = @("testing", "quality", "validation", "review", "best_practices")
            default_context = "Quality assurance specialist focused on testing strategies, validation approaches, code quality, and best practices"
            color = "red"
            specializations = @(
                "Testing strategy development", 
                "Code review processes",
                "Quality metric implementation",
                "Validation frameworks",
                "Best practices enforcement"
            )
        }
        documentation = @{
            name = "Documentation Specialist"
            description = "Specializes in creating and maintaining project documentation"
            capabilities = @("documentation", "writing", "technical_writing", "knowledge_management")
            default_context = "Documentation specialist focused on creating clear, comprehensive documentation for all project aspects"
            color = "teal"
            specializations = @(
                "Technical documentation",
                "API documentation", 
                "Process documentation",
                "Knowledge base creation",
                "User guides"
            )
        }
    }
}

# Function to list all personas
function List-Personas {
    Write-Info "Available Personas:"
    foreach ($personaName in $PersonasConfig.personas.Keys) {
        $info = $PersonasConfig.personas[$personaName]
        Write-Host "  $personaName`: $($info.name) - $($info.description)" -ForegroundColor White
    }
}

# Function to show current persona
function Show-CurrentPersona {
    $CurrentPersona = Get-Content $CurrentPersonaFile -Raw | ForEach-Object { $_.Trim() }
    
    if ($CurrentPersona -eq "general") {
        Write-Success "Current Persona: $CurrentPersona (General Agent)"
        Write-Info "Description: General goal-driven development agent"
    } else {
        $PersonaInfo = $PersonasConfig.personas[$CurrentPersona]
        if ($PersonaInfo) {
            Write-Success "Current Persona: $CurrentPersona ($($PersonaInfo.name))"
            Write-Info "Description: $($PersonaInfo.description)"
        } else {
            Write-Error "Unknown persona: $CurrentPersona"
        }
    }
}

# Function to switch persona
function Switch-Persona {
    param([string]$TargetPersona)
    
    if (-not $PersonasConfig.personas.ContainsKey($TargetPersona)) {
        Write-Error "Invalid persona: $TargetPersona"
        $validPersonas = $PersonasConfig.personas.Keys -join ", "
        Write-Info "Valid personas: $validPersonas"
        exit 1
    }
    
    $PersonaInfo = $PersonasConfig.personas[$TargetPersona]
    
    # Save the new persona
    $TargetPersona | Out-File $CurrentPersonaFile -Encoding UTF8
    
    Write-Success "Switched to persona: $TargetPersona ($($PersonaInfo.name))"
    
    # Update agent context with new persona info
    Update-AgentContext
    
    # Show persona details
    Write-Info "Capabilities: $($PersonaInfo.capabilities -join ", ")"
    $specializations = $PersonaInfo.specializations
    if ($specializations.Count -gt 0) {
        $dispSpecs = if ($specializations.Count -gt 3) { 
            ($specializations[0..2] -join ", ") + "..." 
        } else { 
            ($specializations -join ", ") 
        }
        Write-Info "Specializations: $dispSpecs"
    }
}

# Function to show detailed status
function Show-Status {
    Show-CurrentPersona
    $CurrentPersona = Get-Content $CurrentPersonaFile -Raw | ForEach-Object { $_.Trim() }
    $PersonaInfo = $PersonasConfig.personas[$CurrentPersona]
    
    Write-Host ""
    Write-Info "Persona Details:"
    Write-Host "  Name: $($PersonaInfo.name)" -ForegroundColor White
    Write-Host "  Capabilities: $($PersonaInfo.capabilities -join ", ")" -ForegroundColor White
    Write-Host "  Specializations:" -ForegroundColor White
    foreach ($spec in $PersonaInfo.specializations) {
        Write-Host "    - $spec" -ForegroundColor Gray
    }
}

# Execute command
switch ($Command) {
    "list" {
        List-Personas
    }
    "current" {
        Show-CurrentPersona
    }
    "switch" {
        if (-not $Persona) {
            Write-Error "Please specify a persona to switch to"
            Show-Usage
            exit 1
        }
        Switch-Persona -TargetPersona $Persona
    }
    "status" {
        Show-Status
    }
    "help" {
        Show-Usage
    }
    default {
        Write-Error "Unknown command: $Command"
        Show-Usage
        exit 1
    }
}
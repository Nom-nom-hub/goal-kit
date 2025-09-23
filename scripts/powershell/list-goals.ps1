# list-goals.ps1 - List all goals in the goal-dev-spec project
# Usage: .\list-goals.ps1

# Check if we're in a goal-dev-spec project
if (-not (Test-Path "./.goal/goal.yaml") -and -not (Test-Path "./goal.yaml")) {
    Write-Error "Not in a goal-dev-spec project directory"
    Write-Host "Run 'goal init' first or navigate to a goal-dev-spec project directory"
    exit 1
}

# Use the goal CLI to list goals
if (Get-Command goal -ErrorAction SilentlyContinue) {
    goal list
} else {
    Write-Error "goal CLI not found"
    Write-Host "Please install goal-dev-spec CLI to use this script"
    exit 1
}
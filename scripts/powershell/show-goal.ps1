# show-goal.ps1 - Show details of a specific goal in the goal-dev-spec project
# Usage: .\show-goal.ps1 <goal-id>

# Check if we're in a goal-dev-spec project
if (-not (Test-Path "./.goal/goal.yaml") -and -not (Test-Path "./goal.yaml")) {
    Write-Error "Not in a goal-dev-spec project directory"
    Write-Host "Run 'goal init' first or navigate to a goal-dev-spec project directory"
    exit 1
}

# Check arguments
if ($args.Count -lt 1) {
    Write-Host "Usage: .\show-goal.ps1 <goal-id>"
    Write-Host "Use 'list-goals.ps1' to find goal IDs"
    exit 1
}

$goalId = $args[0]

# Use the goal CLI to show the goal
if (Get-Command goal -ErrorAction SilentlyContinue) {
    goal show $goalId
} else {
    Write-Error "goal CLI not found"
    Write-Host "Please install goal-dev-spec CLI to use this script"
    exit 1
}
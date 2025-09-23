# create-goal.ps1 - Create a new goal in the goal-dev-spec project
# Usage: .\create-goal.ps1 "Goal Title" "Goal Description"

# Check if we're in a goal-dev-spec project
if (-not (Test-Path "./.goal/goal.yaml") -and -not (Test-Path "./goal.yaml")) {
    Write-Error "Not in a goal-dev-spec project directory"
    Write-Host "Run 'goal init' first or navigate to a goal-dev-spec project directory"
    exit 1
}

# Check arguments
if ($args.Count -lt 2) {
    Write-Host "Usage: .\create-goal.ps1 'Goal Title' 'Goal Description'"
    exit 1
}

$goalTitle = $args[0]
$goalDescription = $args[1]

# Use the goal CLI to create the goal
if (Get-Command goal -ErrorAction SilentlyContinue) {
    goal create $goalTitle $goalDescription
} else {
    Write-Error "goal CLI not found"
    Write-Host "Please install goal-dev-spec CLI to use this script"
    exit 1
}
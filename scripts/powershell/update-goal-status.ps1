# update-goal-status.ps1 - Update the status of a specific goal in the goal-dev-spec project
# Usage: .\update-goal-status.ps1 <goal-id> <status>

# Check if we're in a goal-dev-spec project
if (-not (Test-Path "./.goal/goal.yaml") -and -not (Test-Path "./goal.yaml")) {
    Write-Error "Not in a goal-dev-spec project directory"
    Write-Host "Run 'goal init' first or navigate to a goal-dev-spec project directory"
    exit 1
}

# Check arguments
if ($args.Count -lt 2) {
    Write-Host "Usage: .\update-goal-status.ps1 <goal-id> <status>"
    Write-Host "Valid statuses: draft, planned, in_progress, completed, blocked"
    exit 1
}

$goalId = $args[0]
$status = $args[1]

# Use the goal CLI to update the goal status
if (Get-Command goal -ErrorAction SilentlyContinue) {
    # This would require implementing an update command in the goal CLI
    Write-Host "Updating goal $goalId status to $status"
    Write-Host "Note: This functionality needs to be implemented in the goal CLI"
} else {
    Write-Error "goal CLI not found"
    Write-Host "Please install goal-dev-spec CLI to use this script"
    exit 1
}
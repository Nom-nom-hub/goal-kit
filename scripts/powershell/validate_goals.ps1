# PowerShell script to validate goal files
# This simply calls the Python script since PowerShell can run Python

param(
    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$GoalFiles
)

# Check if Python is available
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Python is required to run the goal validator" -ForegroundColor Red
    exit 1
}

# Call the Python validation script with the provided files
$result = python "$PSScriptRoot\validate_goals.py" @GoalFiles

# Pass through the exit code from the Python script
exit $LASTEXITCODE
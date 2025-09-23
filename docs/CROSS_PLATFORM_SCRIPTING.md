# Goal-Dev-Spec Cross-Platform Scripting Capabilities

This document provides a comprehensive overview of the Goal-Dev-Spec cross-platform scripting capabilities, detailing how to create and manage scripts that work across different operating systems.

## Overview

The Goal-Dev-Spec cross-platform scripting system provides tools for creating and managing scripts that work seamlessly across different operating systems. This includes support for both bash/shell scripts on Unix-like systems and PowerShell scripts on Windows, with automatic selection based on the user's platform.

## Scripting System Components

### Script Directory Structure

Scripts are organized in the following structure:

```
scripts/
├── bash/
│   ├── setup/
│   ├── deployment/
│   ├── maintenance/
│   └── utilities/
├── powershell/
│   ├── setup/
│   ├── deployment/
│   ├── maintenance/
│   └── utilities/
└── cross-platform/
    ├── build.sh
    ├── test.ps1
    └── deploy.sh
```

### Script CLI Commands

The scripting system is accessible through CLI commands:

- `goal script create`: Create a new cross-platform script
- `goal script run`: Run a specific script
- `goal script list`: List available scripts
- `goal script validate`: Validate script compatibility

## CLI Commands

### `goal script create` - Create Script

Create a new cross-platform script.

#### Usage

```bash
goal script create SCRIPT_NAME
```

#### Options

- `--type`: Script type (setup, deployment, maintenance, utility)
- `--platform`: Platform support (auto, bash, powershell, both)
- `--description`: Script description

#### Features

- Template-based script creation
- Cross-platform compatibility checks
- Automatic platform detection
- Script validation

#### Examples

```bash
# Create a new utility script with automatic platform detection
goal script create backup-script --type utility --description "Database backup utility"

# Create a setup script for both platforms
goal script create setup-environment --type setup --platform both

# Create a deployment script for bash only
goal script create deploy-bash --type deployment --platform bash
```

#### Interactive Process

```
Creating new script: backup-script
Script Type: utility
Platform Support: auto (detect based on system)

Available Templates:
↑ Basic Utility Script
  Environment Setup Script
  Deployment Script
  Maintenance Script
  Custom Template
↓ Cancel

Template Selection: Basic Utility Script
Script Description: Database backup utility

Generated Scripts:
- scripts/bash/utilities/backup-script.sh
- scripts/powershell/utilities/backup-script.ps1

Scripts created successfully!
```

### `goal script run` - Run Script

Run a specific script.

#### Usage

```bash
goal script run SCRIPT_NAME [ARGS...]
```

#### Features

- Automatic platform detection
- Parameter passing to scripts
- Execution logging
- Error handling and reporting

#### Examples

```bash
# Run a script
goal script run backup-script

# Run a script with parameters
goal script run backup-script -- --database prod --compress

# Run a script in a specific directory
goal script run deploy-script -- --environment staging
```

#### Output

```
Running script: backup-script
Platform detected: Windows
Executing: scripts/powershell/utilities/backup-script.ps1

Script Output:
Starting database backup...
Connecting to database: myapp_prod
Backup directory: C:\backups\2025-01-15
Creating backup file: backup_20250115_1430.sql
Backup completed successfully (Size: 2.4GB, Duration: 4m 32s)

Execution completed successfully!
Exit code: 0
```

### `goal script list` - List Scripts

List available scripts with their information.

#### Usage

```bash
goal script list [OPTIONS]
```

#### Options

- `--type`: Filter by script type
- `--platform`: Show scripts for specific platform
- `--detailed`: Show detailed script information

#### Features

- Script discovery and listing
- Type-based filtering
- Platform compatibility information
- Script metadata display

#### Examples

```bash
# List all scripts
goal script list

# List setup scripts only
goal script list --type setup

# List with detailed information
goal script list --detailed
```

#### Output

```
Available Scripts:
Type: Setup
- setup-environment (bash, powershell) - Environment setup script
- install-dependencies (bash, powershell) - Install project dependencies

Type: Deployment
- deploy-staging (bash, powershell) - Deploy to staging environment
- deploy-production (bash) - Deploy to production environment

Type: Maintenance
- backup-script (bash, powershell) - Database backup utility
- cleanup-logs (powershell) - Clean up old log files

Type: Utilities
- run-tests (bash, powershell) - Run project tests
- generate-report (bash) - Generate project report
```

### `goal script validate` - Validate Script

Validate script compatibility and correctness.

#### Usage

```bash
goal script validate [SCRIPT_PATH]
```

#### Features

- Syntax validation
- Cross-platform compatibility checking
- Dependency validation
- Security scanning

#### Examples

```bash
# Validate all scripts
goal script validate

# Validate a specific script
goal script validate scripts/bash/setup/setup-environment.sh
```

#### Output

```
Script Validation Results:
Validating: scripts/powershell/utilities/backup-script.ps1

Results:
✓ Syntax validation passed
✓ Cross-platform compatibility: Compatible with PowerShell 5.1+
✓ Dependency check: All required modules available
✓ Security scan: No security issues detected
✓ Best practices: Following PowerShell best practices

Overall Status: PASS
```

## Cross-Platform Script Templates

### Bash Script Template

```bash
#!/bin/bash
# 
# Script: ${SCRIPT_NAME}
# Description: ${DESCRIPTION}
# Platform: Unix/Linux/macOS
# Generated by Goal-Dev-Spec
#

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Script configuration
SCRIPT_NAME="${SCRIPT_NAME}"
SCRIPT_VERSION="1.0.0"
DESCRIPTION="${DESCRIPTION}"

# Default values
DEFAULT_PARAM1="default_value"
DEFAULT_PARAM2=0

# Parse command line arguments
PARAM1="$DEFAULT_PARAM1"
PARAM2="$DEFAULT_PARAM2"
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --param1)
            PARAM1="$2"
            shift 2
            ;;
        --param2)
            PARAM2="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo "  --param1 VALUE   Set parameter 1 (default: $DEFAULT_PARAM1)"
            echo "  --param2 VALUE   Set parameter 2 (default: $DEFAULT_PARAM2)"
            echo "  --verbose, -v    Enable verbose output"
            echo "  --help, -h       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [[ "$level" == "ERROR" ]]; then
        echo "[ERROR]   [$timestamp] $message" >&2
    elif [[ "$level" == "WARN" ]]; then
        echo "[WARN]    [$timestamp] $message" >&2
    elif [[ "$VERBOSE" == true ]]; then
        echo "[INFO]    [$timestamp] $message"
    fi
}

# Main execution
main() {
    log "INFO" "Starting $SCRIPT_NAME v$SCRIPT_VERSION"
    log "INFO" "Parameter 1: $PARAM1"
    log "INFO" "Parameter 2: $PARAM2"
    
    # Add your script logic here
    log "INFO" "Script completed successfully"
}

# Execute main function
main "$@"
```

### PowerShell Script Template

```powershell
<#
.SYNOPSIS
    ${SCRIPT_NAME}
.DESCRIPTION
    ${DESCRIPTION}
.PARAMETER Param1
    First parameter description
.PARAMETER Param2
    Second parameter description
.PARAMETER Verbose
    Enable verbose output
.EXAMPLE
    .\${SCRIPT_NAME}.ps1 -Param1 "value" -Param2 42
.NOTES
    Version: 1.0.0
    Platform: Windows PowerShell 5.1+, PowerShell Core
    Generated by Goal-Dev-Spec
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$Param1 = "default_value",
    
    [Parameter(Mandatory=$false)]
    [int]$Param2 = 0,
    
    [Parameter(Mandatory=$false)]
    [switch]$Verbose = $false
)

# Script configuration
$SCRIPT_NAME = "${SCRIPT_NAME}"
$SCRIPT_VERSION = "1.0.0"
$DESCRIPTION = "${DESCRIPTION}"

# Logging function
function Write-Log {
    param(
        [ValidateSet("INFO", "WARN", "ERROR")]
        [string]$Level,
        [string]$Message
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$Level] [$timestamp] $Message"
    
    switch ($Level) {
        "ERROR" { Write-Error $logEntry }
        "WARN"  { Write-Warning $logEntry }
        "INFO"  { 
            if ($Verbose) {
                Write-Host $logEntry
            }
        }
    }
}

# Main execution
try {
    Write-Log "INFO" "Starting $SCRIPT_NAME v$SCRIPT_VERSION"
    Write-Log "INFO" "Parameter 1: $Param1"
    Write-Log "INFO" "Parameter 2: $Param2"
    
    # Add your script logic here
    Write-Log "INFO" "Script completed successfully"
}
catch {
    Write-Log "ERROR" "Script failed: $($_.Exception.Message)"
    exit 1
}
```

## Script Management

### Script Configuration

Script configurations are stored in `scripts/config.yaml`:

```yaml
# scripts/config.yaml
scripts:
  default_platform: "auto"  # auto, bash, powershell
  execution_timeout: 300    # seconds
  backup_enabled: true
  logging_level: "info"     # debug, info, warn, error
  
  paths:
    bash: "scripts/bash"
    powershell: "scripts/powershell"
    cross_platform: "scripts/cross-platform"
    
  categories:
    - name: "setup"
      description: "Environment setup scripts"
      path: "setup"
      
    - name: "deployment"
      description: "Deployment scripts"
      path: "deployment"
      
    - name: "maintenance"
      description: "System maintenance scripts"
      path: "maintenance"
      
    - name: "utilities"
      description: "Utility scripts"
      path: "utilities"
```

### Script Metadata

Each script includes metadata for proper management:

```bash
# At the top of bash scripts
# @goal-script
# @name backup-script
# @version 1.0.0
# @description Database backup utility
# @platform bash,powershell
# @category utilities
# @author Kaiden
```

```powershell
# At the top of PowerShell scripts
<# @goal-script
@name backup-script
@version 1.0.0
@description Database backup utility
@platform powershell
@category utilities
@author Kaiden
#>
```

## Platform Detection and Execution

### Automatic Platform Detection

The system automatically detects the appropriate platform:

```python
import os
import platform

def detect_platform():
    system = platform.system().lower()
    if system == "windows":
        return "powershell"
    elif system in ["linux", "darwin"]:  # Darwin is macOS
        return "bash"
    else:
        return "bash"  # Default to bash for other Unix-like systems

def get_script_path(script_name, platform=None):
    if not platform:
        platform = detect_platform()
    
    if platform == "powershell":
        return f"scripts/powershell/utilities/{script_name}.ps1"
    elif platform == "bash":
        return f"scripts/bash/utilities/{script_name}.sh"
    else:
        raise ValueError(f"Unsupported platform: {platform}")
```

### Cross-Platform Execution Wrapper

```python
import subprocess
import platform
from pathlib import Path

def execute_script(script_name, args=None):
    if platform.system() == "Windows":
        # Use PowerShell
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", 
               "-File", f"scripts/powershell/utilities/{script_name}.ps1"]
    else:
        # Use bash
        cmd = ["bash", f"scripts/bash/utilities/{script_name}.sh"]
    
    if args:
        cmd.extend(args)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return {
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }
```

## Common Script Patterns

### Environment Setup Scripts

Environment setup scripts should:

1. Check for existing installations
2. Install missing dependencies
3. Configure environment variables
4. Validate the setup

```bash
#!/bin/bash
# Environment setup script

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 before continuing."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not available. Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Install project dependencies
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo "Dependencies installed successfully."
else
    echo "requirements.txt not found. Skipping dependency installation."
fi
```

### Deployment Scripts

Deployment scripts should:

1. Validate deployment environment
2. Backup current deployment (if applicable)
3. Deploy new version
4. Run post-deployment checks
5. Handle rollback if needed

```bash
#!/bin/bash
# Deployment script

set -euo pipefail

ENVIRONMENT=${1:-staging}
APP_NAME="myapp"

echo "Deploying $APP_NAME to $ENVIRONMENT environment..."

# Pre-deployment checks
if [ "$ENVIRONMENT" = "production" ]; then
    read -p "Deploying to production. Are you sure? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 0
    fi
fi

# Backup current version
if [ -d "/opt/$APP_NAME/backup" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    cp -r "/opt/$APP_NAME/current" "/opt/$APP_NAME/backup/backup_$TIMESTAMP"
    echo "Current version backed up."
fi

# Deploy new version
echo "Deploying new version..."
# Add deployment logic here

echo "Deployment completed successfully."
```

### Maintenance Scripts

Maintenance scripts should:

1. Perform routine tasks
2. Clean up temporary files
3. Generate reports
4. Check system health

```bash
#!/bin/bash
# Maintenance script - System cleanup

echo "Starting system maintenance..."

# Clean temporary files
echo "Cleaning temporary files..."
find /tmp -type f -atime +7 -delete

# Clean log files older than 30 days
echo "Cleaning old log files..."
find /var/log -name "*.log" -mtime +30 -delete

# Check disk usage
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//g')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Warning: Disk usage is ${DISK_USAGE}%"
else
    echo "Disk usage is OK: ${DISK_USAGE}%"
fi

echo "Maintenance completed."
```

## Security Considerations

### Script Security Best Practices

1. **Input Validation**: Always validate inputs to scripts
2. **Principle of Least Privilege**: Run scripts with minimal required permissions
3. **Secure Storage**: Store sensitive data securely, not in scripts
4. **Code Signing**: Sign scripts for integrity verification
5. **Audit Logging**: Log script execution for security monitoring

### Security Validation

The system includes security validation:

```bash
# Security checks for bash scripts
security_check() {
    # Check for hardcoded credentials
    if grep -E "(password|secret|key|token).*=" "$1" > /dev/null; then
        echo "Security warning: Hardcoded credentials detected in $1"
        return 1
    fi
    
    # Check for insecure file permissions
    if [ "$(stat -c %a "$1")" -ge 777 ]; then
        echo "Security warning: Insecure file permissions for $1"
        return 1
    fi
    
    return 0
}
```

## Troubleshooting

### Common Issues

1. **Script Execution Policy**: On Windows, PowerShell execution policy may prevent running scripts
2. **File Permissions**: On Unix systems, scripts may need execute permissions
3. **Path Issues**: Scripts may fail due to incorrect paths
4. **Platform Differences**: Behavior may differ between platforms

### Platform-Specific Solutions

#### Windows (PowerShell)

```powershell
# If getting execution policy errors:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run with bypass:
powershell -ExecutionPolicy Bypass -File script.ps1
```

#### Unix/Linux/macOS (Bash)

```bash
# If getting permission errors:
chmod +x script.sh

# Or run with explicit interpreter:
bash script.sh
```

### Getting Help

For additional help with cross-platform scripting features:
- Use `goal script --help` for command-specific help
- Check the scripting documentation in the `docs/` directory
- Review script templates in the `scripts/` directory
- Examine existing scripts for examples

## Best Practices

### 1. Consistent Script Organization

- Use consistent naming conventions
- Organize scripts by function or lifecycle stage
- Include metadata in all scripts
- Maintain version control for scripts

### 2. Robust Error Handling

- Implement proper error handling
- Use exit codes appropriately
- Provide meaningful error messages
- Include logging for debugging

### 3. Cross-Platform Compatibility

- Test scripts on all target platforms
- Use portable commands where possible
- Handle platform differences gracefully
- Document platform-specific behavior

### 4. Security Consciousness

- Never hardcode credentials
- Validate all inputs
- Use secure methods for sensitive operations
- Regularly review scripts for security issues

### 5. Maintainability

- Include usage documentation in scripts
- Use meaningful variable names
- Include comments for complex logic
- Make scripts configurable where appropriate

This cross-platform scripting system ensures that automation tasks can be performed consistently across different operating systems while maintaining security, reliability, and maintainability.
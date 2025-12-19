---
layout: default
title: Troubleshooting Guide
---

# Troubleshooting Guide

Solutions for common Goal Kit issues.

## Installation Issues

### "command not found: goalkeeper"

**Symptoms**: Command works after installation, then stops working

**Causes**:
- Path not updated
- Installation location changed
- Environment variables reset

**Solutions**:

```bash
# Check installation location
which goalkeeper        # macOS/Linux
where.exe goalkeeper   # Windows

# Reinstall with uv
uv tool install --force --from . goalkeeper

# Or add to PATH manually
export PATH="$HOME/.local/bin:$PATH"  # Add to ~/.bashrc or ~/.zshrc
```

### Python Version Mismatch

**Symptoms**: "Python 3.8+ required" error

**Solution**:
```bash
# Check Python version
python --version

# If using Python < 3.8, upgrade
brew install python@3.11      # macOS
sudo apt install python3.11   # Linux
# Windows: Download from python.org

# Verify installation
python3.11 --version

# Install with specific Python
python3.11 -m pip install -e .
```

### Module Import Errors

**Symptoms**: "ModuleNotFoundError: No module named 'goalkeeper_cli'"

**Solutions**:

```bash
# Verify you're in the goal-kit directory
cd /path/to/goal-kit
ls -la | grep pyproject.toml

# Reinstall in development mode
pip install -e .

# Or use uv
uv tool install --from . goalkeeper
```

## Project Issues

### "Not in a goal kit project"

**Symptoms**: Error when running goalkeeper commands in project

**Causes**:
- Missing `.goalkit/` directory
- Not in project root
- Incomplete initialization

**Solutions**:

```bash
# Check project structure
ls -la | grep goalkit

# If missing, initialize project
goalkeeper init

# Or manually create structure
mkdir -p .goalkit/goals
touch .goalkit/vision.md
git init
```

### Goal Directory Not Found

**Symptoms**: "Goal directory does not exist" when running `/goalkit.strategies`

**Causes**:
- Goal not created yet
- Wrong path provided
- Goal directory deleted

**Solutions**:

```bash
# List existing goals
ls -la .goalkit/goals/

# Create goal first
/goalkit.goal [goal description]

# Verify goal was created
ls -la .goalkit/goals/001-*/
```

### Missing goal.md File

**Symptoms**: Goal directory exists but goal.md is missing

**Solutions**:

```bash
# Create goal.md manually
cat > .goalkit/goals/001-your-goal/goal.md << 'EOF'
# Goal Statement: [Your Goal]

## 🎯 Goal Definition
[Content...]

## 📊 Success Metrics
[Metrics...]
EOF

# Or recreate using /goalkit.goal command
```

## Git Issues

### "Not in a git repository"

**Symptoms**: "Not in a git repository" error when creating goals

**Causes**:
- Project not initialized as git repository
- Git not installed
- Wrong working directory

**Solutions**:

```bash
# Initialize git repository
git init

# Verify git is installed
git --version

# Add and commit initial structure
git add .goalkit/
git commit -m "Initialize goal kit"

# Verify git status
git status
```

### Branch Creation Issues

**Symptoms**: Error when creating goal branches

**Solutions**:

```bash
# Check git status
git status

# Commit any pending changes
git add .
git commit -m "Work in progress"

# Verify branch creation works
git checkout -b test-branch
git checkout main  # or master

# Delete test branch
git branch -d test-branch
```

### "Permission denied" when Creating Branch

**Symptoms**: Git permission errors when creating branches

**Solutions**:

```bash
# Check git configuration
git config --list

# Set git user (if not configured)
git config user.name "Your Name"
git config user.email "your@email.com"

# Try creating branch again
/goalkit.goal [goal]
```

## Script Execution Issues

### Scripts Not Found

**Symptoms**: "Command not found" for shell scripts

**Causes**:
- Scripts not executable
- Wrong path
- Script not created

**Solutions**:

```bash
# Make scripts executable
chmod +x scripts/bash/*.sh
chmod +x scripts/powershell/*.ps1

# Verify scripts exist
ls -la scripts/bash/
ls -la scripts/powershell/

# Run from project root
cd /path/to/goal-kit
bash scripts/bash/create-new-goal.sh "My Goal"
```

### "Permission Denied" on Linux/macOS

**Symptoms**: "Permission denied" when running bash scripts

**Solutions**:

```bash
# Make script executable
chmod +x scripts/bash/create-new-goal.sh

# Or run with bash explicitly
bash scripts/bash/create-new-goal.sh "My Goal"

# Check permissions
ls -la scripts/bash/create-new-goal.sh
```

### PowerShell Execution Policy

**Symptoms**: "running scripts is disabled" error on Windows

**Solutions**:

```powershell
# Check current policy
Get-ExecutionPolicy

# Allow script execution temporarily
powershell -ExecutionPolicy Bypass -File scripts/powershell/create-new-goal.ps1 "My Goal"

# Or set policy permanently (admin required)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### PowerShell Script Fails After Init

**Symptoms**: Scripts fail with "template not found", "path not found", or execution errors after project initialization

**Common Causes**:

1. **Template Path Issues**: Scripts use incorrect path resolution for templates
2. **Working Directory**: Scripts called from agents may run from different directories
3. **Missing Error Handling**: Scripts don't gracefully handle missing dependencies

**Solutions**:

```powershell
# Test script execution from project root
cd /path/to/your/project
powershell -ExecutionPolicy Bypass -File ".goalkit\scripts\powershell\create-new-goal.ps1" -Json "test-goal"

# Verify template directory exists
Test-Path ".goalkit\templates"

# Check all required tools
powershell -ExecutionPolicy Bypass -Command ". .goalkit\scripts\powershell\common.ps1; Test-Prerequisites"

# Manual context update
powershell -ExecutionPolicy Bypass -File ".goalkit\scripts\powershell\update-agent-context.ps1" -AgentType claude
```

**Debug Steps**:

1. Ensure you're in the project root directory
2. Verify `.goalkit\templates` directory contains template files
3. Check git repository status (`git status`)
4. Test with `-DryRun` parameter first when available
5. Use `-Json` parameter for better error output from agents

## Agent Context Issues

### Agent Context Not Updating

**Symptoms**: AI agent doesn't have current goal information

**Causes**:
- Context file not found
- Script not running
- File permissions

**Solutions**:

```bash
# Manual update on Linux/macOS
bash scripts/bash/common.sh
source scripts/bash/common.sh
update_agent_context

# Manual update on Windows
. scripts/powershell/common.ps1
Update-AgentContext

# Manual update on Linux/macOS
bash scripts/bash/common.sh
source scripts/bash/common.sh
update_agent_context

# Verify context file exists
cat CLAUDE.md        # For Claude
cat CURSOR.md        # For Cursor
cat GEMINI.md        # For Gemini
```

### Bash Script Fails After Init

**Symptoms**: Scripts fail with "template not found", "command not found", or execution errors after project initialization

**Common Causes**:

1. **Template Path Issues**: Scripts use incorrect path resolution for templates
2. **Missing Dependencies**: Required tools not installed or not in PATH
3. **Permission Issues**: Scripts don't have execute permissions

**Solutions**:

```bash
# Make scripts executable
chmod +x scripts/bash/*.sh

# Test script execution from project root
cd /path/to/your/project
bash scripts/bash/create-new-goal.sh --json "test-goal"

# Verify template directory exists
test -d ".goalkit/templates"

# Check all required tools
bash scripts/bash/common.sh -c "source scripts/bash/common.sh; test_prerequisites"

# Manual context update
bash scripts/bash/update-agent-context.sh claude
```

**Debug Steps**:

1. Ensure you're in the project root directory
2. Verify `.goalkit/templates` directory contains template files
3. Check script permissions: `ls -la scripts/bash/`
4. Test with `--dry-run` parameter first when available
5. Use `--json` parameter for better error output from agents
6. Check for missing tools: `git --version`, `which uv`

### Context File Not Found

**Symptoms**: "No agent context file found to update"

**Causes**:
- Agent context file not created
- Wrong filename
- File deleted

**Solutions**:

```bash
# Create context file for Claude
touch CLAUDE.md

# Or for other agents
touch CURSOR.md
touch GEMINI.md
touch WINDSURF.md

# Verify files exist
ls -la *.md
```

## AI Agent Issues

### Agent Doesn't Recognize Commands

**Symptoms**: Commands like `/goalkit.goal` not recognized

**Causes**:
- Outdated agent system
- Agent configuration incomplete
- Command templates not found

**Solutions**:

1. **Update agent context file**:
   ```bash
   bash scripts/bash/common.sh && update_agent_context
   ```

2. **Try command with full path**:
   ```
   Use scripts/bash/create-new-goal.sh directly instead of /goalkit.goal
   ```

3. **Check agent has latest templates**:
   - Tell agent to: "Load the latest Goal Kit templates"
   - Have agent check `.goalkit/` directory exists

### Agent Can't Create Files

**Symptoms**: Agent creates goal definitions but files don't save

**Causes**:
- Permission issues
- Wrong working directory
- File system full

**Solutions**:

```bash
# Check permissions on .goalkit
ls -la .goalkit/
chmod 755 .goalkit/
chmod 755 .goalkit/goals/

# Verify disk space
df -h

# Check working directory
pwd

# Try creating file manually
mkdir -p .goalkit/goals/001-test
touch .goalkit/goals/001-test/goal.md
```

## Command Issues

### "/goalkit.goal" Stuck or Slow

**Symptoms**: Command takes too long or freezes

**Causes**:
- Large goal directories
- Git operations slow
- Network timeout (if remote repo)

**Solutions**:

```bash
# Check git status (might be slow with many files)
git status --short

# Try creating goal directly with script
bash scripts/bash/create-new-goal.sh "My Goal" --json

# Test git performance
time git log

# Force stop current operation
Ctrl+C (or Cmd+C on macOS)
```

### JSON Output Malformed

**Symptoms**: Agent can't parse goal creation JSON output

**Causes**:
- Script error
- Encoding issue
- Special characters in goal name

**Solutions**:

```bash
# Test script directly
bash scripts/bash/create-new-goal.sh "Simple Goal" --json

# Check JSON validity
bash scripts/bash/create-new-goal.sh "My Goal" --json | python3 -m json.tool

# Use simpler goal name (alphanumeric only)
bash scripts/bash/create-new-goal.sh "Goal One" --json

# On Windows, ensure UTF-8 encoding
chcp 65001  # Set to UTF-8
```

## File System Issues

### "File Already Exists"

**Symptoms**: Cannot create goal, strategies, or milestones (file exists)

**Causes**:
- File already created
- Permission issues
- Partial previous attempt

**Solutions**:

```bash
# Check what exists
ls -la .goalkit/goals/001-goal-name/

# Use --force flag to overwrite
bash scripts/bash/create-new-goal.sh "Goal" --force

# Or delete and recreate
rm -rf .goalkit/goals/001-old-goal/
bash scripts/bash/create-new-goal.sh "Goal"
```

### Special Characters in Goal Names

**Symptoms**: Invalid directory names or JSON parsing errors

**Causes**:
- Special characters in goal description
- Unicode characters
- Spaces or symbols

**Solutions**:

```bash
# Use simple names (alphanumeric and hyphens)
/goalkit.goal Add user authentication

# Avoid these characters
# ✗ "Goal: Why?" 
# ✗ "Feature @2024"
# ✗ "API/REST"

# Better:
# ✓ "Add user authentication"
# ✓ "Feature for 2024"
# ✓ "API REST implementation"
```

## Performance Issues

### "Out of Memory" Errors

**Symptoms**: System runs out of memory with large projects

**Causes**:
- Too many goals/files
- Large context files
- Memory leak in process

**Solutions**:

```bash
# Check memory usage
free -h              # Linux
vm_stat              # macOS
Get-Process | Select | Sort -Descending  # Windows

# Archive old goals
mkdir archive
mv .goalkit/goals/old-goals/ archive/

# Reduce agent context file size
# (Keep only recent goals)
```

### Slow Goal Creation

**Symptoms**: Goal creation takes longer than expected

**Causes**:
- Large .git directory
- Slow disk I/O
- Many files in goals directory

**Solutions**:

```bash
# Check git repo size
du -sh .git

# Clean git history (if safe to do)
git gc

# Use --json flag (faster)
bash scripts/bash/create-new-goal.sh "Goal" --json

# Check disk speed
dd if=/dev/zero of=test.img bs=1M count=100
```

## Network Issues

### GitHub Token/Authentication Issues

**Symptoms**: "Authentication failed" when pulling templates

**Causes**:
- GitHub token expired
- Not authenticated
- Network connectivity

**Solutions**:

```bash
# Check network connectivity
ping github.com

# Verify git authentication
git config --list | grep credential

# Set GitHub token (if needed)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Use HTTPS instead of SSH
git remote set-url origin https://github.com/Nom-nom-hub/goal-kit.git
```

## Still Having Issues?

### Before Reporting

1. **Check Goal Kit version**:
   ```bash
   goalkeeper --version
   ```

2. **Verify Python version**:
   ```bash
   python --version
   ```

3. **Check git status**:
   ```bash
   git --version
   git status
   ```

4. **Review error messages carefully** - first line usually tells you the issue

5. **Try on a fresh project**:
   ```bash
   mkdir test-project
   cd test-project
   goalkeeper init
   ```

### Getting Help

- **GitHub Issues**: [Report on GitHub](https://github.com/Nom-nom-hub/goal-kit/issues)
- **Discussions**: [Ask questions](https://github.com/Nom-nom-hub/goal-kit/discussions)
- **Documentation**: [Read docs](./README.md)

When reporting issues, include:
- Goal Kit version: `goalkeeper --version`
- Python version: `python --version`
- OS: macOS/Linux/Windows
- Error message (full text)
- Steps to reproduce
- Project structure (output of `ls -la .goalkit/`)

---

**Found a solution?** Consider updating this guide to help others!

---
layout: default
title: Installation Guide
---

# Installation Guide

Goal Kit installation instructions for different platforms and use cases.

## System Requirements

- **Python**: 3.8 or higher
- **Git**: Required for goal branch management
- **OS**: Linux, macOS, or Windows

## Installation Methods

### Method 1: Using uv (Recommended)

The fastest and most reliable method using the `uv` package manager.

#### Install uv First

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Install Goal Kit

From GitHub (recommended):
```bash
uv tool install --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper-cli
```

Or from local repository:
```bash
cd /path/to/goal-kit
uv tool install --from . goalkeeper-cli
```

After installation, verify:
```bash
goalkeeper --version
```

### Method 2: Global Installation via pip

Install Goal Kit globally on your system.

From GitHub:
```bash
pip install --upgrade pip
pip install git+https://github.com/Nom-nom-hub/goal-kit.git
```

Or from local repository:
```bash
cd /path/to/goal-kit
pip install --upgrade pip
pip install -e .
```

Verify installation:
```bash
goalkeeper --version
```

### Method 3: One-Time Usage (No Installation)

Run Goal Kit without installing to your system.

```bash
uv run --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper-cli init my-project
uv run --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper-cli check
```

This is useful for:
- Testing Goal Kit before installing
- CI/CD pipelines
- Containerized environments

### Method 4: Local Development Installation

Install from source for contributing or customizing.

```bash
git clone https://github.com/Nom-nom-hub/goal-kit.git
cd goal-kit
pip install -e ".[dev]"
```

## Post-Installation Setup

### 1. Verify Installation

```bash
# Check version
goalkeeper --version

# Check available agents
goalkeeper check
```

### 2. Initialize Your First Project

```bash
# Create and initialize a new project
goalkeeper init my-first-project
cd my-first-project

# Check project setup
ls -la
```

This creates:
- `.goalkit/` - Configuration directory
- `.goalkit/vision.md` - Project vision template
- `.goalkit/goals/` - Goals directory
- Agent context files (CLAUDE.md, etc.)

### 3. Configure Your Agent

Goal Kit detects and configures for these agents:
- Claude (Claude Code)
- GitHub Copilot
- Google Gemini
- Cursor
- Qwen Code
- Windsurf
- Kilo Code
- Amazon Q
- And others

Configuration happens automatically on `goalkeeper init`.

To manually configure for a specific agent:

```bash
# Initialize with specific agent
goalkeeper init my-project --agent claude
```

## Platform-Specific Instructions

### macOS

#### Using Homebrew (Optional)

```bash
# Install uv via Homebrew
brew install uv

# Then install Goal Kit
uv tool install --from . goalkeeper-cli
```

#### Using Native Python

```bash
# Install Python 3.8+
brew install python@3.11

# Install Goal Kit
pip install -e .
```

#### Verify Git

Git comes pre-installed on macOS. Verify:
```bash
git --version
```

### Linux (Ubuntu/Debian)

#### Using Package Manager

```bash
# Update package manager
sudo apt update
sudo apt install python3.11 python3.11-venv git

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Goal Kit
uv tool install --from . goalkeeper-cli
```

#### Verify Installation

```bash
python3 --version
git --version
goalkeeper --version
```

### Windows

#### Prerequisites

1. **Install Python**:
   - Download from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation
   - Choose Python 3.8 or higher

2. **Install Git**:
   - Download from [git-scm.com](https://git-scm.com/download/win)
   - Use default installation settings

3. **Install uv**:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

#### Install Goal Kit

```powershell
uv tool install --from . goalkeeper-cli
```

#### Verify Installation

Open PowerShell and run:
```powershell
goalkeeper --version
```

### Docker

Run Goal Kit in a Docker container:

```dockerfile
FROM python:3.11-slim

# Install git and required tools
RUN apt-get update && apt-get install -y git

# Install Goal Kit
RUN pip install git+https://github.com/Nom-nom-hub/goal-kit.git

WORKDIR /workspace
```

Build and run:
```bash
docker build -t goal-kit .
docker run -it -v $(pwd):/workspace goal-kit goalkeeper init my-project
```

## Troubleshooting Installation

### "command not found: goalkeeper"

**Solution 1**: Verify installation path
```bash
# Find where goalkeeper was installed
which goalkeeper  # macOS/Linux
where goalkeeper  # Windows

# Add to PATH if needed
export PATH="$HOME/.cargo/bin:$PATH"  # Add to ~/.bashrc or ~/.zshrc
```

**Solution 2**: Use full path
```bash
~/.cargo/bin/goalkeeper --version
```

**Solution 3**: Reinstall with uv
```bash
uv tool install --force --from . goalkeeper-cli
```

### "No module named 'goalkeeper_cli'"

**Solution**: Ensure you're in the Goal Kit project directory
```bash
cd /path/to/goal-kit
pip install -e .
```

### Python Version Issues

**Solution**: Install Python 3.8 or higher
```bash
# Check current version
python --version

# Install specific version (macOS with Homebrew)
brew install python@3.11
python3.11 -m pip install -e .

# On Windows, use Python installer or:
choco install python --version=3.11.0
```

### Git Not Found

**Solution**: Install git
```bash
# macOS
brew install git

# Linux
sudo apt install git

# Windows
# Download from: https://git-scm.com/download/win
```

Verify:
```bash
git --version
```

### Permission Denied on Unix

**Solution**: Use user installation
```bash
# Install for current user only
pip install --user -e .

# Or use uv (recommended)
uv tool install --from . goalkeeper-cli
```

### Virtual Environment Issues

**Solution**: Use uv which handles environments automatically
```bash
uv tool install --from . goalkeeper-cli
```

Or manually with venv:
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install
pip install -e .
```

## Verification Checklist

After installation, verify everything works:

- [ ] `goalkeeper --version` shows a version number
- [ ] `goalkeeper check` lists detected agents
- [ ] `goalkeeper init test-project` creates a project
- [ ] `.goalkit/` directory exists in the project
- [ ] `git init` works in the project directory

## Updating Goal Kit

### Using uv

```bash
uv tool upgrade goalkeeper
```

### Using pip

```bash
pip install --upgrade goal-kit
```

### From Source

```bash
cd /path/to/goal-kit
git pull
pip install --upgrade -e .
```

## Uninstalling Goal Kit

### Using uv

```bash
uv tool uninstall goalkeeper
```

### Using pip

```bash
pip uninstall goal-kit
```

## Next Steps

After successful installation:

1. **Quick Start**: Read [Quick Start Guide](./quickstart.md)
2. **First Project**: Run `goalkeeper init my-project`
3. **Learn Methodology**: Read [Goal-Driven Development](./goal-driven.md)
4. **See Examples**: Check [Practical Examples](./examples.md)

## Getting Help

- **Issues**: Check [GitHub Issues](https://github.com/Nom-nom-hub/goal-kit/issues)
- **Troubleshooting**: Read [Troubleshooting Guide](./troubleshooting.md)
- **Documentation**: Visit [Goal Kit Docs](./README.md)

---

**Ready to install?** Start with [Method 1 (uv)](#method-1-using-uv-recommended) for the smoothest experience.

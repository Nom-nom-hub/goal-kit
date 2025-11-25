# Contributing to Goal Kit

Thank you for your interest in contributing to Goal Kit! We welcome contributions from everyone. Here are some guidelines to help you get started.

## How to Contribute

### 1. Fork and Clone
```bash
git clone https://github.com/nom-nom-hub/goal-kit.git
cd goal-kit
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/amazing-feature
# or
git checkout -b fix/bug-fix
```

### 3. Make Your Changes
- Follow the existing code style and structure
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Test Your Changes
```bash
# Test bash scripts
bash scripts/bash/create-new-goal.sh --json "test-goal"

# Test PowerShell scripts (on Windows)
& ".\scripts\powershell\create-new-goal.ps1" -Json "test-goal"

# Check formatting
# (Add formatting checks as needed)
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "Add amazing feature"
```

### 6. Push and Create Pull Request
```bash
git push origin feature/amazing-feature
```

Then open a Pull Request on GitHub.

## Contribution Guidelines

### Code Style
- Use consistent indentation (2 spaces for YAML, 4 spaces for Python)
- Follow existing naming conventions
- Keep lines under 100 characters when possible
- Add comments for complex logic

### Templates
- Ensure templates are AI-friendly with clear structure
- Use consistent placeholder formatting: `[VARIABLE_NAME]`
- Include validation criteria where appropriate
- Test templates with multiple AI agents

### Documentation
- Update README.md for user-facing changes
- Update docs/ for documentation changes
- Add examples for new features
- Update CHANGELOG.md for notable changes

### Scripts
- Use `#!/usr/bin/env python3` for Python scripts
- Include error handling with `set -euo pipefail`
- Add usage comments and examples

## Types of Contributions

### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include steps to reproduce
- Add environment information
- Provide expected vs actual behavior

### ✨ Feature Requests
- Discuss in GitHub Discussions first
- Provide use cases and motivation
- Consider implementation complexity
- Suggest multiple approaches if applicable

### 📝 Documentation Improvements
- Fix typos and unclear sections
- Add missing examples
- Improve step-by-step instructions
- Update outdated information

### 🧪 Template Enhancements
- Improve AI compatibility
- Add validation criteria
- Enhance user guidance
- Fix formatting issues

## Development Workflow

### Setting Up Development Environment
```bash
# Clone repository
git clone https://github.com/nom-nom-hub/goal-kit.git

# Make scripts executable
# No need for executable permissions for Python scripts

# Install dependencies (if any)
pip install mkdocs mkdocs-material  # For documentation
```

### Testing Changes
```bash
# Test bash script functionality
bash scripts/bash/create-new-goal.sh --json "test-goal"

# Test PowerShell script functionality (on Windows)
& ".\scripts\powershell\create-new-goal.ps1" -Json "test-goal"

# Build documentation
mkdocs build
```

### Creating New Templates
1. Study existing templates in `templates/`
2. Follow the naming convention: `[type]-template.md`
3. Include clear sections and placeholders
4. Add to navigation in `docs/mkdocs.yml`
5. Test with multiple AI agents

## Community Guidelines

### Be Respectful
- Use inclusive language
- Respect different opinions
- Focus on constructive feedback
- Help other contributors

### Communication
- Use GitHub issues for bugs and features
- Use Discussions for questions and ideas
- Be clear and concise in descriptions
- Provide context for your contributions

### Quality Standards
- Ensure changes don't break existing functionality
- Add tests for new features
- Update documentation for user-facing changes
- Follow security best practices

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- GitHub release notes
- Documentation credits
- Project README

## Questions?

- Check existing GitHub issues and discussions
- Review the documentation in `docs/`
- Ask questions in GitHub Discussions
- Reach out to maintainers for complex issues

---

*Thank you for contributing to Goal Kit! Your help makes goal-driven development better for everyone.*
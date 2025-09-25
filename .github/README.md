# 🚀 GitHub Actions for Goal-Kit

This directory contains automated workflows for the Goal-Kit project, providing comprehensive CI/CD, testing, and release management capabilities.

## 📋 Available Workflows

### 🔄 Automated Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| **🚀 Release** | `release` published or manual | Creates release packages and publishes to GitHub Releases |
| **🔍 CI** | Push/PR to main/develop | Validates templates, scripts, and overall quality |
| **🔄 Dependencies** | Weekly schedule or manual | Updates dependencies and checks for security issues |
| **📚 Documentation** | Push to main (docs changes) | Deploys documentation to GitHub Pages |
| **🧪 Testing** | Push/PR to main/develop | Comprehensive automated testing suite |

---

## 🚀 Release Workflow

### Automatic Release Process

When you publish a release on GitHub:

1. **Version Detection** - Automatically detects version from tag or input
2. **Template Packaging** - Packages templates for all AI agents and platforms
3. **Checksum Generation** - Creates SHA256 checksums for security
4. **Release Upload** - Uploads all packages to GitHub Releases
5. **Release Notes** - Generates comprehensive release documentation

### Manual Release

You can also trigger releases manually:

1. Go to **Actions** tab in GitHub
2. Select **🚀 Release Goal-Kit Templates** workflow
3. Click **Run workflow**
4. Specify version and release type
5. Click **Run workflow**

### Release Package Format

Following Spec-Kit conventions:

```
goal-kit-template-[AGENT]-[PLATFORM]-v[VERSION].zip
```

**Examples:**
- `goal-kit-template-cursor-sh-v0.0.1.zip` (Cursor + Bash)
- `goal-kit-template-claude-ps-v0.0.1.zip` (Claude + PowerShell)
- `goal-kit-template-qwen-sh-v0.0.1.zip` (Qwen + Bash)

### Supported AI Agents
- ✅ **Cursor** - Full support
- ✅ **Claude** - Full support
- ✅ **Qwen** - Full support
- ✅ **Roo** - Full support
- ✅ **Copilot** - Full support
- ✅ **Auggie** - Full support
- ✅ **Gemini** - Full support
- ✅ **Windsurf** - Full support
- ✅ **Codex** - Full support
- ✅ **Kilocode** - Full support
- ✅ **Opencode** - Full support

---

## 🔍 Continuous Integration

### Automated Validation

The CI workflow runs on every push and PR:

#### ✅ Template Validation
- JSON structure validation
- Required fields verification
- Milestone structure checking
- Template integrity tests

#### ✅ Script Validation
- Bash script syntax checking
- PowerShell script validation
- Cross-platform compatibility
- Dependency analysis

#### ✅ AI Integration Testing
- TOML command file validation
- AI-friendly template structure
- Agent-specific configuration
- Integration compatibility

#### 🔒 Security Scanning
- Secret detection
- Dependency vulnerability checks
- Package integrity validation
- Access permission verification

### Quality Gates

All CI checks must pass before:
- ✅ Merging to main branch
- ✅ Creating releases
- ✅ Deploying documentation

---

## 🔄 Dependency Management

### Weekly Updates

Automated dependency checking every Monday:

- **GitHub Actions** - Latest versions
- **System Dependencies** - Security updates
- **Node.js/Python** - Version compatibility
- **Build Tools** - Latest releases

### Manual Updates

Force update dependencies anytime:

```bash
# Trigger manual dependency update
# Go to Actions → 🔄 Update Dependencies → Run workflow
```

### What Gets Updated

- **GitHub Actions** - All workflow actions
- **Base Images** - Security patches
- **System Packages** - Critical updates
- **Documentation** - Dependency references

---

## 📚 Documentation Deployment

### Automatic Deployment

Documentation deploys automatically when:

- Changes pushed to `main` branch
- Documentation files modified
- Workflow triggered manually

### Deployed Content

- **📖 Main Documentation** - Project overview and guides
- **🤖 AI Agent Guides** - Agent-specific integration docs
- **🛠️ Development Docs** - Contributing and development guides
- **📋 Reference Material** - API and template references

### Access Documentation

After deployment, access at:
```
https://[username].github.io/goal-dev-spec/
```

---

## 🧪 Comprehensive Testing

### Test Categories

#### 📝 Template Testing
- JSON schema validation
- Required field verification
- Milestone structure testing
- Cross-template compatibility

#### 🔧 Script Testing
- Syntax validation
- Execution testing
- Error handling
- Cross-platform compatibility

#### 📦 Packaging Testing
- Package creation validation
- Integrity checking
- Checksum verification
- Multi-agent support

#### 🔗 Integration Testing
- End-to-end workflow testing
- Component interaction validation
- Configuration compatibility
- Performance benchmarking

### Test Execution

Tests run automatically on:
- ✅ **Push to main/develop** - Full test suite
- ✅ **Pull requests** - Comprehensive validation
- ✅ **Manual trigger** - On-demand testing

---

## 📊 Workflow Status and Monitoring

### GitHub Actions Dashboard

Monitor all workflows at:
```
https://github.com/[username]/goal-dev-spec/actions
```

### Status Badges

Add these badges to your README:

```markdown
<!-- Release Status -->
![Release](https://github.com/[username]/goal-dev-spec/actions/workflows/release.yml/badge.svg)

<!-- CI Status -->
![CI](https://github.com/[username]/goal-dev-spec/actions/workflows/ci.yml/badge.svg)

<!-- Tests -->
![Tests](https://github.com/[username]/goal-dev-spec/actions/workflows/test.yml/badge.svg)

<!-- Documentation -->
![Docs](https://github.com/[username]/goal-dev-spec/actions/workflows/docs.yml/badge.svg)
```

### Workflow Notifications

Configure notifications for:
- ✅ **Release Success/Failure**
- ✅ **CI Failures**
- ✅ **Security Alerts**
- ✅ **Dependency Updates**

---

## 🛠️ Workflow Configuration

### Environment Variables

Key environment variables used:

```yaml
env:
  NODE_VERSION: '20'           # Node.js version for tooling
  PYTHON_VERSION: '3.11'       # Python version for scripts
  AI_AGENTS: '["cursor", "claude", "qwen", "roo", ...]'  # Supported agents
  PLATFORMS: '["sh", "ps"]'    # Supported platforms
```

### Secrets Required

Add these secrets to repository settings:

- `GITHUB_TOKEN` - Automatically provided by GitHub Actions
- `SNYK_TOKEN` - Optional: For security scanning (if using Snyk)

### Customizing Workflows

To modify workflows:

1. **Edit workflow files** in `.github/workflows/`
2. **Test changes** using manual workflow dispatch
3. **Validate** with CI before merging
4. **Monitor** execution after deployment

---

## 🚨 Troubleshooting

### Common Issues

#### Release Failures
- **Check version format** - Must be semantic (e.g., `0.0.1`)
- **Verify permissions** - Ensure GITHUB_TOKEN has write access
- **Check file sizes** - Large packages may timeout

#### CI Failures
- **Validate templates** - Run `jq` validation locally
- **Check scripts** - Test with `bash -n` and PowerShell syntax check
- **Review dependencies** - Ensure all tools are installed

#### Documentation Issues
- **Check file paths** - Verify all referenced files exist
- **Validate Markdown** - Run markdownlint locally
- **Test deployment** - Use manual workflow dispatch

### Getting Help

1. **Check workflow logs** - Detailed execution logs available
2. **Review error messages** - Specific error details provided
3. **Test locally** - Run scripts and validations locally first
4. **Community support** - Ask in GitHub Discussions

---

## 📈 Performance and Optimization

### Workflow Efficiency

- **Parallel Execution** - Jobs run in parallel when possible
- **Caching** - Dependencies cached between runs
- **Incremental Builds** - Only changed components rebuilt
- **Smart Triggers** - Workflows only run when needed

### Monitoring and Analytics

- **Execution Time** - Track workflow performance
- **Success Rates** - Monitor reliability metrics
- **Resource Usage** - Optimize for cost and speed
- **Error Tracking** - Identify and fix recurring issues

---

## 🎯 Best Practices

### Workflow Management

- **Keep workflows simple** - Each workflow has a single responsibility
- **Use descriptive names** - Clear naming for easy identification
- **Document changes** - Add comments for complex logic
- **Test thoroughly** - Validate workflows before production

### Release Management

- **Semantic versioning** - Follow semantic version conventions
- **Clear release notes** - Comprehensive documentation for each release
- **Tag consistently** - Use proper Git tags for releases
- **Test releases** - Verify packages before publishing

### Security

- **Minimal permissions** - Use least-privileged access
- **Secret management** - Never commit secrets
- **Dependency scanning** - Regular security checks
- **Access control** - Protect sensitive workflows

---

## 📋 Quick Reference

### Manual Workflow Triggers

```bash
# Trigger release workflow
gh workflow run "🚀 Release Goal-Kit Templates" --field version=0.0.2 --field release_type=minor

# Trigger dependency update
gh workflow run "🔄 Update Dependencies" --field force_update=true

# Trigger documentation deployment
gh workflow run "📚 Deploy Documentation"

# Trigger testing
gh workflow run "🧪 Automated Testing"
```

### Workflow Status Commands

```bash
# List all workflows
gh workflow list

# View workflow runs
gh run list

# View specific run logs
gh run view [RUN_ID]

# Watch workflow execution
gh run watch [RUN_ID]
```

---

## 🎉 Ready for Production!

Your Goal-Kit project now has **enterprise-grade GitHub Actions** providing:

- ✅ **Automated releases** with multi-agent support
- ✅ **Comprehensive testing** and validation
- ✅ **Dependency management** and security scanning
- ✅ **Documentation deployment** to GitHub Pages
- ✅ **Professional monitoring** and reporting

The workflows are **production-ready** and follow **industry best practices** for CI/CD, security, and automation. 🚀
# Release Strategy

Goal Kit now uses a controlled, intentional release process to avoid excessive versioning.

## How Releases Work

### Version Source of Truth
- **pyproject.toml** is the single source of truth for version numbers
- Version must be explicitly updated in `pyproject.toml` to trigger a release
- Follows semantic versioning (MAJOR.MINOR.PATCH)

### Release Triggers
Releases only occur when:
1. `pyproject.toml` is updated with a new version, **OR**
2. The `workflow_dispatch` trigger is manually invoked

Regular code changes (templates, scripts, documentation) do NOT automatically create releases.

### Release Workflow Steps

1. **Version Check**: `get-next-version.sh` reads version from `pyproject.toml`
2. **Comparison**: Compares with latest Git tag
3. **Skip If Match**: If already released, workflow exits cleanly
4. **Package Creation**: Creates release packages for all agent types
5. **Release Notes**: Generates notes from git history
6. **GitHub Release**: Creates release with assets

## How to Create a Release

### Automatic Release (Recommended)
1. Update `pyproject.toml` version field:
   ```toml
   [project]
   version = "0.0.100"
   ```

2. Update `CHANGELOG.md` with changes for this version
   ```markdown
   ## [0.0.100] - 2025-11-26
   
   ### Changed
   - Description of changes
   ```

3. Commit both files:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Release 0.0.100"
   git push
   ```

4. GitHub Actions automatically:
   - Detects version change
   - Creates release with all packages
   - Tags the commit

### Manual Release
If needed, you can trigger a release manually via GitHub Actions:
1. Go to Actions → Create Release workflow
2. Click "Run workflow"
3. Select branch and confirm

## Benefits of This Approach

- ✅ **Intentional Versioning**: Only meaningful versions are released
- ✅ **Clear History**: All releases documented in CHANGELOG
- ✅ **Reduced Clutter**: No more 100+ patch versions
- ✅ **Single Source of Truth**: pyproject.toml controls versioning
- ✅ **CI/CD Safe**: Protects against accidental releases
- ✅ **Semantic Versioning**: Follows industry standards

## Previous Issue

Previously, releases were created on every push that modified:
- src/
- scripts/
- templates/
- README.md
- etc.

This resulted in 117 releases (0.0.117) in a short time. The new approach ensures releases are intentional and meaningful.

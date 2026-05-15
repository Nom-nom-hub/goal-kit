# Release Notes: Make Goal-Kit More Effective and Smarter

## Overview
This release improves goal-kit by removing AI drift code, enhancing the analyzer with actionable insights, and simplifying the template system.

## Changes

### Core Improvements

1. **Removed AI Drift Code**
   - Deleted `src/goalkeeper_cli/ai/providers.py` (not used, called external APIs)
   - Deleted `src/goalkeeper_cli/templates.py` (dead code)
   - Goal-kit now works purely via markdown files and scripts

2. **Enhanced Analyzer** (`src/goalkeeper_cli/analyzer.py`)
   - Added `get_insights()` method with contextual recommendations
   - Added `get_insights_from_result()` static method for efficiency
   - Fixed summary generation for all health score levels
   - Fixed phase consistency ("execute" vs "execution")

3. **Updated Status Command** (`src/goalkeeper_cli/commands/status.py`)
   - Shows actionable insights, concerns, and strengths
   - JSON output includes insights section
   - Uses existing analysis result (no redundant processing)

### Template Simplification

4. **Deleted 23 Unused Templates**
   - Kept only 6 core templates:
     - `vision-template.md`
     - `goal-template.md`
     - `lite-goal-template.md`
     - `strategies-template.md`
     - `milestones-template.md`
     - `execution-template.md`

5. **Improved Template Structure**
   - Added Summary section (2-3 sentences) to vision & goal
   - Added Key Stakeholders section
   - Added Risks section with parseable format
   - Added Progress field to goal header
   - Synced `.goalkit/templates/` with `templates/`

### Bug Fixes

6. **Fixed Scripts**
   - `create-vision.sh` - Now creates vision file in JSON mode
   - `update-agent-context.sh` - Fixed `write_host` error

7. **Removed Test Directory**
   - Deleted `goalkit-test` submodule from repo

## Testing
- Syntax verification passed for all modified Python files
- All changes pushed to branch `001-make-goal-kit-more-affective-and-smarter`

## Migration
- No breaking changes
- Templates are backward compatible
- Existing goals remain valid
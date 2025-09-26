---
description: Track and update progress on goals and milestones
scripts:
  sh: update-progress.sh
  ps: update-progress.ps1
---

## Progress Tracking Command

Update and track progress on goals and milestones with the following capabilities:

**Command**: `{SCRIPT} {ARGS}`

### Parameters
- `target_id`: ID of the goal or milestone to update
- `status`: Current status (not_started, in_progress, completed, blocked)
- `progress`: Percentage progress (0-100)
- `notes`: Additional notes about progress or blockers
- `next_steps`: Planned next steps

### Usage
This command will update the progress tracking information for the specified goal or milestone. It allows for:

1. Status updates with timestamps
2. Progress percentage tracking
3. Notes about challenges or achievements
4. Planning for next steps

### Output
The progress tracking file will be updated with the new information and validated against the original goal/milestone specifications.

**Agent Type**: __AGENT__
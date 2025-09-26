---
description: Achieve and close out a goal or milestone
scripts:
  sh: generate-report.sh --achieve
  ps: generate-report.ps1 -Achieve
---

## Achievement Command

Mark a goal or milestone as achieved and generate completion reports:

**Command**: `{SCRIPT} {ARGS}`

### Parameters
- `target_id`: ID of the goal or milestone to mark as achieved
- `results`: Summary of results achieved
- `metrics`: Quantifiable metrics that show success
- `lessons_learned`: Key lessons learned during the process
- `next_actions`: Recommended next actions based on results

### Usage
This command will mark the specified goal or milestone as completed and generate:

1. Achievement documentation
2. Success metrics and analysis
3. Lessons learned and recommendations
4. Next steps and follow-up items

### Output
The goal/milestone status will be updated to 'completed' and comprehensive achievement documentation will be generated, including reports for stakeholders.

**Agent Type**: __AGENT__
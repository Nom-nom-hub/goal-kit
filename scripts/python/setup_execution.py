#!/usr/bin/env python3
"""Create an execution plan for a goal with learning and adaptation framework."""

import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    """Create execution plan file."""
    if len(sys.argv) < 2:
        print("Usage: setup_execution.py <goal_dir> [--json]")
        return 1

    goal_dir = Path(sys.argv[1])
    json_mode = "--json" in sys.argv

    if not goal_dir.exists():
        if json_mode:
            print(json.dumps({"error": f"Goal directory not found: {goal_dir}"}))
        else:
            print(f"Error: Goal directory not found: {goal_dir}")
        return 1

    # Check for required files
    goal_file = goal_dir / "goal.md"
    strategies_file = goal_dir / "strategies.md"
    milestones_file = goal_dir / "milestones.md"

    if not all([goal_file.exists(), strategies_file.exists(), milestones_file.exists()]):
        if json_mode:
            print(json.dumps({
                "error": "Missing required files. Ensure goal.md, strategies.md, and milestones.md exist."
            }))
        else:
            print("Error: Missing required files (goal.md, strategies.md, milestones.md)")
        return 1

    execution_file = goal_dir / "execution.md"

    # Create execution template
    execution_content = f"""# Execution Plan

**Date Created**: {datetime.now().strftime('%Y-%m-%d')}

## Quick Start

1. **Review** the goal, strategies, and milestones
2. **Choose** the current milestone to execute
3. **Establish** measurement framework
4. **Run** learning loops daily and weekly
5. **Document** all insights and learnings

## Current Milestone Focus

[Specify which milestone you're implementing]

## Execution Strategy

### Hypothesis Testing
[What assumptions are you validating?]

### Success Criteria
[How will you know the milestone is achieved?]

### Alternative Approaches
[What backup plans do you have?]

## Measurement Framework

### Key Metrics
- [Metric 1]
- [Metric 2]
- [Metric 3]

### Measurement Methods
- [How to collect data]

### Success Thresholds
- [When milestone is considered successful]

## Learning Loop Process

### Daily Learning Loop
1. **Build**: Implement planned work
2. **Measure**: Collect data on progress
3. **Learn**: Capture insights and blockers
4. **Document**: Record learnings

### Weekly Learning Loop
1. **Review**: Assess progress toward milestone
2. **Analyze**: Identify patterns in results
3. **Adapt**: Adjust approach based on learnings
4. **Plan**: Set focus for next week

### Progress Assessment
[Regular evaluation schedule and methods]

### Insight Documentation
[How and where to capture learnings]

## Adaptation Framework

### Progress Indicators
- [Signs that current approach is working]
- [Evidence of success]

### Warning Indicators
- [Early signs of problems]
- [When to consider pivoting]

### Pivot Decision Process
[Framework for deciding to change approach]

### Strategy Switch Options
[Alternative approaches if primary fails]

## Daily Tracking

### Template for Daily Log
```
**Date**: [YYYY-MM-DD]
**Milestone Focus**: [Current milestone]
**Hypothesis Tested**: [What assumption did we test?]
**Results**: [What happened?]
**Insight**: [What did we learn?]
**Blocker**: [Any obstacles?]
**Next Day Focus**: [What's next?]
```

## Risk Management

### Current Risks
- [Risk 1 - Mitigation strategy]
- [Risk 2 - Mitigation strategy]

### Risk Monitoring Process
[How to identify and track new risks]

### Risk Response Plan
[How to respond if risks materialize]

## Success Validation

### Milestone Completion Checklist
- [ ] Success criteria met
- [ ] Learning objectives accomplished
- [ ] Value delivered
- [ ] No critical issues

### Goal Progress
- [ ] Measurable advancement toward goal
- [ ] Learnings integrated into next phase
- [ ] Strategy validated or adjusted
- [ ] Stakeholders aligned

## Notes

[Additional thoughts and context]
"""

    execution_file.write_text(execution_content)

    if json_mode:
        result = {
            "status": "success",
            "message": "Execution plan created",
            "file": str(execution_file),
            "goal_dir": str(goal_dir),
        }
        print(json.dumps(result))
    else:
        print(f"Execution plan created: {execution_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

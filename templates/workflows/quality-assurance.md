---
description: Define quality standards and assurance processes for goal deliverables. Establishes testing strategy, acceptance criteria, and quality metrics.
handoffs:
  - label: Risk Register
    agent: goalkit.risk-register
    prompt: Add quality-related risks to the goal risk register
    send: false
scripts:
  sh: scripts/bash/setup-quality-assurance.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-quality-assurance.ps1 -Json "{GOAL_ID}"
---

## User Input

- **Goal or Deliverable**: Which goal or product needs quality standards?
- **Quality Scope**: Functionality, Performance, Reliability, Usability, Accessibility, Security?
- **Testing Responsibility**: Dedicated QA, shared, or engineering-owned?

## Execution Flow

1. **Quality Dimensions** (15 min)
   - Define 3-4 critical quality attributes with concrete targets (e.g., "99.9% uptime", "<200ms load time")

2. **Testing Strategy** (30 min)
   - Set coverage targets: 80% unit, 40% integration, 10% E2E
   - Plan test types: Functional, Performance, Reliability, Accessibility, Security
   - Define execution cadence (per commit, daily, release gate)

3. **Acceptance Gates** (20 min)
   - Code Quality: Lint/type checks passing, coverage ≥ target
   - Functional: All critical tests passing, 0 blockers
   - Performance: Benchmarks met, <10% regression
   - Security: 0 unaddressed Critical/High findings

4. **Quality Metrics** (15 min)
   - Track: test coverage, pass rate, bug density, critical bug count, release success rate
   - Set up weekly dashboard with escalation path for declining metrics

## Validation Gate

- [ ] Critical quality dimensions identified (3-4)
- [ ] Testing strategy covers all required levels
- [ ] Release gates defined with clear approval authority
- [ ] Quality metrics and monitoring documented

## Guidelines

- **Test Pyramid**: 70% unit, 20% integration, 10% E2E
- **Acceptance Criteria Format**: Given [context], When [action], Then [result]
- **Bug Severity**: Critical (fix now), High (this cycle), Medium (2 sprints), Low (backlog)

## Output

- **Output File**: `.goalkit/goals/[GOAL_ID]/quality-assurance.md`
- **Dashboard**: Coverage, test pass rate, bug trends, release gate status

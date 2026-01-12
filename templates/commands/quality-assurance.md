---
description: Define comprehensive quality standards and assurance processes for goal deliverables. Establishes testing strategy, acceptance criteria, and quality metrics.
handoffs:
  - label: Risk Register
    agent: goalkit.risk-register
    prompt: Add quality-related risks to the goal risk register
    send: false
  - label: Detailed Retrospective
    agent: goalkit.detailed-retrospective
    prompt: Review quality outcomes and metrics post-completion
    send: false
scripts:
  sh: scripts/bash/setup-quality-assurance.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-quality-assurance.ps1 -Json "{GOAL_ID}"
---

## User Input

- **Goal or Deliverable**: Which goal or product are you defining quality standards for?
- **Quality Scope**: Functionality, performance, reliability, usability, accessibility, or all?
- **Testing Responsibility**: Dedicated QA team, shared responsibility, or engineering-owned?

## Outline

### Execution Flow

1. **Quality Dimensions Definition** (30 min)
   - Define quality attributes: Functionality (does it work?), Performance (is it fast?), Reliability (does it stay up?), Usability (is it easy to use?), Accessibility (can everyone use it?), Security (is it protected?)
   - For each dimension, set 2-3 concrete quality goals (e.g., "99.9% uptime", "< 200ms load time", "WCAG 2.1 AA compliance")
   - Extract critical quality dimensions (3-4 max) for this goal

2. **Testing Strategy** (45 min)
   - Define test coverage target (e.g., 80% unit, 40% integration, 10% E2E)
   - Plan test types:
     - **Functional Testing**: Feature acceptance, regression, critical path
     - **Performance Testing**: Load testing, stress testing, profiling
     - **Reliability Testing**: Fault tolerance, failover, recovery
     - **Accessibility Testing**: Screen reader compatibility, keyboard navigation, contrast ratios
     - **Security Testing**: Input validation, authentication/authorization, data exposure
   - Assign testing owners (engineering, QA, product)
   - Define test execution cadence (per commit, daily, weekly, release gate)

3. **Acceptance Criteria & Gates** (30 min)
   - Document acceptance criteria for each feature/component (clear, testable, measurable)
   - Define release gates:
     - **Code Quality**: Lint passing, type checking clean, test coverage ≥ target
     - **Functional Quality**: All critical tests passing, no unresolved blockers
     - **Performance Quality**: Benchmarks met, no regressions ≥ 10%
     - **Accessibility Quality**: Accessibility audit passing, no critical violations
     - **Security Quality**: No Critical/High security findings unaddressed
   - Document who approves gate (QA lead, product, engineering lead)

4. **Quality Metrics & Monitoring** (30 min)
   - Define key metrics:
     - Test coverage (unit, integration, E2E)
     - Test pass rate (weekly target, trend)
     - Bug density (bugs per 1000 LOC, trend)
     - Critical/High bug count (weekly)
     - Release/deployment frequency and success rate
     - User-reported issues (post-release)
   - Set up weekly quality dashboard (coverage, pass rates, bug trends)
   - Establish escalation path (declining coverage, spiking bugs)

5. **Quality Documentation** (15 min)
   - Create test inventory (what tests exist, who maintains them, coverage)
   - Document known limitations and accepted quality trade-offs
   - Create quality runbook (how to run tests, interpret results, escalate issues)
   - Establish quality review cadence (weekly quality sync, 30 min)

### Validation Gate: Quality Assurance Check

**Agent Must Confirm**:
- [ ] Critical quality dimensions identified (3-4 max)
- [ ] Testing strategy covers unit, integration, E2E, and critical non-functional areas
- [ ] Acceptance criteria are testable and measurable
- [ ] Release gates defined with clear approval authority
- [ ] Quality metrics and monitoring approach documented
- [ ] Testing responsibility clearly assigned

**If Not Met**: Expand testing strategy or clarify acceptance criteria.

### General Guidelines

- **Coverage Targets**: Aim for 80% unit, 40% integration, 10% E2E minimum; adjust based on risk
- **Test Pyramid**: 70% unit, 20% integration, 10% E2E to optimize for speed and maintainability
- **Acceptance Criteria Format**: Given [context], When [action], Then [observable result]
- **Bug Severity Scale**:
  - **Critical**: System down, data loss, security breach (fix immediately)
  - **High**: Feature broken, workaround difficult (fix this cycle)
  - **Medium**: Feature partially working or degraded (fix within 2 sprints)
  - **Low**: Minor cosmetic or performance issue (backlog)
- **Release Gate Thresholds**:
  - Code quality: 100% passing (no critical lint/type errors)
  - Functional: 95%+ test pass rate, 0 critical bugs
  - Performance: ≤ 10% regression, targets met
  - Accessibility: 100% critical issues resolved
  - Security: 0 unaddressed Critical/High findings
- **Monitoring Cadence**: Daily test results, weekly quality dashboard, escalate trends

### Reporting

- **Output File**: `.goalkit/goals/[GOAL_ID]/quality-assurance.md`
- **Quality Dashboard**: Coverage, test pass rate, bug trends, release gate status
- **Test Inventory**: All tests, owners, coverage areas (updated weekly)
- **Release Readiness**: Gate checklist with pass/fail for each dimension

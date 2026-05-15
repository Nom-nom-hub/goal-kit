---
description: Document compliance requirements and validation across legal, regulatory, and organizational standards.
handoffs:
  - label: Security Review
    agent: goalkit.security-review
    prompt: Review security compliance aspects
    send: false
  - label: Risk Register
    agent: goalkit.risk-register
    prompt: Track compliance-related risks
    send: false
scripts:
  sh: scripts/bash/setup-compliance-checklist.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-compliance-checklist.ps1 -Json "{GOAL_ID}"
---

## User Input

- **Goal or Deliverable**: Which goal deliverable needs compliance review?
- **Compliance Scope**: Legal, Regulatory (GDPR, HIPAA, SOC2, PCI-DSS), or Internal policies?
- **Key Stakeholders**: Legal, compliance team, regulatory body, audit partner?

## Execution Flow

1. **Requirements Identification** (30 min)
   - Identify applicable frameworks (GDPR, HIPAA, SOC2, PCI-DSS, WCAG, OWASP)
   - List 3-5 specific requirements per framework, prioritize by risk (Critical→Low)

2. **Gap Analysis** (30 min)
   - Assess each requirement: Met / Partially Met / At Risk / Not Met
   - Calculate compliance coverage % (Met ÷ Total)
   - Flag Critical/High gaps for immediate remediation

3. **Remediation Planning** (20 min)
   - For each gap: define control, owner, timeline, validation method
   - Timeline: Critical→immediate, High→1 week, Medium→1 month

4. **Evidence & Monitoring** (15 min)
   - Document evidence for each requirement (logs, tests, policies)
   - Set up automated checks and review cadence (monthly critical, quarterly full)

## Validation Gate

- [ ] All applicable compliance frameworks identified
- [ ] Gap analysis complete for each requirement
- [ ] Critical/High gaps have owners and timelines
- [ ] Compliance monitoring and review cadence defined

## Output

- **Output File**: `.goalkit/goals/[GOAL_ID]/compliance-checklist.md`
- **Dashboard**: Coverage % by framework, gap count by status, remediation progress

---
description: Conduct a security assessment of goal deliverables. Identifies vulnerabilities, validates compliance, and documents remediation plans.
handoffs:
  - label: Risk Register
    agent: goalkit.risk-register
    prompt: Add security-specific risks to the goal risk register
    send: false
  - label: Compliance Checklist
    agent: goalkit.compliance-checklist
    prompt: Validate compliance and regulatory alignment
    send: false
scripts:
  sh: scripts/bash/setup-security-review.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-security-review.ps1 -Json "{GOAL_ID}"
---

## User Input

- **Goal or System**: Which goal, service, or system needs security review?
- **Scope**: Full system, specific components, APIs, data handling, auth?
- **Compliance Requirements**: GDPR, HIPAA, SOC2, PCI-DSS, or internal standards?

## Execution Flow

1. **Threat Assessment** (30 min)
   - Identify threat vectors: external attacks, insider threats, data breaches, DoS, supply chain
   - Document data flows (input, storage, transmission) and external dependencies
   - Extract 6-8 top threat scenarios

2. **Vulnerability Scan** (20 min)
   - Check code for OWASP Top 10 (injection, broken auth, XSS, CSRF)
   - Scan dependencies for CVEs (npm audit, pip safety)
   - Validate secrets management and auth/authorization implementation

3. **Compliance Validation** (20 min)
   - Verify encryption at rest and in transit (TLS 1.2+, AES-256)
   - Review audit logging, data retention, and deletion policies

4. **Findings Triage** (20 min)
   - Classify: Critical (fix now), High (1 week), Medium (2-4 weeks), Low (track)
   - For Critical/High: define remediation, owner, target date, acceptance criteria

## Validation Gate

- [ ] All threat vectors identified for system scope
- [ ] Dependency scan complete (no unaddressed Critical/High CVEs)
- [ ] Critical findings have owners and target dates
- [ ] Authentication/authorization mechanisms reviewed

## Guidelines

- **Threat Categories**: Auth, Authorization, Data Protection, API, Infrastructure, Supply Chain
- **Compliance Checklist**: Encryption, MFA, least privilege, audit logging, PII handling
- **Remediation**: Critical→immediate, High→1 week, Medium→2-4 weeks, Low→track

## Output

- **Output File**: `.goalkit/goals/[GOAL_ID]/security-review.md`
- **Findings Dashboard**: Count by severity with remediation status

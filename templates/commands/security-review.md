---
description: Conduct a comprehensive security assessment of goal deliverables. Identifies vulnerabilities, validates compliance with security standards, and documents remediation plans.
handoffs:
  - label: Risk Register
    agent: goalkit.risk-register
    prompt: Add security-specific risks to the goal risk register
    send: false
  - label: Compliance Checklist
    agent: goalkit.compliance-checklist
    prompt: Validate compliance and regulatory/standards alignment
    send: false
scripts:
  sh: scripts/bash/setup-security-review.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-security-review.ps1 -Json "{GOAL_ID}"
---

## User Input

- **Goal or Deliverable**: Which goal, service, or system needs security review?
- **Scope**: Full system, specific components, APIs, data handling, infrastructure, or authentication?
- **Compliance Requirements**: GDPR, HIPAA, SOC2, PCI-DSS, or internal security standards?

## Outline

### Execution Flow

1. **Security Threat Assessment** (45 min)
   - Identify threat vectors (external attacks, insider threats, data breaches, DoS, supply chain)
   - Document data flows (input/output, storage, transmission)
   - List external dependencies and third-party integrations
   - Extract top 6-8 threat scenarios per component

2. **Vulnerability Scan** (30 min)
   - Review code for OWASP Top 10 issues (injection, broken auth, XSS, CSRF, etc.)
   - Check dependencies for known CVEs using security scanner (npm audit, pip safety, etc.)
   - Validate secrets management (no hardcoded keys, proper rotation)
   - Assess authentication/authorization implementation

3. **Compliance Validation** (30 min)
   - Check alignment with compliance requirements (if applicable)
   - Validate encryption at rest and in transit (TLS, key management)
   - Document data retention and deletion policies
   - Review audit logging and monitoring capabilities

4. **Security Findings Triage** (30 min)
   - Classify findings: Critical (immediate risk), High (remediate within 1 week), Medium (2-4 weeks), Low (track)
   - For Critical/High findings:
     - Define remediation approach
     - Assign owner
     - Set target date
     - Document acceptance criteria
   - For Medium/Low findings, add to tracking list with owner

5. **Documentation & Handoff** (15 min)
   - Create security review report with findings, risk scores, and remediation plans
   - Communicate Critical/High findings to security lead and team
   - Schedule weekly security triage (15 min) for remediation tracking

### Validation Gate: Security Review Check

**Agent Must Confirm**:
- [ ] All threat vectors identified for system scope
- [ ] Dependency scan complete (no unaddressed CVEs in Critical/High)
- [ ] Critical findings have remediation owners and target dates
- [ ] Compliance requirements validated (if applicable)
- [ ] All data flows documented with security controls
- [ ] Authentication/authorization mechanisms reviewed

**If Not Met**: Expand threat assessment or escalate to security team.

### General Guidelines

- **Severity Scale**:
  - **Critical**: Immediate exploitation risk, data exposure, service compromise (fix now)
  - **High**: Likely to be exploited, significant impact (fix within 1 week)
  - **Medium**: Possible exploitation, moderate impact (fix within 2-4 weeks)
  - **Low**: Unlikely to be exploited, minimal impact (track and remediate opportunistically)

- **Threat Categories**: Authentication, Authorization, Data Protection, API Security, Infrastructure, Supply Chain, Logging/Monitoring

- **Compliance Checklist Items**:
  - Encryption (TLS 1.2+, AES-256 for data at rest)
  - Authentication (multi-factor, strong password policy)
  - Access Control (principle of least privilege, role-based)
  - Audit Logging (all access logged, retention policy)
  - Data Privacy (PII handling, data classification)
  - Incident Response (detection, response, notification process)

- **Remediation Timeline**: Critical/High findings start immediately; Medium within 2 weeks; Low tracked for future sprints

- **Monitoring**: Weekly security triage for remediation progress; escalate blockers immediately

### Reporting

- **Output File**: `.goalkit/goals/[GOAL_ID]/security-review.md`
- **Findings Dashboard**: Count of Critical/High/Medium/Low with remediation status
- **Compliance Report**: Coverage status against requirements (if applicable)
- **Escalation Alert**: Any Critical findings to security lead and engineering leadership

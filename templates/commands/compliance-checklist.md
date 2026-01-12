---
description: Document compliance requirements and validation across legal, regulatory, and organizational standards. Ensures goal deliverables meet all applicable compliance obligations.
handoffs:
  - label: Security Review
    agent: goalkit.security-review
    prompt: Review security compliance aspects
    send: false
  - label: Risk Register
    agent: goalkit.risk-register
    prompt: Track compliance-related risks
    send: false
  - label: Detailed Retrospective
    agent: goalkit.detailed-retrospective
    prompt: Review compliance outcomes post-completion
    send: false
scripts:
  sh: scripts/bash/setup-compliance-checklist.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-compliance-checklist.ps1 -Json "{GOAL_ID}"
---

## User Input

- **Goal or Deliverable**: Which goal deliverable needs compliance review?
- **Compliance Scope**: Legal (contracts, IP), Regulatory (GDPR, HIPAA, SOC2, etc.), Industry (PCI-DSS, etc.), Internal (policies, standards)?
- **Key Stakeholders**: Legal, compliance team, customer, regulatory body, or audit partner?

## Outline

### Execution Flow

1. **Compliance Requirements Identification** (45 min)
   - List all applicable compliance frameworks:
     - **Regulatory**: GDPR (EU data protection), HIPAA (healthcare), PCI-DSS (payment cards), CCPA (CA privacy), SOC2 (security/availability), ISO 27001 (information security)
     - **Industry Standards**: WCAG 2.1 (accessibility), OWASP (security), accessibility standards
     - **Contractual**: Customer data processing agreements (DPA), service level agreements (SLA), vendor contracts
     - **Internal Policies**: Data classification, security standards, code of conduct
   - For each framework, identify specific requirements (3-5 per framework, focus on material ones)
   - Prioritize by risk level (Critical, High, Medium, Low)

2. **Compliance Gap Analysis** (45 min)
   - For each requirement, assess current state: Met, Partially Met, At Risk, Not Met
   - Document evidence for Met/Partially Met (audit log, control, documentation)
   - For gaps, identify root cause (missing control, documentation, or process)
   - Calculate compliance coverage % (Met / Total)
   - Flag any Critical or High gaps for immediate remediation

3. **Remediation Planning** (30 min)
   - For each gap, define remediation approach:
     - **Control Implementation**: What new control is needed
     - **Owner**: Who implements
     - **Timeline**: When to complete (Critical: immediate, High: 1 week, Medium: 1 month)
     - **Validation Method**: How to verify compliance (audit, test, documentation review)
     - **Acceptance Criteria**: What "compliant" looks like
   - For Medium/Low gaps, add to backlog with priority

4. **Documentation & Evidence Collection** (30 min)
   - Create compliance evidence inventory:
     - Policies and procedures documentation
     - Control implementation details (code, configs, processes)
     - Audit logs, monitoring data, test results
     - Training records, certifications
   - Organize evidence by requirement (for audits)
   - Establish retention policy for evidence (typically 3-7 years)

5. **Compliance Monitoring & Review** (15 min)
   - Set up monitoring for continuous compliance:
     - Automated checks (code scanning for OWASP, access reviews for SOC2)
     - Manual reviews (quarterly compliance audit, annual framework renewal)
     - Change management: Every code/config change assessed for compliance impact
   - Schedule compliance review cadence (monthly for Critical/High gaps, quarterly for full framework review)
   - Define escalation path (audit findings, requirement changes)

### Validation Gate: Compliance Checklist Check

**Agent Must Confirm**:
- [ ] All applicable compliance frameworks identified and documented
- [ ] Gap analysis complete (current state assessed for each requirement)
- [ ] Critical/High gaps have owners and remediation timelines
- [ ] Evidence collection plan documented
- [ ] Compliance coverage % calculated and tracked
- [ ] Monitoring and review cadence defined

**If Not Met**: Expand requirements identification or clarify gap assessment.

### General Guidelines

- **Compliance Framework Reference**:
  - **GDPR**: Data protection, consent, data subject rights, DPA, breach notification, DPO
  - **HIPAA**: PHI encryption, access controls, audit logging, business associate agreements, breach notification
  - **SOC2**: Security (access, data protection), Availability (uptime), Processing integrity (completeness), Confidentiality (authorized access), Privacy (personal information handling)
  - **PCI-DSS**: Cardholder data security, vulnerability management, access control, regular monitoring, policies
  - **WCAG 2.1**: Perceivable, Operable, Understandable, Robust (AA or AAA level per requirement)

- **Compliance Risk Scoring**:
  - **Critical**: Regulatory violation, legal exposure, customer breach, financial penalty > $1M
  - **High**: Regulatory warning, customer contract breach, financial penalty $100K-$1M
  - **Medium**: Audit finding, internal policy violation, financial penalty $10K-$100K
  - **Low**: Best practice gap, documentation issue, financial penalty < $10K

- **Evidence Standards**: Written policies, system documentation, audit logs (timestamped, immutable), test results, training records, approvals

- **Audit Readiness**: Maintain compliance evidence in accessible format; conduct internal audit quarterly; respond to external audits (SOC2, customer, regulatory) within SLA

- **Change Management**: Every requirement change (new regulation, customer mandate) assessed for delivery impact; prioritize Critical/High changes immediately

### Reporting

- **Output File**: `.goalkit/goals/[GOAL_ID]/compliance-checklist.md`
- **Compliance Dashboard**: Coverage % by framework, gap count by status (Met/Partially Met/At Risk/Not Met), remediation progress
- **Gap Report**: All High/Critical gaps with owners, timelines, and remediation status
- **Evidence Inventory**: Complete list of supporting documentation and audit location
- **Audit Ready Report**: Summary for external auditors with evidence links

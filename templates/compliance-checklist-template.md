# Compliance Checklist

**Goal/Deliverable**: [Goal Name or Service Name]  
**Review Date**: [Date]  
**Compliance Officer**: [Name]  
**Compliance Frameworks**: [GDPR, HIPAA, SOC2, PCI-DSS, WCAG, Internal Policies, other]  

---

## Compliance Coverage Summary

| Framework | Requirements | Met | Partial | Gap | Coverage % |
|-----------|--------------|-----|---------|-----|-----------|
| GDPR | [#] | [#] | [#] | [#] | [%] |
| HIPAA | [#] | [#] | [#] | [#] | [%] |
| SOC2 | [#] | [#] | [#] | [#] | [%] |
| PCI-DSS | [#] | [#] | [#] | [#] | [%] |
| WCAG 2.1 | [#] | [#] | [#] | [#] | [%] |
| Internal Policies | [#] | [#] | [#] | [#] | [%] |
| **TOTAL** | [#] | [#] | [#] | [#] | [%] |

**Overall Compliance Status**: [✓ Fully Compliant / ⚠ Partial / ✗ At Risk]

---

## Critical & High Gaps (Action Required)

### [FRAMEWORK] Gap 1: [Requirement]

- **Status**: Gap (currently not met)
- **Risk Level**: Critical / High
- **Description**: [What's missing, why it's a gap]
- **Business Impact**: [Regulatory violation risk, customer contract breach, financial penalty, etc.]
- **Remediation Plan**:
  - [ ] Implement [specific control]
  - [ ] Document [policy/procedure]
  - [ ] Test/validate compliance
- **Owner**: [Name]
- **Target Date**: [Date]
- **Validation Method**: [How we verify compliance]
- **Acceptance Criteria**: [What "compliant" looks like]

### [FRAMEWORK] Gap 2: [Requirement]

[Same structure]

---

## GDPR Compliance (if applicable)

### Data Protection Requirements

| Requirement | Status | Evidence | Gap (if any) |
|-------------|--------|----------|------------|
| Lawful basis for processing defined | [Met/Partial/Gap] | [Policy ref or doc] | [Description] |
| Privacy policy published and accessible | [Met/Partial/Gap] | [URL/Doc] | [Description] |
| Explicit consent obtained (where required) | [Met/Partial/Gap] | [Process/Log] | [Description] |
| Data Processing Agreement (DPA) in place | [Met/Partial/Gap] | [DPA version] | [Description] |
| Data inventory documented | [Met/Partial/Gap] | [Data map location] | [Description] |
| Data retention policy defined | [Met/Partial/Gap] | [Policy doc] | [Description] |
| Data deletion capability implemented | [Met/Partial/Gap] | [Process/Code] | [Description] |

### Data Subject Rights

| Right | Status | Implementation | Gap (if any) |
|------|--------|-----------------|------------|
| Right to access | [Met/Partial/Gap] | [How we provide data export] | [Description] |
| Right to erasure ("Right to be Forgotten") | [Met/Partial/Gap] | [How we delete data] | [Description] |
| Right to rectification | [Met/Partial/Gap] | [How users update data] | [Description] |
| Right to data portability | [Met/Partial/Gap] | [Export format/process] | [Description] |
| Right to restrict processing | [Met/Partial/Gap] | [How we honor requests] | [Description] |

### Security & Governance

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| Encryption at rest (AES-256) | [Met/Partial/Gap] | [Config/Code] | [Description] |
| Encryption in transit (TLS 1.2+) | [Met/Partial/Gap] | [Config/Cert] | [Description] |
| Access control (principle of least privilege) | [Met/Partial/Gap] | [IAM config] | [Description] |
| Data Protection Officer (DPO) assigned | [Met/Partial/Gap] | [Contact info] | [N/A or description] |
| Privacy by design implemented | [Met/Partial/Gap] | [Process/Design docs] | [Description] |
| Data breach notification process | [Met/Partial/Gap] | [Process doc, SLA] | [Description] |
| DPIA (Data Protection Impact Assessment) | [Met/Partial/Gap] | [DPIA doc] | [Description] |

---

## HIPAA Compliance (if applicable)

### Protected Health Information (PHI) Controls

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| PHI encryption at rest (AES-256) | [Met/Partial/Gap] | [Config/Code] | [Description] |
| PHI encryption in transit (TLS 1.2+) | [Met/Partial/Gap] | [Config] | [Description] |
| Access controls for PHI | [Met/Partial/Gap] | [IAM logs] | [Description] |
| Audit logging (all PHI access logged) | [Met/Partial/Gap] | [Log sample] | [Description] |
| Authentication (multi-factor for admin access) | [Met/Partial/Gap] | [MFA enabled] | [Description] |
| Integrity controls (data cannot be altered undetected) | [Met/Partial/Gap] | [Checksums/hash verification] | [Description] |

### Business Associate Agreement (BAA)

| Requirement | Status | Evidence | Gap (if any) |
|-------------|--------|----------|------------|
| BAA signed with all vendors handling PHI | [Met/Partial/Gap] | [BAA signatures] | [List unsigned vendors] |
| Subcontractors covered | [Met/Partial/Gap] | [Flow-down BAAs] | [Description] |
| Breach notification clause included | [Met/Partial/Gap] | [BAA section ref] | [Description] |

### Breach Notification

| Control | Status | Process | Gap (if any) |
|---------|--------|---------|------------|
| Breach detection capability | [Met/Partial/Gap] | [Monitoring/alerting] | [Description] |
| Notification SLA (60 days) | [Met/Partial/Gap] | [Policy doc] | [Description] |
| HHS notification process | [Met/Partial/Gap] | [Process doc] | [Description] |

---

## SOC2 Compliance (if applicable)

### Security (CC)

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| Change management process | [Met/Partial/Gap] | [Process doc, approval log] | [Description] |
| Access control policy | [Met/Partial/Gap] | [Policy, IAM logs] | [Description] |
| Least privilege implementation | [Met/Partial/Gap] | [IAM config audit] | [Description] |
| Vulnerability management program | [Met/Partial/Gap] | [Scan reports, remediation log] | [Description] |
| Incident response process | [Met/Partial/Gap] | [IR plan, test records] | [Description] |

### Availability (A)

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| Uptime SLA defined | [Met/Partial/Gap] | [SLA document] | [Description] |
| Uptime achieved | [Met/Partial/Gap] | [Monitoring dashboard] | [% uptime] |
| Disaster recovery plan | [Met/Partial/Gap] | [DR plan, RTO/RPO] | [Description] |
| Failover/backup tested | [Met/Partial/Gap] | [Test results, frequency] | [Description] |

### Processing Integrity (PI)

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| Complete/accurate transaction logging | [Met/Partial/Gap] | [Log sample audit] | [Description] |
| Error handling and monitoring | [Met/Partial/Gap] | [Process, alert setup] | [Description] |
| Data completeness validation | [Met/Partial/Gap] | [Reconciliation process] | [Description] |

### Confidentiality (C)

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| Encryption for sensitive data | [Met/Partial/Gap] | [Config/code review] | [Description] |
| Key management | [Met/Partial/Gap] | [Key rotation policy] | [Description] |

### Privacy (P)

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| Privacy policy published | [Met/Partial/Gap] | [Policy URL] | [Description] |
| Data handling practices transparent | [Met/Partial/Gap] | [Policy, terms] | [Description] |
| Customer consent documented | [Met/Partial/Gap] | [Consent mechanism] | [Description] |

---

## PCI-DSS Compliance (if applicable)

### Cardholder Data Security

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| Encrypted storage (AES-256) | [Met/Partial/Gap] | [Config/code] | [Description] |
| Encrypted transmission (TLS 1.2+) | [Met/Partial/Gap] | [Config] | [Description] |
| Access controls (least privilege) | [Met/Partial/Gap] | [IAM logs] | [Description] |
| No cleartext sensitive data in logs | [Met/Partial/Gap] | [Log audit sample] | [Description] |
| No storage of CVV/PIN | [Met/Partial/Gap] | [Architecture review] | [Description] |

### Vulnerability Management

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| Penetration testing (annual) | [Met/Partial/Gap] | [PT report date] | [Description] |
| Vulnerability scanning (quarterly) | [Met/Partial/Gap] | [Scan results] | [Description] |
| Patch management | [Met/Partial/Gap] | [Patch log] | [Description] |

### Audit & Compliance

| Control | Status | Evidence | Gap (if any) |
|---------|--------|----------|------------|
| Network segmentation (cardholder data isolated) | [Met/Partial/Gap] | [Network diagram] | [Description] |
| Audit logging (all access) | [Met/Partial/Gap] | [Log sample] | [Description] |
| ASV (Approved Scanning Vendor) scan | [Met/Partial/Gap] | [ASV report] | [Description] |
| AOC (Attestation of Compliance) submitted | [Met/Partial/Gap] | [AOC level, date] | [Description] |

---

## WCAG 2.1 Accessibility Compliance (if applicable)

### Level A (Foundational)

| Criterion | Status | Evidence | Gap (if any) |
|-----------|--------|----------|------------|
| 1.1.1 Non-text Content (alt text) | [Met/Partial/Gap] | [Audit/code review] | [Description] |
| 1.3.1 Info & Relationships (semantic HTML) | [Met/Partial/Gap] | [Code review] | [Description] |
| 1.4.1 Use of Color (not color alone) | [Met/Partial/Gap] | [Design review] | [Description] |
| 2.1.1 Keyboard (all interactive elements accessible) | [Met/Partial/Gap] | [Manual testing] | [Description] |
| 2.4.1 Bypass Blocks (skip to content link) | [Met/Partial/Gap] | [Code review] | [Description] |
| 3.2.1 On Focus (no unexpected behavior) | [Met/Partial/Gap] | [Testing] | [Description] |
| 3.3.1 Error Identification (errors marked) | [Met/Partial/Gap] | [Testing] | [Description] |
| 4.1.1 Parsing (valid HTML, no duplicate IDs) | [Met/Partial/Gap] | [HTML validation] | [Description] |

### Level AA (Enhanced)

| Criterion | Status | Evidence | Gap (if any) |
|-----------|--------|----------|------------|
| 1.4.3 Contrast (Minimum) (4.5:1 text, 3:1 graphics) | [Met/Partial/Gap] | [Color audit] | [Description] |
| 2.4.3 Focus Order (logical tab order) | [Met/Partial/Gap] | [Manual testing] | [Description] |
| 2.4.4 Link Purpose (descriptive link text) | [Met/Partial/Gap] | [Content review] | [Description] |
| 3.2.4 Consistent Identification (icons used consistently) | [Met/Partial/Gap] | [Design review] | [Description] |
| 3.3.3 Error Suggestion (correction suggestions provided) | [Met/Partial/Gap] | [Testing] | [Description] |

---

## Internal Policy Compliance

| Policy | Status | Evidence | Gap (if any) |
|--------|--------|----------|------------|
| [Policy 1: Code of Conduct] | [Met/Partial/Gap] | [Training/attestation] | [Description] |
| [Policy 2: Security Standards] | [Met/Partial/Gap] | [Architecture review] | [Description] |
| [Policy 3: Data Classification] | [Met/Partial/Gap] | [Data mapping] | [Description] |
| [Policy 4: Incident Response] | [Met/Partial/Gap] | [Plan/drill results] | [Description] |
| [Policy 5: Change Management] | [Met/Partial/Gap] | [Change log audit] | [Description] |

---

## Evidence Inventory

### Policies & Procedures
- [ ] [Policy/Procedure 1]: Location: [Path/URL], Last Updated: [Date]
- [ ] [Policy/Procedure 2]: Location: [Path/URL], Last Updated: [Date]

### Control Documentation
- [ ] [Control 1]: Evidence location: [Path], Last Validated: [Date]
- [ ] [Control 2]: Evidence location: [Path], Last Validated: [Date]

### Audit Logs & Monitoring
- [ ] [Log type 1]: Location: [Path], Retention: [Years], Access: [Restricted]
- [ ] [Log type 2]: Location: [Path], Retention: [Years], Access: [Restricted]

### Training & Certifications
- [ ] [Training 1]: Completed by: [Team], Date: [Date], Renewal: [Date]
- [ ] [Training 2]: Completed by: [Team], Date: [Date], Renewal: [Date]

---

## Remediation Timeline

### Critical (Immediate)
- [Gap 1]: Owner: [Name], Target: [ASAP]
- [Gap 2]: Owner: [Name], Target: [ASAP]

### High (Within 1 Week)
- [Gap 3]: Owner: [Name], Target: [Date]
- [Gap 4]: Owner: [Name], Target: [Date]

### Medium (Within 1 Month)
- [Gap 5]: Owner: [Name], Target: [Date]

### Low (Next Quarter)
- [Gap 6]: Owner: [Name], Target: [Date]

---

## Audit & Review Schedule

- **Monthly**: Gap status review, remediation progress
- **Quarterly**: Full compliance audit, framework renewal
- **Annually**: External audit (if required), certification renewal

---

## Sign-Off

- **Compliance Officer**: [Name] | [Date]
- **Legal Counsel** (if applicable): [Name] | [Date]
- **Executive Sponsor**: [Name] | [Date]

**Next Review Date**: [Date]

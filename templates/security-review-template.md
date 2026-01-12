# Security Review

**Goal/Deliverable**: [Goal Name or Service Name]  
**Review Date**: [Date]  
**Security Reviewer**: [Name/Team]  
**Scope**: [Full system / Components / APIs / Data handling / Infrastructure / Authentication]  
**Compliance Requirements**: [GDPR / HIPAA / SOC2 / PCI-DSS / Internal Standards / None]  

---

## Executive Summary

| Finding | Count | Status |
|---------|-------|--------|
| Critical Issues | [#] | [% Resolved] |
| High Issues | [#] | [% Resolved] |
| Medium Issues | [#] | [% Resolved] |
| Low Issues | [#] | [% Resolved] |
| **Total** | [#] | [% Resolved] |

**Overall Risk**: [Critical / High / Medium / Low]  
**Compliance Status**: [Fully Compliant / Partial / At Risk / Non-Compliant]  

---

## System Overview

### System Architecture
[High-level diagram or description of system components]

### Data Classification
- **Sensitive Data Handled**: [PII, PHI, PCI, credentials, other]
- **Data Storage**: [Databases, caches, logs, where sensitive data lives]
- **Data in Transit**: [APIs, messaging, replication]

### External Dependencies & Integrations
- [Service 1]: [Type of integration, data shared]
- [Service 2]: [Type of integration, data shared]
- [Service 3]: [Type of integration, data shared]

---

## Threat Vectors & Assessment

### 1. External Attacks

| Threat Vector | Likelihood | Impact | Mitigation Status |
|----------------|-----------|--------|-------------------|
| Network attacks (DDoS, scanners) | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |
| API abuse or exploitation | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |
| Injection attacks (SQL, command) | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |
| Authentication bypass | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |

### 2. Insider Threats

| Threat Vector | Likelihood | Impact | Mitigation Status |
|----------------|-----------|--------|-------------------|
| Unauthorized access to sensitive data | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |
| Malicious code injection | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |
| Credential theft or abuse | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |

### 3. Data Breaches

| Threat Vector | Likelihood | Impact | Mitigation Status |
|----------------|-----------|--------|-------------------|
| Unencrypted data at rest | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |
| Unencrypted data in transit | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |
| Insecure backups or logs | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |

### 4. Supply Chain & Dependency Risks

| Threat Vector | Likelihood | Impact | Mitigation Status |
|----------------|-----------|--------|-------------------|
| Vulnerable dependencies (CVEs) | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |
| Compromised third-party services | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |
| Vendor lock-in or service unavailability | [Low/Med/High] | [Low/Med/High] | [In Place / Planned / Gap] |

---

## Critical Findings

### [CRITICAL-1]: [Finding Title]

- **Description**: [What is the vulnerability]
- **CVSS Score**: [9.0-10.0]
- **Affected Component(s)**: [Service/Module]
- **Root Cause**: [Why it exists]
- **Exploitation Risk**: [How likely and how easy to exploit]
- **Potential Impact**: [Data loss, service compromise, compliance violation]
- **Remediation**: 
  - Action: [Specific fix]
  - Owner: [Name]
  - Target Date: [ASAP, within X days]
  - Acceptance Criteria: [How we verify fix]
- **Status**: [Not Started / In Progress / Blocked / Resolved]

### [CRITICAL-2]: [Finding Title]

[Same structure]

---

## High Findings

### [HIGH-1]: [Finding Title]

- **Description**: [What is the vulnerability]
- **CVSS Score**: [7.0-8.9]
- **Affected Component(s)**: [Service/Module]
- **Root Cause**: [Why it exists]
- **Remediation**: 
  - Action: [Specific fix]
  - Owner: [Name]
  - Target Date: [Within 1 week]
  - Acceptance Criteria: [How we verify fix]
- **Status**: [Not Started / In Progress / Blocked / Resolved]

### [HIGH-2]: [Finding Title]

[Same structure]

---

## Medium & Low Findings (Summary)

| ID | Finding | Component | CVSS | Owner | Target Date | Status |
|----|---------|-----------|------|-------|------------|--------|
| MED-1 | [Title] | [Component] | [Score] | [Owner] | [Date] | [Status] |
| MED-2 | [Title] | [Component] | [Score] | [Owner] | [Date] | [Status] |
| LOW-1 | [Title] | [Component] | [Score] | [Owner] | [Date] | [Status] |

---

## Dependency Scan Results

### Vulnerable Dependencies

| Package | Version | CVE | Severity | Status |
|---------|---------|-----|----------|--------|
| [Package] | [Version] | [CVE-ID] | [Critical/High] | [Needs Update / Updating / Safe] |
| [Package] | [Version] | [CVE-ID] | [Critical/High] | [Needs Update / Updating / Safe] |

**Scan Tool**: [npm audit, pip safety, OWASP DependencyCheck, etc.]  
**Last Scan**: [Date]  
**Next Scan**: [Date]  

---

## Authentication & Authorization Review

### Authentication Mechanisms

- **Type**: [OAuth2, JWT, API Keys, Basic Auth, Multi-factor, other]
- **Implementation**: [Secure, acceptable, needs improvement]
- **Issues**: [None / List any findings]
- **Remediation**: [If applicable]

### Authorization Controls

- **Model**: [Role-Based Access Control, Attribute-Based, other]
- **Coverage**: [Applied to APIs, UI, backend services, databases]
- **Issues**: [None / Privilege escalation risks, missing controls, scope creep]
- **Remediation**: [If applicable]

### Secrets Management

- **API Keys**: [Rotated regularly, stored securely, access logs, other]
- **Database Credentials**: [Encrypted, rotated, limited access, other]
- **Issue**: [None / Hardcoded secrets, weak rotation, overly permissive]
- **Remediation**: [If applicable]

---

## Encryption & Data Protection

### Encryption at Rest

- **Databases**: [AES-256, full database encryption, application-level]
- **Backups**: [Encrypted, key management, access control]
- **Logs**: [PII redacted, retention policy, access restricted]
- **Issue**: [None / Unencrypted data, weak keys, key management gaps]
- **Remediation**: [If applicable]

### Encryption in Transit

- **TLS Version**: [1.2+ for all connections]
- **Certificate Management**: [Valid, non-expired, auto-renewal]
- **HTTP/S**: [All HTTPS except internal-only services]
- **API Encryption**: [All sensitive data encrypted]
- **Issue**: [None / Missing TLS, weak cipher, unencrypted channels]
- **Remediation**: [If applicable]

---

## Compliance Alignment (if applicable)

### [GDPR / HIPAA / SOC2 / PCI-DSS / Other]

| Requirement | Status | Gap | Remediation |
|-------------|--------|-----|-------------|
| [Requirement 1] | [Met / Partial / Gap] | [If gap, what's missing] | [How to remediate] |
| [Requirement 2] | [Met / Partial / Gap] | [If gap, what's missing] | [How to remediate] |

---

## Logging & Monitoring

- **Audit Logging**: [All access logged, timestamp, user, action, data touched]
- **Log Storage**: [Secure, tamper-proof, retention policy]
- **Alerting**: [Real-time alerts for suspicious activity, escalation path]
- **Issue**: [None / Insufficient logging, alert gaps, log access not restricted]
- **Remediation**: [If applicable]

---

## Incident Response & Recovery

- **Incident Plan**: [Documented, tested, all team aware]
- **Detection**: [Time to detect breach/compromise]
- **Response SLA**: [Time to contain and remediate]
- **Notification**: [Customer notification process, regulatory notification]
- **Recovery**: [Backup/restore tested, RTO/RPO defined]
- **Gap**: [Any gaps in incident response capability]

---

## Remediation Timeline

### Critical (Fix Now)
- [CRITICAL-1]: By [Date]
- [CRITICAL-2]: By [Date]

### High (Within 1 Week)
- [HIGH-1]: By [Date]
- [HIGH-2]: By [Date]

### Medium (Within 1 Month)
- [MED-1]: By [Date]
- [MED-2]: By [Date]

### Low (Opportunistic)
- [LOW-1]: [No target date, backlog]

---

## Approval & Sign-Off

- **Security Lead**: [Name] | [Date]
- **Engineering Lead**: [Name] | [Date]
- **Compliance Officer** (if applicable): [Name] | [Date]

**Next Review Date**: [Date]

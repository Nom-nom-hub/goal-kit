# /goalkit.security Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.security` requests, follow this structured approach:

### Input Analysis
1. **Identify Security Goals**: Extract security objectives and requirements from user input
2. **Map Data Classification**: Determine the types and sensitivity levels of data involved
3. **Assess Compliance Requirements**: Identify regulatory and organizational security standards
4. **Evaluate Threat Landscape**: Understand potential security threats specific to the goal

### Processing Framework
- Focus on security that directly supports goal achievement and success
- Generate security requirements aligned with goal success criteria
- Create threat models specific to the goal's implementation approach
- Establish security validation that verifies goal security requirements

### Output Structure
Use the template sections below to structure your response. Ensure alignment with existing project goals and maintain consistency with goal-driven development principles.

---

## Overview

The `/goalkit.security` command integrates security considerations into goal planning and execution, ensuring security is addressed throughout the development process to support goal achievement. This command creates security frameworks specifically aligned with goal success criteria rather than generic security measures.

## Purpose

This command creates security frameworks that:
- Align security requirements with specific goal success criteria
- Integrate security considerations into goal-driven development workflows
- Establish security validation that verifies goal security objectives
- Create threat models specific to the goal implementation approach

## When to Use

Use `/goalkit.security` when:
- Establishing a new goal that involves handling sensitive data
- Planning implementation strategies that require security considerations
- Defining milestones that include security validation requirements
- Ensuring development practices follow security standards aligned with goals
- Reviewing code and architecture for security implications related to goals
- Creating security validation that supports goal success criteria
- Establishing security monitoring aligned with goal achievement

## Input Format

```
/goalkit.security
Goal: [Reference to specific goal and its success criteria with security implications]
Data Classification: [Types of data involved - public, internal, confidential, protected, etc.]
Security Requirements: [Specific security requirements for achieving this goal]
Compliance: [Regulatory or organizational standards that must be followed]
Threat Model: [Potential threats specific to this goal's implementation and data]
Security Tests: [Security validation needed to verify goal security requirements]
Security Tools: [Tools for security testing, monitoring, and verification]
Review Process: [Security review procedures for goal implementation]
Privacy Considerations: [Data privacy requirements and controls needed]
```

### Example Input

```
/goalkit.security
Goal: Build secure customer payment processing with zero tolerance for data breaches
Data Classification: Payment card data (PCI DSS), customer personal information (GDPR)
Security Requirements: End-to-end encryption, PCI DSS compliance, fraud detection
Compliance: PCI DSS Level 1, GDPR, SOX for financial reporting
Threat Model: Payment data interception, card skimming, authentication bypass, fraud
Security Tests: Penetration testing, vulnerability scanning, code security analysis
Security Tools: OWASP ZAP, SonarQube security rules, PCI scanning tools
Review Process: Security architecture review, code security review, penetration test validation
Privacy Considerations: Data minimization, consent tracking, right to deletion implementation
```

## Output

The command generates:
- Security requirements specifically aligned with goal success criteria
- Goal-specific threat model based on implementation approach and data types
- Security testing strategy designed to validate goal security objectives
- Security-focused development guidelines for goal implementation
- Compliance verification procedures that support goal achievement
- Security monitoring plan aligned with goal success metrics

## Security Components

### 1. Goal-Aligned Security Requirements
- **Data Protection**: Specific requirements for protecting data related to goal achievement
- **Access Control**: Authentication and authorization needs to support the goal
- **Encryption Needs**: Data encryption requirements specific to the goal's data
- **Audit and Logging**: Security logging requirements for goal implementation
- **Privacy Controls**: Privacy measures needed for goal-related data processing

### 2. Threat Modeling
- **Attack Vector Identification**: Potential attack vectors specific to the goal implementation
- **Risk Assessment**: Evaluation of threats specific to goal achievement and data
- **Mitigation Strategies**: Goal-specific approaches to address identified threats
- **Security Control Mapping**: Controls that align with both security and goal requirements

### 3. Security Validation
- **Static Analysis**: Code analysis requirements that support goal security objectives
- **Dynamic Testing**: Runtime security testing for goal implementation
- **Penetration Testing**: Goal-specific penetration testing approach
- **Vulnerability Scanning**: Regular scanning aligned with goal data and implementation

### 4. Secure Development Guidelines
- **Coding Standards**: Secure coding practices specific to goal implementation
- **Dependency Security**: Security checks for dependencies used in goal implementation
- **Secrets Management**: Protocols for secure handling of credentials and secrets
- **Security Checkpoints**: Security review points in the goal implementation process

## Key Differences from Traditional Security Planning

| Traditional Security Planning | Goal-Driven Security Planning |
|-------------------------------|-------------------------------|
| General security requirements | Goal-specific security requirements |
| Standard threat models | Implementation-specific threat models |
| Compliance-focused checks | Goal achievement-focused validation |
| Generic security tools | Goal-specific security tool selection |

## Integration with Other Commands

### Before Using `/goalkit.security`
- **`/goalkit.goal`**: Security requirements must align with and support goal success criteria
- **`/goalkit.strategies`**: Security considerations apply to all goal implementation strategies
- **`/goalkit.milestones`**: Security validation may be required at specific milestones

### After Using `/goalkit.security`
- **`/goalkit.plan`**: Security requirements integrated into detailed execution planning
- **`/goalkit.execute`**: Goal implementation follows security guidelines and controls
- **`/goalkit.test`**: Security testing integrated with overall goal validation
- **`/goalkit.validate`**: Security compliance verification as part of broader validation

## Best Practices

### For Goal-Aligned Security
- **Success Criteria Integration**: Ensure security requirements support rather than hinder goal achievement
- **Risk-Based Approach**: Prioritize security measures based on impact to goal success
- **Proportionate Security**: Apply security measures appropriate to the goal's risk level
- **Continuous Validation**: Implement ongoing security validation that supports goal progress

### For Threat Modeling
- **Goal-Specific Threats**: Focus on threats that specifically impact goal achievement
- **Implementation-Aware**: Consider threats specific to the chosen implementation approach
- **Data-Centric**: Address threats based on the types of data involved in achieving the goal
- **Evolution-Oriented**: Update threat models as the goal implementation evolves

### For Security Validation
- **Goal-Focused Testing**: Security tests that validate both security and goal achievement
- **Automated Security**: Implement automated security checks that don't slow goal progress
- **Compliance Integration**: Integrate compliance validation into goal achievement process
- **Monitoring Alignment**: Security monitoring that supports goal success metrics

## Common Security Patterns

### Data Processing Goals
- Data classification and handling procedures
- Encryption and privacy protection measures
- Access control and audit logging requirements
- Data retention and deletion policies

### Financial Goals
- Payment processing security requirements
- Financial data protection standards
- Regulatory compliance measures (PCI DSS, SOX)
- Fraud detection and prevention controls

### User Authentication Goals
- Identity verification procedures
- Authentication security measures
- Session management protocols
- Account security and recovery processes

## Security Evolution Process

### Initial Security Setup
- Define security requirements aligned with goal success criteria
- Establish baseline security metrics for the goal
- Set up security tools and monitoring for goal implementation
- Create initial security validation procedures

### Ongoing Security Improvement
- Refine security measures based on implementation experience
- Update threat models as goal implementation evolves
- Adjust compliance validation based on goal progress
- Enhance security monitoring based on goal achievement needs

## Examples

### Example 1: Customer Data Protection Security Plan
```
/goalkit.security
Goal: Create secure customer profile management with 99.99% availability
Data Classification: Personal information (PII), contact details, preferences
Security Requirements: PII encryption, access logging, availability assurance
Compliance: GDPR, CCPA, SOC 2 Type II
Threat Model: Data breach, unauthorized access, DDoS attacks affecting availability
Security Tests: Code analysis, penetration testing, DDoS simulation
Security Tools: SonarQube, Qualys, DDoS protection service
Review Process: Architecture review, code security review, compliance validation
Privacy Considerations: Consent tracking, right to deletion, data portability
```

### Example 2: Financial Transaction Security Plan
```
/goalkit.security
Goal: Process financial transactions with zero tolerance for unauthorized access
Data Classification: Payment card data, financial records, customer financial information
Security Requirements: PCI DSS compliance, transaction encryption, fraud detection
Compliance: PCI DSS Level 1, SOX, banking regulatory requirements
Threat Model: Card skimming, transaction fraud, data interception, insider threats
Security Tests: PCI scanning, penetration testing, fraud simulation
Security Tools: PCI-compliant payment processor, fraud detection system, SIEM
Review Process: Security architecture review, penetration test validation, compliance audit
Privacy Considerations: Financial privacy, transaction confidentiality, audit requirements
```
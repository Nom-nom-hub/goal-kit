# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting Security Vulnerabilities

We take security seriously. If you discover a security vulnerability, please follow these guidelines:

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. **Create a private GitHub Security Advisory**:
   - Go to [GitHub Security Advisories](https://github.com/Nom-nom-hub/goal-kit/security/advisories)
   - Click "Report a vulnerability"
   - Provide detailed information about the security issue
3. **Include** as much detail as possible:
    - Description of the vulnerability
    - Steps to reproduce
    - Potential impact
    - Suggested fix (if known)

### What to Expect

- **Response Time**: We aim to acknowledge security reports within 48 hours
- **Investigation**: Security team will investigate and assess the vulnerability
- **Resolution**: Valid vulnerabilities will be fixed in the next appropriate release
- **Credit**: We will credit researchers who responsibly disclose vulnerabilities

### Security Updates

- Critical security fixes will be released as patch versions (e.g., 1.0.1)
- Security updates will be announced via GitHub Releases
- Major version updates may include security improvements

## Security Best Practices

### For Users
- Keep Goal Kit updated to the latest version
- Use templates as intended and validate generated content
- Be cautious with automated goal and strategy generation
- Review and customize generated documentation before use

### For Contributors
- Follow secure coding practices in scripts and templates
- Validate user input in any interactive components
- Keep dependencies updated and audited
- Use parameterized commands to prevent injection attacks

## Scope

This security policy covers:
- Goal Kit core functionality and templates
- Documentation and examples
- Build and deployment scripts
- GitHub Actions workflows

It does not cover:
- Third-party AI services or agents using Goal Kit
- User-generated content or goals
- External integrations or APIs

## Contact

### Security Issues
- **GitHub Security Advisories**: [Report vulnerabilities privately](https://github.com/Nom-nom-hub/goal-kit/security/advisories)
- **Private Reports Only**: Do NOT create public issues for security vulnerabilities

### Non-Security Issues
- **GitHub Issues**: [Create issues for bugs and feature requests](https://github.com/Nom-nom-hub/goal-kit/issues)
- **GitHub Discussions**: [General questions and discussions](https://github.com/Nom-nom-hub/goal-kit/discussions)

---

*Last updated: December 2024*
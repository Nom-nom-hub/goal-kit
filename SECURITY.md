# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting Security Vulnerabilities

We take security seriously. If you discover a security vulnerability, please follow these guidelines:

### How to Report

1. **Do NOT** create a public GitHub issue for security vulnerabilities
2. **Email** the security team: security@goal-kit.dev
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

- **Security Email**: security@goal-kit.dev
- **Project Email**: contact@goal-kit.dev
- **GitHub Issues**: Use for non-security related issues and feature requests

---

*Last updated: December 2024*
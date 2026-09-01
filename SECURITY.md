# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | :white_check_mark: Active |
| < Latest | :x: No |

Always use the latest version to receive security patches and improvements.

---

## Reporting a Vulnerability

The EskomSense AI team takes security seriously. We appreciate your efforts to responsibly disclose any security concerns.

**Please do NOT report security vulnerabilities through public GitHub issues.**

### Step-by-Step Reporting Process

1. **Identify the vulnerability** — Document the issue with clear reproduction steps.
2. **Email the security team** at **raphasha27@github.com** with the following:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)
3. **Wait for acknowledgment** — You will receive a response within **48 hours**.
4. **Collaborate on the fix** — We may reach out for additional details.
5. **Disclosure** — We will coordinate a public disclosure timeline with you.

### What to Include

- Type of vulnerability (e.g., model poisoning, data leakage, API abuse)
- Affected component and version
- Attack vector and prerequisites
- Proof of concept (if available)
- Your suggested remediation

---

## Security Response Timeline

| Phase | Timeframe |
|-------|-----------|
| Initial acknowledgment | 48 hours |
| Severity assessment | 5 business days |
| Patch development | 10–15 business days |
| Coordinated disclosure | 30 days after fix |

Critical infrastructure-related vulnerabilities may receive expedited timelines.

---

## Security Design

This project implements the following security measures:

- **Environment Variables** — No hardcoded secrets or API keys
- **Input Validation** — Pydantic models validate all API inputs
- **Model Integrity** — Checksums for model artifact verification
- **File Upload Restrictions** — Only CSV files accepted for training data
- **Rate Limiting** — API endpoints protected from abuse
- **Dependency Scanning** — Automated vulnerability checks in CI

---

## Security Best Practices for Users

When deploying or developing with EskomSense AI:

### Configuration
- Always use **environment variables** for API keys and model paths
- Never commit `.env` files or secrets to version control
- Use strong, unique secrets for any authentication layer
- Restrict API access to trusted networks

### Model Security
- Verify model artifact integrity before deployment
- Use checksums to detect tampered model files
- Monitor for adversarial input patterns in prediction requests
- Validate input data ranges before inference

### Data Protection
- Training data may contain sensitive grid information — ensure proper access controls
- Encrypt data at rest and in transit for production deployments
- Audit data access logs regularly
- Use synthetic data for development and testing

### Network
- Deploy behind a reverse proxy with TLS termination
- Enable CORS only for trusted frontend origins
- Use HTTPS for all API communications
- Restrict database access to application network

### Dependencies
- Run `pip audit` for Python dependency vulnerabilities
- Enable Dependabot alerts for automatic vulnerability notifications
- Review dependency updates before merging
- Pin dependency versions for reproducibility

---

## Dependency Management

### Python Dependencies

```bash
# Check for known vulnerabilities
pip install pip-audit
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Automated Scanning

- **Dependabot** is enabled for automatic dependency update PRs.
- **CI pipeline** runs `pip-audit` on every PR.
- Review and merge Dependabot PRs promptly.

---

## Responsible Disclosure

We follow [coordinated disclosure](https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure) principles:

- Report vulnerabilities privately before public disclosure.
- We will credit reporters in release notes (unless anonymity is preferred).
- We ask that you do not exploit the vulnerability beyond what is necessary to demonstrate it.
- We will not pursue legal action against researchers who follow this policy.

---

## Contact

- **Security Email**: raphasha27@github.com
- **General Issues**: [GitHub Issues](../../issues)

Thank you for helping keep EskomSense AI and its users safe.

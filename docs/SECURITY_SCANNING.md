# Security Scanning in CI/CD

## Overview
Our CI/CD pipeline includes multiple open-source security tools to scan for vulnerabilities before deployment. This provides similar functionality to commercial tools like Nexus IQ or Sonatype Lifecycle.

## Security Tools Integrated

### 1. **pip-audit** (Dependency Vulnerability Scanning)
- **Purpose:** Scans Python dependencies for known CVEs
- **Database:** PyPI Advisory Database + OSV
- **When it runs:** On every push/PR to `api/` or `functions/`
- **Fail behavior:** Continues on error (warnings only)

**Example output:**
```
Found 2 known vulnerabilities in 1 package
Name    Version ID             Fix Versions
------- ------- -------------- ------------
werkzeug 2.0.1  GHSA-xxx-xxx  2.0.2,2.1.0
```

### 2. **Bandit** (SAST - Static Application Security Testing)
- **Purpose:** Finds common security issues in Python code
- **Checks for:** SQL injection, hardcoded passwords, unsafe YAML loading, insecure random, etc.
- **Severity levels:** Low, Medium, High
- **Configuration:** Scans with `-ll` (medium and high severity only)

**Example issues detected:**
- Use of `eval()`
- Hardcoded passwords or secrets
- Use of `pickle` (unsafe deserialization)
- SQL injection vulnerabilities

### 3. **Trivy** (Container Image Scanning)
- **Purpose:** Scans Docker images for OS and application vulnerabilities
- **Database:** NVD, Red Hat, Debian, Alpine, etc.
- **Coverage:** OS packages, Python packages, Node modules, etc.
- **Integration:** Results uploaded to GitHub Security tab (SARIF format)

**What it scans:**
- Base image vulnerabilities (python:3.11-slim)
- Application dependencies installed via pip
- OS-level packages (apt packages)

### 4. **Gitleaks** (Secrets Detection)
- **Purpose:** Prevents hardcoded secrets from being committed
- **Detects:** API keys, passwords, tokens, private keys, AWS credentials
- **Database:** 140+ secret patterns
- **Action:** Fails the build if secrets found

**Example patterns detected:**
- AWS Access Keys
- GitHub tokens
- GCP service account keys
- Private SSH keys
- Database connection strings with passwords

## CI/CD Workflows

### API Deployment Pipeline (`api.yml`)
```
Push to api/ → Security Scan → Build Docker → Push to GCR → Deploy to Cloud Run → Health Check
```

**Steps:**
1. **Security Scanning Job:**
   - pip-audit: Scan `requirements.txt`
   - Bandit: SAST on Python code
   - Trivy: Scan Docker image
   - Gitleaks: Check for secrets
   - Upload reports as artifacts

2. **Build & Deploy Job:**
   - Authenticate via Workload Identity
   - Build Docker image with version tags
   - Push to Google Container Registry
   - Deploy to Cloud Run with new image
   - Run health check
   - Comment deployment info on PR

### Functions Deployment Pipeline (`functions.yml`)
```
Push to functions/ → Security Scan → Deploy Cloud Function
```

**Steps:**
1. Security scan with pip-audit and Bandit
2. Deploy via `gcloud functions deploy`
3. Version tracking with git SHA

## Viewing Security Results

### GitHub Security Tab
1. Go to repository → **Security** tab
2. Click **Code scanning alerts**
3. View Trivy findings (CRITICAL and HIGH severity)

### Workflow Artifacts
1. Go to **Actions** tab
2. Click on workflow run
3. Download **security-reports** artifact
4. Contains:
   - `pip-audit-report.json`
   - `bandit-report.json`
   - `trivy-results.sarif`

## Security Policy

### Blocking vs Warning
- **Blocking (build fails):**
  - Gitleaks finds secrets
  - Build or deployment errors
  
- **Warning only (continues):**
  - pip-audit finds vulnerabilities
  - Bandit finds security issues
  - Trivy finds vulnerabilities

**Rationale:** For a demo project, we want visibility without blocking deployments. In production, you would set `continue-on-error: false` for critical checks.

## Production Recommendations

### Upgrade to Commercial Tools (Optional)
If your organization requires enterprise features:

1. **Snyk** (replaces pip-audit + Trivy)
   - Real-time vulnerability database
   - Auto-remediation PRs
   - License compliance
   ```yaml
   - uses: snyk/actions/python@master
     with:
       command: test
   ```

2. **Sonatype Nexus IQ** (replaces pip-audit)
   - Policy enforcement
   - License risk analysis
   - Component firewall
   ```yaml
   - uses: sonatype-nexus-community/iq-github-action@main
     with:
       serverUrl: ${{ secrets.NEXUS_IQ_URL }}
       applicationId: sre-governance-api
   ```

3. **SonarQube** (replaces Bandit)
   - Code quality + security
   - Technical debt tracking
   - Coverage analysis

### Hardening for Production

**In `api.yml` and `functions.yml`, change:**
```yaml
# From:
continue-on-error: true

# To:
continue-on-error: false
```

**Add dependency approval workflow:**
```yaml
- name: Check for high severity vulnerabilities
  run: |
    CRITICAL=$(pip-audit -r requirements.txt --format json | jq '.vulnerabilities | length')
    if [ "$CRITICAL" -gt 0 ]; then
      echo "Found $CRITICAL vulnerabilities"
      exit 1
    fi
```

**Add container signing:**
```yaml
- name: Sign container image
  uses: sigstore/cosign-installer@main
- run: cosign sign ${{ env.IMAGE_NAME }}:${{ github.sha }}
```

## Local Development

### Run security scans locally:

**Python dependencies:**
```bash
cd api
pip install pip-audit
pip-audit -r requirements.txt
```

**Code security:**
```bash
pip install bandit
bandit -r api/ -ll
```

**Container scan:**
```bash
docker build -t api:test api/
docker run --rm aquasec/trivy image api:test
```

**Secrets scan:**
```bash
brew install gitleaks  # or download binary
gitleaks detect --source . --verbose
```

## Comparison: Open Source vs Nexus IQ

| Feature | Open Source Stack | Nexus IQ |
|---------|------------------|----------|
| Dependency scanning | pip-audit (free) | ✅ Built-in |
| Container scanning | Trivy (free) | ✅ Built-in |
| SAST | Bandit (free) | ✅ Built-in |
| License compliance | ❌ Manual | ✅ Automated |
| Policy enforcement | ❌ Manual | ✅ Built-in |
| Auto-remediation | ❌ Manual | ✅ Automated |
| Cost | **$0** | ~$3000-10000/year |

**For a portfolio/demo project:** Open source stack is perfect ✅

**For production at scale:** Consider commercial tools if budget allows

## Further Reading
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [GitHub Advanced Security](https://docs.github.com/en/code-security)
- [Supply Chain Security Best Practices](https://slsa.dev/)

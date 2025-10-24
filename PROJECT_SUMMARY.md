# SRE Observability & Governance Platform - Project Summary

## 🎯 Project Overview
**Mock Project**: GCP Cloud Platform Governance & Observability System

Built an SRE governance platform for a customer engagement application on GCP, focusing on change management, compliance automation, and SLO monitoring (simulating enterprise ServiceNow-like workflows).

---

## 📐 Architecture

### Application Layer (Serverless - No Kubernetes)
- **Cloud Run**: Serverless microservices (customer engagement API)
- **Cloud Functions**: Event-driven automation (alerts, triggers)
- **Cloud SQL**: Managed PostgreSQL database
- **Cloud Storage**: Static assets and backups

**Why Serverless?** → Simpler governance, easier change tracking, aligns with enterprise consumer servicing use cases

---

## 🏗️ Key Components to Build

### 1. Infrastructure as Code (Terraform)
```
terraform/
├── cloud-run/          # API services
├── cloud-functions/    # Automation functions
├── cloud-sql/          # Database setup
├── networking/         # VPC, firewall rules
└── iam/               # Service accounts & permissions
```

**Deliverables:**
- ✅ Terraform modules for all GCP resources
- ✅ State management with remote backend
- ✅ All changes tracked via Git
- ✅ GitHub Actions for automated deployments

---

### 2. Governance & Change Management System

**Python-based Change Management Tracker** (Mock ServiceNow):

```
change-management/
├── app.py                    # Flask/FastAPI web app
├── models.py                 # Database models (changes, incidents)
├── database.py               # SQLite/PostgreSQL connection
├── dashboard.py              # Streamlit dashboard
└── templates/                # Web UI templates
```

**Features to Implement:**
- ✅ Change request tracking with approval workflows
- ✅ Incident management (create, track, resolve)
- ✅ Problem management
- ✅ CMDB-style inventory (apps, dependencies, CIs)
- ✅ Risk assessment scoring
- ✅ Change calendar visualization
- ✅ MTTR (Mean Time To Recovery) metrics
- ✅ Automated change record creation from Terraform deployments

**Database Schema:**
- Changes table (ID, title, status, risk, approver, timestamp)
- Incidents table (ID, severity, status, created_at, resolved_at)
- CMDB table (service_name, dependencies, owner, version)

---

### 3. Observability & SLO Monitoring

#### Cloud Monitoring Setup (GCP Native)

**Metrics Collection:**
- **Automatic**: CPU, memory, request count, latency (no code needed)
- **Custom** (optional): Add 1-2 custom metrics using `google-cloud-monitoring` library
  - Example: `checkout_failures`, `transaction_success_rate`

**SLO Dashboards to Create:**
1. **API Availability SLO**: 99.9% uptime target
2. **Latency SLO**: p95 < 300ms, p99 < 500ms
3. **Error Budget Tracking**: Current vs. allocated budget
4. **Request Success Rate**: 99.5% target

**Alerting Configuration:**
- ✅ Alert policies for SLO violations
- ✅ Slack/Email notification channels
- ✅ Integration with incident tracker (auto-create incidents)

#### Cloud Logging
- ✅ Centralized log aggregation
- ✅ Log-based metrics
- ✅ Search and analysis queries
- ✅ Export to BigQuery (optional for analysis)

**Monitoring vs Logging:**
- **Cloud Monitoring** = Metrics (numbers) → Dashboards, alerts, SLOs
- **Cloud Logging** = Logs (text events) → Search, analysis, audit trails

---

### 4. Security & Compliance Automation

**Python Scripts to Build:**

```
compliance/
├── vulnerability_scanner.py      # Dependency scanning (pip-audit/safety)
├── iam_audit.py                 # Review IAM permissions
├── resource_inventory.py        # Generate CMDB updates
├── monthly_report.py            # Compliance dashboard report
└── evidence_collector.py        # Collect audit evidence
```

**Automated Compliance Checks:**
- ✅ Monthly vulnerability scans (pip-audit, safety)
- ✅ Dependency security checks
- ✅ IAM permission audits (detect overprivileged accounts)
- ✅ Resource inventory updates
- ✅ Cost anomaly detection
- ✅ Evidence collection for controls (PDF/JSON reports)

**Evidence Collection Process:**
```python
# evidence_collector.py generates monthly compliance pack:
{
    "month": "2025-10",
    "vulnerability_scan": scan_report_url,
    "change_approvals": approved_changes_list,
    "slo_compliance": slo_status,
    "iam_audit": permissions_review
}
```

---

### 5. Chaos Engineering & Incident Simulation

**Python Chaos Scripts** (Proves monitoring works):

```
chaos/
├── trigger_latency_incident.py       # Simulate slow API responses
├── trigger_error_spike.py            # Generate 5xx errors
└── simulate_deployment_failure.py    # Test rollback procedures
```

**Example Flow:**
1. Run `trigger_latency_incident.py`
2. Cloud Monitoring detects SLO breach
3. Alert fires → Creates incident ticket automatically
4. Follow runbook to resolve
5. Document MTTR and lessons learned

**Why This Matters:** Shows chaos engineering mindset + validates observability stack

---

### 6. Documentation & Runbooks

```
docs/
├── runbooks/
│   ├── high-api-latency.md
│   ├── service-unavailable.md
│   ├── failed-deployment-rollback.md
│   └── security-alert-response.md
├── architecture/
│   ├── gcp-platform-diagram.png
│   └── data-flow-diagram.png
├── compliance/
│   └── control-evidence.md
├── slo-definitions.md
└── change-management-procedures.md
```

**Runbook Template:**
```markdown
# Runbook: High API Latency

## Symptoms
- p95 latency > 500ms
- Alert: "API_LATENCY_HIGH"

## Investigation Steps
1. Check Cloud Monitoring dashboard
2. Review recent deployments (last 2 hours)
3. Check Cloud SQL connection pool
4. Review Cloud Logging for errors

## Resolution
- Rollback: `terraform apply -target=module.api`
- Scale Cloud Run: `gcloud run services update...`

## Post-Incident
- Create incident report in change management system
- Update CMDB if configuration changed
```

**Create 3-4 Runbooks:**
- ✅ High API latency
- ✅ Service unavailable (5xx errors)
- ✅ Failed deployment rollback
- ✅ Security alert response

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Cloud Platform** | Google Cloud Platform (GCP) |
| **Compute** | Cloud Run, Cloud Functions |
| **Database** | Cloud SQL (PostgreSQL) |
| **Storage** | Cloud Storage |
| **IaC** | Terraform |
| **Observability** | Cloud Monitoring, Cloud Logging |
| **Backend** | Python (Flask/FastAPI) |
| **Dashboard** | Streamlit |
| **CI/CD** | GitHub Actions |
| **Security** | pip-audit, safety, Trivy |

---

## 📦 GitHub Repository Structure

### **MVP Structure (6-hour scope)**
```
sre-governance-platform/
│
├── api/                            # Simple Flask API
│   ├── app.py                     # 2 endpoints: /health, /api/users
│   ├── requirements.txt
│   └── Dockerfile                 # For Cloud Run
│
├── terraform/                      # Basic IaC
│   ├── main.tf                    # Cloud Run + Cloud Function
│   ├── variables.tf
│   └── outputs.tf
│
├── dashboard/                      # Streamlit governance dashboard
│   ├── app.py                     # Single-file dashboard (~150 lines)
│   └── requirements.txt
│
├── monitoring/                     # Observability configs
│   └── slo-config.yaml            # 1 SLO definition
│
├── chaos/                          # Chaos script
│   └── trigger_latency.py         # Simple load test with delay
│
├── functions/                      # Cloud Function
│   └── alert-handler/
│       ├── main.py                # Receives alert webhook
│       └── requirements.txt
│
├── compliance/                     # Basic security
│   └── scan_dependencies.py       # Runs pip-audit
│
├── docs/                           # Documentation
│   ├── runbooks/
│   │   └── high-latency.md        # 1 runbook
│   ├── architecture.png           # Simple diagram
│   └── screenshots/               # Dashboard images
│
├── README.md                       # Project overview
└── .gitignore
```

### **Full Structure (with enhancements)**
```
sre-governance-platform/
│
├── api/                            # Flask API
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── terraform/                      # Complete IaC
│   ├── cloud-run/
│   ├── cloud-functions/
│   ├── networking/
│   └── iam/
│
├── dashboard/                      # Interactive dashboard
│   ├── app.py                     # Streamlit with SQLite
│   ├── database.py                # DB operations
│   ├── models.py                  # Data models
│   └── requirements.txt
│
├── monitoring/                     # Observability
│   ├── slo-definitions.yaml
│   ├── alert-policies.yaml
│   └── dashboards/
│
├── compliance/                     # Security automation
│   ├── vulnerability_scanner.py
│   ├── iam_audit.py
│   ├── resource_inventory.py
│   └── evidence_collector.py
│
├── chaos/                          # Chaos engineering
│   ├── trigger_latency_incident.py
│   ├── trigger_error_spike.py
│   └── simulate_deployment_failure.py
│
├── functions/                      # Cloud Functions
│   ├── alert-handler/
│   └── incident-creator/
│
├── .github/workflows/              # CI/CD
│   ├── terraform-deploy.yaml
│   └── compliance-scan.yaml
│
├── docs/                           # Documentation
│   ├── runbooks/
│   │   ├── high-latency.md
│   │   ├── service-unavailable.md
│   │   └── rollback-procedure.md
│   ├── architecture/
│   │   ├── infrastructure-diagram.png
│   │   └── data-flow-diagram.png
│   └── slo-definitions.md
│
└── README.md
```

---

## 🚀 Implementation Phases

### **MVP - 6 Hour Scope (AI-Assisted Build)**

**Goal:** Demonstrate SRE governance skills with minimal but impressive deliverables

#### **Hour 1-2: Core Infrastructure**
1. ✅ Simple Flask API (2 endpoints: `/health`, `/api/users`)
2. ✅ Basic Terraform for Cloud Run deployment
   - **Important:** Set `min-instances = 1` (not scale-to-zero)
   - Reason: Accurate SLO tracking - cold starts would skew availability metrics
   - Cost: ~$8-10/month (covered by GCP free tier)
3. ✅ Deploy to GCP Cloud Run
4. ✅ Enable Cloud Monitoring (automatic metrics)

**Deliverable:** Live API with URL

---

#### **Hour 3-4: Observability & Governance Dashboard**
5. ✅ Streamlit dashboard (single file, ~150 lines)
   - Mock incident list (3-4 hardcoded examples)
   - Mock change list (3-4 examples with status)
   - Simple metrics display (uptime, MTTR)
   - CMDB table (5-6 services with dependencies)
6. ✅ Cloud Monitoring SLO configuration (1 SLO: availability)
7. ✅ Screenshot dashboards

**Deliverable:** Interactive governance dashboard

---

#### **Hour 5: Automation & Chaos**
8. ✅ Build chaos mode into Flask API
   - Add `?chaos=latency` parameter that triggers `time.sleep(3)` on server side
   - Add `?chaos=error` parameter that returns 500 errors
   - **Key:** Delay must be in API code (server-side), not in test script (client-side)
9. ✅ One chaos script: `trigger_latency.py` (hits API with `?chaos=latency` parameter)
10. ✅ One Cloud Function: Alert handler (receives Pub/Sub message, logs to Cloud Logging)
   - **MVP approach:** Function logs alert details (no actual email sent)
   - Logs structured data: incident ID, condition, severity, timestamp
   - **Production note:** Would integrate SendGrid/PagerDuty/ServiceNow APIs
11. ✅ Alert policy in Cloud Monitoring (created via Terraform)
   - **Flow:** API latency > 2s → Alert fires → Publishes to Pub/Sub → Triggers Cloud Function
   - **Key components:** Alert policy, Pub/Sub topic, notification channel
   - Alert policy lives in Cloud Monitoring, configured by Terraform
12. ✅ Run chaos → trigger alert → check Cloud Logging for function output

**Deliverable:** Working alert → automation flow (visible in Cloud Logging)

---

#### **Hour 6: Documentation & Polish**
12. ✅ One runbook: `high-latency.md` (with real commands)
13. ✅ Architecture diagram (simple draw.io/Excalidraw)
14. ✅ README with screenshots
15. ✅ Quick compliance script: `scan_dependencies.py` (runs pip-audit, saves output)

**Deliverable:** Professional GitHub repo ready to demo

---

### **Post-MVP Enhancements (Optional, if you have more time)**

#### **Phase 2A: Make Dashboard Dynamic (2-3 hours)**
- Replace hardcoded data with SQLite database
- Add forms to create incidents/changes
- Store real chaos incident data

#### **Phase 2B: CI/CD Pipeline (1-2 hours)**
- GitHub Actions: Deploy on push to main
- Terraform plan on PR

#### **Phase 2C: More Compliance (2 hours)**
- IAM audit script
- Evidence collector
- Monthly report generator

**Total realistic timeline:** 6 hours MVP + 5-7 hours enhancements = **1-2 days complete project**

---

## 🎓 Key Concepts Explained

### Cloud Run vs Cloud Functions
| Cloud Run | Cloud Functions |
|-----------|----------------|
| Containers (any language) | Code snippets only |
| HTTP services & background jobs | Event-driven only |
| Full control over server | Managed runtime |
| **Use for:** APIs, microservices | **Use for:** Automation, triggers |

### Cloud Monitoring Metrics Collection
- **Automatic Metrics** (no code): CPU, memory, requests, latency
- **Custom Metrics** (need library): Business metrics like `checkout_failures`
  ```python
  from google.cloud import monitoring_v3
  # Send custom metric to Cloud Monitoring
  ```

### OpenTelemetry (OTEL) vs Cloud Logging
- **OTEL** = Instrumentation framework (collects data) - vendor-agnostic
- **Cloud Logging** = Storage/analysis backend (where data goes) - GCP-specific
- You can use both: OTEL SDK → exports to Cloud Logging
- **For this project:** Use Cloud Logging directly (simpler)

### SRE Runbooks
Step-by-step incident response guides. Essential for:
- Consistency in incident handling
- Onboarding new team members
- Reducing MTTR
- Post-incident documentation

### Evidence Collection
Proves compliance controls are working for audits:
- "We scan vulnerabilities monthly" → Evidence: scan reports + timestamps
- "All changes are approved" → Evidence: change records with approvals
- "We monitor uptime" → Evidence: SLO compliance reports

---

## 📊 Key Deliverables to Showcase

### 1. Live Dashboard (Streamlit/Flask)
- Current SLO status (availability, latency, error budget)
- Open incidents and changes
- Compliance score
- MTTR metrics
- Change calendar

### 2. GitHub Repository
- Clean, modular Terraform code
---

## ⏱️ Realistic Time Estimates

**MVP (Portfolio-ready):** 6 hours
- Can be built in one focused Saturday
- AI (Claude) writes most code
- You test, deploy, document

**Enhanced Version:** 11-13 hours total
- MVP (6h) + Enhancements (5-7h)
- Add dynamic database, CI/CD, more compliance scripts

**Full Featured:** 15-20 hours
- Everything in the summary
- Multiple runbooks, comprehensive testing
- Production-quality polish

**Budget:** $0-5/month (GCP Free Tier covers everything in MVP)
- Architecture diagrams (GCP resources, data flow)
- 3-4 incident response runbooks
- SLO definitions and calculations
- Compliance evidence collection process
- Change management procedures

### 4. Demo Materials
- Screenshots of dashboards
- Video walkthrough (5-10 minutes)
- Incident simulation demonstration
- Compliance report samples

---

## ✅ Success Criteria

**This project demonstrates:**
- ✅ GCP cloud engineering expertise (Cloud Run, Functions, Monitoring)
- ✅ Infrastructure as Code (Terraform best practices)
- ✅ Observability & SLO management (Cloud Monitoring)
- ✅ Governance thinking (change/incident management)
- ✅ Compliance automation (security scanning, evidence collection)
- ✅ Python scripting & automation
- ✅ CI/CD pipelines (GitHub Actions)
- ✅ SRE mindset (runbooks, chaos engineering, MTTR tracking)
- ✅ Process documentation (runbooks, architecture)

**Aligns with job requirements:**
- GCP orchestration & infrastructure automation ✓
- ServiceNow-like governance workflows ✓
- Python scripting for automation ✓
- Observability and SLO monitoring ✓
- Compliance and risk management ✓
- Documentation and runbooks ✓

---

## 🎯 Next Steps

1. **Set up GCP project** and enable necessary APIs
2. **Initialize Git repository** with the structure above
3. **Start with Phase 1** (MVP infrastructure)
4. **Build incrementally** - test each component
5. **Document as you go** - don't leave docs for the end
6. **Take screenshots** of dashboards and workflows
7. **Create demo video** showing incident flow
8. **Polish GitHub README** with architecture diagrams

---

## 📚 Resources Needed

- GCP Free Tier account (sufficient for this project)
- GitHub account
- Python 3.9+
- Terraform CLI
- gcloud CLI
- Text editor/IDE

---

**Estimated Timeline:** 6 weeks (part-time) or 2-3 weeks (full-time)

**Budget:** $0-20/month (GCP Free Tier covers most resources)

---

*This project showcases enterprise SRE governance capabilities without requiring actual ServiceNow access, proving you understand both technical implementation and process-driven operations.*

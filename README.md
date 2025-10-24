# SRE Governance Platform

A production-grade Site Reliability Engineering platform demonstrating enterprise SRE practices, cloud infrastructure automation, and ServiceNow-like governance workflows on Google Cloud Platform.

## 🎯 Project Overview

This project showcases key competencies for Senior SRE roles: **observability**, **operational excellence**, **SLO monitoring**, **infrastructure automation**, and **governance compliance**.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     GCP Cloud Infrastructure                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Cloud Run API  ─────────┐                                      │
│  (Flask + Chaos)         │                                      │
│                          ▼                                      │
│              Cloud Monitoring ────► Alert Policy               │
│                          │          (SLO burn rate)             │
│                          │                 │                    │
│                          ▼                 ▼                    │
│                  Custom SLOs         Pub/Sub Topic              │
│                  • Availability       (sre-alerts)              │
│                  • Latency                   │                  │
│                                              ▼                  │
│                                    Cloud Function (2nd gen)     │
│                                    (Alert Handler)              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
         ▲                              ▲                ▲
         │                              │                │
    Terraform IaC                 GitHub Actions      Monitoring
    (GCS Backend)                 (CI/CD + Security)  Dashboard
```

## 🔑 Key Capabilities Demonstrated

### 1. **Cloud Infrastructure & Automation (GCP)**
- Infrastructure as Code with **Terraform** (14 managed resources)
- Remote state management in **GCS** with versioning
- Cloud Run services, Cloud Functions (2nd gen), Pub/Sub messaging
- Automated deployments via **GitHub Actions CI/CD**

### 2. **Observability & SLO Monitoring**
- **Custom SLOs**: API Availability (99.5%) & Latency (95% < 1s)
- **Alert Policies**: High latency threshold with Pub/Sub notifications
- **Error Budget Tracking**: Real-time burn rate monitoring
- **Dashboards**: Streamlit UI mimicking ServiceNow governance views

### 3. **ServiceNow Governance Practices**
- Incident management simulation via alert handler
- Change tracking through Git + CI/CD pipeline
- CMDB-like configuration tracking in Terraform state
- Compliance evidence via automated security scanning

### 4. **Security & Compliance Controls**
- **Dependency scanning**: pip-audit (CVE detection)
- **SAST**: Bandit for Python code security
- **Container scanning**: Trivy (replaces NexusIQ functionality)
- **Secrets detection**: Gitleaks
- **Infrastructure scanning**: Automated in CI/CD pipeline

### 5. **Chaos Engineering & Resilience**
- Chaos modes: latency injection, error simulation
- Traffic generation scripts for SLO validation
- Automated incident triggering for alert testing

### 6. **Python Automation & Scripting**
- Flask API with observability instrumentation
- Cloud Functions for event-driven incident handling
- Chaos engineering automation scripts
- Infrastructure compliance scanning

## 📁 Project Structure

```
.
├── terraform/              # IaC for all GCP resources
│   ├── main.tf            # Cloud Run, SLOs, Alerts, Functions
│   └── outputs.tf         # Resource IDs and URLs
├── api/                   # Cloud Run Flask API
│   ├── app.py            # Chaos modes + observability
│   └── Dockerfile        # Container build
├── functions/             # Cloud Function (2nd gen)
│   └── alert-handler/    # Pub/Sub alert processor
├── .github/workflows/     # CI/CD pipelines
│   ├── terraform.yml     # Infrastructure deployment
│   ├── api.yml          # API security + deployment
│   └── functions.yml     # Function deployment
├── chaos/                # Chaos engineering scripts
│   ├── trigger_latency.py
│   └── healthy_traffic.py
├── dashboard/            # ServiceNow-like UI
│   └── app.py           # Streamlit dashboard
└── docs/                 # Documentation
    ├── CICD_SETUP.md
    └── SECURITY_SCANNING.md
```

## 🚀 Key Features

### SLO Management
- **Availability SLO**: 99.5% uptime target over 30-day rolling window
- **Latency SLO**: 95% of requests < 1000ms
- Alert on SLO burn rate with automated notification

### Automated CI/CD Pipeline
- **Security-first**: pip-audit, Bandit, Trivy, Gitleaks on every commit
- **Terraform**: Auto-apply infrastructure changes on merge to main
- **API Deployment**: Docker build → GCR push → Cloud Run deploy
- **Functions**: Automated deployment with version tracking

### Compliance & Governance
- Infrastructure state tracking (Terraform state in GCS)
- Change audit trail (Git history + CI/CD logs)
- Security scan evidence (artifacts in GitHub Actions)
- Dependency vulnerability reports (NexusIQ alternative)

## 🛠️ Technologies

**Cloud**: Google Cloud Platform (Cloud Run, Cloud Functions, Pub/Sub, Cloud Monitoring)  
**IaC**: Terraform 1.11.0 with GCS backend  
**Languages**: Python 3.11, Bash  
**CI/CD**: GitHub Actions with Workload Identity Federation  
**Security**: pip-audit, Bandit, Trivy, Gitleaks  
**Monitoring**: Cloud Monitoring, Custom SLOs, Alert Policies  

## 📊 Observability Highlights

- **Custom Metrics**: Request latency (p50, p95, p99)
- **SLO Tracking**: Real-time error budget consumption
- **Alert Integration**: Pub/Sub → Cloud Function → Incident notification
- **Dashboard**: Multi-view UI (Incidents, Changes, CMDB, Compliance)

## 🎓 Skills Demonstrated

✅ **Lead SRE Practices**: SLO ownership, error budget management, operational excellence  
✅ **GCP Cloud Engineering**: Cloud Run, Functions, Terraform automation  
✅ **ServiceNow Governance**: Incident/Change/CMDB workflows, compliance evidence  
✅ **Python Automation**: API development, chaos scripts, infrastructure tooling  
✅ **Security Controls**: Vulnerability scanning (NexusIQ alternative), compliance reporting  
✅ **CI/CD**: GitHub Actions, automated deployments, security scanning  
✅ **Risk Mitigation**: Chaos testing, SLO monitoring, automated alerting  

## 🔗 Live Deployment

- **API**: https://sre-governance-api-qxt5h5aqiq-uc.a.run.app
- **Monitoring**: GCP Console → Cloud Monitoring → SLOs
- **CI/CD**: GitHub Actions workflows on every push

---

**Built to demonstrate enterprise SRE capabilities for Lead/Senior SRE positions**

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Page config
st.set_page_config(
    page_title="SRE Governance Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Header
st.title("🛡️ SRE Governance & Observability Platform")
st.markdown("**Mock ServiceNow-like Dashboard** | Real-time monitoring, incident management, and compliance tracking")

# Sidebar
st.sidebar.header("Navigation")
view = st.sidebar.radio("Select View", ["Overview", "Incidents", "Changes", "CMDB", "Compliance"])

# Mock Data
mock_incidents = [
    {"id": "INC001", "severity": "High", "status": "Open", "description": "API Latency Spike", "created": "2025-10-23 14:30", "mttr": "-"},
    {"id": "INC002", "severity": "Medium", "status": "Resolved", "description": "Database Connection Pool Exhausted", "created": "2025-10-22 09:15", "mttr": "45 min"},
    {"id": "INC003", "severity": "Critical", "status": "Resolved", "description": "Service Unavailable - 5xx Errors", "created": "2025-10-21 18:20", "mttr": "22 min"},
    {"id": "INC004", "severity": "Low", "status": "Resolved", "description": "Slow Dashboard Load Time", "created": "2025-10-20 11:00", "mttr": "1.5 hr"},
]

mock_changes = [
    {"id": "CHG001", "title": "Deploy API v1.2.0", "risk": "Medium", "status": "Approved", "date": "2025-10-24 10:00", "approver": "Sarah Chen"},
    {"id": "CHG002", "title": "Scale Cloud Run to min-instances=2", "risk": "Low", "status": "Pending", "date": "2025-10-25 14:00", "approver": "Pending"},
    {"id": "CHG003", "title": "Update Terraform Config - Alert Policy", "risk": "Low", "status": "Approved", "date": "2025-10-23 16:00", "approver": "Mike Johnson"},
    {"id": "CHG004", "title": "Database Schema Migration", "risk": "High", "status": "Scheduled", "date": "2025-10-26 02:00", "approver": "Sarah Chen"},
]

mock_cmdb = [
    {"service": "sre-governance-api", "type": "Cloud Run", "dependencies": "Cloud Monitoring, Pub/Sub", "owner": "SRE Team", "version": "1.0.0"},
    {"service": "alert-handler", "type": "Cloud Function", "dependencies": "Pub/Sub, Cloud Logging", "owner": "SRE Team", "version": "1.0.0"},
    {"service": "governance-dashboard", "type": "Streamlit", "dependencies": "Cloud Run API", "owner": "SRE Team", "version": "1.0.0"},
    {"service": "cloud-monitoring", "type": "GCP Service", "dependencies": "Cloud Run", "owner": "Google", "version": "N/A"},
    {"service": "pubsub-alerts", "type": "Pub/Sub Topic", "dependencies": "Cloud Monitoring, Cloud Function", "owner": "SRE Team", "version": "N/A"},
]

mock_slo_data = {
    "availability": {"target": 99.9, "actual": 99.95, "budget_remaining": 85},
    "latency_p95": {"target": 300, "actual": 245, "unit": "ms"},
    "latency_p99": {"target": 500, "actual": 420, "unit": "ms"},
    "error_rate": {"target": 0.5, "actual": 0.12, "unit": "%"},
}

# ========================================
# OVERVIEW VIEW
# ========================================
if view == "Overview":
    # SLO Metrics Row
    st.header("📊 SLO Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Availability SLO",
            value=f"{mock_slo_data['availability']['actual']}%",
            delta=f"{mock_slo_data['availability']['actual'] - mock_slo_data['availability']['target']:.2f}%"
        )
        st.caption(f"Target: {mock_slo_data['availability']['target']}% | Budget: {mock_slo_data['availability']['budget_remaining']}%")
    
    with col2:
        st.metric(
            label="⚡ p95 Latency",
            value=f"{mock_slo_data['latency_p95']['actual']}ms",
            delta=f"{mock_slo_data['latency_p95']['target'] - mock_slo_data['latency_p95']['actual']}ms"
        )
        st.caption(f"Target: < {mock_slo_data['latency_p95']['target']}ms")
    
    with col3:
        st.metric(
            label="⚡ p99 Latency",
            value=f"{mock_slo_data['latency_p99']['actual']}ms",
            delta=f"{mock_slo_data['latency_p99']['target'] - mock_slo_data['latency_p99']['actual']}ms"
        )
        st.caption(f"Target: < {mock_slo_data['latency_p99']['target']}ms")
    
    with col4:
        st.metric(
            label="❌ Error Rate",
            value=f"{mock_slo_data['error_rate']['actual']}%",
            delta=f"{mock_slo_data['error_rate']['target'] - mock_slo_data['error_rate']['actual']:.2f}%"
        )
        st.caption(f"Target: < {mock_slo_data['error_rate']['target']}%")
    
    st.divider()
    
    # Status Overview Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚨 Open Incidents")
        open_incidents = [inc for inc in mock_incidents if inc["status"] == "Open"]
        if open_incidents:
            for inc in open_incidents:
                severity_icon = "🔴" if inc["severity"] == "Critical" else "🟠" if inc["severity"] == "High" else "🟡"
                st.warning(f"{severity_icon} **{inc['id']}** - {inc['description']} (Created: {inc['created']})")
        else:
            st.success("✅ No open incidents")
        
        st.metric(label="Average MTTR (Last 7 Days)", value="36 minutes", delta="-12 min")
    
    with col2:
        st.subheader("📋 Pending Changes")
        pending_changes = [chg for chg in mock_changes if chg["status"] in ["Pending", "Scheduled"]]
        if pending_changes:
            for chg in pending_changes:
                risk_icon = "🔴" if chg["risk"] == "High" else "🟠" if chg["risk"] == "Medium" else "🟢"
                st.info(f"{risk_icon} **{chg['id']}** - {chg['title']} (Scheduled: {chg['date']})")
        else:
            st.success("✅ No pending changes")
        
        st.metric(label="Changes This Week", value="12", delta="+3")

# ========================================
# INCIDENTS VIEW
# ========================================
elif view == "Incidents":
    st.header("🚨 Incident Management")
    
    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Open", "Resolved"])
    with col2:
        severity_filter = st.selectbox("Filter by Severity", ["All", "Critical", "High", "Medium", "Low"])
    
    # Filter data
    filtered_incidents = mock_incidents
    if status_filter != "All":
        filtered_incidents = [inc for inc in filtered_incidents if inc["status"] == status_filter]
    if severity_filter != "All":
        filtered_incidents = [inc for inc in filtered_incidents if inc["severity"] == severity_filter]
    
    # Display table
    df_incidents = pd.DataFrame(filtered_incidents)
    st.dataframe(df_incidents, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # MTTR Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average MTTR", "36 min", delta="-12 min")
    with col2:
        st.metric("Total Incidents (30d)", "28", delta="-5")
    with col3:
        st.metric("Critical Incidents (30d)", "2", delta="-1")

# ========================================
# CHANGES VIEW
# ========================================
elif view == "Changes":
    st.header("📋 Change Management")
    
    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Approved", "Scheduled"])
    with col2:
        risk_filter = st.selectbox("Filter by Risk", ["All", "High", "Medium", "Low"])
    
    # Filter data
    filtered_changes = mock_changes
    if status_filter != "All":
        filtered_changes = [chg for chg in filtered_changes if chg["status"] == status_filter]
    if risk_filter != "All":
        filtered_changes = [chg for chg in filtered_changes if chg["risk"] == risk_filter]
    
    # Display table
    df_changes = pd.DataFrame(filtered_changes)
    st.dataframe(df_changes, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Change Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Changes This Month", "45", delta="+8")
    with col2:
        st.metric("Success Rate", "98.2%", delta="+1.5%")
    with col3:
        st.metric("Avg Approval Time", "4.2 hours", delta="-0.8 hr")

# ========================================
# CMDB VIEW
# ========================================
elif view == "CMDB":
    st.header("🗂️ Configuration Management Database")
    st.markdown("Service inventory with dependencies and ownership")
    
    # Display CMDB table
    df_cmdb = pd.DataFrame(mock_cmdb)
    st.dataframe(df_cmdb, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Service Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Services", "5", delta="+1")
    with col2:
        st.metric("Cloud Run Services", "2")
    with col3:
        st.metric("Cloud Functions", "1")

# ========================================
# COMPLIANCE VIEW
# ========================================
elif view == "Compliance":
    st.header("✅ Security & Compliance")
    
    # Compliance Score
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Compliance Score", "94%", delta="+2%")
    with col2:
        st.metric("Open Vulnerabilities", "3", delta="-5")
    with col3:
        st.metric("Last Scan", "2 hours ago")
    
    st.divider()
    
    # Compliance Checks
    st.subheader("🔍 Recent Compliance Checks")
    
    compliance_checks = [
        {"check": "Dependency Vulnerability Scan", "status": "✅ Pass", "last_run": "2025-10-23 20:00", "next_run": "2025-11-23 20:00"},
        {"check": "IAM Permission Audit", "status": "⚠️ Warning", "last_run": "2025-10-20 08:00", "next_run": "2025-11-20 08:00"},
        {"check": "Resource Inventory Update", "status": "✅ Pass", "last_run": "2025-10-23 22:00", "next_run": "2025-10-24 22:00"},
        {"check": "SLO Compliance Report", "status": "✅ Pass", "last_run": "2025-10-23 18:00", "next_run": "2025-10-24 18:00"},
    ]
    
    df_compliance = pd.DataFrame(compliance_checks)
    st.dataframe(df_compliance, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Vulnerability Details
    st.subheader("🐛 Open Vulnerabilities")
    st.warning("⚠️ **CVE-2024-12345**: Moderate severity - Update Flask to 3.0.1+ (Scheduled in CHG001)")
    st.info("ℹ️ **CVE-2024-67890**: Low severity - Update gunicorn to 21.2.1+ (Scheduled)")
    st.info("ℹ️ **Overprivileged Service Account**: Remove compute.admin role from alert-handler-sa")

# Footer
st.divider()
st.caption("🛡️ SRE Governance Platform v1.0.0 | Mock ServiceNow-like Dashboard | Built with Streamlit + GCP")

import base64
import json
import logging
from datetime import datetime
import functions_framework
from google.cloud import logging as cloud_logging

# Initialize Cloud Logging properly
cloud_logging.Client().setup_logging()
logger = logging.getLogger(__name__)

@functions_framework.cloud_event
def handle_alert(cloud_event):
    """
    Cloud Run Function (2nd gen) triggered by Pub/Sub to handle alerts from Cloud Monitoring.
    
    Version: 2.0 - Enhanced logging and CI/CD integration
    In MVP: Logs alert details + simulates email notification
    Production: Would integrate with SendGrid/PagerDuty/ServiceNow APIs
    """
    
    # Decode Pub/Sub message from CloudEvent
    message_data = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
    alert_payload = json.loads(message_data)
    
    # Extract alert information
    incident_id = alert_payload.get('incident', {}).get('incident_id', 'unknown')
    condition_name = alert_payload.get('incident', {}).get('condition_name', 'unknown')
    summary = alert_payload.get('incident', {}).get('summary', 'No summary')
    state = alert_payload.get('incident', {}).get('state', 'unknown')
    severity = alert_payload.get('incident', {}).get('severity', 'unknown')
    policy_name = alert_payload.get('incident', {}).get('policy_name', 'unknown')
    
    # Log alert with proper Cloud Logging
    logger.info("=" * 60)
    logger.info(f"🚨 ALERT RECEIVED [v2.0]: {policy_name}")
    logger.info(f"📋 Incident ID: {incident_id}")
    logger.info(f"🔍 Condition: {condition_name}")
    logger.info(f"⚠️ State: {state} | Severity: {severity}")
    logger.info(f"📝 Summary: {summary}")
    logger.info("=" * 60)
    
    # Simulate email notification
    logger.info("📧 MOCK EMAIL NOTIFICATION:")
    logger.info(f"  To: ops-team@example.com")
    logger.info(f"  Subject: 🚨 ALERT: {policy_name}")
    logger.info(f"  Body: Incident {incident_id} - {condition_name}")
    
    # Production integrations would go here:
    # - SendGrid: sendgrid.send_email(...)
    # - PagerDuty: pagerduty.create_incident(...)
    # - ServiceNow: servicenow.create_incident(...)
    # - Slack: slack.post_message(...)
    
    logger.info(f"✅ Alert {incident_id} processed successfully")
    
    # Force log flush
    print(f"FORCE_LOG: Alert {incident_id} processed at {datetime.utcnow().isoformat()}", flush=True)

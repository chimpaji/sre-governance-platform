#!/usr/bin/env python3
"""
Chaos Engineering Script - Trigger Latency Incident

This script repeatedly calls the API with the chaos=latency parameter
to trigger high latency and test the monitoring/alerting system.

Expected flow:
1. Script hits API with ?chaos=latency (3s delay per request)
2. Cloud Monitoring detects p99 latency > 2000ms
3. Alert fires after 60s of sustained high latency
4. Alert publishes message to Pub/Sub topic
5. (Future) Cloud Function processes alert and logs to Cloud Logging
"""

import requests
import time
import sys
from datetime import datetime

# Configuration
API_URL = "https://sre-governance-api-qxt5h5aqiq-uc.a.run.app"
ENDPOINT = "/api/users"
CHAOS_PARAM = "chaos=latency"
DURATION_SECONDS = 120  # Run for 2 minutes to trigger 60s alert threshold
REQUEST_INTERVAL = 0.5  # Time between requests

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def trigger_latency():
    """Trigger latency chaos on the API"""
    log(f"🔥 Starting chaos engineering test")
    log(f"Target: {API_URL}{ENDPOINT}?{CHAOS_PARAM}")
    log(f"Duration: {DURATION_SECONDS} seconds")
    log(f"Expected: 3 second delay per request")
    log("-" * 60)
    
    start_time = time.time()
    request_count = 0
    success_count = 0
    error_count = 0
    
    try:
        while (time.time() - start_time) < DURATION_SECONDS:
            request_count += 1
            request_start = time.time()
            
            try:
                response = requests.get(
                    f"{API_URL}{ENDPOINT}",
                    params={"chaos": "latency"},
                    timeout=10
                )
                request_duration = time.time() - request_start
                
                if response.status_code == 200:
                    success_count += 1
                    log(f"✅ Request #{request_count}: {response.status_code} | "
                        f"Duration: {request_duration:.2f}s | "
                        f"Users: {response.json().get('count', 'N/A')}")
                else:
                    error_count += 1
                    log(f"❌ Request #{request_count}: {response.status_code} | "
                        f"Duration: {request_duration:.2f}s")
                    
            except requests.exceptions.RequestException as e:
                error_count += 1
                request_duration = time.time() - request_start
                log(f"❌ Request #{request_count}: Failed | "
                    f"Duration: {request_duration:.2f}s | Error: {str(e)}")
            
            # Wait before next request
            time.sleep(REQUEST_INTERVAL)
    
    except KeyboardInterrupt:
        log("\n⚠️  Test interrupted by user")
    
    # Summary
    total_duration = time.time() - start_time
    log("-" * 60)
    log(f"🏁 Chaos test completed")
    log(f"Total requests: {request_count}")
    log(f"Successful: {success_count}")
    log(f"Failed: {error_count}")
    log(f"Total duration: {total_duration:.2f}s")
    log("-" * 60)
    log(f"📊 Next steps:")
    log(f"1. Check Cloud Monitoring for latency spike")
    log(f"2. Wait 1-2 minutes for alert to fire")
    log(f"3. Check Pub/Sub topic 'sre-alerts' for messages")
    log(f"4. View alert in GCP Console: Cloud Monitoring > Alerting")

if __name__ == "__main__":
    log("🚀 Chaos Engineering - API Latency Test")
    trigger_latency()

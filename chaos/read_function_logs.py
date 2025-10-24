#!/usr/bin/env python3
"""
Read Cloud Function logs using Cloud Logging API
"""

from google.cloud import logging
from datetime import datetime, timedelta
import sys

def read_function_logs():
    # Initialize Cloud Logging client
    client = logging.Client()
    
    # Calculate time range (last 30 minutes)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)
    
    # Format timestamps for the filter
    start_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    # Build filter for Cloud Function logs
    filter_str = f'''
    resource.type="cloud_run_revision"
    AND resource.labels.service_name="alert-handler"
    AND timestamp >= "{start_str}"
    AND timestamp <= "{end_str}"
    AND (
        textPayload!=""
        OR jsonPayload.message!=""
        OR severity >= "INFO"
    )
    '''
    
    print(f"🔍 Reading Cloud Function logs from {start_str} to {end_str}")
    print("="*80)
    
    try:
        # Query logs
        entries = client.list_entries(filter_=filter_str, order_by=logging.ASCENDING)
        
        log_count = 0
        for entry in entries:
            log_count += 1
            timestamp = entry.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')
            severity = entry.severity
            
            # Get log message
            if entry.payload:
                if hasattr(entry.payload, 'get'):
                    # JSON payload
                    message = entry.payload.get('message', str(entry.payload))
                else:
                    # Text payload
                    message = str(entry.payload)
            else:
                message = "No message"
            
            # Print formatted log
            print(f"[{timestamp}] [{severity}] {message}")
            
            # Show additional fields if available
            if hasattr(entry, 'labels') and entry.labels:
                for key, value in entry.labels.items():
                    if key in ['execution_id', 'instance_id']:
                        print(f"  {key}: {value}")
        
        print("="*80)
        print(f"📊 Found {log_count} log entries")
        
        if log_count == 0:
            print("💡 No application logs found. This could mean:")
            print("   - Function hasn't been invoked recently")
            print("   - Python logs are buffered/not showing")
            print("   - Function is running but not producing output")
            print("   - Try triggering an alert and checking again")
            
            # Check for HTTP requests instead
            print("\n🔄 Checking for HTTP invocations...")
            http_filter = f'''
            resource.type="cloud_run_revision"
            AND resource.labels.service_name="alert-handler"
            AND httpRequest.status>=200
            AND timestamp >= "{start_str}"
            '''
            
            http_entries = client.list_entries(filter_=http_filter, order_by=logging.ASCENDING)
            http_count = 0
            
            for entry in http_entries:
                http_count += 1
                timestamp = entry.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')
                if hasattr(entry, 'http_request'):
                    status = entry.http_request.status
                    method = entry.http_request.request_method
                    print(f"[{timestamp}] HTTP {method} {status}")
            
            print(f"📊 Found {http_count} HTTP requests")
        
    except Exception as e:
        print(f"❌ Error reading logs: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = read_function_logs()
    sys.exit(exit_code)
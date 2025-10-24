#!/usr/bin/env python3
"""
Healthy Traffic Generator - Improve SLO Metrics

Sends rapid, successful requests to the API to improve SLO compliance.
This demonstrates SLO recovery after chaos testing.
"""

import requests
import time
from datetime import datetime

API_URL = "https://sre-governance-api-qxt5h5aqiq-uc.a.run.app/api/users"
DURATION_SECONDS = 180  # 3 minutes
REQUEST_INTERVAL = 0.02  # 20ms between requests = 50 req/sec

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🏥 Healthy Traffic Generator")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🎯 Improving SLO metrics")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Target: {API_URL}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Duration: {DURATION_SECONDS} seconds ({DURATION_SECONDS // 60} minutes)")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Expected: Fast responses (~100-200ms)")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Rate: ~10 requests/second")
    print("-" * 70)
    
    start_time = time.time()
    total_requests = 0
    successful_requests = 0
    failed_requests = 0
    total_latency = 0
    
    try:
        while time.time() - start_time < DURATION_SECONDS:
            request_start = time.time()
            
            try:
                response = requests.get(API_URL, timeout=5)
                request_duration = (time.time() - request_start) * 1000  # Convert to ms
                
                total_requests += 1
                total_latency += request_duration
                
                if response.status_code == 200:
                    successful_requests += 1
                    data = response.json()
                    users_count = data.get('count', 0)
                    
                    if total_requests % 50 == 0:  # Log every 50 requests
                        avg_latency = total_latency / total_requests
                        elapsed = time.time() - start_time
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                              f"✅ {total_requests} requests | "
                              f"Avg: {avg_latency:.0f}ms | "
                              f"Success rate: {(successful_requests/total_requests)*100:.1f}% | "
                              f"Elapsed: {elapsed:.0f}s")
                else:
                    failed_requests += 1
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                          f"❌ Request #{total_requests}: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                failed_requests += 1
                total_requests += 1
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                      f"❌ Request #{total_requests} failed: {str(e)[:50]}")
            
            # Sleep to maintain desired rate
            time.sleep(REQUEST_INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️  Test interrupted by user")
    
    # Final summary
    elapsed_time = time.time() - start_time
    avg_latency = total_latency / total_requests if total_requests > 0 else 0
    success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
    
    print("-" * 70)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🏁 Healthy traffic test completed")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Total requests: {total_requests}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Successful: {successful_requests}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed: {failed_requests}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Success rate: {success_rate:.2f}%")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Average latency: {avg_latency:.0f}ms")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Total duration: {elapsed_time:.0f}s")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Request rate: {total_requests/elapsed_time:.1f} req/s")
    print("-" * 70)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📊 Next steps:")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 1. Wait 2-3 minutes for metrics to update")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 2. Check Cloud Monitoring SLOs")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 3. Observe improved error budget")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 4. Note: Full recovery requires 30-day rolling window")

if __name__ == "__main__":
    main()

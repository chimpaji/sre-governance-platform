# Jam with healthy traffic
cd chaos && source venv/bin/activate && python healthy_traffic.py


# Jam with latency traffic
cd chaos && source venv/bin/activate &&  python trigger_latency.py


# Stream alert-handler log 
gcloud beta run services logs tail alert-handler --region=us-central1 --project=uber-clone-api-325213
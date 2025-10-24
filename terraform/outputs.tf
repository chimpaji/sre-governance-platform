output "api_url" {
  description = "Cloud Run service URL"
  value       = google_cloud_run_service.api.status[0].url
}

output "alert_topic" {
  description = "Pub/Sub alert topic"
  value       = google_pubsub_topic.alert_topic.name
}

output "function_name" {
  description = "Cloud Run Function name"
  value       = google_cloudfunctions2_function.alert_handler.name
}

output "slo_availability_id" {
  description = "API Availability SLO ID"
  value       = google_monitoring_slo.api_availability.id
}

output "slo_latency_id" {
  description = "API Latency SLO ID"
  value       = google_monitoring_slo.api_latency.id
}

output "custom_service_id" {
  description = "Custom Service ID for SLOs"
  value       = google_monitoring_custom_service.api_service.service_id
}

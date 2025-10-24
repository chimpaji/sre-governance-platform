terraform {
  required_version = ">= 1.0"
  
  backend "gcs" {
    bucket = "uber-clone-api-325213-tfstate"
    prefix = "terraform/state"
  }
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# CI/CD Pipeline: GitHub Actions automatically deploys changes on push to main

provider "google" {
  project = var.project_id
  region  = var.region
}

# Pub/Sub topic for alerts
resource "google_pubsub_topic" "alert_topic" {
  name = "sre-alerts"
}

# Grant Cloud Monitoring permission to publish to the topic
resource "google_pubsub_topic_iam_member" "monitoring_publisher" {
  topic  = google_pubsub_topic.alert_topic.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:service-557303580741@gcp-sa-monitoring-notification.iam.gserviceaccount.com"
}

# Cloud Run service
resource "google_cloud_run_service" "api" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/${var.service_name}:latest"
        
        ports {
          container_port = 8080
        }

        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }
      }

      # Allow higher concurrency for testing
      container_concurrency = 80
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "10"  # Allow more instances for testing
        "run.googleapis.com/cpu-throttling"  = "false"  # Always allocate CPU (better for latency)
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow unauthenticated access (for demo purposes)
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.api.name
  location = google_cloud_run_service.api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# SLO - API Availability (99.5% target)
resource "google_monitoring_slo" "api_availability" {
  service      = google_monitoring_custom_service.api_service.service_id
  display_name = "API Availability SLO"
  
  goal                = 0.995  # 99.5% availability target
  rolling_period_days = 30
  
  request_based_sli {
    good_total_ratio {
      # Good requests: HTTP 2xx and 3xx responses
      good_service_filter = "metric.type=\"run.googleapis.com/request_count\" resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${var.service_name}\" metric.labels.response_code_class=monitoring.regex.full_match(\"2.*|3.*\")"
      
      # Total requests
      total_service_filter = "metric.type=\"run.googleapis.com/request_count\" resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${var.service_name}\""
    }
  }
}

# SLO - API Latency (95% of requests < 1000ms)
resource "google_monitoring_slo" "api_latency" {
  service      = google_monitoring_custom_service.api_service.service_id
  display_name = "API Latency SLO"
  
  goal                = 0.95  # 95% of requests should be fast
  rolling_period_days = 30
  
  request_based_sli {
    distribution_cut {
      distribution_filter = "metric.type=\"run.googleapis.com/request_latencies\" resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${var.service_name}\""
      
      range {
        min = 0
        max = 1000  # 1000ms threshold
      }
    }
  }
}

# Custom Service for SLOs
resource "google_monitoring_custom_service" "api_service" {
  service_id   = "sre-governance-api-service"
  display_name = "SRE Governance API"
  
  telemetry {
    resource_name = "//run.googleapis.com/projects/${var.project_id}/locations/${var.region}/services/${var.service_name}"
  }
}

# Note: SLO burn rate alerts require specific MQL syntax not fully supported in Terraform
# For production, configure via Console or gcloud CLI
# Example: gcloud alpha monitoring policies create --notification-channels=... \
#   --condition-threshold-value=10 \
#   --condition-threshold-filter='select_slo_burn_rate("projects/.../serviceLevelObjectives/...", "3600s")'

# Cloud Monitoring Alert Policy - High Latency
resource "google_monitoring_alert_policy" "high_latency" {
  display_name = "High API Latency Alert"
  combiner     = "OR"
  
  conditions {
    display_name = "Request latency > 2000ms"
    
    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${var.service_name}\" AND metric.type=\"run.googleapis.com/request_latencies\""
      duration        = "60s"
      comparison      = "COMPARISON_GT"
      threshold_value = 2000
      
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_PERCENTILE_99"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.pubsub.id]

  alert_strategy {
    auto_close = "1800s"  # 30 minutes (GCP minimum)
  }
  
  documentation {
    content   = "API latency exceeded 2000ms threshold. Check application logs and resource utilization."
    mime_type = "text/markdown"
  }
}

# Notification channel - Pub/Sub
resource "google_monitoring_notification_channel" "pubsub" {
  display_name = "SRE Alert Handler"
  type         = "pubsub"
  
  labels = {
    topic = google_pubsub_topic.alert_topic.id
  }
}

# Service Account for Cloud Run API
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-api-sa"
  display_name = "Cloud Run API Service Account"
}

# Service Account for Cloud Function
resource "google_service_account" "function_sa" {
  account_id   = "alert-handler-sa"
  display_name = "Alert Handler Service Account"
}

# Grant permissions to write logs
resource "google_project_iam_member" "function_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

# Grant Pub/Sub subscription permission
resource "google_project_iam_member" "function_pubsub" {
  project = var.project_id
  role    = "roles/pubsub.subscriber"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

# Cloud Run Function (2nd gen) - Alert Handler
resource "google_cloudfunctions2_function" "alert_handler" {
  name     = "alert-handler"
  location = var.region

  build_config {
    runtime     = "python310"
    entry_point = "handle_alert"
    
    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    max_instance_count               = 10   # Limit scaling to prevent runaway costs from alert storms
    min_instance_count               = 0    # Scale to zero when idle
    available_memory                 = "256M"
    timeout_seconds                  = 60
    max_instance_request_concurrency = 10   # Allow concurrent alert processing
    service_account_email            = google_service_account.function_sa.email
    
    environment_variables = {
      PROJECT_ID = var.project_id
    }
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.alert_topic.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

# Storage bucket for Cloud Function source code
resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-functions"
  location = var.region
  
  uniform_bucket_level_access = true
  
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  # Delete old versions after 30 days
    }
  }
}

# Upload Cloud Function code
resource "google_storage_bucket_object" "function_zip" {
  name   = "alert-handler-${filemd5("${path.module}/../functions/alert-handler.zip")}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = "${path.module}/../functions/alert-handler.zip"
}

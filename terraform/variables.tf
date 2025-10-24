variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "uber-clone-api-325213"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Cloud Run service name"
  type        = string
  default     = "sre-governance-api"
}

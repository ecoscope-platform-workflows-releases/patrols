resource "google_cloud_scheduler_job" "warmup_job" {
  name             = "ecoscope-${var.application_name}-warmup-${var.env}"
  description      = "Keeps the ecoscope ${var.application_name} warm by making periodic requests"
  schedule         = "*/10 * * * *"
  time_zone        = "Etc/UTC"
  project          = var.project_id
  region           = var.location
  attempt_deadline = "30s"

  http_target {
    uri         = google_cloud_run_v2_service.default.uri
    http_method = "GET"

    oidc_token {
      service_account_email = google_service_account.default.email
      audience = google_cloud_run_v2_service.default.uri
    }
  }

  depends_on = [
    google_cloud_run_v2_service.default,
    google_cloud_run_domain_mapping.default
  ]
}

resource "google_service_account" "default" {
  account_id = "workflow-patrols"
  project    = var.project_id
}

resource "google_service_account_iam_member" "gha-sa-user" {
  service_account_id = google_service_account.default.id
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:gha-compose@${var.project_id}.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "serviceAgent" {
  project = var.project_id
  role    = "roles/run.serviceAgent"
  member  = "serviceAccount:${google_service_account.default.email}"
}

resource "google_service_account" "default" {
  account_id = startswith(var.env, "dev-preview")? "wf-patrols-${var.env}" : "workflow-patrols-${var.env}"
  project    = var.project_id
}

resource "google_project_iam_member" "serviceAgent" {
  project = var.project_id
  role    = "roles/run.serviceAgent"
  member  = "serviceAccount:${google_service_account.default.email}"
}

resource "google_project_iam_member" "invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.default.email}"
}

# Github Actions SA is able to use cloud run account
resource "google_service_account_iam_member" "gha-sa-user" {
  service_account_id = google_service_account.default.id
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:gha-compose@${var.project_id}.iam.gserviceaccount.com"
}

# Cloud run account can access workflow results bucket
resource "google_storage_bucket_iam_member" "workflow-results-member" {
  bucket = var.workflows_results_bucket
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.default.email}"
}

resource "google_project_iam_member" "pubsub-subscriber-member" {
  project = var.project_id
  role    = "roles/pubsub.subscriber"
  member  = "serviceAccount:${google_service_account.default.email}"
}
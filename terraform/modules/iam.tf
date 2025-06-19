resource "google_service_account" "default" {
  account_id = startswith(var.env, "dev-preview")? "wf-patrols-${var.env}" : "workflow-patrols-${var.env}"
  project    = var.project_id
}

resource "google_service_account" "batch_job" {
  account_id = startswith(var.env, "dev-preview")? "wf-${var.application_short_name}-bj-${var.env}" : "${var.application_name}-bj-${var.env}"
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

resource "google_project_iam_member" "batch_editor" {
  project = var.project_id
  role    = "roles/batch.jobsEditor"
  member  = "serviceAccount:${google_service_account.default.email}"
}

# Workflow SA is able to use Batch SA
resource "google_service_account_iam_member" "batch_sa_user" {
  service_account_id = google_service_account.batch_job.id
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.default.email}"
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

resource "google_project_iam_member" "batch_agent_reporter" {
  project = var.project_id
  role    = "roles/batch.agentReporter"
  member  = "serviceAccount:${google_service_account.batch_job.email}"
}

resource "google_project_iam_member" "batch_log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.batch_job.email}"
}

resource "google_project_iam_member" "batch_storage_viewer" {
  project = var.project_id
  role    = "roles/storage.bucketViewer"
  member  = "serviceAccount:${google_service_account.batch_job.email}"
}

resource "google_project_iam_member" "batch_storage_object_user" {
  project = var.project_id
  role    = "roles/storage.objectUser"
  member  = "serviceAccount:${google_service_account.batch_job.email}"
}

resource "google_project_iam_member" "batch_artifact_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.batch_job.email}"
}
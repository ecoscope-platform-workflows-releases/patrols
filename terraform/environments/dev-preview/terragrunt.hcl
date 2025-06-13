terraform {
  source = "../../modules"
}

remote_state {
  backend = "gcs"
  config = {
    bucket   = "ecoscope-tf-state"
    prefix   = "workflow-patrols/dev-preview-##PREVIEW_NAME/terraform.tfstate"
    project  = "ecoscope-poc-421907"
    location = "us"
  }
}

inputs = {
  image = "" # Override at pipeline level

  project_id                         = "ecoscope-poc-421907"
  env                                = "dev-preview-##PREVIEW_NAME"
  network_name                       = "ecoscope-dev"
  service_url                        = "patrols-preview-##PREVIEW_NAME.dev.ecoscope.io"
  workflows_services_custom_audience = "ecoscope-workflows-services-dev-preview-##PREVIEW_NAME"
  workflows_results_bucket           = "ecoscope-workflows-results-dev-preview-##PREVIEW_NAME"
  max_instance_count                 = "5"
  location                           = "us-west2"
}

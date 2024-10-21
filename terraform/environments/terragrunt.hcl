remote_state {
  backend = "gcs"
  config = {
    bucket   = "ecoscope-tf-state"
    prefix   = "workflow-patrols/${path_relative_to_include()}/terraform.tfstate"
    project  = "ecoscope-poc-421907"
    location = "us"
  }
}

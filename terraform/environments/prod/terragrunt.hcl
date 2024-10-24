include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../modules"
}

inputs = {
  image = "" # Override at pipeline level

  project_id   = "ecoscope-prod"
  env          = "prod"
  network_name = "ecoscope-prod"
  service_url  = "patrols.ecoscope.io"
  workflows_services_custom_audience = "ecoscope-workflows-services-prod"
  workflows_results_bucket           = "ecoscope-workflows-results-prod"
}

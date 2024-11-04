include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../modules"
}

inputs = {
  image = "" # Override at pipeline level

  project_id                         = "ecoscope-stage"
  env                                = "stage"
  network_name                       = "ecoscope-stage"
  service_url                        = "patrols.stage.ecoscope.io"
  workflows_services_custom_audience = "ecoscope-workflows-services-stage"
  workflows_results_bucket           = "ecoscope-workflows-results-stage"
}

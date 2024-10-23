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
}

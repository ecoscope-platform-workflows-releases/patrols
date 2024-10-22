include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../modules"
}

inputs = {
  image = "" # Override at pipeline level

  project_id   = "ecoscope-poc-421907"
  env          = "dev"
  network_name = "ecoscope-dev"
  service_url  = "patrols.dev.ecoscope.io"
}

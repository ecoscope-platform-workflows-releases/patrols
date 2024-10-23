terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.8"
    }
  }
  backend "gcs" {}
  required_version = "~> 1.9.0"
}

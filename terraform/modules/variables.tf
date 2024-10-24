variable "project_id" {
  type        = string
  description = "The GCP project id"
}

variable "env" {
  type        = string
  description = "The environment name"
}

variable "location" {
  type        = string
  description = "The location of the cloud run service"
  default     = "us-west1"
}

variable "ingress" {
  type        = string
  description = "Provides the ingress settings for this Service"
  default     = "INGRESS_TRAFFIC_INTERNAL_ONLY"
}

variable "min_instance_count" {
  type        = number
  description = "Minimum number of serving instances that this resource should have"
  default     = 0
}

variable "max_instance_count" {
  type        = number
  description = "Maximum number of serving instances that this resource should have."
  default     = "2"
}

variable "image" {
  description = "GCR hosted image URL to deploy"
  type        = string
}

# template spec container
# resources
# cpu = (core count * 1000)m
# memory = (size) in Mi/Gi
variable "limits" {
  type        = map(string)
  description = "Resource limits to the container"
  default     = { "cpu" = "1000m", "memory" = "4Gi" }
}

variable "network_name" {
  type        = string
  description = "VPC network name"
}

variable "subnet" {
  type        = string
  default     = "cloud-run"
  description = "The subnet cloud run will use"
}

variable "service_url" {
  type = string
}

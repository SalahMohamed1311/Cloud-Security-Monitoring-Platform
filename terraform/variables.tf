variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "Cloud-Security-Monitoring"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "v2-automation"
}
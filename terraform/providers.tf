provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "Cloud-Security-Monitoring"
      Environment = "v2-automation"
    }
  }
}
variable "region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "eu-west-1"
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket to store the Terraform state"
  type        = string
  default     = "etl-testing-fwk-backend-s3"
}

variable "dynamodb_table_name" {
  description = "The name of the DynamoDB table for state locking"
  type        = string
  default     = "etl-testing-fwk-locks"
}
variable "owner" {
  description = "Owner of the resources, this is your user name (NOT Account ID)"
  type        = string
}

variable "env" {
  description = "Environment (e.g., dev, staging, prod)"
  type        = string
  default = "dev"
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

locals {
  common_tags = merge({
    Owner = var.owner,
    Environment = var.env
  }, var.tags)
}
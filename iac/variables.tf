variable "region" {
  default = "eu-west-1"
}

variable "github_token" {
  description = "GitHub OAuth token"
  type        = string
}

variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket to store the Terraform state"
  type        = string
  default     = "etl-testing-fwk-backend-s3"
}

variable "dynamodb_table_name" {
  description = "The name of the DynamoDB table for state locking"
  type        = string
  default     = "etl-testing-fwk-dynamo"
}


variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "etl-testing-fwk"
}

variable "environment" {
  description = "The environment for the deployment"
  type        = string
  default     = "dev"
}

variable "codepipeline_name" {
  description = "The environment for the deployment"
  type        = string
  default     = "etl-testing-fwk-pipeline"
}
variable "codebuild_role" {
  description = "IAM role ARN for CodeBuild"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}

variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
}

variable "region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "eu-west-1"
}

variable "branch" {
  description = "Git branch that triggered the pipeline"
  type        = string
}

variable "commit" {
  description = "Git commit that triggered the pipeline"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "codebuild_test_name" {
  description = "CodeBuild project name for tests"
  type        = string
  default     = "etl-test"
}

variable "artifact_bucket" {
  description = "S3 bucket name for CodeBuild artifacts"
  type        = string
}

variable "raw_bucket" {
  description = "S3 bucket name for raw data"
  type        = string
}

variable "curated_bucket" {
  description = "S3 bucket name for curated data"
  type        = string
}

variable "clean_bucket" {
  description = "S3 bucket name for clean data"
  type        = string
}

variable "allure_report_bucket" {
  description = "S3 bucket name for Allure reports"
  type        = string
}

variable "sns_topic_arn" {
  description = "ARN of the SNS topic for notifications"
  type        = string
}

variable "owner" {
  description = "Owner or project identifier"
  type        = string
}

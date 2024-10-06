variable "region" {
  default = "eu-west-1"
}
variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}

variable "backend_bucket_name" {
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
variable "branch" {
  description = "The name of the working branch"
  type        = string
  default     = "master"
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

variable "owner" {
  description = "Owner of the resources, this is your user name (NOT Account ID)"
  type        = string
}

variable "env" {
  description = "Environment (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}
variable "etl_codepipeline_bucket" {
  description = "Codepipeline bucket"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

locals {
  common_tags = merge({
    Owner       = var.owner,
    Environment = var.env
  }, var.tags)
}


variable "codebuild_role_name" {
  description = "Code build role name"
  type        = string
  default     = "codebuild-service-role"
}

variable "codebuild_report_permissions_name" {
  description = "Code build permissions"
  type        = string
  default     = "CodeBuildReportPermissions"
}

variable "codepipeline_role_name" {
  description = "Code pipeline role name"
  type        = string
  default     = "codepipeline-service-role"
}
variable "codepipeline_report_permissions_name" {
  description = "Code pipeline permissions"
  type        = string
  default     = "CodePipelineStartBuild"
}

variable "codebuild_name" {
  description = "Code Build Name"
  type        = string
  default     = "e2e-testing-etl-cb"
}
variable "codestar_name" {
  description = "Codestar name, connection to GitHub"
  type        = string
}
variable "codebuild_test_name" {
  description = "CodeBuild project name for tests"
  type        = string
}
variable "allure_bucket" {
  description = "Allure bucket name"
  type        = string
}

variable "great_expectations_bucket" {
  description = "Great Expectation Bucket Name"
  type        = string
}

variable "codepipeline_role" {
  description = "IAM role for CodePipeline"
  type        = string
}
variable "codepipeline_name" {
  description = "IAM role for CodePipeline"
  type        = string
  default     = "etl-pipeline"
}
variable "codebuild_project" {
  description = "CodeBuild project name"
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

variable "github_token" {
  description = "GitHub OAuth token"
  type        = string
}

variable "artifact_bucket" {
  description = "S3 bucket for CodePipeline artifacts"
  type        = string
}

variable "region" {
  default = "eu-west-1"
}

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

variable "artifact_bucket" {
  description = "S3 bucket for CodePipeline artifacts"
  type        = string
}

variable "codestar_arn" {
  description = "Codestar arn for github connection"
  type        = string
}

variable "region" {
  default = "eu-west-1"
}
variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "full_repository" {
  default = ""
}
variable "branch" {
  default = ""
}

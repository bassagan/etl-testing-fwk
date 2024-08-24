variable "region" {
  description = "The AWS region to deploy to"
  type        = string
  default = "eu-west-1"
}
variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}
variable "codebuild_role_name" {
  description = "Code build role name"
  type = string
  default = "codebuild-service-role"
}

variable "codebuild_report_permissions_name" {
  description = "Code build permissions"
  type = string
  default = "CodeBuildReportPermissions"
}
variable "codepipeline_report_permissions_name" {
  description = "Code build permissions"
  type = string
  default = "CodePipelineStartBuild"
}


variable "codepipeline_role_name" {
    description = "Code pipeline role name"
  type = string
  default = "codepipeline-service-role"
}
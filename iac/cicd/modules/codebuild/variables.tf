variable "codebuild_role" {
  description = "IAM role for CodeBuild"
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

variable "region" {
  default = "eu-west-1"
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
variable "region" {
  default = "us-west-2"
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

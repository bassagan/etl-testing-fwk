variable "codestar_name" {
  description = "Codestar name, connection to GitHub"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}
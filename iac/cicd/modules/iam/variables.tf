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
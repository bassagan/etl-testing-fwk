variable "env" {
  description = "Deployment environment"
  type        = string
}

variable "notification_email" {
  description = "Email address for receiving notifications"
  type        = string
}
variable "tags" {
  description = "Tags to apply to the S3 bucket"
  type        = map(string)
}

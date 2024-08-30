variable "notification_mail" {
  description = "Email address for receiving notifications"
  type        = string
}
variable "tags" {
  description = "Tags to apply to the S3 bucket"
  type        = map(string)
}

variable "sns_topic_name" {
  description = "Name of the SNS topic"
  type        = string
}

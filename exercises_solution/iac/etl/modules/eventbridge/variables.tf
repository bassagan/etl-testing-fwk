variable "env" {
  description = "Deployment environment"
  type        = string
}

variable "schedule_expression" {
  description = "Cron expression or rate for triggering the ETL process"
  type        = string
}

variable "raw_clean_function_arn" {
  description = "ARN of the Lambda function to trigger"
  type        = string
}

variable "clean_curated_function_arn" {
  description = "ARN of the Lambda function to trigger"
  type        = string
}

variable "raw_clean_function_name" {
  description = "Name of the Lambda function"
  type        = string
}
variable "clean_curated_function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "tags" {
  description = "Tags to apply to the S3 bucket"
  type        = map(string)
}
variable "raw_clean_event_rule_name" {
  description = "Name for the raw to clean EventBridge rule"
  type        = string
}

variable "clean_curated_event_rule_name" {
  description = "Name for the clean to curated EventBridge rule"
  type        = string
}

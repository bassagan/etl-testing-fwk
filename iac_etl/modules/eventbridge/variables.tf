variable "env" {
  description = "Deployment environment"
  type        = string
}

variable "schedule_expression" {
  description = "Cron expression or rate for triggering the ETL process"
  type        = string
}

variable "lambda_function_arn" {
  description = "ARN of the Lambda function to trigger"
  type        = string
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
}

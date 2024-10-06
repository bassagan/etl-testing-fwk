variable "raw_clean_function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "lambda_role_arn" {
  description = "IAM Role ARN for Lambda execution"
  type        = string
}

variable "s3_bucket" {
  description = "S3 Bucket used by the Lambda function"
  type        = string
}

variable "lambda_package" {
  description = "Path to the Lambda function package"
  type        = string
}

variable "lambda_bucket" {
  description = "S3 Bucket where the Lambda package is stored"
  type        = string
}

variable "tags" {
  description = "Tags to apply to the Lambda function"
  type        = map(string)
  default     = {}
}

variable "lambda_package_data_generator" {
  description = "Path to the zip package for the data generator lambda function"
  type        = string
}

variable "data_generator_function_name" {
  description = "Name of the data generator lambda function"
  type        = string
  default     = "data-generator-function"
}

variable "clean_curated_function_name" {
  description = "Name of the data generator lambda function"
  type        = string
}

variable "cloudwatch_event_rule_name" {
  description = "Name of the cloudwatch event rule"
  type        = string
}

variable "lambda_role_name" {
  description = "Name of the IAM role for Lambda functions"
  type        = string
}
variable "notification_mail" {
  description = "Email address to send notifications to"
  type        = string
}
variable "raw_bucket" {
  description = "Name of the raw bucket"
  type        = string
}
variable "clean_bucket" {
  description = "Name of the clean bucket"
  type        = string
}
variable "curated_bucket" {
  description = "Name of the curated bucket"
  type        = string
}

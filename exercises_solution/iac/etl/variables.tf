variable "region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "eu-west-1"
}

variable "env" {
  description = "The environment (e.g., dev, prod)"
  type        = string
  default     = "dev"
}

variable "lambda_code_bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}
variable "raw_bucket_name" {
  description = "The name of the S3 bucket for raw source ingestion"
  type        = string
}
variable "raw_clean_function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "sns_topic_name" {
  description = "The name of the SNS topic"
  type        = string
}

variable "schedule_expression" {
  description = "The schedule expression for EventBridge rule"
  type        = string
}

# Include Lambda module for ETL processing
variable "lambda_package" {
  default = ""
}

# Include SNS module for notifications
variable "notification_mail" {
  default = ""
}

variable "athena_db_name" {
  description = "Name of the Athena database"
  type        = string
  default     = "etl_db"
}

variable "clean_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "curated_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
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

variable "etl_workgorup_name" {
  description = "Athena workgroup"
  default     = "etl-workgroup"
}

variable "clean_curated_function_name" {
  description = "Name of the data generator lambda function"
  type        = string
  default     = "clean_curated_function"
}

variable "owner" {
  description = "The owner of the resources"
  type        = string
}

variable "tags" {
  description = "Additional tags to apply to the resources"
  type        = map(string)
  default     = {}
}

locals {
  common_tags = merge({
    Owner = var.owner
  }, var.tags)
}
variable "cloudwatch_event_rule_name" {
  description = "Name of the cloudwatch event rule"
  type        = string
}

variable "raw_clean_event_rule_name" {
  description = "Name for the raw to clean EventBridge rule"
  type        = string
}

variable "clean_curated_event_rule_name" {
  description = "Name for the clean to curated EventBridge rule"
  type        = string
}

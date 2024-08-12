variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "env" {
  description = "Deployment environment"
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

variable "lambda_layer_s3_key" {
  description = "The S3 key for the Lambda layer ZIP file"
  default     = "lambda_layer.zip"
}
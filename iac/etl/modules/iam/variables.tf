# Variables used in this IAM main.tf
variable "lambda_bucket" {
  description = "S3 bucket where Lambda packages are stored"
  type        = string
}

variable "raw_bucket_name" {
  description = "S3 bucket where raw data is stored"
  type        = string
}

variable "clean_bucket_name" {
  description = "S3 bucket where cleaned data is stored"
  type        = string
}

variable "curated_bucket_name" {
  description = "S3 bucket where cleaned data is stored"
  type        = string
}

variable "athena_result_bucket_name" {
  description = "S3 bucket for storing Athena query results"
  type        = string
}

variable "query_input_bucket_name" {
  description = "S3 bucket containing data for Athena queries"
  type        = string
}


variable "region" {
  description = "AWS region"
  type        = string
}

variable "env" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
}
variable "owner" {
  description = "The owner of the resources"
  type        = string
}

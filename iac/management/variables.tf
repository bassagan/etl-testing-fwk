variable "account_count" {
  description = "Number of AWS accounts to create"
  type        = number
  default     = 1
}
variable "s3_bucket_name" {
  description = "Name of the S3 bucket where the CSV file will be stored"
  type        = string
  default = "s3-user-management-dev"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "user-management"
}

variable "owner" {
  description = "Owner of the resources, this is your user name (NOT Account ID)"
  type        = string
  default     = "paula-bassaganas"
}

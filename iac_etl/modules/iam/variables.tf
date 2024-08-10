variable "env" {
  description = "Environment name"
  type        = string
}

variable "tags" {
  description = "Tags to be applied to resources"
  type        = map(string)
}
variable "lambda_bucket" {
  description = "The name of the S3 bucket for Lambda functions"
  type        = string
}
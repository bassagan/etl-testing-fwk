variable "lambda_code_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}
variable "raw_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "clean_bucket_name" {
  description = "Name of the S3 bucket for clean layer"
  type        = string
}

variable "curated_bucket_name" {
  description = "Name of the S3 bucket for curated layer"
  type        = string
}

variable "enable_versioning" {
  description = "Enable versioning on the bucket"
  type        = bool
  default     = true
}

variable "enable_lifecycle_rules" {
  description = "Enable lifecycle rules on the bucket"
  type        = bool
  default     = true
}

variable "noncurrent_version_expiration_days" {
  description = "Number of days to retain non-current versions"
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags to apply to the S3 bucket"
  type        = map(string)
  default     = {}
}

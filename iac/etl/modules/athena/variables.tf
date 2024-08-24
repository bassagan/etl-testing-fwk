variable "athena_db_name" {
  description = "Name of the Athena database"
  type        = string
  default     = "etl_db"
}
variable "clean_bucket_name" {
  description = "Name of the Athena bucket for clean layer"
  type        = string

}
variable "curated_bucket_name" {
  description = "Name of the Athena bucket for curated layer"
  type        = string

}
variable "tags" {
  description = "Tags to apply to the S3 bucket"
  type        = map(string)
}

variable "etl_workgorup_name" {
  description = "Athena workgroup"
  default = "etl-workgroup"
}
variable "table_name" {
  description = "The name of the DynamoDB table"
  type        = string
}
variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}
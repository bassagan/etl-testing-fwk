variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "etl_codepipeline_bucket" {
  description = "Codepipeline bucket"
  type        = string
}

variable "owner" {
  description = "The owner of the resources"
  type        = string
}
variable "allure_bucket" {
  description = "The bucket for the allure reports"
  type        = string
}

variable "great_expectations_bucket" {
  description = "The bucket for great expectations reports"
  type        = string
}

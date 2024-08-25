variable "owner" {
  type = string
}

variable "resource_arns" {
  type = list(string)
}

variable "tags" {
  type = map(string)
}
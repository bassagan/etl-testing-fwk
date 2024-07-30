#Terraform backend infrastructure to store terraform state

provider "aws" {
  region = var.region
}

module "s3_backend" {
  source      = "../modules/s3"
  bucket_name = var.s3_bucket_name
}

module "dynamodb_backend" {
  source      = "../modules/dynamodb"
  table_name  = var.dynamodb_table_name
}

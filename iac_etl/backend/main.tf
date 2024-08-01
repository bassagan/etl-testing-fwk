#Terraform backend infrastructure to store terraform state

provider "aws" {
  region = var.region
}

module "s3_backend" {
  source      = "../modules/s3"
  bucket_name = var.s3_bucket_name
  env = "dev"
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}

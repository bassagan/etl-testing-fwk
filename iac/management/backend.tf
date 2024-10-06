terraform {
  backend "s3" {
    bucket         = "paula-admin-tf-backend-bucket"
    key            = "etl-testing-fwk/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "paula-admin-tf-backend-dynamodb"
  }
}
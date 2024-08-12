terraform {
  backend "s3" {
    bucket         = "etl-backend-s3-dev"
    key            = "etl-backend/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "etl-locks"
  }
}
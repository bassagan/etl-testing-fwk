terraform {
  backend "s3" {
    bucket         = "etl-testing-fwk-backend-s3"
    key            = "etl-testing-fwk/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "etl-testing-fwk-locks"
  }
}
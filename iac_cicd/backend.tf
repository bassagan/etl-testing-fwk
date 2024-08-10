terraform {
  backend "s3" {
    bucket         = "etl-testing-terraform-state-bucket"
    key            = "etl-testing-fwk/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "etl-testing-fwk-locks"
  }
}
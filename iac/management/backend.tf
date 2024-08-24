terraform {
  backend "s3" {
    bucket         = "paula-bassaganas-manage-users-bucket"
    key            = "etl-testing-fwk/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "paula-bassaganas-manage-users-dynamodb"
  }
}
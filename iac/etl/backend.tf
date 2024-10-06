terraform {
  backend "s3" {

    bucket = "paula_admin-tf-backend-bucket"
    key            = "etl-testing-fwk/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "paula_admin-tf-backend-dynamodb"

  }
}

















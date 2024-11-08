terraform {
  backend "s3" {
    bucket = "conference-user-b25c6fae-tf-backend-bucket"
    key            = "cicd/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "conference-user-b25c6fae-tf-backend-dynamodb"
  }
}


















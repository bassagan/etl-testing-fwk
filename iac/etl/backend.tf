terraform {
  backend "s3" {

    bucket = "conference-user-85c3f2ab-tf-backend-bucket"
    key            = "etl/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "conference-user-85c3f2ab-tf-backend-dynamodb"

  }
}

















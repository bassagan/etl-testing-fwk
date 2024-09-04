terraform {
  backend "s3" {

    bucket = "conference-user-4550cc71-tf-backend-bucket"
    key            = "etl/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "conference-user-4550cc71-tf-backend-dynamodb"

  }
}

















terraform {
  backend "s3" {


    bucket         = "conference-user-df720b8a-tf-backend-bucket"
    key            = "cicd/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "conference-user-df720b8a-tf-backend-dynamodb"

  }
}

















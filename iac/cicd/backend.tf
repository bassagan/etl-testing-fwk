terraform {
  backend "s3" {
    bucket         = "your_bucket_name"
    key            = "etl/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "your_dynamo_db_name"
  }
}

















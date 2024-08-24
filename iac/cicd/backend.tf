terraform {
  backend "s3" {
    bucket = "owner_bucket_name_to_be_replaced_by_script"
    key            = "etl-testing-fwk/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "owner_dynamoname_to_be_replaced_by_script"
  }
}
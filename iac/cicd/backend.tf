terraform {
  backend "s3" {
    bucket = "bucket_name_replaced_by_script"
    key            = "etl-testing-fwk/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "dynamo_name_replaced_by_script"  }
}
provider "aws" {
  region = var.region
}

# Include S3 bucket module for ETL
module "s3" {
  source = "./modules/s3"

  bucket_name = var.bucket_name
  raw_bucket_name = var.raw_bucket_name
  clean_bucket_name = var.clean_bucket_name
  env         = var.env

  tags = var.tags
}

# Include IAM role for Lambda
module "iam" {
  source = "./modules/iam"

  env    = var.env
  tags   = var.tags
}

# Include Lambda module for ETL processing
module "lambda" {
  source = "./modules/lambda"

  function_name   = var.lambda_name
  s3_bucket       = module.s3.bucket_name
  lambda_package  = var.lambda_package
  lambda_bucket   = var.bucket_name
  lambda_role_arn = module.iam.lambda_role_arn
  env             = var.env

  tags = var.tags
    depends_on = [
    module.s3
  ]

}

# Include SNS module for notifications
module "sns" {
  source = "./modules/sns"
  notification_email = var.notification_mail
  env            = var.env

}

# Include EventBridge module for scheduling
module "eventbridge" {
  source               = "./modules/eventbridge"

  lambda_function_arn  = module.lambda.lambda_function_arn
  lambda_function_name = module.lambda.lambda_function_name
  schedule_expression  = var.schedule_expression
  env                  = var.env
  depends_on = [
    module.lambda
  ]
}

module "athena" {
  source = "./modules/athena"

  athena_db_name = var.athena_db_name

  bucket_name  = module.s3.clean_bucket_name

  depends_on = [
    module.s3
  ]
}
variable "access_key" {
  default = ""
}
variable "secret_key" {
  default = ""
}
provider "aws" {
  region = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.64.0"  # Update to the version you need
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.6.2"  # Update to the version you need
    }
  }
}

# Include S3 bucket module for ETL
module "s3" {
  source = "./modules/s3"
  providers = {
    aws = aws
  }
  owner = var.owner
  bucket_name         = var.bucket_name
  raw_bucket_name     = var.raw_bucket_name
  clean_bucket_name   = var.clean_bucket_name
  curated_bucket_name = var.curated_bucket_name
  env                 = var.env

  tags = local.common_tags
}

# Include IAM role for Lambda
module "iam" {
  providers = {
    aws = aws
  }
  source = "./modules/iam"

  env                      = var.env
  lambda_bucket            = module.s3.bucket_name
  clean_bucket_name        = module.s3.clean_bucket_name
  curated_bucket_name      = module.s3.curated_bucket_name
  raw_bucket_name          = module.s3.raw_bucket_name
  athena_result_bucket_name = module.s3.clean_bucket_name
  query_input_bucket_name  = module.s3.clean_bucket_name
  region                   = var.region
  depends_on               = [module.s3]
  owner = var.owner
  tags = local.common_tags
}

# Include Lambda module for ETL processing
module "lambda" {
  source = "./modules/lambda"

  function_name                  = var.lambda_name
  s3_bucket                      = module.s3.bucket_name
  lambda_package                 = var.lambda_package
  lambda_bucket                  = module.s3.bucket_name
  clean_curated_function_name    = var.clean_curated_function_name
  data_generator_function_name   = var.data_generator_function_name
  lambda_role_arn                = module.iam.lambda_role_arn
  env                            = var.env
  lambda_package_data_generator  = var.lambda_package_data_generator
  owner = var.owner
  depends_on                     = [module.s3]

  tags = local.common_tags
}

# Include SNS module for notifications
module "sns" {
  source               = "./modules/sns"
  notification_email   = var.notification_mail
  env                  = var.env
  owner = var.owner
  tags = local.common_tags
}

# Include EventBridge module for scheduling
module "eventbridge" {
  source = "./modules/eventbridge"

  raw_clean_function_arn      = module.lambda.raw_clean_lambda_function_arn
  clean_curated_function_arn  = module.lambda.clean_curated_lambda_function_arn
  raw_clean_function_name     = module.lambda.raw_clean_lambda_function_name
  clean_curated_function_name = module.lambda.clean_curated_lambda_function_name
  schedule_expression         = var.schedule_expression
  env                         = var.env
  depends_on                  = [module.lambda]

  tags = local.common_tags
}

module "athena" {
  source = "./modules/athena"

  athena_db_name       = var.athena_db_name
  clean_bucket_name    = module.s3.clean_bucket_name
  curated_bucket_name  = module.s3.curated_bucket_name
  depends_on           = [module.s3]
  owner = var.owner
  tags = local.common_tags
}


output "sns_topic_arn" {
  value = module.sns.sns_topic_arn
}

output "raw_bucket_name" {
  value = module.s3.raw_bucket_name
}
output "clean_bucket_name" {
  value = module.s3.clean_bucket_name
}
output "curated_bucket_name" {
  value = module.s3.curated_bucket_name
}
output "lambda_clean_curated_function_name" {
  value = module.lambda.clean_curated_lambda_function_name
}
output "lambda_raw_clean_function_name" {
  value = module.lambda.raw_clean_lambda_function_name
}

output "data_generator_function_name" {
  value = module.lambda.data_generator_function_name
}

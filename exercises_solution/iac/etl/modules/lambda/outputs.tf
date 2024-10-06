output "raw_clean_lambda_function_arn" {
  value = aws_lambda_function.raw_clean_function.arn
}

output "raw_clean_lambda_function_name" {
  value = aws_lambda_function.raw_clean_function.function_name
}

output "clean_curated_lambda_function_arn" {
  value = aws_lambda_function.clean_curated_function.arn
}

output "clean_curated_lambda_function_name" {
  value = aws_lambda_function.clean_curated_function.function_name
}

output "data_generator_lambda_function_arn" {
  value = aws_lambda_function.data_generator_function.arn
}

output "data_generator_function_name" {
  value = aws_lambda_function.data_generator_function.function_name
}

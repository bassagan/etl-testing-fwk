output "lambda_function_arn" {
  value = aws_lambda_function.etl_function.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.etl_function.function_name
}


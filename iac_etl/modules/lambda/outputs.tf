output "lambda_function_arn" {
  value = aws_lambda_function.etl_function.arn
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_execution_role.arn
}

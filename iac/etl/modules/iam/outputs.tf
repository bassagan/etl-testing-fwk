output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}


output "lambda_role_name" {
  description = "Name of the Lambda IAM role"
  value       = aws_iam_role.lambda_role.name
}



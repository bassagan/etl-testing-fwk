output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}
output "codepipeline_role_arn" {
  description = "ARN of the CodePipeline IAM role"
  value       = aws_iam_role.codepipeline_role.arn
}

output "codebuild_role_arn" {
  description = "ARN of the CodeBuild IAM role"
  value       = aws_iam_role.codebuild_role.arn
}

output "cloudwatch_role_arn" {
  description = "ARN of the CloudWatch IAM role"
  value       = aws_iam_role.cloudwatch_role.arn
}

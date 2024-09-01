output "codebuild_project_name" {
  value = aws_codebuild_project.etl_build.name
}

output "codebuild_project_arn" {
  value = aws_codebuild_project.etl_build.arn
}

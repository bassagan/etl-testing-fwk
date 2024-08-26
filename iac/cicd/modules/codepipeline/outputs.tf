output "codepipeline_name" {
  value = aws_codepipeline.etl_pipeline.name
}
output "codepipeline_arn" {
  value = aws_codepipeline.etl_pipeline.arn
}

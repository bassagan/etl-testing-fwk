output "codepipeline_bucket" {
  value = aws_s3_bucket.codepipeline_bucket.bucket
}
output "codepipeline_bucket_arn" {
  value = aws_s3_bucket.codepipeline_bucket.arn
}


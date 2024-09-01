output "codepipeline_bucket" {
  value = aws_s3_bucket.codepipeline_bucket.bucket
}
output "codepipeline_bucket_arn" {
  value = aws_s3_bucket.codepipeline_bucket.arn
}

output "allure_bucket_website_endpoint" {
  value       = "http://${aws_s3_bucket.allure_bucket.bucket}.s3-website-eu-west-1.amazonaws.com"
  description = "The website endpoint URL for the Allure reports bucket"
}

output "allure_bucket_arn" {
  value = aws_s3_bucket.allure_bucket.arn
}

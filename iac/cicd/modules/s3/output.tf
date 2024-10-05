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
output "raw_bucket" {
  value = aws_s3_bucket.raw_bucket.id
}

output "curated_bucket" {
  value = aws_s3_bucket.curated_bucket.id
}

output "clean_bucket" {
  value = aws_s3_bucket.clean_bucket.id
}

output "allure_report_bucket" {
  value = aws_s3_bucket.allure_report_bucket.id
}

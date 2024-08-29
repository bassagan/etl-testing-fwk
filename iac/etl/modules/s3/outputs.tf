output "lambda_code_bucket_arn" {
  value = aws_s3_bucket.lambda_code_bucket.arn
}

output "lambda_code_bucket_name" {
  value = aws_s3_bucket.lambda_code_bucket.bucket
}

output "clean_bucket_name" {
  value = aws_s3_bucket.clean_bucket.bucket
}


output "raw_bucket_name" {
  value = aws_s3_bucket.raw_bucket.bucket
}

output "curated_bucket_name" {
  value = aws_s3_bucket.curated_bucket.bucket
}

output "clean_bucket_arn" {
  value = aws_s3_bucket.clean_bucket.arn
}

output "raw_bucket_arn" {
  value = aws_s3_bucket.raw_bucket.arn
}

output "curated_bucket_arn" {
  value = aws_s3_bucket.curated_bucket.arn
}

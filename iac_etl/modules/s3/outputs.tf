output "bucket_arn" {
  value = aws_s3_bucket.etl_bucket.arn
}

output "bucket_name" {
  value = aws_s3_bucket.etl_bucket.bucket
}

output "clean_bucket_name" {
  value = aws_s3_bucket.clean_bucket.bucket
}


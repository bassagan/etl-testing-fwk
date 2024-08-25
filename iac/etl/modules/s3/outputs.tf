output "bucket_arn" {
  value = aws_s3_bucket.etl_bucket.arn
}

output "bucket_name" {
  value = aws_s3_bucket.etl_bucket.bucket
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
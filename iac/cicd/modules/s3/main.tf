resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket        = var.etl_codepipeline_bucket
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket" "allure_bucket" {
  bucket        = var.allure_bucket
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_website_configuration" "allure_bucket_website" {
  bucket = aws_s3_bucket.allure_bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "allure_bucket_public_access" {
  bucket = aws_s3_bucket.allure_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "allure_bucket_policy" {
  bucket = aws_s3_bucket.allure_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.allure_bucket.arn}/*"
      },
    ]
  })
}

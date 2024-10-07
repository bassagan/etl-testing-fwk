resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket        = var.etl_codepipeline_bucket
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_versioning" "codepipeline_bucket_versioning" {
  bucket = aws_s3_bucket.codepipeline_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "allure_bucket" {
  bucket        = var.allure_bucket
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_ownership_controls" "allure_bucket_ownership" {
  bucket = aws_s3_bucket.allure_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "allure_bucket_public_access" {
  bucket = aws_s3_bucket.allure_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "allure_bucket_acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.allure_bucket_ownership,
    aws_s3_bucket_public_access_block.allure_bucket_public_access,
  ]

  bucket = aws_s3_bucket.allure_bucket.id
  acl    = "public-read"
}

resource "aws_s3_bucket_website_configuration" "allure_bucket_website" {
  bucket = aws_s3_bucket.allure_bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "allure_bucket_policy" {
  depends_on = [aws_s3_bucket_public_access_block.allure_bucket_public_access]

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

resource "aws_s3_bucket" "great_expectations_bucket" {
  bucket        = var.great_expectations_bucket
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_ownership_controls" "great_expectations_bucket_ownership" {
  bucket = aws_s3_bucket.great_expectations_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "great_expectations_bucket_public_access" {
  bucket = aws_s3_bucket.great_expectations_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "great_expectations_bucket_acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.great_expectations_bucket_ownership,
    aws_s3_bucket_public_access_block.great_expectations_bucket_public_access,
  ]

  bucket = aws_s3_bucket.great_expectations_bucket.id
  acl    = "public-read"
}

resource "aws_s3_bucket_website_configuration" "great_expectations_bucket_website" {
  bucket = aws_s3_bucket.great_expectations_bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "great_expectations_bucket_policy" {
  depends_on = [aws_s3_bucket_public_access_block.great_expectations_bucket_public_access]

  bucket = aws_s3_bucket.great_expectations_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.great_expectations_bucket.arn}/*"
      },
    ]
  })
}

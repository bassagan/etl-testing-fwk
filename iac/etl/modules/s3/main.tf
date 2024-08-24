terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.64.0"  # Update this to match the provider version in your root module
    }
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket" "etl_bucket" {
  bucket = "${var.owner}-${var.bucket_name}-${random_string.bucket_suffix.result}"
  tags = var.tags
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.etl_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
  
}

resource "aws_s3_bucket_lifecycle_configuration" "lifecycle" {
  bucket = aws_s3_bucket.etl_bucket.id

  rule {
    id     = "expire-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}
resource "aws_s3_bucket" "raw_bucket" {
  bucket = "${var.raw_bucket_name}-${random_string.bucket_suffix.result}"
  tags = var.tags
}

resource "aws_s3_bucket" "clean_bucket" {
  bucket = "${var.clean_bucket_name}-${random_string.bucket_suffix.result}"
  tags = var.tags

}
resource "aws_s3_bucket" "curated_bucket" {
  bucket = "${var.curated_bucket_name}-${random_string.bucket_suffix.result}"
  tags = var.tags

}

resource "aws_s3_bucket_policy" "clean_bucket_policy" {
  bucket = aws_s3_bucket.clean_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "athena.amazonaws.com"
        },
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.clean_bucket.id}",
          "arn:aws:s3:::${aws_s3_bucket.clean_bucket.id}/*"
        ]
      }
    ]
  })
}

resource "aws_s3_bucket_policy" "curated_bucket_policy" {
  bucket = aws_s3_bucket.curated_bucket.id
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "athena.amazonaws.com"
        },
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.curated_bucket.id}",
          "arn:aws:s3:::${aws_s3_bucket.curated_bucket.id}/*"
        ]
      }
    ]
  })
  
}
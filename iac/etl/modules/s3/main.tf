terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.64.0" # Update this to match the provider version in your root module
    }
  }
}


resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket        = var.lambda_code_bucket_name
  tags          = var.tags
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  versioning_configuration {
    status = "Enabled"
  }

}

resource "aws_s3_bucket_lifecycle_configuration" "lifecycle" {
  bucket = aws_s3_bucket.lambda_code_bucket.id

  rule {
    id     = "expire-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}
resource "aws_s3_bucket" "raw_bucket" {
  bucket        = var.raw_bucket_name
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket" "clean_bucket" {
  bucket        = var.clean_bucket_name
  force_destroy = true
  tags          = var.tags

}
resource "aws_s3_bucket" "curated_bucket" {
  bucket        = var.curated_bucket_name
  force_destroy = true
  tags          = var.tags

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

# Upload ZIP Files to S3
resource "aws_s3_object" "upload_lambda_generator" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key    = "lambda_generator_package.zip"
  source = "${path.root}/../../lambda_packages/lambda_generator_package.zip" # Adjust path to your ZIP file
  acl    = "private"
}

resource "aws_s3_object" "upload_lambda_raw_clean" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key    = "lambda_raw_clean.zip"
  source = "${path.root}/../../lambda_packages/lambda_raw_clean.zip" # Adjust path to your ZIP file
  acl    = "private"
}

resource "aws_s3_object" "upload_lambda_clean_curated" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key    = "lambda_clean_curated.zip"
  source = "${path.root}/../../lambda_packages/lambda_clean_curated.zip" # Adjust path to your ZIP file
  acl    = "private"
}

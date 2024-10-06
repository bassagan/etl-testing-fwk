terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.64.0" # Update this to match the provider version in your root module
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "${var.owner}-lambda-execution-role-${var.env}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "LambdaS3AccessPolicy-${var.env}"
  role = aws_iam_role.lambda_role.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${var.lambda_bucket}",       # Specific Lambda bucket
          "arn:aws:s3:::${var.lambda_bucket}/*",     # All objects in Lambda bucket
          "arn:aws:s3:::${var.raw_bucket_name}",     # Specific Raw data bucket
          "arn:aws:s3:::${var.raw_bucket_name}/*",   # All objects in Raw data bucket
          "arn:aws:s3:::${var.clean_bucket_name}",   # Specific Clean data bucket
          "arn:aws:s3:::${var.clean_bucket_name}/*", # All objects in Clean data bucket
          "arn:aws:s3:::${var.curated_bucket_name}", # Specific Curated data bucket
          "arn:aws:s3:::${var.curated_bucket_name}/*"
        ]
      }
    ]
  })
}



resource "aws_iam_role" "athena_role" {
  name = "${var.owner}-athena-execution-role-${var.env}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "athena.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "athena_s3_policy" {
  name = "AthenaS3AccessPolicy-${var.env}"
  role = aws_iam_role.athena_role.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${var.query_input_bucket_name}",  # Input bucket for Athena queries
          "arn:aws:s3:::${var.query_input_bucket_name}/*" # All objects in input bucket for Athena queries
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject"
        ],
        Resource = [
          "arn:aws:s3:::${var.athena_result_bucket_name}",  # Athena result bucket
          "arn:aws:s3:::${var.athena_result_bucket_name}/*" # All objects in Athena result bucket
        ]
      }
    ]
  })
}

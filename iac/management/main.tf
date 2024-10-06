provider "aws" {
  region = "eu-west-1"
}


# IAM Role for Lambda Execution
resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role-dev"

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

  tags = {
    "Environment" = "Conference"
  }
}

# IAM Policy for Lambda to manage IAM users and keys
resource "aws_iam_role_policy" "lambda_iam_policy" {
  name   = "LambdaIAMManagementPolicy"
  role   = aws_iam_role.lambda_role.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "iam:CreateUser",
          "iam:DeleteUser",
          "iam:GetUser",
          "iam:CreateAccessKey",
          "iam:DeleteAccessKey",
          "iam:ListUsers",
          "iam:ListAccessKeys",
          "iam:PutUserPolicy",
          "iam:AttachUserPolicy",
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "iam:*",
          "tag:*",
          "resource-groups:*"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = "iam:PassRole",
        Resource = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/*"
      }
    ]
  })
}

# Data source to get the current AWS account ID
data "aws_caller_identity" "current" {}

# S3 Bucket to store the User Management zip
resource "aws_s3_bucket" "lambda_user_management_bucket" {
  bucket = var.s3_bucket_name  # Bucket name passed via variable

  tags = {
    "Environment" = "Conference"
  }
}

resource "aws_s3_object" "upload_lambda_user_management" {
  bucket = aws_s3_bucket.lambda_user_management_bucket.bucket
  key    = "lambda_user_management.zip"
  source = "${path.root}/../../lambda_packages/lambda_user_management.zip"  # Adjust path to your ZIP file
  acl    = "private"
}

resource "aws_iam_policy" "service_user_restricted_policy" {
  name        = "ServiceUserRestrictedPolicy"
  description = "Policy to restrict users to their own resources"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:*",
          "lambda:*",
          "athena:*",
          "codebuild:*",
          "codepipeline:*",
          "dynamodb:*",
          "events:*",
          "sns:*",
          "codestar:*",
          "codestar-connections:*",
          "iam:*",
          "glue:*"
        ],
        "Resource": "*",
      }
    ]
  })
}

resource "aws_iam_policy" "user_restricted_policy" {
  name        = "UserRestrictedPolicy"
  description = "Policy to restrict users to their own resources"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
     {
			"Effect": "Allow",
			"Action": [
				"s3:List*",
				"athena:List*",
				"lambda:List*",
				"codebuild:List*",
				"codepipeline:List*",
				"dynamodb:ListTables",
				"events:List*",
				"sns:List*",
				"codestar:List*",
                "glue:*"
			],
			"Resource": "*"
		},
      {
        "Effect": "Allow",
        "Action": [
          "dynamodb:*"
        ],
        "Resource": "*",
      },
      {
        "Effect": "Allow",
        "Action": [
          "s3:*",
          "lambda:*",
          "athena:*",
          "codebuild:*",
          "codepipeline:*",
          "dynamodb:*",
          "events:*",
          "sns:*",
          "codestar:*"
        ],
        "Resource": "*",
        "Condition": {
          "StringEquals": {
            "aws:ResourceTag/Owner": "$${aws:username}"
          }
        }
      },
      {
        "Effect": "Allow",
        "Action": "iam:PassRole",
        "Resource": "*",
        "Condition": {
          "StringEqualsIfExists": {
            "aws:ResourceTag/Owner": "$${aws:username}"
          }
        }
      }
    ]
  })
}


# Lambda Function to manage users and generate CSV
resource "aws_lambda_function" "user_management_lambda" {
  function_name    = "lambda-user-management-dev"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_role.arn
  s3_bucket        = aws_s3_bucket.lambda_user_management_bucket.bucket
  s3_key           = "lambda_user_management.zip"

  memory_size = 256
  timeout = 60

  tags = {
    "Environment" = "Conference"
  }

  depends_on = [
    aws_iam_role.lambda_role,  # Ensure IAM role is created before the Lambda function
    aws_s3_bucket.lambda_user_management_bucket
  ]
}

resource "aws_lambda_function_url" "create_user_url" {
  function_name      = aws_lambda_function.user_management_lambda.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["GET"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }
}


output "lambda_function_arn" {
  value = aws_lambda_function.user_management_lambda.arn
}

output "s3_bucket_name" {
  value = aws_s3_bucket.lambda_user_management_bucket.bucket
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.lambda_user_management_bucket.arn
}


# Output the Lambda Function URL
output "lambda_function_url" {
  value = aws_lambda_function_url.create_user_url.function_url
}
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.64.0" # Update this to match the provider version in your root module
    }
  }
}

resource "aws_lambda_function" "raw_clean_function" {
  function_name = var.raw_clean_function_name
  handler       = "etl_function.lambda_handler"
  runtime       = "python3.9"
  role          = var.lambda_role_arn
  s3_bucket     = var.lambda_bucket
  s3_key        = "lambda_raw_clean.zip"

  memory_size = 256
  timeout     = 60
  environment {
    variables = {
      S3_BUCKET     = var.s3_bucket
      SOURCE_BUCKET = var.raw_bucket
      TARGET_BUCKET = var.clean_bucket
      SNS_TOPIC_ARN = aws_sns_topic.pipeline_notification.arn
    }
  }
  layers     = ["arn:aws:lambda:eu-west-1:336392948345:layer:AWSSDKPandas-Python39:24"]
  tags       = var.tags
  depends_on = [var.lambda_bucket, aws_iam_role_policy.lambda_sns_publish]
}

resource "aws_lambda_function_event_invoke_config" "raw-clean-notifications" {
  function_name = var.raw_clean_function_name

  destination_config {
    on_failure {
      destination = aws_sns_topic.pipeline_notification.arn
    }

    on_success {
      destination = aws_sns_topic.pipeline_notification.arn
    }
  }
  depends_on = [aws_lambda_function.raw_clean_function  ]
}

resource "aws_lambda_function" "clean_curated_function" {
  function_name = var.clean_curated_function_name
  handler       = "clean_curated_function.lambda_handler"
  runtime       = "python3.9"
  role          = var.lambda_role_arn
  s3_bucket     = var.lambda_bucket
  s3_key        = "lambda_clean_curated.zip"

  memory_size = 256
  timeout     = 60
  environment {
    variables = {
      S3_BUCKET     = var.s3_bucket
      SOURCE_BUCKET = var.clean_bucket
      TARGET_BUCKET = var.curated_bucket
    }
  }
  layers     = ["arn:aws:lambda:eu-west-1:336392948345:layer:AWSSDKPandas-Python39:24"]
  tags       = var.tags
  depends_on = [var.lambda_bucket]
}
resource "aws_lambda_function" "data_generator_function" {
  function_name = var.data_generator_function_name
  handler       = "sample_data_generator.lambda_handler"
  runtime       = "python3.9"
  role          = var.lambda_role_arn
  s3_bucket     = var.lambda_bucket
  s3_key        = "lambda_generator_package.zip"
  memory_size   = 256
  timeout       = 60
  environment {
    variables = {
      S3_BUCKET = var.lambda_bucket
    }
  }

  tags       = var.tags
  depends_on = [var.lambda_bucket, aws_iam_role_policy.lambda_s3_read]
}


// Add SNS trigger for clean_curated_function
resource "aws_sns_topic_subscription" "clean_curated_sns_subscription" {
  topic_arn = aws_sns_topic.pipeline_notification.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.clean_curated_function.arn
}

// Update SNS Topic Policy to allow Lambda to subscribe
resource "aws_sns_topic_policy" "default" {
  arn = aws_sns_topic.pipeline_notification.arn
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowLambdaToPublishAndSubscribe"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action   = ["SNS:Publish", "SNS:Subscribe"]
        Resource = aws_sns_topic.pipeline_notification.arn
      }
    ]
  })
}

// Add permission for SNS to invoke clean_curated_function
resource "aws_lambda_permission" "allow_sns_invoke_clean_curated" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.clean_curated_function.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.pipeline_notification.arn
}

# IAM policy for Lambda to publish to SNS
resource "aws_iam_role_policy" "lambda_sns_publish" {
  name = "lambda_sns_publish"
  role = var.lambda_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.pipeline_notification.arn
      }
    ]
  })
}

# SNS Topic for pipeline notifications
resource "aws_sns_topic" "pipeline_notification" {
  name = "${var.raw_clean_function_name}-notifications"
  tags = var.tags
}

// Add this resource to grant S3 read permissions to the Lambda function
resource "aws_iam_role_policy" "lambda_s3_read" {
  name = "lambda_s3_read"
  role = var.lambda_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetObject"
        ]
        Resource = [
          "arn:aws:s3:::${var.lambda_bucket}",
          "arn:aws:s3:::${var.lambda_bucket}/*"
        ]
      }
    ]
  })
}

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
      SNS_TOPIC_ARN = aws_sns_topic.pipeline_notification.arn
    }
  }
  layers     = ["arn:aws:lambda:eu-west-1:336392948345:layer:AWSSDKPandas-Python39:24"]
  tags       = var.tags
  depends_on = [var.lambda_bucket, aws_iam_role_policy.lambda_sns_publish]
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
      S3_BUCKET = var.s3_bucket
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
  depends_on = [var.lambda_bucket]
}
# CloudWatch EventBridge rule for success of raw_clean_function
resource "aws_cloudwatch_event_rule" "raw_clean_success_rule" {
  name = var.cloudwatch_event_rule_name
  event_pattern = jsonencode({
    "source" : ["aws.lambda"],
    "detail-type" : ["Lambda Function Invocation Result - Success"],
    "detail" : {
      "responseElements" : {
        "functionArn" : [aws_lambda_function.raw_clean_function.arn]
      }
    }
  })
  tags = var.tags
}

# EventBridge target to trigger the clean_curated_function
resource "aws_cloudwatch_event_target" "clean_curated_target" {
  rule      = aws_cloudwatch_event_rule.raw_clean_success_rule.name
  target_id = "clean-curated-target"
  arn       = aws_lambda_function.clean_curated_function.arn

}

# Grant permission for EventBridge to invoke clean_curated_function
resource "aws_lambda_permission" "allow_eventbridge_invoke_clean_curated" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.clean_curated_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.raw_clean_success_rule.arn

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

# SNS Topic Policy
resource "aws_sns_topic_policy" "default" {
  arn = aws_sns_topic.pipeline_notification.arn
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowLambdaToPublish"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action   = "SNS:Publish"
        Resource = aws_sns_topic.pipeline_notification.arn
      }
    ]
  })
}

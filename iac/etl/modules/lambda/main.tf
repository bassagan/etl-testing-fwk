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
      S3_BUCKET = var.s3_bucket
    }
  }
  tags       = var.tags
  depends_on = [var.lambda_bucket]
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

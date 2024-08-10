resource "aws_lambda_layer_version" "etl_layer" {
  filename         = "s3://etl-tutorial-bucket-dev/lambda_layer.zip"
  layer_name       = "etl_layer"
  compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_function" "etl_function" {
  function_name    = "${var.function_name}-${var.env}"
  handler          = "etl_function.lambda_handler"
  runtime          = "python3.9"
  role             = var.lambda_role_arn
  s3_bucket        = var.lambda_bucket
  s3_key           = "lambda_etl.zip"
  memory_size = 256
  layers = [
    aws_lambda_layer_version.etl_layer.arn,
  ]
  environment {
    variables = {
      S3_BUCKET = var.s3_bucket
    }
  }

  tags = var.tags
  depends_on = [var.lambda_bucket]
}


resource "aws_lambda_function" "data_generator_function" {
  function_name    = "${var.data_generator_function_name}-${var.env}"
  handler          = "sample_data_generator.lambda_handler"
  runtime          = "python3.9"
  role             = var.lambda_role_arn
  s3_bucket        = var.lambda_bucket
  s3_key           = "lambda_generator_package.zip"
  memory_size = 256
  environment {
    variables = {
      S3_BUCKET = var.lambda_bucket
    }
  }

  tags = var.tags
  depends_on = [var.lambda_bucket]
}



resource "aws_cloudwatch_event_rule" "invoke_data_generator" {
  name                = "invoke-data-generator"
  schedule_expression = "rate(1 hour)"  # Adjust the schedule as needed
}

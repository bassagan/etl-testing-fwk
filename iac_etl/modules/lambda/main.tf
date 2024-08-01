resource "aws_lambda_function" "etl_function" {
  function_name    = "${var.function_name}-${var.env}"
  handler          = "etl_function.lambda_handler"
  runtime          = "python3.8"
  role             = var.lambda_role_arn
  s3_bucket        = var.lambda_bucket
  s3_key           = aws_s3_object.lambda_zip.key
  source_code_hash = filebase64sha256(var.lambda_package)

  environment {
    variables = {
      S3_BUCKET = var.s3_bucket
    }
  }

  tags = var.tags
  depends_on = [var.lambda_bucket]
}

resource "aws_s3_object" "lambda_zip" {
  bucket = var.lambda_bucket
  key    = "${var.function_name}.zip"
  source = var.lambda_package
  etag   = filemd5(var.lambda_package)
  depends_on = [var.lambda_bucket]
}

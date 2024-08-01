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
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda-execution-role-${var.env}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_access" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_s3_object" "lambda_zip" {
  bucket = var.lambda_bucket
  key    = "${var.function_name}.zip"
  source = var.lambda_package
  etag   = filemd5(var.lambda_package)
}

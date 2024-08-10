resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role-${var.env}"

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

resource "aws_iam_policy_attachment" "lambda_policy_attachment" {
  name       = "lambda-basic-execution-role-attachment-${var.env}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  roles      = [aws_iam_role.lambda_role.name]
}

# Add this new resource for S3 access
resource "aws_iam_role_policy" "lambda_s3_policy" {
  name   = "LambdaS3AccessPolicy-${var.env}"
  role   = aws_iam_role.lambda_role.name

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
        Resource = "*"
      }
    ]
  })
}

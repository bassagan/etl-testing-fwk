resource "aws_iam_policy" "owner_full_access" {
  name        = "owner-full-access-cicd-${var.owner}"
  description = "Full access policy for the owner user to manage generated resources"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iam:*",
          "codebuild:*",
          "codepipeline:*",
          "codestar-connections:*",
          "s3:*",
        ]
        Resource = var.resource_arns
      },
      {
        "Action" : [
          "resource-groups:*",
          "tag:*",
          "cloudformation:*"
        ],
        "Effect" : "Allow",
        "Resource" : "*"
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_user_policy_attachment" "owner_full_access_attachment" {
  user       = var.owner
  policy_arn = aws_iam_policy.owner_full_access.arn
}

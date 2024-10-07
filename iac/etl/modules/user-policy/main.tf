# Add this at the top of the file
data "aws_caller_identity" "current" {}

resource "aws_iam_policy" "owner_full_access" {
  name        = "owner-full-access-etl-${var.owner}"
  description = "Full access policy for the owner user to manage generated resources"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iam:*",
          "s3:*",
          "lambda:*",
          "athena:*",
          "dynamodb:*",
          "events:*",
          "sns:*",
          "glue:*",
          "resource-groups:*",
          "tag:*",
          "cloudwatch:*",
          "logs:*",
        ]
        Resource = concat(
          var.resource_arns,
          ["arn:aws:athena:*:${data.aws_caller_identity.current.account_id}:workgroup/${var.owner}-*"]
        )
      },
      {
        "Action" : [
          	"resource-groups:*",
            "tag:*",
            "cloudformation:*",
            "athena:GetWorkGroup",
            "athena:ListWorkGroups",
            "athena:StartQueryExecution",
            "athena:GetQueryExecution",
            "glue:GetDatabases",
            "glue:GetDatabase",
            "glue:GetTables",
            "glue:GetTable",
            "glue:GetPartitions"
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

region       = "eu-west-1"
github_token = "YOUR_GITHUB_TOKEN"
github_owner = "bassagan"
github_repo  = "etl-testing-fwk"
s3_bucket_name = "etl-testing-fwk-backend-s3"
dynamodb_table_name = "etl-testing-fwk-dynamo"
codebuild_role = "arn:aws:iam::123456789012:role/codebuild-service-role"
codepipeline_name = "{branch_name}-{repo_name}-codepipeline-{env}"
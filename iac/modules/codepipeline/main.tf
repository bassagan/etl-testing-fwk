resource "aws_codepipeline" "etl_pipeline" {
  name     = "etl-pipeline"
  role_arn = var.codepipeline_role

  artifact_store {
    location = var.artifact_bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        Owner      = var.github_owner
        Repo       = var.github_repo
        Branch     = "master"
        OAuthToken = var.github_token
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      version          = "1"

     configuration = {
        ProjectName = var.codebuild_project
      }
    }
  }
}
# Webhook to trigger pipeline on GitHub commits
resource "aws_codepipeline_webhook" "github_webhook" {
  name            = "github-webhook"
  target_action   = "Source"
  target_pipeline = aws_codepipeline.etl_pipeline.name
  authentication  = "GITHUB_HMAC"

  authentication_configuration {
    secret_token = var.github_token
  }

  filter {
    json_path    = "$.ref"
    match_equals = "refs/heads/master"
  }

  filter {
    json_path    = "$.ref"
    match_equals = "refs/heads/develop"
  }

  filter {
    json_path    = "$.ref"
    match_equals = "refs/heads/feature/*"
  }
  filter {
    json_path    = "$.ref"
    match_equals = "refs/heads/training/*"
  }
}

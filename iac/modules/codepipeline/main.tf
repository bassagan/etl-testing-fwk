resource "aws_codepipeline" "etl_pipeline" {
  name     = var.codepipeline_name
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
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        ConnectionArn    = "arn:aws:codeconnections:eu-west-1:087559609246:connection/b0171203-62d8-4ebb-964d-907be5d5a213"
        FullRepositoryId = "${var.github_owner}/${var.github_repo}"
        BranchName       = "feature/initial-pytest-config"
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

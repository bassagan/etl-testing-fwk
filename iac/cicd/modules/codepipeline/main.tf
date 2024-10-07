resource "aws_codepipeline" "etl_pipeline" {
  name     = var.codepipeline_name
  role_arn = var.codepipeline_role
  tags     = var.tags
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
      provider         = "S3"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        S3Bucket    = var.artifact_bucket
        S3ObjectKey = "${var.branch}/repo.zip"
      }
    }
  }

  stage {
    name = "BuildAndTest"

    action {
      name             = "BuildAndTest"
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

provider "aws" {
  region = var.region
}

module "iam" {
  source = "./modules/iam"
}

module "codebuild" {
  source          = "./modules/codebuild"
  codebuild_role  = module.iam.codebuild_role_arn
  github_repo     = var.github_repo
  github_owner    = var.github_owner
  github_token    = var.github_token
}

module "codepipeline" {
  source             = "./modules/codepipeline"
  codepipeline_role  = module.iam.codepipeline_role_arn
  codebuild_project  = module.codebuild.codebuild_project_name
  github_repo        = var.github_repo
  github_owner       = var.github_owner
  github_token       = var.github_token
  artifact_bucket    = aws_s3_bucket.codepipeline_bucket.bucket
}

resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = "etl-codepipeline-bucket"
}


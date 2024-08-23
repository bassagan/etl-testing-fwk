provider "aws" {
  region = var.region
}
terraform {
  required_providers {
    random = {
      source = "hashicorp/random"
    }
  }
}

module "iam" {
  source = "./modules/iam"

  tags = local.common_tags
}

module "codebuild" {
  source         = "./modules/codebuild"
  codebuild_role = module.iam.codebuild_role_arn
  github_repo    = var.github_repo
  github_owner   = var.github_owner
  github_token   = var.github_token
  branch         = "" # Will be set by CodePipeline
  commit         = "" # Will be set by CodePipeline

  tags = local.common_tags
}


module "s3" {
  source         = "./modules/s3"
  etl_codepipeline_bucket = var.etl_codepipeline_bucket
  tags = local.common_tags
  owner = var.owner
}


module "codepipeline" {
  source            = "./modules/codepipeline"
  codepipeline_role = module.iam.codepipeline_role_arn
  codebuild_project = module.codebuild.codebuild_project_name
  github_repo       = var.github_repo
  github_owner      = var.github_owner
  github_token      = var.github_token
  artifact_bucket   = module.s3.codepipeline_bucket
  codepipeline_name = var.codepipeline_name

  tags = local.common_tags
}

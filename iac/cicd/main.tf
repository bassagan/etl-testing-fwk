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

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}



module "iam" {
  source                                = "./modules/iam"
  codebuild_role_name                   = "${var.codebuild_role_name}-${random_string.bucket_suffix.result}"
  codebuild_report_permissions_name     = "${var.codebuild_report_permissions_name}-${random_string.bucket_suffix.result}"
  codepipeline_role_name                = "${var.codepipeline_role_name}-${random_string.bucket_suffix.result}"
  codepipeline_report_permissions_name  = "${var.codepipeline_report_permissions_name}-${random_string.bucket_suffix.result}"
  tags = local.common_tags
}

module "codebuild" {
  source         = "./modules/codebuild"
  codebuild_role = module.iam.codebuild_role_arn
  codebuild_name = "${var.codebuild_name}-${random_string.bucket_suffix.result}"
  github_repo    = var.github_repo
  github_owner   = var.github_owner
  branch         = "" # Will be set by CodePipeline
  commit         = "" # Will be set by CodePipeline

  tags = local.common_tags
}
module "codestar" {
  source          = "./modules/codestar"
  codestar_name   = "${var.owner}-${var.codestar_name}-${random_string.bucket_suffix.result}"


  tags = local.common_tags
}
module "s3" {
  source         = "./modules/s3"
  etl_codepipeline_bucket = "${var.owner}-${var.etl_codepipeline_bucket}-${random_string.bucket_suffix.result}"
  tags = local.common_tags
  owner = var.owner
}

module "codestar" {
  source          = "./modules/codestar"
  codestar_name   = "${var.owner}-${var.codestar_name}"


  tags = local.common_tags
}

module "codepipeline" {
  source            = "./modules/codepipeline"
  codepipeline_role = module.iam.codepipeline_role_arn
  codebuild_project = module.codebuild.codebuild_project_name
  artifact_bucket   = module.s3.codepipeline_bucket
  full_repository   = "${var.github_owner}/${var.github_repo}"
  branch            = var.branch
  codestar_arn      = module.codestar.codestar_arn
  codepipeline_name = "${var.branch}-${var.codepipeline_name}-${var.environment}"
  depends_on                     = [module.codestar]
  tags = local.common_tags
}

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
  source                               = "./modules/iam"
  codebuild_role_name                  = "${var.codebuild_role_name}-${random_string.bucket_suffix.result}"
  codebuild_report_permissions_name    = "${var.codebuild_report_permissions_name}-${random_string.bucket_suffix.result}"
  codepipeline_role_name               = "${var.codepipeline_role_name}-${random_string.bucket_suffix.result}"
  codepipeline_report_permissions_name = "${var.codepipeline_report_permissions_name}-${random_string.bucket_suffix.result}"
  tags                                 = local.common_tags
}

module "codebuild" {
  source               = "./modules/codebuild"
  codebuild_role       = module.iam.codebuild_role_arn
  artifact_bucket      = module.s3.codepipeline_bucket
  allure_report_bucket = module.s3.allure_bucket
  gx_report_bucket     = module.s3.gx_bucket_name
  github_repo          = var.github_repo
  github_owner         = var.github_owner
  branch               = var.branch
  commit               = "" # Will be set by CodePipeline
  tags                 = local.common_tags
  owner                = var.owner
}

module "codepipeline" {
  source                 = "./modules/codepipeline"
  codepipeline_name      = "cicd-${var.owner}-cp-${replace(var.branch, "/", "-")}"
  codepipeline_role      = module.iam.codepipeline_role_arn
  codebuild_project      = module.codebuild.codebuild_project_name
  artifact_bucket        = module.s3.codepipeline_bucket
  full_repository        = "${var.github_owner}/${var.github_repo}"
  branch                 = replace(var.branch, "/", "-")
  codestar_arn           = module.codestar.codestar_arn
  depends_on             = [module.codestar]
  tags                   = local.common_tags
}

module "s3" {
  source                    = "./modules/s3"
  etl_codepipeline_bucket   = "${var.etl_codepipeline_bucket}-${var.owner}-${random_string.bucket_suffix.result}"
  allure_bucket             = "${var.allure_bucket}-${var.owner}-${random_string.bucket_suffix.result}"
  great_expectations_bucket = "${var.great_expectations_bucket}-${var.owner}-${random_string.bucket_suffix.result}"
  tags                      = local.common_tags
  owner                     = var.owner
}

module "codestar" {
  source        = "./modules/codestar"
  codestar_name = "${var.codestar_name}${var.owner}"


  tags = local.common_tags
}


module "user-policy" {
  source = "./modules/user-policy"

  owner = var.owner
  resource_arns = [
    module.iam.codebuild_role_arn,
    module.iam.codepipeline_role_arn,
    module.codebuild.codebuild_project_arn,
    module.codestar.codestar_arn,
    module.s3.codepipeline_bucket_arn,
    "${module.s3.codepipeline_bucket_arn}/*",
    module.codepipeline.codepipeline_arn,
    module.s3.allure_bucket_arn,
    module.s3.gx_bucket_arn,
    "${module.s3.gx_bucket_arn}/*"
  ]
  tags = local.common_tags

  depends_on = [
    module.iam,
    module.codebuild,
    module.codestar,
    module.s3,
    module.codepipeline
  ]
}

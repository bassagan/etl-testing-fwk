resource "aws_codebuild_project" "etl_build" {
  name         = "${var.codebuild_test_name}-build"
  service_role = var.codebuild_role

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:4.0"
    type         = "LINUX_CONTAINER"

    environment_variable {
      name  = "AWS_DEFAULT_REGION"
      value = var.region
    }

    environment_variable {
      name  = "ALLURE_RESULTS_DIR"
      value = "/tmp/allure-results"
    }


    environment_variable {
      name  = "LAMBDA_CLEAN_CURATED_FUNCTION_NAME"
      value = "clean_curated_lmb-${var.owner}"
    }

    environment_variable {
      name  = "LAMBDA_RAW_CLEAN_FUNCTION_NAME"
      value = "raw_clean_lmb-${var.owner}"
    }

    environment_variable {
      name  = "DATA_GENERATOR_FUNCTION_NAME"
      value = "data_generator-${var.owner}"
    }

    environment_variable {
      name  = "ALLURE_REPORT_BUCKET"
      value = var.allure_report_bucket
    }

    environment_variable {
      name  = "GX_REPORT_BUCKET"
      value = var.gx_report_bucket
    }
  }

  source {
    type      = "S3"
    location  = "${var.artifact_bucket}/${replace(var.branch, "/", "-")}/repo.zip"
    buildspec = "buildspec.yml"
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "/aws/codebuild/${var.github_repo}"
      stream_name = "build-log"
      status      = "ENABLED"
    }
  }
  tags = var.tags
}

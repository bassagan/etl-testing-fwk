resource "aws_codebuild_project" "etl_build" {
  name         = var.codebuild_test_name
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
      name  = "GIT_BRANCH"
      value = var.branch
    }

    environment_variable {
      name  = "GIT_COMMIT"
      value = var.commit
    }
    environment_variable {
      name  = "ALLURE_RESULTS_DIR"
      value = "/tmp/allure-results"
    }
  }

  source {
    type            = "GITHUB"
    location        = "https://github.com/${var.github_owner}/${var.github_repo}.git"
    buildspec       = "buildspec.yml"
    git_clone_depth = 1
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

// Add a new CodeBuild project for running tests
resource "aws_codebuild_project" "etl_test" {
  name         = var.codebuild_test_name
  service_role = var.codebuild_role

  artifacts {
    type = "CODEPIPELINE"
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
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "buildspec-test.yml"
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "/aws/codebuild/${var.github_repo}-test"
      stream_name = "test-log"
      status      = "ENABLED"
    }
  }
  tags = var.tags
}

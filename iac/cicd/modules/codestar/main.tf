resource "aws_codestarconnections_connection" "github_connection" {
  name          = var.codestar_name
  provider_type = "GitHub"
  tags = var.tags
}
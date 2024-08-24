resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = var.etl_codepipeline_bucket
  force_destroy = true
  tags = var.tags
}
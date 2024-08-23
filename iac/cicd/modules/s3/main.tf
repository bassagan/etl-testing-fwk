
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = "${var.owner}-${var.etl_codepipeline_bucket}-${random_string.bucket_suffix.result}"
  tags = var.tags
}
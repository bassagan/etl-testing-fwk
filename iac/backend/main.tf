#Terraform backend infrastructure to store terraform state
provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = lower(replace("${var.owner}-${var.s3_bucket_name}", " ", "-"))
  tags = var.tags
}

resource "aws_s3_bucket_lifecycle_configuration" "terraform_state_lifecycle" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    id     = "expire-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}
resource "aws_dynamodb_table" "terraform_locks" {
  name         = lower(replace("${var.owner}-manage-users-dynamodb", " ", "-"))
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}


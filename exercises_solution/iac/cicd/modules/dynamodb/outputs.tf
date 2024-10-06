output "table_name" {
  value = aws_dynamodb_table.terraform_locks.name
}
output "table_arn" {
  value = aws_dynamodb_table.terraform_locks.arn
}

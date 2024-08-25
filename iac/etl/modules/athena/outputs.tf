output "athena_database_arn" {
  description = "ARN of the Athena database"
  value       = aws_athena_database.etl_db.arn
}

output "athena_workgroup_arn" {
  description = "ARN of the Athena workgroup"
  value       = aws_athena_workgroup.etl_workgroup.arn
}

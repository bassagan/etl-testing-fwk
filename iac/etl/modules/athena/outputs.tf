output "athena_workgroup_arn" {
  description = "ARN of the Athena workgroup"
  value       = aws_athena_workgroup.etl_workgroup.arn
}

output "athena_table_patients_arn" {
  description = "ARN of the Athena table patients"
  value       = aws_glue_catalog_table.patients_table.arn
}
output "athena_table_visits_arn" {
  description = "ARN of the Athena table visits"
  value       = aws_glue_catalog_table.visits_table.arn
}

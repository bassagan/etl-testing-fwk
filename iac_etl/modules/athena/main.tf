resource "aws_athena_database" "etl_db" {
  name   = var.athena_db_name
  bucket = var.clean_bucket_name


}

resource "aws_athena_workgroup" "etl_workgroup" {
  name        = "etl-workgroup-dev"
  state       = "ENABLED"
  description = "Workgroup for ETL queries"

  configuration {
    enforce_workgroup_configuration = true

    result_configuration {
      output_location = "s3://${var.clean_bucket_name}/athena-results/"
    }
  }
}

resource "aws_athena_named_query" "etl_query" {
  name      = "etl-sample-query"
  database  = aws_athena_database.etl_db.name
  query     = "SELECT * FROM your_table LIMIT 10;"
  workgroup = aws_athena_workgroup.etl_workgroup.name

  depends_on = [
    aws_athena_database.etl_db,
    aws_athena_workgroup.etl_workgroup
  ]
}

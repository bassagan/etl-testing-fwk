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

resource "aws_glue_catalog_table" "etl_table" {
  name          = "etl_table"
  database_name = aws_athena_database.etl_db.name
  table_type    = "EXTERNAL_TABLE"

  storage_descriptor {
    location          = "s3://${var.clean_bucket_name}/curated_data"
    input_format      = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format     = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    compressed        = false
    number_of_buckets = -1

    columns {
      name = "patient_id"
      type = "string"
    }

    columns {
      name = "name"
      type = "string"
    }

    columns {
      name = "date_of_birth"
      type = "string"
    }

    columns {
      name = "visit_date"
      type = "string"
    }

    columns {
      name = "diagnosis"
      type = "string"
    }

    columns {
      name = "medication"
      type = "string"
    }

    columns {
      name = "doctor"
      type = "string"
    }

    columns {
      name = "address"
      type = "string"
    }



    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }
  }

}

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

resource "aws_glue_catalog_table" "patients_table" {
  name          = "patients"
  database_name = aws_athena_database.etl_db.name
  table_type    = "EXTERNAL_TABLE"

  storage_descriptor {
    location          = "s3://${var.clean_bucket_name}/cleaned/patients/"
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
      type = "timestamp"
    }

    columns {
      name = "address"
      type = "string"
    }

    columns {
      name = "phone_number"
      type = "string"
    }

    columns {
      name = "email"
      type = "string"
    }

    columns {
      name = "insurance_provider"
      type = "string"
    }

    columns {
      name = "policy_number"
      type = "string"
    }

    columns {
      name = "policy_valid_till"
      type = "timestamp"
    }

    columns {
      name = "record_created_at"
      type = "timestamp"
    }

    columns {
      name = "record_updated_at"
      type = "timestamp"
    }

    columns {
      name = "start_date"
      type = "timestamp"
    }

    columns {
      name = "end_date"
      type = "timestamp"
    }

    columns {
      name = "is_current"
      type = "boolean"
    }

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }
  }

  partition_keys {
    name = "year_of_birth"
    type = "int"
  }

  partition_keys {
    name = "month_of_birth"
    type = "int"
  }
}


resource "aws_glue_catalog_table" "visits_table" {
  name          = "visits"
  database_name = aws_athena_database.etl_db.name
  table_type    = "EXTERNAL_TABLE"

  storage_descriptor {
    location          = "s3://${var.clean_bucket_name}/cleaned/visits/"
    input_format      = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format     = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    compressed        = false
    number_of_buckets = -1

    columns {
      name = "appointment_id"
      type = "string"
    }

    columns {
      name = "patient_id"
      type = "string"
    }

    columns {
      name = "appointment_date"
      type = "timestamp"
    }

    columns {
      name = "doctor"
      type = "string"
    }

    columns {
      name = "department"
      type = "string"
    }

    columns {
      name = "purpose"
      type = "string"
    }

    columns {
      name = "status"
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
      name = "notes"
      type = "string"
    }

    columns {
      name = "record_created_at"
      type = "timestamp"
    }

    columns {
      name = "record_updated_at"
      type = "timestamp"
    }

    columns {
      name = "start_date"
      type = "timestamp"
    }

    columns {
      name = "end_date"
      type = "timestamp"
    }

    columns {
      name = "is_current"
      type = "boolean"
    }

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }
  }

  partition_keys {
    name = "year"
    type = "int"
  }

  partition_keys {
    name = "month"
    type = "int"
  }
}


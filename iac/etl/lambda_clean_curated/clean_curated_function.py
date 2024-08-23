import boto3
import json
import logging
import pandas as pd
import io
from curated_patient_transform import CuratedPatientTransform
from curated_visit_transform import CuratedVisitTransform
from data_writer import DataWriter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    clean_bucket = event.get('clean_bucket', 'clean-etl-bucket-dev')
    curated_bucket = event.get('curated_bucket', 'curated-etl-bucket-dev')

    # Load visits data
    df_visits = load_parquet_from_s3(s3_client, clean_bucket, 'cleaned/visits/latest/visits_latest.parquet')

    # Transform visits data
    visit_transformer = CuratedVisitTransform()
    df_curated_visits = visit_transformer.transform(df_visits)

    # Load patients data
    df_patients = load_parquet_from_s3(s3_client, clean_bucket, 'cleaned/patients/latest/patients_latest.parquet')

    # Transform patients data with visits summary
    patient_transformer = CuratedPatientTransform()
    df_curated_patients = patient_transformer.transform(df_patients, df_curated_visits)

    # Write the curated data back to S3, partitioned by necessary columns
    data_writer = DataWriter(s3_client, curated_bucket)
    data_writer.write_partitioned(df_curated_patients, 'curated/patients', ['year_of_birth', 'month_of_birth'])
    data_writer.write_partitioned(df_curated_visits, 'curated/visits', ['visit_year', 'visit_month'])

    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "Curated patients and visits data processing complete.",
            "patients_count": len(df_curated_patients),
            "visits_count": len(df_curated_visits)
        })
    }

def load_parquet_from_s3(s3_client, bucket, key):
    """Reads a Parquet file from S3 and returns a DataFrame."""
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read()  # Read the entire file into memory
    return pd.read_parquet(io.BytesIO(data))  # Use BytesIO to create a file-like object

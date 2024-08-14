import boto3
from datetime import datetime
import pandas as pd
import json
import logging
import io

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    # Define the source and destination buckets
    clean_bucket = event.get('clean_bucket', 'clean-etl-bucket-dev')
    curated_bucket = event.get('curated_bucket', 'curated-etl-bucket-dev')

    # Define the schema for the clean visits data
    visits_schema = {
        'appointment_id': 'string',
        'patient_id': 'string',
        'appointment_date': 'datetime64[ns]',
        'doctor': 'string',
        'department': 'string',
        'purpose': 'string',
        'status': 'string',
        'diagnosis': 'string',
        'medication': 'string',
        'notes': 'string',
        'record_created_at': 'datetime64[ns]',
        'record_updated_at': 'datetime64[ns]'
    }

    # Read the clean visits data from S3
    clean_visits_key = 'cleaned/visits/visits_latest.parquet'
    try:
        df_visits = read_parquet_from_s3(s3_client, clean_bucket, clean_visits_key, visits_schema)
    except s3_client.exceptions.NoSuchKey:
        logger.error(f"The key {clean_visits_key} was not found in the bucket {clean_bucket}.")
        return {
            'statusCode': 404,
            'body': json.dumps(f"Key {clean_visits_key} not found in bucket {clean_bucket}.")
        }

    # Transform data
    df_curated_visits = transform_visits_data(df_visits)

    # Store curated data to S3
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    curated_visits_key = f'curated/visits/visits_{timestamp}.parquet'
    write_parquet_to_s3(s3_client, df_curated_visits, curated_bucket, curated_visits_key)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "Curated visits data processing complete.",
            "visits_count": len(df_curated_visits)
        })
    }


def read_parquet_from_s3(s3_client, bucket, key, schema):
    """Reads a Parquet file from S3 and returns a DataFrame."""
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    data = pd.read_parquet(obj['Body'])
    return data.astype(schema)


def write_parquet_to_s3(s3_client, df, bucket, key):
    """Writes a DataFrame as a Parquet file to S3."""
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    s3_client.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())


def transform_visits_data(df_visits):
    """Transforms the clean visit data into the curated visit model."""

    # Derive visit month and year from appointment_date
    df_visits['visit_month'] = df_visits['appointment_date'].dt.month
    df_visits['visit_year'] = df_visits['appointment_date'].dt.year

    # Standardize doctor name, department, and other fields if necessary
    df_visits['doctor_name'] = df_visits['doctor'].str.title()
    df_visits['department'] = df_visits['department'].str.title()

    # Return the curated DataFrame
    return df_visits


if __name__ == "__main__":
    lambda_handler(None, None)

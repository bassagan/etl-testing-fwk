import json
import pandas as pd
import boto3
import io
from pyarrow import parquet as pq
from datetime import datetime


def read_json_from_s3(s3_client, bucket_name, key):
    """Read a JSON file from S3 and return as a DataFrame."""
    obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    data = json.loads(obj['Body'].read().decode('utf-8'))
    # Normalize JSON data to handle nested dictionaries
    df = pd.json_normalize(data)
    return df


def write_parquet_to_s3(s3_client, df, bucket_name, key):
    """Write a DataFrame as a Parquet file to S3."""
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False, engine='pyarrow')
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=buffer.getvalue())


def lambda_handler(event, context):
    """AWS Lambda handler."""
    s3_client = boto3.client('s3')

    source_bucket = event.get('source_bucket', 'raw-etl-bucket-dev')
    destination_bucket = event.get('destination_bucket', 'clean-etl-bucket-dev')
    source_key_prefix = event.get('source_key_prefix', 'source_a/')
    destination_key_prefix = event.get('destination_key_prefix', 'curated_data/')

    # List objects in the source S3 bucket
    response = s3_client.list_objects_v2(Bucket=source_bucket, Prefix=source_key_prefix)

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps("No files found in the specified S3 prefix.")
        }

    # Process each file
    data_frames = []
    for obj in response['Contents']:
        df = read_json_from_s3(s3_client, source_bucket, obj['Key'])
        data_frames.append(df)

    # Concatenate all data into a single DataFrame
    if data_frames:
        df_combined = pd.concat(data_frames, ignore_index=True)

        # Remove duplicates
        df_cleaned = df_combined.drop_duplicates()

        # Generate the destination key
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        destination_key = f"{destination_key_prefix}curated_data_{timestamp}.parquet"

        # Write the cleaned DataFrame to Parquet and upload to S3
        write_parquet_to_s3(s3_client, df_cleaned, destination_bucket, destination_key)

        return {
            'statusCode': 200,
            'body': json.dumps(f"Data successfully transformed and saved to {destination_key}")
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps("No data files found to process.")
        }


if __name__ == "__main__":
    lambda_handler(None, None)

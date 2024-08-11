import json
import pandas as pd
import boto3
import io

class DataReader:
    def __init__(self, s3_client, bucket_name):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def read_json_from_s3(self, key):
        """Read a JSON file from S3 and return as a DataFrame."""
        obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
        data = json.loads(obj['Body'].read().decode('utf-8'))
        df = pd.json_normalize(data)  # Normalize JSON data to handle nested dictionaries
        return df

    def list_files(self, prefix):
        """List files in an S3 bucket under a specific prefix."""
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        if 'Contents' in response:
            return [content['Key'] for content in response['Contents']]
        return []
    def read_parquet_from_s3(self, key):
        """Read a Parquet file from S3 and return as a DataFrame."""
        obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
        df = pd.read_parquet(io.BytesIO(obj['Body'].read()))
        return df

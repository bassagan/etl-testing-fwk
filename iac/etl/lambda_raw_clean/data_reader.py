import json
import pandas as pd
import boto3
import io
import re

class DataReader:
    def __init__(self, s3_client, bucket_name, last_processed_timestamp_key):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.last_processed_timestamp_key = last_processed_timestamp_key
        self.last_processed_timestamp = self.load_last_processed_timestamp()

    def load_last_processed_timestamp(self):
        """Load the last processed timestamp from S3."""
        try:
            obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.last_processed_timestamp_key)
            return obj['Body'].read().decode('utf-8')
        except self.s3_client.exceptions.NoSuchKey:
            return '00000000000000'  # Use a very old timestamp if no record is found

    def update_last_processed_timestamp(self, timestamp):
        """Update the last processed timestamp in S3."""
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=self.last_processed_timestamp_key,
            Body=timestamp
        )

    def list_unprocessed_files(self, prefix):
        """List files in S3 with a timestamp later than the last processed timestamp."""
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        if 'Contents' in response:
            all_files = [content['Key'] for content in response['Contents']]
            unprocessed_files = []
            for file in all_files:
                match = re.search(r'(\d{14})', file)
                if match:
                    file_timestamp = match.group(1)
                    if file_timestamp > self.last_processed_timestamp:
                        unprocessed_files.append(file)
            return unprocessed_files
        return []
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

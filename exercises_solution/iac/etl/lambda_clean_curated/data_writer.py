import io
import boto3
import pandas as pd

class DataWriter:
    def __init__(self, s3_client, bucket):
        self.s3_client = s3_client
        self.bucket = bucket

    def write_parquet(self, df, key):
        """Writes a DataFrame as a Parquet file to S3."""
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        self.s3_client.put_object(Bucket=self.bucket, Key=key, Body=buffer.getvalue())

    def write_partitioned(self, df, base_key, partition_columns):
        """Writes a DataFrame as Parquet files to S3, partitioned by specified columns."""
        grouped = df.groupby(partition_columns)
        for partition_values, group in grouped:
            partition_subdir = "/".join([f"{col}={val}" for col, val in zip(partition_columns, partition_values)])
            key = f"{base_key}/{partition_subdir}/data.parquet"
            self.write_parquet(group, key)

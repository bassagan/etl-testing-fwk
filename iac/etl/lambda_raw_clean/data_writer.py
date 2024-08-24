import io
import pandas as pd

class DataWriter:
    def __init__(self, s3_client, bucket_name):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def write_parquet_to_s3(self, df, key):
        """Write a DataFrame as a Parquet file to S3."""
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False, engine='pyarrow')
        self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=buffer.getvalue())

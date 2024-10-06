import great_expectations as gx
import os

class DataContextManager:
    def __init__(self):
        self.context = gx.get_context(mode="file")
        self.data_source = self._setup_data_source()

    def _setup_data_source(self):
        data_source_name = "s3_raw_data_source"
        bucket_name = os.environ.get("RAW_BUCKET", "default-bucket-name")  # Updated to use environment variable
        boto_endpoint = os.environ.get("S3_ENDPOINT", "https://s3.eu-west-1.amazonaws.com")
        boto3_options = {"region_name": "eu-west-1", "endpoint_url": boto_endpoint}
        site_config = {
            "class_name": "SiteBuilder",
            "site_index_builder": {"class_name": "DefaultSiteIndexBuilder"},
            "store_backend": {
                "class_name": "TupleS3StoreBackend",
                "bucket": os.environ.get("GX_REPORT_BUCKET", "default-store-bucket"),  # Updated to use environment variable
                "prefix": "great_expectations",
                "boto3_options": boto3_options,
            },
        }
        
        self.context.add_data_docs_site(site_name="data_docs_paula", site_config=site_config)

        try:
            data_source = self.context.get_datasource(data_source_name)
            print(f"Using existing data source: {data_source_name}")
        except ValueError:
            print(f"Creating new data source: {data_source_name}")
            data_source = self.context.data_sources.add_pandas_s3(
                name=data_source_name, bucket=bucket_name, boto3_options=boto3_options
            )

        return data_source
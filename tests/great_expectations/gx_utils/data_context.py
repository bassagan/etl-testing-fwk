import great_expectations as gx
import os

class DataContextManager:
    def __init__(self, context_directory = None):
        self.context_directory = context_directory
        self.context = gx.get_context(mode="file", project_root_dir=context_directory)
        self.data_sources = {}  # Changed from list to dict

    def add_data_source(self, data_source_name, bucket_name):
        boto3_options = self._get_boto3_options()
        site_config = self._get_site_config(boto3_options)

        self._ensure_data_docs_site_exists(site_config)

        data_source = self._get_or_create_data_source(data_source_name, bucket_name, boto3_options)
        return data_source
        

    def _get_boto3_options(self):
        boto_endpoint = os.environ.get("S3_ENDPOINT", "https://s3.eu-west-1.amazonaws.com")
        return {"region_name": "eu-west-1", "endpoint_url": boto_endpoint}

    def _get_site_config(self, boto3_options):
        return {
            "class_name": "SiteBuilder",
            "site_index_builder": {"class_name": "DefaultSiteIndexBuilder"},
            "store_backend": {
                "class_name": "TupleS3StoreBackend",
                "bucket": os.environ.get("GX_REPORT_BUCKET", "default-store-bucket"),
                "prefix": self.context_directory,
                "boto3_options": boto3_options,
            },
        }

    def _ensure_data_docs_site_exists(self, site_config):
        if "data_docs_paula" not in self.context.list_data_docs_sites():
            self.context.add_data_docs_site(site_name="data_docs_paula", site_config=site_config)
        else:
            print(f"Data Docs Site `data_docs_paula` already exists.")

    def _get_or_create_data_source(self, data_source_name, bucket_name, boto3_options):
        try:
            data_source = self.context.get_datasource(data_source_name)
            self.data_sources[data_source_name] = data_source  
            print(f"Data source `{data_source_name}` added to the dictionary.")
            return data_source
        except ValueError:
            print(f"Creating new data source: {data_source_name}")
            data_source = self.context.data_sources.add_pandas_s3(
                name=data_source_name, bucket=bucket_name, boto3_options=boto3_options
            )
            self.data_sources[data_source_name] = data_source  
            print(f"Data source `{data_source_name}` added to the dictionary.")
            return data_source 
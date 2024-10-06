import boto3
from botocore.exceptions import ClientError
from datetime import datetime

class AssetManager:
    def __init__(self, context, data_sources):  
        self.context = context
        self.data_sources = data_sources
        self.s3_client = boto3.client('s3')


    def setup_assets_by_type(self, data_source_name, config):
        if config['type'] == 'json':
            self._setup_json_assets(config['assets'], data_source_name)  # Pass data source name
        elif config['type'] == 'parquet':
            self._setup_parquet_assets(config['assets'], data_source_name)  # Pass data source name

        # Setup batch definitions for all assets
        for asset in config['assets']:  # Loop through each asset to setup batches
            self._setup_batch_definitions(asset['batches'], data_source_name, asset['name'])  # Pass asset name

    def _setup_json_assets(self, assets, data_source_name):  # Accept data source name
        for asset in assets:
            asset_name = asset['name']
            s3_prefix = asset['s3_prefix']
            try:
                self.data_sources[data_source_name].get_asset(asset_name)  # Use data source name
                print(f"Using existing asset: {asset_name}")
            except (ValueError, LookupError):
                print(f"Creating new asset: {asset_name}")
                self.data_sources[data_source_name].add_json_asset(
                    name=asset_name,
                    s3_prefix=s3_prefix,
                )
    
    def _setup_parquet_assets(self, assets, data_source_name):  # Accept data source name
        for asset in assets:
            asset_name = asset['name']
            s3_prefix = asset['s3_prefix']
            try:
                self.data_sources[data_source_name].get_asset(asset_name)  # Use data source name
                print(f"Using existing asset: {asset_name}")
            except (ValueError, LookupError):
                print(f"Creating new asset: {asset_name}")
                self.data_sources[data_source_name].add_parquet_asset(
                    name=asset_name,
                    s3_prefix=s3_prefix,
                )

    def _setup_batch_definitions(self, batches, data_source_name, asset_name):
        for batch in batches:
            file_prefix = batch['file_prefix']
            asset = self.data_sources[data_source_name].get_asset(asset_name)
            try:
                asset.get_batch_definition(batch['name'])
                print(f"Using existing batch definition: {batch['name']}")
            except (ValueError, KeyError):
                print(f"Creating new batch definition: {batch['name']}")
                file_name = self._get_latest_created_file(file_prefix, self.get_bucket_name(data_source_name))  # Adjust this if needed
                asset.add_batch_definition_path(name=batch['name'], path=file_name)


    def _get_latest_created_file(self, prefix, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(
                Bucket= bucket_name,
                Prefix=prefix
            )
            files = [
                obj for obj in response.get('Contents', [])
                if obj['Key'].lower().endswith('.json') or obj['Key'].lower().endswith('.parquet') 
            ]
            if files:
                latest_file = max(files, key=lambda x: x['LastModified'])
                file_name = latest_file['Key'].replace(prefix, '', 1).lstrip('/')
                print("Found file is:", file_name)
                return file_name
            return None
        except ClientError as e:
            print(f"Error accessing S3: {e}")
            return None

    def get_bucket_name(self, data_source_name):
            return self.data_sources[data_source_name].bucket
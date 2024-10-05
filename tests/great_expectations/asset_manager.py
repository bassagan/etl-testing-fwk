import boto3
from botocore.exceptions import ClientError
from datetime import datetime

class AssetManager:
    def __init__(self, context, data_source):
        self.context = context
        self.data_source = data_source
        self.bucket_name = "raw-s3-conference-user-df720b8a-ohmm6c2l"
        self.s3_client = boto3.client('s3')

    def setup_assets(self):
        self._setup_json_assets()

        self._setup_batch_definitions()

    def _setup_json_assets(self):
        for asset_name, s3_prefix in [
            ("patients_data", r"patients/"),
            ("visits_data", r"visits/")
        ]:
            try:
                self.data_source.get_asset(asset_name)
                print(f"Using existing asset: {asset_name}")
            except (ValueError, LookupError):
                print(f"Creating new asset: {asset_name}")
                self.data_source.add_json_asset(
                    name=asset_name,
                    s3_prefix=s3_prefix,
                )

    def _setup_batch_definitions(self):
        for asset_name, batch_name, file_name in [
            ("patients_data", "batch_patients", self._get_latest_created_json_file("patients")),
            ("visits_data", "batch_visits", self._get_latest_created_json_file("visits"))
        ]:
            asset = self.data_source.get_asset(asset_name)
            try:
                asset.get_batch_definition(batch_name)
                print(f"Using existing batch definition: {batch_name}")
            except (ValueError, KeyError):
                print(f"Creating new batch definition: {batch_name}")
                asset.add_batch_definition_path(name=batch_name, path=file_name)

    def get_batch(self, asset_name, batch_name):
        return self.data_source.get_asset(asset_name).get_batch_definition(batch_name).get_batch()

    def _get_latest_created_json_file(self, prefix):
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            json_files = [
                obj for obj in response.get('Contents', [])
                if obj['Key'].lower().endswith('.json')
            ]
            if json_files:
                latest_file = max(json_files, key=lambda x: x['LastModified'])
                file_name = latest_file['Key'].replace(prefix, '', 1).lstrip('/')
                print("Found json is:", file_name)
                return file_name
            return None
        except ClientError as e:
            print(f"Error accessing S3: {e}")
            return None
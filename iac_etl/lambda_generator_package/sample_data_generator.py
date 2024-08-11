import json
import boto3
from moto import mock_aws
from data_generator import DataGenerator

# S3 bucket and file names
PATIENTS_FILE = 'patients.json'
VISITS_FILE = 'visits.json'

@mock_aws
def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = event.get('s3_bucket', 'default-bucket-name')

    # Set ranges for initial patients and new patients over time
    initial_patients_range = (50, 100)
    new_patients_range = (5, 50)

    # Instantiate the DataGenerator class
    data_gen = DataGenerator(bucket_name, s3_client, PATIENTS_FILE, VISITS_FILE)

    # Load existing data, update it, and save back to S3
    data_gen.load_existing_data()
    data_gen.update_existing_data(initial_patients_range, new_patients_range)
    data_gen.save_data_to_s3()

    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "Data successfully generated and uploaded.",
            "patients_count": len(data_gen.patients),
            "visits_count": len(data_gen.visits)
        })
    }

if __name__ == "__main__":
    mock_event = {
        '{
  "s3_bucket": "your-s3-bucket-name"
}s3_bucket': 'my-test-bucket',
    }
    lambda_handler(mock_event, None)

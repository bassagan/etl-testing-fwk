import json
import boto3
from data_generator import DataGenerator
from datetime import datetime


def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = event.get('s3_bucket', 'default-bucket-name')



    # Set ranges for initial patients and new patients over time
    initial_patients_range = (50, 100)
    new_patients_range = (5, 50)

    # Generate a timestamp or unique identifier for this execution
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Instantiate the DataGenerator class with file paths including the timestamp
    data_gen = DataGenerator(
        bucket_name=bucket_name,
        s3_client=s3_client,
        patients_file=f'patients/patients_{timestamp}.json',
        visits_file=f'visits/visits_{timestamp}.json',
        latest_patients_prefix='patients/',
        latest_visits_prefix='visits/'
    )

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
    lambda_handler(None, None)

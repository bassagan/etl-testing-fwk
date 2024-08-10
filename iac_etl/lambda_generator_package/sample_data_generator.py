import json
import random
import uuid
import faker
import boto3
from datetime import datetime, timedelta

# Initialize Faker for generating synthetic data
fake = faker.Faker()

def generate_patient_record(patient_id):
    """Generates a single patient record with potential for duplicates."""
    visit_date = fake.date_time_this_year()
    return {
        "patient_id": patient_id,
        "name": fake.name(),
        "date_of_birth": fake.date_of_birth(minimum_age=20, maximum_age=90).isoformat(),
        "visit_date": visit_date.isoformat(),
        "diagnosis": fake.text(max_nb_chars=20),
        "medication": fake.text(max_nb_chars=20),
        "doctor": fake.name(),
        "address": fake.address().replace("\n", ", "),
        "insurance_details": {
            "provider": fake.company(),
            "policy_number": fake.bothify(text='???-########'),
            "valid_till": (visit_date + timedelta(days=random.randint(30, 365))).isoformat()
        }
    }

def generate_source_data(num_records):
    """Generates a list of patient records with duplicates."""
    records = []
    for _ in range(num_records):
        patient_id = str(uuid.uuid4())
        record = generate_patient_record(patient_id)
        records.append(record)

        # Add duplicate record
        if random.random() < 0.1:  # 10% chance of duplicate
            records.append(record.copy())

    return records

def save_to_s3(bucket_name, key, data):
    """Saves data to S3 bucket."""
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(data))

def lambda_handler(event, context):
    """AWS Lambda handler"""
    # Parameters
    num_records = random.randint(10, 100)  # Generate between 10 and 100 records
    bucket_name = event['s3_bucket']

    # Generate data for two sources
    source_a_data = generate_source_data(num_records)
    source_b_data = generate_source_data(num_records)

    # Save data to S3
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    save_to_s3(bucket_name, f'source_a/data_{timestamp}.json', source_a_data)
    save_to_s3(bucket_name, f'source_b/data_{timestamp}.json', source_b_data)

    return {
        'statusCode': 200,
        'body': json.dumps(f"Generated and uploaded {len(source_a_data)} records for Source A and {len(source_b_data)} records for Source B.")
    }

if __name__ == "__main__":
    lambda_handler(None, None)

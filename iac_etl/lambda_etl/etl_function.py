import boto3
from datetime import datetime
import pandas as pd
import json
from data_reader import DataReader
from data_cleaner import DataCleaner
from scd_historization import SCDHistorization
from data_writer import DataWriter

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    # Define the source and destination buckets and the key to store the last processed timestamp
    source_bucket = event.get('source_bucket', 'raw-etl-bucket-dev')
    destination_bucket = event.get('destination_bucket', 'clean-etl-bucket-dev')
    last_processed_timestamp_key = 'last-processed-timestamp.txt'

    # Define schema and keys for patients and visits
    patients_schema = {
        'patient_id': 'string',
        'name': 'string',
        'date_of_birth': 'datetime64[ns]',
        'address': 'string',
        'phone_number': 'string',
        'email': 'string',
        'insurance_provider': 'string',
        'policy_number': 'string',
        'policy_valid_till': 'datetime64[ns]',
        'record_created_at': 'datetime64[ns]',
        'record_updated_at': 'datetime64[ns]'
    }
    visits_schema = {
        'appointment_id': 'string',
        'patient_id': 'string',
        'appointment_date': 'datetime64[ns]',
        'doctor': 'string',
        'department': 'string',
        'purpose': 'string',
        'status': 'string',
        'diagnosis': 'string',
        'medication': 'string',
        'notes': 'string',
        'record_created_at': 'datetime64[ns]',
        'record_updated_at': 'datetime64[ns]'
    }
    patients_keys = ['patient_id']
    visits_keys = ['appointment_id', 'patient_id']

    # Instantiate the classes
    data_reader = DataReader(s3_client, source_bucket, last_processed_timestamp_key)
    data_cleaner_patients = DataCleaner(patients_schema)
    data_cleaner_visits = DataCleaner(visits_schema)
    scd_patients = SCDHistorization(patients_keys)
    scd_visits = SCDHistorization(visits_keys)
    data_writer = DataWriter(s3_client, destination_bucket)

    # Process patients data
    patient_files = data_reader.list_unprocessed_files('patients/')
    patients_data_frames = [data_reader.read_json_from_s3(file) for file in patient_files]
    if patients_data_frames:
        df_patients = pd.concat(patients_data_frames, ignore_index=True)
        df_patients = data_cleaner_patients.enforce_schema(df_patients)
        df_patients = data_cleaner_patients.remove_duplicates(df_patients)

        # Retrieve existing patient data for SCD Type 2
        existing_patients_key = 'cleaned/patients/latest.parquet'
        try:
            df_existing_patients = data_reader.read_parquet_from_s3(existing_patients_key)
        except:
            df_existing_patients = None

        df_patients = scd_patients.apply_scd_type_2(df_patients, df_existing_patients)

        # Write cleaned patients data to S3
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        patients_key = f'cleaned/patients/patients_{timestamp}.parquet'
        data_writer.write_parquet_to_s3(df_patients, patients_key)
        data_writer.write_parquet_to_s3(df_patients, existing_patients_key)

        # Update the last processed timestamp to the most recent file processed
        latest_timestamp = max(re.search(r'(\d{14})', file).group(1) for file in patient_files)
        data_reader.update_last_processed_timestamp(latest_timestamp)

    # Process visits data
    visit_files = data_reader.list_unprocessed_files('visits/')
    visits_data_frames = [data_reader.read_json_from_s3(file) for file in visit_files]
    if visits_data_frames:
        df_visits = pd.concat(visits_data_frames, ignore_index=True)
        df_visits = data_cleaner_visits.enforce_schema(df_visits)
        df_visits = data_cleaner_visits.remove_duplicates(df_visits)

        # Retrieve existing visit data for SCD Type 2
        existing_visits_key = 'cleaned/visits/latest.parquet'
        try:
            df_existing_visits = data_reader.read_parquet_from_s3(existing_visits_key)
        except:
            df_existing_visits = None

        df_visits = scd_visits.apply_scd_type_2(df_visits, df_existing_visits)

        # Write cleaned visits data to S3
        visits_key = f'cleaned/visits/visits_{timestamp}.parquet'
        data_writer.write_parquet_to_s3(df_visits, visits_key)
        data_writer.write_parquet_to_s3(df_visits, existing_visits_key)

        # Update the last processed timestamp to the most recent file processed
        latest_timestamp = max(re.search(r'(\d{14})', file).group(1) for file in visit_files)
        data_reader.update_last_processed_timestamp(latest_timestamp)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "Data processing complete.",
            "patients_count": len(df_patients) if patients_data_frames else 0,
            "visits_count": len(df_visits) if visits_data_frames else 0
        })
    }

if __name__ == "__main__":
    lambda_handler(None, None)

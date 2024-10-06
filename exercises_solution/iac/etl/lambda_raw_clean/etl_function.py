import boto3
from datetime import datetime
import pandas as pd
import json
import re
from data_reader import DataReader
from data_cleaner import DataCleaner
from scd_historization import SCDHistorization
from data_writer import DataWriter
import os

def normalize_month(month):
    """Ensure month is always in MM format."""
    return f'{int(month):02d}'

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    # Define the source and destination buckets and the key to store the last processed timestamp
    source_bucket = os.environ.get('SOURCE_BUCKET') or event.get('source_bucket') or 'raw-etl-bucket-dev'
    destination_bucket = os.environ.get('TARGET_BUCKET') or event.get('destination_bucket') or 'clean-etl-bucket-dev'
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
    patients_keys = ['patient_id', 'address']
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
        existing_patients_key = 'cleaned/patients/latest/patients_latest.parquet'
        try:
            df_existing_patients = data_reader.read_parquet_from_s3(existing_patients_key)
        except:
            df_existing_patients = None

        df_patients = scd_patients.apply_scd_type_2(df_patients, df_existing_patients)

        # Partition patients data by year and month of birth
        df_patients['year_of_birth'] = df_patients['date_of_birth'].dt.year
        df_patients['month_of_birth'] = df_patients['date_of_birth'].dt.month.apply(normalize_month)

        for (year, month), group in df_patients.groupby(['year_of_birth', 'month_of_birth']):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            partition_key = f'cleaned/patients/year={year}/month={month}/patients_{timestamp}.parquet'
            data_writer.write_parquet_to_s3(group, partition_key)

        # Write the latest patients data to a "latest" file
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
        existing_visits_key = 'cleaned/visits/latest/visits_latest.parquet'
        try:
            df_existing_visits = data_reader.read_parquet_from_s3(existing_visits_key)
        except:
            df_existing_visits = None

        df_visits = scd_visits.apply_scd_type_2(df_visits, df_existing_visits)

        # Partition visits data by year and month of appointment
        df_visits['year'] = df_visits['appointment_date'].dt.year
        df_visits['month'] = df_visits['appointment_date'].dt.month.apply(normalize_month)

        for (year, month), group in df_visits.groupby(['year', 'month']):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            partition_key = f'cleaned/visits/year={year}/month={month}/visits_{timestamp}.parquet'
            data_writer.write_parquet_to_s3(group, partition_key)

        # Write the latest visits data to a "latest" file
        data_writer.write_parquet_to_s3(df_visits, existing_visits_key)

        # Update the last processed timestamp to the most recent file processed
        latest_timestamp = max(re.search(r'(\d{14})', file).group(1) for file in visit_files)
        data_reader.update_last_processed_timestamp(latest_timestamp)

    # Send message to SNS to trigger clean-curated function
    sns_client = boto3.client('sns')
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    
    try:
        # Success message (as previously added)
        if sns_topic_arn:
            success_message = {
                "status": "success",
                "message": "Raw to Clean ETL complete. Start Clean to Curated ETL.",
                "patients_count": len(df_patients) if patients_data_frames else 0,
                "visits_count": len(df_visits) if visits_data_frames else 0
            }
            
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=json.dumps(success_message)
            )
        else:
            print("SNS_TOPIC_ARN not set. Skipping SNS notification.")

        return {
            'statusCode': 200,
            'body': json.dumps(success_message)
        }

    except Exception as e:
        error_message = {
            "status": "error",
            "message": f"Raw to Clean ETL failed: {str(e)}",
            "error_details": str(e)
        }
        
        if sns_topic_arn:
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=json.dumps(error_message)
            )
        else:
            print("SNS_TOPIC_ARN not set. Skipping error notification.")
        
        # Re-raise the exception after sending the notification
        raise

if __name__ == "__main__":
    lambda_handler(None, None)


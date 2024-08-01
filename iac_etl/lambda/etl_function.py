import json
import boto3
import os
import pandas as pd
from io import StringIO
from datetime import datetime

# Initialize the S3 client
s3_client = boto3.client('s3')

# Initialize the SNS client
sns_client = boto3.client('sns')

# Initialize the DynamoDB client for historization
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('HISTORICAL_TABLE_NAME')

def lambda_handler(event, context):
    # Get the bucket and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    try:
        # Download the file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')

        # Process the file (for example, parse JSON or CSV)
        processed_data = process_data(content)

        # Store the historical data
        store_historical_data(processed_data, object_key)

        # Send a notification via SNS
        sns_topic_arn = os.environ['SNS_TOPIC_ARN']
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=f'Processed and stored data from {object_key} in {bucket_name}: {processed_data}',
            Subject='ETL Process Notification'
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Processing and historization complete')
        }

    except Exception as e:
        print(f"Error processing file {object_key} from bucket {bucket_name}: {str(e)}")
        raise e

def process_data(data):
    """
    Apply business rules to transform the data using Pandas.
    """
    # Convert the CSV data into a Pandas DataFrame
    df = pd.read_csv(StringIO(data))

    # Example transformations:
    # 1. Convert the 'name' column to uppercase
    df['name'] = df['name'].str.upper()

    # 2. Apply a discount to 'price' if it exceeds a threshold
    discount_threshold = 100
    discount_rate = 0.1
    df['price'] = df['price'].apply(lambda x: x * (1 - discount_rate) if x > discount_threshold else x)

    # 3. Add a timestamp column for when the data was processed
    df['timestamp'] = datetime.utcnow().isoformat()

    # 4. Convert 'status' to a boolean 'is_active' column
    df['is_active'] = df['status'].apply(lambda x: True if x == 'active' else False)

    # Convert the DataFrame back to JSON
    return df.to_dict(orient='records')

def store_historical_data(processed_data, object_key):
    """
    Store the processed data in DynamoDB for historization.
    """
    table = dynamodb.Table(table_name)

    for record in processed_data:
        # Add the S3 object key and processing time for historization
        record['s3_object_key'] = object_key
        record['processed_at'] = datetime.utcnow().isoformat()

        # Store the record in DynamoDB
        table.put_item(Item=record)

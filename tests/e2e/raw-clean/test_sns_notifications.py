import pytest
import json
import boto3
import time
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Add these lines at the beginning of the file
REGION_NAME = os.environ.get('AWS_REGION', 'eu-west-1')
RAW_BUCKET = os.environ.get('RAW_BUCKET')
CURATED_BUCKET = os.environ.get('CURATED_BUCKET')
CLEAN_BUCKET = os.environ.get('CLEAN_BUCKET')
LAMBDA_RAW_CLEAN_FUNCTION_NAME = os.environ.get('LAMBDA_RAW_CLEAN_FUNCTION_NAME')

@pytest.fixture
def lambda_client():
    return boto3.client("lambda", region_name=REGION_NAME)

@pytest.fixture
def sns_client():
    return boto3.client("sns", region_name=REGION_NAME)

@pytest.fixture
def lambda_event():
    return {}

@pytest.fixture
def lambda_function_name():
    print("RAW_BUCKET", RAW_BUCKET)
    print("LAMBDA_RAW_CLEAN_FUNCTION_NAME", LAMBDA_RAW_CLEAN_FUNCTION_NAME)
    return LAMBDA_RAW_CLEAN_FUNCTION_NAME

import os
os.environ['no_proxy'] = '*'

@pytest.fixture
def sqs_client():
    return boto3.client("sqs", region_name=REGION_NAME)


class TestSNSNotifications:

    @pytest.mark.parametrize("invocation_type", ["RequestResponse"])
    def test_lambda_execution(self,lambda_client, lambda_event, lambda_function_name, invocation_type):
        # Act
        response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(lambda_event)
        )

        # Assert
        assert response['StatusCode'] == 200, f"Lambda execution failed with status code {response['StatusCode']}"
    
   
        # Act
        lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(lambda_event)
        )

        # Assert
        # Poll the SQS queue for messages
        max_attempts = 20  # Increase the number of attempts
        for attempt in range(max_attempts):
            response = sqs_client.receive_message(
                QueueUrl=sqs_queue,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=5  # Increase wait time
            )
            
            print(f"Attempt {attempt + 1}: {response}")  # Add debug output
            
            if 'Messages' in response:
                message = json.loads(json.loads(response['Messages'][0]['Body'])['Message'])
                
                # Verify the message content
                assert 'patients_count' in message, "Expected 'patients_count' not found in SNS message"
                assert 'visits_count' in message, "Expected 'visits_count' not found in SNS message"
                return
            
            time.sleep(2)  # Increase sleep time between attempts
        
        # If no message is received, print queue attributes for debugging
        queue_attributes = sqs_client.get_queue_attributes(
            QueueUrl=sqs_queue,
            AttributeNames=['All']
        )
        print(f"Queue attributes: {queue_attributes}")
        
        pytest.fail("No message received from SNS after multiple attempts")
import pytest
import json
import boto3
import time
import os

# Add these lines at the beginning of the file
REGION_NAME = os.environ.get('AWS_REGION', 'eu-west-1')
RAW_BUCKET = os.environ['RAW_BUCKET']
CURATED_BUCKET = os.environ['CURATED_BUCKET']
CLEAN_BUCKET = os.environ['CLEAN_BUCKET']
LAMBDA_FUNCTION_NAME = os.environ['LAMBDA_FUNCTION_NAME']

@pytest.fixture
def lambda_client():
    return boto3.client("lambda", region_name=REGION_NAME)

@pytest.fixture
def sns_client():
    return boto3.client("sns", region_name=REGION_NAME)

@pytest.fixture
def lambda_event():
    return {
        'source_bucket': RAW_BUCKET,
        'destination_bucket': CLEAN_BUCKET
    }

@pytest.fixture
def lambda_function_name():
    return LAMBDA_FUNCTION_NAME

import os
os.environ['no_proxy'] = '*'

@pytest.fixture
def sqs_client():
    return boto3.client("sqs", region_name=REGION_NAME)

@pytest.fixture
def sqs_queue(sqs_client, sns_client, lambda_client, lambda_function_name):
    # Create a temporary SQS queue
    queue_name = f"test-queue-{int(time.time())}"
    response = sqs_client.create_queue(QueueName=queue_name)
    queue_url = response['QueueUrl']

    # Get the SNS topic ARN
    lambda_config = lambda_client.get_function_configuration(FunctionName=lambda_function_name)
    sns_topic_arn = lambda_config['Environment']['Variables']['SNS_TOPIC_ARN']

    # Subscribe the SQS queue to the SNS topic
    sns_client.subscribe(
        TopicArn=sns_topic_arn,
        Protocol='sqs',
        Endpoint=sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['QueueArn'])['Attributes']['QueueArn']
    )

    yield queue_url

    # Cleanup: delete the temporary queue
    sqs_client.delete_queue(QueueUrl=queue_url)

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
    
    def test_sns_notification_sent(self, lambda_client, sns_client, sqs_client, sqs_queue, lambda_event, lambda_function_name):
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
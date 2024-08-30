import pytest
import json
import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()
os.environ['no_proxy'] = '*'

# Pytest fixture to create a boto3 Lambda client
# Fixtures are reusable pieces of code that set up resources for tests
@pytest.fixture
def lambda_client(region_name):
    return boto3.client("lambda", region_name=region_name)


@pytest.fixture
def raw_clean_lambda_function_name():
    return os.environ.get('LAMBDA_RAW_CLEAN_FUNCTION_NAME')


@pytest.fixture
def sqs_client(region_name):
    return boto3.client("sqs", region_name=region_name)

@pytest.fixture
def region_name():
    return os.environ.get('AWS_REGION', 'eu-west-1')

@pytest.fixture
def raw_bucket():
    return os.environ.get('RAW_BUCKET')

@pytest.fixture
def curated_bucket():
    return os.environ.get('CURATED_BUCKET')

@pytest.fixture
def clean_bucket():
    return os.environ.get('CLEAN_BUCKET')

@pytest.fixture
def lambda_client(region_name):
    return boto3.client("lambda", region_name=region_name)

class TestSNSNotifications:
    # Pytest parametrize decorator to run the test with different invocation types
    @pytest.mark.parametrize("invocation_type", ["RequestResponse"])
    def test_lambda_execution(self,lambda_client, raw_clean_lambda_function_name, invocation_type):
        # Act: Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=raw_clean_lambda_function_name,
            InvocationType=invocation_type,
            Payload=json.dumps({})
        )

        # Assert: Check if the Lambda execution was successful 
        assert response['StatusCode'] == 200, f"Lambda execution failed with status code {response['StatusCode']}"



import pytest
import os
import boto3
import json
from dotenv import load_dotenv


load_dotenv()

@pytest.fixture
def lambda_client(region_name):
    return boto3.client("lambda", region_name=region_name)


@pytest.fixture
def raw_clean_lambda_function_name():
    return os.environ.get('LAMBDA_RAW_CLEAN_FUNCTION_NAME', "data_generator-conference-user-df720b8a")

@pytest.fixture
def data_generator_function_name():
    return os.environ.get('DATA_GENERATOR_FUNCTION_NAME', "raw_clean_lmb-conference-user-df720b8a")


@pytest.fixture
def sqs_client(region_name):
    return boto3.client("sqs", region_name=region_name)

@pytest.fixture
def region_name():
    return os.environ.get('AWS_REGION', 'eu-west-1')

@pytest.fixture
def raw_bucket():
    return os.environ.get('RAW_BUCKET', "raw-s3-conference-user-df720b8a-ohmm6c2l")

@pytest.fixture
def curated_bucket():
    return os.environ.get('CURATED_BUCKET', "curated-s3-conference-user-df720b8a-ohmm6c2l")

@pytest.fixture
def clean_bucket():
    return os.environ.get('CLEAN_BUCKET', "clean-s3-conference-user-df720b8a-ohmm6c2l")

@pytest.fixture
def lambda_client(region_name):
    return boto3.client("lambda", region_name=region_name)

@pytest.fixture(autouse=True)
def generate_test_data(lambda_client, data_generator_function_name, raw_bucket):
    """
    Fixture to generate test data by invoking the data generator Lambda function.
    This fixture runs automatically before each test.
    """
    # Invoke the data generator Lambda function
    response = lambda_client.invoke(
        FunctionName=data_generator_function_name,
        InvocationType='Event',
        Payload=json.dumps({"s3_bucket": raw_bucket})
    )
    
    # Assert that the Lambda function was called successfully
    assert response['StatusCode'] == 202, "Failed to invoke data generator Lambda function"
    


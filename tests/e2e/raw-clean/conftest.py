
import pytest
import os
import boto3
import json
from dotenv import load_dotenv

# Exercise 2.2: Implement a fixture to generate test data.
# 
# Notes:
# 1. In pytest, fixtures are typically defined at the module level, outside of test classes.
# 2. The convention is to place shared fixtures in a conftest.py file in the test directory.
# 3. There's no built-in 'before_each' in pytest; instead, we use fixtures with appropriate scopes.
#
# Steps:
# 1. Move all existing fixtures from test_sns_notifications.py file to the conftest.py file.
# 2. In the conftest.py file, create a new fixture named 'generate_test_data'.
# 3. Use the @pytest.fixture decorator, adding (autouse=True) if you want it to run automatically. So it will run before each test. 
#       i.e. @pytest.fixture(autouse=True)
# 4. Implement the fixture to call the data generator lambda function. 
#       i.e. use the boto3 client to invoke the lambda function: 
#           aws_lambda_client.invoke(FunctionName=data_generator_function_name, 
#                                    InvocationType='Event', 
#                                    Payload=json.dumps({}))
# 5. Assert that the data generator lambda function was called successfully.
#       i.e. assert that the lambda function was called successfully by checking the response from the lambda function.
# 6. In test_sns_notifications.py, remove any fixture definitions that were moved to conftest.py.
# 7. Use the new 'generate_test_data' fixture in your test methods by adding it as a parameter. 
#       i.e. def test_sns_notifications(other_fixtures, generate_test_data):

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
        Payload=json.dumps({"s3_bucket":raw_bucket})
    )
    
    # Assert that the Lambda function was called successfully
    assert response['StatusCode'] == 202, "Failed to invoke data generator Lambda function"
    
    # The fixture doesn't need to return anything as it's used for its side effects

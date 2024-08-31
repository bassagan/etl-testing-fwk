import pytest
import json
import os
from dotenv import load_dotenv
import boto3
import allure

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
    @allure.feature("Lambda Function")
    @allure.story("Raw Clean Lambda Execution")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("invocation_type", [
        pytest.param("RequestResponse", id="Synchronous Invocation")
    ])
    def test_lambda_execution(self, lambda_client, raw_clean_lambda_function_name, invocation_type):
        """
        Test the execution of the Raw Clean Lambda function.

        :param lambda_client: Boto3 Lambda client
        :param raw_clean_lambda_function_name: Name of the Lambda function to test
        :param invocation_type: Type of Lambda invocation (RequestResponse for synchronous)
        """
        with allure.step("Prepare Lambda invocation parameters"):
            payload = json.dumps({})

        with allure.step(f"Invoke Lambda function '{raw_clean_lambda_function_name}' with {invocation_type} invocation"):
            response = lambda_client.invoke(
                FunctionName=raw_clean_lambda_function_name,
                InvocationType=invocation_type,
                Payload=payload
            )

        with allure.step("Check Lambda execution status"):
            assert response['StatusCode'] == 200, f"Lambda execution failed with status code {response['StatusCode']}"

        with allure.step("Save Lambda execution response"):
            serializable_response = {
                'StatusCode': response['StatusCode'],
                'ExecutedVersion': response.get('ExecutedVersion'),
                'FunctionError': response.get('FunctionError'),
                'LogResult': response.get('LogResult'),
            }
            allure.attach(
                json.dumps(serializable_response, indent=2),
                name="Lambda Response",
                attachment_type=allure.attachment_type.JSON
            )

        # Add more assertions here if needed to verify the response payload


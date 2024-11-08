import pytest
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import boto3

# TODO: Exercise 3 - Import Allure
#import allure

# Load environment variables from .env file
load_dotenv()
# Pytest fixture to create a boto3 Lambda client
# Fixtures are reusable pieces of code that set up resources for tests
@pytest.fixture
def lambda_client(region_name):
    return boto3.client("lambda", region_name=region_name)

@pytest.fixture
def s3_client(region_name):
    return boto3.client("s3", region_name=region_name)

@pytest.fixture
def raw_clean_lambda_function_name():
    return os.environ.get('LAMBDA_RAW_CLEAN_FUNCTION_NAME')
@pytest.fixture
def data_generator_function_name():
    return os.environ.get('DATA_GENERATOR_FUNCTION_NAME')

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

class TestRawToClean:
    # Pytest parametrize decorator to run the test with different invocation types
    @pytest.mark.parametrize("invocation_type", ["RequestResponse"])
    def test_lambda_execution(self, lambda_client,
                              raw_clean_lambda_function_name,
                              invocation_type,
                              generate_test_data):
        # Act: Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=raw_clean_lambda_function_name,
            InvocationType=invocation_type,
            Payload=json.dumps({})
        )
        # Assert: Check if the Lambda execution was successful
        payload = json.loads(response['Payload'].read())

        status_code = payload.get('statusCode')
        body_json = json.loads(payload.get('body'))

        assert status_code == 200, f"Lambda execution failed with status code {response['StatusCode']}"
        assert body_json['patients_count'] != 0, "No patients were processed"
        assert body_json['visits_count'] != 0, "No visits were processed"

    @pytest.mark.parametrize("invocation_type", ["RequestResponse"])
    def test_lambda_execution_no_new_data(self, lambda_client,
                              raw_clean_lambda_function_name,
                              invocation_type):
        # Act: Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=raw_clean_lambda_function_name,
            InvocationType=invocation_type,
            Payload=json.dumps({})
        )
        # Assert: Check if the Lambda execution was successful
        payload = json.loads(response['Payload'].read())

        status_code = payload.get('statusCode')
        body_json = json.loads(payload.get('body'))

        assert status_code == 200, f"Lambda execution failed with status code {response['StatusCode']}"
        assert body_json['patients_count'] == 0, "Patients were processed"
        assert body_json['visits_count'] == 0, "Visits were processed"

    # TODO: Exercise 3 - Add Allure decorators to the test class and use the mock_patient_data fixture
    @pytest.mark.skip(reason="Remove this line on exercise 3")
    # @allure.feature("Lambda Function")
    # @allure.title("New title for the test case")
    # @allure.story("Raw Clean Lambda Execution")
    @pytest.mark.parametrize("invocation_type", [
        pytest.param("RequestResponse", id="Synchronous Invocation")
    ])
    def test_lambda_execution_invalid_data(self, lambda_client, raw_clean_lambda_function_name,raw_bucket, s3_client, invocation_type):
        """
        Test the execution of the Raw Clean Lambda function.

        :param lambda_client: Boto3 Lambda client
        :param raw_clean_lambda_function_name: Name of the Lambda function to test
        :param invocation_type: Type of Lambda invocation (RequestResponse for synchronous)
        """

        # TODO: Exercise 3 - Add Allure step for invoking Lambda function
        # with allure.step(f"Invoke Lambda function '{raw_clean_lambda_function_name}' with {invocation_type} invocation"):
        response = lambda_client.invoke(
            FunctionName=raw_clean_lambda_function_name,
            InvocationType=invocation_type,
            Payload=json.dumps({})
        )

        # Exercise 3 - Add Allure step for checking Lambda execution status
        # with allure.step("Check Lambda execution status"):
        # Assert: Check if the Lambda execution was successful
        payload = json.loads(response['Payload'].read())
        status_code = response['StatusCode']
        body_json = json.loads(payload.get('body'))

        assert status_code == 200, f"Lambda execution failed with status code {response['StatusCode']}"
        assert body_json['patients_count'] == 2, "Patients were processed"
        assert body_json['visits_count'] == 0, "Visits were processed"

        # TODO: Exercise 3 - Add Allure step for saving Lambda execution response
        # with allure.step("Save Lambda execution response"):

        # TODO: Exercise 3 - Attach the serializable_response to the Allure report
        #     allure.attach(
        #         json.dumps(payload, indent=2),
        #         name="Lambda Response",
        #         attachment_type=allure.attachment_type.JSON
        #     )

        # Add more assertions here if needed to verify the response payload

# TODO: Exercise 3 - Additional Allure features to consider:
# 1. Use @allure.severity() to indicate the severity level of the test
# 2. Use @allure.description() to add a detailed description of the test
# 3. Consider using @allure.link() to add relevant links to the test (e.g., documentation, JIRA tickets)
# 4. If applicable, use @allure.issue() to link to specific issues related to this test
# 5. Explore using @allure.step() as a decorator for helper methods to create more granular steps
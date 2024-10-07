import pytest
import json
import os
from dotenv import load_dotenv

# TODO: Exercise 3 - Import Allure
import allure

# Load environment variables from .env file
load_dotenv()

class TestSNSNotifications:
    # Pytest parametrize decorator to run the test with different invocation types
    @pytest.mark.parametrize("invocation_type", ["RequestResponse"])
    def test_lambda_execution(self, lambda_client, raw_clean_lambda_function_name, invocation_type):
        # Act: Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=raw_clean_lambda_function_name,
            InvocationType=invocation_type,
            Payload=json.dumps({})
        )

        # Assert: Check if the Lambda execution was successful
        assert response['StatusCode'] == 200, f"Lambda execution failed with status code {response['StatusCode']}"

    # TODO: Exercise 3 - Add Allure decorators to the test class
    @allure.feature("Lambda Function")
    @allure.title("New title for the test case")
    @allure.story("Raw Clean Lambda Execution")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Here a detailed description for the test case")
    @pytest.mark.parametrize("invocation_type", [
        pytest.param("RequestResponse", id="Synchronous Invocation")
    ])
    def test_lambda_execution_exercise3(self, lambda_client, raw_clean_lambda_function_name, invocation_type):
        """
        Test the execution of the Raw Clean Lambda function.

        :param lambda_client: Boto3 Lambda client
        :param raw_clean_lambda_function_name: Name of the Lambda function to test
        :param invocation_type: Type of Lambda invocation (RequestResponse for synchronous)
        """
        # TODO: Exercise 3 - Add Allure step for preparing Lambda invocation parameters
        with allure.step("Prepare Lambda invocation parameters"):
            payload = json.dumps({})

        # TODO: Exercise 3 - Add Allure step for invoking Lambda function
        with allure.step(f"Invoke Lambda function '{raw_clean_lambda_function_name}' with {invocation_type} invocation"):
            response = lambda_client.invoke(
                FunctionName=raw_clean_lambda_function_name,
                InvocationType=invocation_type,
                Payload=payload
            )

        # Exercise 3 - Add Allure step for checking Lambda execution status
        with allure.step("Check Lambda execution status"):
            assert response['StatusCode'] == 200, f"Lambda execution failed with status code {response['StatusCode']}"

        # TODO: Exercise 3 - Add Allure step for saving Lambda execution response
        with allure.step("Save Lambda execution response"):
            serializable_response = {
                'StatusCode': response['StatusCode'],
                'ExecutedVersion': response.get('ExecutedVersion'),
                'FunctionError': response.get('FunctionError'),
                'LogResult': response.get('LogResult'),
            }
        # TODO: Exercise 3 - Attach the serializable_response to the Allure report
        allure.attach(
            json.dumps(serializable_response, indent=2),
            name="Lambda Response",
            attachment_type=allure.attachment_type.JSON
        )

        # Add more assertions here if needed to verify the response payload

# TODO: Exercise 3 - Additional Allure features to consider:
# 1. Use @allure.severity() to indicate the severity level of the test
# 2. Use @allure.description() to add a detailed description of the test
# 3. Consider using @allure.link() to add relevant links to the test (e.g., documentation, JIRA tickets)
# 4. If applicable, use @allure.issue() to link to specific issues related to this test
# 5. Explore using @allure.step() as a decorator for helper methods to create more granular steps
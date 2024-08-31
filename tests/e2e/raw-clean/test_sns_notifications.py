import pytest
import json

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


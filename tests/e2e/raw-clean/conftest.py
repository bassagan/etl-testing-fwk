
import pytest
import os
import boto3
from dotenv import load_dotenv

# Exercise 2.1: Implement a fixture to generate test data.
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

# @pytest.fixture(autouse=True)
# def generate_test_data(lambda_client, data_generator_function_name):
#     """
#     Fixture to generate test data by invoking the data generator Lambda function.
#     This fixture runs automatically before each test.
#     """
#     # Invoke the data generator Lambda function
#     # response = lambda_client.invoke(
#     #     ...
#     #     ...
#     #     ..
#     # )
#     
#     # Assert that the Lambda function was called successfully
#     # assert ...
#     
#     # The fixture doesn't need to return anything as it's used for its side effects




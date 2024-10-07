
import pytest
import os
import boto3
import json
from dotenv import load_dotenv


load_dotenv()

# Exercise 2.2: Implement a fixture to generate test data.
#
# Notes:
# 1. In pytest, fixtures are typically defined at the module level, outside of test classes.
# 2. The convention is to place shared fixtures in a conftest.py file in the test directory.
# 3. There's no built-in 'before_each' in pytest; instead, we use fixtures with appropriate scopes.
#
# Step

# 1. Move all existing fixtures from test_lambda_raw_clean.py file to the conftest.py file.
#TODO: Move fixtures here:

# 2. In the conftest.py file, create a new fixture named 'generate_test_data'.
# 3. Use the @pytest.fixture decorator, adding (autouse=True) if you want it to run automatically. So it will run before each test.
#       i.e. @pytest.fixture(autouse=True)
# 4. Implement the fixture to call the data generator lambda function.

# TODO: Uncomment fixture generate_test_data
#       i.e. use the boto3 client to invoke the lambda function:

# @pytest.fixture(autouse=True)
# def generate_test_data(lambda_client, data_generator_function_name, raw_bucket):
#     """
#     Fixture to generate test data by invoking the data generator Lambda function.
#     This fixture runs automatically before each test.
#     """
#     # Invoke the data generator Lambda function
#         response = lambda_client.invoke(
#             FunctionName=data_generator_function_name,
#             InvocationType='Event',
#             Payload=json.dumps({"s3_bucket": raw_bucket})
#         )
#     # 5. Assert that the data generator lambda function was called successfully.
#     #       i.e. assert that the lambda function was called successfully by checking the response from the lambda function.
#     # TODO: assert lambda response, look at test_lambda_raw_clean.py for reference,
#           take into account that in this case the function should return a 202 status code
#     # assert ...


# 6. In test_lambda_raw_clean.py, remove any fixture definitions that were moved to conftest.py.
#     # The fixture doesn't need to return anything as it's used for its side effects
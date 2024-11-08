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
# TODO: Move fixtures here:

# 2. In the conftest.py file, create a new fixture named 'generate_test_data'.
# 3. Use the @pytest.fixture decorator, adding (autouse=True) if you want it to run automatically. So it will run before each test.
#       i.e. @pytest.fixture(autouse=True)
# 4. Implement the fixture to call the data generator lambda function.

# TODO: Uncomment fixture generate_test_data
#       i.e. use the boto3 client to invoke the lambda function:

# @pytest.fixture()
# def generate_test_data(lambda_client, data_generator_function_name, raw_bucket):
#     """
#     Fixture to generate test data by invoking the data generator Lambda function.
#     This fixture runs automatically before each test.
#     """
#     # Invoke the data generator Lambda function
#     response = lambda_client.invoke(
#         FunctionName=data_generator_function_name,
#         InvocationType='RequestResponse',
#         Payload=json.dumps({"s3_bucket": raw_bucket})
#     )
# #     # 5. Assert that the data generator lambda function was called successfully.
# #     #       i.e. assert that the lambda function was called successfully by checking the response from the lambda function.
# #     # TODO: assert lambda response, look at test_lambda_raw_clean.py for reference,
# #     assert ...

# TODO: Remove unused fixtures from conftest.py
# 6. In test_lambda_raw_clean.py, remove any fixture definitions that were moved to conftest.py.
#     # The fixture doesn't need to return anything as it's used for its side effects

# TODO: What if we need to tear down or clean our test data after the test?
# We will use yield fixtures, which allow us to run teardown code after the test completes.

# Once pytest figures out a linear order for the fixtures,
# it will run each one up until it returns or yields,
# and then move on to the next fixture in the list to do the same thing.
# Check this fixture that will be used on exercise 3 to create invalid data and clean it after the test is done.

# @pytest.fixture
# def mock_patient_data(s3_client, raw_bucket):
#     # Mock raw data files with one valid and one invalid file
#     valid_data = json.dumps([{"patient_id": "633b64fb-2097-4abe-8707-bd9bdfaa6dc9", "name": "Cassandra Morgan",
#                               "date_of_birth": "1981-05-22",
#                               "address": "96948 Edward Lodge Suite 544, North Christopher, IL 87380",
#                               "phone_number": "369.136.3325x60629",
#                               "email": "lcarlson@example.net", "insurance_provider": "Dunn LLC", "policy_number": "fHL-48108220", "policy_valid_till": "2025-03-02T17:51:13.360906", "record_created_at": "2024-11-08T17:51:13.360923", "record_updated_at": "2024-11-08T17:51:13.360925"}])
#     invalid_data = json.dumps([{"patient_id": "633b64fb-2097-4abe-8707-bd9bdfaa6dc9", "name": "Cassandra Morgan", "date_of_birth": "invalid", "address": "96948 Edward Lodge Suite 544, North Christopher, IL 87380", "phone_number": "invalid", "email": "invalid", "insurance_provider": "Dunn LLC", "policy_number": "fHL-48108220", "policy_valid_till": "2025-03-02T17:51:13.360906", "record_created_at": "invalid", "record_updated_at": "invalid"}])
#     current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
#
#     valid_key = f'patients/patients_{current_datetime}_valid.json'
#     invalid_key = f'patients/patients_{current_datetime}_invalid.json'
#
#     s3_client.put_object(Bucket=raw_bucket, Key=valid_key, Body=valid_data)
#     s3_client.put_object(Bucket=raw_bucket, Key=invalid_key, Body=invalid_data)
#
#     yield
#
#     # Delete the created patient files
#     s3_client.delete_object(Bucket=raw_bucket, Key=valid_key)
#     s3_client.delete_object(Bucket=raw_bucket, Key=invalid_key)




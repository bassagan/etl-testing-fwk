import pytest
import json
import time
import boto3
import os
from botocore.exceptions import ClientError

# @pytest.fixture(scope="module")
# def aws_clients():
#     # This can be module scope since the clients can be reused
#     return {
#         'sns': boto3.client('sns', region_name='eu-west-1'),
#         'lambda': boto3.client('lambda', region_name='eu-west-1')
#     }

# @pytest.fixture(scope="module")
# def sns_topic_arn():
#     # This can also be module scope if it doesn't change between tests
#     return os.getenv('SNS_TOPIC_ARN', 'arn:aws:sns:eu-west-1:087559609246:etl-notifications-conference-user-2661cb9d')

# @pytest.fixture(scope="module")
# def lambda_function_name():
#     # Module scope if it's constant for all tests
#     return "raw_clean_lmb-conference-user-2661cb9d"

#     # Function scope is appropriate here as it modifies state
#     sns_client = aws_clients['sns']
#     try:
#         # List all subscriptions for the topic
#         subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=sns_topic_arn)['Subscriptions']
        
#         # Unsubscribe from each subscription
#         for subscription in subscriptions:
#             sns_client.unsubscribe(SubscriptionArn=subscription['SubscriptionArn'])
        
#         # Delete the topic
#         sns_client.delete_topic(TopicArn=sns_topic_arn)
        
#         # Recreate the topic
#         new_topic = sns_client.create_topic(Name=sns_topic_arn.split(':')[-1])
        
#         # Resubscribe to the new topic
#         for subscription in subscriptions:
#             sns_client.subscribe(
#                 TopicArn=new_topic['TopicArn'],
#                 Protocol=subscription['Protocol'],
#                 Endpoint=subscription['Endpoint']
#             )
#     except ClientError as e:
#         print(f"Error clearing SNS notifications: {e}")
#         raise
#     yield

#     # Function scope for cleanup
#     s3_client = aws_clients['s3']
#     # Delete all objects in the bucket
#     response = s3_client.list_objects_v2(Bucket=bucket_name)
#     if 'Contents' in response:
#         for obj in response['Contents']:
#             s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
#     yield

# @pytest.fixture(scope="module")
# def clear_sns_notifications():
#     sns_client = aws_clients['sns']
#     try:
#         # List all subscriptions for the topic
#         subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=sns_topic_arn)['Subscriptions']
        
#         # Unsubscribe from each subscription
#         for subscription in subscriptions:
#             sns_client.unsubscribe(SubscriptionArn=subscription['SubscriptionArn'])
        
#         # Delete the topic
#         sns_client.delete_topic(TopicArn=sns_topic_arn)
        
#         # Recreate the topic
#         new_topic = sns_client.create_topic(Name=sns_topic_arn.split(':')[-1])
        
#         # Resubscribe to the new topic
#         for subscription in subscriptions:
#             sns_client.subscribe(
#                 TopicArn=new_topic['TopicArn'],
#                 Protocol=subscription['Protocol'],
#                 Endpoint=subscription['Endpoint']
#             )
#     except ClientError as e:
#         print(f"Error clearing SNS notifications: {e}")
#         raise

#     return clear_sns_notifications

# @pytest.fixture(scope="function")
# def prepare_s3_bucket(aws_clients, bucket_name):
#     # Function scope as it modifies bucket state
#     s3_client = aws_clients['s3']
#     # Generate and upload fake data to S3
#     fake_data = json.dumps({"test_key": "test_value"})
#     s3_client.put_object(Bucket=bucket_name, Key="test_file.json", Body=fake_data)
#     yield
#     # Add cleanup code here if needed

# @pytest.fixture(scope="function")
# def clean_s3_bucket(aws_clients, bucket_name):
#     # Function scope for cleanup
#     s3_client = aws_clients['s3']
#     # Delete all objects in the bucket
#     response = s3_client.list_objects_v2(Bucket=bucket_name)
#     if 'Contents' in response:
#         for obj in response['Contents']:
#             s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
#     yield
    
# @pytest.fixture(autouse=True)
# def setup_and_teardown(clear_sns_notifications, prepare_s3_bucket, clean_s3_bucket):
#         # Setup: Ensure a clean state before each test
#         clear_sns_notifications()
#         prepare_s3_bucket()
#         yield
#         # Teardown: Clean up after each test
#         clear_sns_notifications()
#         clean_s3_bucket()

os.environ['no_proxy'] = '*'
class TestSNSNotifications:
   
    @pytest.mark.parametrize("invocation_type", ["RequestResponse"])
    def test_lambda_execution(self, invocation_type):
        # Arrange
        print("Invoking Lambda function")
        lambda_client = boto3.client("lambda", region_name='eu-west-1')
        event = {
            'source_bucket': 'raw-s3-conference-user-2661cb9d-o8mdtsgg',
            'destination_bucket': 'clean-s3-conference-user-2661cb9d-o8mdtsgg'
        }

        # Act
        response = lambda_client.invoke(
            FunctionName="raw_clean_lmb-conference-user-2661cb9d",
            InvocationType=invocation_type,
            Payload=json.dumps(event)
        )

        # Assert
        lambda_output = json.loads(response['Payload'].read().decode("utf-8"))
        assert 'statusCode' in lambda_output, "Expected 'statusCode' not found in Lambda output"
        assert lambda_output['statusCode'] == 200, f"Lambda execution failed with status code {lambda_output['statusCode']}"
        
        body = json.loads(lambda_output['body'])
        assert 'message' in body, "Expected 'message' not found in Lambda output body"
        assert body['message'] == "Data processing complete.", "Unexpected message in Lambda output"
        assert 'patients_count' in body, "Expected 'patients_count' not found in Lambda output body"
        assert 'visits_count' in body, "Expected 'visits_count' not found in Lambda output body"

    # def test_sns_notifications_received(self, aws_clients, sns_topic_arn, lambda_function_name):
    #     # Arrange
    #     sns_client = aws_clients['sns']
    #     lambda_client = aws_clients['lambda']

    #     # Act
    #     lambda_client.invoke(FunctionName=lambda_function_name, InvocationType="Event")
    #     notifications_received = self.poll_for_sns_notifications(sns_client, sns_topic_arn)

    #     # Assert
    #     assert notifications_received, "Failed to receive SNS notifications"

    # def test_sns_subscriptions_active(self, aws_clients, sns_topic_arn):
    #     # Arrange
    #     sns_client = aws_clients['sns']

    #     # Act
    #     subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=sns_topic_arn)

    #     # Assert
    #     assert 'Subscriptions' in subscriptions, "No subscriptions found for the SNS topic"
    #     assert len(subscriptions['Subscriptions']) > 0, "No active subscriptions found for the SNS topic"

    #     for subscription in subscriptions['Subscriptions']:
    #         assert subscription['SubscriptionArn'] != 'PendingConfirmation', f"Subscription {subscription['SubscriptionArn']} is still pending confirmation"

    # @pytest.mark.timeout(40)
    # def poll_for_sns_notifications(self, sns_client, topic_arn, timeout=30, interval=2):
    #     start_time = time.time()
    #     while time.time() - start_time < timeout:
    #         try:
    #             # Check for active subscriptions
    #             subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
                
    #             if 'Subscriptions' in subscriptions and subscriptions['Subscriptions']:
    #                 for subscription in subscriptions['Subscriptions']:
    #                     if subscription['SubscriptionArn'] != 'PendingConfirmation':
    #                         # Verify timing with 1 second tolerance
    #                         pytest.approx(time.time() - start_time, abs=1)
    #                         return True  # Active subscription found
                
    #             time.sleep(interval)
    #         except ClientError as e:
    #             pytest.fail(f"Error polling SNS: {e}")

    #     return False  # No active subscriptions found within timeout



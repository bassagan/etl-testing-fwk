import boto3
import csv
import os
import uuid
import secrets
import string
import json
import time

# Initialize AWS clients
iam_client = boto3.client('iam')
s3_client = boto3.client('s3')
ssm_client = boto3.client('ssm')
ec2_client = boto3.client('ec2')
resource_tagging_client = boto3.client('resourcegroupstaggingapi')
lambda_client = boto3.client('lambda')
athena_client = boto3.client('athena')
dynamodb_client = boto3.client('dynamodb')
sns_client = boto3.client('sns')
codepipeline_client = boto3.client('codepipeline')
codebuild_client = boto3.client('codebuild')
codestar_client = boto3.client('codestar-connections')
events_client = boto3.client('events')


def lambda_handler(event, context):
    operation = event.get('operation')
    account_count = event.get('account_count', 1)
    s3_bucket = event.get('s3_bucket')
    target_destroy_user = event.get('destroy_user')

    if operation == 'create':
        response = handle_create_operation(account_count, s3_bucket)
    elif operation == 'destroy':
        response = handle_destroy_operation(target_destroy_user)
    else:
        response = {
            'statusCode': 400,
            'body': f'Unknown operation: {operation}'
        }

    return response


def handle_create_operation(account_count, s3_bucket):
    accounts = create_accounts(account_count)
    csv_file_path = generate_csv(accounts)
    s3_url = upload_to_s3(csv_file_path, s3_bucket)
    return {
        'statusCode': 200,
        'body': {
            'message': 'Accounts created successfully',
            'csv_url': s3_url
        }
    }


def handle_destroy_operation(target_destroy_user):
    destroy_accounts(target_destroy_user)
    return {
        'statusCode': 200,
        'body': 'Accounts destroyed successfully'
    }


def create_accounts(count):
    accounts = []
    account_id = boto3.client('sts').get_caller_identity().get('Account')

    for i in range(count):
        console_user_name = f"conference-user-{i}"
        service_user_name = f"service-conference-user-{i}"
        user = {}
        # Check if the console user already exists
        if user_exists(console_user_name):
            print(f"User {console_user_name} already exists. Skipping creation.")
        else:
            user = create_console_user(console_user_name, account_id)

        # Check if the service user already exists
        if user_exists(service_user_name):
            print(f"User {service_user_name} already exists. Skipping creation.")
        else:
            user.update(create_service_user(service_user_name))
        accounts.append(user)
    return accounts


def user_exists(user_name):
    """Checks if a user already exists."""
    try:
        iam_client.get_user(UserName=user_name)
        return True
    except iam_client.exceptions.NoSuchEntityException:
        return False


def create_console_user(user_name, account_id):
    """Creates a console user with login profile and attaches necessary policies."""
    iam_client.create_user(UserName=user_name)

    # Generate a random password for the console user
    password = generate_random_password()

    iam_client.create_login_profile(
        UserName=user_name,
        Password=password,
        PasswordResetRequired=False  # Require password change on first login
    )

    # Attach the policy that allows the user to change their password
    attach_password_change_policy(user_name)

    # Attach policy allowing the user to assume the restricted-user-role
    attach_custom_policy(user_name)

    # Attach policy allowing the user to assume the restricted-user-role
    attach_assume_role_policy(user_name, 'restricted-user-role')

    # Store the account and user information
    login_url = f"https://{account_id}.signin.aws.amazon.com/console"
    account_info = {
        'account_id': account_id,
        'user_name': user_name,
        'password': password,
        'login_url': login_url
    }
    return account_info


def attach_assume_role_policy(user_name, role_name):
    """Attaches a policy allowing the user to assume a specific role."""
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": f"arn:aws:iam::{boto3.client('sts').get_caller_identity().get('Account')}:role/{role_name}"
            }
        ]
    }
    iam_client.put_user_policy(
        UserName=user_name,
        PolicyName='AssumeRestrictedUserRolePolicy',
        PolicyDocument=json.dumps(assume_role_policy)
    )


def create_service_user(user_name):
    """Creates a service user with access keys for programmatic access and tags the user as a service user."""
    iam_client.create_user(UserName=user_name)

    # Tag the user as a service user
    iam_client.tag_user(
        UserName=user_name,
        Tags=[
            {
                'Key': 'UserType',
                'Value': 'service'
            }
        ]
    )

    # Create access keys for the service user
    access_keys = iam_client.create_access_key(UserName=user_name)

    attach_custom_service_policy(user_name=user_name)

    # Store the service user's access keys
    account_info = {
        'access_key_id': access_keys['AccessKey']['AccessKeyId'],
        'secret_access_key': access_keys['AccessKey']['SecretAccessKey']
    }
    return account_info


def generate_random_password(length=12):
    """Generates a random password with a mix of letters, digits, and symbols."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            break
    return password


def attach_custom_policy(user_name):
    policy_arn = "arn:aws:iam::087559609246:policy/UserRestrictedPolicyLambda"  # Replace with your custom policy ARN
    iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )
    policy_arn = "arn:aws:iam::087559609246:policy/UserRestrictedPolicyAthena"  # Replace with your custom policy ARN
    iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )
    policy_arn = "arn:aws:iam::087559609246:policy/UserRestrictedPolicyS3"  # Replace with your custom policy ARN
    iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )
    policy_arn = "arn:aws:iam::087559609246:policy/UserRestrictedPolicyEventbridge"  # Replace with your custom policy ARN
    iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )
    policy_arn = "arn:aws:iam::087559609246:policy/UserRestrictedPolicyDynamoDB"  # Replace with your custom policy ARN
    iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )
    policy_arn = "arn:aws:iam::087559609246:policy/UserRestrictedPolicyCICD"  # Replace with your custom policy ARN
    iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )


def attach_custom_service_policy(user_name):
    policy_arn = "arn:aws:iam::087559609246:policy/ServiceUserRestrictedPolicy"  # Replace with your custom policy ARN
    iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )


def attach_password_change_policy(user_name):
    """Attaches a policy allowing password changes."""
    password_change_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "iam:ChangePassword",
                "Resource": f"arn:aws:iam::{boto3.client('sts').get_caller_identity().get('Account')}:user/{user_name}"
            }
        ]
    }
    iam_client.put_user_policy(
        UserName=user_name,
        PolicyName='AllowChangePassword',
        PolicyDocument=json.dumps(password_change_policy)
    )


def generate_csv(accounts):
    """Generates a CSV file with the account information."""
    csv_file_path = f"/tmp/accounts_{uuid.uuid4()}.csv"
    with open(csv_file_path, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Account ID', 'User Name', 'Password', 'Access Key ID', 'Secret Access Key', 'Login URL'])
        for account in accounts:
            writer.writerow([
                account.get('account_id', ''),
                account.get('user_name', ''),
                account.get('password', ''),
                account.get('access_key_id', ''),
                account.get('secret_access_key', ''),
                account.get('login_url', '')
            ])

    return csv_file_path


def upload_to_s3(csv_file_path, s3_bucket):
    """Uploads the CSV file to S3 and generates a presigned URL."""
    s3_key = os.path.basename(csv_file_path)
    s3_client.upload_file(csv_file_path, s3_bucket, s3_key)

    # Generate a presigned URL for downloading the file
    s3_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': s3_bucket, 'Key': s3_key}, ExpiresIn=3600)
    return s3_url


def destroy_accounts(target_user_name=None):
    """Deletes all conference users and their associated Terraform-managed resources, or a single user."""
    users = iam_client.list_users()

    for user in users['Users']:
        user_name = user['UserName']

        # Check if we should target a single user or all users
        if target_user_name and user_name != target_user_name:
            continue

        # Check if the user has the "conference-user-" or "service-conference-user-" prefix
        if user_name.startswith("conference-user-") or user_name.startswith("service-conference-user-"):
            print(f"Deleting user: {user_name}")

            # Destroy all tagged resources
            destroy_tagged_resources(user_name)

            # Delete all access keys associated with the user
            access_keys = iam_client.list_access_keys(UserName=user_name)
            for key in access_keys['AccessKeyMetadata']:
                iam_client.delete_access_key(UserName=user_name, AccessKeyId=key['AccessKeyId'])

            # Delete the login profile associated with the user
            try:
                iam_client.delete_login_profile(UserName=user_name)
            except iam_client.exceptions.NoSuchEntityException:
                print(f"No login profile found for {user_name}, skipping.")

            # Delete the inline policy allowing password change
            try:
                iam_client.delete_user_policy(UserName=user_name, PolicyName='AllowChangePassword')
            except iam_client.exceptions.NoSuchEntityException:
                print(f"No inline policy found for {user_name}, skipping.")

                # Detach all managed policies attached to the user
                attached_policies = iam_client.list_attached_user_policies(UserName=user_name)
                for policy in attached_policies['AttachedPolicies']:
                    print(f"Atached policies for {user_name}: {policy}")
                    iam_client.detach_user_policy(UserName=user_name, PolicyArn=policy['PolicyArn'])

                # Delete all inline policies attached to the user
                inline_policies = iam_client.list_user_policies(UserName=user_name)
                for policy_name in inline_policies['PolicyNames']:
                    print(f"Inline policies for {user_name}: {policy_name}")
                    iam_client.delete_user_policy(UserName=user_name, PolicyName=policy_name)

                # Finally, delete the user
                try:
                    iam_client.delete_user(UserName=user_name)
                    print(f"User {user_name} deleted successfully.")
                except iam_client.exceptions.DeleteConflictException as e:
                    print(f"Error deleting user {user_name}: {e}")

    return {
        'statusCode': 200,
        'body': 'All conference users deleted successfully'
    }


def destroy_tagged_resources(user_name):
    """Destroys all resources with the tag 'Owner' set to the user_name."""
    paginator = resource_tagging_client.get_paginator('get_resources')

    response_iterator = paginator.paginate(
        TagFilters=[
            {
                'Key': 'Owner',
                'Values': [user_name]
            }
        ]
    )

    for page in response_iterator:
        for resource_tag_mapping in page['ResourceTagMappingList']:
            resource_arn = resource_tag_mapping['ResourceARN']
            service_name = resource_arn.split(":")[2]
            resource_id = resource_arn.split("/")[-1]

            print(f"Found tagged resource: {resource_arn} for user {user_name}")

            if service_name == 's3':
                bucket_name = resource_arn.split(":")[-1]
                delete_s3_bucket(bucket_name)

            elif service_name == 'lambda':
                lambda_client.delete_function(FunctionName=resource_id)
                print(f"Lambda function {resource_id} deleted.")

            elif service_name == 'athena':
                delete_athena_resources(resource_id)

            elif service_name == 'dynamodb':
                dynamodb_client.delete_table(TableName=resource_id)
                print(f"DynamoDB table {resource_id} deleted.")

            elif service_name == 'sns':
                sns_client.delete_topic(TopicArn=resource_arn)
                print(f"SNS topic {resource_arn} deleted.")

            elif service_name == 'codepipeline':
                codepipeline_client.delete_pipeline(name=resource_id)
                print(f"CodePipeline {resource_id} deleted.")

            elif service_name == 'codebuild':
                codebuild_client.delete_project(name=resource_id)
                print(f"CodeBuild project {resource_id} deleted.")

            elif service_name == 'events':
                # Detach targets from the rule before deletion
                rule_targets = events_client.list_targets_by_rule(Rule=resource_id)
                target_ids = [target['Id'] for target in rule_targets['Targets']]
                if target_ids:
                    events_client.remove_targets(Rule=resource_id, Ids=target_ids)
                    print(f"Removed targets from EventBridge rule {resource_id}.")
                events_client.delete_rule(Name=resource_id)
                print(f"EventBridge rule {resource_id} deleted.")

            elif service_name == 'codestar-connections':
                codestar_client.delete_connection(ConnectionArn=resource_arn)
                print(f"CodeStar connection {resource_arn} deleted.")


def delete_s3_bucket(bucket_name):
    """Delete all objects in an S3 bucket and then the bucket itself."""
    try:
        # First delete all objects in the bucket
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f"Deleted all objects in S3 bucket {bucket_name}.")

        # Now delete the bucket
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"S3 bucket {bucket_name} deleted.")
    except Exception as e:
        print(f"Error deleting S3 bucket {bucket_name}: {e}")


def delete_athena_resources(resource_id):
    """Delete Athena databases or workgroups by ARN."""
    try:
        if resource_id.startswith('workgroup/'):
            athena_client.delete_workgroup(WorkGroup=resource_id.split('/')[-1], RecursiveDeleteOption=True)
            print(f"Athena workgroup {resource_id} deleted.")
        elif resource_id.startswith('database/'):
            database_name = resource_id.split('/')[-1]
            # Deleting database in Athena requires first dropping all tables
            athena_client.start_query_execution(
                QueryString=f"DROP DATABASE {database_name} CASCADE",
                ResultConfiguration={'OutputLocation': 's3://your-output-bucket/'}
                # Replace with your actual output location
            )
            print(f"Athena database {database_name} deletion initiated.")
    except Exception as e:
        print(f"Error deleting Athena resource {resource_id}: {e}")



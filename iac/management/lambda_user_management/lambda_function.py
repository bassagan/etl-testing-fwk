import boto3
import csv
import os
import uuid
import secrets
import string
import json

# Initialize AWS clients
iam_client = boto3.client('iam')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    operation = event.get('operation')
    account_count = event.get('account_count', 1)
    s3_bucket = event.get('s3_bucket')

    if operation == 'create':
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

    elif operation == 'destroy':
        destroy_accounts()

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
        PasswordResetRequired=True  # Require password change on first login
    )

    # Attach the policy that allows the user to change their password
    attach_password_change_policy(user_name)

    # Attach a custom policy that allows access to specific resources
    attach_custom_policy(user_name)

    # Store the account and user information
    login_url = f"https://{account_id}.signin.aws.amazon.com/console"
    account_info = {
        'account_id': account_id,
        'user_name': user_name,
        'password': password,
        'login_url': login_url
    }
    return account_info
    # accounts.append(account_info)


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
    # accounts.append(account_info)


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
    policy_arn = "arn:aws:iam::087559609246:policy/UserRestrictedPolicy"  # Replace with your custom policy ARN
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


def destroy_accounts():
    """Deletes all conference users."""
    users = iam_client.list_users()

    for user in users['Users']:
        user_name = user['UserName']

        # Check if the user has the "conference-user-" or "service-conference-user-" prefix
        if user_name.startswith("conference-user-") or user_name.startswith("service-conference-user-"):
            print(f"Deleting user: {user_name}")

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

            # Detach any attached policies
            attached_policies = iam_client.list_attached_user_policies(UserName=user_name)
            for policy in attached_policies['AttachedPolicies']:
                iam_client.detach_user_policy(UserName=user_name, PolicyArn=policy['PolicyArn'])

            # Delete the user
            iam_client.delete_user(UserName=user_name)
            print(f"User {user_name} deleted successfully.")

    return {
        'statusCode': 200,
        'body': 'All conference users deleted successfully'
    }

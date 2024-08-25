import boto3
import os
import secrets
import string
import json

# Initialize AWS clients
iam_client = boto3.client('iam')

# Get account ID from environment variable
ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID', '087559609246')

def lambda_handler(event, context):
    # Check if it's a GET request
    if event['requestContext']['http']['method'] == 'GET':
        try:
            # Create user
            user_info = create_user()

            return {
                'statusCode': 200,
                'body': json.dumps(user_info),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

def create_user():
    account_id = ACCOUNT_ID

    suffix = os.urandom(4).hex()
    console_user_name = f"conference-user-{suffix}"
    service_user_name = f"service-conference-user-{suffix}"
    if user_exists(console_user_name) or user_exists(service_user_name):
        raise Exception("User already exists. Try again.")

    user = create_console_user(console_user_name, account_id)
    user.update(create_service_user(service_user_name))
    return user

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
        PasswordResetRequired=False
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
                "Resource": f"arn:aws:iam::{ACCOUNT_ID}:role/{role_name}"
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
                "Resource": f"arn:aws:iam::{ACCOUNT_ID}:user/{user_name}"
            }
        ]
    }
    iam_client.put_user_policy(
        UserName=user_name,
        PolicyName='AllowChangePassword',
        PolicyDocument=json.dumps(password_change_policy)
    )
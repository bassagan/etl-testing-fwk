import boto3
import os
import secrets
import string
import json
import urllib.parse
import csv
import io

# Initialize AWS clients
iam_client = boto3.client('iam')
resource_groups_client = boto3.client('resource-groups')

# Get account ID from environment variable
ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID', '087559609246')

def lambda_handler(event, context):
    # Check if it's a GET request
    if event['requestContext']['http']['method'] == 'GET':
        try:
            # Create user and get information
            user_info, resource_group_url = create_user()

            # Generate HTML content
            html_content = generate_html_response(user_info, resource_group_url)

            return {
                'statusCode': 200,
                'body': html_content,
                'headers': {
                    'Content-Type': 'text/html'
                }
            }
        except Exception as e:
            error_html = f"""
            <html>
                <head>
                    <title>ETL Testing Framework - Error</title>
                </head>
                <body>
                    <h1>Error</h1>
                    <p>{str(e)}</p>
                </body>
            </html>
            """
            return {
                'statusCode': 500,
                'body': error_html,
                'headers': {
                    'Content-Type': 'text/html'
                }
            }
    else:
        method_not_allowed_html = """
        <html>
            <head>
                <title>ETL Testing Framework - Method Not Allowed</title>
            </head>
            <body>
                <h1>Method Not Allowed</h1>
                <p>This endpoint only supports GET requests.</p>
            </body>
        </html>
        """
        return {
            'statusCode': 405,
            'body': method_not_allowed_html,
            'headers': {
                'Content-Type': 'text/html'
            }
        }

def generate_html_response(user_info, resource_group_url):
    # Prepare CSV data
    csv_data = io.StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['Field', 'Value'])
    for key, value in user_info.items():
        writer.writerow([key, value])
    writer.writerow(['Resource Group URL', resource_group_url])
    csv_string = csv_data.getvalue()

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ETL Testing Framework</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(to bottom, #1E34B2, #152164);
            }}
            .logo {{
                display: block;
                margin: 0 auto 20px;
                max-width: 100%;
                height: auto;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                color: #333333;
            }}
            h1, h2 {{
                color: #1E34B2;
                text-align: center;
                margin-bottom: 10px;
            }}
            .info-box {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 10px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
            }}
            .info-item {{
                margin-bottom: 5px;
            }}
            .info-box a {{
                color: #1E34B2;
            }}
            .warning {{
                color: #721c24;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 20px;
            }}
            .btn {{
                background-color: #1E34B2;
                color: #ffffff;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin-top: 10px;
            }}
            .copy-btn {{
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 3px 6px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 10px;
                margin-left: 5px;
                cursor: pointer;
                border-radius: 3px;
            }}
            .url-section {{
                margin-top: 20px;
                border-top: 1px solid #e9ecef;
                padding-top: 20px;
            }}
            .url-box {{
                background-color: #e9ecef;
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }}
            .url-box a {{
                color: #0056b3;
                word-break: break-all;
            }}
            small {{
                color: #666666;
                display: block;
                font-size: 0.8em;
            }}
        </style>
        <script>
            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text).then(function() {{
                    alert('Copied to clipboard!');
                }}, function(err) {{
                    console.error('Could not copy text: ', err);
                }});
            }}
        </script>
    </head>
    <body>
        <img src="https://automation.eurostarsoftwaretesting.com/wp-content/uploads/2024/07/AutomationSTAR-Vienna-Design-Colour.webp" alt="AutomationSTAR Vienna Logo" class="logo">
        <div class="container">
            <h1>ETL Testing Framework</h1>
            <h2>"Here's your AWS User details - may the tests be ever in your favor!"</h2>

            <div class="info-box">
                <div class="info-item">
                    <strong>Account ID:</strong> {user_info['account_id']} <button class="copy-btn" onclick="copyToClipboard('{user_info['account_id']}')">Copy</button>
                    <small>The unique identifier for your AWS account.</small>
                </div>
                <div class="info-item">
                    <strong>Username:</strong> {user_info['user_name']} <button class="copy-btn" onclick="copyToClipboard('{user_info['user_name']}')">Copy</button>
                    <small>Use this to log in to the AWS Management Console.</small>
                </div>
                <div class="info-item">
                    <strong>Password:</strong> {user_info['password']} <button class="copy-btn" onclick="copyToClipboard('{user_info['password']}')">Copy</button>
                    <small>The password for your AWS Management Console login.</small>
                </div>
                <div class="info-item">
                    <strong>Access Key ID:</strong> {user_info['access_key_id']} <button class="copy-btn" onclick="copyToClipboard('{user_info['access_key_id']}')">Copy</button>
                    <small>Used for programmatic access to AWS services.</small>
                </div>
                <div class="info-item">
                    <strong>Secret Access Key:</strong> {user_info['secret_access_key']} <button class="copy-btn" onclick="copyToClipboard('{user_info['secret_access_key']}')">Copy</button>
                    <small>The "password" for your Access Key ID. Keep this secret!</small>
                </div>
                <div class="info-item">
                    <a href="data:text/csv;charset=utf-8,{urllib.parse.quote(csv_string)}" download="user_info.csv" class="btn" style="color: white;">Download CSV</a>
                </div>
                
            </div>
            
            <div class="url-section">
                <div class="url-box">
                    <p><strong>Login to AWS:</strong></p>
                    <a href="{user_info['login_url']}" target="_blank">Click here to access the AWS Management Console</a>
                </div>
                
                <div class="url-box">
                    <p><strong>AWS Resources:</strong></p>
                    <a href="{resource_group_url}" target="_blank">Click here to see your AWS resources after you create them</a>
                </div>
            </div>
            <div class="warning">
                <p><strong>Important:</strong> This AWS user will be deleted after the tutorial. Please save any important information before the session ends.</p>
            </div>
            
        </div>
    </body>
    </html>
    """
    return html_content

def create_user():
    account_id = ACCOUNT_ID

    suffix = os.urandom(4).hex()
    console_user_name = f"conference-user-{suffix}"
    service_user_name = f"service-conference-user-{suffix}"
    if user_exists(console_user_name) or user_exists(service_user_name):
        raise Exception("User already exists. Try again.")

    user = create_console_user(console_user_name, account_id)
    user.update(create_service_user(service_user_name))
    # Create a resource group for the console user
    resource_group_url = create_resource_group_for_user(console_user_name)

    return user, resource_group_url


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
    # New Resource Group policy
    policy_arn = "arn:aws:iam::087559609246:policy/UserRestrictedPolicyResourceGroups"  # Replace with your custom policy ARN
    iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )
    # New Tagging policy
    policy_arn = "arn:aws:iam::087559609246:policy/UserRestrictedPolicyTagging"  # Replace with your custom policy ARN
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

def create_resource_group_for_user(user_name):
    """Creates a resource group for the user based on the Owner tag and returns the console URL."""
    group_name = f"{user_name}-resources"
    resource_query = {
        'ResourceTypeFilters': [
            'AWS::AllSupported'
        ],
        'TagFilters': [
            {
                'Key': 'Owner',
                'Values': [user_name]
            }
        ]
    }

    try:
        response = resource_groups_client.create_group(
            Name=group_name,
            Description=f"Resources owned by {user_name}",
            ResourceQuery={
                'Type': 'TAG_FILTERS_1_0',
                'Query': json.dumps(resource_query)
            }
        )
        print(f"Created resource group: {group_name}")

        # Generate the console URL for the resource group
        encoded_group_name = urllib.parse.quote(group_name)
        console_url = f"https://console.aws.amazon.com/resource-groups/group/{encoded_group_name}?region={resource_groups_client.meta.region_name}"
        return console_url
    except resource_groups_client.exceptions.BadRequestException as e:
        print(f"Error creating resource group: {str(e)}")
        return None
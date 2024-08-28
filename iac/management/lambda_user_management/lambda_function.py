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

# Add this constant at the top of the file
DESTROY_KEY = os.environ.get('DESTROY_KEY', 'default_destroy_key')

def lambda_handler(event, context):
    # Check if it's a GET request
    if event['requestContext']['http']['method'] == 'GET':
        path = event['requestContext']['http']['path']
        
        if path == '/destroy':
            # Check for the destroy key
            query_params = event.get('queryStringParameters', {})
            if query_params and query_params.get('key') == DESTROY_KEY:
                try:
                    destroy_users()
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'message': 'All users destroyed successfully'}),
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
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Invalid or missing destroy key'}),
                    'headers': {
                        'Content-Type': 'application/json'
                    }
                }
        else:
            # Existing code for creating users
            try:
                user_info, resource_group_url = create_user()
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
    """Creates a console user with login profile."""
    iam_client.create_user(UserName=user_name)

    # Generate a random password for the console user
    password = generate_random_password()

    iam_client.create_login_profile(
        UserName=user_name,
        Password=password,
        PasswordResetRequired=False
    )

    # Store the account and user information
    login_url = f"https://{account_id}.signin.aws.amazon.com/console"
    account_info = {
        'account_id': account_id,
        'user_name': user_name,
        'password': password,
        'login_url': login_url
    }
    return account_info


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
    """Generates a random password with a mix of letters, digits, and allowed symbols."""
    alphabet = string.ascii_letters + string.digits + "*!?_-"
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "*!?_-" for c in password)):
            break
    return password


def attach_custom_service_policy(user_name):
    policy_arn = "arn:aws:iam::087559609246:policy/ServiceUserRestrictedPolicy"  # Replace with your custom policy ARN
    iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
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

def destroy_users():
    """Destroy all service and console users and their associated resources."""
    deleted_users = []
    users = iam_client.list_users()['Users']
    for user in users:
        user_name = user['UserName']
        if user_name.startswith('conference-user-') or user_name.startswith('service-conference-user-'):
     
            # Delete access keys
            access_keys = iam_client.list_access_keys(UserName=user_name)['AccessKeyMetadata']
            for key in access_keys:
                iam_client.delete_access_key(UserName=user_name, AccessKeyId=key['AccessKeyId'])
            
            # Delete login profile if it exists
            try:
                iam_client.delete_login_profile(UserName=user_name)
            except iam_client.exceptions.NoSuchEntityException:
                pass
            
            # Detach all managed policies
            attached_policies = iam_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
            for policy in attached_policies:
                iam_client.detach_user_policy(UserName=user_name, PolicyArn=policy['PolicyArn'])
            
            # Delete all inline policies
            inline_policies = iam_client.list_user_policies(UserName=user_name)['PolicyNames']
            for policy_name in inline_policies:
                iam_client.delete_user_policy(UserName=user_name, PolicyName=policy_name)
            
            # Delete the user
            iam_client.delete_user(UserName=user_name)
            deleted_users.append(user_name)
    
    # Delete resource groups
    groups = resource_groups_client.list_groups()['GroupIdentifiers']
    for group in groups:
        if group['Name'].startswith('conference-user-') or group['Name'].startswith('service-conference-user-'):
            resource_groups_client.delete_group(GroupName=group['Name'])
    
    return deleted_users


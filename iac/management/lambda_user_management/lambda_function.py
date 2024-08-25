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
ec2_client = boto3.client('ec2')  # Example for EC2
resource_tagging_client = boto3.client('resourcegroupstaggingapi')  # AWS Resource Groups Tagging API
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
        accounts = create_accounts(account_count)
        csv_file_path = generate_csv(accounts)
        s3_url = upload_to_s3(csv_file_path, s3_bucket)
        user_name = event.get('user_name', None)  # Add user_name parameter for targeted deletion

        return {
            'statusCode': 200,
            'body': {
                'message': 'Accounts created successfully',
                'csv_url': s3_url
            }
        }

    elif operation == 'destroy':
        destroy_accounts(target_destroy_user)

        return {
            'statusCode': 200,
            'body': 'Accounts destroyed successfully'
        }
    elif operation == 'create_ssm_managed_instance':
        instance_id = create_ssm_managed_instance()
        return {
            'statusCode': 200,
            'body': f'SSM managed instance created with ID: {instance_id}'
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

            # Destroy all resources managed by Terraform
            destroy_terraform_resources(user_name)

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



def destroy_terraform_resources(user_name):
    """Destroys Terraform-managed resources for a specific user using SSM."""
    # Assuming the S3 bucket and DynamoDB table names follow a pattern based on the user_name
    s3_bucket_name = f"{user_name}-tf-backend-bucket"
    dynamodb_table_name = f"{user_name}-tf-backend-dynamodb"

    # Prepare the command to run Terraform destroy
    commands = [
        "aws s3 cp s3://{}/terraform.tfstate /tmp/terraform.tfstate".format(s3_bucket_name),
        "terraform init -backend=true -backend-config='bucket={}' -backend-config='key=terraform.tfstate' -backend-config='region=eu-west-1'".format(s3_bucket_name),
        "terraform destroy -auto-approve"
    ]

    # Send command to SSM
    response = ssm_client.send_command(
        InstanceIds=['<Your-Managed-Instance-ID>'],  # Replace with your managed instance ID
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': commands},
    )

    print(f"Terraform destroy command initiated for user {user_name}. Check SSM for execution status.")



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
                # Athena resource handling: delete database or workgroup if appropriate
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
                events_client.delete_rule(Name=resource_id, Force=True)
                print(f"EventBridge rule {resource_id} deleted.")

            elif service_name == 'codestar-connections':
                codestar_client.delete_connection(ConnectionArn=resource_arn)
                print(f"CodeStar connection {resource_arn} deleted.")

            # Continue adding handlers for each type of AWS service


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
            )
            print(f"Athena database {database_name} deleted.")
    except Exception as e:
        print(f"Error deleting Athena resource {resource_id}: {e}")

def create_ssm_managed_instance():
    """Creates an EC2 instance that is managed by AWS Systems Manager (SSM)."""
    # Create an IAM role for EC2 with SSM permissions
    role_name = 'EC2SSMManagedRole'
    instance_profile_name = 'EC2SSMInstanceProfile'

    try:
        # Create the IAM role for SSM
        iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "ec2.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }]
            })
        )

        # Attach the AmazonSSMManagedInstanceCore policy to the role
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
        )

        # Create instance profile
        iam_client.create_instance_profile(InstanceProfileName=instance_profile_name)

        # Add role to instance profile
        iam_client.add_role_to_instance_profile(
            InstanceProfileName=instance_profile_name,
            RoleName=role_name
        )

    except iam_client.exceptions.EntityAlreadyExistsException:
        print("Role or Instance Profile already exists. Skipping creation.")

    # Wait for the instance profile to be created and ready
    time.sleep(10)

    # User data script to install SSM agent (Amazon Linux 2 has it by default)
    user_data_script = """#!/bin/bash
    yum install -y aws-cli
    """

    # Launch the EC2 instance with the necessary IAM role
    response = ec2_client.run_instances(
        ImageId='ami-0c02fb55956c7d316',  # Amazon Linux 2 AMI (HVM) - Update with your region's AMI ID
        InstanceType='t2.micro',
        IamInstanceProfile={
            'Name': instance_profile_name
        },
        MinCount=1,
        MaxCount=1,
        UserData=user_data_script,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Owner', 'Value': 'ssm-managed-instance'}]
        }]
    )

    instance_id = response['Instances'][0]['InstanceId']

    # Wait for the instance to initialize and be managed by SSM
    print(f"Waiting for instance {instance_id} to be ready...")
    ec2_client.get_waiter('instance_status_ok').wait(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is ready and managed by SSM.")

    return instance_id

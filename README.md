# Exercise 1: Setting Up the Environment

Welcome to the first exercise of our ETL Testing Framework tutorial! In this exercise, you'll set up the necessary AWS infrastructure and local environment to begin working with the ETL testing framework.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Instructions](#step-by-step-instructions)
    - [1. AWS Account Setup](#1-aws-account-setup)
    - [2. Fork the Repository](#2-fork-the-repository)
    - [3. Environment Setup](#3-environment-setup)
    - [4. Terraform Initialization](#4-terraform-initialization)
    - [5. AWS Resource Verification](#5-aws-resource-verification)
4. [Common Issues and Tips](#common-issues-and-tips)
5. [Next Steps](#next-steps)

## Overview
In this exercise, you will:
- Set up your AWS account and configure your environment within GitHub Codespaces.
- Fork the GitHub repository and launch a Codespace.
- Initialize and deploy the infrastructure using Terraform.
- Verify that all necessary AWS resources have been created.

## Prerequisites
Before you begin, make sure you have the following:
- An AWS account.
- A GitHub account with access to the repository and GitHub Codespaces enabled.
- Basic understanding of Git, Terraform, and AWS services.


## Step-by-Step Instructions

### 1. AWS Account Setup
Ensure you have an active AWS account. If you don't have one, [create an AWS account here](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).


### 2. Fork the Repository
1. Go to the main repository on GitHub.
2. Click the "Fork" button at the top right to fork the repository into your own GitHub space.
    - ![Screenshot of GitHub Fork Button](assets/github-fork-button.png)
2. **Launch a Codespace**:
    - Once you have forked the repository, **navigate to your fork**.
    - Click on the "Code" button, then select "Open with Codespaces" and create a new Codespace.
    - ![Screenshot of Codespaces launch](assets/github-codespaces-new.png)
    - The Codespace will automatically set up your environment based on the repository's configuration (e.g., `.devcontainer`).
   **Important, this process can take few minutes, be patient:**
   ![Screenshot of CodeSpace Building](assets/github-codespace-building.png)
    - You will know the CodeSpace is ready when you can see: 
   ![Screenshot of CodeSpace Building](assets/github-codespace-ready.png)
2. **Checkout the initial branch**:
   -In order to switch branches you can run git commands in the terminal:
   ```bash
    git checkout master
    ```
   Or you can interact directly with the IDE  ![Screenshot of CodeSpace Branches section](assets/github-codespace-change-branche.png)
   
### 3. Environment Setup
1. **Set Up AWS CLI in Codespaces**:
    - Open the terminal in Codespaces and configure the AWS CLI with your credentials:
    ```bash
    aws configure
    ```
    - When prompted, enter:
        - **AWS Access Key ID**: [Follow this guide to obtain it.](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)
        - **AWS Secret Access Key**: [See instructions here.](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)
        - **Default Region Name**: Choose the appropriate region, like `us-east-1` or `eu-west-1`.
        - **Default Output Format**: Use `json` unless otherwise needed.
    - Example of terminal input:
    
   ```bash
    $ aws configure
    AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
    AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    Default region name [None]: eu-west-1
    Default output format [None]: json
    ```

2. **Set Up Python Environment**:
    - Activate the pre-configured Python environment:
    ```bash
    source venv/bin/activate 
    ```
    - Install the necessary Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    - ![Screenshot of Python environment setup](path/to/screenshot-python-env.png)

### 4. Terraform Initialization
1. **Terraform Backend Setup**:
    - Update the `terraform.tfvars.template` file with your specific values and rename it to `terraform.tfvars`.
    - ![Screenshot of terraform.tfvars.template](path/to/screenshot-terraform-tfvars.png)
2. **Initialize Terraform**:
    - Run the following command to initialize Terraform:
    ```bash
    terraform init
    ```
    - ![Screenshot of Terraform init output](path/to/screenshot-terraform-init.png)
3. **Validate Terraform Configuration**:
    - Validate the Terraform files to ensure there are no syntax errors:
    ```bash
    terraform validate
    ```
    - ![Screenshot of Terraform validate output](path/to/screenshot-terraform-validate.png)
4. **Plan the Infrastructure**:
    - Create an execution plan to see what Terraform will do:
    ```bash
    terraform plan
    ```
    - ![Screenshot of Terraform plan output](path/to/screenshot-terraform-plan.png)
5. **Apply the Infrastructure**:
    - Deploy the infrastructure:
    ```bash
    terraform apply
    ```
    - Confirm the apply action.
    - ![Screenshot of Terraform apply output](path/to/screenshot-terraform-apply.png)

### 5. AWS Resource Verification
1. **Login to AWS Console**: Log in to your AWS account and verify that all resources have been created.
2. **Check S3 Buckets**: Confirm that the S3 buckets for the backend, Lambda functions, raw, clean, and curated data are present.
    - ![Screenshot of S3 buckets](path/to/screenshot-s3-buckets.png)
3. **Check Other Resources**: Verify that the IAM roles, CodeBuild, and CodePipeline have been created.
    - ![Screenshot of IAM roles, CodeBuild, and CodePipeline](path/to/screenshot-aws-resources.png)

## Common Issues and Tips
- **Terraform Init Errors**: Ensure your AWS credentials are correctly configured. Use `aws configure` to reset them if necessary.
- **Python Environment Issues**: If you encounter issues with Python dependencies, ensure you are using the correct Python version and the virtual environment is activated.
- **Resource Verification**: Double-check the AWS region specified in your Terraform configuration; resources may be created in a different region if it's not consistent.

## Next Steps
Once you have successfully set up your environment and verified the resources, you are ready to move on to [Exercise 2: Running the Data Generator and ETL Processes](#).

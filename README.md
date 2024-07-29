# ETL Testing Framework

This repository contains the infrastructure as code (IaC) for setting up an ETL testing framework using AWS services and Terraform. 
The infrastructure includes a CI/CD pipeline with CodePipeline and CodeBuild.

## Structure

- `iac/`: Contains all Terraform configuration files and modules.
  - `main.tf`: Main Terraform configuration file.
  - `variables.tf`: Variable definitions.
  - `outputs.tf`: Output definitions.
  - `terraform.tfvars`: Default variable values.
  - `modules/`: Contains Terraform modules for IAM roles, CodeBuild, and CodePipeline.

## Prerequisites

- Terraform CLI installed.
- AWS account with necessary permissions.
- GitHub OAuth token for accessing your repository.

## Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/etl-testing-fwk.git
   cd etl-testing-fwk/iac

#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <owner> "
    exit 1
fi

# Assign input arguments to variables
OWNER="$1"
GITHUB_TOKEN="$2"

# Retrieve current Git branch name
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD | sed 's/[^a-zA-Z0-9._-]/-/g')

# Retrieve Git repository name
REPO_NAME=$(basename -s .git $(git config --get remote.origin.url) | sed 's/[^a-zA-Z0-9._-]/-/g')

# Retrieve GitHub owner (assumes the URL is in the form of https://github.com/owner/repo.git)
GITHUB_OWNER=$(git config --get remote.origin.url | awk -F'[:/]' '{print $(NF-1)}')

# Retrieve GitHub mail
GITHUB_OWNER_MAIL=$(git config --get user.email)


# Define paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BACKEND_TEMPLATE_FILE="${SCRIPT_DIR}/../iac/backend/terraform.tfvars.template"
ETL_TEMPLATE_FILE="${SCRIPT_DIR}/../iac/etl/terraform.tfvars.template"
CICD_TEMPLATE_FILE="${SCRIPT_DIR}/../iac/cicd/terraform.tfvars.template"
BACKEND_TFVARS_FILE="${SCRIPT_DIR}/../iac/backend/terraform.tfvars"
ETL_TFVARS_FILE="${SCRIPT_DIR}/../iac/etl/terraform.tfvars"
CICD_TFVARS_FILE="${SCRIPT_DIR}/../iac/cicd/terraform.tfvars"

# Predefined values for some parameters
REGION="eu-west-1"
ENV="dev"

# Function to generate tfvars file
generate_tfvars() {
    local template_file=$1
    local output_file=$2

    # Check if the template file exists
    if [ ! -f "$template_file" ]; then
        echo "Error: Template file '${template_file}' not found."
        exit 1
    fi

    # Replace placeholders with values
    sed -e "s/{branch}/$BRANCH_NAME/" \
        -e "s/{repo_name}/$REPO_NAME/" \
        -e "s/{github_owner}/$GITHUB_OWNER/" \
        -e "s/{github_owner_mail}/$GITHUB_OWNER_MAIL/" \
        -e "s/{owner}/$OWNER/" \
        -e "s/{region}/$REGION/" \
        -e "s/{env}/$ENV/" \
        "$template_file" > "$output_file"

    echo "Terraform variable file has been generated at $output_file."
}

# Generate tfvars for all BACKEND,  ETL and CICD
generate_tfvars "$BACKEND_TEMPLATE_FILE" "$BACKEND_TFVARS_FILE"
generate_tfvars "$ETL_TEMPLATE_FILE" "$ETL_TFVARS_FILE"
generate_tfvars "$CICD_TEMPLATE_FILE" "$CICD_TFVARS_FILE"

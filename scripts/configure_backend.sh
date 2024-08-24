#!/bin/bash

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the path to the backend directory
BACKEND_DIR="${SCRIPT_DIR}/../iac/backend"

# Define the paths to the backend directories for ETL and CICD
ETL_BACKEND_DIR="${SCRIPT_DIR}/../iac/etl"
CICD_BACKEND_DIR="${SCRIPT_DIR}/../iac/cicd"

# Extract the 'owner' value from iac/backend/terraform.tfvars
OWNER=$(grep '^owner' "${BACKEND_DIR}/terraform.tfvars" | sed 's/.*= *"\([^"]*\)".*/\1/')

# Check if OWNER is extracted correctly
if [ -z "$OWNER" ]; then
    echo "Error: Could not extract 'owner' from terraform.tfvars."
    exit 1
fi

# Define the S3 bucket and DynamoDB table names using the extracted OWNER
S3_BUCKET_NAME="${OWNER}-etl-testing-fwk-backend-s3"
DYNAMODB_TABLE_NAME="${OWNER}-manage-users-dynamodb"

# Define the backend configuration file path for both ETL and CICD
ETL_BACKEND_CONFIG="${ETL_BACKEND_DIR}/backend.tf"
CICD_BACKEND_CONFIG="${CICD_BACKEND_DIR}/backend.tf"

# Function to update backend configuration directly in backend.tf
update_backend_config() {
    local backend_file=$1

    # Check if the backend.tf file exists
    if [ ! -f "$backend_file" ]; then
        echo "Error: Backend configuration file '$backend_file' not found."
        return 1
    fi

    # Use sed to update the backend configuration directly in the backend.tf file
    sed -i '' -e "s/bucket *= *\".*\"/bucket = \"${S3_BUCKET_NAME}\"/" \
        -e "s/dynamodb_table *= *\".*\"/dynamodb_table = \"${DYNAMODB_TABLE_NAME}\"/" \
        "$backend_file"

    echo "Backend configuration has been updated in $backend_file."
}

# Update backend configuration for ETL
update_backend_config "${ETL_BACKEND_CONFIG}"

# Update backend configuration for CICD
update_backend_config "${CICD_BACKEND_CONFIG}"

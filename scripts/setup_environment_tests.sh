#!/bin/bash

# Change to the directory containing Terraform state
cd "$(dirname "$0")/../iac/etl" || {
    echo "Failed to change directory to ../iac/etl"
    exit 1  # Exit if directory change fails
}

# Capture Terraform outputs and write them to a .env file
env_file="$(dirname "$0")/../../tests/.env"

# Write variables to .env file
{
    echo "RAW_BUCKET=$(terraform output -raw raw_bucket_name)"
    echo "CURATED_BUCKET=$(terraform output -raw curated_bucket_name)"
    echo "CLEAN_BUCKET=$(terraform output -raw clean_bucket_name)"
    echo "DATA_GENERATOR_FUNCTION_NAME=$(terraform output -raw data_generator_function_name)"
    echo "SNS_TOPIC_ARN=$(terraform output -raw sns_topic_arn)"
    echo "LAMBDA_CLEAN_CURATED_FUNCTION_NAME=$(terraform output -raw lambda_clean_curated_function_name)"
    echo "LAMBDA_RAW_CLEAN_FUNCTION_NAME=$(terraform output -raw lambda_raw_clean_function_name)"
} > "$env_file"

cd "$(dirname "$0")/../cicd" || {
    echo "Failed to change directory to ../cicd"
    exit 1  # Exit if directory change fails
}

{
    echo "GX_REPORT_BUCKET=$(terraform output -raw gx_bucket_name)"
} >> "$env_file"



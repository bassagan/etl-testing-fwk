#!/bin/bash

# Script to package AWS Lambda functions located in different directories.
# Installs dependencies, creates ZIP files, and stores them in 'lambda_packages'.
# Cleans up temporary files after packaging.

# Usage: Run this script with `./package_lambda_functions.sh`
# Requirements: Python 3, pip, and terraform.tfvars file with 'bucket_name' and 'owner' in iac/etl.



# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define paths to the Lambda directories
ETL_DIR="${SCRIPT_DIR}/../iac/etl"
MANAGEMENT_DIR="${SCRIPT_DIR}/../iac/management"

# Define the path to store Lambda ZIP packages
ZIP_OUTPUT_DIR="${SCRIPT_DIR}/../lambda_packages"

# Ensure the ZIP output directory exists
mkdir -p "${ZIP_OUTPUT_DIR}"

# Extract the S3 bucket name from terraform.tfvars in iac/etl
S3_BUCKET=$(grep 'bucket_name' "${ETL_DIR}/terraform.tfvars" | cut -d '=' -f2 | sed 's/[", ]//g')
OWNER=$(grep 'owner' "${ETL_DIR}/terraform.tfvars" | cut -d '=' -f2 | sed 's/[", ]//g')

# Check if the bucket name was extracted correctly
if [ -z "$S3_BUCKET" ]; then
    echo "Error: Could not extract 'bucket_name' from terraform.tfvars."
    exit 1
fi

# Helper function to install dependencies, package Lambda functions, and clean up
package_lambda() {
  local lambda_dir=$1
  local zip_name=$2
  local base_dir=$3

  echo "Packaging Lambda function in directory: $lambda_dir"

  pushd "${base_dir}/${lambda_dir}" || exit 1

  # Install dependencies
  echo "Installing dependencies for ${lambda_dir}..."
  pip install --upgrade pip
  pip install --no-cache-dir --no-deps -r requirements.txt -t .

  # Package the Lambda function
  echo "Creating zip package ${zip_name}..."
  zip -r "${ZIP_OUTPUT_DIR}/${zip_name}" .

  # Clean up dependencies
  echo "Cleaning up dependencies for ${lambda_dir}..."
  find . -type d -name "__pycache__" -exec rm -rf {} +
  find . -type d -name "*.dist-info" -exec rm -rf {} +
  find . -type d -name "*.egg-info" -exec rm -rf {} +
  find . -type d -name "boto*" -exec rm -rf {} +
  find . -type d -name "pip*" -exec rm -rf {} +

  echo "Cleaning up dependencies for ${lambda_dir}..."
  rm -rf bin numpy pandas pyarrow pytz faker moto __pycache__ *.dist-info *.egg-info


  popd || exit 1

}

# Package Lambda functions in iac/etl directory
package_lambda "lambda_generator_package" "lambda_generator_package.zip" "$ETL_DIR"
package_lambda "lambda_raw_clean" "lambda_raw_clean.zip" "$ETL_DIR"
package_lambda "lambda_clean_curated" "lambda_clean_curated.zip" "$ETL_DIR"

echo "All Lambda functions have been packaged and stored in ${ZIP_OUTPUT_DIR}."

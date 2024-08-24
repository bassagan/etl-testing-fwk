#!/bin/bash

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the path to the iac/etl directory
ETL_DIR="${SCRIPT_DIR}/../iac/etl"

# Extract the S3 bucket name from terraform.tfvars in iac/etl
S3_BUCKET=$(grep 'bucket_name' "${ETL_DIR}/terraform.tfvars" | cut -d '=' -f2 | sed 's/[", ]//g')
OWNER=$(grep 'owner' "${ETL_DIR}/terraform.tfvars" | cut -d '=' -f2 | sed 's/[", ]//g')

# Check if the bucket name was extracted correctly
if [ -z "$S3_BUCKET" ]; then
    echo "Error: Could not extract 'bucket_name' from terraform.tfvars."
    exit 1
fi

# Helper function to install dependencies and package Lambda functions
package_lambda() {
  local lambda_dir=$1
  local zip_name=$2

  echo "Packaging Lambda function in directory: $lambda_dir"

  pushd "${ETL_DIR}/${lambda_dir}" || exit 1

  # Install dependencies
  echo "Installing dependencies for ${lambda_dir}..."
  pip install --upgrade pip
  pip install --no-cache-dir --no-deps -r requirements.txt -t .

  # Package the Lambda function
  echo "Creating zip package ${zip_name}..."
  zip -r "../${zip_name}" .

  popd || exit 1
}

# Package Lambda Generator Function
package_lambda "lambda_generator_package" "lambda_generator_package.zip"

# Package Lambda Raw-Clean ETL
package_lambda "lambda_raw_clean" "lambda_raw_clean.zip"

# Package Lambda Clean-Curated ETL
package_lambda "lambda_clean_curated" "lambda_clean_curated.zip"

echo "All Lambda functions have been packaged."

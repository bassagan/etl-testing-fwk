#!/bin/bash

# Check if all arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <branch_name> <repo_name> <env>"
    exit 1
fi

branch_name=$(echo "$1" | sed 's/[^a-zA-Z0-9._-]/-/g')
repo_name=$(echo "$2" | awk -F/ '{print $2}' | sed 's/[^a-zA-Z0-9._-]/-/g')
env=$3

# Define paths relative to the root of the repository
TEMPLATE_FILE="${GITHUB_WORKSPACE}/iac/terraform.tfvars.template"
OUTPUT_FILE="${GITHUB_WORKSPACE}/iac/terraform.tfvars"

# Ensure the template file exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Template file not found: $TEMPLATE_FILE"
    exit 1
fi

# Replace placeholders in terraform.tfvars.template and output to terraform.tfvars
sed -e "s/{branch_name}/$branch_name/" -e "s/{repo_name}/$repo_name/" -e "s/{env}/$env/" "$TEMPLATE_FILE" > "$OUTPUT_FILE"

# Echo the contents of the updated terraform.tfvars for debugging purposes
echo "Modified terraform.tfvars for branch $branch_name"
cat "$OUTPUT_FILE"

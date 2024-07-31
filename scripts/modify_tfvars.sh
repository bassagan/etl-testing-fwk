#!/bin/bash

# Check if all arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <branch_name> <repo_name> <env>"
    exit 1
fi

branch_name=$(echo "$1" | sed 's/[^a-zA-Z0-9._-]/-/g')
repo_name=$(echo "$2" | awk -F/ '{print $2}' | sed 's/[^a-zA-Z0-9._-]/-/g')
echo "pipeline_name=${branch_name}-${repo_name}-codepipeline-$3" >> terraform.tfvars

env=$3

# Replace placeholders in terraform.tfvars.template and output to terraform.tfvars
sed -e "s/{branch_name}/$branch_name/" -e "s/{repo_name}/$repo_name/" -e "s/{env}/$env/" terraform.tfvars.template > terraform.tfvars

echo "Modified terraform.tfvars for branch $branch_name"

# Display the content of terraform.tfvars
echo "Content of terraform.tfvars:"
cat terraform.tfvars
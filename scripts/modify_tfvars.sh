#!/bin/bash

# Check if all arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <branch_name> <repo_name> <env>"
    exit 1
fi

branch_name=$(echo "$1" | sed 's/[^a-zA-Z0-9._-]/-/g')
repo_name=$(echo "$2" | awk -F/ '{print $2}' | sed 's/[^a-zA-Z0-9._-]/-/g')
env=$3

# Update the codepipeline_name variable in terraform.tfvars
echo "pipeline_name=${branch_name}-${repo_name}-codepipeline-$3" >> ../iac/terraform.tfvars

# Replace placeholders in terraform.tfvars.template and output to terraform.tfvars
sed -e "s/{branch_name}/$branch_name/" -e "s/{repo_name}/$repo_name/" -e "s/{env}/$env/" ../iac/terraform.tfvars.template > ../iac/terraform.tfvars

# Echo the contents of the updated terraform.tfvars for debugging purposes
echo "Modified terraform.tfvars for branch $branch_name"
cat ../iac/terraform.tfvars

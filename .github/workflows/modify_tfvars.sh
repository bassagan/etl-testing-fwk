#!/bin/bash

# Check if all arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <branch_name> <repo_name> <env>"
    exit 1
fi

branch_name=$1
repo_name=$2
env=$3

# Replace placeholders in terraform.tfvars.template and output to terraform.tfvars
sed -e "s/{branch_name}/$branch_name/" -e "s/{repo_name}/$repo_name/" -e "s/{env}/$env/" terraform.tfvars.template > terraform.tfvars

echo "Modified terraform.tfvars for branch $branch_name"

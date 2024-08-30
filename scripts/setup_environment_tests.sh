#!/bin/bash

# Set environment variables
export RAW_BUCKET=$(terraform output -raw raw_bucket_name)
export CURATED_BUCKET=$(terraform output -raw curated_bucket_name)
export CLEAN_BUCKET=$(terraform output -raw clean_bucket_name)
export SNS_TOPIC_ARN=$(terraform output -raw sns_topic_arn)

# Add any other environment variables you need

# Print the variables (optional, for verification)
echo "Environment variables set:"
echo "RAW_BUCKET: $RAW_BUCKET"
echo "CURATED_BUCKET: $CURATED_BUCKET"
echo "CLEAN_BUCKET: $CLEAN_BUCKET"
echo "SNS_TOPIC_ARN: $SNS_TOPIC_ARN"
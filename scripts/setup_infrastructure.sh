#!/bin/bash

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Paths to the other scripts
CONFIGURE_BACKEND_SCRIPT="${SCRIPT_DIR}/configure_backend.sh"
GENERATE_TFVARS_SCRIPT="${SCRIPT_DIR}/generate_tfvars.sh"
PACKAGE_LAMBDAS_SCRIPT="${SCRIPT_DIR}/package_lambdas.sh"

# AWS CLI Configuration
configure_aws_cli() {
    echo "Checking AWS CLI configuration..."
    if ! aws sts get-caller-identity >/dev/null 2>&1; then
        echo "AWS CLI not configured. Running 'aws configure' for access key and secret access key..."
        read -p "Enter AWS Access Key ID: " aws_access_key_id
        read -p "Enter AWS Secret Access Key: " aws_secret_access_key
        echo

        aws configure set aws_access_key_id "$aws_access_key_id"
        aws configure set aws_secret_access_key "$aws_secret_access_key"
        aws configure set region "eu-west-1"
        aws configure set output "json"

        echo "AWS CLI configured with default region '$DEFAULT_REGION' and output format '$DEFAULT_OUTPUT_FORMAT'."
    else
        read -p "AWS CLI is already configured. Do you want to reconfigure it? (y/n): " choice
        if [[ "$choice" == [Yy]* ]]; then
            read -p "Enter AWS Access Key ID: " aws_access_key_id
            read -s -p "Enter AWS Secret Access Key: " aws_secret_access_key
            echo

            aws configure set aws_access_key_id "$aws_access_key_id"
            aws configure set aws_secret_access_key "$aws_secret_access_key"
            aws configure set region "$DEFAULT_REGION"
            aws configure set output "$DEFAULT_OUTPUT_FORMAT"

            echo "AWS CLI reconfigured with default region '$DEFAULT_REGION' and output format '$DEFAULT_OUTPUT_FORMAT'."
        else
            echo "Proceeding with existing AWS configuration."
        fi
    fi
}

# Check if virtual environment exists and activate it
setup_virtualenv() {
    VENV_DIR="${SCRIPT_DIR}/../venv"

    if [ -d "$VENV_DIR" ]; then
        echo "Activating existing virtual environment..."
        source "$VENV_DIR/bin/activate"
    else
        echo "Creating and activating virtual environment..."
        python3 -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
        echo "Installing required Python packages..."
        pip install --upgrade pip
        pip install -r "${SCRIPT_DIR}/requirements.txt"
    fi
}

# Check if all required scripts exist
check_scripts() {
    if [ ! -f "$CONFIGURE_BACKEND_SCRIPT" ]; then
        echo "Error: configure_backend.sh script not found."
        exit 1
    fi

    if [ ! -f "$GENERATE_TFVARS_SCRIPT" ]; then
        echo "Error: generate_tfvars.sh script not found."
        exit 1
    fi

    if [ ! -f "$PACKAGE_LAMBDAS_SCRIPT" ]; then
        echo "Error: package_lambdas.sh script not found."
        exit 1
    fi
}

# Run the scripts in sequence
run_scripts() {
    # Run generate_tfvars.sh with the required argument for the owner
    echo "Running generate_tfvars.sh..."
    bash "$GENERATE_TFVARS_SCRIPT" "$1"
    if [ $? -ne 0 ]; then
        echo "Error: generate_tfvars.sh failed."
        exit 1
    fi

    # Run configure_backend.sh
    echo "Running configure_backend.sh..."
    bash "$CONFIGURE_BACKEND_SCRIPT"
    if [ $? -ne 0 ]; then
        echo "Error: configure_backend.sh failed."
        exit 1
    fi

    # Run package_lambdas.sh
    echo "Running package_lambdas.sh..."
    bash "$PACKAGE_LAMBDAS_SCRIPT"
    if [ $? -ne 0 ]; then
        echo "Error: package_lambdas.sh failed."
        exit 1
    fi
}

# Main script execution
main() {
    # Check if the correct number of arguments are provided
    if [ "$#" -ne 1 ]; then
        echo "Usage: $0 <owner>"
        exit 1
    fi

    OWNER="$1"

    # Run AWS CLI configuration if necessary
    configure_aws_cli

    # Set up and activate virtual environment
    setup_virtualenv

    # Check if all required scripts exist
    check_scripts

    # Run all scripts
    run_scripts "$OWNER"

    echo "All scripts have been executed successfully."
}

# Start the main script
main "$@"

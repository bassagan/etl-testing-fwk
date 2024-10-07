# Use the official Python image as a base
FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Install additional dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add - && \
    apt-add-repository 'deb [arch=amd64] https://apt.releases.hashicorp.com focal main' && \
    apt-get update && \
    apt-get install -y terraform && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# Install Allure
RUN apt-get update && \
    apt-get install -y default-jdk && \
    curl -o allure-2.22.1.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.22.1/allure-commandline-2.22.1.tgz && \
    tar -zxvf allure-2.22.1.tgz -C /opt/ && \
    ln -s /opt/allure-2.22.1/bin/allure /usr/bin/allure && \
    rm allure-2.22.1.tgz

# Create and activate a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# Set the working directory
WORKDIR /workspace

import os

import boto3
import json
import time

quicksight = boto3.client('quicksight')
athena = boto3.client('athena')

aws_account_id = os.getenv("AWS_ACCOUNT_ID", "087559609246")
region = os.getenv("AWS_DEFAULT_REGION", "eu-west-1")
quicksight_user = os.getenv("QUICKSIGHT_USER", "quicksight_user")

def run_athena_query(query_execution_id):
    """Wait for the Athena query to complete and return the result."""
    while True:
        response = athena.get_query_execution(QueryExecutionId=query_execution_id)
        status = response['QueryExecution']['Status']['State']

        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break

        time.sleep(5)

    if status == 'SUCCEEDED':
        return athena.get_query_results(QueryExecutionId=query_execution_id)
    else:
        raise Exception(f"Athena query failed with status: {status}")

def create_data_source():
    response = quicksight.create_data_source(
        AwsAccountId=aws_account_id,
        DataSourceId='athena-datasource-id',
        Name='AthenaDataSource',
        Type='ATHENA',
        DataSourceParameters={
            'AthenaParameters': {
                'WorkGroup': 'etl-workgroup-dev'
            }
        }
    )
    return response['Arn']

def create_dataset_from_query(data_source_arn, query):
    query_execution = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'etl_clean_athena_dev'},
        ResultConfiguration={'OutputLocation': 's3://clean-etl-bucket-dev/athena-results/'}
    )
    results = run_athena_query(query_execution['QueryExecutionId'])

    response = quicksight.create_data_set(
        AwsAccountId=aws_account_id,
        DataSetId='visits-dataset-id',
        Name='VisitsDataset',
        PhysicalTableMap={
            'PhysicalTable1': {
                'CustomSql': {
                    'DataSourceArn': data_source_arn,
                    'Name': 'VisitsQuery',
                    'SqlQuery': query,
                    'Columns': [ # Add columns based on your query
                        {'Name': 'doctor_name', 'Type': 'STRING'},
                        {'Name': 'department', 'Type': 'STRING'},
                    ]
                }
            }
        }
    )
    return response['Arn']

def main():
    data_source_arn = create_data_source()

    with open('../iac/etl/modules/athena/queries/top_doctors.sql', 'r') as file:
        top_doctors_query = file.read()

    dataset_arn = create_dataset_from_query(data_source_arn, top_doctors_query)

    print(f"Dataset created with ARN: {dataset_arn}")

if __name__ == '__main__':
    main()

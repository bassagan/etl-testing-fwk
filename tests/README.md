# Exercise 5: Implementing a New Data Source and Expectations for the Clean Bucket

Welcome to the fifth exercise of our ETL Testing Framework tutorial! In this exercise, you'll learn how to implement a new data source for the clean bucket, add expectations for the data sources, and build and run checkpoints to ensure data quality.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setting up the new data source](#setting-up-the-new-data-source)
4. [Adding expectations for data sources](#adding-expectations-for-data-sources)
5. [Building and running checkpoints](#building-and-running-checkpoints)
6. [Common Issues and Tips](#common-issues-and-tips)
7. [Next Steps](#next-steps)

## Exercise 5 Checklist

Use this checklist to ensure you've completed all the necessary steps for Exercise 5:

- [ ] Implement a new data source for the clean bucket
- [ ] Add expectations for the new data source
- [ ] Build and run checkpoints to validate data quality

Once you've checked off all these items, you've successfully completed Exercise 5!

## Prerequisites
Before you begin, make sure you have completed Exercise 4 and have the following:
- Access to the clean bucket in your AWS S3
- Basic understanding of data validation and expectations

## Setting up the new data source

In this section, you'll implement a new data source that will feed data into the clean bucket.

1. **Create a new data source script**:
   - Navigate to the `src/data_sources` directory and create a new Python script named `new_clean_data_source.py`.

   ```python
   # src/data_sources/new_clean_data_source.py

   import boto3
   import json

   def fetch_data():
       # Logic to fetch data from the new source
       data = {
           "patient_id": "123e4567-e89b-12d3-a456-426614174000",
           "name": "John Doe",
           "address": "123 Main St",
           "phone_number": "555-1234",
           "email": "john.doe@example.com",
           "insurance_provider": "Health Insurance Co.",
           "policy_number": "ABC123456",
           "record_created_at": "2023-01-01T00:00:00Z",
           "record_updated_at": "2023-01-01T00:00:00Z"
       }
       return data

   def upload_to_clean_bucket(data):
       s3 = boto3.client('s3')
       bucket_name = 'your-clean-bucket-name'
       s3.put_object(Bucket=bucket_name, Key='data/new_clean_data.json', Body=json.dumps(data))

   if __name__ == "__main__":
       data = fetch_data()
       upload_to_clean_bucket(data)
   ```

2. **Run the new data source script**:
   - Execute the script to upload data to the clean bucket.

   ```bash
   python src/data_sources/new_clean_data_source.py
   ```

## Adding expectations for data sources

Next, you'll add expectations to validate the data being uploaded to the clean bucket.

1. **Update the `ExpectationSuiteManager` class**:
   - Modify the `expectation_suites.py` file to include expectations for the new data source.

   ```python
   # tests/great_expectations/expectation_suites.py

   def _add_clean_data_expectations(self):
       clean_data_expectations = [
           gxe.ExpectColumnValuesToNotBeNull(column="patient_id"),
           gxe.ExpectColumnValuesToMatchRegex(column="patient_id", regex=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'),
           gxe.ExpectColumnValuesToNotBeNull(column="name"),
           gxe.ExpectColumnValueLengthsToBeBetween(column="name", min_value=2, max_value=100),
           gxe.ExpectColumnValuesToNotBeNull(column="address"),
           gxe.ExpectColumnValuesToNotBeNull(column="phone_number"),
           gxe.ExpectColumnValuesToMatchRegex(column="email", regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
           gxe.ExpectColumnValuesToNotBeNull(column="insurance_provider"),
           gxe.ExpectColumnValuesToNotBeNull(column="policy_number"),
           gxe.ExpectColumnValuesToBeOfType(column="record_created_at", type_="datetime64"),
           gxe.ExpectColumnValuesToBeOfType(column="record_updated_at", type_="datetime64"),
       ]
       for expectation in clean_data_expectations:
           self.clean_data_suite.add_expectation(expectation)
   ```

2. **Run the expectations setup**:
   - Ensure that the expectations are set up correctly by running the `setup_suites` method in the `ExpectationSuiteManager`.

   ```python
   # In your main execution script
   from tests.great_expectations.expectation_suites import ExpectationSuiteManager
   from tests.great_expectations.data_context import DataContextManager

   context_manager = DataContextManager()
   suite_manager = ExpectationSuiteManager(context_manager.context)
   suite_manager.setup_suites()
   ```

## Building and running checkpoints

Finally, you'll build and run checkpoints to ensure data quality.

1. **Update the `ValidationManager` class**:
   - Modify the `validation_manager.py` file to include a checkpoint for the new data source.

   ```python
   # tests/great_expectations/validation_manager.py

   def setup_validations(self, asset_manager, suite_manager):
       # Existing validations...
       
       clean_data_vd = self._create_validation_definition(
           "clean_data_validation_definition",
           "clean_data",
           "batch_clean_data",
           suite_manager.clean_data_suite
       )

       self._create_checkpoint([clean_data_vd])
   ```

2. **Run the checkpoint**:
   - Use the `run_checkpoint` method to validate the new data source.

   ```python
   # In your main execution script
   validation_manager = ValidationManager(context_manager.context)
   validation_manager.setup_validations(asset_manager, suite_manager)
   validation_results = validation_manager.run_checkpoint()
   print(validation_results)
   ```

## Common Issues and Tips
- Ensure that your AWS credentials are correctly configured and have the necessary permissions to access the clean bucket.
- Double-check the data structure and expectations to ensure they align with your data source.

## Next Steps
Once you have successfully implemented the new data source, added expectations, and run the checkpoints, you are ready to move on to Exercise 6, where you'll explore advanced data validation techniques and reporting.

For more details on Exercise 6, please refer to the [Exercise 6 README](reports/README.md).

## Reference Solution

For reference and guidance, you can check the `feature/exercise_5_solved` branch. This branch contains a complete solution for Exercise 5, which may be helpful if you encounter any difficulties or want to compare your implementation.

To check out the reference solution, use the following command:
```bash
git checkout feature/exercise_5_solved
```

Remember, it's best to try solving the exercise on your own first, but don't hesitate to use the reference solution if you need additional clarity or want to verify your approach.

## Key Takeaways

In this exercise, you've learned and practiced the following key concepts:

1. Implementing a new data source for the clean bucket.
2. Adding expectations to validate data quality.
3. Building and running checkpoints to ensure data integrity.

These skills will enhance your ability to manage and validate data in your ETL processes effectively.
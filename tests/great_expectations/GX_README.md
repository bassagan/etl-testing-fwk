# Exercise 4: Playing with Great Expectations

Welcome to the forth exercise of our ETL Testing Framework tutorial! In this exercise, you'll learn how to implement a new data source for the clean bucket, add expectations for the data sources, and build and run checkpoints to ensure data quality.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Adding expectations for data sources](#adding-expectations-for-data-sources)
3. [Building and running checkpoints](#building-and-running-checkpoints)
4. [Common Issues and Tips](#common-issues-and-tips)
5. [Next Steps](#next-steps)

## Exercise 4 Checklist

Use this checklist to ensure you've completed all the necessary steps for Exercise 5:

- [ ] Implement a new data source for the clean bucket
- [ ] Add expectations for the new data source
- [ ] Build and run checkpoints to validate data quality

Once you've checked off all these items, you've successfully completed Exercise 5!

## Prerequisites
Before you begin, make sure you have completed Exercise 4 and have the following:
- Access to the clean bucket in your AWS S3
- Basic understanding of data validation and expectations

## Exercise 4.1: Understanding Great Expectations
In this exercise, you will run the `main.py` script to execute raw validation against your data.
1. **Check and uncomment dependencies**:
   - Open the `tests/requirements.txt` file and ensure that the Great Expectations dependencies are not commented out. 

2. **Install dependencies**:
   - After ensuring the dependencies are uncommented, run the following command to install them:

```bash
pip install -r tests/requirements.txt
```

3. **Navigate to the Great Expectations directory and set Python Path**:
```bash
cd tests/great_expectations
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

4. **Run the main script**:
```bash
python raw_validation/main.py
```

This will initiate the Great Expectations validation process for your raw data. Ensure that your AWS credentials are correctly configured to access the S3 bucket.

To view the results of your Great Expectations validation, you can open the 
On CodeSpaces you won't be able to visualize the data docs locally. So you can navigate to the printed path in the terminal to see the data docs:
![CodeSpaces Terminal DataDocs URL](..%2F..%2Fassets%2Fgithub-codespaces-terminal-gx-url.png)


## Exercise 4.2: Adding Expectations to the Clean Layer

In this exercise, you will add expectations to validate the data in the clean layer. Before proceeding, check how your data looks in Athena to ensure that the structure aligns with your expectations.
Let's prepare the data first:
0. **Navigate to the raw bucket** and ensure that you have patients/ and visits/ folders with json files. If not, you will have to execute the data generator lambda function

1. **Review Data in Athena**:
   - Open the AWS Athena console and run queries to inspect the `patients` and `visits` tables. This will help you understand the data structure and identify any necessary expectations.
   - In case you cannot run the queries on Athena console, you can see the csv samples. This will help you to understand the data structure and identify any necessary expectations. 
     - [clean_patients_sample.csv](..%2F..%2Fassets%2Fclean_patients_sample.csv)
     - [clean_visits_sample.csv](..%2F..%2Fassets%2Fclean_visits_sample.csv)
     
![aws_athena_query.png](..%2F..%2Fassets%2Faws_athena_query.png)
     - 
2. **Update the `CleanExpectationSuiteManager` class**:
   - Navigate to the `tests/great_expectations/clean_validation/clean_expectation_suites.py` file.
   - Modify the `clean_expectation_suites.py` file to include two expectations for each asset in clean data source. Feel free to choose and play with them.
   - You can find the available expectations at the [Expectations Gallery](https://greatexpectations.io/expectations/).

```python
# tests/great_expectations/clean_validation/clean_expectation_suites.py

#....  existing code ....
    def _add_patient_expectations(self):
        patient_expectations = [
            gxe.ExpectColumnValuesToNotBeNull(column="patient_id"),
            #TODO: Add here your expectations. You can check for available expectations at: https://greatexpectations.io/expectations/
        ]
        for expectation in patient_expectations:
            self.patients_suite.add_expectation(expectation)

    def _add_visit_expectations(self):
        visit_expectations = [
            gxe.ExpectColumnValuesToNotBeNull(column="appointment_id"),
           #TODO: Add here your expectations. You can check for available expectations at: https://greatexpectations.io/expectations/
        ]
        for expectation in visit_expectations:
            self.visits_suite.add_expectation(expectation)
```


3. **Run the main script for clean validations**:
```bash
python clean_validation/main.py
 ```
4. **CICD pipeline execution**:
   - Open the `buildspec.yml` file and uncomment the `Great Expectations` section to run the expectations in the CI/CD pipeline.
   - Commit and push the changes to trigger the pipeline.
   - Go to the CodePipeline console and monitor the pipeline execution.
   - Open again the data docs url to see the results of the expectations.


## Common Issues and Tips
- Ensure that your AWS credentials are correctly configured and have the necessary permissions to access the clean bucket.
- Double-check the data structure and expectations to ensure they align with your data source.


## Reference Solution

The final solution for all four exercises can be found in the `exercises_solution` folder. To use it, substitute the folders in the root directory with those in the solution folder and reexecute all steps from the first exercise.

Remember, it's best to try solving the exercise on your own first, but don't hesitate to use the reference solution if you need additional clarity or want to verify your approach.


## Key Takeaways

In this exercise, you've learned and practiced the following key concepts:

1. Adding expectations to validate data quality.
2. Building and running checkpoints to ensure data integrity.
3. Adding GX to our CICD pipeline
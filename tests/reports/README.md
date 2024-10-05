# Exercise 3: Integrating Allure Reports

In this exercise, you'll learn how to integrate Allure reports into your pytest-based test automation framework. Allure provides rich and detailed test reports that can help you better understand and analyze your test results. For more information about Allure, you can refer to the [official Allure documentation](https://docs.qameta.io/allure/).

## Objectives:
* Install Allure and its pytest plugin
* Add Allure decorators to your test cases
* Generate and view Allure reports
* Add history to Allure reports

## Table of Contents

## Exercise 3 Checklist
Use this checklist to ensure you've completed all the necessary steps:
- [ ] Install Allure command-line tool
- [ ] Add allure-pytest to requirements.txt
- [ ] Install updated requirements
- [ ] Add Allure decorators to test class and method
- [ ] Add Allure steps to test method
- [ ] Generate and view Allure report locally
- [ ] Set up Allure history
- [ ] Generate and view report with history locally
- [ ] Configure buildspec.yml for Allure report generation and publication in AWS

## Prerequisites
Before you begin, make sure you have completed Exercise 2 and have the following:
- At least one test case and its fixtures

## Setting up the testing environment

### 3.1. Install Allure
First, we need to install the Allure command-line tool and the Allure-pytest plugin.
a. Install Allure command-line.  You don't need to do this on the codespace
    * For Mac:
    ```bash
   brew install allure
   ```
   * For Linux:
   ```bash
   sudo apt-get install allure
   ```
   * For Windows:
   ```bash
   choco install allure
   ```  
b. Install Allure-pytest plugin to your [requirements.txt](../requirements.txt) file:
    ```
    allure-pytest==2.13.5
    ```
```bash
   pip install -r requirements.txt
```
### 3.2. Add Allure to Test Cases:

Now, let's add Allure decorators to our existing tests in [test_lambda_raw_clean.py](../e2e/raw-clean/test_lambda_raw_clean.py).

a. Open [test_lambda_raw_clean.py](../e2e/raw-clean/test_lambda_raw_clean.py) file
b. Import Allure at the top of the file:
``` python
import allure
```
c. Add Allure decorators to the test cases:
``` python
@allure.feature("Raw Clean Lambda Function")
@allure.story("Test Lambda Execution")
@allure.title("Test Lambda Execution")
def test_lambda_execution(generate_test_data):
    ...
```
d. Add Allure steps to the test cases:
``` python
@allure.step("Generate test data")
def generate_test_data():
    ...

```
``` python
with allure.step(f"Invoke Lambda function '{raw_clean_lambda_function_name}' with {invocation_type} invocation"):
        response = lambda_client.invoke(
            FunctionName=raw_clean_lambda_function_name,
            InvocationType=invocation_type,
            Payload=payload
        )
```
e. add test evidence to allure report:
``` python
    allure.attach(
        json.dumps(serializable_response, indent=2),
        name="Lambda Response",
        attachment_type=allure.attachment_type.JSON
    )
```

### 3.3. Generate and View Allure Report
Now that we've added Allure to our tests, let's generate and view the reports.

a. Run the tests with Allure:
```bash
   python -m pytest --alluredir allure-results
   ```

b. Generate and view the Allure report:
```bash
    allure generate allure-results -o allure-report --clean
    allure open allure-report
```
This command will generate a report from the results and open it in your default web browser. The report will include:
- An overview of test execution
- Detailed test cases with steps and attachments
- Graphs and charts showing test statistics

c. Explore the Allure report:
- Check the "Suites" tab to see test cases grouped by features and stories
- Click on individual test cases to see detailed steps and any attached evidence
- Use the "Graphs" tab to view test execution trends and statistics

### 3.4. Add History to Allure Reports
To track test results over time, we can add history to our Allure reports.

a. After running tests and before generating a new report, copy the history:
```bash
    cp -R allure-report/history allure-results/history
```
This step ensures that the history from previous test runs is included in the new report.

b. Generate the report with history:
```bash
    allure generate allure-results -o allure-report --clean
```
This command generates a new report in the `allure-report` directory, including the history data.

d. View the report with history:
```bash
    allure open allure-report
```
This opens the generated report in your browser. You can now see:
- Trend charts showing test results over time
- Retries and flaky tests across multiple runs
- Historical data for each test case

e. For subsequent test runs, repeat steps b-d to maintain and update the history.

By following these steps, you'll have a comprehensive Allure report setup that includes detailed test information, evidence, and historical data to track your test suite's performance over time.

### 3.5. Configure AWS CodeBuild for Allure Reports

These changes will configure AWS CodeBuild to generate Allure reports and publish them to an S3 bucket after each build. Make sure to update the ALLURE_REPORT_BUCKET variable with your actual S3 bucket name for storing Allure reports.


a. Open your [buildspec.yml](../../buildspec.yml) file.
b. Add the following environment variable to the buildspec.yml file:
```yaml
    ALLURE_REPORT_BUCKET: "allure-reports-conference-user-9fe23ed6-xdrnxgxz"
    ALLURE_RESULTS_DIR: "/tmp/allure-results"
```
c. In the `install` section, add the following command:
```bash
          # ... existing commands ...
      - npm install -g allure-commandline --save-dev
      - allure --version
```
d. In the build phase, add the command to run tests with Allure:
```bash
  build:
    commands:
      - echo "Running pytest tests..."
      - pytest tests --alluredir=$ALLURE_RESULTS_DIR
```
e. Add a post_build phase to generate and upload the Allure report:
```bash
  post_build:
    commands:
      - echo "Downloading existing Allure history"
      - aws s3 sync s3://$ALLURE_REPORT_BUCKET/history/ $ALLURE_RESULTS_DIR/history/ || true
      - echo "Generating Allure report"
      - allure generate $ALLURE_RESULTS_DIR -o allure-report --clean
      - echo "Uploading Allure report to S3"
      - aws s3 sync allure-report s3://$ALLURE_REPORT_BUCKET/ --delete
      - echo "Updating Allure history"
      - aws s3 sync allure-report/history s3://$ALLURE_REPORT_BUCKET/history/ --delete
```
f. Add an artifacts section to include the Allure report:
```bash
  artifacts:
    files:
      - '**/*'
    name: test-output
    base-directory: allure-report
```

## Common Issues and Tips
- If you encounter issues with Allure installation, make sure you have the necessary permissions and that your package manager is up to date.
- When adding Allure steps, ensure that the content within each step is meaningful and provides valuable information for debugging.
- If the Allure report doesn't open automatically, check the console output for the URL and open it manually in your browser.

## Next Steps
Once you have successfully implemented and verified the test data generator fixture, you are ready to move on to Exercise 3, where you'll explore Great Expectations for testing data transformations.


## Reference Solution

For reference and guidance, you can check the `feature/exercise_3_solved` branch. This branch contains a complete solution for Exercise 3, which may be helpful if you encounter any difficulties or want to compare your implementation.

To check out the reference solution, use the following command:
```bash
git checkout feature/exercise_3_solved
```

Remember, it's best to try solving the exercise on your own first, but don't hesitate to use the reference solution if you need additional clarity or want to verify your approach.

## Key Takeaways

In this exercise, you've learned and practiced the following key concepts:

1. Setting up a pytest testing environment for AWS-based ETL processes.
2. Using pytest fixtures to manage test setup and teardown.
3. Implementing a test data generator fixture using boto3 to interact with AWS Lambda.
4. Moving common fixtures to conftest.py for better organization and reusability.
5. Executing and debugging test cases using pytest and the VS Code Test Explorer.
6. Writing end-to-end tests for SNS notifications in an ETL pipeline.
7. Using environment variables to configure tests for different environments.

These skills form a solid foundation for writing robust, maintainable tests for complex ETL processes in AWS environments.
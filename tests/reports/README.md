# Exercise 3: Integrating Allure Reports

In this exercise, you'll learn how to integrate Allure reports into your pytest-based test automation framework. Allure provides rich and detailed test reports that can help you better understand and analyze your test results.

## Objectives:
* Install Allure and its pytest plugin
* Add Allure decorators to your test cases
* Generate and view Allure reports
* Add history to Allure reports

## Table of Contents

## Exercise 3 Checklist
Use this checklist to ensure you've completed all the necessary steps:
[ ] Installed Allure command-line tool
[ ] Added allure-pytest to requirements.txt
[ ] Installed updated requirements
[ ] Added Allure decorators to test class and method
[ ] Added Allure steps to test method
[ ] Generated and viewed Allure report
[ ] Set up Allure history
[ ] Generated and viewed report with history

## Prerequisites
Before you begin, make sure you have completed Exercise 2 and have the following:
- Two different test cases and its fixtures

## Setting up the testing environment

### 3.1. Install Allure
First, we need to install the Allure command-line tool and the Allure-pytest plugin.
a. Install Allure command-line tool:
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


### 3.3. Generate and View Allure Report
Now that we've added Allure to our tests, let's generate and view the reports.

a. Run the tests with Allure:
```bash
   python -m pytest --alluredir allure-results
   ```

b. Generate and view the Allure report:
```bash
    allure serve allure-results
```
This will open your default web browser and display the Allure report.

### 3.4. Add History to Allure Reports
To track test results over time, we can add history to our Allure reports.
a. Create a directory for Allure history:
```bash
    mkdir allure-history
```
b. After running tests and before generating a new report, copy the history:
```bash
    cp -R allure-report/history allure-results/history
```
c. Generate the report with history:
```bash
    allure generate allure-results -o allure-report --clean
```
d. View the report with history:
```bash
    allure open allure-report
```

### Steps:

1. Open the [`conftest.py`](e2e/raw-clean/conftest.py) file in the `tests/e2e/raw-clean/` directory.
2. Move all existing fixtures from [`test_sns_notifications.py`](e2e/raw-clean/test_sns_notifications.py) to [`conftest.py`](e2e/raw-clean/conftest.py).
3. Create a new fixture named `generate_test_data` in `conftest.py`.
4. Use the `@pytest.fixture(autouse=True)` decorator for the new fixture.
5. Implement the fixture to call the data generator lambda function using boto3.
6. Assert that the data generator lambda function was called successfully.
7. Update `test_sns_notifications.py` to remove moved fixtures and use the new `generate_test_data` fixture.

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
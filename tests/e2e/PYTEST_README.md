# Exercise 2: Discovering pytest and boto3

Welcome to the second exercise of our ETL Testing Framework tutorial! In this exercise, you'll learn about pytest and boto3, and implement a fixture to generate test data for your E2E tests.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Exercise 2](#exercise-2-discovering-pytest-and-boto3)
    - [1. Setting up the testing environment](#1-setting-up-the-testing-environment)
    - [2. Executing and debugging test cases](#2-executing-and-debugging-test-cases)
    - [3. Implementing a Test Data Generator Fixture](#3-implementing-a-test-data-generator-fixture)
3. [Common Issues and Tips](#common-issues-and-tips)
4. [Exercise 2 Checklist](#exercise-2-checklist)
5. [Next Steps](#next-steps)
6. [Reference Solution](#reference-solution)
7. [Key Takeaways](#key-takeaways)

## Prerequisites
Before you begin, make sure you have completed Exercise 1 and have the following:
- AWS credentials configured
- Access to the repository and necessary AWS resources
- Basic understanding of Python, pytest, and boto3

## Exercise 2: Discovering pytest and boto3

### 1. Setting up the testing environment

1. Set up the testing environment by running the provided script:

```bash
cd scripts  
```

```bash
eval $(./setup_environment_tests.sh) 
```

2. Navigate to the `tests` directory:
```bash
cd ../tests/
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

### 2. Executing and debugging test cases

In this part of the exercise, you'll learn how to run and debug your test cases using pytest. Follow these steps to execute and debug your tests:

1. To run all tests with verbose output, use the following command:

   ```bash
   pytest -v
   ```

2. To run a specific test file, use:

   ```bash
   pytest e2e/raw-clean/test_lambda_raw_clean.py
   ```

3. To check for errors in test collection without actually running the tests, use:

   ```bash
   pytest --collect-only
   ```

4. For debugging, you can use the Test Explorer in the lateral menu of your CodeSpace. It's represented by a flask icon.

   ![Test Explorer in CodeSpace](../../assets/tests-debugger.png)

   The Test Explorer allows you to view and run individual tests or test suites. You can also set breakpoints and debug your tests interactively.

5. Expand the test tree to see all available tests. You should see a structure similar to:
   - etl-testing-fwk
     - tests
       - e2e
         - raw-clean
           - test_sns_notifications.py
             - TestRawToClean
               - test_lambda_execution

### 3. Implementing a Test Data Generator Fixture

In this exercise, you'll implement a fixture to generate test data for your E2E tests using pytest and boto3. This test data is crucial for verifying that data is correctly moved and processed in the clean layer of our ETL pipeline.

The need for generating test data arises from the requirement to have consistent, controlled data sets for our tests. By generating this data programmatically, we can ensure that our tests are repeatable and that they cover various scenarios that might occur in the real data processing pipeline.

Detailed instructions and code comments for this exercise are provided in the [`conftest.py`](raw-clean/conftest.py) file. You'll be working primarily with this file to implement the new fixture.

#### Steps:

1. Open the [`conftest.py`](raw-clean/conftest.py) file in the `tests/e2e/raw-clean/` directory.
2. Follow the steps described in the file to implement the test data generator fixture.
3. Run again the test:

```bash
pytest e2e/raw-clean/test_lambda_raw_clean.py
```

## Common Issues and Tips
- Ensure your AWS credentials are correctly configured and have the necessary permissions.
- Double-check that all required environment variables are set correctly.
- If tests fail, review the error messages and use debugging techniques to identify the issue.

## Exercise 2 Checklist

Use this checklist to ensure you've completed all the necessary steps for Exercise 2:

- [ ] Set up the testing environment
- [ ] Understand the existing test structure
- [ ] Move existing fixtures to conftest.py
- [ ] Implement the generate_test_data fixture
- [ ] Update test_sns_notifications.py to use the new fixture
- [ ] Run and verify the updated tests

Once you've checked off all these items, you've successfully completed Exercise 2!

## Next Steps
Once you have successfully implemented and verified the test data generator fixture, you are ready to move on to Exercise 3, where you'll explore how to generate Test Reports using Allure. Refer to the [Exercise 3: Integrating Allure Reports](ALLURE_README.md) for detailed instructions.

## Reference Solution

The final solution for all four exercises can be found in the `exercises_solution` folder. To use it, substitute the folders in the root directory with those in the solution folder and reexecute all steps from the first exercise.

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
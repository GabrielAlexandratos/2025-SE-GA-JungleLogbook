# Testing

We have been doing informal testing so far but now we want to make sure that everything is working as expected and that we can catch any issues early on. We will add in some unit tests and integration tests to make sure that everything is working as expected.

As a software engineer, we would write unit tests to ensure that individual components or functions work as expected. We will also write integration tests to make sure that different components or modules work together correctly. Depending on the company policy you may also write the system and acceptance tests, especially if they do not have a testing team which is common in smaller companies and those following agile methodologies.

As a test engineer, we would review the requirements and design a set of test scenarios and test cases. We will also create a test plan that outlines the scope of testing, the resources required, and the schedule for testing. Once we have our test plan in place, we can begin to execute our tests and document any issues or bugs that we find. These tests would be consider system and user acceptance testing.

## Test Scenarios

- Test Scenario 1: Successful Registration and Login
- Test Scenario 2: Invalid Email Address
- Test Scenario 3: Weak Password
- Test Scenario 4: Existing Email Address
- Test Scenario 5: Corrected Registration and Login

An example of how this would be describe is:

**Test Scenario 2: Invalid Email Address**

* Preconditions:
	+ The user has not previously created an account.
* Steps:
	1. Navigate to the registration page.
	2. Enter an invalid email address (e.g., "invalid_email").
	3. Click the "Register" button.
	4. Verify that the system displays an error message indicating that the email address is invalid.
	5. Attempt to log in with the same invalid email address.
	6. Verify that the system displays an error message indicating that the email address is not recognised.
* Expected Result:
	+ The system prevents registration with an invalid email address.
	+ The user cannot log in with an invalid email address.

**Test Scenario 4: Existing Email Address**

* Preconditions:
	+ A user has previously created an account with the same email address.
* Steps:
	1. Navigate to the registration page.
	2. Enter the email address of an existing user (e.g., "test@example.com").
	3. Click the "Register" button.
	4. Verify that the system displays an error message indicating that the email address is already in use.
	5. Attempt to log in with the same email address and password used for registration.
	6. Verify that the system successfully logs in the user, displaying their account information or dashboard.
* Expected Result:
	+ The system prevents registration with an existing email address.
	+ The user can log in using their email and password.

# Step 1: Setting up the testing environment

We will use pytest to write and run our tests due to its simplicity and powerful features such as fixtures, parameterization, and plugins. Unittest is another option that is built into Python but is more verbose to implement.

Add the pytest library to your `requirements.txt` and run `pip install -r requirements.txt` to install.

```
pytest==8.3.4
```

# Step 2: Writing the Test Cases

As the code is currently written there is no place to use unit tests. We would need to refactor the code to make it more testable. As an example of a unit test consider the following:

```python
# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5
```

You can read more about pytest at [https://docs.pytest.org/en/stable/](https://docs.pytest.org/en/stable/).

We can however write integration tests for the interactions with the database and also routes (urls) for our application.

Create a new folder called `tests` and add `test_expenses.py` in your project directory and add the following code:

```python
from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from expense_tracker.models import Base
from expense_tracker.services import ExpenseService

@pytest.fixture(scope='module')
def db_session():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        yield session
        session.rollback()
        session.close()

@pytest.fixture(scope='module')
def expense_service():
    yield ExpenseService()

def test_add_remove_expense(db_session, expense_service: ExpenseService):
    expense_service.create(db_session, 'test', 'category', 140.50, datetime.now(), "Groceries")
    assert len(expense_service.get_expenses(db_session)) == 1

def test_get_total_expenses(db_session, expense_service: ExpenseService):
    expense_service.create(db_session, 'test', 'category', 140.50, datetime.now(), "Groceries")
    expense_service.create(db_session, 'test', 'category', 200.50, datetime.now(), "Utilities")
    total_expenses = expense_service.calculate_total(db_session)
    assert total_expenses == 341.0
```

Note that we name our file starting with `test_` and also the methods that will be testing our application. This is because pytest will automatically discover and run any files that start with `test_` and any methods within those files that start with `test_`. If you want to run a specific test, you can use the `-k` option followed by the name of the test method or file.

The other habit to develop is using descriptive names for our tests. This will help us understand what each test is doing and also make it easier to identify which test is failing if a test fails. For example, `test_add_remove_expense` clearly indicates that this test is checking if the expense service can add an expense correctly and then removed. You could also append `_success` or `_failure` to indicate if the test is a success or failure scenario. For example, `test_add_remove_expense_success`.


> [!Tip]
> Although these tests are working. You should get into the practice of creating tests that fail on first execution. The reason for this is to ensure that you test is actually working as expected and not just passing because of some other reason. You can do this by intentionally introducing a bug in your code, running the test, and making sure that the test fails. Once you have confirmed that the test is failing as expected, you can then fix the bug in your code and run the test again to make sure it is now passing. Eg: You could change `341.0` to `342.0` in the above code and make sure that the test is failing as expected before fixing it.

> [!Note]
> There is a process call Test Driven Design (TDD) where we write the test before writing the code that makes the test pass. This can help us ensure that our code meets the requirements and is maintainable. It can also lead to software solutions that you didn't think of when you started coding as you are forced to consider all possible scenarios and ensure the code is testable. A drawback is that it can be time-consuming and require a lot of effort upfront.

## Running Tests
To run tests, you need to have Python installed on your machine. Once you have Python installed, you can run the tests by navigating to the top level directory of the project and running the following command:

```
pytest
```

You can also run the tests from within VSCode.

[< Prev: Expense Tracking > ](./expense_tracking.md) | [Next: Deployment >](./deployment.md)
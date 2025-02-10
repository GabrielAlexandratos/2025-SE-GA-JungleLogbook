# Testing

We have been doing informal testing so far but now we want to make sure that everything is working as expected and that we can catch any issues early on. We will add in some integration tests to make sure that everything is working as expected.

As a software engineer, we would write unit tests to ensure that individual components or functions work as expected. We would also write integration tests to make sure that different components or modules work together correctly. Depending on the company policy the software engineer may also write the system and acceptance tests, especially if they do not have a testing team which is common in smaller companies and those following agile methodologies.

As a test engineer, we would review the requirements and design a set of test scenarios and test cases. We would also create a test plan that outlines the scope of testing, the resources required, and the schedule for testing. Once we had our test plan in place, we would begin to execute our tests and document any issues or bugs that we find. These tests would be consider system and user acceptance testing.

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

We will use pytest to write and run our tests due to its simplicity and powerful features such as fixtures, parameterisation, and plugins. Unittest is another option that is built into Python but is more verbose to implement.

Add the pytest library to your `requirements.txt` and run `pip install -r requirements.txt` to install.

```
pytest==8.3.4
```

# Step 2: Writing Unit Test Cases

As the code is currently written there is no place to use unit tests. We would need to refactor the code to make it more testable. As an example of a unit test consider the following example. To try it out create a file named `test_sample.py` in the tests directory.

```python
# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5
```

To run the test, simply execute `pytest` in your terminal from the root of your project. You can also run the test through VSCode's IDE.

> [!Note]
> You will need to fix the test if it does not pass.

You can read more about pytest at [https://docs.pytest.org/en/stable/](https://docs.pytest.org/en/stable/).

We can however write integration tests for the interactions with the database and also routes (urls) for our application.

# Step 3: Writing Integration Test Cases

1. In the `tests` folder add `test_expenses.py` and add the following code:

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

2. Create a `pyproject.toml` file in the root of your project and add the following content:

```
[tool.pytest.ini_options]
pythonpath = [
  "src"
]
```

This configuration tells pytest where to look for the source code of our application. In this case, we are telling pytest to look in the `src` directory.

3. We will also need to go back through our src code and make local imports absolute paths instead of relative paths so our tests can find the methods and classes to call. For example, if we have the following import statement:
```python
from extensions import db, bcrypt
```
change it to:
```python
from expense_tracker.extensions import db, bcrypt
```

4. Their is also a bug in the code. We have initialised the database models incorrectly which prevents us from doing database integration tests. We need to change the following line in our models.py file:

```python
class Expense(db.Model):
# ...

class User(db.Model):
# ...
```

to 

```python
class Expense(Base):
# ...

class User(Base):
    __tablename__ = 'user'
# ...
```

5. Lastly, we need to add in an `__init__.py` file to your src/expense_tracker directory. This file can be empty, but it will tell Python that this directory should be considered a package. This is needed for `pytest` to discover your code for testing and considered best practice for modules that are part of a package or application.

> [!Tip]
> You should get into the practice of creating tests that fail on first execution. The reason for this is to ensure that your test is not just passing because it doesn't test the feature correctly or their is a bug in the code. You can do this by intentionally making the `assert` statement failing on first execution. Once you have confirmed that the test is failing as expected, you can then fix the bug in your test and run the test again to make sure it is now passing. Eg: You could change `341.0` to `342.0` in the above code and make sure that the test is failing as expected before fixing it.

> [!Note]
> There is a process call Test Driven Design (TDD) where we write the test before writing the code that makes the test pass. This can help us ensure that our code meets the requirements and is maintainable. It can also lead to software solutions that you didn't think of when you started coding as you are forced to consider all possible scenarios and ensure the code is testable. A drawback is that it can be time-consuming and require a lot of effort upfront.

## Running Tests
To run tests navigate to the top level directory of the project and running the following command:

```
pytest
```

You can also run the tests from within VSCode.

[< Prev: Expense Tracking > ](./expense_tracking.md) | [Next: Deployment >](./deployment.md)
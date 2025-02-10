# Adding a Database

## Introduction

In this section, we will learn how to add a database to our Flask application. We will use SQLite as our database since it is lightweight and easy to use.

## Step 1: Adding to the configuration file
1. It is good practice to keep you application configurations in a separate file. In a production deployment you would then override key values like passwords and access keys using environment variables. In `config.py` and add the following configuration to the DevelopmentConfig class:

```python

class DevelopmentConfig(Config):
    DEBUG = True
    ENVIRONMENT = "development"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expenses.db' # Set the database location for the application.
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable tracking modifications to reduce overhead.
    SECRET_KEY = 'your_secret_key_here' # Replace with a real secret key in production.
    SQLALCHEMY_ECHO = True  # Enable logging of SQL queries for debugging purposes.

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    ENVIRONMENT = "testing"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Set the database to be in-memory to simplify database cleanup when testing.
```

## Step 2: Include the modules need for database interactions
We will use SQLAlchemy which is an ORM (Object Relational Mapper) that provides some handy features to query and manage our database. You could also use `sqlite3` to connect to a SQLite database and execute SQL queries directly against the database. 

1. Add SqlAlchemy and Migrate to your `requirements.txt` file. We will use the `flask_sqlalchemy` extension which is a Flask extension for SQLAlchemy and `flask_migrate` for handling migrations. 

> [!Note]
> Migrations are a way to keep track of changes in your database schema. They allow you to update your database schema without losing data. By automatically generating migration scripts based on your model changes, you can easily apply these changes to your database. 


```
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.1.0
```

2. Run `pip install -r requirements.txt` to install the new packages.

## Step 3: Add in the code to create and migrate databases

1. Create a new file called `extensions.py` in your project directory. This file will contain all your database models. We will use this file later to extend our with additional functionality.

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db)
```

2. Update your `app.py` to look like the code below.

```python
from flask import Flask, render_template
import logging

from config import config, Config
from extensions import db, migrate      #1

logger = logging.getLogger(__name__)

def configure_logging(configuration: Config):
    '''Configure the logger to write to a file'''
    
    logger.setLevel(configuration.LOG_LEVEL)
    
    handler = logging.FileHandler(configuration.LOG_FILENAME, mode='w')
    formatter = logging.Formatter(configuration.LOG_FORMAT)

    # add formatter to the handler and logger
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def create_app(configuration: str = 'development') -> Flask:  #2

    app = Flask(__name__)

    configuration = config[configuration]
    configure_logging(configuration)
    app.config.from_object(configuration)

    db.init_app(app)  #3
    migrate.init_app(app, db)  #4

    @app.route('/')
    def index():
        logger.info("Rendering the index page")
        return render_template('index.html')

    return app

if __name__ == '__main__':
    create_app('development').run()
```
1. Import the extension module where we create the database and migrations.
2. Provide a default configuration to allow us to run migrations without specifying a configuration.
3. Initialize SQLAlchemy with Flask app.
4. Initialize Flask-Migrate with Flask app and SQLAlchemy.

## Step 4. Create the Database Tables

Up to now, the work we have done in the code has been to satisfy non-functional requirements such as logging and configuration management. Now we need to start creating the tables for our application that will support our functional requirements.

Create a file called `models.py` in your project directory and add the following code:

```python
from extensions import db
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone

# Define the base class for declarative models.
class Base(DeclarativeBase):                  ## 1
  pass

class Expense(db.Model):                      ## 2
    __tablename__ = 'expense'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.Date, nullable=False, default=datetime.now(timezone.utc))
    description = db.Column(db.String(255), nullable=True)


    def __repr__(self):                       ## 3
        return f"Expense('{self.title}', '{self.category}', {self.amount}, {self.date})"
```

1. Define a base class `Base` for all declarative models using SQLAlchemy's DeclarativeBase.
2. Create an `Expense` model with fields for title, category, amount, date, and description. The `id` field is set as the primary key.
3. Define a `__repr__` method for the model to provide a string representation of an instance. This is useful for debugging and logging purposes.

To create the database tables based on the defined models, you can use Flask-Migrate's migration commands:
```
flask db init
```

Once this has run successfully you need to modify the `env.py` to be able to find your models.

Replace the comments that look like:
``` python
# Add your model's MetaData object here
# for 'autogenerate' support
# from myapp import db_session
# target_metadata = db_session.get_bind()
```

with

```python
from expense_tracker.models import Base  # noqa: E402
target_metadata = Base.metadata
```

Then run the following commands to generate a migration script and apply it to create the tables:

```
flask db migrate -m "Initial migration."
flask db upgrade
```
This will initialize a migrations directory, create an initial migration script, and apply the migration to create the tables in your database. 

Once you have run these commands, select the database which will be in '/instance/expenses.db' and see that the 'expenses' table has been created with the appropriate columns. 

> [!Note]
> There is more going on here with using Flask-SQLAlchemy, but it is not a requirement to understand the details. You can read more about it at[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) and [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/).

## Step 5: Verify everything working
```
flask run --debug
```
Then check you have a webpage that works and it is logging information when we visit the page. 

[< Prev: Logging](./database.md) | [Next: Authentication Backend >](./user_auth_backend.md)
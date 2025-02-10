import logging

class Config:
    LOG_LEVEL = logging.WARN
    LOG_FILENAME = 'app.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    LOG_LEVEL = logging.INFO
    DEBUG = True
    ENVIRONMENT = "development"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expenses.db' # Set the database location for the application.
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable tracking modifications to reduce overhead.
    SECRET_KEY = 'your_secret_key_here' # Replace with a real secret key in production.
    SQLALCHEMY_ECHO = True  # Enable logging of SQL queries for debugging purposes.


class TestingConfig(Config):
    LOG_LEVEL = logging.INFO
    DEBUG = True
    TESTING = True
    ENVIRONMENT = "testing"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Create an in-memory database to simplify database cleanup when testing.

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
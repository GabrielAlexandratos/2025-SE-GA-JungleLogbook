# Logging in the Application

Logging is an essential aspect of any software application, as it helps in tracking and debugging issues that may arise during runtime. In this section, we will discuss how to implement logging in our application. An alternative is to use print statements throughout your code but this approach can be cumbersome and difficult to maintain.

## Step 1: Define the Log Levels
Before we start implementing logging, we need to define the different log levels that our application will use. These levels will help us categorise the logs based on their severity and importance.
- **DEBUG**: This level is used for debugging purposes. It provides detailed information about the internal workings of the application.
- **INFO**: This level is used for informational purposes. It provides general information about the state of the application.
- **WARNING**: This level is used for warning messages. It indicates that something may go wrong in the future, but it does not necessarily mean an error has occurred.
- **ERROR**: This level is used for error messages. It indicates that an error has occurred and the application cannot continue running.
- **CRITICAL**: This level is used for critical errors. It indicates that the application cannot continue running and the system may be in a state of emergency.

Fortunately, python has a library that supports these logging levels so you don't need to define these yourself. 

Syllabus: PW-DW-11.01, PF-SD-01.6

## Step 2: Implement the Logger
Once we have defined the log levels, we can implement the logger in our application. The logger will be responsible for writing logs to a file. Some companies will use a database to store logs but many companies will create structure or unstructured log files that are then loaded into an ELK stack if using an open source solution or Splunk if using a commercial solution.

``` python
from flask import Flask, render_template
import logging                                # 1

logger = logging.getLogger(__name__)          # 2

def configure_logging(configuration: Config):
    """Configure the logger to write to a file"""

    logger.setLevel(configuration.LOG_LEVEL)

    handler = logging.FileHandler(configuration.LOG_FILENAME, mode="w")
    formatter = logging.Formatter(configuration.LOG_FORMAT)

    # add formatter to the handler and logger
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def create_app(configuration: str = "default") -> Flask:
    app = Flask(__name__)

    configuration = config[configuration]
    configure_logging(configuration)
    app.config.from_object(configuration)

    @app.route('/')
    def index():
        logger.info("Rendering the index page")
        return render_template('index.html')

    return app

if __name__ == '__main__':
    create_app('config.DevelopmentConfig').run()
```

1. import the logging module
2. create a logger object using logging.getLogger(__name__)
3. configure the logger by setting the filename and level

## Step 3: Configure the Logger
After implementing the logger, we need to configure it so that it writes logs to the correct file. This can be done by setting environment variables or by modifying configuration files in our application. We should also consider how we will handle log rotation and compression to ensure that our logs are not too large or difficult to manage.

We can move the configuration of the logger into `config.py` to improve functionality and use different settings when testing, developing or in production.



## Step 4: Test the Logger
Once we have implemented and configured the logger, we need to test it thoroughly to ensure that it works as expected. This can be done by writing unit tests for the logger and integration tests for the entire application. We should also consider how we will handle log errors and exceptions to ensure that our logs are not corrupted or incomplete.

## Step 5: Document the Logger
Finally, we need to document the logger so that other developers can understand how it works and how to use it in their applications. This can be done by writing a README file for the logger and creating documentation for the entire application. We should also consider how we will handle log changes and updates to ensure that our logs are always up-to-date with the latest changes in the application.

More details on logging in python can be found at [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html).

[< Prev: Refactoring](./refactor_for_extensibility_and_scalability.md) | [Next: Database >](./database.md)
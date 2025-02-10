# Refactor for Extensibility and Scalability

## What do we mean when we say refactor? 
Refactoring is the process of restructuring existing code without changing its external behaviour. It's a way to improve the internal structure of your code, making it easier to understand, maintain, and extend. This can be labelled as paying down technical debt as it is improving the quality of the codebase.

## Why do we need to refactor? 
Refactoring is necessary because as our application grows, the initial design may become less effective. Refactoring helps us to improve the structure of our code and make it more maintainable. It also allows us to add new features without breaking existing functionality.

> [!Tip]
> Refactoring should only be done when there is a clear benefit, such as improving performance or making the code more maintainable. Refactoring should not be done for the sake of refactoring. Also, you should not add features when refactoring as it can introduce new technical debt and make it harder to prove that your refactoring has not broken something.


## How can we refactor for extensibility and scalability? 
There are several ways to refactor for extensibility and scalability, including:

1. **Using design patterns**: Design patterns provide proven solutions to common problems in software design. By using design patterns, we can create code that is more modular, reusable, and easier to understand.
2. **Implementing a microservices architecture**: A microservices architecture allows us to break our application into smaller, independent services that can be developed, deployed, and scaled independently. This makes it easier to add new features and improve the performance of our application.
3. **Using an application factory pattern**: An application factory pattern is a design pattern that allows us to create instances of our application without hardcoding any dependencies. This makes it easier to test our code and make changes to our application in the future.
4. **Implementing a layered architecture**: A layered architecture separates our application into different layers, each with its own responsibility. This makes it easier to understand and maintain our code, as well as to add new features without breaking existing functionality.

## Conclusion 
Refactoring is an important part of the development process, especially for large applications. By using design patterns, implementing a microservices architecture, using an application factory pattern, and implementing a layered architecture, we can refactor our code for extensibility and scalability. This will make it easier to add new features, improve maintainability, and improve the performance of our application in the future. 

> [!Note]
> You don't need to apply all of these techniques to refactor code. There are many other techniques and patterns that can be used to refactor code, depending on the specific needs of your application. The key is to identify areas where refactoring will improve maintainability and scalability, and then apply the appropriate techniques.

## Step 1: Make it a Factory Application

Change main to be the following:
```python

from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)

```

Run the application and make sure it is working. This is a simple factory application that creates an instance of the Flask app and returns it. This allows us to easily create multiple instances of the app in different environments, such as development and testing.

We have also ensured we haven't added any new functionality so to prove that the change was successful

See [Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) for more details.

## Step 2: Implement a configuration file

Creating a configuration file allows us to separate our configuration settings from our code. We can also use different configuration files for different environments, such as development and testing. This allows us to easily switch between different configurations and manage our settings without changing our code. 

``` python
# config.py
class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    ENVIRONMENT = "development"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    ENVIRONMENT = "testing"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
```

We are using inheritance to create different configuration classes for different environments. We can then use a dictionary to map the environment name to the corresponding configuration class. This allows us to easily switch between different configurations by passing in the appropriate environment name when we create an instance of the app.

> [!Note]
> Using python is one of many types of file formats that can be used to store configuration data. You could also use json, ini or yaml file formats as well.

See [Flask Configuration](https://flask.palletsprojects.com/en/stable/config/) for more details.

## Step 3: Update the application to use the configuration file

We need to update our application to use the configuration file. We can do this by passing the configuration object to the `create_app()` function when we create an instance of the app. I have also added in some type information to make our code easier to read.

``` python
from flask import Flask, render_template

from config import config   #1

def create_app(configuration: str = 'default') -> Flask:   #2

    app = Flask(__name__)

    configuration = config[configuration]
    app.config.from_object(configuration)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    create_app('development').run()
```

1. Importing the configuration module.
2. Defining a function to configure the application based on the provided configuration object using the `default` configuration if one is not provided.

> [!TIP]
> Try changing the configuration file to `testing` and see how it affects the application.

[< Prev: Serving a webpage](./serving_a_webpage.md) | [Next: Logging >](./logging.md)








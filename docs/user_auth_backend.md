# User Authentication Backend

One of the requirements is to provide user authentication. See:
- [Functional Requirement 1](https://github.com/orgs/KillarneyHeightsHS/projects/2?pane=issue&itemId=95481908)

## Implementation Details

Flask provides a simple way to implement user authentication using the `flask_login` extension. This extension provides user session management for Flask applications, handling the common tasks of logging in, logging out, and remembering users' sessions over extended periods of time. `Flask-Bcrypt` is used to hash passwords for security.

## Step 1: Install flask-login
Update the requirements.txt file with the following line:
```
flask_login==0.6.3
Flask-Bcrypt==1.0.1
```

and install the module.

```
pip install -r requirements.txt
```


## Step 2: Setup the user model in `models.py`

``` python
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password) #1
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<email {self.email}>"
```
1. It is important that we hash the password before storing it in the database so as not to expose sensitive information. This is not the most secure way of hashing passwords, we should also salt the password as well, but it is sufficient for this example.

## Step 3: Add extensions for user authentication and password hashing

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate(db)
bcrypt = Bcrypt()     #1
login_manager = LoginManager()  #2
```
1. We are using `Flask-Bcrypt` to handle password hashing and verification.
2. We are using `Flask-Login` to manage user sessions.

## Step 4: Adding a service layer
It is good practice to not directly access the database directly from our models, instead we should use a service layer to handle all database operations. Lets create one for the user model in a new file called `services.py`.

```python
from models import User

class UserService:
    def get_user(self, user_id):
        return User.query.get(user_id)
```

## Step 5: Update `app.py`

```python
from flask import Flask, render_template
import logging

from config import config, Config
from extensions import db, migrate, login_manager   #1
from services import UserService                    #2

logger = logging.getLogger(__name__)

def configure_logging(configuration: Config):
    '''Configure the logger to write to a file'''
    
    logger.setLevel(configuration.LOG_LEVEL)
    
    handler = logging.FileHandler(configuration.LOG_FILENAME, mode='w')
    formatter = logging.Formatter(configuration.LOG_FORMAT)

    # add formatter to the handler and logger
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def create_app(configuration: str = 'development') -> Flask:

    app = Flask(__name__)

    configuration = config[configuration]
    configure_logging(configuration)
    app.config.from_object(configuration)

    login_manager.init_app(app)
    db.init_app(app)  # Initialize SQLAlchemy with Flask app
    migrate.init_app(app, db)  # Initialize Flask-Migrate with Flask app and SQLAlchemy

    @app.route('/')
    def index():
        logger.info("Rendering the index page")
        return render_template('index.html')

    return app

user_service = UserService()        #3

# used to reload the user object from the user ID stored in the session
@login_manager.user_loader          #4
def load_user(user_id: str):
    return user_service.get_user(user_id)

if __name__ == '__main__':
    create_app('development').run()

```

1. import the login_manager
2. import the user service we create to have access to verifying a user's credentials.
3. create an instance of the UserService class.
4. Verify that a user is authenticated by checking their credentials against the database.


## Question
1. Why would we only return the email address for the user in the __repr__ method?

Once you have the code in place try to run it and see if it works as expected.

## Step 6: Create routes for authentication
We want to support user authentication in our application. To do this we will create a UI for user login and implement the necessary backend logic to handle the login process. We will also need to ensure that the user's credentials are verified against the database before granting access to the application. The routes needed are:

- `/login` - This route will display the login form.
- `/logout` - This route will log out the user and redirect them to the login page.
- `/register` - This route will allow a user to register for an account.

To keep our app clean we don't want to keep adding routes to `app.py`. Instead we will create a new file called `auth.py` and move all of the authentication routes there.

Create the following routes in `auth.py`:

```python
from flask import Blueprint, redirect, render_template

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')   #1

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])   #2
def login_post():
    # login code goes here
    return redirect('/home')

@auth_bp.route('/logout')
def logout():
    return render_template('logout.html')

@auth_bp.route('/register')
def register():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register_post():
    # registration code goes here
    return redirect('/home')
```

1. Create a new Blueprint for authentication routes. This will allow us to organise our routes better and keep them separate from other parts of the app.
2. Add a POST route to handle form submissions. When a user submits the login form, this route will be called. We can then add code to check the user's credentials and log them in if they are correct. The form used will send a `post` request to `/auth/login`.

> [!Note]
> There are several verbs that can be used with routes, such as GET, POST, PUT and DELETE. Each verb has its own purpose
> - GET: retrieves data from a specified resource.
> - POST: sends data to be processed to a specified resource.
> - PUT: updates or replaces an existing resource with new data.
> - DELETE: removes a specified resource.

To load blueprint in the app, we need to import it and register it with the Flask application. In `app.py`, add the following code:

```python
from flask import Flask, render_template
import logging

from config import config, Config
from extensions import db, migrate, login_manager
from services import UserService

from auth import auth_bp

logger = logging.getLogger(__name__)

# .... other code not changed

def create_app(configuration: str = 'development') -> Flask:

    app = Flask(__name__)
    app.register_blueprint(auth_bp) 

    configuration = config[configuration]

# .... other code not changed

    @app.route('/home')
    def home():
        logger.info("Rendering the home page")
        return render_template('home.html')

    return app
```

[< Prev: Database](./database.md) | [Next: Authentication Frontend >](./user_auth_frontend.md)
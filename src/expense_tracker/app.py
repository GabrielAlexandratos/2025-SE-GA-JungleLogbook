from flask import Flask, render_template
import logging

from config import config, Config
from extensions import db, migrate, login_manager, db_session
from services import UserService

from auth import auth_bp

logger = logging.getLogger(__name__)

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
    app.register_blueprint(auth_bp) 

    configuration = config[configuration]
    configure_logging(configuration)
    app.config.from_object(configuration)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        logger.info("Rendering the index page")
        return render_template('index.html')

    @app.route('/home')
    def home():
        logger.info("Rendering the home page")
        return render_template('home.html')

    return app

user_service = UserService()

# used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id: str):
    return user_service.get_user(db_session(), user_id)

if __name__ == '__main__':
    create_app('development').run()
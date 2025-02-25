from flask import Flask, render_template
import logging

from flask_login import login_required

from expense_tracker.config import config, Config
from expense_tracker.extensions import db, migrate, login_manager, db_session, csrf
from expense_tracker.services import UserService, ExpenseService

from expense_tracker.auth import auth_bp
from expense_tracker.expense_routes import expense_bp


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
    app.register_blueprint(expense_bp)

    configuration = config[configuration]
    configure_logging(configuration)
    app.config.from_object(configuration)

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    @app.route('/')
    def index():
        logger.info("Rendering the index page")
        return render_template('index.html')

    @app.route("/home")
    @login_required
    def home():
        logger.info("Rendering the home page")
        expenses = expense_service.get_expenses(db_session())
        total = expense_service.calculate_total(db_session())
        logger.info(f"Calculated total expenses: {total}")
        logger.info(f"Retrieved {len(expenses)} expenses for the current user")
        logger.info("Rendering the home page with expenses")
        return render_template("home.html", expenses=expenses, total_amount=total)

    return app

user_service = UserService()
expense_service = ExpenseService()

# used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id: str):
    return user_service.get_user(db_session(), user_id)

if __name__ == '__main__':
    create_app('development').run()
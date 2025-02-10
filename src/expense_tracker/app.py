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
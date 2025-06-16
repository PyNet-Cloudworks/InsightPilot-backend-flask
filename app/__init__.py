import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load config from environment
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')  # if you use a DB

    from .routes import main
    app.register_blueprint(main)

    return app

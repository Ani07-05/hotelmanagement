# app/app.py
from flask import Flask
from .config import Config
from .database import DatabaseManager

db_manager = DatabaseManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        from . import routes
        routes.init_app(app)

    return app
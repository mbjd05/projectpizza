# The __init__.py file is used to create the flask app which then initializes the database connection and registers the blueprints. The blueprints are used to separate the routes into different files.
import configparser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

config = configparser.ConfigParser()
config.read('config.ini')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{config.get("mysql", "user")}:{config.get("mysql", "password")}@{config.get("mysql", "host")}/{config.get("mysql", "db")}'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Blueprint registration for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint registration for main routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

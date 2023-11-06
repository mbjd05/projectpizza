# The __init__.py file is used to create the flask app which then initializes the database connection and registers the blueprints. The blueprints are used to separate the routes into different files.
import configparser
from flask import Flask
from .models import db
from .helpers import add_pizzas_from_json, total_pizza_quantity
from flask_login import LoginManager

config = configparser.ConfigParser()
config.read('config.ini')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{config.get("mysql", "user")}:{config.get("mysql", "password")}@{config.get("mysql", "host")}/{config.get("mysql", "db")}'
    app.secret_key = config.get("app", "secret_key")
    app.config['SESSION_TYPE'] = 'filesystem'
    @app.context_processor
    def utility_functions():
        return dict(total_pizza_quantity=total_pizza_quantity)

    db.init_app(app)
    with app.app_context():
        from .models import User, Pizzas, Orders
        db.create_all()
        add_pizzas_from_json(Pizzas)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # Blueprint registration for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint registration for main routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

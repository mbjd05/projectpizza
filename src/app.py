# The __init__.py file is used to create the flask app which then initializes the database connection and registers the blueprints. The blueprints are used to separate the routes into different files.
import configparser
from flask import Flask
from flask_socketio import SocketIO
from models import db, Pizzas, Orders
from helpers import *
from sqlalchemy import and_
from threading import Thread
import time

config = configparser.ConfigParser()
config.read('config.ini')

def main():
    app = Flask(__name__)
    socketio = SocketIO(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{config.get("mysql", "user")}:{config.get("mysql", "password")}@{config.get("mysql", "host")}/{config.get("mysql", "db")}'
    app.secret_key = config.get("app", "secret_key")
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    with app.app_context():
        from models import Pizzas, Orders
        db.create_all()
        add_pizzas_from_json(Pizzas)

    # Blueprint registration for main routes
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app, socketio


def check_orders():
      while True:
        with app.app_context():  
            time.sleep(5)
            updated_orders = Orders.query.filter(and_(Orders.ready == 1, Orders.picked_up == 0)).all()
            for order in updated_orders:
                socketio.emit('order_ready', {'order_id': order.order_id})

def ordercheck_in_backround():
    t = Thread(target=check_orders)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    app, socketio = main()  # Create the Flask app and SocketIO
    ordercheck_in_backround() # Start the order check function in the background
    socketio.run(app, debug=True, port=5000)
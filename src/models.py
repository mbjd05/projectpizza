# Models are classes that translate to database tables
# Each class is a table and each attribute is a column

from sqlalchemy import  Nullable
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression

db = SQLAlchemy()

class Pizzas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    position = db.Column(db.Integer)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer)
    pizza_id = db.Column(db.Integer, nullable=False)
    pizza_name = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    ready = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    picked_up = db.Column(db.Boolean, server_default=expression.false(), nullable=False)

    #Set the pizza_name in the orders table from the name field in the pizzas table
    def set_pizza_name(self):
        pizza = Pizzas.query.get(self.pizza_id)
        if pizza:
            self.pizza_name = pizza.name
        else:
            self.pizza_name = "Unknown"
    
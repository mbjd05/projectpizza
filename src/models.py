# Models are classes that translate to database tables
# Each class is a table and each attribute is a column
from flask_login import UserMixin
from sqlalchemy import  Nullable
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(1000))

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

    def set_pizza_name(self):
        pizza = Pizzas.query.get(self.pizza_id)
        if pizza:
            self.pizza_name = pizza.name
        else:
            self.pizza_name = "Unknown"
    
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, session, url_for
import json
from models import db, Pizzas

def add_pizzas_from_json(Pizzas):
    # Read the pizzas.json file
    with open('pizzas.json') as f:
        pizzas_data = json.load(f)

    # Add or update pizzas in the Pizzas table
    for pizza_data in pizzas_data:
        pizza = Pizzas.query.filter_by(name=pizza_data['name']).first()
        if not pizza: # If the pizza does not exist, add it.
            pizza = Pizzas(name=pizza_data['name'], price=pizza_data['price'], description=pizza_data['description'], position=pizza_data['position'])
            db.session.add(pizza)
        else:
            pizza.position = pizza_data['position']
            db.session.commit()

    # Delete pizzas that are not in the JSON file
    for pizza in Pizzas.query.all():
        if not any(p['name'] == pizza.name for p in pizzas_data): # If the pizza is not in the JSON file, delete it.
            db.session.delete(pizza)
    db.session.commit()
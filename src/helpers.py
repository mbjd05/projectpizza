from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

def add_pizzas_from_json(Pizzas):
    # Read the pizzas.json file
    with open('pizzas.json') as f:
        pizzas_data = json.load(f)

    # Add pizzas to the Pizzas table
    for pizza_data in pizzas_data:
        pizza = Pizzas.query.filter_by(name=pizza_data['name']).first()
        if not pizza:
            pizza = Pizzas(name=pizza_data['name'], price=pizza_data['price'], description=pizza_data['description'])
            db.session.add(pizza)

    db.session.commit()

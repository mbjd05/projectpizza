from flask import Blueprint, render_template
from helpers import *
from models import Pizzas, Orders
from flask_cors import cross_origin
import json, random

main = Blueprint('main', __name__)

@main.route('/Order', methods=['POST', 'OPTIONS'])
@cross_origin()
def new_order():
    data = request.get_json()
    #get all order_id from Orders table and keep regenerating until a unique one is found
    unique = False
    while not unique:
        order_id = int(random.randrange(1, 300))
        existing_order_ids = Orders.query.with_entities(Orders.order_id).distinct().all() #get all exiting order_ids once, using distinct.
        if order_id not in existing_order_ids:
            unique = True
    for item in data['items']:
        pizza = Pizzas.query.get(item['id'])
        if pizza:
            order = Orders(order_id=order_id, pizza_id=str(item['id']), quantity=str(item['quantity']))
            order.set_pizza_name()   
            db.session.add(order)
    db.session.commit()
    return_str = f"Your order id is: {order_id}"
    #change retun_str to json
    response = json.dumps(return_str)
    return response

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/kitchen')
def kitchen():
    return render_template('kitchen.html')
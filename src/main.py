from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .helpers import *
from .models import Pizzas, Orders
from flask_cors import cross_origin
import json, uuid

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pizzas = Pizzas.query.order_by(Pizzas.position).all()
    return render_template('index.html', pizzas=pizzas)

@main.route('/Order', methods=['POST', 'OPTIONS'])
@cross_origin()
def recieve_data():
    data = request.get_json()
    #print(data)
    for item in data['items']:
        pizza = Pizzas.query.get(item['id'])
        if pizza:
            print(f"id: {item['id']}, quantity: {item['quantity']}, name: {pizza.name}")
            unique = False
            while not unique:
                order_id = str(uuid.uuid4())
                existing_order = Orders.query.filter_by(order_id=order_id).first()
                if not existing_order:
                    unique = True
            order = Orders(order_id=order_id)   

            #return a client id for tracking order
            return_str = f"Your order id is: {order_id}"
    return return_str, 200

@main.route('/orders')
@login_required
def orders():
    return render_template('orders.html', username=current_user.name)

@main.route('/checkout')
@login_required
def checkout():
    #session stored orders to db
    order = session.get('order', [])

    return render_template('checkout.html', username=current_user.name)

@main.route('/clearorder')
def clear_order():
    session.pop('order', None)
    return redirect(url_for('main.index'))

@main.route('/reviews')
def reviews():
    return render_template('reviews.html')
from flask import Blueprint, render_template, send_from_directory
from flask_login import current_user, login_required
from .helpers import *
from .models import Pizzas
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pizzas = Pizzas.query.order_by(Pizzas.position).all()
    return render_template('index.html', pizzas=pizzas)

@main.route('/Order', methods=['POST'])
def recieve_data():
    data = request.get_json()
    session['order'] = data['pizzaID']
    print(session['order'])
    return 'good job!', 200

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
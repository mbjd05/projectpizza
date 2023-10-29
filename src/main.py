from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .helpers import *
from .models import Pizzas

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pizzas = Pizzas.query.order_by(Pizzas.position).all()
    return render_template('index.html', pizzas=pizzas)

@main.route('/orders')
@login_required
def orders():
    return render_template('orders.html', username=current_user.name)
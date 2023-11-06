from flask import Blueprint, render_template, send_from_directory
from flask_login import current_user, login_required
from .helpers import *
from .models import Pizzas

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pizzas = Pizzas.query.order_by(Pizzas.position).all()
    return render_template('index.html', pizzas=pizzas)

@main.route('/order', methods=['POST'])
def add_pizza():
    pizza_id = request.form.get('pizza_id')
    quantity = int(request.form.get('quantity'))

    pizza = Pizzas.query.get(pizza_id)
    order = session.get('order', [])  # Initialize order as an empty list

    for item in list(order):  # Create a copy of the list for iteration
        if item['pizza_id'] == pizza_id:
            item['quantity'] += quantity  # adjust quantity
            if item['quantity'] <= 0:
                # If updated quantity is 0 or less, remove the pizza type from the order
                order.remove(item)
            break
    else:
        # If pizza_id was not in the order and quantity is greater than 0, add it
        if quantity > 0:
            order.append({
                'pizza_id': pizza_id, 
                'name': pizza.name, 
                'quantity': quantity, 
                'price': pizza.price
            })

    # If quantity is 0, remove the pizza from the order
    if quantity == 0:
        order = [item for item in order if item['pizza_id'] != pizza_id]

    session['order'] = order  # Update the session with the new order
    print(session['order'])

    return redirect(url_for('main.index'))  # Redirect back to the index page

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
<<<<<<< HEAD
    return render_template('reviews.html')

@main.route('/contact_us')
def contact_us():
    return render_template('Contact_us.html')
=======
    return render_template('reviews.html')
>>>>>>> 01338598fed69c191835e2c14c66793197f3451a

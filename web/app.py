#!/usr/bin/python3

""" this is a module for the application,
it handles the routing process and serve dynamic content
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask import abort, flash, jsonify
from models import storage
from models.user import User
from models.category import Category
from models.transaction import Transaction
import hashlib
import service
import secrets
import json
from datetime import datetime
from decimal import Decimal

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key


@app.teardown_appcontext
def close_session(exception):
    """ close session """
    storage.close()


@app.route('/')
def index():
    """ index page """
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """ dashboard page """
    if 'user' not in session:
        return redirect(url_for('login'))

    user = storage.get_object(User, session['user'])
    categories = service.get_categoiries_for_user(user)
    transactions = service.transactions_for_user(user)
    return render_template('dashboard.html',
                           user=user,
                           categories=categories,
                           transactions=transactions)


@app.route('/login', methods=['GET'])
def login():
    """ login page """
    if 'user' in session:
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    """ login post """

    email = request.form['email']
    password = request.form['password']
    password = hashlib.md5(password.encode()).hexdigest()
    user = service.get_user(email, password)
    if user:
        session['user'] = user.id
        return redirect(url_for('dashboard'))
    # if wrong credentials
    # return to login page with error message
    return render_template('login.html', error='Invalid email or password')


@app.route('/logout')
def logout():
    """ logout """
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET'])
def register():
    """ register page """
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    """ register post """

    email = request.form['email']
    password = request.form['password']
    password_confirmation = request.form['confirm_password']
    name = request.form['name']

    if password != password_confirmation:
        return render_template('register.html',
                               error='Password and confirmation do not match')

    if len(password) < 8:
        return render_template('register.html',
                               error='Password must be at least 8 characters')

    if "@" not in email or "." not in email:
        return render_template('register.html', error='Invalid email')

    if service.check_email(email):
        return render_template('register.html', error='User already exists')

    password = hashlib.md5(password.encode()).hexdigest()
    user = User(name=name, email=email, password=password)
    user.save()
    session['user'] = user.id
    # message success on sign up and redirect to dashboard
    return render_template('register.html',
                           success='User created successfully')


@app.route('/api/v1/categories', methods=['GET'])
def categories():
    """ categories page """
    if 'user' not in session:
        return redirect(url_for('login'))

    user = storage.get_object(User, session['user'])
    categories = service.get_categoiries_for_user(user)
    headers = {'Content-Type': 'application/json'}
    body = {'categories': [service.to_dict(
        category) for category in categories]}
    body = json.dumps(body)
    return body, 200, headers


@app.route('/api/v1/transactions', methods=['GET'])
def transactions():
    """ transactions page """
    if 'user' not in session:
        return redirect(url_for('login'))

    user = storage.get_object(User, session['user'])
    transactions = service.transactions_for_user(user)
    headers = {'Content-Type': 'application/json'}
    body = {
        'transactions': [service.to_dict(transaction) for transaction in transactions]
    }
    body = json.dumps(body)
    return body, 200, headers


@app.route('/api/v1/income-month', methods=['GET'])
def income_month():
    """ income month page """
    if 'user' not in session:
        return redirect(url_for('login'))

    user = storage.get_object(User, session['user'])
    transactions = service.transactions_for_user(user)
    income = 0
    for transaction in transactions:
        if (transaction.amount > 0
                and transaction.created_at.month == datetime.now().month):
            income += transaction.amount
    headers = {'Content-Type': 'application/json'}
    body = {'income': str(income)}
    body = json.dumps(body)
    return body, 200, headers


@app.route('/api/v1/expenses-month', methods=['GET'])
def expense_month():
    """ expense month page """
    if 'user' not in session:
        return redirect(url_for('login'))

    user = storage.get_object(User, session['user'])
    transactions = service.transactions_for_user(user)
    expense = 0
    for transaction in transactions:
        if (transaction.amount < 0
                and transaction.created_at.month == datetime.now().month):
            expense += transaction.amount
    headers = {'Content-Type': 'application/json'}
    body = {'expenses': str(expense)}
    body = json.dumps(body)
    return body, 200, headers


@app.route('/categories', methods=['GET'])
def category():
    """ category page """
    if 'user' not in session:
        return redirect(url_for('login'))

    user = storage.get_object(User, session['user'])
    return render_template('categories.html', user=user)


@app.route('/transactions', methods=['GET'])
def transaction():
    """ transaction page """
    if 'user' not in session:
        return redirect(url_for('login'))

    user = storage.get_object(User, session['user'])
    categories = service.get_categoiries_for_user(user)
    return render_template('transactions.html',
                           user=user, categories=categories)


@app.route('/api/v1/transactions', methods=['POST'])
def transaction_post():
    """ transaction post """
    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'User not logged in'
        }), 401

    user = storage.get_object(User, session['user'])
    data = request.get_json()
    amount = data['amount']
    amount = Decimal(amount)
    amount_type = data['type']
    category_id = data['category_id']
    date = data['date']
    category = storage.get_object(Category, category_id)
    date = datetime.strptime(date, "%Y-%m-%d")
    if amount_type == 'Income':
        amount = abs(amount)
    else:
        amount = -abs(amount)

    transaction = Transaction(amount=amount, created_at=date)
    user.add_transaction(transaction, category)
    storage.save()

    return jsonify({
        'success': True,
        'transaction': {
            'id': transaction.id,
            'date': transaction.created_at,
            'amount': str(transaction.amount),
            'category': category.name,
            'type': amount_type,
            'created_at': transaction.created_at,
            'name': category.name,
            'category_id': category.id
        }
    })


@app.route('/api/v1/transactions/<transaction_id>', methods=['PUT'])
def transaction_put(transaction_id):
    """ transaction put """
    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'User not logged in'
        }), 401

    user = storage.get_object(User, session['user'])
    transaction = storage.get_object(Transaction, transaction_id)
    if transaction.user_id != user.id:
        return jsonify({
            'success': False,
            'message': 'Transaction does not belong to user'
        }), 401

    data = request.get_json()
    amount = data['amount']
    amount = Decimal(amount)
    amount_type = data['type']
    category_id = data['category_id']
    date = data['date']
    category = storage.get_object(Category, category_id)
    date = datetime.strptime(date, "%Y-%m-%d")
    if amount_type == 'Income':
        amount = abs(amount)
    else:
        amount = -abs(amount)

    transaction.amount = amount
    transaction.created_at = date
    transaction.category_id = category_id
    storage.save()

    return jsonify({
        'success': True,
        'transaction': {
            'id': transaction.id,
            'date': transaction.created_at,
            'amount': str(transaction.amount),
            'category': category.name,
            'type': amount_type,
            'created_at': transaction.created_at,
            'name': category.name,
            'category_id': category.id
        }
    })


@app.route('/api/v1/transactions/<transaction_id>', methods=['DELETE'])
def transaction_delete(transaction_id):
    """ transaction delete """
    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'User not logged in'
        }), 401

    user = storage.get_object(User, session['user'])
    transaction = storage.get_object(Transaction, transaction_id)
    if transaction.user_id != user.id:
        return jsonify({
            'success': False,
            'message': 'Transaction does not belong to user'
        }), 401

    storage.delete(transaction)
    storage.save()

    return jsonify({
        'success': True,
        'message': 'Transaction deleted successfully'
    })


@app.route('/api/v1/categories', methods=['POST'])
def category_post():
    """ category post """
    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'User not logged in'
        }), 401

    user = storage.get_object(User, session['user'])
    data = request.get_json()
    name = data['name']
    date = data['date']
    current_balance = data['balance']
    description = data['description']

    if not current_balance:
        current_balance = 0
    if not description:
        description = ""

    date = datetime.strptime(date, "%Y-%m-%d")
    category = Category(name=name,
                        created_at=date,
                        current_balance=current_balance,
                        description=description)
    user.add_category(category)
    storage.save()

    return jsonify({
        'success': True,
        'category': {
            'id': category.id,
            'name': category.name,
            'created_at': category.created_at,
            'transaction_count': category.transaction_count,
            'current_balance': category.current_balance,
            'description': category.description
        }
    })


@app.route('/api/v1/categories/<category_id>', methods=['DELETE'])
def category_delete(category_id):
    """ category delete """
    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'User not logged in'
        }), 401

    user = storage.get_object(User, session['user'])
    category = storage.get_object(Category, category_id)
    if category.user_id != user.id:
        return jsonify({
            'success': False,
            'message': 'Category does not belong to user'
        }), 401

    storage.delete(category)
    storage.save()

    return jsonify({
        'success': True,
        'message': 'Category deleted successfully'
    })


@app.route('/api/v1/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    """ a function to update category """

    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'User not logged in'
        }), 401

    user = storage.get_object(User, session['user'])
    category = storage.get_object(Category, category_id)
    if category.user_id != user.id:
        return jsonify({
            'success': False,
            'message': 'Category does not belong to user'
        }), 401

    data = request.get_json()
    category.name = data['name']
    category.current_balance = data['balance']
    category.description = data['description']
    category.created_at = datetime.strptime(data['date'], "%Y-%m-%d")
    storage.save()

    return jsonify({
        'success': True,
        'message': 'Category updated successfully',
        'category': {
            'id': category.id,
            'name': category.name,
            'created_at': category.created_at,
            'transaction_count': category.transaction_count,
            'current_balance': category.current_balance,
            'description': category.description
        }
    })

# Error handler for Method Not Allowed


@app.errorhandler(405)
def method_not_allowed(e):
    # You can return a custom message or JSON response
    return jsonify({'error': 'Method Not Allowed'}), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

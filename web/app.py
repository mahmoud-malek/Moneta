#!/usr/bin/python3

""" this is a module for the application,
it handles the routing process and serve dynamic content
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask import abort, flash
from models import storage
from models.user import User
from models.category import Category
from models.transaction import Transaction
import hashlib
import service
import secrets
import json
from datetime import datetime

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

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
    abort(404)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

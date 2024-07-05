#!/usr/bin/python3

""" this is a module for the application,
handles services needed """

from models import storage
from models.user import User
from models.category import Category
from models.transaction import Transaction


def check_email(email):
    """ check if email exists """
    all_users = storage.all(User).values()
    for user in all_users:
        if user.email == email:
            return True
    return False


def get_user(email, password):
    """ get user by email and password """
    all_users = storage.all(User).values()
    for user in all_users:
        if user.email == email and user.password == password:
            return user
    return None


def get_categoiries_for_user(user=None, id=None):
    """ get categories for user """
    if user is None and id is None:
        return []

    if user is None and id is not None:
        user = storage.get_object(User, id)
        return user.categories
    if user:
        return user.categories

    return []


def transactions_for_user(user=None, id=None):
    """ get transactions for user """
    if user is None and id is None:
        return []

    if user is None and id is not None:
        user = storage.get_object(User, id)
        return user.transactions
    if user:
        return user.transactions

    return []

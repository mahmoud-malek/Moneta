#!/usr/bin/python3

""" this is a module for the application,
handles services needed """

from decimal import Decimal
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


def to_dict(obj):
	"""Convert object to dictionary."""
	if obj is None or not isinstance(obj, (User, Category, Transaction)):
		return None

	# Create a copy of the dictionary items for safe iteration
	items_copy = list(obj.__dict__.items())
	for key, value in items_copy:
		if key.startswith('_'):
			# Modify the original dictionary, not the copy
			obj.__dict__.pop(key)
		elif key == 'created_at' or key == 'modified_at':
			obj.__dict__[key] = value.isoformat()
		elif isinstance(value, Decimal):
			# Convert Decimal to string for JSON serialization
			obj.__dict__[key] = str(value)
	return obj.__dict__

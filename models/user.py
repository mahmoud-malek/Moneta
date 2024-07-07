#!/usr/bin/python3

""" this is a user module that defines a user class """

from models.base import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy import DECIMAL
from sqlalchemy.orm import relationship
import models
from models.category import Category
from models.transaction import Transaction
from decimal import Decimal
known_classes = {'Category': Category, 'Transaction': Transaction}


class User(BaseModel, Base):
    """ the user class """

    __tablename__ = 'users'
    id = Column(String(36), primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(255), nullable=False)
    category_count = Column(Integer, default=0)
    transaction_count = Column(Integer, default=0)
    current_balance = Column(DECIMAL(15, 3), default=0.0)
    categories = relationship('Category',
                              backref='user',
                              cascade='all, delete')
    transactions = relationship('Transaction',
                                backref='user',
                                cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """ constructor method to initialize the user object """
        self.transaction_count = 0
        self.category_count = 0
        self.current_balance = 0.0
        super().__init__(*args, **kwargs)

    def add_category(self, category):
        """ adds a category to the user """

        if not isinstance(category, Category) or category in self.categories:
            return

        self.category_count += 1
        category.user_id = self.id
        self.categories.append(category)

    def delete_category(self, category):
        """ deletes a category from the user """

        # check validation of category
        try:
            if isinstance(category, str) and category in known_classes:
                category = known_classes[category]

            elif not isinstance(category, Category):
                return

            if category not in self.categories:
                return

            self.categories.remove(category)
            self.category_count -= 1
            self.current_balance -= category.current_balance
            self.transaction_count -= category.transaction_count
            category.delete_category()
        except Exception as e:
            return

    def add_transaction(self, transaction, category):
        """ a function that adds a transaction """

        if (not isinstance(transaction, Transaction)
            or not isinstance(category, Category)
            or category not in self.categories
                or transaction in self.transactions):
            return

        self.transaction_count += 1
        self.current_balance += Decimal(transaction.amount)
        transaction.user_id = self.id
        category.add_transaction(transaction)
        self.transactions.append(transaction)
        return transaction

    def delete_transaction(self, transaction):
        """ a function that deletes a transaction """

        if not isinstance(transaction,
                          Transaction) or transaction not in self.transactions:
            return None

        self.transactions.remove(transaction)
        transaction.category.delete_transaction(transaction)
        transaction.delete_transaction()
        self.transaction_count -= 1
        self.current_balance -= transaction.amount

    def update_balance(self, amount):
        """ a function that updates the user's balance """

        self.current_balance = amount
        return self

    def get_transactions(self):
        """ a function that returns all transactions of the user """

        return self.transactions

    def get_categories(self):
        """ a function that returns all categories of the user """

        return self.categories

    def get_transactions_by_category(self, category):
        """ a function that returns all transactions of
         the user by category """

        if not isinstance(category, Category):
            return None

        if category not in self.categories:
            return []

        return category.transactions

    def get_transactions_by_date(self, date):
        """ a function that returns all transactions of the user by date """

        transactions = self.transactions
        result = []
        for transaction in transactions:
            if transaction.created_at == date:
                result.append(transaction)
        return result

    def get_transactions_by_amount(self, amount):
        """ a function that returns all transactions of the user by amount """

        transactions = self.transactions
        result = []
        for transaction in transactions:
            if transaction.amount == amount:
                result.append(transaction)
        return result

    def update_user(self, **kwargs):
        """ a function that updates the user """

        if kwargs:
            for key, value in kwargs.items():
                if key in self.__dict__:
                    setattr(self, key, value)
            return self
        return None

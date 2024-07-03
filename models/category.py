#!/usr/bin/python3

""" this is a category module that defines a category class """

import models
from models.base import BaseModel, Base
from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from models.transaction import Transaction


class Category(BaseModel, Base):
    """ the category model represents the groups or
    categories the user will create to track and analyze
    """

    __tablename__ = 'categories'
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(255))
    transactions = relationship('Transaction',
                                backref='category',
                                cascade='all, delete-orphan')
    transaction_count = Column(Integer, default=0)
    current_balance = Column(DECIMAL(15, 3), default=0.0)

    def __init__(self, *args, **kwargs):
        """ constructor to initialize the category """
        self.transaction_count = 0
        self.current_balance = 0.0

        super().__init__(*args, **kwargs)

    def create_category(self, user_id, name, description):
        """ method to create a new category """
        self.user_id = user_id
        self.name = name
        self.description = description
        return self

    def add_transaction(self, transaction):
        """ adds a transaction to the category """
        if not isinstance(transaction,
                          Transaction) or transaction in self.transactions:
            return

        self.transaction_count += 1
        self.current_balance += transaction.amount
        transaction.category_id = self.id
        self.transactions.append(transaction)
        return transaction

    def delete_transaction(self, transaction):
        """ deletes a transaction from the category """
        if not isinstance(transaction, Transaction):
            return
        if transaction not in self.transactions:
            return
        self.transactions.remove(transaction)
        self.transaction_count -= 1
        self.current_balance -= transaction.amount

        return transaction

    def update_category(self, **kwargs):
        """ method to update the category """
        if kwargs:
            for key, value in kwargs.items():
                if key in self.__dict__:
                    setattr(self, key, value)
            return self
        return None

    def delete_category(self):
        """ method to delete the category """
        models.storage.delete(self)
        return self

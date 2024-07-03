#!/usr/bin/python3

""" this is a transaction module that defines a transaction class """

import models
from models.base import BaseModel, Base
from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship


class Transaction(BaseModel, Base):
    """ the transaction class """

    __tablename__ = 'transactions'
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    category_id = Column(String(36),
                         ForeignKey('categories.id'),
                         nullable=False)
    amount = Column(DECIMAL(15.3), nullable=False)
    description = Column(String(255))

    def __init__(self, *args, **kwargs):
        """ constractor method to initialize the transaction object """
        super().__init__(*args, **kwargs)

    def create_transaction(self, user_id, category_id, amount, description):
        """ method to create a new transaction """
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.description = description
        return self

    def delete_transaction(self):
        """ method to delete a transaction """
        # check if transaction exists
        if models.storage.get_object(Transaction, self.id):
            self.delete()
        return None

    def update_transaction(self, **kwargs):
        """ method to update a transaction """
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            return self
        return None

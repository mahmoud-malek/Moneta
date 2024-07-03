#!/usr/bin/python3

""" Unit tests for the transaction module """

import unittest
import models
from models.transaction import Transaction
from models.user import User
from models.category import Category


class TestTransaction(unittest.TestCase):
    """ Test the Transaction class """

    def setUp(self):
        """ Create a new transaction object """
        models.storage.reload()
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description='test transaction')
        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        u1.save()
        self.transaction = t1

    def tearDown(self):
        """ Tear down the test """
        models.storage.close()

    def test_transaction_instantiation(self):
        """ Test that the transaction object is correctly instantiated """
        self.assertIsInstance(self.transaction, Transaction)

    def test_transaction_attributes(self):
        """ Test that the transaction object has the required attributes """
        self.assertTrue(hasattr(self.transaction, 'user_id'))
        self.assertTrue(hasattr(self.transaction, 'category_id'))

    def test_create_transaction(self):
        """ Test the create_transaction """
        user = User()
        category = Category()
        user.name = 'John'
        user.email = 'jhonrr@ok.com'
        user.password = '123456'

        category.name = 'food'
        category.user_id = user.id

        self.transaction.user_id = user.id
        self.transaction.category_id = category.id
        self.transaction.amount = 100
        self.transaction.description = 'food shopping'

        self.assertEqual(self.transaction.amount, 100)
        self.assertEqual(self.transaction.description, 'food shopping')
        self.assertEqual(self.transaction.user_id, user.id)
        self.assertEqual(self.transaction.category_id, category.id)

    def test_delete_transaction(self):
        """ Test the delete_transaction method """
        self.transaction.delete_transaction()
        self.assertNotIn(self.transaction, models.storage.all().values())

    def test_update_transaction(self):
        """ Test the update_transaction method """
        self.transaction.amount = 100
        self.transaction.update_transaction(amount=200)
        self.assertEqual(self.transaction.amount, 200)
        self.transaction.update_transaction(description='new description')
        self.assertEqual(self.transaction.description, 'new description')
        self.transaction.update_transaction(user_id='123')
        self.assertEqual(self.transaction.user_id, '123')
        self.transaction.update_transaction(category_id='123')
        self.assertEqual(self.transaction.category_id, '123')

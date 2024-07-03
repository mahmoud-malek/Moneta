#!/usr/bin/python3

""" Unit tests for the category module """

import unittest
import models
from models.category import Category
from models.user import User
from models.transaction import Transaction


class TestCategory(unittest.TestCase):
    """ Test the Category class """

    def setUp(self):
        """ Create a new category object """
        models.storage.reload()
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description='test transaction')
        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        u1.save()
        self.category = c1

    def tearDown(self):
        """ Tear down the test """
        models.storage.close()

    def test_category_instantiation(self):
        """ Test that the category object is correctly instantiated """
        self.assertIsInstance(self.category, Category)

    def test_category_attributes(self):
        """ Test that the category object has the required attributes """
        self.assertTrue(hasattr(self.category, 'user_id'))
        self.assertTrue(hasattr(self.category, 'transactions'))
        self.assertTrue(hasattr(self.category, 'name'))

    def test_create_category(self):
        """ Test the create_category """
        user = User()
        user.name = 'John'
        user.email = 'anything'
        user.password = 'ok'
        self.category.name = 'food'
        self.category.user_id = user.id

        self.assertEqual(self.category.name, 'food')
        self.assertEqual(self.category.user_id, user.id)

    def test_delete_category(self):
        """ Test the delete_category """
        self.category.delete()
        self.assertNotIn(self.category, models.storage.all().values())

    def test_update_category(self):
        """ Test the update_category """
        self.category.name = 'food'
        self.category.update_category(name='drink')
        self.assertEqual(self.category.name, 'drink')
        self.category.update_category(name='food')
        self.assertEqual(self.category.name, 'food')

    def test_get_transactions(self):
        """ tests the get_transactions method of the category model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description='test transaction')

        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        self.assertEqual(c1.transactions, [t1])
        self.assertEqual(c1.transactions[0].amount, 1000)
        self.assertEqual(c1.transactions[0].description, 'test transaction')

    def test_get_user(self):
        """ tests the get_user method of the category model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description='test transaction')

        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        self.assertEqual(c1.user, u1)
        self.assertEqual(c1.user.name, 'mahmoud')
        self.assertEqual(c1.user.email, 'example.com')
        self.assertEqual(c1.user.password, 'pass')

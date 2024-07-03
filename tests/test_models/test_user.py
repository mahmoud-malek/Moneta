#!/usr/bin/python3

""" A module that defines test cases for user module """

import models
from models.user import User
from models.category import Category
from models.transaction import Transaction
import unittest
from datetime import datetime, timedelta


class TestUser(unittest.TestCase):
    """ a class that tests defferent features for the
            uesr """

    def setUp(self):
        """ sets up the test """
        models.storage.reload()
        usr = User(name='mahmoud', email='example.com', password='pass')
        cat = Category(name='food')
        trans = Transaction(amount=1000, description='test transaction')

    def tearDown(self):
        """ tears down the test """

        models.storage.close()

    def test_attributes(self):
        """ tests the attributes of the user model """
        u1 = User()
        u1.name = 'mahmoud malek'
        u1.email = 'eaxmolple@gmail.com'
        u1.password = 'pass'
        u1.category_count = 0
        u1.transaction_count = 0
        u1.current_balance = 0.0

        self.assertIsInstance(u1, User)
        self.assertIsNotNone(u1.id)
        self.assertEqual(u1.__class__.__name__, "User")
        self.assertIsInstance(u1.name, str)
        self.assertIsInstance(u1.email, str)
        self.assertIsInstance(u1.password, str)
        self.assertIsInstance(u1.categories, list)
        self.assertIsInstance(u1.transactions, list)
        self.assertIsInstance(u1.created_at, datetime)
        self.assertIsInstance(u1.modified_at, datetime)

    def test_save(self):
        """ tests the save method of the user model """
        u1 = User()
        u1.name = 'mahmoutd malek'
        u1.email = '02002e@gmail.com'
        u1.password = 'pakolklss'

        u1.save()
        self.assertTrue(isinstance(list(models.storage.all().values()), list))
        self.assertIn(u1, list(models.storage.all().values()))

    def test_delete(self):
        """ tests the delete method of the user model """
        u1 = User()
        u1.name = 'mahmoutd wmalek'
        u1.email = 'eaxm22le@gmail.com'
        u1.password = 'pass'
        u1.save()
        u1.delete()
        self.assertNotIn(u1, models.storage.all().values())

    def test_add_category(self):
        """ tests the add_category method of the user model """
        u1 = User()
        c1 = Category()
        u1.add_category(c1)
        self.assertIn(c1, u1.categories)

    def test_delete_category(self):
        """ tests the remove_category method of the user model """
        u1 = User()
        c1 = Category()
        u1.add_category(c1)
        u1.delete_category(c1)
        self.assertNotIn(c1, u1.categories)

    def test_add_transaction(self):
        """ tests the add_transaction method of the user model """
        u1 = User()
        u1.name = 'mahmoutd wmalek'
        u1.email = 'rwere@ok.com'
        u1.password = 'pass'

        c1 = Category(name='food')
        u1.add_category(c1)

        t1 = Transaction(amount=1000, description="test transaction")
        u1.add_transaction(t1, c1)

        self.assertIn(t1, u1.transactions)
        self.assertEqual(t1.user_id, u1.id)
        self.assertNotEqual(t1.category_id, None)

    def test_remove_transaction(self):
        """ tests the remove_transaction method of the user model """
        u1 = User()
        u1.name = 'mahmoutd wmalek'
        u1.email = 'rew@gmail.com'
        u1.password = 'pass'
        c1 = Category(name='food', user_id=u1.id)
        t1 = Transaction(amount=1000, description="test transaction")
        u1.add_transaction(t1, c1)
        models.storage.save()

        u1.delete_transaction(t1)
        self.assertNotIn(t1, u1.transactions)
        self.assertEqual(t1.user_id, None)

    def test_get_transactions(self):
        """ tests the get_transactions method of the user model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description='test transaction')

        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        self.assertIn(t1, u1.transactions)

    def test_get_categories(self):
        """ tests the get_categories method of the user model """
        u1 = User()
        c1 = Category()
        u1.add_category(c1)
        self.assertIn(c1, u1.categories)

    def test_get_transactions_by_category(self):
        """ tests the get_transactions_by_category method of the user model """
        u1 = User()
        c1 = Category()
        c2 = Category()
        t1 = Transaction(amount=1000, description="test transaction")
        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        self.assertIn(t1, u1.get_transactions_by_category(c1))
        self.assertNotIn(t1, u1.get_transactions_by_category(Category(c2)))

    def test_get_transactions_by_date(self):
        """ tests the get_transactions_by_date method of the user model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description='test transaction')

        u1.add_category(c1)
        u1.add_transaction(t1, c1)

        self.assertIn(t1, u1.get_transactions_by_date(t1.created_at))
        self.assertNotIn(t1, u1.get_transactions_by_date(datetime.now()))

    def test_get_transactions_by_amount(self):
        """ tests the get_transactions_by_amount method of the user model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description='test transaction')

        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        self.assertIn(t1, u1.get_transactions_by_amount(1000))
        self.assertNotIn(t1, u1.get_transactions_by_amount(2000))

    def test_get_balance(self):
        """ tests the get_balance method of the user model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description="test transaction")
        t2 = Transaction(amount=1000, description="test transaction")
        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        u1.add_transaction(t2, c1)
        self.assertEqual(u1.current_balance, 2000)

    def test_update_balance(self):
        """ tests the update_balance method of the user model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description="test transaction")
        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        u1.update_balance(1000)
        self.assertEqual(u1.current_balance, 1000)

    def test_update_user(self):
        """ tests the update_user method of the user model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        u1.update_user(name='mahmoud malek',
                       email='example.com',
                       password='pass')
        self.assertEqual(u1.name, 'mahmoud malek')
        self.assertEqual(u1.email, 'example.com')
        self.assertEqual(u1.password, 'pass')
        allowed_delta = timedelta(seconds=2)
        self.assertTrue(
            abs(datetime.utcnow() - u1.modified_at) < allowed_delta)
        self.assertNotEqual(u1.created_at, u1.modified_at)

    def test_balance_deleting(self):
        """ tests the balance deleting method of the user model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description="test transaction")
        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        u1.save()
        u1.delete_transaction(t1)
        self.assertEqual(u1.current_balance, 0)

    def test_user_deleting(self):
        """ tests the user deleting method of the user model """
        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food')
        t1 = Transaction(amount=1000, description="test transaction")
        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        u1.save()
        u1.delete()
        self.assertNotIn(u1, models.storage.all().values())
        self.assertNotIn(c1, models.storage.all().values())
        self.assertNotIn(t1, models.storage.all().values())

#!/usr/bin/python3

""" Unit tests for the db storage module """

import unittest
import models
from models.user import User
from models.category import Category
from models.transaction import Transaction
from time import sleep
from datetime import datetime


class TestDBStorage(unittest.TestCase):
    """ a class that tests the db storage """

    def setUp(self):
        """ sets up the test """

        # delete all data from the database
        for obj in models.storage.all(User).values():
            models.storage.delete(obj)

        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food', description='food category')
        t1 = Transaction(amount=1000, description='test transaction')
        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        u1.save()
        models.storage.save()

        # test that the objects were created successfully
        self.assertIn(u1, models.storage.all(User).values())
        self.assertIn(c1, models.storage.all(Category).values())
        self.assertIn(t1, models.storage.all(Transaction).values())

        self.user = u1
        self.category = c1
        self.transaction = t1

    def tearDown(self):
        """ tears down the test """
        models.storage.close()

    def test_get(self):
        """ Test the get method """
        self.assertEqual(models.storage.get_object(User, self.user.id),
                         self.user)
        self.assertEqual(models.storage.get_object(Category, self.category.id),
                         self.category)
        self.assertEqual(
            models.storage.get_object(Transaction, self.transaction.id),
            self.transaction)

    def test_count(self):
        """ Test the count method """
        self.assertEqual(models.storage.count(User), 1)
        self.assertEqual(models.storage.count(Category), 1)
        self.assertEqual(models.storage.count(Transaction), 1)

    def test_save(self):
        """ Test the save method """
        u2 = User(name='mahmoud', email='example.com', password='pass')
        c2 = Category(name='food', description='food category')
        t2 = Transaction(amount=1000, description='test transaction')
        u2.add_category(c2)
        u2.add_transaction(t2, c2)
        u2.save()
        self.assertEqual(models.storage.count(User), 2)
        self.assertEqual(models.storage.count(Category), 2)
        self.assertEqual(models.storage.count(Transaction), 2)
        self.assertIn(u2, models.storage.all(User).values())
        self.assertIn(c2, models.storage.all(Category).values())
        self.assertIn(t2, models.storage.all(Transaction).values())

    def test_reload(self):
        """ Test the reload method """
        self.user = self.user.id
        self.category = self.category.id
        self.transaction = self.transaction.id

        # important note: when reloading the database the attributes that were
        # refers to the objects will be lost, so we have to take the id of the
        # objects to be able to get them after reloading the database

        models.storage.reload()
        self.assertTrue(models.storage.get_object(User, self.user))
        self.assertTrue(models.storage.get_object(Category, self.category))
        self.assertTrue(
            models.storage.get_object(Transaction, self.transaction))

    def test_delete(self):
        """ Test the delete method """
        models.storage.delete(self.user)
        self.assertIsNone(models.storage.get_object(User, self.user.id))

        models.storage.delete(self.category)
        self.assertIsNone(models.storage.get_object(Category,
                                                    self.category.id))

        models.storage.delete(self.transaction)
        self.assertIsNone(
            models.storage.get_object(Transaction, self.transaction.id))

    def test_mine(self):
        """ this test is complicated, it tests the relationship between the
                user, category, and transaction objects """

        u1 = User(name='mahmoud', email='example.com', password='pass')
        c1 = Category(name='food', description='food category')
        c2 = Category(name='transport', description='transport category')

        t1 = Transaction(amount=1000, description='test transaction')
        t2 = Transaction(amount=2000, description='test transaction 2')
        t3 = Transaction(amount=3000, description='test transaction 3')
        t4 = Transaction(amount=-4000, description='test transaction 4')

        u1.add_category(c1)

        self.assertTrue(u1.categories == [c1])
        self.assertFalse(u1.transaction_count == 4)
        self.assertTrue(u1.transaction_count == 0)
        self.assertTrue(u1.category_count == 1)
        self.assertTrue(u1.current_balance == 0.0)
        self.assertTrue(c1.user_id == u1.id)
        self.assertTrue(c1.user == u1)
        self.assertTrue(c1.transactions == [])
        u1.add_transaction(t1, c1)
        u1.add_transaction(t2, c1)

        self.assertTrue(u1.transaction_count == 2)
        self.assertTrue(u1.current_balance == 3000.0)
        self.assertTrue(c1.transactions == [t1, t2])
        self.assertTrue(t1.category == c1)
        self.assertTrue(t2.category == c1)
        self.assertTrue(t1.user == u1)
        self.assertTrue(t2.user == u1)
        self.assertTrue(c1.transaction_count == 2)
        self.assertTrue(u1.transaction_count == 2)
        self.assertTrue(c1.current_balance == 3000.0)
        self.assertTrue(t1.category == c1)
        self.assertTrue(t2.category == c1)

        u1.add_category(c2)
        self.assertTrue(u1.category_count == 2)
        self.assertTrue(c2.user_id == u1.id)
        self.assertTrue(c2.user == u1)
        self.assertTrue(c2.transactions == [])
        self.assertTrue(c2.transaction_count == 0)
        self.assertTrue(c2.current_balance == 0.0)

        u1.add_transaction(t3, c2)
        u1.add_transaction(t4, c2)

        self.assertTrue(u1.transaction_count == 4)
        self.assertTrue(u1.current_balance == 2000.0)
        self.assertTrue(c2.transactions == [t3, t4])
        self.assertTrue(t3.category == c2)
        self.assertTrue(t4.category == c2)
        self.assertTrue(t3.user == u1)
        self.assertTrue(t4.user == u1)
        self.assertTrue(c2.transaction_count == 2)
        self.assertTrue(u1.transaction_count == 4)
        self.assertTrue(c2.current_balance == -1000.0)

        u1.delete_transaction(t1)
        self.assertTrue(u1.transaction_count == 3)
        self.assertTrue(u1.current_balance == 1000.0)
        self.assertTrue(c1.transactions == [t2])
        self.assertTrue(t1.category is None)
        self.assertTrue(t1.user is None)
        self.assertTrue(c1.transaction_count == 1)
        self.assertTrue(u1.transaction_count == 3)
        self.assertTrue(c1.current_balance == 2000.0)
        self.assertTrue(t1.category is None)
        self.assertTrue(t2.category == c1)
        self.assertTrue(t2.user == u1)

        u1.delete_transaction(t2)
        self.assertTrue(u1.transaction_count == 2)
        self.assertTrue(c1.transactions == [])
        self.assertTrue(t1.category is None)
        self.assertTrue(t1.user is None)
        self.assertTrue(u1.current_balance == -1000.0)
        self.assertTrue(c1.transaction_count == 0)
        self.assertTrue(u1.transaction_count == 2)
        self.assertTrue(c1.current_balance == 0.0)
        self.assertTrue(t1.category is None)
        self.assertTrue(t2.category is None)
        self.assertTrue(t2.user is None)

        u1.delete_category(c1)
        self.assertTrue(u1.category_count == 1)
        self.assertTrue(c1.user is None)
        self.assertTrue(c1.transactions == [])
        self.assertTrue(c1.transaction_count == 0)
        self.assertTrue(c1.current_balance == 0.0)
        self.assertTrue(u1.transaction_count == 2)
        self.assertTrue(u1.current_balance == -1000.0)
        self.assertTrue(t1.category is None)
        self.assertTrue(t2.category is None)
        self.assertTrue(t2.user is None)

        u1.delete_category(c2)
        self.assertTrue(u1.category_count == 0)
        self.assertTrue(c2.user is None)
        self.assertTrue(u1.transaction_count == 0)
        self.assertTrue(u1.current_balance == 0.0)
        self.assertTrue(t1.category is None)
        self.assertTrue(t2.category is None)
        self.assertTrue(t2.user is None)

        u1.add_category(c1)
        u1.add_transaction(t1, c1)
        self.assertIn(t1, u1.get_transactions_by_category(c1))
        self.assertNotIn(t1, u1.get_transactions_by_category(Category(c2)))
        self.assertIn(t1, u1.get_transactions_by_date(t1.created_at))
        sleep(0.005)
        self.assertNotIn(t1, u1.get_transactions_by_date(datetime.now()))
        self.assertIn(t1, u1.get_transactions_by_amount(1000))
        self.assertNotIn(t1, u1.get_transactions_by_amount(2000))
        self.assertEqual(u1.current_balance, 1000)

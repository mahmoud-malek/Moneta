#!/usr/bin/python3
""" Unittest for base model """

import unittest
from models.base import BaseModel


class test_base(unittest.TestCase):
    """ Testing the base model to ensure it is working
        properly """

    def test_create_instance(self):
        m1 = BaseModel()
        self.assertTrue(isinstance(m1, BaseModel))

    def test_string_representation(self):
        m1 = BaseModel()
        self.assertEqual(str(m1),
                         "[BaseModel] ({}) {}".format(m1.id, m1.__dict__))

    def test_created_at(self):
        m1 = BaseModel()
        self.assertIsNotNone(m1.created_at)

    def test_modified_at(self):
        m1 = BaseModel()
        self.assertIsNotNone(m1.modified_at)

    def test_id(self):
        m1 = BaseModel()
        self.assertIsNotNone(m1.id)

    def test_kwargs(self):
        # it should not set the attribute if it is not in the class
        m1 = BaseModel(name='John')
        self.assertFalse(hasattr(m1, 'name'))

        # it should set the attribute if it is in the class
        m1 = BaseModel(id='123')
        self.assertEqual(m1.id, '123')

        m1 = BaseModel(created_at='2020-06-29T15:27:48.276722')
        self.assertEqual(str(m1.created_at), '2020-06-29 15:27:48.276722')
        self.assertNotEqual(str(m1.modified_at), str(m1.created_at))

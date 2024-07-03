#!/usr/bin/python3

""" defines the db class """

import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base
from models import user, category, transaction
import os

known_classes = {
    'User': user.User,
    'Category': category.Category,
    'Transaction': transaction.Transaction}


class DBStorage:
    """ a class to interact wtih mysql databaes """

    __engine = None
    __session = None

    def __init__(self):
        """ creates the session with mysql database """
        user = os.getenv('MONETA_MYSQL_USER')
        password = os.getenv('MONETA_MYSQL_PWD')
        host = os.getenv('MONETA_MYSQL_HOST')
        database = os.getenv('MONETA_MYSQL_DB')
        DB_URL = (f'mysql+mysqldb://{user}:{password}@{host}/{database}')

        self.__engine = create_engine(DB_URL, pool_pre_ping=True)

    def all(self, target=None):
        """ qury all records for all or specific class """
        objects = None
        result = {}

        if target is None:
            objects = list()
            for cls in known_classes.values():
                for obj in self.__session.query(cls).all():
                    objects.append(obj)

        elif not isinstance(target, str):
            target = target.__name__
            target = target.lower().capitalize()

            if target in known_classes:
                objects = self.__session.query(known_classes[target]).all()
            else:
                return None

        if objects:
            result = self.convert_to_dic(objects)
        return result

    def reload(self):
        """ this is a method to reload all the data
        from the database and creates a session for usage later
         """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session

    def close(self):
        """ terminate the session """
        self.__session.remove()

    def save(self):
        """ a method to save the current session """
        self.__session.commit()

    def delete(self, target=None):
        """A method to delete a target object from the database."""
        if target is not None:
            self.__session.delete(target)
            self.save()

    def add(self, obj=None):
        """ a method to add an object to the current session """
        if obj is not None:
            self.__session.add(obj)

    def get_object(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        id = str(id)
        if cls and id:
            objects = self.all(cls)
            for obj in objects.values():
                if obj.id == id:
                    return obj
        return None

    def count(self, cls=None):
        """ count the number of objects in the database """
        objects = self.all(cls)
        return len(objects)

    def convert_to_dic(self, objects):
        """ convert the object to dictionary """
        if objects:
            if isinstance(objects, list):
                result = {}
                for obj in objects:
                    key = obj.__class__.__name__ + '.' + obj.id
                    result[key] = obj
                return result
        return None

    def refresh(self, obj):
        """ refresh the object """
        self.__session.refresh(obj)
        return obj

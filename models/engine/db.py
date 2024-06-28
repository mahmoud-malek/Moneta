#!/usr/bin/python3

""" defines the db class """

import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base
import os

known_classes = ['user', 'category', 'transcation']


class DBStorage:
    """ a class to interact wtih mysql databaes """

    __engine = None
    __session = None

    def __init__(self):
        """ creates the session with mysql database """
        MONETA_MYSQL_USER = os.getenv('MONETA_MYSQL_USER')
        MONETA_MYSQL_PWD = os.getenv('MONETA_MYSQL_PWD')
        MONETA_MYSQL_HOST = os.getenv('MONETA_MYSQL_HOST')
        MONETA_MYSQL_DB = os.getenv('MONETA_MYSQL_DB')

        DB_URL = "mysql+mysqldb://{}:{}@{}/{}".format(MONETA_MYSQL_USER,
                                                      MONETA_MYSQL_PWD,
                                                      MONETA_MYSQL_HOST)

        self.__engine = create_engine(DB_URL)

    def get_all(self, target=None):
        """ qury all records for all or specific class """
        records = {}
        data = {}
        if str(target) in known_classes:
            data = self.__session.query(str(target)).all()

    def reload(self):
        """ this is a method to reload all the data
                from the database and creates a session for usage later
                """
        Base.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session

    def close(self):
        """ terminate the session """
        self.__session.remove()

        def delete(self, target):
            """ a method to delete a target object from database """
            if target is not None and str(target) in known_classes:
                self.__session.delete(target)

        def find(self, target, id)
        """ this method searches for a target object
            in mysql database
            """

        data = self

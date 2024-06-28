#!/usr/bin/python3

""" defines a base for all models in Moneta project """

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
import models

Base = declarative_base()
time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """ defines the base model for all other models """

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """ constructor to initialize the models """

        if kwargs:
            for key, value in kwargs.items():
                self.__setattr__(key, value)

            # check for created_date
            if kwargs.get('created_at', None) and isinstance(
                    self.created_at, str):
                self.created_at = datetime.strptime(kwargs['created_at'], time)
            else:
                self.created_at = datetime.utcnow()

            # check for modified date
            if kwargs.get('modified_at', None) and isinstance(
                    self.modified_at, str):
                self.modified_at = datetime.strptime(kwargs['modified_at'],
                                                     time)
            else:
                self.modified_at = datetime.utcnow()

            # check for id
            if kwargs.get('id', None) is None:
                self.id = str(uuid.uuid4())

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.modified_at = datetime.utcnow()

    def __str__(self):
        """ string representation of BaseModel """
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def delete(self):
        """ deletes the object from the databse """
        models.storage.delete(self)

    def save(self):
        """ saves the object to mysql database """
        self.modified_at = datetime.utcnow
        models.storage.new(self)
        models.storage.save()
